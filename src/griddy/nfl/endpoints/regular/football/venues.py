"""NFL venue and stadium information endpoints."""

from typing import Mapping, Optional

from griddy.core._constants import COLLECTION_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import BaseSDK, EndpointConfig
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class Venues(BaseSDK):
    r"""NFL venue and stadium information endpoints."""

    def _get_venues_config(
        self,
        *,
        season: int,
        limit: Optional[int] = 20,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get NFL Venues

        Retrieves information about all NFL stadiums and venues, including international venues.
        Provides venue details such as addresses, locations, and territories.

        Args:
            season: Season year.
            limit: Maximum number of venues to return.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            VenuesResponse containing venue and stadium data for the
            specified season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetVenuesRequest(
            season=season,
            limit=limit,
        )

        return EndpointConfig(
            method="GET",
            path="/football/v2/venues",
            operation_id="getVenues",
            request=request,
            response_type=models.VenuesResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=False,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
