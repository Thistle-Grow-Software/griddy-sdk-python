"""NGS Games endpoints for live scores and game center data."""

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
class NgsGames(NgsBaseSDK):
    """NGS Games endpoints for live scores and game center data.

    Provides access to:
    - Live game scores
    - Game center overview with detailed NGS metrics
    """

    def _get_live_scores_config(
        self,
        *,
        season: int,
        season_type: str,
        week: int,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get live game scores for a specific week.

        Returns live scores for all games in the specified week, including
        quarter-by-quarter scoring, game status, and team information.

        Args:
            season: The season year (e.g., 2025).
            season_type: Season type (REG, PRE, POST).
            week: Week number.
            retries: Override the default retry configuration.
            server_url: Override the default server URL.
            timeout_ms: Override the default timeout.
            http_headers: Additional headers to send.

        Returns:
            NgsLiveScoresResponse with game scores.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/live/games/scores",
            operation_id="getNgsLiveScores",
            request=models.GetNgsLiveScoresRequest(
                season=season,
                season_type=season_type,
                week=week,
            ),
            response_type=models.NgsLiveScoresResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_overview_config(
        self,
        *,
        game_id: int,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get detailed game center overview with NGS metrics.

        Returns comprehensive game data including:
        - Passer statistics with zone breakdowns
        - Rusher statistics with location maps
        - Receiver statistics with separation metrics
        - Pass rusher statistics
        - Game leaders (speed, sacks, pass distance)

        Args:
            game_id: The unique game identifier (e.g., 2025112700).
            retries: Override the default retry configuration.
            server_url: Override the default server URL.
            timeout_ms: Override the default timeout.
            http_headers: Additional headers to send.

        Returns:
            NgsGameCenterOverviewResponse with game overview data.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/gamecenter/overview",
            operation_id="getNgsGameOverview",
            request=models.GetNgsGameOverviewRequest(game_id=game_id),
            response_type=models.NgsGameCenterOverviewResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )
