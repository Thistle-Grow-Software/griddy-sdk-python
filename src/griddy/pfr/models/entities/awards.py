"""Pydantic models for PFR Awards, Hall of Fame, and Pro Bowl pages.

Covers three page types:
- ``/awards/{award}.htm`` — award history (table ``#awards``)
- ``/hof/`` — Hall of Fame inductees (table ``#hof_players``)
- ``/years/{year}/probowl.htm`` — Pro Bowl roster (table ``#pro_bowl``)
"""

from __future__ import annotations

from typing import List, Optional

from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel

# ---------------------------------------------------------------------------
# Award Winner (one row in /awards/{award}.htm)
# ---------------------------------------------------------------------------


class AwardWinnerTypedDict(TypedDict):
    year: NotRequired[int]
    year_href: NotRequired[str]
    league: NotRequired[str]
    pos: NotRequired[str]
    player: NotRequired[str]
    player_id: NotRequired[str]
    player_href: NotRequired[str]
    team: NotRequired[str]
    team_href: NotRequired[str]
    voting_href: NotRequired[str]


class AwardWinner(BaseModel):
    year: Optional[int] = None
    year_href: Optional[str] = None
    league: Optional[str] = None
    pos: Optional[str] = None
    player: Optional[str] = None
    player_id: Optional[str] = None
    player_href: Optional[str] = None
    team: Optional[str] = None
    team_href: Optional[str] = None
    voting_href: Optional[str] = None


# ---------------------------------------------------------------------------
# Award History (top-level for /awards/{award}.htm)
# ---------------------------------------------------------------------------


class AwardHistoryTypedDict(TypedDict):
    award: NotRequired[str]
    winners: NotRequired[List[AwardWinnerTypedDict]]


class AwardHistory(BaseModel):
    award: Optional[str] = None
    winners: List[AwardWinner] = []


# ---------------------------------------------------------------------------
# HOF Player (one row in /hof/)
# ---------------------------------------------------------------------------


class HofPlayerTypedDict(TypedDict):
    rank: NotRequired[int]
    player: NotRequired[str]
    player_id: NotRequired[str]
    player_href: NotRequired[str]
    pos: NotRequired[str]
    year_induction: NotRequired[int]
    year_induction_href: NotRequired[str]
    year_min: NotRequired[int]
    year_max: NotRequired[int]
    all_pros_first_team: NotRequired[int]
    pro_bowls: NotRequired[int]
    years_as_primary_starter: NotRequired[int]
    career_av: NotRequired[int]
    g: NotRequired[int]
    pass_cmp: NotRequired[int]
    pass_att: NotRequired[int]
    pass_yds: NotRequired[int]
    pass_td: NotRequired[int]
    pass_long: NotRequired[int]
    pass_int: NotRequired[int]
    pass_sacked: NotRequired[int]
    pass_sacked_yds: NotRequired[int]
    rush_att: NotRequired[int]
    rush_yds: NotRequired[int]
    rush_td: NotRequired[int]
    rush_long: NotRequired[int]
    rec: NotRequired[int]
    rec_yds: NotRequired[int]
    rec_td: NotRequired[int]
    rec_long: NotRequired[int]
    all_purpose_yds: NotRequired[int]
    all_td: NotRequired[int]
    tackles_combined: NotRequired[int]
    sacks: NotRequired[float]
    def_int: NotRequired[int]


