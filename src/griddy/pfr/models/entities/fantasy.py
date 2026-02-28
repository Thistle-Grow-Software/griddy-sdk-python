"""Pydantic models for PFR Fantasy Rankings pages.

Covers:
- ``/years/{year}/fantasy.htm`` — Top Fantasy Players (table ``#fantasy``)
"""

from __future__ import annotations

from typing import Any, List, Optional

from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel

# ---------------------------------------------------------------------------
# FantasyPlayer (one row in /years/{year}/fantasy.htm)
# ---------------------------------------------------------------------------


class FantasyPlayerTypedDict(TypedDict):
    rank: NotRequired[int]
    player: NotRequired[str]
    player_href: NotRequired[str]
    player_id: NotRequired[str]
    team: NotRequired[str]
    team_href: NotRequired[str]
    fantasy_pos: NotRequired[str]
    age: NotRequired[int]
    # Games
    g: NotRequired[int]
    gs: NotRequired[int]
    # Passing
    pass_cmp: NotRequired[int]
    pass_att: NotRequired[int]
    pass_yds: NotRequired[int]
    pass_td: NotRequired[int]
    pass_int: NotRequired[int]
    # Rushing
    rush_att: NotRequired[int]
    rush_yds: NotRequired[int]
    rush_yds_per_att: NotRequired[Any]
    rush_td: NotRequired[int]
    # Receiving
    targets: NotRequired[int]
    rec: NotRequired[int]
    rec_yds: NotRequired[int]
    rec_yds_per_rec: NotRequired[Any]
    rec_td: NotRequired[int]
    # Fumbles
    fumbles: NotRequired[int]
    fumbles_lost: NotRequired[int]
    # Scoring
    all_td: NotRequired[int]
    two_pt_md: NotRequired[int]
    two_pt_pass: NotRequired[int]
    # Fantasy
    fantasy_points: NotRequired[Any]
    fantasy_points_ppr: NotRequired[Any]
    draftkings_points: NotRequired[Any]
    fanduel_points: NotRequired[Any]
    vbd: NotRequired[int]
    fantasy_rank_pos: NotRequired[int]
    fantasy_rank_overall: NotRequired[int]


class FantasyPlayer(BaseModel):
    rank: Optional[int] = None
    player: Optional[str] = None
    player_href: Optional[str] = None
    player_id: Optional[str] = None
    team: Optional[str] = None
    team_href: Optional[str] = None
    fantasy_pos: Optional[str] = None
    age: Optional[int] = None
    # Games
    g: Optional[int] = None
    gs: Optional[int] = None
    # Passing
    pass_cmp: Optional[int] = None
    pass_att: Optional[int] = None
    pass_yds: Optional[int] = None
    pass_td: Optional[int] = None
    pass_int: Optional[int] = None
    # Rushing
    rush_att: Optional[int] = None
    rush_yds: Optional[int] = None
    rush_yds_per_att: Optional[float] = None
    rush_td: Optional[int] = None
    # Receiving
    targets: Optional[int] = None
    rec: Optional[int] = None
    rec_yds: Optional[int] = None
    rec_yds_per_rec: Optional[float] = None
    rec_td: Optional[int] = None
    # Fumbles
    fumbles: Optional[int] = None
    fumbles_lost: Optional[int] = None
    # Scoring
    all_td: Optional[int] = None
    two_pt_md: Optional[int] = None
    two_pt_pass: Optional[int] = None
    # Fantasy
    fantasy_points: Optional[float] = None
    fantasy_points_ppr: Optional[float] = None
    draftkings_points: Optional[float] = None
    fanduel_points: Optional[float] = None
    vbd: Optional[int] = None
    fantasy_rank_pos: Optional[int] = None
    fantasy_rank_overall: Optional[int] = None


# ---------------------------------------------------------------------------
# TopFantasyPlayers (top-level for /years/{year}/fantasy.htm)
# ---------------------------------------------------------------------------


class TopFantasyPlayersTypedDict(TypedDict):
    players: NotRequired[List[FantasyPlayerTypedDict]]


class TopFantasyPlayers(BaseModel):
    players: List[FantasyPlayer] = []
