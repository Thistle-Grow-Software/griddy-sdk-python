"""Team endpoints for Pro Football Reference.

Provides ``get_team_season()`` to fetch and parse a PFR team season page
(``/teams/{team_abbrev}/{year}.htm``) and ``get_team_franchise()`` to fetch
and parse a PFR team franchise page (``/teams/{team_abbrev}/``).
"""

from typing import Optional

from griddy.pfr.parsers import TeamFranchiseParser, TeamSeasonParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import TeamFranchise, TeamSeason


class Teams(BaseSDK):
    """Sub-SDK for PFR team data (season and franchise pages)."""

    # ------------------------------------------------------------------
    # Team Season
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Team Franchise
    # ------------------------------------------------------------------

    def _get_team_franchise_config(
        self,
        *,
        team: str,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/teams/{team}/",
            operation_id="getTeamFranchise",
            wait_for_element="#team_index",
            parser=TeamFranchiseParser().parse,
            response_type=TeamFranchise,
            path_params={"team": team.lower()},
            timeout_ms=timeout_ms,
        )

    def get_team_franchise(
        self,
        *,
        team: str,
        timeout_ms: Optional[int] = None,
    ) -> TeamFranchise:
        """Fetch and parse a team franchise page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/teams/{team}/``
        using the Browserless ``/chromium/unblock`` API with a residential
        proxy, then connects via Playwright CDP to extract the fully-rendered
        HTML and parse it into structured franchise data.

        Args:
            team: The PFR team abbreviation (e.g. ``"nwe"`` for New England
                Patriots). Case-insensitive; will be lowercased.
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.TeamFranchise` instance containing
            the franchise metadata and year-by-year season records.
        """
        config = self._get_team_franchise_config(team=team, timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return TeamFranchise.model_validate(data)
