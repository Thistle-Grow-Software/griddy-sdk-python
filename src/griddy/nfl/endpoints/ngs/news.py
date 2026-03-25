"""NGS News endpoints for articles and videos.

Note: These endpoints use a different server (api.nfl.com) than the other NGS endpoints.
"""

from __future__ import annotations

from typing import Mapping, Optional

from griddy.core._constants import NGS_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models
from griddy.nfl.basesdk import BaseSDK, EndpointConfig
from griddy.nfl.sdkconfiguration import SERVERS
from griddy.nfl.types import UNSET, OptionalNullable
from griddy.nfl.utils import RetryConfig

# NFL Content API server URL (different from NGS server)
NFL_API_SERVER_URL = SERVERS["regular"]


@sdk_endpoints
class NgsNews(BaseSDK):
    """NGS News endpoints for articles and videos.

    Note: This sub-SDK uses api.nfl.com instead of nextgenstats.nfl.com.

    Provides access to:
    - Mixed content (articles and videos)
    - Articles
    - Video clips
    """

    def _resolve_base_url(
        self,
        server_url: Optional[str] = None,
        url_variables: Optional[dict] = None,
    ) -> str:
        """Override to use NFL API server for news endpoints."""
        if server_url is not None:
            return server_url
        return NFL_API_SERVER_URL

    def _get_mixed_content_config(
        self,
        *,
        limit: int = 16,
        offset: int = 0,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get mixed NGS content (articles and videos).

        Args:
            limit: Number of items to return (default: 16).
            offset: Offset for pagination (default: 0).

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/content/v1/mixed/next-gen-stats",
            operation_id="getNgsMixedContent",
            request=models.GetNgsMixedContentRequest(limit=limit, offset=offset),
            response_type=models.NgsMixedContentResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_articles_config(
        self,
        *,
        category: str = "next-gen-stats-news",
        limit: int = 16,
        offset: int = 0,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get NGS articles.

        Args:
            category: Article category slug (default: "next-gen-stats-news").
            limit: Number of items to return (default: 16).
            offset: Offset for pagination (default: 0).

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/content/v1/articles",
            operation_id="getNgsArticles",
            request=models.GetNgsArticlesRequest(
                category=category, limit=limit, offset=offset
            ),
            response_type=models.NgsArticlesResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_video_clips_config(
        self,
        *,
        video_channel: str = "next-gen-stats-vc",
        limit: int = 16,
        offset: int = 0,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get NGS video clips.

        Args:
            video_channel: Video channel slug (default: "next-gen-stats-vc").
            limit: Number of items to return (default: 16).
            offset: Offset for pagination (default: 0).

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/content/v1/videos/clips",
            operation_id="getNgsVideoClips",
            request=models.GetNgsVideoClipsRequest(
                video_channel=video_channel, limit=limit, offset=offset
            ),
            response_type=models.NgsVideosResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )
