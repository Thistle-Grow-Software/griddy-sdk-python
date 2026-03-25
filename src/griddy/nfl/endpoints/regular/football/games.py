"""Game endpoints for schedules, box scores, play-by-play, live stats, and weekly details."""

from typing import List, Mapping, Optional

from griddy.core._constants import COLLECTION_ERROR_CODES, RESOURCE_ERROR_CODES
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import BaseSDK, EndpointConfig
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class Games(BaseSDK):
    r"""Game endpoints for schedules, box scores, play-by-play, and live stats.

    Provides access to:
    - Game schedules by season, type, and week
    - Box score data for individual games
    - Play-by-play data with optional penalties and formations
    - Live game statistics and summaries
    - Weekly game details with drive charts and replays
    """

    def _get_games_config(
        self,
        *,
        season: int,
        season_type: models.SeasonTypeEnum,
        week: int,
        with_external_ids: Optional[bool] = False,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Games by Season, Type, and Week

        Retrieves game information for a specific season, season type, and week from the Football API.
        This endpoint provides core game data with external IDs.

        Args:
            season: Season year.
            season_type: Type of season.
            week: Week number.
            with_external_ids: Include external IDs in response.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            FootballGamesResponse containing game data for the specified
            season, type, and week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetFootballGamesRequest(
            season=season,
            season_type=season_type,
            week=week,
            with_external_ids=with_external_ids,
        )

        return EndpointConfig(
            method="GET",
            path="/football/v2/games/season/{season}/seasonType/{seasonType}/week/{week}",
            operation_id="getFootballGames",
            request=request,
            response_type=models.FootballGamesResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_box_score_config(
        self,
        *,
        game_id: str,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Game Box Score (Football API)

        Retrieves comprehensive box score data for a specific game including
        team statistics, individual player statistics, and scoring summary.

        Args:
            game_id: Game identifier (UUID).
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            ProBoxScoreResponse containing team statistics, individual player
            statistics, and scoring summary for the specified game.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetFootballBoxScoreRequest(game_id=game_id)

        return EndpointConfig(
            method="GET",
            path="/football/v2/games/{gameId}/boxscore",
            operation_id="getFootballBoxScore",
            request=request,
            response_type=models.ProBoxScoreResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_play_by_play_config(
        self,
        *,
        game_id: str,
        include_penalties: Optional[bool] = True,
        include_formations: Optional[bool] = False,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Play-by-Play Data

        Retrieves detailed play-by-play data for a specific game including
        all plays, drives, scoring events, and key statistics.

        Args:
            game_id: Game identifier (UUID).
            include_penalties: Include penalty details.
            include_formations: Include offensive/defensive formations.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            PlayByPlayResponse containing detailed play-by-play data
            including drives, plays, and scoring events.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetPlayByPlayRequest(
            game_id=game_id,
            include_penalties=include_penalties,
            include_formations=include_formations,
        )

        return EndpointConfig(
            method="GET",
            path="/football/v2/games/{gameId}/playbyplay",
            operation_id="getPlayByPlay",
            request=request,
            response_type=models.PlayByPlayResponse,
            error_status_codes=RESOURCE_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=True,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_live_game_stats_config(
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
        r"""Get Live Game Statistics

        Retrieves live game statistics and summaries for games in progress or completed games.
        Provides real-time statistical data for specified season, type, and week.

        Args:
            season: Season year.
            season_type: Type of season.
            week: Week number.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            GameStatsResponse containing live game statistics and summaries
            for the specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetLiveGameStatsRequest(
            season=season,
            season_type=season_type,
            week=week,
        )

        return EndpointConfig(
            method="GET",
            path="/football/v2/stats/live/game-summaries",
            operation_id="getLiveGameStats",
            request=request,
            response_type=models.GameStatsResponse,
            error_status_codes=COLLECTION_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=False,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_weekly_game_details_config(
        self,
        *,
        season: int,
        type_: models.SeasonTypeEnum,
        week: int,
        include_drive_chart: Optional[bool] = False,
        include_replays: Optional[bool] = False,
        include_standings: Optional[bool] = False,
        include_tagged_videos: Optional[bool] = False,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Weekly Game Details

        Retrieves detailed game information for a specific week including team standings,
        drive charts, replays, and tagged videos.

        Args:
            season: Season year.
            type_: Season type.
            week: Week number.
            include_drive_chart: Include drive chart data.
            include_replays: Include replay videos.
            include_standings: Include team standings.
            include_tagged_videos: Include tagged video content.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration
                for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            List[WeeklyGameDetail] containing detailed game information
            for each game in the specified week.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        request = models.GetWeeklyGameDetailsRequest(
            season=season,
            type=type_,
            week=week,
            include_drive_chart=include_drive_chart,
            include_replays=include_replays,
            include_standings=include_standings,
            include_tagged_videos=include_tagged_videos,
        )

        return EndpointConfig(
            method="GET",
            path="/football/v2/experience/weekly-game-details",
            operation_id="getWeeklyGameDetails",
            request=request,
            response_type=List[models.WeeklyGameDetail],
            error_status_codes=COLLECTION_ERROR_CODES,
            request_body_required=False,
            request_has_path_params=False,
            request_has_query_params=True,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )
