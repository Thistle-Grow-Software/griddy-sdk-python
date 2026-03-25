r"""Player rushing statistics by week and season endpoints."""

from typing import List, Mapping, Optional

from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.pro.stats.base import PlayerStatsBase
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class PlayerRushingStats(PlayerStatsBase):
    r"""Player rushing statistics by week and season."""

    def _get_weekly_summary_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        week: models.WeekSlugEnum,
        limit: Optional[int] = 50,
        offset: Optional[int] = 0,
        page: Optional[int] = 1,
        sort_key: Optional[models.GetPlayerRushingStatsByWeekSortKey] = "yds",
        sort_value: Optional[models.SortOrderEnum] = None,
        qualified_rusher: Optional[bool] = False,
        team_offense: Optional[List[str]] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Player Rushing Statistics by Week

        Retrieves comprehensive rushing statistics for NFL players during a specified week.

        Args:
            season: Season year.
            season_type: Type of season.
            week: Week identifier.
            limit: Maximum number of players to return.
            offset: Number of records to skip for pagination.
            page: Page number for pagination.
            sort_key: Field to sort by.
            sort_value: Sort direction.
            qualified_rusher: Filter to only qualified rushers.
            team_offense: Filter by specific team IDs.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            WeeklyRushingStatsResponse containing player rushing statistics
            for the specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return self._make_stats_config(
            "/api/secured/stats/players-offense/rushing/week",
            "getPlayerRushingStatsByWeek",
            models.GetPlayerRushingStatsByWeekRequest,
            models.WeeklyRushingStatsResponse,
            season=season,
            season_type=season_type,
            week=week,
            limit=limit,
            offset=offset,
            page=page,
            sort_key=sort_key,
            sort_value=sort_value,
            qualified_rusher=qualified_rusher,
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
        sort_key: Optional[models.GetPlayerRushingStatsBySeasonSortKey] = "yds",
        sort_value: Optional[models.SortOrderEnum] = None,
        qualified_rusher: Optional[bool] = False,
        team_offense: Optional[List[str]] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Player Rushing Statistics by Season

        Retrieves comprehensive rushing statistics for NFL players during a specified season.

        Args:
            season: Season year.
            season_type: Type of season.
            limit: Maximum number of players to return.
            offset: Number of records to skip for pagination.
            page: Page number for pagination.
            sort_key: Field to sort by.
            sort_value: Sort direction.
            qualified_rusher: Filter to only qualified rushers.
            team_offense: Filter by specific team IDs.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            RushingStatsResponse containing player rushing statistics
            for the specified season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return self._make_stats_config(
            "/api/secured/stats/players-offense/rushing/season",
            "getPlayerRushingStatsBySeason",
            models.GetPlayerRushingStatsBySeasonRequest,
            models.RushingStatsResponse,
            season=season,
            season_type=season_type,
            limit=limit,
            offset=offset,
            page=page,
            sort_key=sort_key,
            sort_value=sort_value,
            qualified_rusher=qualified_rusher,
            team_offense=team_offense,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
