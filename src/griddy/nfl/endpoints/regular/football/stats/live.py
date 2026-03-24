"""Live game statistics endpoints for real-time team and player stats."""

from typing import Mapping, Optional

from griddy.core._constants import RESOURCE_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import BaseSDK, EndpointConfig
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class LiveStats(BaseSDK):
    r"""Live game statistics for teams and players."""

    def _get_team_statistics_config(
        self,
        *,
        game_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Live Team Statistics

        Retrieves live team statistics for a specific game.
        Returns awayTeam and homeTeam objects each containing 100+ stat fields.

        Args:
            game_id: Game identifier (UUID).
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            LiveTeamStatisticsResponse containing away and home team
            stat objects for the specified game.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetLiveTeamStatisticsRequest(
            game_id=game_id,
        )

        return EndpointConfig(
            method="GET",
            path="/football/v2/stats/live/team-statistics/{gameId}",
            operation_id="getLiveTeamStatistics",
            request=request,
            response_type=models.LiveTeamStatisticsResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=False,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_player_statistics_config(
        self,
        *,
        game_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Live Player Statistics

        Retrieves live player statistics for a specific game.
        Returns awayTeam and homeTeam objects, each containing a players
        array with per-player identification and 100+ stat fields.

        Args:
            game_id: Game identifier (UUID).
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            LivePlayerStatisticsResponse containing per-player statistics
            for away and home teams in the specified game.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetLivePlayerStatisticsRequest(
            game_id=game_id,
        )

        return EndpointConfig(
            method="GET",
            path="/football/v2/stats/live/player-statistics/{gameId}",
            operation_id="getLivePlayerStatistics",
            request=request,
            response_type=models.LivePlayerStatisticsResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=False,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
