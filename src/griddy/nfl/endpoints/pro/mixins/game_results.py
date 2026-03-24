r"""Mixin providing game results, boxscores, play data, and win probability endpoints."""

from typing import List, Mapping, Optional

from griddy.core._constants import RESOURCE_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class GameResultsDataMixin:
    """Mixin for game results and play data endpoints."""

    def _get_stats_boxscore_config(
        self,
        *,
        game_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Game Boxscore (Stats API)

        Retrieves comprehensive boxscore data for a specific game including team statistics,
        individual player statistics, and scoring summary. Returns empty arrays for future games.

        Args:
            game_id: Game identifier (10-digit format YYYYMMDDNN).
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            BoxscoreResponse containing comprehensive boxscore data
            for the specified game.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/stats/boxscore",
            operation_id="getStatsBoxscore",
            request=models.GetStatsBoxscoreRequest(game_id=game_id),
            response_type=models.BoxscoreResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_playlist_config(
        self,
        *,
        game_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Game Playlist.

        Args:
            game_id: Game identifier(s) in 10-digit format (YYYYMMDDNN). Can be a single game ID or multiple game IDs for batch retrieval.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            PlaylistResponse containing playlist data for the specified game.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/plays/playlist/game",
            operation_id="getPlaysWinProbability",
            request=models.GetPlayListRequest(game_id=game_id),
            response_type=models.PlaylistResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_summary_play_config(
        self,
        *,
        game_id: str,
        play_id: int,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Play Summary

        Retrieves detailed information about a specific play in a game including play description,
        statistics, involved players, win probability, and expected points.

        Args:
            game_id: Game identifier (UUID format).
            play_id: Play identifier within the game.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            PlaySummaryResponse containing detailed information about the
            specified play.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/plays/summaryPlay",
            operation_id="getSummaryPlay",
            request=models.GetSummaryPlayRequest(
                game_id=game_id,
                play_id=play_id,
            ),
            response_type=models.PlaySummaryResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_plays_win_probability_config(
        self,
        *,
        game_id: models.GameID,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Game Win Probability by Plays

        Retrieves comprehensive win probability data for every play in specified games.
        Returns pre-game win probabilities and detailed play-by-play probability changes,
        including Win Probability Added (WPA) metrics for each play. This advanced analytics
        endpoint tracks how each play impacts the probability of each team winning the game.
        Supports querying multiple games simultaneously.

        Args:
            game_id: Game identifier(s) in 10-digit format (YYYYMMDDNN). Can be a single game ID or multiple game IDs for batch retrieval.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            PlayWinProbabilityResponse containing win probability data
            for every play in the specified games.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/plays/winProbability",
            operation_id="getPlaysWinProbability",
            request=models.GetPlaysWinProbabilityRequest(game_id=game_id),
            response_type=models.PlayWinProbabilityResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_win_probability_min_config(
        self,
        *,
        fapi_game_id: List[str],
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Minimal Win Probability Data

        Retrieves minimal win probability data for specified games, including pregame
        win probabilities and play-by-play probability changes throughout the game.
        This endpoint provides essential win probability metrics with optimized data
        structure for performance. Supports multiple games in a single request.

        Args:
            fapi_game_id: Football API game identifiers (UUID format). Supports multiple game IDs to retrieve win probability data for multiple games simultaneously.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            WinProbabilityResponse containing minimal win probability data
            for the specified games.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/plays/winProbabilityMin",
            operation_id="getWinProbabilityMin",
            request=models.GetWinProbabilityMinRequest(fapi_game_id=fapi_game_id),
            response_type=models.WinProbabilityResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
