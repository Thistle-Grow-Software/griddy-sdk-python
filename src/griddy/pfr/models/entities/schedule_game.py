from __future__ import annotations

from typing import Optional

from typing_extensions import NotRequired, TypedDict

from ...types import BaseModel


class ScheduleGameTypedDict(TypedDict):
    week_num: str
    game_day_of_week: str
    game_date: str
    gametime: NotRequired[Optional[str]]
    winner: str
    game_location: str
    loser: str
    boxscore_word: NotRequired[Optional[str]]
    pts_win: NotRequired[Optional[int]]
    pts_lose: NotRequired[Optional[int]]
    yards_win: NotRequired[Optional[int]]
    to_win: NotRequired[Optional[int]]
    yards_lose: NotRequired[Optional[int]]
    to_lose: NotRequired[Optional[int]]
    winner_href: NotRequired[Optional[str]]
    loser_href: NotRequired[Optional[str]]
    boxscore_word_href: NotRequired[Optional[str]]


class ScheduleGame(BaseModel):
    week_num: str
    game_day_of_week: str
    game_date: str
    gametime: Optional[str] = None
    winner: str
    game_location: str
    loser: str
    boxscore_word: Optional[str] = None
    pts_win: Optional[int] = None
    pts_lose: Optional[int] = None
    yards_win: Optional[int] = None
    to_win: Optional[int] = None
    yards_lose: Optional[int] = None
    to_lose: Optional[int] = None
    winner_href: Optional[str] = None
    loser_href: Optional[str] = None
    boxscore_word_href: Optional[str] = None
