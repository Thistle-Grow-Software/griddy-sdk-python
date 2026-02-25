from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel

# --- Team Season Metadata ---


class TeamSeasonMetaTypedDict(TypedDict, total=False):
    record: str
    division: str
    division_href: str
    coach: str
    coach_href: str
    points_for: str
    points_against: str
    expected_wl: str
    srs: str
    sos: str
    playoffs: str
    offensive_coordinator: str
    offensive_coordinator_href: str
    defensive_coordinator: str
    defensive_coordinator_href: str
    stadium: str
    stadium_href: str
    offensive_scheme: str
    defensive_alignment: str
    preseason_odds: str
    training_camp: str


class TeamSeasonMeta(BaseModel):
    record: Optional[str] = None
    division: Optional[str] = None
    division_href: Optional[str] = None
    coach: Optional[str] = None
    coach_href: Optional[str] = None
    points_for: Optional[str] = None
    points_against: Optional[str] = None
    expected_wl: Optional[str] = None
    srs: Optional[str] = None
    sos: Optional[str] = None
    playoffs: Optional[str] = None
    offensive_coordinator: Optional[str] = None
    offensive_coordinator_href: Optional[str] = None
    defensive_coordinator: Optional[str] = None
    defensive_coordinator_href: Optional[str] = None
    stadium: Optional[str] = None
    stadium_href: Optional[str] = None
    offensive_scheme: Optional[str] = None
    defensive_alignment: Optional[str] = None
    preseason_odds: Optional[str] = None
    training_camp: Optional[str] = None


# --- Season Game (from games table) ---


class SeasonGameTypedDict(TypedDict):
    week_num: str
    game_day_of_week: NotRequired[Optional[str]]
    game_date: NotRequired[Optional[str]]
    game_time: NotRequired[Optional[str]]
    boxscore_word: NotRequired[Optional[str]]
    boxscore_word_href: NotRequired[Optional[str]]
    game_outcome: NotRequired[Optional[str]]
    overtime: NotRequired[Optional[str]]
    team_record: NotRequired[Optional[str]]
    game_location: NotRequired[Optional[str]]
    opp: str
    opp_href: NotRequired[Optional[str]]
    pts_off: NotRequired[Optional[int]]
    pts_def: NotRequired[Optional[int]]
    first_down_off: NotRequired[Optional[int]]
    yards_off: NotRequired[Optional[int]]
    pass_yds_off: NotRequired[Optional[int]]
    rush_yds_off: NotRequired[Optional[int]]
    to_off: NotRequired[Optional[int]]
    first_down_def: NotRequired[Optional[int]]
    yards_def: NotRequired[Optional[int]]
    pass_yds_def: NotRequired[Optional[int]]
    rush_yds_def: NotRequired[Optional[int]]
    to_def: NotRequired[Optional[int]]
    exp_pts_off: NotRequired[Optional[float]]
    exp_pts_def: NotRequired[Optional[float]]
    exp_pts_st: NotRequired[Optional[float]]


class SeasonGame(BaseModel):
    week_num: str
    game_day_of_week: Optional[str] = None
    game_date: Optional[str] = None
    game_time: Optional[str] = None
    boxscore_word: Optional[str] = None
    boxscore_word_href: Optional[str] = None
    game_outcome: Optional[str] = None
    overtime: Optional[str] = None
    team_record: Optional[str] = None
    game_location: Optional[str] = None
    opp: str
    opp_href: Optional[str] = None
    pts_off: Optional[int] = None
    pts_def: Optional[int] = None
    first_down_off: Optional[int] = None
    yards_off: Optional[int] = None
    pass_yds_off: Optional[int] = None
    rush_yds_off: Optional[int] = None
    to_off: Optional[int] = None
    first_down_def: Optional[int] = None
    yards_def: Optional[int] = None
    pass_yds_def: Optional[int] = None
    rush_yds_def: Optional[int] = None
    to_def: Optional[int] = None
    exp_pts_off: Optional[float] = None
    exp_pts_def: Optional[float] = None
    exp_pts_st: Optional[float] = None


# --- Top-level Team Season ---


class TeamSeasonTypedDict(TypedDict):
    meta: TeamSeasonMetaTypedDict
    team_stats: Dict[str, Dict[str, Union[str, int, float, None]]]
    games: List[SeasonGameTypedDict]
    team_conversions: Dict[str, Dict[str, Union[str, int, float, None]]]
    passing: List[Dict[str, Any]]
    passing_post: List[Dict[str, Any]]
    rushing_and_receiving: List[Dict[str, Any]]


class TeamSeason(BaseModel):
    meta: TeamSeasonMeta
    team_stats: Dict[str, Dict[str, Union[str, int, float, None]]]
    games: List[SeasonGame]
    team_conversions: Dict[str, Dict[str, Union[str, int, float, None]]]
    passing: List[Dict[str, Any]]
    passing_post: List[Dict[str, Any]]
    rushing_and_receiving: List[Dict[str, Any]]
