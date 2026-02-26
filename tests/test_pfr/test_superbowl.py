"""Tests for PFR Super Bowl endpoints.

Covers:
- Super Bowl history (``/super-bowl/``)
- Super Bowl leaders (``/super-bowl/leaders.htm``)
- Super Bowl standings (``/super-bowl/standings.htm``)
"""

from unittest.mock import patch

import pytest

from griddy.pfr.models import (
    SuperBowlGame,
    SuperBowlHistory,
    SuperBowlLeaderEntry,
    SuperBowlLeaders,
    SuperBowlLeaderTable,
    SuperBowlQB,
    SuperBowlStanding,
    SuperBowlStandings,
)
from griddy.pfr.parsers.superbowl import SuperBowlParser
from griddy.pfr.sdk import GriddyPFR
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "super_bowl"

_parser = SuperBowlParser()

# -------------------------------------------------------------------------
# Fixtures — History
# -------------------------------------------------------------------------


@pytest.fixture(scope="module")
def history_html() -> str:
    return (FIXTURE_DIR / "history.htm").read_text()


@pytest.fixture(scope="module")
def history_parsed(history_html: str) -> dict:
    return _parser.parse_history(history_html)


@pytest.fixture(scope="module")
def history_model(history_parsed: dict) -> SuperBowlHistory:
    return SuperBowlHistory.model_validate(history_parsed)


# -------------------------------------------------------------------------
# Fixtures — Leaders
# -------------------------------------------------------------------------


@pytest.fixture(scope="module")
def leaders_html() -> str:
    return (FIXTURE_DIR / "leaders.htm").read_text()


@pytest.fixture(scope="module")
def leaders_parsed(leaders_html: str) -> dict:
    return _parser.parse_leaders(leaders_html)


@pytest.fixture(scope="module")
def leaders_model(leaders_parsed: dict) -> SuperBowlLeaders:
    return SuperBowlLeaders.model_validate(leaders_parsed)


# -------------------------------------------------------------------------
# Fixtures — Standings
# -------------------------------------------------------------------------


@pytest.fixture(scope="module")
def standings_html() -> str:
    return (FIXTURE_DIR / "standings.htm").read_text()


@pytest.fixture(scope="module")
def standings_parsed(standings_html: str) -> dict:
    return _parser.parse_standings(standings_html)


@pytest.fixture(scope="module")
def standings_model(standings_parsed: dict) -> SuperBowlStandings:
    return SuperBowlStandings.model_validate(standings_parsed)


# =========================================================================
# History — Smoke tests
# =========================================================================


@pytest.mark.unit
class TestHistorySmoke:
    def test_parse_returns_dict(self, history_parsed):
        assert isinstance(history_parsed, dict)

    def test_has_games_key(self, history_parsed):
        assert "games" in history_parsed

    def test_model_validates(self, history_model):
        assert isinstance(history_model, SuperBowlHistory)

    def test_game_count(self, history_model):
        assert len(history_model.games) == 60


# =========================================================================
# History — Game data
# =========================================================================


@pytest.mark.unit
class TestHistoryGames:
    def test_first_game_is_most_recent(self, history_model):
        first = history_model.games[0]
        assert isinstance(first, SuperBowlGame)
        assert first.superbowl == "LX"
        assert first.superbowl_number == 60

    def test_first_game_teams(self, history_model):
        first = history_model.games[0]
        assert first.winner == "Seattle Seahawks"
        assert first.winner_href == "/teams/sea/2025.htm"
        assert first.winner_points == 29
        assert first.loser == "New England Patriots"
        assert first.loser_href == "/teams/nwe/2025.htm"
        assert first.loser_points == 13

    def test_first_game_mvp(self, history_model):
        first = history_model.games[0]
        assert first.mvp == "Kenneth Walker III"
        assert first.mvp_href == "/players/W/WalkKe00.htm"

    def test_first_game_venue(self, history_model):
        first = history_model.games[0]
        assert first.stadium == "Levi's Stadium"
        assert first.city == "Santa Clara"
        assert first.state == "California"

    def test_first_game_date(self, history_model):
        first = history_model.games[0]
        assert first.game_date == "Feb 8, 2026"

    def test_boxscore_href(self, history_model):
        first = history_model.games[0]
        assert first.boxscore_href == "/boxscores/202602080nwe.htm"

    def test_last_game_is_super_bowl_i(self, history_model):
        last = history_model.games[-1]
        assert last.superbowl == "I"
        assert last.superbowl_number == 1
        assert last.winner == "Green Bay Packers"
        assert last.winner_points == 35
        assert last.loser == "Kansas City Chiefs"
        assert last.loser_points == 10

    def test_mvp_name_strips_plus_marker(self, history_model):
        """MVPs like 'Bart Starr+' should have the '+' stripped from the name."""
        last = history_model.games[-1]
        assert last.mvp == "Bart Starr"
        assert "+" not in (last.mvp or "")


