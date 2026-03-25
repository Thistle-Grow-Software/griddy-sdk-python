"""Team standings endpoints for retrieving division, conference, and overall standings."""

from typing import Mapping, Optional

from griddy.core._constants import COLLECTION_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import BaseSDK, EndpointConfig
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class Standings(BaseSDK):
    r"""Team standings endpoints by season, type, and week."""

    def _get_standings_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        week: int,
        limit: Optional[int] = 20,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Standings

        Retrieves team standings for a specific season, season type, and week.
        Includes division, conference, and overall standings with detailed statistics.

        Args:
            season: Season year.
            season_type: Type of season.
            week: Week number.
            limit: Maximum number of results to return.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            StandingsResponse containing team standings for the specified
            season, type, and week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetStandingsRequest(
            season=season,
            season_type=season_type,
            week=week,
            limit=limit,
        )

        return EndpointConfig(
            method="GET",
            path="/football/v2/standings",
            operation_id="getStandings",
            request=request,
            response_type=models.StandingsResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=False,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
