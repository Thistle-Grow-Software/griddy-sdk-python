"""Base SDK class and endpoint configuration dataclasses used by all SDK endpoints."""

from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
)
from urllib.parse import parse_qs, urlparse

import httpx

from griddy.core import utils
from griddy.core._constants import (
    CLIENT_ERROR_PREFIX,
    DEFAULT_RETRY_STATUS_CODES,
    HTTP_OK,
    SERVER_ERROR_PREFIX,
)
from griddy.core.hooks import (
    AfterErrorContext,
    AfterSuccessContext,
    BeforeRequestContext,
)
from griddy.core.hooks.types import HookContext
from griddy.core.types import UNSET, OptionalNullable
from griddy.core.utils import RetryConfig, SerializedRequestBody, get_body_content
from griddy.core.utils.unmarshal_json_response import unmarshal_json_response

T = TypeVar("T")

_UNRESOLVED = object()

# TypeVar for provider-specific SDKConfiguration subclasses.
# Bound to the base SDKConfiguration so subclasses get full type safety.
from griddy.core.sdkconfiguration import SDKConfiguration as BaseSDKConfig

T_Config = TypeVar("T_Config", bound=BaseSDKConfig)


@dataclass
class BaseEndpointConfig:
    """Shared fields for all endpoint configurations (NFL, PFR, etc.)."""

    operation_id: str
    response_type: Type[T]
    timeout_ms: Optional[int] = None


@dataclass
class EndpointConfig(BaseEndpointConfig):
    """Configuration for an API endpoint, enabling sync/async factory pattern.

    This dataclass captures all the configuration needed to execute an endpoint,
    allowing a single definition to generate both sync and async implementations.
    """

    # HTTP method and path
    method: str = ""
    path: str = ""

    # Request model instance (already constructed with parameters)
    request: Any = None

    # Response configuration
    error_status_codes: List[str] = field(default_factory=list)

    # Request configuration flags
    request_body_required: bool = False
    request_has_path_params: bool = False
    request_has_query_params: bool = True

    # Optional overrides
    server_url: Optional[str] = None
    http_headers: Optional[Mapping[str, str]] = None
    retries: Any = field(default_factory=lambda: UNSET)  # OptionalNullable[RetryConfig]

    # For endpoints that need raw JSON (due to Pydantic model issues)
    return_raw_json: bool = False

    # Optional body serializer
    get_serialized_body: Optional[Callable[[], Optional[SerializedRequestBody]]] = None

    # Standard headers (rarely need to change)
    user_agent_header: str = "user-agent"
    accept_header_value: str = "application/json"