# =========================================================================
# Leaders — Smoke tests
# =========================================================================


@pytest.mark.unit
class TestLeadersSmoke:
    def test_parse_returns_dict(self, leaders_parsed):
        assert isinstance(leaders_parsed, dict)

    def test_has_tables_key(self, leaders_parsed):
        assert "tables" in leaders_parsed

    def test_model_validates(self, leaders_model):
        assert isinstance(leaders_model, SuperBowlLeaders)

    def test_table_count(self, leaders_model):
        assert len(leaders_model.tables) == 53


# =========================================================================
# Leaders — Table data
# =========================================================================


@pytest.mark.unit
class TestLeadersTables:
    def test_first_table_is_game_passer_rating(self, leaders_model):
        first = leaders_model.tables[0]
        assert isinstance(first, SuperBowlLeaderTable)
        assert first.category == "Game Passer Rating"

    def test_first_table_top_entry(self, leaders_model):
        entry = leaders_model.tables[0].entries[0]
        assert isinstance(entry, SuperBowlLeaderEntry)
        assert entry.rank == 1
        assert entry.player == "Phil Simms"
        assert entry.player_href == "/players/S/SimmPh00.htm"
        assert entry.value == "150.9"

    def test_game_leader_has_description(self, leaders_model):
        """Game leaders should have a description like 'NYG·XXI'."""
        entry = leaders_model.tables[0].entries[0]
        assert entry.description is not None
        assert "NYG" in entry.description

    def test_career_leader_has_games_description(self, leaders_model):
        """Career leaders should have a description like '4G'."""
        career_table = leaders_model.tables[1]
        assert career_table.category == "Career Passer Rating"
        entry = career_table.entries[0]
        assert entry.description is not None
        assert entry.description.endswith("G")

    def test_career_passer_rating_first_entry(self, leaders_model):
        entry = leaders_model.tables[1].entries[0]
        assert entry.player == "Joe Montana"
        assert entry.value == "127.8"

    def test_last_table(self, leaders_model):
        last = leaders_model.tables[-1]
        assert last.category == "Career Tackles Combined"
        assert len(last.entries) > 0

    def test_passing_td_table(self, leaders_model):
        """Game Passing TD table should include multi-TD games."""
        td_table = next(
            t for t in leaders_model.tables if t.category == "Game Passing TD"
        )
        first = td_table.entries[0]
        assert first.player == "Steve Young"
        assert first.value == "6"


# =========================================================================
# Standings — Smoke tests
# =========================================================================


@pytest.mark.unit
class TestStandingsSmoke:
    def test_parse_returns_dict(self, standings_parsed):
        assert isinstance(standings_parsed, dict)

    def test_has_teams_key(self, standings_parsed):
        assert "teams" in standings_parsed

    def test_model_validates(self, standings_model):
        assert isinstance(standings_model, SuperBowlStandings)

    def test_team_count(self, standings_model):
        assert len(standings_model.teams) == 28


# =========================================================================
# Standings — Team data
# =========================================================================


@pytest.mark.unit
class TestStandingsTeams:
    def test_first_team_is_steelers(self, standings_model):
        first = standings_model.teams[0]
        assert isinstance(first, SuperBowlStanding)
        assert first.rank == 1
        assert first.team == "Pittsburgh Steelers"
        assert first.team_href == "/teams/pit/"

    def test_first_team_record(self, standings_model):
        first = standings_model.teams[0]
        assert first.games == 8
        assert first.wins == 6
        assert first.losses == 2
        assert first.win_loss_pct == ".750"

    def test_first_team_points(self, standings_model):
        first = standings_model.teams[0]
        assert first.points == 193
        assert first.points_opp == 164
        assert first.points_diff == "+29"

    def test_first_team_qbs(self, standings_model):
        first = standings_model.teams[0]
        assert len(first.qbs) == 3
        assert all(isinstance(qb, SuperBowlQB) for qb in first.qbs)
        bradshaw = first.qbs[0]
        assert bradshaw.player == "Terry Bradshaw"
        assert bradshaw.record == "4-0"
        assert bradshaw.player_href == "/players/B/BradTe00.htm"

    def test_last_team(self, standings_model):
        last = standings_model.teams[-1]
        assert last.team == "Arizona Cardinals"
        assert last.wins == 0
        assert last.losses == 1
        assert len(last.qbs) == 1
        assert last.qbs[0].player == "Kurt Warner"
        assert last.qbs[0].record == "0-1"

    def test_negative_point_diff(self, standings_model):
        """Teams with losing records should have negative point differentials."""
        last = standings_model.teams[-1]
        assert last.points_diff == "-4"

    def test_single_qb_team(self, standings_model):
        """Teams with only one Super Bowl should have exactly one QB."""
        last = standings_model.teams[-1]
        assert len(last.qbs) == 1


