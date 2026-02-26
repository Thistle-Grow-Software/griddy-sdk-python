"""Tests for griddy.pfr.parsers.leaders and the leaders.get endpoint."""

import json
from unittest.mock import patch

import pytest

from griddy.pfr import GriddyPFR
from griddy.pfr.models.entities.leaders import (
    Leaderboard,
    LeaderEntry,
)
from griddy.pfr.parsers.leaders import LeadersParser
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "leaders"


@pytest.fixture
def parser() -> LeadersParser:
    return LeadersParser()


# ---------------------------------------------------------------------------
# Career fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def career_html() -> str:
    return (FIXTURE_DIR / "pass_yds_career.htm").read_text()


@pytest.fixture(scope="module")
def career_parsed(career_html: str) -> dict:
    return LeadersParser().parse(career_html, stat="pass_yds", scope="career")


@pytest.fixture(scope="module")
def career_board(career_parsed: dict) -> Leaderboard:
    return Leaderboard.model_validate(career_parsed)


# ---------------------------------------------------------------------------
# Single-season fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def single_season_html() -> str:
    return (FIXTURE_DIR / "rush_td_single_season.htm").read_text()


@pytest.fixture(scope="module")
def single_season_parsed(single_season_html: str) -> dict:
    return LeadersParser().parse(
        single_season_html, stat="rush_td", scope="single_season"
    )


@pytest.fixture(scope="module")
def single_season_board(single_season_parsed: dict) -> Leaderboard:
    return Leaderboard.model_validate(single_season_parsed)


# ---------------------------------------------------------------------------
# Career parse -- smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCareerSmoke:
    """Smoke test: career fixture should parse without errors."""

    def test_parse_returns_dict(self, career_parsed):
        assert isinstance(career_parsed, dict)

    def test_parsed_data_has_all_keys(self, career_parsed):
        expected_keys = {"stat", "scope", "title", "entries"}
        assert set(career_parsed.keys()) == expected_keys

    def test_model_validates_successfully(self, career_board):
        assert isinstance(career_board, Leaderboard)

    def test_stat_is_set(self, career_board):
        assert career_board.stat == "pass_yds"

    def test_scope_is_set(self, career_board):
        assert career_board.scope == "career"

    def test_title_is_set(self, career_board):
        assert career_board.title == "NFL Passing Yards Career Leaders"


# ---------------------------------------------------------------------------
# Career entries
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCareerEntries:
    def test_entry_count(self, career_board):
        assert len(career_board.entries) == 250

    def test_entry_is_model(self, career_board):
        assert isinstance(career_board.entries[0], LeaderEntry)

    # First entry: Tom Brady
    def test_first_rank(self, career_board):
        assert career_board.entries[0].rank == 1

    def test_first_player(self, career_board):
        assert career_board.entries[0].player == "Tom Brady"

    def test_first_player_id(self, career_board):
        assert career_board.entries[0].player_id == "BradTo00"

    def test_first_player_href(self, career_board):
        assert career_board.entries[0].player_href == "/players/B/BradTo00.htm"

    def test_first_stat_value(self, career_board):
        assert career_board.entries[0].stat_value == "89,214"

    def test_first_years(self, career_board):
        assert career_board.entries[0].years == "2000-2022"

    def test_first_team(self, career_board):
        assert career_board.entries[0].team == "2TM"

    def test_first_no_year(self, career_board):
        """Career entries should not have a single year field."""
        assert career_board.entries[0].year is None

    # Second entry: Drew Brees (HOF)
    def test_second_player(self, career_board):
        assert career_board.entries[1].player == "Drew Brees"

    def test_second_is_hof(self, career_board):
        assert career_board.entries[1].is_hof is True

    # Active player detection
    def test_active_player(self, career_board):
        """Find an active player (wrapped in <strong>) and verify is_active."""
        active = [e for e in career_board.entries if e.is_active]
        assert len(active) > 0

    def test_inactive_player(self, career_board):
        """Tom Brady is retired and should not be active."""
        assert career_board.entries[0].is_active is False

    # Single-team player with team link
    def test_single_team_has_href(self, career_board):
        """Find a single-team player and verify the team_href."""
        single_team = [e for e in career_board.entries if e.team_href is not None]
        assert len(single_team) > 0
        assert single_team[0].team_href.startswith("/teams/")

    # Multi-team player without team link
    def test_multi_team_no_href(self, career_board):
        """Tom Brady is multi-team and should not have a team_href."""
        assert career_board.entries[0].team_href is None

    # Last entry
    def test_last_rank(self, career_board):
        assert career_board.entries[249].rank is not None


