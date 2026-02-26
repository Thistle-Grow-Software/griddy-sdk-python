"""PFR SDK client for accessing Pro Football Reference data.

This module provides the GriddyPFR class, the main entry point for accessing
Pro Football Reference data.

Example:
    >>> from griddy.pfr import GriddyPFR
    >>> pfr = GriddyPFR()
    >>> games = pfr.schedule.get_season_schedule(season=2015)
"""

import weakref
from typing import TYPE_CHECKING, Dict, Optional, cast

import httpx

from griddy.core._lazy_load import LazySubSDKMixin
from griddy.core.hooks.sdkhooks import SDKHooks
from griddy.core.utils.logger import get_default_logger

from ._hooks.registration import init_hooks
from .basesdk import BaseSDK
from .httpclient import AsyncHttpClient, ClientOwner, HttpClient, close_clients
from .sdkconfiguration import SDKConfiguration
from .types import UNSET, OptionalNullable
from .utils import Logger, RetryConfig

if TYPE_CHECKING:
    from .endpoints.coaches import Coaches
    from .endpoints.games import Games
    from .endpoints.leaders import Leaders
    from .endpoints.officials import Officials
    from .endpoints.players import Players
    from .endpoints.schedule import Schedule
    from .endpoints.seasons import Seasons
    from .endpoints.stadiums import Stadiums
    from .endpoints.teams import Teams


class GriddyPFR(LazySubSDKMixin, BaseSDK):
    """Main client for accessing Pro Football Reference data.

    Sub-SDKs are loaded lazily on first access to minimize startup time.

    Example:
        >>> from griddy.pfr import GriddyPFR
        >>> pfr = GriddyPFR()
        >>> games = pfr.schedule.get_season_schedule(season=2015)
    """

    coaches: "Coaches"
    games: "Games"
    leaders: "Leaders"
    officials: "Officials"
    players: "Players"
    schedule: "Schedule"
    seasons: "Seasons"
    stadiums: "Stadiums"
    teams: "Teams"

    _sub_sdk_map = {
        "coaches": ("griddy.pfr.endpoints.coaches", "Coaches"),
        "games": ("griddy.pfr.endpoints.games", "Games"),
        "leaders": ("griddy.pfr.endpoints.leaders", "Leaders"),
        "officials": ("griddy.pfr.endpoints.officials", "Officials"),
        "players": ("griddy.pfr.endpoints.players", "Players"),
        "schedule": ("griddy.pfr.endpoints.schedule", "Schedule"),
        "seasons": ("griddy.pfr.endpoints.seasons", "Seasons"),
        "stadiums": ("griddy.pfr.endpoints.stadiums", "Stadiums"),
        "teams": ("griddy.pfr.endpoints.teams", "Teams"),
    }

    def __init__(
        self,
        pfr_auth: Optional[Dict[str, str]] = None,
        server_idx: Optional[int] = None,
        server_url: Optional[str] = None,
        url_params: Optional[Dict[str, str]] = None,
        client: Optional[HttpClient] = None,
        async_client: Optional[AsyncHttpClient] = None,
        retry_config: OptionalNullable[RetryConfig] = UNSET,
        timeout_ms: Optional[int] = None,
        debug_logger: Optional[Logger] = None,
    ) -> None:
        """Initialize the GriddyPFR client.

        Args:
            pfr_auth: Optional dictionary containing authentication information.
                PFR does not currently require auth, but this is available for
                future use. Example: {"accessToken": "your_token"}
            server_idx: Index of the server to use from the server list.
            server_url: Override the default server URL.
            url_params: Parameters to template into the server URL.
            client: Custom synchronous HTTP client (must implement HttpClient).
            async_client: Custom async HTTP client (must implement AsyncHttpClient).
            retry_config: Configuration for automatic request retries.
            timeout_ms: Request timeout in milliseconds.
            debug_logger: Custom logger for debug output.
        """
        client_supplied = True
        if client is None:
            client = httpx.Client(follow_redirects=True)
            client_supplied = False

        assert issubclass(
            type(client), HttpClient
        ), "The provided client must implement the HttpClient protocol."

        async_client_supplied = True
        if async_client is None:
            async_client = httpx.AsyncClient(follow_redirects=True)
            async_client_supplied = False

        if debug_logger is None:
            debug_logger = get_default_logger(env_var="GRIDDY_PFR_DEBUG")

        assert issubclass(
            type(async_client), AsyncHttpClient
        ), "The provided async_client must implement the AsyncHttpClient protocol."

        security = None
        if pfr_auth and "accessToken" in pfr_auth:
            from . import models

            security = models.Security(pfr_auth=pfr_auth["accessToken"])

        if server_url is not None:
            if url_params is not None:
                from griddy.core.utils import template_url

                server_url = template_url(server_url, url_params)

        BaseSDK.__init__(
            self,
            SDKConfiguration(
                client=client,
                client_supplied=client_supplied,
                async_client=async_client,
                async_client_supplied=async_client_supplied,
                security=security,
                server_url=server_url,
                server_idx=server_idx,
                retry_config=retry_config,
                timeout_ms=timeout_ms,
                debug_logger=debug_logger,
            ),
            parent_ref=self,
        )

        hooks = SDKHooks(init_hooks_fn=init_hooks)

        # pylint: disable=protected-access
        self.sdk_configuration.__dict__["_hooks"] = hooks

        self.sdk_configuration = hooks.sdk_init(self.sdk_configuration)

        weakref.finalize(
            self,
            close_clients,
            cast(ClientOwner, self.sdk_configuration),
            self.sdk_configuration.client,
            self.sdk_configuration.client_supplied,
            self.sdk_configuration.async_client,
            self.sdk_configuration.async_client_supplied,
        )

    def __enter__(self):
        return self

    async def __aenter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (
            self.sdk_configuration.client is not None
            and not self.sdk_configuration.client_supplied
        ):
            self.sdk_configuration.client.close()
        self.sdk_configuration.client = None

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if (
            self.sdk_configuration.async_client is not None
            and not self.sdk_configuration.async_client_supplied
        ):
            await self.sdk_configuration.async_client.aclose()
        self.sdk_configuration.async_client = None
