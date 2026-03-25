"""NFL Scouting Combine endpoints for prospect profiles and event rankings."""

from typing import Mapping, Optional

from griddy.core._constants import RESOURCE_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import BaseSDK, EndpointConfig
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class Combine(BaseSDK):
    r"""NFL Scouting Combine endpoints for profiles and rankings."""

    def _get_profiles_config(
        self,
        *,
        year: int,
        limit: int = 1000,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Combine Profiles

        Retrieves NFL Scouting Combine participant profiles for a given
        draft year.

        Args:
            year: Draft year.
            limit: Maximum number of combine profiles to return.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            CombineProfilesResponse containing combine participant profiles
            for the specified year.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetCombineProfilesRequest(year=year, limit=limit)

        return EndpointConfig(
            method="GET",
            path="/football/v2/combine/profiles",
            operation_id="getCombineProfiles",
            request=request,
            response_type=models.CombineProfilesResponse,
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

    def _get_rankings_config(
        self,
        *,
        rank_attribute: models.EventFilterEnum,
        sort_order: models.SortOrderEnum,
        year: int,
        limit: int = 1000,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Combine Rankings

        Retrieves ranked combine results for a specific event attribute
        and draft year.

        Args:
            rank_attribute: Attribute to rank by.
            sort_order: Sort order.
            year: Draft year.
            limit: Maximum number of combine profiles to return.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            CombineRankingsResponse containing ranked combine results for the
            specified attribute and year.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetCombineRankingsRequest(
            rank_attribute=rank_attribute,
            sort_order=sort_order,
            year=year,
            limit=limit,
        )

        return EndpointConfig(
            method="GET",
            path="/football/v2/combine/rankings",
            operation_id="getCombineRankings",
            request=request,
            response_type=models.CombineRankingsResponse,
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
