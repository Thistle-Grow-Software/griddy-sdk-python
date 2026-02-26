"""Pydantic models for PFR executive profile pages.

Covers the ``/executives/{ExecutiveId}.htm`` pages on Pro Football Reference,
including career team results and per-team summary totals.
"""

from __future__ import annotations

from typing import List, Optional

from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel

# --- Executive Bio (from #meta div) ---


class ExecutiveBioTypedDict(TypedDict):
    name: str


class ExecutiveBio(BaseModel):
    name: str


# --- Executive Result (from exec_results table body) ---


class ExecutiveResultTypedDict(TypedDict):
    year: NotRequired[str]
    year_href: NotRequired[str]
    team: NotRequired[str]
    team_href: NotRequired[str]
    league: NotRequired[str]
    job_title: NotRequired[str]
    wins: NotRequired[int]
    losses: NotRequired[int]
    ties: NotRequired[int]
    win_loss_pct: NotRequired[str]
    playoff_wins: NotRequired[int]
    playoff_losses: NotRequired[int]
    playoff_result: NotRequired[str]
    playoff_result_href: NotRequired[str]


class ExecutiveResult(BaseModel):
    year: Optional[str] = None
    year_href: Optional[str] = None
    team: Optional[str] = None
    team_href: Optional[str] = None
    league: Optional[str] = None
    job_title: Optional[str] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    ties: Optional[int] = None
    win_loss_pct: Optional[str] = None
    playoff_wins: Optional[int] = None
    playoff_losses: Optional[int] = None
    playoff_result: Optional[str] = None
    playoff_result_href: Optional[str] = None


# --- Executive Results Total (from exec_results table footer) ---


class ExecutiveResultsTotalTypedDict(TypedDict):
    label: NotRequired[str]
    tenure: NotRequired[str]
    wins: NotRequired[int]
    losses: NotRequired[int]
    ties: NotRequired[int]
    playoff_wins: NotRequired[int]
    playoff_losses: NotRequired[int]


class ExecutiveResultsTotal(BaseModel):
    label: Optional[str] = None
    tenure: Optional[str] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    ties: Optional[int] = None
    playoff_wins: Optional[int] = None
    playoff_losses: Optional[int] = None


# --- Executive Profile (top-level model) ---


class ExecutiveProfileTypedDict(TypedDict):
    bio: ExecutiveBioTypedDict
    exec_results: List[ExecutiveResultTypedDict]
    exec_results_totals: List[ExecutiveResultsTotalTypedDict]


class ExecutiveProfile(BaseModel):
    bio: ExecutiveBio
    exec_results: List[ExecutiveResult]
    exec_results_totals: List[ExecutiveResultsTotal]
