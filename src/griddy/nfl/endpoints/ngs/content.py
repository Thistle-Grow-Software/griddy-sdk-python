"""NGS Content endpoints for charts and highlights."""

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
class NgsContent(NgsBaseSDK):
    """NGS Content endpoints for charts and highlights.

    Provides access to:
    - Player charts (route, pass, carry)
    - Chart players list
    - Play highlights
    """

    def _get_charts_config(
        self,
        *,
        season: int,
        count: int = 12,
        week: str = "all",
        chart_type: str = "all",
        team_id: str = "all",
        esb_id: str = "all",
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get player charts (route, pass, carry).

        Args:
            season: Season year (e.g., 2025).
            count: Number of charts to return (default: 12).
            week: Week filter or "all" (default: "all").
            chart_type: Chart type filter: "all", "route", "pass", "carry".
            team_id: Team ID filter or "all".
            esb_id: Player ESB ID filter or "all".

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/content/microsite/chart",
            operation_id="getNgsCharts",
            request=models.GetNgsChartsRequest(
                season=season,
                count=count,
                week=week,
                chart_type=chart_type,
                team_id=team_id,
                esb_id=esb_id,
            ),
            response_type=models.NgsChartsResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_players_config(
        self,
        *,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get players available in the chart system.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/content/microsite/chart/players",
            operation_id="getNgsChartPlayers",
            request=models.GetNgsCurrentScheduleRequest(),  # No params needed
            response_type=models.NgsChartPlayersResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=False,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_highlights_config(
        self,
        *,
        season: int,
        limit: int = 16,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get play highlights.

        Args:
            season: Season year (e.g., 2025).
            limit: Number of highlights to return (default: 16).

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/plays/highlights",
            operation_id="getNgsHighlights",
            request=models.GetNgsHighlightsRequest(season=season, limit=limit),
            response_type=models.NgsHighlightsResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )
