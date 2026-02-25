"""Stadium endpoint for Pro Football Reference.

Provides ``get_stadium()`` to fetch and parse a PFR stadium page
(``/stadiums/{stadium_id}.htm``) and return structured stadium data.
"""

from typing import Optional

from griddy.pfr.parsers import StadiumParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import StadiumProfile


class Stadiums(BaseSDK):
    """Sub-SDK for PFR stadium data."""

    def _get_stadium_config(
        self,
        *,
        stadium_id: str,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/stadiums/{stadium_id}.htm",
            operation_id="getStadium",
            wait_for_element="#leaders",
            parser=StadiumParser().parse,
            response_type=StadiumProfile,
            path_params={"stadium_id": stadium_id},
            timeout_ms=timeout_ms,
        )

    def get_stadium(
        self,
        *,
        stadium_id: str,
        timeout_ms: Optional[int] = None,
    ) -> StadiumProfile:
        """Fetch and parse a stadium page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/stadiums/{stadium_id}.htm``
        using the Browserless ``/chromium/unblock`` API with a residential
        proxy, then connects via Playwright CDP to extract the fully-rendered
        HTML and parse it into structured stadium data.

        Args:
            stadium_id: The PFR stadium identifier (e.g. ``"BOS00"``
                for Gillette Stadium).
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.StadiumProfile` instance containing
            the stadium's bio, career leaders, best games, and notable game
            summaries.
        """
        config = self._get_stadium_config(stadium_id=stadium_id, timeout_ms=timeout_ms)
        data = self._execute_endpoint(config)
        return StadiumProfile.model_validate(data)
