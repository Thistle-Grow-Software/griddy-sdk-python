"""Pydantic models for PFR Super Bowl pages.

Covers three page types:
- ``/super-bowl/`` — Super Bowl history (table ``#super_bowls``)
- ``/super-bowl/leaders.htm`` — Super Bowl leaders (leaderboard tables)
- ``/super-bowl/standings.htm`` — franchise standings (table ``#standings``)
"""

from __future__ import annotations

from typing import List, Optional

from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel

# ---------------------------------------------------------------------------
# Super Bowl Game (one row in /super-bowl/)
# ---------------------------------------------------------------------------


class SuperBowlGameTypedDict(TypedDict):
    game_date: NotRequired[str]
    superbowl: NotRequired[str]
    superbowl_number: NotRequired[int]
    boxscore_href: NotRequired[str]
    winner: NotRequired[str]
    winner_href: NotRequired[str]
    winner_points: NotRequired[int]
    loser: NotRequired[str]
    loser_href: NotRequired[str]
    loser_points: NotRequired[int]
    mvp: NotRequired[str]
    mvp_href: NotRequired[str]
    stadium: NotRequired[str]
    stadium_href: NotRequired[str]
    city: NotRequired[str]
    state: NotRequired[str]


class SuperBowlGame(BaseModel):
    game_date: Optional[str] = None
    superbowl: Optional[str] = None
    superbowl_number: Optional[int] = None
    boxscore_href: Optional[str] = None
    winner: Optional[str] = None
    winner_href: Optional[str] = None
    winner_points: Optional[int] = None
    loser: Optional[str] = None
    loser_href: Optional[str] = None
    loser_points: Optional[int] = None
    mvp: Optional[str] = None
    mvp_href: Optional[str] = None
    stadium: Optional[str] = None
    stadium_href: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None


# ---------------------------------------------------------------------------
# Super Bowl History (top-level for /super-bowl/)
# ---------------------------------------------------------------------------


class SuperBowlHistoryTypedDict(TypedDict):
    games: NotRequired[List[SuperBowlGameTypedDict]]


class SuperBowlHistory(BaseModel):
    games: List[SuperBowlGame] = []


# ---------------------------------------------------------------------------
# Super Bowl Leader Entry (one row in a leader table)
# ---------------------------------------------------------------------------


class SuperBowlLeaderEntryTypedDict(TypedDict):
    rank: NotRequired[int]
    player: NotRequired[str]
    player_href: NotRequired[str]
    description: NotRequired[str]
    value: NotRequired[str]


class SuperBowlLeaderEntry(BaseModel):
    rank: Optional[int] = None
    player: Optional[str] = None
    player_href: Optional[str] = None
    description: Optional[str] = None
    value: Optional[str] = None


# ---------------------------------------------------------------------------
# Super Bowl Leader Table (one leaderboard table)
# ---------------------------------------------------------------------------


class SuperBowlLeaderTableTypedDict(TypedDict):
    category: NotRequired[str]
    entries: NotRequired[List[SuperBowlLeaderEntryTypedDict]]


class SuperBowlLeaderTable(BaseModel):
    category: Optional[str] = None
    entries: List[SuperBowlLeaderEntry] = []


# ---------------------------------------------------------------------------
# Super Bowl Leaders (top-level for /super-bowl/leaders.htm)
# ---------------------------------------------------------------------------


class SuperBowlLeadersTypedDict(TypedDict):
    tables: NotRequired[List[SuperBowlLeaderTableTypedDict]]


class SuperBowlLeaders(BaseModel):
    tables: List[SuperBowlLeaderTable] = []


# ---------------------------------------------------------------------------
# Super Bowl QB (one QB in standings sb_qbs column)
# ---------------------------------------------------------------------------


class SuperBowlQBTypedDict(TypedDict):
    player: NotRequired[str]
    player_href: NotRequired[str]
    record: NotRequired[str]


class SuperBowlQB(BaseModel):
    player: Optional[str] = None
    player_href: Optional[str] = None
    record: Optional[str] = None


# ---------------------------------------------------------------------------
# Super Bowl Standing (one row in /super-bowl/standings.htm)
# ---------------------------------------------------------------------------


class SuperBowlStandingTypedDict(TypedDict):
    rank: NotRequired[int]
    team: NotRequired[str]
    team_href: NotRequired[str]
    games: NotRequired[int]
    wins: NotRequired[int]
    losses: NotRequired[int]
    win_loss_pct: NotRequired[str]
    points: NotRequired[int]
    points_opp: NotRequired[int]
    points_diff: NotRequired[str]
    qbs: NotRequired[List[SuperBowlQBTypedDict]]


class SuperBowlStanding(BaseModel):
    rank: Optional[int] = None
    team: Optional[str] = None
    team_href: Optional[str] = None
    games: Optional[int] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    win_loss_pct: Optional[str] = None
    points: Optional[int] = None
    points_opp: Optional[int] = None
    points_diff: Optional[str] = None
    qbs: List[SuperBowlQB] = []


# ---------------------------------------------------------------------------
# Super Bowl Standings (top-level for /super-bowl/standings.htm)
# ---------------------------------------------------------------------------


class SuperBowlStandingsTypedDict(TypedDict):
    teams: NotRequired[List[SuperBowlStandingTypedDict]]


class SuperBowlStandings(BaseModel):
    teams: List[SuperBowlStanding] = []
