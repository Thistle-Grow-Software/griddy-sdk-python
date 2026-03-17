"""Pydantic models for NFL Draft Buzz position rankings pages."""

from __future__ import annotations

from typing import List, Optional

from ..base import DraftBuzzBaseModel


class RankedProspect(DraftBuzzBaseModel):
    """A single prospect entry from a position rankings page."""

    name: Optional[str] = None
    position: Optional[str] = None
    school: Optional[str] = None
    rank: Optional[int] = None
    href: Optional[str] = None


class PositionRankings(DraftBuzzBaseModel):
    """Rankings page result containing a list of ranked prospects.

    Returned by the ``rankings.get_position_rankings()`` endpoint.
    """

    position: Optional[str] = None
    year: Optional[int] = None
    page: Optional[int] = None
    total_pages: Optional[int] = None
    entries: List[RankedProspect] = []
