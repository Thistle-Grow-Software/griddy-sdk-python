"""Schedule endpoint for Pro Football Reference.

Provides ``get_season_schedule()`` to fetch and parse the PFR season
schedule page (``/years/{season}/games.htm``).
"""

from typing import List, Optional

from ..basesdk import BaseSDK, EndpointConfig
from ..models.entities.schedule_game import ScheduleGame
from ..utils.parsers import ScheduleParser


class Schedule(BaseSDK):
    """Sub-SDK for PFR season schedule data."""

    def _get_season_schedule_config(
        self,
        *,
        season: int,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/years/{season}/games.htm",
            operation_id="getSeasonSchedule",
            wait_for_element="#games",
            parser=ScheduleParser().parse,
            response_type=ScheduleGame,
            path_params={"season": season},
            timeout_ms=timeout_ms,
        )

    def get_season_schedule(
        self,
        *,
        season: int,
        timeout_ms: Optional[int] = None,
    ) -> List[ScheduleGame]:
        """Fetch and parse the season schedule from Pro Football Reference.

        Scrapes ``https://www.pro-football-reference.com/years/{season}/games.htm``
        using Browserless + Playwright, then parses the HTML table into
        structured game data.

        Args:
            season: The NFL season year (e.g. 2015, 2024).
            timeout_ms: Optional timeout in milliseconds for the page selector.

        Returns:
            A list of ``ScheduleGame`` models, one per game.
        """
        config = self._get_season_schedule_config(season=season, timeout_ms=timeout_ms)
        return self._execute_endpoint(config)
