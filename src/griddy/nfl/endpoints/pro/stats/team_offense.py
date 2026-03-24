r"""Team offensive overview statistics and situational analytics endpoints."""

from typing import List, Mapping, Optional

from griddy.core._constants import STATS_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.pro import ProSDK
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class TeamOffenseStats(ProSDK):
    r"""Comprehensive team offensive overview statistics and situational analytics"""

    def _get_season_overview_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        limit: Optional[int] = 35,
        offset: Optional[int] = 0,
        page: Optional[int] = 1,
        sort_key: Optional[models.GetTeamOffenseStatsBySeasonSortKey] = "ypg",
        sort_value: Optional[models.SortOrderEnum] = None,
        team_defense: Optional[str] = None,
        split: Optional[List[models.GetTeamOffenseStatsBySeasonSplit]] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Offense Overview Statistics by Season.

        Returns:
            TeamOffenseStatsResponse containing team offense overview
            statistics for the specified season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/stats/team-offense/overview/season",
            operation_id="getTeamOffenseStatsBySeason",
            request=models.GetTeamOffenseStatsBySeasonRequest(
                season=season,
                season_type=season_type,
                limit=limit,
                offset=offset,
                page=page,
                sort_key=sort_key,
                sort_value=sort_value,
                team_defense=team_defense,
                split=split,
            ),
            response_type=models.TeamOffenseStatsResponse,
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
        sort_key: Optional[models.GetTeamOffenseStatsByWeekSortKey] = "ypg",
        sort_value: Optional[models.SortOrderEnum] = None,
        team_defense: Optional[str] = None,
        split: Optional[List[models.GetTeamOffenseStatsByWeekSplit]] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Offense Overview Statistics by Week.

        Returns:
            TeamOffenseStatsResponse containing team offense overview
            statistics for the specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/stats/team-offense/overview/week",
            operation_id="getTeamOffenseStatsByWeek",
            request=models.GetTeamOffenseStatsByWeekRequest(
                season=season,
                season_type=season_type,
                week=week,
                limit=limit,
                offset=offset,
                page=page,
                sort_key=sort_key,
                sort_value=sort_value,
                team_defense=team_defense,
                split=split,
            ),
            response_type=models.TeamOffenseStatsResponse,
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
        sort_key: Optional[models.GetTeamOffensePassStatsBySeasonSortKey] = "passYpg",
        sort_value: Optional[models.SortOrderEnum] = None,
        team_defense: Optional[str] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Offense Pass Statistics by Season.

        Returns:
            TeamOffensePassStatsResponse containing team offense pass
            statistics for the specified season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/stats/team-offense/pass/season",
            operation_id="getTeamOffensePassStatsBySeason",
            request=models.GetTeamOffensePassStatsBySeasonRequest(
                season=season,
                season_type=season_type,
                limit=limit,
                offset=offset,
                page=page,
                sort_key=sort_key,
                sort_value=sort_value,
                team_defense=team_defense,
            ),
            response_type=models.TeamOffensePassStatsResponse,
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
        sort_key: Optional[models.GetTeamOffensePassStatsByWeekSortKey] = "passYpg",
        sort_value: Optional[models.SortOrderEnum] = None,
        team_defense: Optional[str] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Offense Pass Statistics by Week.

        Returns:
            TeamOffensePassStatsResponse containing team offense pass
            statistics for the specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/stats/team-offense/pass/week",
            operation_id="getTeamOffensePassStatsByWeek",
            request=models.GetTeamOffensePassStatsByWeekRequest(
                season=season,
                season_type=season_type,
                week=week,
                limit=limit,
                offset=offset,
                page=page,
                sort_key=sort_key,
                sort_value=sort_value,
                team_defense=team_defense,
            ),
            response_type=models.TeamOffensePassStatsResponse,
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
        sort_key: Optional[models.GetTeamOffenseRushStatsBySeasonSortKey] = "rushYpg",
        sort_value: Optional[models.SortOrderEnum] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Offense Rush Statistics by Season.

        Returns:
            TeamOffenseRushStatsResponse containing team offense rush
            statistics for the specified season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/stats/team-offense/rush/season",
            operation_id="getTeamOffenseRushStatsBySeason",
            request=models.GetTeamOffenseRushStatsBySeasonRequest(
                season=season,
                season_type=season_type,
                limit=limit,
                offset=offset,
                page=page,
                sort_key=sort_key,
                sort_value=sort_value,
            ),
            response_type=models.TeamOffenseRushStatsResponse,
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
        sort_key: Optional[models.GetTeamOffenseRushStatsByWeekSortKey] = "rushYpg",
        sort_value: Optional[models.SortOrderEnum] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Offense Rush Statistics by Week.

        Returns:
            TeamOffenseRushStatsResponse containing team offense rush
            statistics for the specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/stats/team-offense/rush/week",
            operation_id="getTeamOffenseRushStatsByWeek",
            request=models.GetTeamOffenseRushStatsByWeekRequest(
                season=season,
                season_type=season_type,
                week=week,
                limit=limit,
                offset=offset,
                page=page,
                sort_key=sort_key,
                sort_value=sort_value,
            ),
            response_type=models.TeamOffenseRushStatsResponse,
            error_status_codes=STATS_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )
