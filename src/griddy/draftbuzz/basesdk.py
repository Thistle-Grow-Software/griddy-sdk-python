from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol, Type, Union
from urllib.parse import urlencode

from griddy.core.basesdk import BaseEndpointConfig
from griddy.core.basesdk import BaseSDK as CoreBaseSDK

from . import errors, models
from .backends import AsyncScrapingBackend, ScrapingBackend
from .errors import ParsingError
from .sdkconfiguration import SDKConfiguration


class DraftBuzzParser(Protocol):
    """Protocol that all DraftBuzz parsers must satisfy.

    Parse methods must accept an HTML string and return a plain ``dict``
    (for single-model endpoints) or a ``list[dict]`` (for list endpoints).
    Pydantic model construction is handled by the base SDK, not the parser.
    """

    def __call__(self, html: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Parse raw HTML and return a dict or list of dicts for model validation."""
        ...


@dataclass
class EndpointConfig(BaseEndpointConfig):
    """Configuration for a DraftBuzz HTML-scraping endpoint."""

    path_template: str = ""
    wait_for_element: str = ""
    parser: DraftBuzzParser = None  # type: ignore[assignment]
    path_params: Dict[str, Any] = field(default_factory=dict)
    query_params: Dict[str, str] = field(default_factory=dict)


class BaseSDK(CoreBaseSDK[SDKConfiguration]):
    """DraftBuzz-specific BaseSDK with error classes and scraping backends.

    Uses Playwright (Firefox) by default to fetch fully-rendered HTML
    from nfldraftbuzz.com. A custom scraping backend can be injected
    via the ``scraping_backend`` parameter on :class:`GriddyDraftBuzz`.
    """

    scraper: ScrapingBackend
    async_scraper: AsyncScrapingBackend

    def __init__(
        self,
        sdk_config: SDKConfiguration,
        parent_ref: Optional[object] = None,
    ) -> None:
        """Initialize DraftBuzz BaseSDK with scraping backends for HTML fetching.

        The scraping backend is resolved in the following order:

        1. A backend stored on ``sdk_config.scraping_backend`` (set when the
           user passes ``scraping_backend`` to :class:`GriddyDraftBuzz`).
        2. A default :class:`PlaywrightBackend` instance using Firefox.

        Args:
            sdk_config: DraftBuzz SDK configuration with server details.
            parent_ref: Optional reference to the parent SDK instance.
        """
        super().__init__(sdk_config=sdk_config, parent_ref=parent_ref)

        if sdk_config.scraping_backend is not None:
            self.scraper = sdk_config.scraping_backend
        else:
            headless = getattr(self, "_headless", True)
            from .utils.playwright import PlaywrightBackend

            self.scraper = PlaywrightBackend(headless=headless)

        if sdk_config.async_scraping_backend is not None:
            self.async_scraper = sdk_config.async_scraping_backend
        else:
            headless = getattr(self, "_headless", True)
            from .utils.playwright import AsyncPlaywrightBackend

            self.async_scraper = AsyncPlaywrightBackend(headless=headless)

    @property
    def _default_error_cls(self) -> Type[Exception]:
        """Return the default error class for DraftBuzz API response errors."""
        return errors.GriddyDraftBuzzDefaultError

    @property
    def _no_response_error_cls(self) -> Type[Exception]:
        """Return the error class raised when DraftBuzz returns no response body."""
        return errors.NoResponseError

    @property
    def _security_model_cls(self) -> Any:
        """Return the Pydantic security model class for DraftBuzz authentication."""
        return models.Security

    @property
    def _security_env_mapping(self) -> Optional[Dict[str, str]]:
        """Return the mapping of security fields to environment variable names."""
        return {"draftbuzz_auth": "GRIDDY_DRAFTBUZZ_AUTH"}

    def _build_url(self, config: EndpointConfig) -> str:
        """Build the full URL from the base server URL, path template, and query params."""
        base_url, _ = self.sdk_configuration.get_server_details()
        path = config.path_template.format(**config.path_params)
        url = f"{base_url}{path}"
        if config.query_params:
            url = f"{url}?{urlencode(config.query_params)}"
        return url

    def _parse_and_validate(self, config: EndpointConfig, html: str) -> Any:
        """Run the endpoint parser and validate results into Pydantic models."""
        try:
            result = config.parser(html)
        except ParsingError:
            raise

        if isinstance(result, list):
            return [config.response_type.model_validate(item) for item in result]
        return config.response_type.model_validate(result)

    def _execute_endpoint(self, config: EndpointConfig) -> Any:
        """Execute a DraftBuzz scraping endpoint using its configuration.

        Resolves the base URL, templates path params, fetches HTML via
        Playwright, and runs the configured parser.
        """
        url = self._build_url(config)

        html = self.scraper.get_page_content(
            url,
            wait_for_element=config.wait_for_element,
        )

        try:
            return self._parse_and_validate(config, html)
        except ParsingError as exc:
            exc.url = url
            raise

    async def _execute_endpoint_async(self, config: EndpointConfig) -> Any:
        """Async version of :meth:`_execute_endpoint`."""
        url = self._build_url(config)

        html = await self.async_scraper.get_page_content(
            url,
            wait_for_element=config.wait_for_element,
        )

        try:
            return self._parse_and_validate(config, html)
        except ParsingError as exc:
            exc.url = url
            raise
