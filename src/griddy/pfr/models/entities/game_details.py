from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import Field
from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel

# --- Scorebox ---


class ScoreboxTeamTypedDict(TypedDict):
    name: str
    href: str
    score: int
    record: str
    coach: str
    coach_href: str


class ScoreboxTeam(BaseModel):
    name: str
    href: str
    score: int
    record: str
    coach: str
    coach_href: str


class ScoreboxMetaTypedDict(TypedDict, total=False):
    date: str
    Start_Time: str
    Stadium: str
    Attendance: str
    Time_of_Game: str


class ScoreboxMeta(BaseModel):
    date: Optional[str] = None
    start_time: Optional[str] = Field(default=None, alias="Start Time")
    stadium: Optional[str] = Field(default=None, alias="Stadium")
    attendance: Optional[str] = Field(default=None, alias="Attendance")
    time_of_game: Optional[str] = Field(default=None, alias="Time of Game")


class ScoreboxTypedDict(TypedDict):
    away: ScoreboxTeamTypedDict
    home: ScoreboxTeamTypedDict
    meta: ScoreboxMetaTypedDict


class Scorebox(BaseModel):
    away: ScoreboxTeam
    home: ScoreboxTeam
    meta: ScoreboxMeta


# --- Linescore ---


class LinescoreEntryTypedDict(TypedDict):
    team: str
    team_href: str
    quarters: Dict[str, int]


class LinescoreEntry(BaseModel):
    team: str
    team_href: str
    quarters: Dict[str, int]


# --- Scoring ---


class ScoringPlayTypedDict(TypedDict):
    quarter: NotRequired[Optional[int]]
    time: str
    team: str
    description: str
    description_href: str
    vis_team_score: int
    home_team_score: int


class ScoringPlay(BaseModel):
    quarter: Optional[int] = None
    time: str
    team: str
    description: str
    description_href: str
    vis_team_score: int
    home_team_score: int


# --- Expected Points ---


class ExpectedPointsTypedDict(TypedDict):
    team_name: str
    pbp_exp_points_tot: float
    pbp_exp_points_off_tot: float
    pbp_exp_points_off_pass: float
    pbp_exp_points_off_rush: float
    pbp_exp_points_off_to: float
    pbp_exp_points_def_tot: float
    pbp_exp_points_def_pass: float
    pbp_exp_points_def_rush: float
    pbp_exp_points_def_to: float
    pbp_exp_points_st: float
    pbp_exp_points_k: float
    pbp_exp_points_kr: float
    pbp_exp_points_p: float
    pbp_exp_points_pr: float
    pbp_exp_points_fgxp: float


class ExpectedPoints(BaseModel):
    team_name: str
    pbp_exp_points_tot: float
    pbp_exp_points_off_tot: float
    pbp_exp_points_off_pass: float
    pbp_exp_points_off_rush: float
    pbp_exp_points_off_to: float
    pbp_exp_points_def_tot: float
    pbp_exp_points_def_pass: float
    pbp_exp_points_def_rush: float
    pbp_exp_points_def_to: float
    pbp_exp_points_st: float
    pbp_exp_points_k: float
    pbp_exp_points_kr: float
    pbp_exp_points_p: float
    pbp_exp_points_pr: float
    pbp_exp_points_fgxp: float


# --- Player Offense ---


class PlayerOffenseTypedDict(TypedDict):
    player: str
    player_href: str
    player_id: str
    team: str
    pass_cmp: int
    pass_att: int
    pass_yds: int
    pass_td: int
    pass_int: int
    pass_sacked: int
    pass_sacked_yds: int
    pass_long: NotRequired[Optional[int]]
    pass_rating: NotRequired[Optional[float]]
    rush_att: int
    rush_yds: int
    rush_td: int
    rush_long: NotRequired[Optional[int]]
    targets: int
    rec: int
    rec_yds: int
    rec_td: int
    rec_long: NotRequired[Optional[int]]
    fumbles: int
    fumbles_lost: int


class PlayerOffense(BaseModel):
    player: str
    player_href: str
    player_id: str
    team: str
    pass_cmp: int
    pass_att: int
    pass_yds: int
    pass_td: int
    pass_int: int
    pass_sacked: int
    pass_sacked_yds: int
    pass_long: Optional[int] = None
    pass_rating: Optional[float] = None
    rush_att: int
    rush_yds: int
    rush_td: int
    rush_long: Optional[int] = None
    targets: int
    rec: int
    rec_yds: int
    rec_td: int
    rec_long: Optional[int] = None
    fumbles: int
    fumbles_lost: int


# --- Player Defense ---


class PlayerDefenseTypedDict(TypedDict):
    player: str
    player_href: str
    player_id: str
    team: str
    def_int: int
    def_int_yds: int
    def_int_td: int
    def_int_long: int
    pass_defended: int
    sacks: float
    tackles_combined: int
    tackles_solo: int
    tackles_assists: int
    tackles_loss: int
    qb_hits: int
    fumbles_rec: int
    fumbles_rec_yds: int
    fumbles_rec_td: int
    fumbles_forced: int


