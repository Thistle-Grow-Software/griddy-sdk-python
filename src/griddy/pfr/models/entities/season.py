"""Pydantic models for PFR season overview and stat category pages.

Covers the ``/years/{year}/`` main page (standings, team stats) and
``/years/{year}/{category}.htm`` stat category pages on Pro Football Reference.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel

# --- Conference Standing (AFC / NFC standings tables) ---


class ConferenceStandingTypedDict(TypedDict):
    division: NotRequired[str]
    team: NotRequired[str]
    team_href: NotRequired[str]
    wins: NotRequired[int]
    losses: NotRequired[int]
    win_loss_perc: NotRequired[str]
    points: NotRequired[int]
    points_opp: NotRequired[int]
    points_diff: NotRequired[int]
    mov: NotRequired[str]
    sos_total: NotRequired[str]
    srs_total: NotRequired[str]
    srs_offense: NotRequired[str]
    srs_defense: NotRequired[str]


class ConferenceStanding(BaseModel):
    division: Optional[str] = None
    team: Optional[str] = None
    team_href: Optional[str] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    win_loss_perc: Optional[str] = None
    points: Optional[int] = None
    points_opp: Optional[int] = None
    points_diff: Optional[int] = None
    mov: Optional[str] = None
    sos_total: Optional[str] = None
    srs_total: Optional[str] = None
    srs_offense: Optional[str] = None
    srs_defense: Optional[str] = None


# --- Playoff Game (playoff_results table) ---


class PlayoffGameTypedDict(TypedDict):
    week_num: NotRequired[str]
    game_day_of_week: NotRequired[str]
    game_date: NotRequired[str]
    winner: NotRequired[str]
    winner_href: NotRequired[str]
    game_location: NotRequired[str]
    loser: NotRequired[str]
    loser_href: NotRequired[str]
    boxscore_word: NotRequired[str]
    boxscore_href: NotRequired[str]
    pts_win: NotRequired[int]
    pts_lose: NotRequired[int]


class PlayoffGame(BaseModel):
    week_num: Optional[str] = None
    game_day_of_week: Optional[str] = None
    game_date: Optional[str] = None
    winner: Optional[str] = None
    winner_href: Optional[str] = None
    game_location: Optional[str] = None
    loser: Optional[str] = None
    loser_href: Optional[str] = None
    boxscore_word: Optional[str] = None
    boxscore_href: Optional[str] = None
    pts_win: Optional[int] = None
    pts_lose: Optional[int] = None


# --- Playoff Standing (afc/nfc_playoff_standings tables) ---


class PlayoffStandingTypedDict(TypedDict):
    team: NotRequired[str]
    team_href: NotRequired[str]
    wins: NotRequired[int]
    losses: NotRequired[int]
    ties: NotRequired[int]
    why: NotRequired[str]
    reason: NotRequired[str]


class PlayoffStanding(BaseModel):
    team: Optional[str] = None
    team_href: Optional[str] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    ties: Optional[int] = None
    why: Optional[str] = None
    reason: Optional[str] = None


# --- Season Overview (top-level for /years/{year}/) ---


class SeasonOverviewTypedDict(TypedDict):
    afc_standings: List[ConferenceStandingTypedDict]
    nfc_standings: List[ConferenceStandingTypedDict]
    playoff_results: List[PlayoffGameTypedDict]
    afc_playoff_standings: List[PlayoffStandingTypedDict]
    nfc_playoff_standings: List[PlayoffStandingTypedDict]
    team_stats: List[Dict[str, Any]]
    passing: List[Dict[str, Any]]
    rushing: List[Dict[str, Any]]
    returns: List[Dict[str, Any]]
    kicking: List[Dict[str, Any]]
    punting: List[Dict[str, Any]]
    team_scoring: List[Dict[str, Any]]
    team_conversions: List[Dict[str, Any]]
    drives: List[Dict[str, Any]]


class SeasonOverview(BaseModel):
    afc_standings: List[ConferenceStanding] = []
    nfc_standings: List[ConferenceStanding] = []
    playoff_results: List[PlayoffGame] = []
    afc_playoff_standings: List[PlayoffStanding] = []
    nfc_playoff_standings: List[PlayoffStanding] = []
    team_stats: List[Dict[str, Any]] = []
    passing: List[Dict[str, Any]] = []
    rushing: List[Dict[str, Any]] = []
    returns: List[Dict[str, Any]] = []
    kicking: List[Dict[str, Any]] = []
    punting: List[Dict[str, Any]] = []
    team_scoring: List[Dict[str, Any]] = []
    team_conversions: List[Dict[str, Any]] = []
    drives: List[Dict[str, Any]] = []


# --- Season Stats (top-level for /years/{year}/{category}.htm) ---


class SeasonStatsTypedDict(TypedDict):
    regular_season: List[Dict[str, Any]]
    postseason: List[Dict[str, Any]]


class SeasonStats(BaseModel):
    regular_season: List[Dict[str, Any]] = []
    postseason: List[Dict[str, Any]] = []


# --- Week Game (individual game from /years/{year}/week_{number}.htm) ---


class WeekGameTypedDict(TypedDict):
    game_date: NotRequired[str]
    away_team: NotRequired[str]
    away_team_href: NotRequired[str]
    away_score: NotRequired[int]
    home_team: NotRequired[str]
    home_team_href: NotRequired[str]
    home_score: NotRequired[int]
    winner: NotRequired[str]
    boxscore_href: NotRequired[str]
    top_passer: NotRequired[str]
    top_passer_href: NotRequired[str]
    top_passer_yds: NotRequired[str]
    top_rusher: NotRequired[str]
    top_rusher_href: NotRequired[str]
    top_rusher_yds: NotRequired[str]
    top_receiver: NotRequired[str]
    top_receiver_href: NotRequired[str]
    top_receiver_yds: NotRequired[str]


class WeekGame(BaseModel):
    game_date: Optional[str] = None
    away_team: Optional[str] = None
    away_team_href: Optional[str] = None
    away_score: Optional[int] = None
    home_team: Optional[str] = None
    home_team_href: Optional[str] = None
    home_score: Optional[int] = None
    winner: Optional[str] = None
    boxscore_href: Optional[str] = None
    top_passer: Optional[str] = None
    top_passer_href: Optional[str] = None
    top_passer_yds: Optional[str] = None
    top_rusher: Optional[str] = None
    top_rusher_href: Optional[str] = None
    top_rusher_yds: Optional[str] = None
    top_receiver: Optional[str] = None
    top_receiver_href: Optional[str] = None
    top_receiver_yds: Optional[str] = None


# --- Week Summary (top-level for /years/{year}/week_{number}.htm) ---


class WeekSummaryTypedDict(TypedDict):
    games: List[WeekGameTypedDict]
    players_of_the_week: List[Dict[str, Any]]
    top_passers: List[Dict[str, Any]]
    top_receivers: List[Dict[str, Any]]
    top_rushers: List[Dict[str, Any]]
    top_defenders: List[Dict[str, Any]]


class WeekSummary(BaseModel):
    games: List[WeekGame] = []
    players_of_the_week: List[Dict[str, Any]] = []
    top_passers: List[Dict[str, Any]] = []
    top_receivers: List[Dict[str, Any]] = []
    top_rushers: List[Dict[str, Any]] = []
    top_defenders: List[Dict[str, Any]] = []
