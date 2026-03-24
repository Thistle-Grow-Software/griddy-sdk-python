"""NFL Draft endpoints for retrieving draft picks and team needs."""

from typing import Mapping, Optional

from griddy.core._constants import RESOURCE_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import BaseSDK, EndpointConfig
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class Draft(BaseSDK):
    r"""NFL Draft endpoints for picks and team needs."""

    def _get_picks_report_config(
        self,
        *,
        year: int,
        limit: Optional[int] = 1000,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Draft Information

        Retrieves draft information for a specific year including all rounds,
        picks, traded picks, and compensatory selections.

        Args:
            year: Draft year.
            limit: Maximum number of picks to return.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            DraftResponse containing draft rounds, picks, traded picks,
            and compensatory selections for the specified year.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetDraftPicksReportRequest(year=year, limit=limit)

        return EndpointConfig(
            method="GET",
            path="/football/v2/draft/picks/report",
            operation_id="getDraftInfo",
            request=request,
            response_type=models.DraftResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=False,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_teamneeds_config(
        self,
        *,
        year: int,
        limit: Optional[int] = 1000,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Team Needs for Draft

        Retrieves team positional needs heading into the draft for a
        specific year.

        Args:
            year: Draft year.
            limit: Maximum number of results.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            TeamNeedsResponse containing team needs data for the specified
            draft year.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetTeamNeedsRequest(year=year, limit=limit)

        return EndpointConfig(
            method="GET",
            path="/football/v2/draft/teamneeds",
            operation_id="getTeamNeeds",
            request=request,
            response_type=models.TeamNeedsResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=False,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
