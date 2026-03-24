r"""Betting odds and lines endpoints for NFL games."""

from typing import Mapping, Optional

from griddy.core._constants import COLLECTION_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.pro import ProSDK
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class Betting(ProSDK):
    r"""Game betting odds and lines"""

    def _get_weekly_betting_odds_config(
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
        r"""Get Weekly Betting Odds

        Retrieves comprehensive betting odds for all games in a specified week.
        Returns point spreads, money lines, and totals (over/under) for each game
        with the latest odds updates from betting markets.

        Args:
            season: Season year.
            season_type: Type of season.
            week: Week number within the season.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            WeeklyOddsResponse containing betting odds for all games
            in the specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/schedules/week/odds",
            operation_id="getWeeklyBettingOdds",
            request=models.GetWeeklyBettingOddsRequest(
                season=season,
                season_type=season_type,
                week=week,
            ),
            response_type=models.WeeklyOddsResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
