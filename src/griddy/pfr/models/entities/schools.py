"""Pydantic models for PFR Schools & Colleges pages.

Covers two page types:
- ``/schools/`` — All Player Colleges (table ``#college_stats_table``)
- ``/schools/high_schools.cgi`` — High Schools (table ``#high_schools``)
"""

from __future__ import annotations

from typing import List, Optional

from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel

# ---------------------------------------------------------------------------
# College (one row in /schools/)
# ---------------------------------------------------------------------------


class CollegeTypedDict(TypedDict):
    rank: NotRequired[int]
    college_name: NotRequired[str]
    college_href: NotRequired[str]
    state: NotRequired[str]
    players: NotRequired[int]
    players_active: NotRequired[int]
    hofers: NotRequired[int]
    pro_bowls: NotRequired[int]
    games: NotRequired[int]
    touchdowns: NotRequired[int]
    best_career_av_player: NotRequired[str]
    best_career_av_player_href: NotRequired[str]
    best_career_av: NotRequired[int]
    most_td_player: NotRequired[str]
    most_td_player_href: NotRequired[str]
    most_td: NotRequired[int]
    most_games_player: NotRequired[str]
    most_games_player_href: NotRequired[str]
    most_games: NotRequired[int]


class College(BaseModel):
    rank: Optional[int] = None
    college_name: Optional[str] = None
    college_href: Optional[str] = None
    state: Optional[str] = None
    players: Optional[int] = None
    players_active: Optional[int] = None
    hofers: Optional[int] = None
    pro_bowls: Optional[int] = None
    games: Optional[int] = None
    touchdowns: Optional[int] = None
    best_career_av_player: Optional[str] = None
    best_career_av_player_href: Optional[str] = None
    best_career_av: Optional[int] = None
    most_td_player: Optional[str] = None
    most_td_player_href: Optional[str] = None
    most_td: Optional[int] = None
    most_games_player: Optional[str] = None
    most_games_player_href: Optional[str] = None
    most_games: Optional[int] = None


# ---------------------------------------------------------------------------
# CollegeList (top-level for /schools/)
# ---------------------------------------------------------------------------


class CollegeListTypedDict(TypedDict):
    colleges: NotRequired[List[CollegeTypedDict]]


class CollegeList(BaseModel):
    colleges: List[College] = []


# ---------------------------------------------------------------------------
# HighSchool (one row in /schools/high_schools.cgi)
# ---------------------------------------------------------------------------


class HighSchoolTypedDict(TypedDict):
    name: NotRequired[str]
    name_href: NotRequired[str]
    city: NotRequired[str]
    state: NotRequired[str]
    num_players: NotRequired[int]
    num_active: NotRequired[int]


class HighSchool(BaseModel):
    name: Optional[str] = None
    name_href: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    num_players: Optional[int] = None
    num_active: Optional[int] = None


# ---------------------------------------------------------------------------
# HighSchoolList (top-level for /schools/high_schools.cgi)
# ---------------------------------------------------------------------------


class HighSchoolListTypedDict(TypedDict):
    schools: NotRequired[List[HighSchoolTypedDict]]


class HighSchoolList(BaseModel):
    schools: List[HighSchool] = []