# =========================================================================
# JSON serialization
# =========================================================================


@pytest.mark.unit
class TestJsonSerialization:
    def test_history_roundtrip(self, history_model):
        data = history_model.model_dump()
        rebuilt = SuperBowlHistory.model_validate(data)
        assert len(rebuilt.games) == len(history_model.games)

    def test_leaders_roundtrip(self, leaders_model):
        data = leaders_model.model_dump()
        rebuilt = SuperBowlLeaders.model_validate(data)
        assert len(rebuilt.tables) == len(leaders_model.tables)

    def test_standings_roundtrip(self, standings_model):
        data = standings_model.model_dump()
        rebuilt = SuperBowlStandings.model_validate(data)
        assert len(rebuilt.teams) == len(standings_model.teams)

    def test_standings_qbs_preserved(self, standings_model):
        data = standings_model.model_dump()
        rebuilt = SuperBowlStandings.model_validate(data)
        assert rebuilt.teams[0].qbs[0].player == "Terry Bradshaw"
        assert rebuilt.teams[0].qbs[0].record == "4-0"


# =========================================================================
# Endpoint integration tests (mocked)
# =========================================================================


@pytest.mark.unit
class TestHistoryEndpoint:
    def test_history_returns_model(self, history_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.superbowl.browserless,
            "get_page_content",
            return_value=history_html,
        ) as mock_fetch:
            result = pfr.superbowl.history()

        mock_fetch.assert_called_once()
        assert isinstance(result, SuperBowlHistory)
        assert len(result.games) == 60

    def test_history_url_construction(self, history_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.superbowl.browserless,
            "get_page_content",
            return_value=history_html,
        ) as mock_fetch:
            pfr.superbowl.history()

        call_args = mock_fetch.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get("url", "")
        assert "/super-bowl/" in url

    def test_history_wait_for_element(self, history_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.superbowl.browserless,
            "get_page_content",
            return_value=history_html,
        ) as mock_fetch:
            pfr.superbowl.history()

        call_args = mock_fetch.call_args
        wait_for = (
            call_args[1].get("wait_for_element") if call_args[1] else call_args[0][1]
        )
        assert wait_for == "#super_bowls"


@pytest.mark.unit
class TestLeadersEndpoint:
    def test_leaders_returns_model(self, leaders_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.superbowl.browserless,
            "get_page_content",
            return_value=leaders_html,
        ) as mock_fetch:
            result = pfr.superbowl.leaders()

        mock_fetch.assert_called_once()
        assert isinstance(result, SuperBowlLeaders)
        assert len(result.tables) == 53

    def test_leaders_url_construction(self, leaders_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.superbowl.browserless,
            "get_page_content",
            return_value=leaders_html,
        ) as mock_fetch:
            pfr.superbowl.leaders()

        call_args = mock_fetch.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get("url", "")
        assert "/super-bowl/leaders.htm" in url


@pytest.mark.unit
class TestStandingsEndpoint:
    def test_standings_returns_model(self, standings_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.superbowl.browserless,
            "get_page_content",
            return_value=standings_html,
        ) as mock_fetch:
            result = pfr.superbowl.standings()

        mock_fetch.assert_called_once()
        assert isinstance(result, SuperBowlStandings)
        assert len(result.teams) == 28

    def test_standings_url_construction(self, standings_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.superbowl.browserless,
            "get_page_content",
            return_value=standings_html,
        ) as mock_fetch:
            pfr.superbowl.standings()

        call_args = mock_fetch.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get("url", "")
        assert "/super-bowl/standings.htm" in url

    def test_standings_wait_for_element(self, standings_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.superbowl.browserless,
            "get_page_content",
            return_value=standings_html,
        ) as mock_fetch:
            pfr.superbowl.standings()

        call_args = mock_fetch.call_args
        wait_for = (
            call_args[1].get("wait_for_element") if call_args[1] else call_args[0][1]
        )
        assert wait_for == "#standings"


# =========================================================================
# Lazy loading
# =========================================================================


@pytest.mark.unit
class TestLazyLoading:
    def test_superbowl_in_sub_sdk_map(self):
        assert "superbowl" in GriddyPFR._sub_sdk_map

    def test_superbowl_lazy_load(self):
        pfr = GriddyPFR()
        from griddy.pfr.endpoints.superbowl import SuperBowl

        assert isinstance(pfr.superbowl, SuperBowl)
