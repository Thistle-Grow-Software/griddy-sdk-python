"""Prospect endpoints for NFL Draft Buzz.

Provides ``get_prospect()`` to fetch and parse a complete prospect
profile including stats from two separate page fetches.
"""

from functools import cached_property
from typing import Any, Optional

from griddy.core.decorators import sdk_endpoints
from griddy.draftbuzz.parsers import ProspectProfileParser

from ..basesdk import BaseSDK, EndpointConfig
from ..models import ProspectProfile


@sdk_endpoints
class Prospects(BaseSDK):
    """Sub-SDK for DraftBuzz prospect profile pages."""

    @cached_property
    def _parser(self) -> ProspectProfileParser:
        """Lazily instantiate and cache the prospect profile parser."""
        return ProspectProfileParser()

    def _get_prospect_config(
        self,
        *,
        slug: str,
        position: str,
        timeout_ms: Optional[int] = None,
    ) -> EndpointConfig:
        r"""Fetch and parse a prospect profile from NFL Draft Buzz.

        Scrapes the prospect profile page at
        ``https://www.nfldraftbuzz.com/{slug}`` and returns structured
        prospect data including basic info, ratings, skills, scouting
        report, and comparisons.

        **Note:** This endpoint only fetches the profile page. Stats are
        fetched separately by the ``get_prospect`` method which combines
        both pages into a complete ``ProspectProfile``.

        Args:
            slug: The prospect URL slug (e.g.
                ``"players/cam-ward-qb-2025"``).
            position: Canonical position group (e.g. ``"QB"``, ``"WR"``).
            timeout_ms: Optional timeout in milliseconds for the page
                selector.

        Returns:
            A :class:`~griddy.draftbuzz.models.ProspectProfile` instance.
        """
        parser = self._parser
        return EndpointConfig(
            path_template="/{slug}",
            operation_id="getProspect",
            wait_for_element=".player-info__first-name",
            parser=lambda html: parser.parse_profile(html, position=position),
            response_type=ProspectProfile,
            path_params={"slug": slug},
            timeout_ms=timeout_ms,
        )

    # Override auto-generated get_prospect to add stats fetching
    def get_prospect(
        self,
        *,
        slug: str,
        position: str,
        timeout_ms: Optional[int] = None,
    ) -> ProspectProfile:
        """Fetch a complete prospect profile including stats.

        Makes two requests: one for the profile page and one for the
        stats page, combining results into a single ``ProspectProfile``.

        Args:
            slug: The prospect URL slug (e.g.
                ``"players/cam-ward-qb-2025"``).
            position: Canonical position group (e.g. ``"QB"``, ``"WR"``).
            timeout_ms: Optional timeout in milliseconds.

        Returns:
            A :class:`~griddy.draftbuzz.models.ProspectProfile` with all
            fields populated including stats.
        """
        config = self._get_prospect_config(
            slug=slug, position=position, timeout_ms=timeout_ms
        )
        profile: ProspectProfile = self._execute_endpoint(config)

        # Fetch stats from separate page
        stats = self._fetch_stats(slug=slug, position=position)
        if stats is not None:
            profile = profile.model_copy(update={"stats": stats})

        return profile

    async def get_prospect_async(
        self,
        *,
        slug: str,
        position: str,
        timeout_ms: Optional[int] = None,
    ) -> ProspectProfile:
        """Async version of :meth:`get_prospect`."""
        config = self._get_prospect_config(
            slug=slug, position=position, timeout_ms=timeout_ms
        )
        profile: ProspectProfile = await self._execute_endpoint_async(config)

        stats = await self._fetch_stats_async(slug=slug, position=position)
        if stats is not None:
            profile = profile.model_copy(update={"stats": stats})

        return profile

    def _fetch_stats(self, *, slug: str, position: str) -> Any:
        """Fetch and parse the stats page for a prospect."""
        stats_slug = self._build_stats_slug(slug)
        url = self._build_url(
            EndpointConfig(
                path_template="/{slug}",
                operation_id="getProspectStats",
                path_params={"slug": stats_slug},
            )
        )

        try:
            html = self.browserless.get_page_content(url, wait_for_element="table")
        except Exception:
            return None

        return self._parser.parse_stats(html, position=position)

    async def _fetch_stats_async(self, *, slug: str, position: str) -> Any:
        """Async version of :meth:`_fetch_stats`."""
        stats_slug = self._build_stats_slug(slug)
        url = self._build_url(
            EndpointConfig(
                path_template="/{slug}",
                operation_id="getProspectStats",
                path_params={"slug": stats_slug},
            )
        )

        try:
            html = await self.async_browserless.get_page_content(
                url, wait_for_element="table"
            )
        except Exception:
            return None

        return self._parser.parse_stats(html, position=position)

    @staticmethod
    def _build_stats_slug(slug: str) -> str:
        """Convert a profile slug to a stats slug.

        ``"players/cam-ward-qb-2025"`` → ``"players/stats/cam-ward-qb-2025"``
        """
        parts = slug.split("/")
        if len(parts) >= 2:
            return f"{parts[0]}/stats/{'/'.join(parts[1:])}"
        return f"players/stats/{slug}"
