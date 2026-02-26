"""Super Bowl endpoint for Pro Football Reference.

Provides ``history()``, ``leaders()``, and ``standings()`` to fetch and parse
PFR Super Bowl pages.
"""

from typing import Optional

from griddy.pfr.parsers.superbowl import SuperBowlParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import SuperBowlHistory, SuperBowlLeaders, SuperBowlStandings

_parser = SuperBowlParser()


class SuperBowl(BaseSDK):
    """Sub-SDK for PFR Super Bowl pages."""

    def _get_history_config(
        self,
        *,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/super-bowl/",
            operation_id="getSuperBowlHistory",
            wait_for_element="#super_bowls",
            parser=lambda html: _parser.parse_history(html),
            response_type=SuperBowlHistory,
            path_params={},
            timeout_ms=timeout_ms,
        )

    def history(
        self,
        *,
        timeout_ms: Optional[int] = None,
    ) -> SuperBowlHistory:
        """Fetch and parse the Super Bowl history page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/super-bowl/``
        and returns structured data for every Super Bowl game.

        Args:
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.SuperBowlHistory` instance containing
            all Super Bowl game entries.
        """
        config = self._get_history_config(timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return SuperBowlHistory.model_validate(data)

    def _get_leaders_config(
        self,
        *,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/super-bowl/leaders.htm",
            operation_id="getSuperBowlLeaders",
            wait_for_element="table",
            parser=lambda html: _parser.parse_leaders(html),
            response_type=SuperBowlLeaders,
            path_params={},
            timeout_ms=timeout_ms,
        )

    def leaders(
        self,
        *,
        timeout_ms: Optional[int] = None,
    ) -> SuperBowlLeaders:
        """Fetch and parse the Super Bowl leaders page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/super-bowl/leaders.htm``
        and returns career and single-game statistical leaderboards.

        Args:
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.SuperBowlLeaders` instance containing
            all leaderboard tables.
        """
        config = self._get_leaders_config(timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return SuperBowlLeaders.model_validate(data)

    def _get_standings_config(
        self,
        *,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/super-bowl/standings.htm",
            operation_id="getSuperBowlStandings",
            wait_for_element="#standings",
            parser=lambda html: _parser.parse_standings(html),
            response_type=SuperBowlStandings,
            path_params={},
            timeout_ms=timeout_ms,
        )

    def standings(
        self,
        *,
        timeout_ms: Optional[int] = None,
    ) -> SuperBowlStandings:
        """Fetch and parse the Super Bowl standings page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/super-bowl/standings.htm``
        and returns franchise Super Bowl standings with win/loss records.

        Args:
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.SuperBowlStandings` instance
            containing all franchise standings entries.
        """
        config = self._get_standings_config(timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return SuperBowlStandings.model_validate(data)
