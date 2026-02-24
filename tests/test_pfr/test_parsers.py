"""Tests for griddy.pfr.utils.parsers module."""

from pathlib import Path

import pytest

from griddy.pfr.models.entities.schedule_game import ScheduleGame
from griddy.pfr.utils.parsers import ScheduleParser

# Path to the saved HTML fixture at the repo root.
FIXTURE_PATH = Path(__file__).resolve().parents[2] / "pfr_2015_sked.html"


@pytest.fixture
def parser() -> ScheduleParser:
    return ScheduleParser()


@pytest.fixture
def schedule_html() -> str:
    """Load the 2015 PFR schedule HTML fixture."""
    return FIXTURE_PATH.read_text()


@pytest.mark.unit
class TestParseScheduleTable:
    def test_returns_list_of_schedule_games(
        self, parser: ScheduleParser, schedule_html: str
    ):
        result = parser.parse(schedule_html)
        assert isinstance(result, list)
        assert len(result) > 0
        assert isinstance(result[0], ScheduleGame)

    def test_game_count(self, parser: ScheduleParser, schedule_html: str):
        """2015 season: 256 regular-season + 11 playoff = 267 games."""
        games = parser.parse(schedule_html)
        assert len(games) == 267

    def test_first_game_is_week_1(self, parser: ScheduleParser, schedule_html: str):
        games = parser.parse(schedule_html)
        first = games[0]
        assert first.week_num == "1"
        assert first.game_date == "2015-09-10"
        assert first.winner == "New England Patriots"
        assert first.loser == "Pittsburgh Steelers"
        assert first.pts_win == 28
        assert first.pts_lose == 21

    def test_first_game_links(self, parser: ScheduleParser, schedule_html: str):
        games = parser.parse(schedule_html)
        first = games[0]
        assert first.winner_href == "/teams/nwe/2015.htm"
        assert first.loser_href == "/teams/pit/2015.htm"
        assert first.boxscore_word_href == "/boxscores/201509100nwe.htm"

    def test_last_game_is_super_bowl(self, parser: ScheduleParser, schedule_html: str):
        games = parser.parse(schedule_html)
        last = games[-1]
        assert last.week_num == "SuperBowl"
        assert last.winner == "Denver Broncos"
        assert last.loser == "Carolina Panthers"
        assert last.pts_win == 24
        assert last.pts_lose == 10

    def test_away_game_has_at_symbol(self, parser: ScheduleParser, schedule_html: str):
        """Green Bay @ Chicago in week 1 (second game)."""
        games = parser.parse(schedule_html)
        gb_at_chi = games[1]
        assert gb_at_chi.winner == "Green Bay Packers"
        assert gb_at_chi.game_location == "@"

    def test_home_game_has_empty_location(
        self, parser: ScheduleParser, schedule_html: str
    ):
        """NE vs PIT in week 1 (first game) — home game."""
        games = parser.parse(schedule_html)
        first = games[0]
        assert first.game_location == ""

    def test_numeric_fields_are_ints(self, parser: ScheduleParser, schedule_html: str):
        games = parser.parse(schedule_html)
        first = games[0]
        for field in (
            "pts_win",
            "pts_lose",
            "yards_win",
            "to_win",
            "yards_lose",
            "to_lose",
        ):
            assert isinstance(getattr(first, field), int), f"{field} should be int"

    def test_thead_separator_rows_excluded(
        self, parser: ScheduleParser, schedule_html: str
    ):
        """No game should have 'Week' as its week_num (that's a thead row)."""
        games = parser.parse(schedule_html)
        for game in games:
            assert game.week_num != "Week"

    def test_playoffs_divider_excluded(
        self, parser: ScheduleParser, schedule_html: str
    ):
        """The 'Playoffs' label row should not appear as a game."""
        games = parser.parse(schedule_html)
        for game in games:
            assert game.game_date != "Playoffs"

    def test_all_games_have_required_fields(
        self, parser: ScheduleParser, schedule_html: str
    ):
        games = parser.parse(schedule_html)
        for i, game in enumerate(games):
            assert game.week_num, f"Game {i} missing week_num"
            assert (
                game.game_day_of_week is not None
            ), f"Game {i} missing game_day_of_week"
            assert game.game_date, f"Game {i} missing game_date"
            assert game.winner, f"Game {i} missing winner"
            assert game.loser, f"Game {i} missing loser"

    def test_raises_on_missing_table(self, parser: ScheduleParser):
        with pytest.raises(ValueError, match="Could not find"):
            parser.parse("<html><body>No table here</body></html>")

    def test_super_bowl_neutral_site(self, parser: ScheduleParser, schedule_html: str):
        """Super Bowl game_location should be 'N' for neutral site."""
        games = parser.parse(schedule_html)
        last = games[-1]
        assert last.game_location == "N"
