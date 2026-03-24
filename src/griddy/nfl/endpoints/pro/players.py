r"""Player detail, projected stats, and search endpoints."""

from typing import Mapping, Optional

from griddy.core._constants import COLLECTION_ERROR_CODES, RESOURCE_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.pro import ProSDK
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class Players(ProSDK):
    r"""Player detail, projected stats, and search endpoints."""

    def _get_player_config(
        self,
        *,
        nfl_id: int,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Player Details

        Retrieves detailed information about a specific NFL player including physical attributes,
        team information, draft details, and current status.

        Args:
            nfl_id: NFL player identifier.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            PlayerDetail containing detailed information about the
            specified player.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/players/player",
            operation_id="getPlayer",
            request=models.GetPlayerRequest(nfl_id=nfl_id),
            response_type=models.PlayerDetail,
            error_status_codes=RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_projected_stats_config(
        self,
        *,
        season: int,
        week: int,
        filter_nfl_team_id: Optional[str] = None,
        page_size: Optional[int] = 20,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Projected Player Statistics

        Retrieves projected fantasy statistics for players based on team, season, and week.
        Returns data in JSON:API format with relationships between players and their projected stats.

        Args:
            season: Season year.
            week: Week number within the season.
            filter_nfl_team_id: Filter by NFL team ID (UUID format).
            page_size: Number of results per page.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            ProjectedStatsResponse containing projected fantasy statistics
            for the specified parameters.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/players/projectedStats",
            operation_id="getProjectedStats",
            request=models.GetProjectedStatsRequest(
                filter_nfl_team_id=filter_nfl_team_id,
                season=season,
                week=week,
                page_size=page_size,
            ),
            response_type=models.ProjectedStatsResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _search_players_config(
        self,
        *,
        term: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Search Players

        Searches for NFL players by name or term. Returns a list of players matching the search criteria
        including both active and retired players.

        Args:
            term: Search term for player name (first or last name).
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            PlayerSearchResponse containing players matching the
            search criteria.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/players/search",
            operation_id="searchPlayers",
            request=models.SearchPlayersRequest(term=term),
            response_type=models.PlayerSearchResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
