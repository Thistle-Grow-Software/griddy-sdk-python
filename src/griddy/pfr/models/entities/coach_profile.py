"""Pydantic models for PFR coach profile pages.

Covers the ``/coaches/{CoachId}.htm`` pages on Pro Football Reference,
including coaching results, coaching ranks, coaching history, coaching
tree (worked-for / employed), and challenge results.
"""

from __future__ import annotations

from typing import List, Optional

from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel

# --- Coach Bio (from #meta div) ---


class CoachBioTypedDict(TypedDict):
    name: str
    full_name: NotRequired[str]
    nicknames: NotRequired[List[str]]
    photo_url: NotRequired[str]
    birth_date: NotRequired[str]
    birth_city: NotRequired[str]
    birth_state: NotRequired[str]
    college: NotRequired[str]
    college_href: NotRequired[str]
    college_coaching_href: NotRequired[str]
    high_schools: NotRequired[List[str]]
    as_exec: NotRequired[str]
    as_exec_href: NotRequired[str]
    relatives: NotRequired[str]
    relatives_href: NotRequired[str]


class CoachBio(BaseModel):
    name: str
    full_name: Optional[str] = None
    nicknames: List[str] = []
    photo_url: Optional[str] = None
    birth_date: Optional[str] = None
    birth_city: Optional[str] = None
    birth_state: Optional[str] = None
    college: Optional[str] = None
    college_href: Optional[str] = None
    college_coaching_href: Optional[str] = None
    high_schools: List[str] = []
    as_exec: Optional[str] = None
    as_exec_href: Optional[str] = None
    relatives: Optional[str] = None
    relatives_href: Optional[str] = None


# --- Coaching Result (from coaching_results table body) ---


class CoachingResultTypedDict(TypedDict):
    year_id: str
    year_href: NotRequired[str]
    age: NotRequired[int]
    team: NotRequired[str]
    team_href: NotRequired[str]
    league_id: NotRequired[str]
    g: NotRequired[int]
    g_href: NotRequired[str]
    wins: NotRequired[int]
    losses: NotRequired[int]
    ties: NotRequired[int]
    win_loss_perc: NotRequired[str]
    srs_total: NotRequired[float]
    srs_offense: NotRequired[float]
    srs_defense: NotRequired[float]
    g_playoffs: NotRequired[int]
    wins_playoffs: NotRequired[int]
    losses_playoffs: NotRequired[int]
    win_loss_playoffs_perc: NotRequired[str]
    rank_team: NotRequired[int]
    chall_num: NotRequired[int]
    chall_won: NotRequired[int]
    coach_remarks: NotRequired[str]


class CoachingResult(BaseModel):
    year_id: str
    year_href: Optional[str] = None
    age: Optional[int] = None
    team: Optional[str] = None
    team_href: Optional[str] = None
    league_id: Optional[str] = None
    g: Optional[int] = None
    g_href: Optional[str] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    ties: Optional[int] = None
    win_loss_perc: Optional[str] = None
    srs_total: Optional[float] = None
    srs_offense: Optional[float] = None
    srs_defense: Optional[float] = None
    g_playoffs: Optional[int] = None
    wins_playoffs: Optional[int] = None
    losses_playoffs: Optional[int] = None
    win_loss_playoffs_perc: Optional[str] = None
    rank_team: Optional[int] = None
    chall_num: Optional[int] = None
    chall_won: Optional[int] = None
    coach_remarks: Optional[str] = None


# --- Coaching Result Total (from coaching_results table footer) ---


class CoachingResultTotalTypedDict(TypedDict):
    label: str
    team: NotRequired[str]
    g: NotRequired[int]
    wins: NotRequired[int]
    losses: NotRequired[int]
    ties: NotRequired[int]
    win_loss_perc: NotRequired[str]
    g_playoffs: NotRequired[int]
    wins_playoffs: NotRequired[int]
    losses_playoffs: NotRequired[int]
    win_loss_playoffs_perc: NotRequired[str]
    rank_avg: NotRequired[float]
    chall_num: NotRequired[int]
    chall_won: NotRequired[int]


class CoachingResultTotal(BaseModel):
    label: str
    team: Optional[str] = None
    g: Optional[int] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    ties: Optional[int] = None
    win_loss_perc: Optional[str] = None
    g_playoffs: Optional[int] = None
    wins_playoffs: Optional[int] = None
    losses_playoffs: Optional[int] = None
    win_loss_playoffs_perc: Optional[str] = None
    rank_avg: Optional[float] = None
    chall_num: Optional[int] = None
    chall_won: Optional[int] = None


# --- Coaching Rank (from coaching_ranks table) ---


