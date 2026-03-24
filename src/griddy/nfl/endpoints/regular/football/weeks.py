"""Week and season schedule endpoints for date lookups and season week listings."""

from typing import Mapping, Optional

from griddy.core._constants import COLLECTION_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import BaseSDK, EndpointConfig
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class Weeks(BaseSDK):
    r"""Week and season schedule endpoints."""

    def _get_week_of_date_config(
        self,
        *,
        date: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Week for Date

        Retrieves the NFL week corresponding to a specific calendar date.

        Args:
            date: YYYY-MM-DD.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            Week containing the season, season type, and week number for
            the specified date.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetWeekOfDateRequest(date=date)

        return EndpointConfig(
            method="GET",
            path="/football/v2/weeks/date/{date}",
            operation_id="getWeekOfDate",
            request=request,
            response_type=models.Week,
            error_status_codes=COLLECTION_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=False,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_season_weeks_config(
        self,
        *,
        season: int,
        limit: Optional[int] = 20,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Season Weeks

        Retrieves all weeks for a specific season including preseason, regular season, and postseason.

        Args:
            season: Season year.
            limit: Maximum number of weeks to return.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            WeeksResponse containing all weeks for the specified season
            including preseason, regular season, and postseason.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetSeasonWeeksRequest(season=season, limit=limit)

        return EndpointConfig(
            method="GET",
            path="/football/v2/weeks/season/{season}",
            operation_id="getSeasonWeeks",
            request=request,
            response_type=models.WeeksResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
