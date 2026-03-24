r"""Film room content, editorial insights, and coaches film video endpoints."""

from typing import List, Mapping, Optional

from griddy.core._constants import (
    COLLECTION_ERROR_CODES,
    PARAMETERLESS_ERROR_CODES,
    SECURED_RESOURCE_ERROR_CODES,
    STATS_ERROR_CODES,
)
from griddy.core.decorators import sdk_endpoints
from griddy.nfl import models, utils
from griddy.nfl.basesdk import EndpointConfig
from griddy.nfl.endpoints.pro import ProSDK
from griddy.nfl.endpoints.pro.mixins import GameContentMixin
from griddy.nfl.types import UNSET, OptionalNullable


@sdk_endpoints
class Content(ProSDK, GameContentMixin):
    r"""Film room content, editorial insights, and coaches film video endpoints."""

    def _get_home_film_cards_config(
        self,
        *,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Home Film Cards

        Retrieves featured film room content cards for the home page.
        Returns weekly playlists and featured player film breakdowns.

        Args:
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            HomeFilmCardsResponse containing featured film room content cards.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/content/home-film-cards",
            operation_id="getHomeFilmCards",
            request=None,
            response_type=models.HomeFilmCardsResponse,
            error_status_codes=PARAMETERLESS_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_season_insights_config(
        self,
        *,
        season: int,
        limit: Optional[int] = 20,
        tags: Optional[List[models.Tag]] = None,
        team_id: Optional[str] = None,
        nfl_id: Optional[str] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        r"""Get Season Content Insights

        Retrieves curated editorial insights and analytics content for NFL players during
        a specified season. Returns expert commentary combining Next Gen Stats data with
        editorial analysis, including pregame previews, postgame breakdowns, fantasy insights,
        and evergreen content. Supports filtering by player, team, content tags, and publication
        limits for targeted content discovery.

        Args:
            season: Season year.
            limit: Maximum number of insights to return.
            tags: Content tags to filter by (supports multiple comma-separated tags).
            team_id: Filter by specific team identifier.
            nfl_id: Filter by specific player NFL identifier.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            List[Insight] containing curated editorial insights for the
            specified season.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/content/insights/season",
            operation_id="getSeasonContentInsights",
            request=models.GetSeasonContentInsightsRequest(
                season=season,
                limit=limit,
                tags=tags,
                team_id=team_id,
                nfl_id=nfl_id,
            ),
            response_type=List[models.Insight],
            error_status_codes=COLLECTION_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
            return_raw_json=False,
        )

    # TODO: Consider how this method signature might be cleaned up
    def _get_filmroom_plays_config(
        self,
        *,
        game_id: Optional[List[str]] = None,
        week_slug: Optional[List[models.WeekSlugEnum]] = None,
        season: Optional[List[int]] = None,
        season_type: Optional[List[models.SeasonTypeEnum]] = None,
        nfl_id: Optional[List[str]] = None,
        quarter: Optional[List[int]] = None,
        down: Optional[List[int]] = None,
        yards_to_go_type: Optional[List[models.YardsToGoType]] = None,
        touchdown: Optional[List[models.BinaryFlagEnum]] = None,
        rush10_plus_yards: Optional[List[models.BinaryFlagEnum]] = None,
        fumble_lost: Optional[List[models.BinaryFlagEnum]] = None,
        fumble: Optional[List[models.BinaryFlagEnum]] = None,
        qb_alignment: Optional[List[models.QbAlignment]] = None,
        redzone: Optional[List[models.BinaryFlagEnum]] = None,
        goal_to_go: Optional[List[models.BinaryFlagEnum]] = None,
        pass_play: Optional[List[models.BinaryFlagEnum]] = None,
        run_play: Optional[List[models.BinaryFlagEnum]] = None,
        play_type: Optional[List[models.PlayTypeEnum]] = None,
        attempt: Optional[List[models.BinaryFlagEnum]] = None,
        completion: Optional[List[models.BinaryFlagEnum]] = None,
        interception: Optional[List[models.BinaryFlagEnum]] = None,
        reception: Optional[List[models.BinaryFlagEnum]] = None,
        sack: Optional[List[models.BinaryFlagEnum]] = None,
        rec_motion: Optional[List[models.BinaryFlagEnum]] = None,
        target_location: Optional[List[models.TargetLocation]] = None,
        air_yard_type: Optional[List[models.AirYardType]] = None,
        dropback_time_type: Optional[List[models.DropbackTimeType]] = None,
        pressure: Optional[List[models.BinaryFlagEnum]] = None,
        blitz: Optional[List[models.BinaryFlagEnum]] = None,
        play_action: Optional[List[models.BinaryFlagEnum]] = None,
        rush_direction: Optional[List[models.RushDirection]] = None,
        run_stuff: Optional[List[models.BinaryFlagEnum]] = None,
        receiver_alignment: Optional[List[models.ReceiverAlignment]] = None,
        separation_type: Optional[List[models.SeparationType]] = None,
        personnel: Optional[List[models.Personnel]] = None,
        defenders_in_the_box_type: Optional[List[models.DefendersInTheBoxType]] = None,
        def_coverage_type: Optional[List[models.DefCoverageType]] = None,
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        # Note that the actual video file itself is acquired by:
        # 1.) Extract the mcpPlaybackId of the game
        # 2.) Using it (and other stuff I've yet to dechipher the meaning of
        #       to send a POST request to https://api.nfl.com/play/v1/asset/<mcpPlaybackId>
        # This request will return a JSON response with:
        # accessUrl, init, and metadata fields
        r"""Get Filmroom Plays with Advanced Filtering

        Retrieves detailed play-by-play data with extensive filtering capabilities for film study.
        Returns comprehensive play information including formations, personnel packages, game situations,
        and detailed play descriptions. This endpoint supports advanced filtering by game situation,
        player involvement, formation types, and tactical elements.

        Args:
            game_id: Filter by specific game IDs (supports multiple values).
            week_slug: Filter by week identifier (supports multiple values).
            season: Filter by season year (supports multiple values).
            season_type: Filter by season type.
            nfl_id: Filter by player NFL ID.
            quarter: Filter by quarter.
            down: Filter by down.
            yards_to_go_type: Filter by yards to go category.
            touchdown: Filter for touchdown plays (1 = yes, 0 = no).
            rush10_plus_yards: Filter for rushing plays of 10+ yards.
            fumble_lost: Filter for plays with fumbles lost.
            fumble: Filter for plays with fumbles.
            qb_alignment: Filter by quarterback alignment.
            redzone: Filter for red zone plays.
            goal_to_go: Filter for goal-to-go situations.
            pass_play: Filter for passing plays.
            run_play: Filter for running plays.
            play_type: Filter by specific play types.
            attempt: Filter for passing attempts.
            completion: Filter for completed passes.
            interception: Filter for interceptions.
            reception: Filter for receptions.
            sack: Filter for sacks.
            rec_motion: Filter by receiver motion.
            target_location: Filter by target location on field.
            air_yard_type: Filter by air yards category.
            dropback_time_type: Filter by dropback time.
            pressure: Filter by quarterback pressure.
            blitz: Filter by defensive blitz.
            play_action: Filter by play action usage.
            rush_direction: Filter by rush direction.
            run_stuff: Filter for stuffed runs.
            receiver_alignment: Filter by receiver alignment.
            separation_type: Filter by receiver separation.
            personnel: Filter by defensive personnel package.
            defenders_in_the_box_type: Filter by defenders in the box.
            def_coverage_type: Filter by defensive coverage type.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            FilmroomPlaysResponse containing play-by-play data matching
            the specified filters.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/videos/filmroom/plays",
            operation_id="getFilmroomPlays",
            request=models.GetFilmroomPlaysRequest(
                game_id=game_id,
                week_slug=week_slug,
                season=season,
                season_type=season_type,
                nfl_id=nfl_id,
                quarter=quarter,
                down=down,
                yards_to_go_type=yards_to_go_type,
                touchdown=touchdown,
                rush10_plus_yards=rush10_plus_yards,
                fumble_lost=fumble_lost,
                fumble=fumble,
                qb_alignment=qb_alignment,
                redzone=redzone,
                goal_to_go=goal_to_go,
                pass_play=pass_play,
                run_play=run_play,
                play_type=play_type,
                attempt=attempt,
                completion=completion,
                interception=interception,
                reception=reception,
                sack=sack,
                rec_motion=rec_motion,
                target_location=target_location,
                air_yard_type=air_yard_type,
                dropback_time_type=dropback_time_type,
                pressure=pressure,
                blitz=blitz,
                play_action=play_action,
                rush_direction=rush_direction,
                run_stuff=run_stuff,
                receiver_alignment=receiver_alignment,
                separation_type=separation_type,
                personnel=personnel,
                defenders_in_the_box_type=defenders_in_the_box_type,
                def_coverage_type=def_coverage_type,
            ),
            response_type=models.FilmroomPlaysResponse,
            error_status_codes=STATS_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )

    def _get_coaches_film_videos_config(
        self,
        *,
        game_id: List[str],
        play_id: List[str],
        retries: OptionalNullable[utils.RetryConfig] = UNSET,
        server_url: Optional[str] = None,
        timeout_ms: Optional[int] = None,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> EndpointConfig:
        # Note that the game_id used in this request
        # corresponds to the Game's UUID often labeled fapi_game_id by the NFL.
        # Why is it different? Nobody knows
        r"""Get Coaches Film Videos

        Retrieves premium coaches film video content for specified games and plays.
        Returns multiple camera angles (endzone, sideline, broadcast) for each play,
        providing comprehensive film study material. Requires NFL Plus Premium subscription
        and appropriate geographic restrictions apply (US only).

        Args:
            game_id: Game identifiers (UUID format, supports multiple games).
            play_id: Play identifiers for specific plays within the games.
            retries: Override the default retry configuration for this method.
            server_url: Override the default server URL for this method.
            timeout_ms: Override the default request timeout configuration for this method in milliseconds.
            http_headers: Additional headers to set or replace on requests.

        Returns:
            CoachesFilmResponse containing multi-angle video content
            for the specified plays.

        Raises:
            APIError: If the API returns an unexpected error response.
            AuthenticationError: If the request is not properly authenticated.
            RateLimitError: If the API rate limit is exceeded.
            NotFoundError: If the requested resource does not exist.
        """
        return EndpointConfig(
            method="GET",
            path="/api/secured/videos/coaches",
            operation_id="getCoachesFilmVideos",
            request=models.GetCoachesFilmVideosRequest(
                game_id=game_id,
                play_id=play_id,
            ),
            response_type=models.CoachesFilmResponse,
            error_status_codes=SECURED_RESOURCE_ERROR_CODES,
            server_url=server_url,
            timeout_ms=timeout_ms,
            http_headers=http_headers,
            retries=retries,
        )
