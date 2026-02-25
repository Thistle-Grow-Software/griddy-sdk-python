"""Season endpoints for Pro Football Reference.

Provides ``get_season()`` and ``get_season_stats()`` to fetch and parse
PFR season overview and stat category pages.
"""

from typing import Optional

from griddy.pfr.parsers import SeasonOverviewParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import SeasonOverview, SeasonStats

_parser = SeasonOverviewParser()


class Seasons(BaseSDK):
    """Sub-SDK for PFR season data."""

    def _get_season_config(
        self,
        *,
        year: int,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/years/{year}/",
            operation_id="getSeason",
            wait_for_element="#AFC",
            parser=_parser.parse,
            response_type=SeasonOverview,
            path_params={"year": year},
            timeout_ms=timeout_ms,
        )

    def get_season(
        self,
        *,
        year: int,
        timeout_ms: Optional[int] = None,
    ) -> SeasonOverview:
        """Fetch and parse a season overview page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/years/{year}/``
        and returns structured season data including conference standings,
        playoff results, and team stats.

        Args:
            year: The NFL season year (e.g. ``2024``).
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.SeasonOverview` instance.
        """
        config = self._get_season_config(year=year, timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return SeasonOverview.model_validate(data)

    def _get_season_stats_config(
        self,
        *,
        year: int,
        category: str,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/years/{year}/{category}.htm",
            operation_id="getSeasonStats",
            wait_for_element="table",
            parser=_parser.parse_stats,
            response_type=SeasonStats,
            path_params={"year": year, "category": category},
            timeout_ms=timeout_ms,
        )

    def get_season_stats(
        self,
        *,
        year: int,
        category: str,
        timeout_ms: Optional[int] = None,
    ) -> SeasonStats:
        """Fetch and parse a season stat category page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/years/{year}/{category}.htm``
        and returns per-player stats for the given category.

        Args:
            year: The NFL season year (e.g. ``2024``).
            category: Stat category slug (e.g. ``"passing"``, ``"rushing"``,
                ``"receiving"``, ``"defense"``, ``"kicking"``, ``"punting"``,
                ``"returns"``, ``"scoring"``, ``"fantasy"``).
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.SeasonStats` instance.
        """
        config = self._get_season_stats_config(
            year=year, category=category, timeout_ms=timeout_ms
        )
        data = self._execute_endpoint(config)
        return SeasonStats.model_validate(data)
