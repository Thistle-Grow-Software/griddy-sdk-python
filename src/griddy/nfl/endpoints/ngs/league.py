"""NGS League endpoints for schedules and team information."""

from __future__ import annotations

from typing import List, Mapping, Optional

from griddy.core._constants import NGS_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.ngs import NgsBaseSDK
from griddy.nfl.types import UNSET, OptionalNullable
from griddy.nfl.utils import RetryConfig


@sdk_endpoints
class NgsLeague(NgsBaseSDK):
    """NGS League endpoints for schedules and team information.

    Provides access to:
    - Current week schedule
    - Full season schedule
    - Team information
    """

    def _get_current_schedule_config(
        self,
        *,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get the current week's schedule.

        Returns the schedule for the current week of the NFL season,
        including game times, teams, scores, and venue information.

        Args:
            retries: Override the default retry configuration for this request.
            server_url: Override the default server URL for this request.
            timeout_ms: Override the default timeout for this request.
            http_headers: Additional headers to send with the request.

        Returns:
            NgsCurrentScheduleResponse containing the current week's games.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/league/schedule/current",
            operation_id="getNgsCurrentSchedule",
            request=models.GetNgsCurrentScheduleRequest(),
            response_type=models.NgsCurrentScheduleResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=False,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_teams_config(
        self,
        *,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get all NFL teams.

        Returns a list of all NFL teams with their details including
        conference, division, stadium, and contact information.

        Args:
            retries: Override the default retry configuration for this request.
            server_url: Override the default server URL for this request.
            timeout_ms: Override the default timeout for this request.
            http_headers: Additional headers to send with the request.

        Returns:
            List of TeamInfo objects.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/league/teams",
            operation_id="getNgsTeams",
            request=models.GetNgsTeamsRequest(),
            response_type=List[models.TeamInfo],
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=False,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_schedule_config(
        self,
        *,
        season: int,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get the full season schedule.

        Returns the complete schedule for a given season, including
        all games from preseason through postseason.

        Args:
            season: The season year (e.g., 2025).
            retries: Override the default retry configuration for this request.
            server_url: Override the default server URL for this request.
            timeout_ms: Override the default timeout for this request.
            http_headers: Additional headers to send with the request.

        Returns:
            List of GameSchedule objects for the entire season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/league/schedule",
            operation_id="getNgsSchedule",
            request=models.GetNgsScheduleRequest(season=season),
            response_type=List[models.GameSchedule],
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
