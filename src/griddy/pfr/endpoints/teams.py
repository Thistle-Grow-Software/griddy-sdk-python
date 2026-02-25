"""Team season endpoint for Pro Football Reference.

Provides ``get_team_season()`` to fetch and parse a PFR team season page
(``/teams/{team_abbrev}/{year}.htm``) and return structured team data
including roster, schedule/results, team stats, and player stats.
"""

from typing import Optional

from griddy.pfr.parsers import TeamSeasonParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import TeamSeason


class Teams(BaseSDK):
    """Sub-SDK for PFR team season data."""

    def _get_team_season_config(
        self,
        *,
        team: str,
        year: int,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/teams/{team}/{year}.htm",
            operation_id="getTeamSeason",
            wait_for_element="#games",
            parser=TeamSeasonParser().parse,
            response_type=TeamSeason,
            path_params={"team": team.lower(), "year": year},
            timeout_ms=timeout_ms,
        )

    def get_team_season(
        self,
        *,
        team: str,
        year: int,
        timeout_ms: Optional[int] = None,
    ) -> TeamSeason:
        """Fetch and parse a team season page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/teams/{team}/{year}.htm``
        using the Browserless ``/chromium/unblock`` API with a residential
        proxy, then connects via Playwright CDP to extract the fully-rendered
        HTML and parse it into structured team season data.

        Args:
            team: The PFR team abbreviation (e.g. ``"nwe"`` for New England
                Patriots). Case-insensitive; will be lowercased.
            year: The season year (e.g. ``2015``).
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.TeamSeason` instance containing
            the team's metadata, stats, game results, conversions,
            and player statistics.
        """
        config = self._get_team_season_config(
            team=team, year=year, timeout_ms=timeout_ms
        )
        data = self._execute_endpoint(config)
        return TeamSeason.model_validate(data)
