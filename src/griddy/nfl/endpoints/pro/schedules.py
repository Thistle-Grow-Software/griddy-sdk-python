r"""Game schedules, standings, betting futures, and season week endpoints."""

from typing import Mapping, Optional

from griddy.core._constants import COLLECTION_ERROR_CODES, PARAMETERLESS_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.pro import ProSDK
from griddy.nfl.endpoints.pro.mixins import GameScheduleMixin
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class Schedules(ProSDK, GameScheduleMixin):
    r"""Game schedules, matchup rankings, and injury reports"""

    def _get_scheduled_games_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        week: int,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Games by Week

        Retrieves all games for a specific season, season type, and week.
        Returns comprehensive game data including teams, venues, broadcast information,
        and ticket details for all games in the specified week.

        Args:
            season: Season year.
            season_type: Type of season.
            week: Week number within the season.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            GamesResponse containing all games for the specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/schedules/games",
            operation_id="getScheduledGames",
            request=models.GetScheduledGamesRequest(
                season=season,
                season_type=season_type,
                week=week,
            ),
            response_type=models.GamesResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_current_week_games_config(
        self,
        *,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Current Week Games

        Retrieves all games for the current week of the NFL season.
        Returns comprehensive game data including teams, venues, broadcast information,
        scores (for completed games), and ticket details. The endpoint automatically
        determines the current week based on the current date.

        Args:
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            CurrentGamesResponse containing all games for the current week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/schedules/current",
            operation_id="getCurrentWeekGames",
            request=None,
            response_type=models.CurrentGamesResponse,
            error_status_codes=PARAMETERLESS_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_future_betting_odds_config(
        self,
        *,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Future Betting Odds

        Retrieves comprehensive betting futures data including Super Bowl odds,
        conference championship odds, and division winner odds for all teams.
        Returns decimal odds for each selection along with availability status.
        This endpoint provides futures market data across multiple betting hierarchies.

        Args:
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            FuturesOddsResponse containing betting futures data across
            multiple market hierarchies.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/schedules/genius/future/odds",
            operation_id="getFutureBettingOdds",
            request=None,
            response_type=models.FuturesOddsResponse,
            error_status_codes=PARAMETERLESS_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_team_standings_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        week: int,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Standings

        Retrieves comprehensive team standings for a specific season, season type, and week.
        Returns detailed standings information including division, conference, home/away records,
        win percentages, points for/against, current streaks, and clinching scenarios.
        Standings are calculated through the specified week.

        Args:
            season: Season year.
            season_type: Type of season.
            week: Week number within the season.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            StandingsResponse containing team standings for the
            specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/schedules/standings",
            operation_id="getTeamStandings",
            request=models.GetTeamStandingsRequest(
                season=season,
                season_type=season_type,
                week=week,
            ),
            response_type=models.StandingsResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_schedule_season_weeks_config(
        self,
        *,
        season: int,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Season Weeks

        Retrieves all weeks for a specific season including preseason, regular season,
        and postseason weeks. Returns week dates, types, and teams on bye for each week.
        This endpoint provides a comprehensive season calendar with all scheduling information.

        Args:
            season: Season year.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            SeasonWeeksResponse containing all weeks for the specified season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/schedules/weeks",
            operation_id="getScheduleSeasonWeeks",
            request=models.GetScheduleSeasonWeeksRequest(
                season=season,
            ),
            response_type=models.SeasonWeeksResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
