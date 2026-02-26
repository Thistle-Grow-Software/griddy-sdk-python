"""Draft endpoints for Pro Football Reference.

Provides ``year()``, ``combine()``, and ``team()`` to fetch and parse
PFR draft-related pages.
"""

from typing import Optional

from griddy.pfr.parsers import DraftParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import CombineResults, TeamDraft, YearDraft

_parser = DraftParser()


class Draft(BaseSDK):
    """Sub-SDK for PFR NFL Draft pages."""

    # ------------------------------------------------------------------
    # Year Draft — /years/{year}/draft.htm
    # ------------------------------------------------------------------

    def _get_year_config(
        self,
        *,
        year: int,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/years/{year}/draft.htm",
            operation_id="getYearDraft",
            wait_for_element="#drafts",
            parser=lambda html: _parser.parse_year_draft(html, year=year),
            response_type=YearDraft,
            path_params={"year": year},
            timeout_ms=timeout_ms,
        )

    def year(
        self,
        *,
        year: int,
        timeout_ms: Optional[int] = None,
    ) -> YearDraft:
        """Fetch and parse a draft year page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/years/{year}/draft.htm``
        and returns structured draft pick data including career stats.

        Args:
            year: The draft year (e.g. ``2024``).
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.YearDraft` instance containing
            all draft picks for the given year.
        """
        config = self._get_year_config(year=year, timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return YearDraft.model_validate(data)

    # ------------------------------------------------------------------
    # Combine — /draft/{year}-combine.htm
    # ------------------------------------------------------------------

    def _get_combine_config(
        self,
        *,
        year: int,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/draft/{year}-combine.htm",
            operation_id="getCombine",
            wait_for_element="#combine",
            parser=lambda html: _parser.parse_combine(html, year=year),
            response_type=CombineResults,
            path_params={"year": year},
            timeout_ms=timeout_ms,
        )

    def combine(
        self,
        *,
        year: int,
        timeout_ms: Optional[int] = None,
    ) -> CombineResults:
        """Fetch and parse a combine page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/draft/{year}-combine.htm``
        and returns structured combine measurement data.

        Args:
            year: The combine year (e.g. ``2024``).
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.CombineResults` instance
            containing all combine entries for the given year.
        """
        config = self._get_combine_config(year=year, timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return CombineResults.model_validate(data)

    # ------------------------------------------------------------------
    # Team Draft — /teams/{team}/draft.htm
    # ------------------------------------------------------------------

    def _get_team_config(
        self,
        *,
        team: str,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/teams/{team}/draft.htm",
            operation_id="getTeamDraft",
            wait_for_element="#draft",
            parser=lambda html: _parser.parse_team_draft(html, team=team),
            response_type=TeamDraft,
            path_params={"team": team.lower()},
            timeout_ms=timeout_ms,
        )

    def team(
        self,
        *,
        team: str,
        timeout_ms: Optional[int] = None,
    ) -> TeamDraft:
        """Fetch and parse a team draft history page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/teams/{team}/draft.htm``
        and returns structured draft history data for the given team.

        Args:
            team: The PFR team abbreviation (e.g. ``"phi"`` for
                Philadelphia Eagles). Case-insensitive; will be lowercased.
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.TeamDraft` instance containing
            all draft picks for the given team.
        """
        config = self._get_team_config(team=team, timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return TeamDraft.model_validate(data)