class BaseSDK(Generic[T_Config]):
    """Base class for all SDK endpoint classes, providing HTTP request building, hook lifecycle, and retry logic."""

    sdk_configuration: T_Config
    parent_ref: Optional[object] = None

    # Subclasses override these to inject provider-specific error/model classes.
    # Using properties allows lazy loading of error modules.
    @property
    def _default_error_cls(self) -> Type[Exception]:
        """Return the default error class for failed API responses."""
        from griddy.core.errors import DefaultSDKError

        return DefaultSDKError

    @property
    def _no_response_error_cls(self) -> Type[Exception]:
        """Return the error class for missing server responses."""
        from griddy.core.errors import NoResponseError

        return NoResponseError

    @property
    def _security_model_cls(self) -> Any:
        """Return the Pydantic security model class, or None."""
        return None

    @property
    def _security_env_mapping(self) -> Optional[Dict[str, str]]:
        """Mapping of security field names to environment variable names."""
        return None

    def __init__(
        self,
        sdk_config: T_Config,
        parent_ref: Optional[object] = None,
    ) -> None:
        """Initialize the SDK with configuration and an optional parent reference."""
        self.sdk_configuration = sdk_config
        self.parent_ref = parent_ref
        self._cached_env_security = _UNRESOLVED

    def _get_url(
        self, base_url: Optional[str], url_variables: Optional[Dict[str, str]]
    ) -> str:
        """Resolve the full base URL from config, applying template variables."""
        sdk_url, sdk_variables = self.sdk_configuration.get_server_details()

        if base_url is None:
            base_url = sdk_url

        if url_variables is None:
            url_variables = sdk_variables

        return utils.template_url(base_url, url_variables)

    def _resolve_base_url(
        self,
        server_url: Optional[str] = None,
        url_variables: Optional[Dict[str, str]] = None,
    ) -> str:
        """Return the server URL override if set, otherwise resolve from config."""
        if server_url is not None:
            return server_url
        return self._get_url(None, url_variables)

    def _resolve_timeout(self, timeout_ms: Optional[int] = None) -> Optional[int]:
        """Return the explicit timeout or fall back to the configured default."""
        if timeout_ms is None:
            return self.sdk_configuration.timeout_ms
        return timeout_ms

    def _resolve_retry_config(
        self,
        retries: OptionalNullable[RetryConfig],
        retry_status_codes: Optional[List[str]] = None,
    ) -> Optional[Tuple[RetryConfig, List[str]]]:
        """Resolve retry configuration from explicit value or SDK config default."""
        if retry_status_codes is None:
            retry_status_codes = list(DEFAULT_RETRY_STATUS_CODES)

        if retries == UNSET:
            if self.sdk_configuration.retry_config is not UNSET:
                retries = self.sdk_configuration.retry_config

        if isinstance(retries, RetryConfig):
            return (retries, retry_status_codes)
        return None

    def _get_security_from_env(self, security: Any) -> Any:
        """Resolve security from env vars. Subclasses can override."""
        security_cls = self._security_model_cls
        if security_cls is None:
            return security
        env_mapping = self._security_env_mapping
        from griddy.core.utils.security import get_security_from_env

        return get_security_from_env(security, security_cls, env_mapping)

    def _resolve_security_source(self) -> Any:
        """Return the security source, caching env var resolution.

        When ``sdk_configuration.security`` is set (e.g. by a hook), it is
        returned directly.  Otherwise the result of ``_get_security_from_env``
        is cached so that environment variables are only read once per SDK
        instance.
        """
        security = self.sdk_configuration.security
        if security is not None:
            return security
        if self._cached_env_security is not _UNRESOLVED:
            return self._cached_env_security
        resolved = self._get_security_from_env(None)
        self._cached_env_security = resolved
        return resolved

    def _create_hook_context(
        self,
        operation_id: str,
        base_url: str,
    ) -> HookContext:
        """Create a HookContext for the given operation and base URL."""
        return HookContext(
            config=self.sdk_configuration,
            base_url=base_url or "",
            operation_id=operation_id,
            oauth2_scopes=[],
            security_source=self._resolve_security_source(),
        )

    def _process_json_error_response(
        self,
        http_res: httpx.Response,
        error_status_codes: List[str],
        stream_to_text: Callable[[httpx.Response], str],
    ) -> None:
        """Raise the appropriate SDK error for a non-success JSON response."""
        client_errors = [
            code for code in error_status_codes if code.startswith(CLIENT_ERROR_PREFIX)
        ]
        if client_errors and utils.match_response(http_res, client_errors, "*"):
            http_res_text = stream_to_text(http_res)
            raise self._default_error_cls("API error occurred", http_res, http_res_text)

        server_errors = [
            code for code in error_status_codes if code.startswith(SERVER_ERROR_PREFIX)
        ]
        if server_errors and utils.match_response(http_res, server_errors, "*"):
            http_res_text = stream_to_text(http_res)
            raise self._default_error_cls("API error occurred", http_res, http_res_text)

        raise self._default_error_cls("Unexpected response received", http_res)

    def _handle_json_response(
        self,
        http_res: httpx.Response,
        response_type: Type[T],
        error_status_codes: List[str],
    ) -> T:
        """Unmarshal a successful JSON response or raise on error status codes.

        On a 2XX ``application/json`` response, deserialises the body into
        ``response_type`` via ``unmarshal_json_response``. Otherwise delegates
        to ``_process_json_error_response`` which raises the appropriate SDK
        error.

        Args:
            http_res: The raw ``httpx.Response``.
            response_type: The Pydantic model (or type) to deserialise into.
            error_status_codes: Status code patterns that indicate an error.

        Returns:
            An instance of ``response_type`` on success.

        Raises:
            DefaultSDKError: When the response matches an error status code.
        """
        if utils.match_response(http_res, HTTP_OK, "application/json"):
            return unmarshal_json_response(response_type, http_res)

        self._process_json_error_response(
            http_res, error_status_codes, utils.stream_to_text
        )

    async def _handle_json_response_async(
        self,
        http_res: httpx.Response,
        response_type: Type[T],
        error_status_codes: List[str],
    ) -> T:
        """Async variant of :meth:`_handle_json_response`.

        Identical behaviour except the error-path response body is read
        asynchronously via ``stream_to_text_async``.
        """
        if utils.match_response(http_res, HTTP_OK, "application/json"):
            return unmarshal_json_response(response_type, http_res)

        http_res_text = await utils.stream_to_text_async(http_res)
        self._process_json_error_response(
            http_res, error_status_codes, lambda _: http_res_text
        )

    def _execute_endpoint(self, config: EndpointConfig) -> T:
        """Execute a sync API request using the given endpoint configuration."""
        base_url = self._resolve_base_url(config.server_url)
        timeout_ms = self._resolve_timeout(config.timeout_ms)

        req = self._build_request(
            method=config.method,
            path=config.path,
            base_url=base_url,
            url_variables=None,
            request=config.request,
            request_body_required=config.request_body_required,
            request_has_path_params=config.request_has_path_params,
            request_has_query_params=config.request_has_query_params,
            user_agent_header=config.user_agent_header,
            accept_header_value=config.accept_header_value,
            http_headers=config.http_headers,
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
            get_serialized_body=config.get_serialized_body,
        )

        retry_config = self._resolve_retry_config(config.retries)
        http_res = self.do_request(
            hook_ctx=self._create_hook_context(config.operation_id, base_url),
            request=req,
            error_status_codes=config.error_status_codes,
            retry_config=retry_config,
        )

        if config.return_raw_json:
            if utils.match_response(http_res, HTTP_OK, "application/json"):
                return http_res.json()

        return self._handle_json_response(
            http_res, config.response_type, config.error_status_codes
        )

    async def _execute_endpoint_async(self, config: EndpointConfig) -> T:
        """Execute an async API request using the given endpoint configuration."""
        base_url = self._resolve_base_url(config.server_url)
        timeout_ms = self._resolve_timeout(config.timeout_ms)

        req = self._build_request_async(
            method=config.method,
            path=config.path,
            base_url=base_url,
            url_variables=None,
            request=config.request,
            request_body_required=config.request_body_required,
            request_has_path_params=config.request_has_path_params,
            request_has_query_params=config.request_has_query_params,
            user_agent_header=config.user_agent_header,
            accept_header_value=config.accept_header_value,
            http_headers=config.http_headers,
            security=self.sdk_configuration.security,
            timeout_ms=timeout_ms,
            get_serialized_body=config.get_serialized_body,
        )

        retry_config = self._resolve_retry_config(config.retries)

        http_res = await self.do_request_async(
            hook_ctx=self._create_hook_context(config.operation_id, base_url),
            request=req,
            error_status_codes=config.error_status_codes,
            retry_config=retry_config,
        )

        if config.return_raw_json:
            if utils.match_response(http_res, HTTP_OK, "application/json"):
                return http_res.json()

        return await self._handle_json_response_async(
            http_res, config.response_type, config.error_status_codes
        )

    def _build_request_async(
        self,
        method: str,
        path: str,
        base_url: Optional[str],
        url_variables: Optional[Dict[str, str]],
        request: Any,
        request_body_required: bool,
        request_has_path_params: bool,
        request_has_query_params: bool,
        user_agent_header: str,
        accept_header_value: str,
        _globals: Optional[Any] = None,
        security: Any = None,
        timeout_ms: Optional[int] = None,
        get_serialized_body: Optional[
            Callable[[], Optional[SerializedRequestBody]]
        ] = None,
        url_override: Optional[str] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> httpx.Request:
        """Build an httpx.Request using the async client."""
        client = self.sdk_configuration.async_client
        return self._build_request_with_client(
            client,
            method,
            path,
            base_url,
            url_variables,
            request,
            request_body_required,
            request_has_path_params,
            request_has_query_params,
            user_agent_header,
            accept_header_value,
            _globals,
            security,
            timeout_ms,
            get_serialized_body,
            url_override,
            http_headers,
        )

    def _build_request(
        self,
        method: str,
        path: str,
        base_url: Optional[str],
        url_variables: Optional[Dict[str, str]],
        request: Any,
        request_body_required: bool,
        request_has_path_params: bool,
        request_has_query_params: bool,
        user_agent_header: str,
        accept_header_value: str,
        _globals: Optional[Any] = None,
        security: Any = None,
        timeout_ms: Optional[int] = None,
        get_serialized_body: Optional[
            Callable[[], Optional[SerializedRequestBody]]
        ] = None,
        url_override: Optional[str] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> httpx.Request:
        """Build an httpx.Request using the sync client."""
        client = self.sdk_configuration.client
        return self._build_request_with_client(
            client,
            method,
            path,
            base_url,
            url_variables,
            request,
            request_body_required,
            request_has_path_params,
            request_has_query_params,
            user_agent_header,
            accept_header_value,
            _globals,
            security,
            timeout_ms,
            get_serialized_body,
            url_override,
            http_headers,
        )

    def _build_request_with_client(
        self,
        client: Any,
        method: str,
        path: str,
        base_url: Optional[str],
        url_variables: Optional[Dict[str, str]],
        request: Any,
        request_body_required: bool,
        request_has_path_params: bool,
        request_has_query_params: bool,
        user_agent_header: str,
        accept_header_value: str,
        _globals: Optional[Any] = None,
        security: Any = None,
        timeout_ms: Optional[int] = None,
        get_serialized_body: Optional[
            Callable[[], Optional[SerializedRequestBody]]
        ] = None,
        url_override: Optional[str] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> httpx.Request:
        """Build an ``httpx.Request`` from endpoint configuration.

        Assembles the full URL (with path and query parameters), resolves
        security credentials, serializes the request body, and merges all
        headers before delegating to ``client.build_request()``.

        Args:
            client: The ``httpx.Client`` or ``httpx.AsyncClient`` used to
                build the request object.
            method: HTTP method (e.g. ``"GET"``, ``"POST"``).
            path: URL path template (e.g. ``"/v1/games/{gameId}"``).
            base_url: Base server URL resolved from ``SDKConfiguration``.
            url_variables: Optional template variables for the base URL.
            request: Pydantic request model containing path/query parameters.
            request_body_required: If ``True``, raise ``ValueError`` when the
                serialized body is ``None``.
            request_has_path_params: Whether ``request`` contains path params
                to interpolate into ``path``.
            request_has_query_params: Whether ``request`` contains query
                params to append to the URL.
            user_agent_header: Header name for the user-agent string.
            accept_header_value: Value for the ``Accept`` header.
            _globals: Optional global parameter overrides.
            security: Security credentials (model instance, callable, or
                ``None`` to resolve from env/config).
            timeout_ms: Request timeout in milliseconds, converted to seconds
                for httpx.
            get_serialized_body: Optional callable returning a
                ``SerializedRequestBody`` for POST/PUT requests.
            url_override: If provided, skip URL generation and use this URL
                directly (query params are parsed from it).
            http_headers: Extra headers that override all others.

        Returns:
            A fully constructed ``httpx.Request`` ready for sending.

        Raises:
            ValueError: If ``request_body_required`` is ``True`` and the
                serialized body is ``None``.
        """
        query_params = {}

        url = url_override
        if url is None:
            url = utils.generate_url(
                self._get_url(base_url, url_variables),
                path,
                request if request_has_path_params else None,
                _globals if request_has_path_params else None,
            )

            query_params = utils.get_query_params(
                request if request_has_query_params else None,
                _globals if request_has_query_params else None,
            )
        else:
            parsed_override = urlparse(str(url_override))
            query_params = parse_qs(parsed_override.query, keep_blank_values=True)

        headers = utils.get_headers(request, _globals)
        headers["Accept"] = accept_header_value
        headers[user_agent_header] = self.sdk_configuration.user_agent

        if security is not None:
            if callable(security):
                security = security()
        if security is None:
            security = self._resolve_security_source()
        if security is not None:
            security_headers, security_query_params = utils.get_security(security)
            headers = {**headers, **security_headers}
            query_params = {**query_params, **security_query_params}

        serialized_request_body = SerializedRequestBody()
        if get_serialized_body is not None:
            rb = get_serialized_body()
            if request_body_required and rb is None:
                raise ValueError("request body is required")

            if rb is not None:
                serialized_request_body = rb

        if (
            serialized_request_body.media_type is not None
            and serialized_request_body.media_type
            not in (
                "multipart/form-data",
                "multipart/mixed",
            )
        ):
            headers["content-type"] = serialized_request_body.media_type

        if http_headers is not None:
            for header, value in http_headers.items():
                headers[header] = value

        timeout = timeout_ms / 1000 if timeout_ms is not None else None

        return client.build_request(
            method,
            url,
            params=query_params,
            content=serialized_request_body.content,
            data=serialized_request_body.data,
            files=serialized_request_body.files,
            headers=headers,
            timeout=timeout,
        )

    def do_request(
        self,
        hook_ctx: HookContext,
        request: httpx.Request,
        error_status_codes: List[str],
        stream: bool = False,
        retry_config: Optional[Tuple[RetryConfig, List[str]]] = None,
    ) -> httpx.Response:
        """Send an HTTP request through the hook lifecycle with optional retries.

        Executes the full request pipeline: ``before_request`` hook, HTTP send
        via the sync client, error handling with ``after_error`` hook, and
        finally the ``after_success`` hook. When ``retry_config`` is provided,
        the entire pipeline is wrapped in a retry loop that re-attempts on
        matching status codes.

        Args:
            hook_ctx: ``HookContext`` passed to each lifecycle hook, carrying
                the operation ID, base URL, and security source.
            request: The ``httpx.Request`` to send.
            error_status_codes: Status code patterns (e.g. ``["4XX", "5XX"]``)
                that should trigger the ``after_error`` hook.
            stream: If ``True``, the response body is streamed rather than
                read immediately.
            retry_config: Optional tuple of ``(RetryConfig, status_codes)``
                controlling automatic retries on transient failures.

        Returns:
            The ``httpx.Response`` (possibly modified by hooks).

        Raises:
            NoResponseError: If the server returns no response.
            DefaultSDKError: If an error status code is matched and the
                ``after_error`` hook does not recover.
        """
        client = self.sdk_configuration.client
        logger = self.sdk_configuration.debug_logger

        hooks = self.sdk_configuration.hooks

        def do():
            http_res = None
            try:
                req = hooks.before_request(BeforeRequestContext(hook_ctx), request)
                logger.debug(
                    "Request:\nMethod: %s\nURL: %s\nHeaders: %s\nBody: %s",
                    req.method,
                    req.url,
                    req.headers,
                    get_body_content(req),
                )

                if client is None:
                    raise ValueError("client is required")

                http_res = client.send(req, stream=stream)
            except Exception as e:
                original_error = e
                _, e = hooks.after_error(AfterErrorContext(hook_ctx), None, e)
                if e is not None:
                    logger.debug("Request Exception", exc_info=True)
                    raise e
                logger.warning(
                    "after_error hook discarded error without providing "
                    "a replacement response or error. "
                    "Re-raising original error: %s",
                    original_error,
                )
                raise original_error

            if http_res is None:
                logger.debug("Raising no response SDK error")
                raise self._no_response_error_cls("No response received")

            logger.debug(
                "Response:\nStatus Code: %s\nURL: %s\nHeaders: %s\nBody: %s",
                http_res.status_code,
                http_res.url,
                http_res.headers,
                "<streaming response>" if stream else http_res.text,
            )

            if utils.match_status_codes(error_status_codes, http_res.status_code):
                result, err = hooks.after_error(
                    AfterErrorContext(hook_ctx), http_res, None
                )
                if err is not None:
                    logger.debug("Request Exception", exc_info=True)
                    raise err
                if result is not None:
                    http_res = result
                else:
                    logger.debug("Raising unexpected SDK error")
                    raise self._default_error_cls("Unexpected error occurred", http_res)

            return http_res

        if retry_config is not None:
            http_res = utils.retry(do, utils.Retries(retry_config[0], retry_config[1]))
        else:
            http_res = do()

        if not utils.match_status_codes(error_status_codes, http_res.status_code):
            http_res = hooks.after_success(AfterSuccessContext(hook_ctx), http_res)

        return http_res

    async def do_request_async(
        self,
        hook_ctx: HookContext,
        request: httpx.Request,
        error_status_codes: List[str],
        stream: bool = False,
        retry_config: Optional[Tuple[RetryConfig, List[str]]] = None,
    ) -> httpx.Response:
        """Async variant of :meth:`do_request`.

        Runs the same hook lifecycle (``before_request`` → send →
        ``after_error`` / ``after_success``) using the async HTTP client.
        See :meth:`do_request` for full parameter and behaviour details.
        """
        client = self.sdk_configuration.async_client
        logger = self.sdk_configuration.debug_logger

        hooks = self.sdk_configuration.hooks

        async def do():
            http_res = None
            try:
                req = hooks.before_request(BeforeRequestContext(hook_ctx), request)
                logger.debug(
                    "Request:\nMethod: %s\nURL: %s\nHeaders: %s\nBody: %s",
                    req.method,
                    req.url,
                    req.headers,
                    get_body_content(req),
                )

                if client is None:
                    raise ValueError("client is required")

                http_res = await client.send(req, stream=stream)
            except Exception as e:
                original_error = e
                _, e = hooks.after_error(AfterErrorContext(hook_ctx), None, e)
                if e is not None:
                    logger.debug("Request Exception", exc_info=True)
                    raise e
                logger.warning(
                    "after_error hook discarded error without providing "
                    "a replacement response or error. "
                    "Re-raising original error: %s",
                    original_error,
                )
                raise original_error

            if http_res is None:
                logger.debug("Raising no response SDK error")
                raise self._no_response_error_cls("No response received")

            logger.debug(
                "Response:\nStatus Code: %s\nURL: %s\nHeaders: %s\nBody: %s",
                http_res.status_code,
                http_res.url,
                http_res.headers,
                "<streaming response>" if stream else http_res.text,
            )

            if utils.match_status_codes(error_status_codes, http_res.status_code):
                result, err = hooks.after_error(
                    AfterErrorContext(hook_ctx), http_res, None
                )
                if err is not None:
                    logger.debug("Request Exception", exc_info=True)
                    raise err
                if result is not None:
                    http_res = result
                else:
                    logger.debug("Raising unexpected SDK error")
                    raise self._default_error_cls("Unexpected error occurred", http_res)

            return http_res

        if retry_config is not None:
            http_res = await utils.retry_async(
                do, utils.Retries(retry_config[0], retry_config[1])
            )
        else:
            http_res = await do()

        if not utils.match_status_codes(error_status_codes, http_res.status_code):
            http_res = hooks.after_success(AfterSuccessContext(hook_ctx), http_res)

        return http_res
