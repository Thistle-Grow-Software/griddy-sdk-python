"""Pydantic models for PFR stadium pages.

Covers the ``/stadiums/{StadiumId}.htm`` pages on Pro Football Reference,
including stadium bio, career leaders, best games, and notable game summaries.
"""

from __future__ import annotations

from typing import List, Optional

from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel

# --- Stadium Team (from #meta teams list) ---


class StadiumTeamTypedDict(TypedDict):
    name: str
    team_href: NotRequired[str]
    years: NotRequired[str]
    regular_season_record: NotRequired[str]
    regular_season_href: NotRequired[str]
    playoff_record: NotRequired[str]
    playoff_href: NotRequired[str]


class StadiumTeam(BaseModel):
    name: str
    team_href: Optional[str] = None
    years: Optional[str] = None
    regular_season_record: Optional[str] = None
    regular_season_href: Optional[str] = None
    playoff_record: Optional[str] = None
    playoff_href: Optional[str] = None


# --- Stadium Bio (from #meta div) ---


class StadiumBioTypedDict(TypedDict):
    name: str
    address: NotRequired[str]
    years_active: NotRequired[str]
    total_games: NotRequired[int]
    surfaces: NotRequired[str]
    teams: List[StadiumTeamTypedDict]


class StadiumBio(BaseModel):
    name: str
    address: Optional[str] = None
    years_active: Optional[str] = None
    total_games: Optional[int] = None
    surfaces: Optional[str] = None
    teams: List[StadiumTeam] = []


# --- Stadium Leader (from leaders table) ---


class StadiumLeaderTypedDict(TypedDict):
    player: NotRequired[str]
    player_id: NotRequired[str]
    player_href: NotRequired[str]
    g: NotRequired[int]
    stats: NotRequired[str]


class StadiumLeader(BaseModel):
    player: Optional[str] = None
    player_id: Optional[str] = None
    player_href: Optional[str] = None
    g: Optional[int] = None
    stats: Optional[str] = None


# --- Stadium Best Game (from games and playoff_games tables) ---


class StadiumBestGameTypedDict(TypedDict):
    player: NotRequired[str]
    player_id: NotRequired[str]
    player_href: NotRequired[str]
    team: NotRequired[str]
    team_href: NotRequired[str]
    stats: NotRequired[str]
    boxscore_word: NotRequired[str]
    boxscore_href: NotRequired[str]


class StadiumBestGame(BaseModel):
    player: Optional[str] = None
    player_id: Optional[str] = None
    player_href: Optional[str] = None
    team: Optional[str] = None
    team_href: Optional[str] = None
    stats: Optional[str] = None
    boxscore_word: Optional[str] = None
    boxscore_href: Optional[str] = None


# --- Stadium Game Leader (stat leader in a game summary) ---


class StadiumGameLeaderTypedDict(TypedDict):
    stat_name: NotRequired[str]
    player: NotRequired[str]
    player_href: NotRequired[str]
    value: NotRequired[str]


class StadiumGameLeader(BaseModel):
    stat_name: Optional[str] = None
    player: Optional[str] = None
    player_href: Optional[str] = None
    value: Optional[str] = None


# --- Stadium Game Summary (notable game from game_summaries section) ---


class StadiumGameSummaryTypedDict(TypedDict):
    label: NotRequired[str]
    date: NotRequired[str]
    team_1: NotRequired[str]
    team_1_href: NotRequired[str]
    team_1_score: NotRequired[int]
    team_2: NotRequired[str]
    team_2_href: NotRequired[str]
    team_2_score: NotRequired[int]
    boxscore_href: NotRequired[str]
    leaders: List[StadiumGameLeaderTypedDict]


class StadiumGameSummary(BaseModel):
    label: Optional[str] = None
    date: Optional[str] = None
    team_1: Optional[str] = None
    team_1_href: Optional[str] = None
    team_1_score: Optional[int] = None
    team_2: Optional[str] = None
    team_2_href: Optional[str] = None
    team_2_score: Optional[int] = None
    boxscore_href: Optional[str] = None
    leaders: List[StadiumGameLeader] = []


# --- Stadium Profile (top-level model) ---


class StadiumProfileTypedDict(TypedDict):
    bio: StadiumBioTypedDict
    leaders: List[StadiumLeaderTypedDict]
    best_games: List[StadiumBestGameTypedDict]
    best_playoff_games: List[StadiumBestGameTypedDict]
    game_summaries: List[StadiumGameSummaryTypedDict]


class StadiumProfile(BaseModel):
    bio: StadiumBio
    leaders: List[StadiumLeader]
    best_games: List[StadiumBestGame]
    best_playoff_games: List[StadiumBestGame]
    game_summaries: List[StadiumGameSummary]
