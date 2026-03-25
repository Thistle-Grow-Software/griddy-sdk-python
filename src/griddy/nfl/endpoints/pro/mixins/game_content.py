r"""Mixin providing game preview and game-specific insight endpoints."""

from typing import List, Mapping, Optional

from griddy.core._constants import COLLECTION_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class GameContentMixin:
    """Mixin for game content-related endpoints."""

    def _get_game_preview_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        week: int,
        visitor_display_name: str,
        home_display_name: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Game Preview Content

        Retrieves preview content and insights for a specific game based on teams and week. Returns preview information, matchup analysis, and key storylines.

        Args:
            season: Season year.
            season_type: Type of season.
            week: Week number.
            visitor_display_name: Visiting team display name.
            home_display_name: Home team display name.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            GamePreviewResponse containing preview content and matchup
            analysis for the specified game.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/content/game/preview",
            operation_id="getGamePreview",
            request=models.GetGamePreviewRequest(
                season=season,
                season_type=season_type,
                week=week,
                visitor_display_name=visitor_display_name,
                home_display_name=home_display_name,
            ),
            response_type=models.GamePreviewResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_game_insights_config(
        self,
        *,
        season: int,
        fapi_game_id: str,
        away_team_id: str,
        home_team_id: str,
        limit: Optional[int] = 20,
        tags: Optional[str] = None,
        exclude_tags: Optional[str] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Game-Specific Insights

        Retrieves analytical insights and advanced statistics for a specific game.
        Can filter by tags and exclude specific content types.

        Args:
            season: Season year.
            fapi_game_id: FAPI Game identifier (UUID).
            away_team_id: Away team identifier.
            home_team_id: Home team identifier.
            limit: Maximum number of insights to return.
            tags: Comma-separated list of tags to filter by.
            exclude_tags: Comma-separated list of tags to exclude.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            List[GameInsight] containing analytical insights for the
            specified game.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/content/insights/game",
            operation_id="getGameInsights",
            request=models.GetGameInsightsRequest(
                season=season,
                limit=limit,
                tags=tags,
                exclude_tags=exclude_tags,
                fapi_game_id=fapi_game_id,
                away_team_id=away_team_id,
                home_team_id=home_team_id,
            ),
            response_type=List[models.GameInsight],
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
