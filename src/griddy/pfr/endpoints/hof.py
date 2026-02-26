"""Hall of Fame endpoint for Pro Football Reference.

Provides ``list()`` to fetch and parse the PFR Hall of Fame page.
"""

from typing import Optional

from griddy.pfr.parsers import AwardsParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import HallOfFame

_parser = AwardsParser()


class Hof(BaseSDK):
    """Sub-SDK for the PFR Hall of Fame page."""

    def _get_hof_config(
        self,
        *,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/hof/",
            operation_id="getHof",
            wait_for_element="#hof_players",
            parser=lambda html: _parser.parse_hof(html),
            response_type=HallOfFame,
            path_params={},
            timeout_ms=timeout_ms,
        )

    def list(
        self,
        *,
        timeout_ms: Optional[int] = None,
    ) -> HallOfFame:
        """Fetch and parse the Hall of Fame page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/hof/``
        and returns structured data for all Hall of Fame inductees.

        Args:
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.HallOfFame` instance containing
            all Hall of Fame player entries.
        """
        config = self._get_hof_config(timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return HallOfFame.model_validate(data)
