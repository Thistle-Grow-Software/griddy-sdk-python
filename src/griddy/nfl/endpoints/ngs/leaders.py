"""NGS Leaders endpoints for top plays and leaderboards."""

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
class NgsLeaders(NgsBaseSDK):
    """NGS Leaders endpoints for top plays and leaderboards.

    Provides access to:
    - Fastest ball carriers (max speed)
    - Fastest sacks (time to sack)
    - Improbable completions (completion probability)
    - Incredible YAC (yards after catch over expectation)
    - Longest plays (in-play distance)
    - Longest tackles (distance covered to tackle)
    - Remarkable rushes (rush yards over expected)
    """

    def _get_fastest_ball_carriers_config(
        self,
        *,
        season: int,
        season_type: str,
        limit: int = 20,
        week: Optional[int] = None,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get fastest ball carrier speeds.

        Returns leaderboard of fastest ball carrier speeds recorded.

        Args:
            season: Season year (e.g., 2025).
            season_type: Season type (REG, PRE, POST).
            limit: Number of results (default: 20).
            week: Optional week filter.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/leaders/speed/ballCarrier",
            operation_id="getNgsFastestBallCarriers",
            request=models.GetNgsLeadersRequest(
                season=season, season_type=season_type, limit=limit, week=week
            ),
            response_type=models.NgsSpeedLeadersResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_fastest_sacks_config(
        self,
        *,
        season: int,
        season_type: str,
        limit: int = 20,
        week: Optional[int] = None,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get fastest sack times.

        Returns leaderboard of quickest sacks by time to tackle.

        Args:
            season: Season year (e.g., 2025).
            season_type: Season type (REG, PRE, POST).
            limit: Number of results (default: 20).
            week: Optional week filter.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/leaders/time/sack",
            operation_id="getNgsFastestSacks",
            request=models.GetNgsLeadersRequest(
                season=season, season_type=season_type, limit=limit, week=week
            ),
            response_type=models.NgsSackLeadersResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_improbable_completions_config(
        self,
        *,
        season: int,
        season_type: str,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get most improbable completions.

        Returns leaderboard of completions with lowest completion probability.

        Args:
            season: Season year (e.g., 2025).
            season_type: Season type (REG, PRE, POST).

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/leaders/expectation/completion/season",
            operation_id="getNgsImprobableCompletions",
            request=models.GetNgsSeasonLeadersRequest(
                season=season, season_type=season_type
            ),
            response_type=models.NgsCompletionLeadersResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_incredible_yac_config(
        self,
        *,
        season: int,
        season_type: str,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get incredible YAC plays.

        Returns leaderboard of yards after catch over expectation.

        Args:
            season: Season year (e.g., 2025).
            season_type: Season type (REG, PRE, POST).

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/leaders/expectation/yac/season",
            operation_id="getNgsIncredibleYAC",
            request=models.GetNgsSeasonLeadersRequest(
                season=season, season_type=season_type
            ),
            response_type=models.NgsYACLeadersResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_longest_plays_config(
        self,
        *,
        season: int,
        season_type: str,
        limit: int = 20,
        week: Optional[int] = None,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get longest plays by in-play distance.

        Returns leaderboard of plays with most distance covered.

        Args:
            season: Season year (e.g., 2025).
            season_type: Season type (REG, PRE, POST).
            limit: Number of results (default: 20).
            week: Optional week filter.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/leaders/distance/ballCarrier",
            operation_id="getNgsLongestPlays",
            request=models.GetNgsLeadersRequest(
                season=season, season_type=season_type, limit=limit, week=week
            ),
            response_type=models.NgsDistanceLeadersResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_longest_tackles_config(
        self,
        *,
        season: int,
        season_type: str,
        limit: int = 20,
        week: Optional[int] = None,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get longest tackles by distance covered.

        Returns leaderboard of tackles with most distance covered to make the tackle.

        Args:
            season: Season year (e.g., 2025).
            season_type: Season type (REG, PRE, POST).
            limit: Number of results (default: 20).
            week: Optional week filter.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/leaders/distance/tackle",
            operation_id="getNgsLongestTackles",
            request=models.GetNgsLeadersRequest(
                season=season, season_type=season_type, limit=limit, week=week
            ),
            response_type=models.NgsTackleLeadersResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_remarkable_rushes_config(
        self,
        *,
        season: int,
        season_type: str,
        retries: OptionalNullable[RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        """Get remarkable rushes.

        Returns leaderboard of rush yards over expected (ERY).

        Args:
            season: Season year (e.g., 2025).
            season_type: Season type (REG, PRE, POST).

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/leaders/expectation/ery/season",
            operation_id="getNgsRemarkableRushes",
            request=models.GetNgsSeasonLeadersRequest(
                season=season, season_type=season_type
            ),
            response_type=models.NgsERYLeadersResponse,
            error_status_codes=NGS_ERROR_CODES,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )
