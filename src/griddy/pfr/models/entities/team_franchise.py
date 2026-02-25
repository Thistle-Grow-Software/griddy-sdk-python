from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel

# --- Franchise Metadata ---


class FranchiseLeaderTypedDict(TypedDict, total=False):
    name: str
    href: str
    stats: str


class FranchiseLeader(BaseModel):
    name: Optional[str] = None
    href: Optional[str] = None
    stats: Optional[str] = None


class FranchiseMetaTypedDict(TypedDict, total=False):
    team_names: str
    seasons: str
    record: str
    playoff_record: str
    super_bowls_won: str
    championships_won: str
    all_time_passing_leader: FranchiseLeaderTypedDict
    all_time_rushing_leader: FranchiseLeaderTypedDict
    all_time_receiving_leader: FranchiseLeaderTypedDict
    all_time_scoring_leader: FranchiseLeaderTypedDict
    all_time_av_leader: FranchiseLeaderTypedDict
    winningest_coach: FranchiseLeaderTypedDict


class FranchiseMeta(BaseModel):
    team_names: Optional[str] = None
    seasons: Optional[str] = None
    record: Optional[str] = None
    playoff_record: Optional[str] = None
    super_bowls_won: Optional[str] = None
    championships_won: Optional[str] = None
    all_time_passing_leader: Optional[FranchiseLeader] = None
    all_time_rushing_leader: Optional[FranchiseLeader] = None
    all_time_receiving_leader: Optional[FranchiseLeader] = None
    all_time_scoring_leader: Optional[FranchiseLeader] = None
    all_time_av_leader: Optional[FranchiseLeader] = None
    winningest_coach: Optional[FranchiseLeader] = None


# --- Franchise Season Record (one row of team_index table) ---


class FranchiseSeasonRecordTypedDict(TypedDict):
    year_id: str
    year_href: NotRequired[Optional[str]]
    league_id: NotRequired[Optional[str]]
    league_href: NotRequired[Optional[str]]
    team: str
    team_href: NotRequired[Optional[str]]
    wins: NotRequired[Optional[int]]
    losses: NotRequired[Optional[int]]
    ties: NotRequired[Optional[int]]
    div_finish: NotRequired[Optional[str]]
    playoff_result: NotRequired[Optional[str]]
    playoff_result_href: NotRequired[Optional[str]]
    points: NotRequired[Optional[int]]
    points_opp: NotRequired[Optional[int]]
    points_diff: NotRequired[Optional[int]]
    coaches: NotRequired[Optional[str]]
    coaches_href: NotRequired[Optional[str]]
    av: NotRequired[Optional[str]]
    av_title: NotRequired[Optional[str]]
    av_href: NotRequired[Optional[str]]
    passer: NotRequired[Optional[str]]
    passer_title: NotRequired[Optional[str]]
    passer_href: NotRequired[Optional[str]]
    rusher: NotRequired[Optional[str]]
    rusher_title: NotRequired[Optional[str]]
    rusher_href: NotRequired[Optional[str]]
    receiver: NotRequired[Optional[str]]
    receiver_title: NotRequired[Optional[str]]
    receiver_href: NotRequired[Optional[str]]
    rank_off_pts: NotRequired[Optional[int]]
    rank_off_yds: NotRequired[Optional[int]]
    rank_def_pts: NotRequired[Optional[int]]
    rank_def_yds: NotRequired[Optional[int]]
    rank_takeaway_giveaway: NotRequired[Optional[int]]
    rank_points_diff: NotRequired[Optional[int]]
    rank_yds_diff: NotRequired[Optional[int]]
    teams_in_league: NotRequired[Optional[int]]
    mov: NotRequired[Optional[float]]
    sos_total: NotRequired[Optional[float]]
    srs_total: NotRequired[Optional[float]]
    srs_offense: NotRequired[Optional[float]]
    srs_defense: NotRequired[Optional[float]]


class FranchiseSeasonRecord(BaseModel):
    year_id: str
    year_href: Optional[str] = None
    league_id: Optional[str] = None
    league_href: Optional[str] = None
    team: str
    team_href: Optional[str] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    ties: Optional[int] = None
    div_finish: Optional[str] = None
    playoff_result: Optional[str] = None
    playoff_result_href: Optional[str] = None
    points: Optional[int] = None
    points_opp: Optional[int] = None
    points_diff: Optional[int] = None
    coaches: Optional[str] = None
    coaches_href: Optional[str] = None
    av: Optional[str] = None
    av_title: Optional[str] = None
    av_href: Optional[str] = None
    passer: Optional[str] = None
    passer_title: Optional[str] = None
    passer_href: Optional[str] = None
    rusher: Optional[str] = None
    rusher_title: Optional[str] = None
    rusher_href: Optional[str] = None
    receiver: Optional[str] = None
    receiver_title: Optional[str] = None
    receiver_href: Optional[str] = None
    rank_off_pts: Optional[int] = None
    rank_off_yds: Optional[int] = None
    rank_def_pts: Optional[int] = None
    rank_def_yds: Optional[int] = None
    rank_takeaway_giveaway: Optional[int] = None
    rank_points_diff: Optional[int] = None
    rank_yds_diff: Optional[int] = None
    teams_in_league: Optional[int] = None
    mov: Optional[float] = None
    sos_total: Optional[float] = None
    srs_total: Optional[float] = None
    srs_offense: Optional[float] = None
    srs_defense: Optional[float] = None


# --- Top-level Team Franchise ---


class FranchiseTypedDict(TypedDict):
    meta: FranchiseMetaTypedDict
    team_index: List[FranchiseSeasonRecordTypedDict]


class Franchise(BaseModel):
    meta: FranchiseMeta
    team_index: List[FranchiseSeasonRecord]
