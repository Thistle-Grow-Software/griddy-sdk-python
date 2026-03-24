r"""Mixin providing game schedule, matchup rankings, team rankings, and injury report endpoints."""

from typing import Mapping, Optional

from griddy.core._constants import COLLECTION_ERROR_CODES, RESOURCE_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class GameScheduleMixin:
    """Mixin for game schedule-related endpoints.

    These methods are designed to be mixed into classes that inherit from ProSDK/BaseSDK,
    which provides the helper methods (_resolve_base_url, _resolve_timeout, etc.).
    """

    def _get_scheduled_game_config(
        self,
        *,
        game_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Single Game Details

        Retrieves detailed information for a specific game by its ID.
        Returns comprehensive game data including teams, score, venue, broadcast information,
        and current game status.

        Args:
            game_id: Game identifier (UUID format).
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            GameDetail containing detailed information for the specified game.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/schedules/game",
            operation_id="getScheduledGame",
            request=models.GetScheduledGameRequest(game_id=game_id),
            response_type=models.GameDetail,
            error_status_codes=RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_game_matchup_rankings_config(
        self,
        *,
        game_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Game Matchup Rankings

        Retrieves comprehensive matchup rankings and statistical comparisons for both teams in a specific game.
        Returns offensive, defensive, and special teams rankings with Z-scores and advantage ratings
        for various statistical categories.

        Args:
            game_id: Game identifier (10-digit format YYYYMMDDNN).
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            MatchupRankingsResponse containing matchup rankings and
            statistical comparisons for both teams.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/schedules/game/matchup/rankings",
            operation_id="getGameMatchupRankings",
            request=models.GetGameMatchupRankingsRequest(game_id=game_id),
            response_type=models.MatchupRankingsResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_game_team_rankings_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        away_team_id: str,
        home_team_id: str,
        week: int,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Rankings for Game

        Retrieves comprehensive statistical rankings for both teams in a specific game.
        Returns 300+ statistical categories with rankings for offensive, defensive, and special teams performance.

        Args:
            season: Season year.
            season_type: Type of season.
            away_team_id: Away team UUID.
            home_team_id: Home team UUID.
            week: Week number.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            TeamRankingsResponse containing statistical rankings for both
            teams in the specified game.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/stats/game/team-rankings",
            operation_id="getGameTeamRankings",
            request=models.GetGameTeamRankingsRequest(
                season=season,
                season_type=season_type,
                away_team_id=away_team_id,
                home_team_id=home_team_id,
                week=week,
            ),
            response_type=models.TeamRankingsResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_team_injuries_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        team_id: str,
        week: int,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Injuries for Game Week

        Retrieves injury report information for a specific team in a given week.
        Returns player injury status and details for the specified team and week.

        Args:
            season: Season year.
            season_type: Type of season.
            team_id: Team identifier (UUID format).
            week: Week number within the season.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            InjuryReportResponse containing injury report information
            for the specified team and week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/schedules/game/team/injuries",
            operation_id="getTeamInjuries",
            request=models.GetTeamInjuriesRequest(
                season=season,
                season_type=season_type,
                team_id=team_id,
                week=week,
            ),
            response_type=models.InjuryReportResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