class HofPlayer(BaseModel):
    rank: Optional[int] = None
    player: Optional[str] = None
    player_id: Optional[str] = None
    player_href: Optional[str] = None
    pos: Optional[str] = None
    year_induction: Optional[int] = None
    year_induction_href: Optional[str] = None
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    all_pros_first_team: Optional[int] = None
    pro_bowls: Optional[int] = None
    years_as_primary_starter: Optional[int] = None
    career_av: Optional[int] = None
    g: Optional[int] = None
    pass_cmp: Optional[int] = None
    pass_att: Optional[int] = None
    pass_yds: Optional[int] = None
    pass_td: Optional[int] = None
    pass_long: Optional[int] = None
    pass_int: Optional[int] = None
    pass_sacked: Optional[int] = None
    pass_sacked_yds: Optional[int] = None
    rush_att: Optional[int] = None
    rush_yds: Optional[int] = None
    rush_td: Optional[int] = None
    rush_long: Optional[int] = None
    rec: Optional[int] = None
    rec_yds: Optional[int] = None
    rec_td: Optional[int] = None
    rec_long: Optional[int] = None
    all_purpose_yds: Optional[int] = None
    all_td: Optional[int] = None
    tackles_combined: Optional[int] = None
    sacks: Optional[float] = None
    def_int: Optional[int] = None


# ---------------------------------------------------------------------------
# Hall of Fame (top-level for /hof/)
# ---------------------------------------------------------------------------


class HallOfFameTypedDict(TypedDict):
    players: NotRequired[List[HofPlayerTypedDict]]


class HallOfFame(BaseModel):
    players: List[HofPlayer] = []


# ---------------------------------------------------------------------------
# Pro Bowl Player (one row in /years/{year}/probowl.htm)
# ---------------------------------------------------------------------------


class ProBowlPlayerTypedDict(TypedDict):
    pos: NotRequired[str]
    player: NotRequired[str]
    player_id: NotRequired[str]
    player_href: NotRequired[str]
    is_starter: NotRequired[bool]
    did_not_play: NotRequired[bool]
    is_replacement: NotRequired[bool]
    conference: NotRequired[str]
    team: NotRequired[str]
    team_href: NotRequired[str]
    age: NotRequired[int]
    experience: NotRequired[int]
    g: NotRequired[int]
    gs: NotRequired[int]
    pass_cmp: NotRequired[int]
    pass_att: NotRequired[int]
    pass_yds: NotRequired[int]
    pass_td: NotRequired[int]
    pass_int: NotRequired[int]
    rush_att: NotRequired[int]
    rush_yds: NotRequired[int]
    rush_td: NotRequired[int]
    rec: NotRequired[int]
    rec_yds: NotRequired[int]
    rec_td: NotRequired[int]
    tackles_solo: NotRequired[int]
    sacks: NotRequired[float]
    def_int: NotRequired[int]
    all_pro_string: NotRequired[str]


class ProBowlPlayer(BaseModel):
    pos: Optional[str] = None
    player: Optional[str] = None
    player_id: Optional[str] = None
    player_href: Optional[str] = None
    is_starter: Optional[bool] = None
    did_not_play: Optional[bool] = None
    is_replacement: Optional[bool] = None
    conference: Optional[str] = None
    team: Optional[str] = None
    team_href: Optional[str] = None
    age: Optional[int] = None
    experience: Optional[int] = None
    g: Optional[int] = None
    gs: Optional[int] = None
    pass_cmp: Optional[int] = None
    pass_att: Optional[int] = None
    pass_yds: Optional[int] = None
    pass_td: Optional[int] = None
    pass_int: Optional[int] = None
    rush_att: Optional[int] = None
    rush_yds: Optional[int] = None
    rush_td: Optional[int] = None
    rec: Optional[int] = None
    rec_yds: Optional[int] = None
    rec_td: Optional[int] = None
    tackles_solo: Optional[int] = None
    sacks: Optional[float] = None
    def_int: Optional[int] = None
    all_pro_string: Optional[str] = None


# ---------------------------------------------------------------------------
# Pro Bowl Roster (top-level for /years/{year}/probowl.htm)
# ---------------------------------------------------------------------------


class ProBowlRosterTypedDict(TypedDict):
    year: NotRequired[int]
    players: NotRequired[List[ProBowlPlayerTypedDict]]


class ProBowlRoster(BaseModel):
    year: Optional[int] = None
    players: List[ProBowlPlayer] = []
