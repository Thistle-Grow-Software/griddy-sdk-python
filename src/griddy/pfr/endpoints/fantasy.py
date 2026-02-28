"""Fantasy endpoint for Pro Football Reference.

Provides ``get_top_players()`` to fetch and parse PFR fantasy ranking pages.
"""

from typing import Optional

from griddy.pfr.parsers.fantasy import FantasyParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import TopFantasyPlayers

_parser = FantasyParser()


class Fantasy(BaseSDK):
    """Sub-SDK for PFR Fantasy Rankings pages."""

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
