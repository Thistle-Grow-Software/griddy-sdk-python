r"""Fantasy football player statistics and scoring metrics endpoints."""

from typing import List, Mapping, Optional

from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.pro.stats.base import PlayerStatsBase
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class Fantasy(PlayerStatsBase):
    r"""Fantasy football player statistics and scoring metrics"""

    def _get_stats_by_season_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        limit: Optional[int] = 35,
        offset: Optional[int] = 0,
        page: Optional[int] = 1,
        sort_key: Optional[models.GetFantasyStatsBySeasonSortKey] = "fpStd",
        sort_value: Optional[models.SortOrderEnum] = None,
        position_group: Optional[
            List[models.GetFantasyStatsBySeasonPositionGroup]
        ] = None,
        team_offense: Optional[str] = None,
        team_defense: Optional[str] = None,
        min_offensive_snaps: Optional[int] = 0,
        last_n_weeks: Optional[int] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Fantasy Football Statistics by Season

        Retrieves comprehensive fantasy football statistics for NFL players during a specified season.
        Returns fantasy-relevant metrics including standard scoring, PPR scoring, snap counts, and
        target share data. Supports filtering by position groups (QB, RB, WR, TE, SPEC), teams,
        minimum offensive snap thresholds, and rolling N-week windows for recent performance analysis.
        Data includes traditional fantasy categories and advanced metrics for lineup optimization.

        Args:
            season: Season year.
            season_type: Type of season.
            limit: Maximum number of players to return.
            offset: Number of records to skip for pagination.
            page: Page number for pagination.
            sort_key: Field to sort by.
            sort_value: Sort direction.
            position_group: Filter by position groups (supports multiple positions).
            team_offense: Filter by specific offensive team ID.
            team_defense: Filter by specific defensive team ID (opponent analysis).
            min_offensive_snaps: Minimum offensive snaps threshold for inclusion.
            last_n_weeks: Number of recent weeks to analyze (rolling window).
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            FantasyStatsResponse containing fantasy football statistics
            for the specified season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return self._make_stats_config(
            "/api/secured/stats/fantasy/season",
            "getFantasyStatsBySeason",
            models.GetFantasyStatsBySeasonRequest,
            models.FantasyStatsResponse,
            season=season,
            season_type=season_type,
            limit=limit,
            offset=offset,
            page=page,
            sort_key=sort_key,
            sort_value=sort_value,
            position_group=position_group,
            team_offense=team_offense,
            team_defense=team_defense,
            min_offensive_snaps=min_offensive_snaps,
            last_n_weeks=last_n_weeks,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
