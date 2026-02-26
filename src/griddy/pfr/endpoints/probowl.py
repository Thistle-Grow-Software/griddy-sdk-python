"""Pro Bowl endpoint for Pro Football Reference.

Provides ``year()`` to fetch and parse PFR Pro Bowl roster pages.
"""

from typing import Optional

from griddy.pfr.parsers import AwardsParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import ProBowlRoster

_parser = AwardsParser()


class ProBowl(BaseSDK):
    """Sub-SDK for PFR Pro Bowl roster pages."""

    def _get_year_config(
        self,
        *,
        year: int,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/years/{year}/probowl.htm",
            operation_id="getProBowlRoster",
            wait_for_element="#pro_bowl",
            parser=lambda html: _parser.parse_probowl(html, year=year),
            response_type=ProBowlRoster,
            path_params={"year": year},
            timeout_ms=timeout_ms,
        )

    def year(
        self,
        *,
        year: int,
        timeout_ms: Optional[int] = None,
    ) -> ProBowlRoster:
        """Fetch and parse a Pro Bowl roster page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/years/{year}/probowl.htm``
        and returns structured data for all Pro Bowl selections.

        Args:
            year: The Pro Bowl year (e.g. ``2024``).
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.ProBowlRoster` instance containing
            all Pro Bowl player entries for the given year.
        """
        config = self._get_year_config(year=year, timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return ProBowlRoster.model_validate(data)
