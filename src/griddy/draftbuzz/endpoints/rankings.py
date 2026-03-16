"""Rankings endpoints for NFL Draft Buzz.

Provides ``get_position_rankings()`` to fetch and parse position
ranking pages.
"""

from functools import cached_property
from typing import Optional

from griddy.core.decorators import sdk_endpoints
from griddy.draftbuzz.parsers import RankingsParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import PositionRankings


@sdk_endpoints
class Rankings(BaseSDK):
    """Sub-SDK for DraftBuzz position rankings pages."""

    @cached_property
    def _parser(self) -> RankingsParser:
        """Lazily instantiate and cache the rankings parser."""
        return RankingsParser()

    def _get_position_rankings_config(
        self,
        *,
        position: str,
        page: int = 1,
        year: int = 2026,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        r"""Fetch and parse a position rankings page from NFL Draft Buzz.

        Scrapes
        ``https://www.nfldraftbuzz.com/positions/{position}/{page}/{year}``
        and returns a list of ranked prospects for the given position.

        Args:
            position: The position to get rankings for (e.g. ``"QB"``).
            page: Page number (default 1).
            year: Draft year (default 2026).
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.draftbuzz.models.PositionRankings` instance
            containing all ranked prospects on the page.
        """
        parser = self._parser
        return EndpointConfig(
            path_template="/positions/{position}/{page}/{year}",
            operation_id="getPositionRankings",
            wait_for_element="#positionRankTable",
            parser=lambda html: parser.parse_position_rankings(
                html, position=position, year=year, page=page
            ),
            response_type=PositionRankings,
            path_params={
                "position": position,
                "page": page,
                "year": year,
            },
            timeout_ms=timeout_ms,
        )
