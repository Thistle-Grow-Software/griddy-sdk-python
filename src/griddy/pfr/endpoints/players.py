"""Player profile endpoint for Pro Football Reference.

Provides ``get_player_profile()`` to fetch and parse a PFR player profile page
(``/players/{letter}/{player_id}.htm``) and return structured player data.
"""

from typing import Optional

from griddy.pfr.parsers import PlayerProfileParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import PlayerProfile


class Players(BaseSDK):
    """Sub-SDK for PFR player profile data."""

    def _get_player_profile_config(
        self,
        *,
        player_id: str,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        first_letter = player_id[0].upper()
        return EndpointConfig(
            path_template="/players/{letter}/{player_id}.htm",
            operation_id="getPlayerProfile",
            wait_for_element="#meta",
            parser=PlayerProfileParser().parse,
            response_type=PlayerProfile,
            path_params={"letter": first_letter, "player_id": player_id},
            timeout_ms=timeout_ms,
        )

    def get_player_profile(
        self,
        *,
        player_id: str,
        timeout_ms: Optional[int] = None,
    ) -> PlayerProfile:
        """Fetch and parse a player profile page from Pro Football Reference.

        Scrapes
        ``https://www.pro-football-reference.com/players/{letter}/{player_id}.htm``
        using the Browserless ``/chromium/unblock`` API with a residential proxy,
        then connects via Playwright CDP to extract the fully-rendered HTML and
        parse it into structured player data.

        Args:
            player_id: The PFR player identifier (e.g. ``"BradTo00"``).
                The first letter is used to resolve the URL path segment.
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.pfr.models.PlayerProfile` instance containing
            the player's bio, jersey numbers, summary stats, full statistics,
            transactions, links, and leaderboard data.
        """
        config = self._get_player_profile_config(
            player_id=player_id, timeout_ms=timeout_ms
        )
        return self._execute_endpoint(config)
