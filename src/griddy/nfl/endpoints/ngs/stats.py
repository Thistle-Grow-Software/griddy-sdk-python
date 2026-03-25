"""NGS Stats endpoints for player statistics."""

from __future__ import annotations

from typing import Mapping, Optional

from griddy.core._constants import NGS_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.ngs import NgsBaseSDK
from griddy.nfl.types import UNSET, OptionalNullable
from griddy.nfl.utils import RetryConfig


@sdk_endpoints
class NgsStats(NgsBaseSDK):
    """NGS Stats endpoints for player statistics.

    Provides access to:
    - Passing statistics (time to throw, air yards, completion probability, etc.)
    - Receiving statistics (separation, cushion, YAC, etc.)
    - Rushing statistics (time to LOS, rush yards over expected, etc.)
    """

    def _get_passing_stats_config(
        self,
        *,
        season: int,
        season_type: str,
        week: Optional[int] = None,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get NGS passing statistics.

        Returns detailed passing statistics including time to throw,
        air yards, completion probability, and more.

        Args:
            season: The season year (e.g., 2025).
            season_type: Season type (REG, PRE, POST).
            week: Optional week filter.
            retries: Override the default retry configuration.
            server_url: Override the default server URL.
            timeout_ms: Override the default timeout.
            http_headers: Additional headers to send.

        Returns:
            Dict containing passing statistics.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/statboard/passing",
            operation_id="getNgsPassingStats",
            request=models.GetNgsPassingStatsRequest(
                season=season,
                season_type=season_type,
                week=week,
            ),
            response_type=models.NgsPassingStatsResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_receiving_stats_config(
        self,
        *,
        season: int,
        season_type: str,
        week: Optional[int] = None,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get NGS receiving statistics.

        Returns detailed receiving statistics including separation,
        cushion, YAC over expectation, and more.

        Args:
            season: The season year (e.g., 2025).
            season_type: Season type (REG, PRE, POST).
            week: Optional week filter.
            retries: Override the default retry configuration.
            server_url: Override the default server URL.
            timeout_ms: Override the default timeout.
            http_headers: Additional headers to send.

        Returns:
            NgsReceivingStatsResponse containing receiving statistics.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/statboard/receiving",
            operation_id="getNgsReceivingStats",
            request=models.GetNgsReceivingStatsRequest(
                season=season,
                season_type=season_type,
                week=week,
            ),
            response_type=models.NgsReceivingStatsResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_rushing_stats_config(
        self,
        *,
        season: int,
        season_type: str,
        week: Optional[int] = None,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get NGS rushing statistics.

        Returns detailed rushing statistics including time to LOS,
        rush yards over expected, efficiency, and more.

        Args:
            season: The season year (e.g., 2025).
            season_type: Season type (REG, PRE, POST).
            week: Optional week filter.
            retries: Override the default retry configuration.
            server_url: Override the default server URL.
            timeout_ms: Override the default timeout.
            http_headers: Additional headers to send.

        Returns:
            NgsRushingStatsResponse containing rushing statistics.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/statboard/rushing",
            operation_id="getNgsRushingStats",
            request=models.GetNgsRushingStatsRequest(
                season=season,
                season_type=season_type,
                week=week,
            ),
            response_type=models.NgsRushingStatsResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )
