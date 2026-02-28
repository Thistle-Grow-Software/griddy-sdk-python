"""Fantasy endpoint for Pro Football Reference.

Provides:
- ``get_top_players()`` — Top Fantasy Players (``/years/{year}/fantasy.htm``)
- ``get_matchups()`` — Fantasy Matchups
  (``/fantasy/{position}-fantasy-matchups.htm``)
- ``get_points_allowed()`` — Fantasy Points Allowed
  (``/years/{year}/fantasy-points-against-{position}.htm``)
"""

from typing import Literal, Optional

from griddy.pfr.parsers.fantasy import FantasyParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import FantasyMatchups, FantasyPointsAllowed, TopFantasyPlayers

_parser = FantasyParser()

PositionLiteral = Literal["qb", "wr", "rb", "te"]


class Fantasy(BaseSDK):
    """Sub-SDK for PFR Fantasy Rankings pages."""

    # ── Top Players ──────────────────────────────────────────────────

    def _get_top_players_config(
        self,
        *,
        year: int,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/years/{year}/fantasy.htm",
            operation_id="getTopFantasyPlayers",
            wait_for_element="#fantasy",
            parser=lambda html: _parser.parse_top_players(html),
            response_type=TopFantasyPlayers,
            path_params={"year": year},
            timeout_ms=timeout_ms,
        )

    def get_top_players(
        self,
        *,
        year: int,
        timeout_ms: Optional[int] = None,
    ) -> TopFantasyPlayers:
        """Fetch and parse the Top Fantasy Players page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/years/{year}/fantasy.htm``
        and returns structured data for every player's fantasy rankings.

        Args:
            year: The NFL season year (e.g. 2025).
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.TopFantasyPlayers` instance containing
            all player entries.
        """
        config = self._get_top_players_config(year=year, timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return TopFantasyPlayers.model_validate(data)

    # ── Matchups ─────────────────────────────────────────────────────

    def _get_matchups_config(
        self,
        *,
        position: PositionLiteral,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/fantasy/{position}-fantasy-matchups.htm",
            operation_id="getFantasyMatchups",
            wait_for_element="#fantasy_stats",
            parser=lambda html: _parser.parse_matchups(html),
            response_type=FantasyMatchups,
            path_params={"position": position},
            timeout_ms=timeout_ms,
        )

    def get_matchups(
        self,
        *,
        position: PositionLiteral,
        timeout_ms: Optional[int] = None,
    ) -> FantasyMatchups:
        """Fetch and parse a Fantasy Matchups page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/fantasy/{position}-fantasy-matchups.htm``
        and returns per-game averages, matchup info, and projected ranks.

        Args:
            position: The position to fetch matchups for.
                One of ``"qb"``, ``"wr"``, ``"rb"``, or ``"te"``.
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.FantasyMatchups` instance containing
            all player matchup entries.
        """
        config = self._get_matchups_config(position=position, timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return FantasyMatchups.model_validate(data)

    # ── Points Allowed ────────────────────────────────────────────────

    def _get_points_allowed_config(
        self,
        *,
        year: int,
        position: PositionLiteral,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/years/{year}/fantasy-points-against-{position}.htm",
            operation_id="getFantasyPointsAllowed",
            wait_for_element="#fantasy_def",
            parser=lambda html: _parser.parse_points_allowed(html),
            response_type=FantasyPointsAllowed,
            path_params={"year": year, "position": position},
            timeout_ms=timeout_ms,
        )

    def get_points_allowed(
        self,
        *,
        year: int,
        position: PositionLiteral,
        timeout_ms: Optional[int] = None,
    ) -> FantasyPointsAllowed:
        """Fetch and parse a Fantasy Points Allowed page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/years/{year}/fantasy-points-against-{position}.htm``
        and returns team-level defensive fantasy stats for the given position.

        Args:
            year: The NFL season year (e.g. 2025).
            position: The position to fetch points allowed for.
                One of ``"qb"``, ``"wr"``, ``"rb"``, or ``"te"``.
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.FantasyPointsAllowed` instance
            containing all team entries.
        """
        config = self._get_points_allowed_config(
            year=year, position=position, timeout_ms=timeout_ms
        )
        data = self._execute_endpoint(config)
        return FantasyPointsAllowed.model_validate(data)
