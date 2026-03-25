r"""Team-level defensive statistics (overview, pass, rush) by week and season endpoints."""

from typing import List, Mapping, Optional

from griddy.core._constants import STATS_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.pro import ProSDK
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class TeamDefenseStats(ProSDK):
    r"""Team-level defensive statistics (overview, pass, rush) by week and season."""

    def _get_season_overview_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        limit: Optional[int] = 35,
        offset: Optional[int] = 0,
        page: Optional[int] = 1,
        sort_key: Optional[models.GetTeamDefenseStatsBySeasonSortKey] = "ypg",
        sort_value: Optional[models.SortOrderEnum] = None,
        split: Optional[List[models.GetTeamDefenseStatsBySeasonSplit]] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Defense Statistics by Season.

        Returns:
            TeamDefenseStatsResponse containing team defense overview
            statistics for the specified season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/stats/team-defense/overview/season",
            operation_id="getTeamDefenseStatsBySeason",
            request=models.GetTeamDefenseStatsBySeasonRequest(
                season=season,
                season_type=season_type,
                limit=limit,
                offset=offset,
                page=page,
                sort_key=sort_key,
                sort_value=sort_value,
                split=split,
            ),
            response_type=models.TeamDefenseStatsResponse,
            error_status_codes=STATS_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_weekly_overview_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        week: models.WeekSlugEnum,
        limit: Optional[int] = 35,
        offset: Optional[int] = 0,
        page: Optional[int] = 1,
        sort_key: Optional[models.TeamDefenseStatsSortKeyEnum] = "ypg",
        sort_value: Optional[models.SortOrderEnum] = None,
        split: Optional[List[models.TeamDefenseStatsSplitEnum]] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Defense Statistics by Week.

        Returns:
            TeamDefenseStatsResponse containing team defense overview
            statistics for the specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/stats/team-defense/overview/week",
            operation_id="getTeamDefenseStatsByWeek",
            request=models.GetTeamDefenseStatsByWeekRequest(
                season=season,
                season_type=season_type,
                week=week,
                limit=limit,
                offset=offset,
                page=page,
                sort_key=sort_key,
                sort_value=sort_value,
                split=split,
            ),
            response_type=models.TeamDefenseStatsResponse,
            error_status_codes=STATS_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_season_pass_stats_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        limit: Optional[int] = 35,
        offset: Optional[int] = 0,
        page: Optional[int] = 1,
        sort_key: Optional[models.GetTeamDefensePassStatsBySeasonSortKey] = "passYpg",
        sort_value: Optional[models.SortOrderEnum] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Defense Pass Statistics by Season.

        Returns:
            TeamDefensePassStatsResponse containing team defense pass
            statistics for the specified season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/stats/team-defense/pass/season",
            operation_id="getTeamDefensePassStatsBySeason",
            request=models.GetTeamDefensePassStatsBySeasonRequest(
                season=season,
                season_type=season_type,
                limit=limit,
                offset=offset,
                page=page,
                sort_key=sort_key,
                sort_value=sort_value,
            ),
            response_type=models.TeamDefensePassStatsResponse,
            error_status_codes=STATS_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_weekly_pass_stats_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        week: models.WeekSlugEnum,
        limit: Optional[int] = 35,
        offset: Optional[int] = 0,
        page: Optional[int] = 1,
        sort_key: Optional[models.GetTeamDefensePassStatsByWeekSortKey] = "passYpg",
        sort_value: Optional[models.SortOrderEnum] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Defense Pass Statistics by Week.

        Returns:
            TeamDefensePassStatsResponse containing team defense pass
            statistics for the specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/stats/team-defense/pass/week",
            operation_id="getTeamDefensePassStatsByWeek",
            request=models.GetTeamDefensePassStatsByWeekRequest(
                season=season,
                season_type=season_type,
                week=week,
                limit=limit,
                offset=offset,
                page=page,
                sort_key=sort_key,
                sort_value=sort_value,
            ),
            response_type=models.TeamDefensePassStatsResponse,
            error_status_codes=STATS_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_season_rush_stats_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        limit: Optional[int] = 35,
        offset: Optional[int] = 0,
        page: Optional[int] = 1,
        sort_key: Optional[models.GetTeamDefenseRushStatsBySeasonSortKey] = "rushYpg",
        sort_value: Optional[models.SortOrderEnum] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Defense Rush Statistics by Season.

        Returns:
            TeamDefenseRushStatsResponse containing team defense rush
            statistics for the specified season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/stats/team-defense/rush/season",
            operation_id="getTeamDefenseRushStatsBySeason",
            request=models.GetTeamDefenseRushStatsBySeasonRequest(
                season=season,
                season_type=season_type,
                limit=limit,
                offset=offset,
                page=page,
                sort_key=sort_key,
                sort_value=sort_value,
            ),
            response_type=models.TeamDefenseRushStatsResponse,
            error_status_codes=STATS_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_weekly_rush_stats_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        week: models.WeekSlugEnum,
        limit: Optional[int] = 35,
        offset: Optional[int] = 0,
        page: Optional[int] = 1,
        sort_key: Optional[models.GetTeamDefenseRushStatsByWeekSortKey] = "rushYpg",
        sort_value: Optional[models.SortOrderEnum] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Defense Rush Statistics by Week.

        Returns:
            TeamDefenseRushStatsResponse containing team defense rush
            statistics for the specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/stats/team-defense/rush/week",
            operation_id="getTeamDefenseRushStatsByWeek",
            request=models.GetTeamDefenseRushStatsByWeekRequest(
                season=season,
                season_type=season_type,
                week=week,
                limit=limit,
                offset=offset,
                page=page,
                sort_key=sort_key,
                sort_value=sort_value,
            ),
            response_type=models.TeamDefenseRushStatsResponse,
            error_status_codes=STATS_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )
