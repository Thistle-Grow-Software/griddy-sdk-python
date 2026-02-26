"""Pydantic models for PFR NFL Draft pages.

Covers three page types:
- ``/years/{year}/draft.htm`` — annual draft results
- ``/draft/{year}-combine.htm`` — NFL Combine measurements
- ``/teams/{team}/draft.htm`` — team-specific draft history
"""

from __future__ import annotations

from typing import List, Optional

from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel

# ---------------------------------------------------------------------------
# Year Draft Pick (one row in /years/{year}/draft.htm)
# ---------------------------------------------------------------------------


class DraftPickTypedDict(TypedDict):
    draft_round: NotRequired[int]
    draft_pick: NotRequired[int]
    team: NotRequired[str]
    team_href: NotRequired[str]
    player: NotRequired[str]
    player_id: NotRequired[str]
    player_href: NotRequired[str]
    pos: NotRequired[str]
    age: NotRequired[int]
    year_max: NotRequired[int]
    all_pros_first_team: NotRequired[int]
    pro_bowls: NotRequired[int]
    years_as_primary_starter: NotRequired[int]
    career_av: NotRequired[int]
    draft_av: NotRequired[int]
    g: NotRequired[int]
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
    def_int: NotRequired[int]
    sacks: NotRequired[float]
    college: NotRequired[str]
    college_href: NotRequired[str]
    college_stats_href: NotRequired[str]


class DraftPick(BaseModel):
    draft_round: Optional[int] = None
    draft_pick: Optional[int] = None
    team: Optional[str] = None
    team_href: Optional[str] = None
    player: Optional[str] = None
    player_id: Optional[str] = None
    player_href: Optional[str] = None
    pos: Optional[str] = None
    age: Optional[int] = None
    year_max: Optional[int] = None
    all_pros_first_team: Optional[int] = None
    pro_bowls: Optional[int] = None
    years_as_primary_starter: Optional[int] = None
    career_av: Optional[int] = None
    draft_av: Optional[int] = None
    g: Optional[int] = None
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
    def_int: Optional[int] = None
    sacks: Optional[float] = None
    college: Optional[str] = None
    college_href: Optional[str] = None
    college_stats_href: Optional[str] = None


# ---------------------------------------------------------------------------
# Year Draft (top-level for /years/{year}/draft.htm)
# ---------------------------------------------------------------------------


class YearDraftTypedDict(TypedDict):
    year: NotRequired[int]
    picks: NotRequired[List[DraftPickTypedDict]]


class YearDraft(BaseModel):
    year: Optional[int] = None
    picks: List[DraftPick] = []


# ---------------------------------------------------------------------------
# Combine Entry (one row in /draft/{year}-combine.htm)
# ---------------------------------------------------------------------------


class CombineEntryTypedDict(TypedDict):
    player: NotRequired[str]
    player_id: NotRequired[str]
    player_href: NotRequired[str]
    pos: NotRequired[str]
    school: NotRequired[str]
    school_href: NotRequired[str]
    college_stats_href: NotRequired[str]
    height: NotRequired[str]
    weight: NotRequired[int]
    forty_yd: NotRequired[float]
    vertical: NotRequired[float]
    bench_reps: NotRequired[int]
    broad_jump: NotRequired[int]
    cone: NotRequired[float]
    shuttle: NotRequired[float]
    draft_info: NotRequired[str]
    drafted_team: NotRequired[str]
    drafted_round: NotRequired[str]
    drafted_pick: NotRequired[str]
    drafted_year: NotRequired[int]


class CombineEntry(BaseModel):
    player: Optional[str] = None
    player_id: Optional[str] = None
    player_href: Optional[str] = None
    pos: Optional[str] = None
    school: Optional[str] = None
    school_href: Optional[str] = None
    college_stats_href: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    forty_yd: Optional[float] = None
    vertical: Optional[float] = None
    bench_reps: Optional[int] = None
    broad_jump: Optional[int] = None
    cone: Optional[float] = None
    shuttle: Optional[float] = None
    draft_info: Optional[str] = None
    drafted_team: Optional[str] = None
    drafted_round: Optional[str] = None
    drafted_pick: Optional[str] = None
    drafted_year: Optional[int] = None


# ---------------------------------------------------------------------------
# Combine Results (top-level for /draft/{year}-combine.htm)
# ---------------------------------------------------------------------------


class CombineResultsTypedDict(TypedDict):
    year: NotRequired[int]
    entries: NotRequired[List[CombineEntryTypedDict]]


class CombineResults(BaseModel):
    year: Optional[int] = None
    entries: List[CombineEntry] = []


# ---------------------------------------------------------------------------
# Team Draft Pick (one row in /teams/{team}/draft.htm)
# ---------------------------------------------------------------------------


class TeamDraftPickTypedDict(TypedDict):
    year: NotRequired[int]
    year_href: NotRequired[str]
    draft_round: NotRequired[int]
    player: NotRequired[str]
    player_id: NotRequired[str]
    player_href: NotRequired[str]
    draft_pick: NotRequired[int]
    pos: NotRequired[str]
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
    pass_int: NotRequired[int]
    rush_att: NotRequired[int]
    rush_yds: NotRequired[int]
    rush_td: NotRequired[int]
    rec: NotRequired[int]
    rec_yds: NotRequired[int]
    rec_td: NotRequired[int]
    def_int: NotRequired[int]
    sacks: NotRequired[float]
    college: NotRequired[str]
    college_href: NotRequired[str]


class TeamDraftPick(BaseModel):
    year: Optional[int] = None
    year_href: Optional[str] = None
    draft_round: Optional[int] = None
    player: Optional[str] = None
    player_id: Optional[str] = None
    player_href: Optional[str] = None
    draft_pick: Optional[int] = None
    pos: Optional[str] = None
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
    pass_int: Optional[int] = None
    rush_att: Optional[int] = None
    rush_yds: Optional[int] = None
    rush_td: Optional[int] = None
    rec: Optional[int] = None
    rec_yds: Optional[int] = None
    rec_td: Optional[int] = None
    def_int: Optional[int] = None
    sacks: Optional[float] = None
    college: Optional[str] = None
    college_href: Optional[str] = None


# ---------------------------------------------------------------------------
# Team Draft (top-level for /teams/{team}/draft.htm)
# ---------------------------------------------------------------------------


class TeamDraftTypedDict(TypedDict):
    team: NotRequired[str]
    picks: NotRequired[List[TeamDraftPickTypedDict]]


class TeamDraft(BaseModel):
    team: Optional[str] = None
    picks: List[TeamDraftPick] = []