class CoachingRankTypedDict(TypedDict):
    year_id: str
    team: NotRequired[str]
    coordinator_type: NotRequired[str]
    teams_in_league: NotRequired[int]
    rank_win_percentage: NotRequired[int]
    rank_takeaway_giveaway: NotRequired[int]
    rank_points_diff: NotRequired[int]
    rank_yds_diff: NotRequired[int]
    rank_off_yds: NotRequired[int]
    rank_off_pts: NotRequired[int]
    rank_off_turnovers: NotRequired[int]
    rank_off_rush_att: NotRequired[int]
    rank_off_rush_yds: NotRequired[int]
    rank_off_rush_td: NotRequired[int]
    rank_off_rush_yds_per_att: NotRequired[int]
    rank_off_fumbles_lost: NotRequired[int]
    rank_off_pass_att: NotRequired[int]
    rank_off_pass_yds: NotRequired[int]
    rank_off_pass_td: NotRequired[int]
    rank_off_pass_int: NotRequired[int]
    rank_off_pass_net_yds_per_att: NotRequired[int]
    rank_def_yds: NotRequired[int]
    rank_def_pts: NotRequired[int]
    rank_def_turnovers: NotRequired[int]
    rank_def_rush_att: NotRequired[int]
    rank_def_rush_yds: NotRequired[int]
    rank_def_rush_td: NotRequired[int]
    rank_def_rush_yds_per_att: NotRequired[int]
    rank_def_fumbles_rec: NotRequired[int]
    rank_def_pass_att: NotRequired[int]
    rank_def_pass_yds: NotRequired[int]
    rank_def_pass_td: NotRequired[int]
    rank_def_pass_int: NotRequired[int]
    rank_def_pass_net_yds_per_att: NotRequired[int]


class CoachingRank(BaseModel):
    year_id: str
    team: Optional[str] = None
    coordinator_type: Optional[str] = None
    teams_in_league: Optional[int] = None
    rank_win_percentage: Optional[int] = None
    rank_takeaway_giveaway: Optional[int] = None
    rank_points_diff: Optional[int] = None
    rank_yds_diff: Optional[int] = None
    rank_off_yds: Optional[int] = None
    rank_off_pts: Optional[int] = None
    rank_off_turnovers: Optional[int] = None
    rank_off_rush_att: Optional[int] = None
    rank_off_rush_yds: Optional[int] = None
    rank_off_rush_td: Optional[int] = None
    rank_off_rush_yds_per_att: Optional[int] = None
    rank_off_fumbles_lost: Optional[int] = None
    rank_off_pass_att: Optional[int] = None
    rank_off_pass_yds: Optional[int] = None
    rank_off_pass_td: Optional[int] = None
    rank_off_pass_int: Optional[int] = None
    rank_off_pass_net_yds_per_att: Optional[int] = None
    rank_def_yds: Optional[int] = None
    rank_def_pts: Optional[int] = None
    rank_def_turnovers: Optional[int] = None
    rank_def_rush_att: Optional[int] = None
    rank_def_rush_yds: Optional[int] = None
    rank_def_rush_td: Optional[int] = None
    rank_def_rush_yds_per_att: Optional[int] = None
    rank_def_fumbles_rec: Optional[int] = None
    rank_def_pass_att: Optional[int] = None
    rank_def_pass_yds: Optional[int] = None
    rank_def_pass_td: Optional[int] = None
    rank_def_pass_int: Optional[int] = None
    rank_def_pass_net_yds_per_att: Optional[int] = None


# --- Coaching History Entry (from coaching_history table) ---


class CoachingHistoryEntryTypedDict(TypedDict):
    year_id: str
    coach_age: NotRequired[int]
    coach_level: NotRequired[str]
    coach_employer: NotRequired[str]
    coach_employer_href: NotRequired[str]
    coach_role: NotRequired[str]


class CoachingHistoryEntry(BaseModel):
    year_id: str
    coach_age: Optional[int] = None
    coach_level: Optional[str] = None
    coach_employer: Optional[str] = None
    coach_employer_href: Optional[str] = None
    coach_role: Optional[str] = None


# --- Coaching Tree Entry (for worked_for and employed tables) ---


class CoachingTreeEntryTypedDict(TypedDict):
    coach_name: str
    coach_href: NotRequired[str]
    roles: NotRequired[str]


class CoachingTreeEntry(BaseModel):
    coach_name: str
    coach_href: Optional[str] = None
    roles: Optional[str] = None


# --- Challenge Result (from challenge_results table) ---


class ChallengeResultTypedDict(TypedDict):
    game_date: NotRequired[str]
    game_date_href: NotRequired[str]
    down: NotRequired[int]
    yds_to_go: NotRequired[int]
    location: NotRequired[str]
    challenge_ruling: NotRequired[str]
    detail: NotRequired[str]


class ChallengeResult(BaseModel):
    game_date: Optional[str] = None
    game_date_href: Optional[str] = None
    down: Optional[int] = None
    yds_to_go: Optional[int] = None
    location: Optional[str] = None
    challenge_ruling: Optional[str] = None
    detail: Optional[str] = None


# --- Coach Profile (top-level model) ---


class CoachProfileTypedDict(TypedDict):
    bio: CoachBioTypedDict
    coaching_results: List[CoachingResultTypedDict]
    coaching_results_totals: List[CoachingResultTotalTypedDict]
    coaching_ranks: List[CoachingRankTypedDict]
    coaching_history: List[CoachingHistoryEntryTypedDict]
    challenge_results: List[ChallengeResultTypedDict]
    worked_for: List[CoachingTreeEntryTypedDict]
    employed: List[CoachingTreeEntryTypedDict]


class CoachProfile(BaseModel):
    bio: CoachBio
    coaching_results: List[CoachingResult]
    coaching_results_totals: List[CoachingResultTotal]
    coaching_ranks: List[CoachingRank]
    coaching_history: List[CoachingHistoryEntry]
    challenge_results: List[ChallengeResult]
    worked_for: List[CoachingTreeEntry]
    employed: List[CoachingTreeEntry]
