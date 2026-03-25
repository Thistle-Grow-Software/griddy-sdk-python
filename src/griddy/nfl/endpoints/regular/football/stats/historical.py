"""Historical game statistics endpoints for team and player stats by game."""

from typing import Mapping, Optional

from griddy.core._constants import RESOURCE_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import BaseSDK, EndpointConfig
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class HistoricalStats(BaseSDK):
    r"""Historical game statistics for teams and players."""

    def _get_team_stats_config(
        self,
        *,
        game_id: str,
        team_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Historical Team Stats

        Retrieves historical team statistics for a specific game and team.
        Returns game info, team info, and deeply nested stat categories
        (defense, passing, rushing, receiving, kicking, etc.).

        Args:
            game_id: Game identifier (UUID).
            team_id: Team identifier (UUID).
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            HistoricalTeamStatsResponse containing game info, team info,
            and nested stat categories for the specified game and team.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetHistoricalTeamStatsRequest(
            game_id=game_id,
            team_id=team_id,
        )

        return EndpointConfig(
            method="GET",
            path="/football/v2/stats/historical/game/{gameId}/team/{teamId}",
            operation_id="getHistoricalTeamStats",
            request=request,
            response_type=models.HistoricalTeamStatsResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=False,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_player_stats_config(
        self,
        *,
        game_id: str,
        team_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Historical Player Stats

        Retrieves historical player statistics for a specific game and team.
        Returns game and team identifiers and a list of per-player stat objects
        with nullable stat categories (defense, passing, rushing, etc.).

        Args:
            game_id: Game identifier (UUID).
            team_id: Team identifier (UUID).
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            HistoricalPlayerStatsResponse containing per-player stat objects
            with nullable stat categories for the specified game and team.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetHistoricalPlayerStatsRequest(
            game_id=game_id,
            team_id=team_id,
        )

        return EndpointConfig(
            method="GET",
            path="/football/v2/stats/historical/game/{gameId}/persons/team/{teamId}",
            operation_id="getHistoricalPlayerStats",
            request=request,
            response_type=models.HistoricalPlayerStatsResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=False,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
