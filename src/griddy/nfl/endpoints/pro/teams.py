r"""Team information, rosters, schedules, and ranking endpoints."""

from typing import List, Mapping, Optional

from griddy.core._constants import COLLECTION_ERROR_CODES, RESOURCE_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.pro import ProSDK
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class Teams(ProSDK):
    r"""Team information, rosters, schedules, and ranking endpoints."""

    def _get_all_teams_config(
        self,
        *,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get All Teams

        Retrieves information for all NFL teams including regular teams and Pro Bowl teams.
        Returns comprehensive team data including colors, logos, stadiums, and contact information.

        Args:
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            List[ProTeam] containing information for all NFL teams.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/teams/all",
            operation_id="getAllTeams",
            request=None,
            response_type=List[models.ProTeam],
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_team_roster_config(
        self,
        *,
        team_id: str,
        season: int,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Roster

        Retrieves the complete roster for a specific team and season.
        Returns detailed player information including physical attributes, college info, and experience.

        Args:
            team_id: Team identifier (4-digit string).
            season: Season year.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            TeamRosterResponse containing the complete roster for the
            specified team and season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/teams/roster",
            operation_id="getTeamRoster",
            request=models.GetTeamRosterRequest(team_id=team_id, season=season),
            response_type=models.TeamRosterResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_weekly_team_roster_config(
        self,
        *,
        team_id: str,
        season: int,
        season_type: models.SeasonTypeEnum,
        week: int,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Weekly Team Roster

        Retrieves the roster for a specific team, season, season type, and week.
        Returns player information with weekly status and availability.

        Args:
            team_id: Team identifier (4-digit string).
            season: Season year.
            season_type: Type of season.
            week: Week number within the season.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            WeeklyRosterResponse containing the roster with weekly status
            for the specified team and week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/teams/rosterWeek",
            operation_id="getWeeklyTeamRoster",
            request=models.GetWeeklyTeamRosterRequest(
                team_id=team_id,
                season=season,
                season_type=season_type,
                week=week,
            ),
            response_type=models.WeeklyRosterResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_team_schedule_config(
        self,
        *,
        team_id: str,
        season: int,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Schedule

        Retrieves the complete schedule for a specific team and season.
        Returns all games including preseason, regular season, and postseason with scores for completed games.

        Args:
            team_id: Team identifier (4-digit string).
            season: Season year.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            List[ScheduledGame] containing the complete schedule for the
            specified team and season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/teams/schedule",
            operation_id="getTeamSchedule",
            request=models.GetTeamScheduleRequest(team_id=team_id, season=season),
            response_type=List[models.ScheduledGame],
            error_status_codes=RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_multiple_rankings_all_teams_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        stat0: str,
        stat1: Optional[str] = None,
        stat2: Optional[str] = None,
        stat3: Optional[str] = None,
        stat4: Optional[str] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Multiple Rankings for All Teams

        Retrieves rankings for all 32 NFL teams across multiple specified statistical categories.
        Allows comparison of teams across up to 5 different statistics simultaneously.

        Args:
            season: Season year.
            season_type: Type of season.
            stat0: First statistical category.
            stat1: Second statistical category.
            stat2: Third statistical category.
            stat3: Fourth statistical category.
            stat4: Fifth statistical category.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            List[MultipleRankingsCategory] containing rankings for all
            teams across the specified statistical categories.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/stats/multiple-rankings/all-teams",
            operation_id="getMultipleRankingsAllTeams",
            request=models.GetMultipleRankingsAllTeamsRequest(
                season=season,
                season_type=season_type,
                stat0=stat0,
                stat1=stat1,
                stat2=stat2,
                stat3=stat3,
                stat4=stat4,
            ),
            response_type=List[models.MultipleRankingsCategory],
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
