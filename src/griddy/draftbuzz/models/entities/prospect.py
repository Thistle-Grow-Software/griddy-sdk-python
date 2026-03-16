"""Pydantic models for NFL Draft Buzz prospect data.

Ported from fbcm dataclasses to Pydantic v2 models for use in the
Griddy SDK data provider pattern.
"""

from __future__ import annotations

from typing import List, Optional, Union

from typing_extensions import TypeAlias

from ..base import DraftBuzzBaseModel

# ---------------------------------------------------------------------------
# Basic Info
# ---------------------------------------------------------------------------


class BasicInfo(DraftBuzzBaseModel):
    """Core biographical information for a draft prospect."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    position: str = ""
    college: str = ""
    class_: str = ""
    jersey: str = ""
    play_style: str = ""
    draft_year: str = ""
    last_updated: str = ""
    height: str = ""
    weight: str = ""
    forty: str = ""
    age: str = ""
    dob: str = ""
    hometown: str = ""
    photo_url: Optional[str] = None


# ---------------------------------------------------------------------------
# Ratings & Rankings
# ---------------------------------------------------------------------------


class RatingsAndRankings(DraftBuzzBaseModel):
    """Prospect ratings, rankings, and recruiting outlet grades."""

    overall_rating: Optional[float] = None
    opposition_rating: Optional[int] = None
    espn: Optional[float] = None
    rtg_247: Optional[float] = None
    rivals: Optional[float] = None
    draft_projection: Optional[str] = None
    overall_rank: Optional[int] = None
    position_rank: Optional[str] = None
    avg_overall_rank: Optional[float] = None
    avg_position_rank: Optional[float] = None


# ---------------------------------------------------------------------------
# Skill Ratings (position-specific)
# ---------------------------------------------------------------------------


class PassingSkills(DraftBuzzBaseModel):
    """Skill ratings for quarterback prospects."""

    release_speed: Optional[int] = None
    short_passing: Optional[int] = None
    medium_passing: Optional[int] = None
    long_passing: Optional[int] = None
    rush_scramble: Optional[int] = None


class RunningBackSkills(DraftBuzzBaseModel):
    """Skill ratings for running back prospects."""

    rushing: Optional[int] = None
    break_tackles: Optional[int] = None
    receiving_hands: Optional[int] = None
    pass_blocking: Optional[int] = None
    run_blocking: Optional[int] = None


class PassCatcherSkills(DraftBuzzBaseModel):
    """Skill ratings for wide receiver and tight end prospects."""

    qb_rating_when_targeted: Optional[float] = None
    hands: Optional[int] = None
    short_receiving: Optional[int] = None
    intermediate_routes: Optional[int] = None
    deep_threat: Optional[int] = None
    blocking: Optional[int] = None


class OffensiveLinemanSkills(DraftBuzzBaseModel):
    """Skill ratings for offensive lineman prospects."""

    pass_blocking: Optional[int] = None
    run_blocking: Optional[int] = None


class DefensiveLinemanSkills(DraftBuzzBaseModel):
    """Skill ratings for defensive lineman and edge rusher prospects."""

    qb_rating_when_targeted: Optional[float] = None
    tackling: Optional[int] = None
    pass_rush: Optional[int] = None
    run_defense: Optional[int] = None
    coverage: Optional[int] = None
    zone: Optional[int] = None
    man_press: Optional[int] = None


class LinebackerSkills(DraftBuzzBaseModel):
    """Skill ratings for linebacker prospects."""

    qb_rating_when_targeted: Optional[float] = None
    tackling: Optional[int] = None
    pass_rush: Optional[int] = None
    run_defense: Optional[int] = None
    coverage: Optional[int] = None
    zone: Optional[int] = None
    man_press: Optional[int] = None


class DefensiveBackSkills(DraftBuzzBaseModel):
    """Skill ratings for defensive back prospects."""

    qb_rating_when_targeted: Optional[float] = None
    tackling: Optional[int] = None
    run_defense: Optional[int] = None
    coverage: Optional[int] = None
    zone: Optional[int] = None
    man_press: Optional[int] = None


SkillRatings: TypeAlias = Union[
    PassingSkills,
    RunningBackSkills,
    PassCatcherSkills,
    OffensiveLinemanSkills,
    DefensiveLinemanSkills,
    LinebackerSkills,
    DefensiveBackSkills,
]


# ---------------------------------------------------------------------------
# Statistical Data (position-specific)
# ---------------------------------------------------------------------------


class BaseStats(DraftBuzzBaseModel):
    """Common fields shared across all stat types."""

    year: Optional[int] = None
    games_played: Optional[int] = None
    snap_count: Optional[int] = None


class PassingStats(BaseStats):
    """Quarterback passing statistics."""

    cmp: Optional[int] = None
    att: Optional[int] = None
    cmp_pct: Optional[float] = None
    yds: Optional[int] = None
    td: Optional[int] = None
    ints: Optional[int] = None
    sack: Optional[int] = None
    qb_rtg: Optional[float] = None


class RushingStats(BaseStats):
    """Rushing statistics."""

    att: Optional[int] = None
    yds: Optional[int] = None
    avg: Optional[float] = None
    td: Optional[int] = None


class ReceivingStats(BaseStats):
    """Receiving statistics."""

    rec: Optional[int] = None
    yds: Optional[int] = None
    avg: Optional[float] = None
    td: Optional[int] = None


class OffenseSkillPlayerStats(BaseStats):
    """Combined rushing and receiving stats for skill position players."""

    rushing: Optional[RushingStats] = None
    receiving: Optional[ReceivingStats] = None


class TackleStats(BaseStats):
    """Tackle statistics for defensive players."""

    total: Optional[int] = None
    solo: Optional[int] = None
    ff: Optional[int] = None
    sacks: Optional[float] = None


class InterceptionStats(BaseStats):
    """Interception statistics for defensive players."""

    ints: Optional[int] = None
    yds: Optional[int] = None
    td: Optional[int] = None
    pds: Optional[int] = None


class DefenseStats(BaseStats):
    """Combined defensive statistics."""

    tackle: Optional[TackleStats] = None
    interception: Optional[InterceptionStats] = None


Stats: TypeAlias = Union[
    PassingStats,
    RushingStats,
    ReceivingStats,
    OffenseSkillPlayerStats,
    DefenseStats,
    BaseStats,
]


# ---------------------------------------------------------------------------
# Scouting Report & Comparisons
# ---------------------------------------------------------------------------


class ScoutingReport(DraftBuzzBaseModel):
    """Scouting report text including bio, strengths, weaknesses, and summary."""

    bio: str = ""
    strengths: List[str] = []
    weaknesses: List[str] = []
    summary: Optional[str] = None


class Comparison(DraftBuzzBaseModel):
    """Player comparison with a similarity score."""

    name: Optional[str] = None
    school: Optional[str] = None
    similarity: Optional[int] = None


# ---------------------------------------------------------------------------
# Position Mappings
# ---------------------------------------------------------------------------

POSITION_TO_GROUP_MAP: dict[str, str] = {
    "QB": "QB",
    "HB": "RB",
    "FB": "RB",
    "RB": "RB",
    "WR": "WR",
    "TE": "TE",
    "OT": "OL",
    "LT": "OL",
    "RT": "OL",
    "OG": "OL",
    "LG": "OL",
    "RG": "OL",
    "C": "OL",
    "DL": "DL",
    "DT": "DL",
    "NT": "DL",
    "NG": "DL",
    "EDGE": "EDGE",
    "LE": "EDGE",
    "RE": "EDGE",
    "DE": "EDGE",
    "LB": "LB",
    "LOLB": "LB",
    "ROLB": "LB",
    "OLB": "LB",
    "MLB": "LB",
    "ILB": "LB",
    "CB": "DB",
    "LCB": "DB",
    "RCB": "DB",
    "S": "DB",
    "FS": "DB",
    "SS": "DB",
    "DB": "DB",
}


# ---------------------------------------------------------------------------
# Top-Level Prospect Profile
# ---------------------------------------------------------------------------


class ProspectProfile(DraftBuzzBaseModel):
    """Complete prospect profile combining all scraped data.

    This is the top-level model returned by the ``prospects.get_prospect()``
    endpoint. It aggregates basic info, ratings, skills, stats, scouting
    report, and player comparisons into a single typed object.
    """

    basic_info: Optional[BasicInfo] = None
    ratings: Optional[RatingsAndRankings] = None
    skills: Optional[SkillRatings] = None
    comparisons: Optional[List[Comparison]] = None
    stats: Optional[List[Stats]] = None
    scouting_report: Optional[ScoutingReport] = None
