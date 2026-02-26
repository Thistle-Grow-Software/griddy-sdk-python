"""Executive profile endpoint for Pro Football Reference.

Provides ``get()`` to fetch and parse a PFR executive profile page
(``/executives/{executive_id}.htm``) and return structured executive data.
"""

from typing import Optional

from griddy.pfr.parsers import ExecutiveProfileParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import ExecutiveProfile


class Executives(BaseSDK):
    """Sub-SDK for PFR executive profile data."""

    def _get_executive_profile_config(
        self,
        *,
        executive_id: str,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        return EndpointConfig(
            path_template="/executives/{executive_id}.htm",
            operation_id="getExecutiveProfile",
            wait_for_element="#exec_results",
            parser=ExecutiveProfileParser().parse,
            response_type=ExecutiveProfile,
            path_params={"executive_id": executive_id},
            timeout_ms=timeout_ms,
        )

    def get(
        self,
        *,
        executive_id: str,
        timeout_ms: Optional[int] = None,
    ) -> ExecutiveProfile:
        """Fetch and parse an executive profile page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/executives/{executive_id}.htm``
        using the Browserless ``/chromium/unblock`` API with a residential
        proxy, then connects via Playwright CDP to extract the fully-rendered
        HTML and parse it into structured executive data.

        Args:
            executive_id: The PFR executive identifier (e.g. ``"AdamBu0"``
                for Bud Adams).
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.ExecutiveProfile` instance containing
            the executive's bio, career team results, and per-team summary
            totals.
        """
        config = self._get_executive_profile_config(
            executive_id=executive_id, timeout_ms=timeout_ms
        )
        data = self._execute_endpoint(config)
        return ExecutiveProfile.model_validate(data)