# ---------------------------------------------------------------------------
# Single-season parse -- smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSingleSeasonSmoke:
    """Smoke test: single-season fixture should parse without errors."""

    def test_parse_returns_dict(self, single_season_parsed):
        assert isinstance(single_season_parsed, dict)

    def test_model_validates_successfully(self, single_season_board):
        assert isinstance(single_season_board, Leaderboard)

    def test_stat_is_set(self, single_season_board):
        assert single_season_board.stat == "rush_td"

    def test_scope_is_set(self, single_season_board):
        assert single_season_board.scope == "single_season"

    def test_title_is_set(self, single_season_board):
        assert (
            single_season_board.title == "NFL Rushing Touchdowns Single-Season Leaders"
        )


# ---------------------------------------------------------------------------
# Single-season entries
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSingleSeasonEntries:
    def test_entry_count(self, single_season_board):
        assert len(single_season_board.entries) == 248

    # First entry: LaDainian Tomlinson
    def test_first_rank(self, single_season_board):
        assert single_season_board.entries[0].rank == 1

    def test_first_player(self, single_season_board):
        assert single_season_board.entries[0].player == "LaDainian Tomlinson"

    def test_first_player_id(self, single_season_board):
        assert single_season_board.entries[0].player_id == "TomlLa00"

    def test_first_stat_value(self, single_season_board):
        assert single_season_board.entries[0].stat_value == "28"

    def test_first_year(self, single_season_board):
        assert single_season_board.entries[0].year == "2006"

    def test_first_year_href(self, single_season_board):
        assert single_season_board.entries[0].year_href == "/years/2006/leaders.htm"

    def test_first_no_years(self, single_season_board):
        """Single-season entries should not have a years field."""
        assert single_season_board.entries[0].years is None

    def test_first_team(self, single_season_board):
        assert single_season_board.entries[0].team == "SDG"

    def test_first_team_href(self, single_season_board):
        assert single_season_board.entries[0].team_href == "/teams/sdg/2006.htm"

    def test_first_is_hof(self, single_season_board):
        assert single_season_board.entries[0].is_hof is True

    # Tied entries (empty rank)
    def test_tied_entries_exist(self, single_season_board):
        """Some entries should have None rank due to ties."""
        tied = [e for e in single_season_board.entries if e.rank is None]
        assert len(tied) > 0

    # Same player can appear multiple times
    def test_duplicate_player(self, single_season_board):
        """A player can appear multiple times for different seasons."""
        players = [e.player for e in single_season_board.entries]
        unique = set(players)
        assert len(unique) < len(players)


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestJsonSerialization:
    def test_serializes(self, career_board):
        output = career_board.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert len(loaded["entries"]) == 250

    def test_round_trip(self, career_board):
        dumped = career_board.model_dump()
        assert len(dumped["entries"]) == 250
        assert dumped["stat"] == "pass_yds"
        assert dumped["scope"] == "career"


# ---------------------------------------------------------------------------
# Leaders endpoint (get)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetEndpoint:
    def test_get_returns_model(self, career_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.leaders.browserless,
            "get_page_content",
            return_value=career_html,
        ) as mock_fetch:
            result = pfr.leaders.get(stat="pass_yds", scope="career")

        mock_fetch.assert_called_once()
        assert isinstance(result, Leaderboard)
        assert len(result.entries) == 250

    def test_get_url_construction(self, career_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.leaders.browserless,
            "get_page_content",
            return_value=career_html,
        ) as mock_fetch:
            pfr.leaders.get(stat="pass_yds", scope="career")

        url = mock_fetch.call_args[0][0]
        assert (
            url == "https://www.pro-football-reference.com/leaders/pass_yds_career.htm"
        )

    def test_get_wait_for_element(self, career_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.leaders.browserless,
            "get_page_content",
            return_value=career_html,
        ) as mock_fetch:
            pfr.leaders.get(stat="pass_yds", scope="career")

        assert mock_fetch.call_args[1]["wait_for_element"] == "table.stats_table"

    def test_get_single_season(self, single_season_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.leaders.browserless,
            "get_page_content",
            return_value=single_season_html,
        ) as mock_fetch:
            result = pfr.leaders.get(stat="rush_td", scope="single_season")

        url = mock_fetch.call_args[0][0]
        assert (
            url
            == "https://www.pro-football-reference.com/leaders/rush_td_single_season.htm"
        )
        assert isinstance(result, Leaderboard)
        assert result.stat == "rush_td"
        assert result.scope == "single_season"
