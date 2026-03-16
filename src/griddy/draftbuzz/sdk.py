"""DraftBuzz SDK client for accessing NFL Draft Buzz data.

This module provides the GriddyDraftBuzz class, the main entry point for
accessing NFL Draft Buzz prospect data.

Example:
    >>> from griddy.draftbuzz import GriddyDraftBuzz
    >>> draftbuzz = GriddyDraftBuzz()
    >>> rankings = draftbuzz.rankings.get_position_rankings(position="QB")
"""

from typing import TYPE_CHECKING, Any, Dict, Optional

from griddy.core._lazy_load import LazySubSDKMixin
from griddy.core.base_griddy_sdk import BaseGriddySDK
from griddy.core.hooks.sdkhooks import SDKHooks

from ._hooks.registration import init_hooks
from .backends import AsyncScrapingBackend, ScrapingBackend
from .basesdk import BaseSDK
from .httpclient import AsyncHttpClient, HttpClient
from .sdkconfiguration import SDKConfiguration
from .utils import Logger
from .utils.browserless import BrowserlessConfig

if TYPE_CHECKING:
    from .endpoints.prospects import Prospects
    from .endpoints.rankings import Rankings

# Re-export for type stubs
UNSET = object()


class GriddyDraftBuzz(LazySubSDKMixin, BaseGriddySDK, BaseSDK):
    """Main client for accessing NFL Draft Buzz data.

    Sub-SDKs are loaded lazily on first access to minimize startup time.

    Example:
        >>> from griddy.draftbuzz import GriddyDraftBuzz
        >>> draftbuzz = GriddyDraftBuzz()
        >>> rankings = draftbuzz.rankings.get_position_rankings(position="QB")
    """

    prospects: "Prospects"
    rankings: "Rankings"

    _sub_sdk_map = {
        "prospects": ("griddy.draftbuzz.endpoints.prospects", "Prospects"),
        "rankings": ("griddy.draftbuzz.endpoints.rankings", "Rankings"),
    }

    def __init__(
        self,
        draftbuzz_auth: Optional[Dict[str, str]] = None,
        server_idx: Optional[int] = None,
        server_url: Optional[str] = None,
        url_params: Optional[Dict[str, str]] = None,
        client: Optional[HttpClient] = None,
        async_client: Optional[AsyncHttpClient] = None,
        retry_config: Any = UNSET,
        timeout_ms: Optional[int] = None,
        debug_logger: Optional[Logger] = None,
        browserless_config: Optional[BrowserlessConfig] = None,
        scraping_backend: Optional[ScrapingBackend] = None,
        async_scraping_backend: Optional[AsyncScrapingBackend] = None,
    ) -> None:
        """Initialize the GriddyDraftBuzz client.

        Args:
            draftbuzz_auth: Optional dictionary containing authentication
                information. DraftBuzz does not currently require auth, but
                this is available for future use.
            server_idx: Index of the server to use from the server list.
            server_url: Override the default server URL.
            url_params: Parameters to template into the server URL.
            client: Custom synchronous HTTP client (must implement HttpClient).
            async_client: Custom async HTTP client (must implement AsyncHttpClient).
            retry_config: Configuration for automatic request retries.
            timeout_ms: Request timeout in milliseconds.
            debug_logger: Custom logger for debug output.
            browserless_config: Configuration for Browserless API requests.
                Overrides default proxy, timeout, and TTL values. Ignored when
                a custom *scraping_backend* is provided.
            scraping_backend: A synchronous scraping backend that satisfies the
                :class:`~griddy.draftbuzz.backends.ScrapingBackend` protocol.
            async_scraping_backend: An asynchronous scraping backend that
                satisfies the :class:`~griddy.draftbuzz.backends.AsyncScrapingBackend`
                protocol.
        """
        self._browserless_config = browserless_config
        self._scraping_backend = scraping_backend
        self._async_scraping_backend = async_scraping_backend
        self._init_sdk(
            auth=draftbuzz_auth,
            server_idx=server_idx,
            server_url=server_url,
            url_params=url_params,
            client=client,
            async_client=async_client,
            retry_config=retry_config,
            timeout_ms=timeout_ms,
            debug_logger=debug_logger,
            scraping_backend=scraping_backend,
            async_scraping_backend=async_scraping_backend,
        )

    # ------------------------------------------------------------------
    # BaseGriddySDK abstract method implementations
    # ------------------------------------------------------------------

    def _get_debug_logger_env_var(self) -> str:
        """Return the environment variable name that enables debug logging."""
        return "GRIDDY_DRAFTBUZZ_DEBUG"

    def _create_security(self, auth: Any) -> Any:
        """Create a Security model from the DraftBuzz auth token, if provided."""
        if auth and "accessToken" in auth:
            from . import models

            return models.Security(draftbuzz_auth=auth["accessToken"])
        return None

    def _create_sdk_configuration(self, **kwargs: Any) -> Any:
        """Create a DraftBuzz-specific SDKConfiguration instance."""
        return SDKConfiguration(**kwargs)

    def _create_hooks(self) -> Any:
        """Create and return the DraftBuzz SDK hooks instance."""
        return SDKHooks(init_hooks_fn=init_hooks)
