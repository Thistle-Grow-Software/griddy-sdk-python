"""Leaders endpoints for Pro Football Reference.

Provides ``get()`` to fetch and parse PFR career, single-season, and
single-game statistical leaderboard pages.
"""

from typing import Optional

from griddy.pfr.parsers import LeadersParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import Leaderboard

_parser = LeadersParser()


class Leaders(BaseSDK):
    """Sub-SDK for PFR statistical leaders pages."""

    def _get_leaders_config(
        self,
        *,
        stat: str,
        scope: str,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/leaders/{stat}_{scope}.htm",
            operation_id="getLeaders",
            wait_for_element="table.stats_table",
            parser=lambda html: _parser.parse(html, stat=stat, scope=scope),
            response_type=Leaderboard,
            path_params={"stat": stat, "scope": scope},
            timeout_ms=timeout_ms,
        )

    def get(
        self,
        *,
        stat: str,
        scope: str,
        timeout_ms: Optional[int] = None,
    ) -> Leaderboard:
        """Fetch and parse a leaders page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/leaders/{stat}_{scope}.htm``
        and returns a structured leaderboard with player entries.

        Args:
            stat: Stat category slug (e.g. ``"pass_yds"``, ``"rush_td"``,
                ``"sacks"``, ``"def_int"``).
            scope: Leaderboard scope (e.g. ``"career"``,
                ``"single_season"``).
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.Leaderboard` instance.
        """
        config = self._get_leaders_config(stat=stat, scope=scope, timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return Leaderboard.model_validate(data)
