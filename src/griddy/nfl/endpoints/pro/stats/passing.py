r"""Player passing statistics by week and season endpoints."""

from typing import List, Mapping, Optional

from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.pro.stats.base import PlayerStatsBase
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class PlayerPassingStats(PlayerStatsBase):
    r"""Player passing statistics by week and season."""

    def _get_weekly_summary_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        week: models.WeekSlugEnum,
        limit: Optional[int] = 50,
        offset: Optional[int] = 0,
        page: Optional[int] = 1,
        sort_key: Optional[models.PassingStatsCategoryEnum] = None,
        sort_value: Optional[models.SortOrderEnum] = None,
        qualified_passer: Optional[bool] = False,
        team_offense: Optional[List[str]] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Player Passing Statistics by Week

        Retrieves comprehensive passing statistics for NFL players during a specified week and season.
        Returns detailed metrics including traditional stats, advanced analytics, and Next Gen Stats
        data. Supports filtering by teams, qualified passers, and various sorting options.

        Args:
            season: Season year.
            season_type: Type of season.
            week: Week identifier.
            limit: Maximum number of players to return.
            offset: Number of records to skip for pagination.
            page: Page number for pagination.
            sort_key: Field to sort by.
            sort_value: Sort direction.
            qualified_passer: Filter to only qualified passers (minimum attempts threshold).
            team_offense: Filter by specific team IDs (supports multiple teams).
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            WeeklyPassingStatsResponse containing player passing statistics
            for the specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return self._make_stats_config(
            "/api/secured/stats/players-offense/passing/week",
            "getPlayerPassingStatsByWeek",
            models.GetPlayerPassingStatsByWeekRequest,
            models.WeeklyPassingStatsResponse,
            season=season,
            season_type=season_type,
            week=week,
            limit=limit,
            offset=offset,
            page=page,
            sort_key=sort_key,
            sort_value=sort_value,
            qualified_passer=qualified_passer,
            team_offense=team_offense,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_season_summary_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        limit: Optional[int] = 35,
        offset: Optional[int] = 0,
        page: Optional[int] = 1,
        sort_key: Optional[models.PassingStatsCategoryEnum] = None,
        sort_value: Optional[models.SortOrderEnum] = None,
        qualified_passer: Optional[bool] = True,
        team_offense: Optional[List[str]] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Player Passing Statistics by Season

        Retrieves comprehensive passing statistics for NFL players during a specified season.

        Args:
            season: Season year.
            season_type: Type of season.
            limit: Maximum number of players to return.
            offset: Number of records to skip for pagination.
            page: Page number for pagination.
            sort_key: Field to sort by.
            sort_value: Sort direction.
            qualified_passer: Filter to only qualified passers (minimum attempts threshold).
            team_offense: Filter by specific team IDs (supports multiple teams).
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            PassingStatsResponse containing player passing statistics
            for the specified season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return self._make_stats_config(
            "/api/secured/stats/players-offense/passing/season",
            "getPlayerPassingStatsBySeason",
            models.GetPlayerPassingStatsBySeasonRequest,
            models.PassingStatsResponse,
            season=season,
            season_type=season_type,
            limit=limit,
            offset=offset,
            page=page,
            sort_key=sort_key,
            sort_value=sort_value,
            qualified_passer=qualified_passer,
            team_offense=team_offense,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