class PlayerDefense(BaseModel):
    player: str
    player_href: str
    player_id: str
    team: str
    def_int: int
    def_int_yds: int
    def_int_td: int
    def_int_long: int
    pass_defended: int
    sacks: float
    tackles_combined: int
    tackles_solo: int
    tackles_assists: int
    tackles_loss: int
    qb_hits: int
    fumbles_rec: int
    fumbles_rec_yds: int
    fumbles_rec_td: int
    fumbles_forced: int


# --- Returns ---


class PlayerReturnTypedDict(TypedDict):
    player: str
    player_href: str
    player_id: str
    team: str
    kick_ret: int
    kick_ret_yds: int
    kick_ret_yds_per_ret: NotRequired[Optional[float]]
    kick_ret_td: int
    kick_ret_long: int
    punt_ret: int
    punt_ret_yds: int
    punt_ret_yds_per_ret: NotRequired[Optional[float]]
    punt_ret_td: int
    punt_ret_long: int


class PlayerReturn(BaseModel):
    player: str
    player_href: str
    player_id: str
    team: str
    kick_ret: int
    kick_ret_yds: int
    kick_ret_yds_per_ret: Optional[float] = None
    kick_ret_td: int
    kick_ret_long: int
    punt_ret: int
    punt_ret_yds: int
    punt_ret_yds_per_ret: Optional[float] = None
    punt_ret_td: int
    punt_ret_long: int


# --- Kicking ---


class PlayerKickingTypedDict(TypedDict):
    player: str
    player_href: str
    player_id: str
    team: str
    xpm: NotRequired[Optional[int]]
    xpa: NotRequired[Optional[int]]
    fgm: NotRequired[Optional[int]]
    fga: NotRequired[Optional[int]]
    punt: int
    punt_yds: int
    punt_yds_per_punt: NotRequired[Optional[float]]
    punt_long: NotRequired[Optional[int]]


class PlayerKicking(BaseModel):
    player: str
    player_href: str
    player_id: str
    team: str
    xpm: Optional[int] = None
    xpa: Optional[int] = None
    fgm: Optional[int] = None
    fga: Optional[int] = None
    punt: int
    punt_yds: int
    punt_yds_per_punt: Optional[float] = None
    punt_long: Optional[int] = None


# --- Starters ---


class StarterTypedDict(TypedDict):
    player: str
    player_href: str
    player_id: str
    pos: str


class Starter(BaseModel):
    player: str
    player_href: str
    player_id: str
    pos: str


# --- Snap Counts ---


class SnapCountTypedDict(TypedDict):
    player: str
    player_href: str
    player_id: str
    pos: str
    offense: int
    off_pct: str
    defense: int
    def_pct: str
    special_teams: int
    st_pct: str


class SnapCount(BaseModel):
    player: str
    player_href: str
    player_id: str
    pos: str
    offense: int
    off_pct: str
    defense: int
    def_pct: str
    special_teams: int
    st_pct: str


# --- Drives ---


class DriveTypedDict(TypedDict):
    drive_num: int
    quarter: int
    time_start: str
    start_at: NotRequired[Optional[str]]
    play_count_tip: int
    time_total: str
    net_yds: int
    end_event: str


class Drive(BaseModel):
    drive_num: int
    quarter: int
    time_start: str
    start_at: Optional[str] = None
    play_count_tip: int
    time_total: str
    net_yds: int
    end_event: str


# --- Top-level Game Details ---


class GameDetailsTypedDict(TypedDict):
    scorebox: ScoreboxTypedDict
    linescore: List[LinescoreEntryTypedDict]
    scoring: List[ScoringPlayTypedDict]
    game_info: Dict[str, str]
    officials: Dict[str, str]
    expected_points: List[ExpectedPointsTypedDict]
    team_stats: Dict[str, Dict[str, str]]
    player_offense: List[PlayerOffenseTypedDict]
    player_defense: List[PlayerDefenseTypedDict]
    returns: List[PlayerReturnTypedDict]
    kicking: List[PlayerKickingTypedDict]
    home_starters: List[StarterTypedDict]
    vis_starters: List[StarterTypedDict]
    home_snap_counts: List[SnapCountTypedDict]
    vis_snap_counts: List[SnapCountTypedDict]
    home_drives: List[DriveTypedDict]
    vis_drives: List[DriveTypedDict]


class GameDetails(BaseModel):
    scorebox: Scorebox
    linescore: List[LinescoreEntry]
    scoring: List[ScoringPlay]
    game_info: Dict[str, str]
    officials: Dict[str, str]
    expected_points: List[ExpectedPoints]
    team_stats: Dict[str, Dict[str, str]]
    player_offense: List[PlayerOffense]
    player_defense: List[PlayerDefense]
    returns: List[PlayerReturn]
    kicking: List[PlayerKicking]
    home_starters: List[Starter]
    vis_starters: List[Starter]
    home_snap_counts: List[SnapCount]
    vis_snap_counts: List[SnapCount]
    home_drives: List[Drive]
    vis_drives: List[Drive]
