r"""Game-centric Pro endpoints including gamecenter stats, live scores, schedules, and results."""

from typing import Mapping, Optional

from griddy.core._constants import COLLECTION_ERROR_CODES, RESOURCE_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.pro import ProSDK
from griddy.nfl.endpoints.pro.mixins import (
    GameContentMixin,
    GameResultsDataMixin,
    GameScheduleMixin,
)
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class ProGames(ProSDK, GameScheduleMixin, GameContentMixin, GameResultsDataMixin):
    r"""Game-centric Pro endpoints including gamecenter stats, live scores, schedules, and results."""

    def _get_gamecenter_config(
        self,
        *,
        game_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        # NOTE: game_id corresponds to an int here.
        # You must use the UUID that is returned by all (or most?) other
        # API endpoints to query the /schedules/game endpoint (or possibly others?)
        # and use the gameId from _that_ response.
        r"""Get Gamecenter Statistics

        Retrieves advanced game statistics including passer zones, receiver separation,
        pass rush metrics, and performance leaders for a specific game.

        Args:
            game_id: Game identifier.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            GamecenterResponse containing advanced game statistics
            for the specified game.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/stats/gamecenter",
            operation_id="getGamecenter",
            request=models.GetGamecenterRequest(game_id=game_id),
            response_type=models.GamecenterResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    def _get_live_game_scores_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        week: int,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Live Game Scores

        Retrieves real-time scores and game status for all games in a specified week.
        This endpoint updates frequently (15-second cache) to provide live scoring updates
        during active games. Returns an empty array when no games are currently being played.

        Args:
            season: Season year.
            season_type: Type of season.
            week: Week number.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            LiveScoresResponse containing real-time scores and game status
            for all games in the specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/scores/live/games",
            operation_id="getLiveGameScores",
            request=models.GetLiveGameScoresRequest(
                season=season,
                season_type=season_type,
                week=week,
            ),
            response_type=models.LiveScoresResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )
