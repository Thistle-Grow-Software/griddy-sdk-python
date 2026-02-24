from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import field_validator
from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel

# --- Player Names ---


class PlayerNamesTypedDict(TypedDict):
    first_name: str
    middle_name: str
    last_name: str
    suffix: str
    nicknames: List[str]
    pretty_name: str


class PlayerNames(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    suffix: str
    nicknames: List[str]
    pretty_name: str


# --- Birth Place ---


class BirthPlaceTypedDict(TypedDict):
    city: str
    state: str


class BirthPlace(BaseModel):
    city: str
    state: str


# --- Draft Info ---


class RoundAndOverallTypedDict(TypedDict):
    round: int
    overall: int


class RoundAndOverall(BaseModel):
    round: int
    overall: int


class DraftInfoTypedDict(TypedDict, total=False):
    team: str
    rd_and_ovr: RoundAndOverallTypedDict
    year: int


class DraftInfo(BaseModel):
    team: str
    rd_and_ovr: RoundAndOverall
    year: int


# --- Player Bio ---


class PlayerBioTypedDict(TypedDict):
    photo_url: str
    names: PlayerNamesTypedDict
    position: str
    height: int
    weight: str
    birth_date: datetime
    birth_place: BirthPlaceTypedDict
    college: str
    high_school: str
    draft: DraftInfoTypedDict
    throws: NotRequired[str]


class PlayerBio(BaseModel):
    photo_url: str
    names: PlayerNames
    position: str
    height: int
    weight: str
    birth_date: datetime
    birth_place: BirthPlace
    college: str
    high_school: str
    draft: Optional[DraftInfo] = None
    throws: Optional[str] = None

    @field_validator("draft", mode="before")
    @classmethod
    def _empty_dict_to_none(cls, v: Any) -> Any:
        if isinstance(v, dict) and not v:
            return None
        return v


# --- Jersey Number ---


class JerseyNumberTypedDict(TypedDict):
    number: str
    team: str
    start_year: int
    end_year: int


class JerseyNumber(BaseModel):
    number: str
    team: str
    start_year: int
    end_year: int


# --- Transaction ---


class TransactionTypedDict(TypedDict):
    date: date
    description: str


class Transaction(BaseModel):
    date: date
    description: str


# --- Player Statistics ---


class PlayerStatisticsTypedDict(TypedDict, total=False):
    regular_season: Dict[str, List[Dict[str, Any]]]
    post_season: Dict[str, List[Dict[str, Any]]]


class PlayerStatistics(BaseModel):
    regular_season: Dict[str, List[Dict[str, Any]]] = {}
    post_season: Dict[str, List[Dict[str, Any]]] = {}


# --- Player Profile (top-level) ---


class PlayerProfileTypedDict(TypedDict):
    bio: PlayerBioTypedDict
    jersey_numbers: List[JerseyNumberTypedDict]
    summary_stats: Dict[str, Union[int, float, str]]
    statistics: PlayerStatisticsTypedDict
    transactions: List[TransactionTypedDict]
    links: Dict[str, Dict[str, str]]
    leader_boards: Dict[str, List[str]]


class PlayerProfile(BaseModel):
    bio: PlayerBio
    jersey_numbers: List[JerseyNumber]
    summary_stats: Dict[str, Union[int, float, str]]
    statistics: PlayerStatistics
    transactions: List[Transaction]
    links: Dict[str, Dict[str, str]]
    leader_boards: Dict[str, List[str]]
