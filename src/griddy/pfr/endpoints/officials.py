"""Official profile endpoint for Pro Football Reference.

Provides ``get_official_profile()`` to fetch and parse a PFR official profile
page (``/officials/{official_id}.htm``) and return structured officiating data.
"""

from typing import Optional

from griddy.pfr.parsers import OfficialProfileParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import OfficialProfile


class Officials(BaseSDK):
    """Sub-SDK for PFR game official profile data."""

    def _get_official_profile_config(
        self,
        *,
        official_id: str,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/officials/{official_id}.htm",
            operation_id="getOfficialProfile",
            wait_for_element="#official_stats",
            parser=OfficialProfileParser().parse,
            response_type=OfficialProfile,
            path_params={"official_id": official_id},
            timeout_ms=timeout_ms,
        )

    def get_official_profile(
        self,
        *,
        official_id: str,
        timeout_ms: Optional[int] = None,
    ) -> OfficialProfile:
        """Fetch and parse an official profile page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/officials/{official_id}.htm``
        using the Browserless ``/chromium/unblock`` API with a residential
        proxy, then connects via Playwright CDP to extract the fully-rendered
        HTML and parse it into structured officiating data.

        Args:
            official_id: The PFR official identifier (e.g. ``"ChefCa0r"``
                for Carl Cheffers).
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.OfficialProfile` instance containing
            the official's bio, season penalty stats, and game logs.
        """
        config = self._get_official_profile_config(
            official_id=official_id, timeout_ms=timeout_ms
        )
        data = self._execute_endpoint(config)
        return OfficialProfile.model_validate(data)
