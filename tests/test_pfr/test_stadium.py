"""Tests for griddy.pfr.parsers.stadium and the Stadiums endpoint."""

import json
from unittest.mock import patch

import pytest

from griddy.pfr import GriddyPFR
from griddy.pfr.models.entities.stadium import (
    StadiumBestGame,
    StadiumBio,
    StadiumGameLeader,
    StadiumGameSummary,
    StadiumLeader,
    StadiumProfile,
    StadiumTeam,
)
from griddy.pfr.parsers.stadium import StadiumParser
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "stadiums"


@pytest.fixture
def parser() -> StadiumParser:
    return StadiumParser()


@pytest.fixture(scope="module")
def raw_html() -> str:
    return (FIXTURE_DIR / "BOS00.htm").read_text()


@pytest.fixture(scope="module")
def parsed_data(raw_html: str) -> dict:
    return StadiumParser().parse(raw_html)


@pytest.fixture(scope="module")
def stadium(parsed_data: dict) -> StadiumProfile:
    return StadiumProfile.model_validate(parsed_data)


# ---------------------------------------------------------------------------
# Full parse -- smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseSmoke:
    """Smoke test: fixture should parse without errors."""

    def test_parse_returns_dict(self, parsed_data):
        assert isinstance(parsed_data, dict)

    def test_parsed_data_has_all_keys(self, parsed_data):
        expected_keys = {
            "bio",
            "leaders",
            "best_games",
            "best_playoff_games",
            "game_summaries",
        }
        assert set(parsed_data.keys()) == expected_keys

    def test_model_validates_successfully(self, stadium):
        assert isinstance(stadium, StadiumProfile)


# ---------------------------------------------------------------------------
# Stadium Bio
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseBio:
    def test_bio_is_stadium_bio(self, stadium):
        assert isinstance(stadium.bio, StadiumBio)

    def test_stadium_name(self, stadium):
        assert stadium.bio.name == "Gillette Stadium"

    def test_address(self, stadium):
        assert stadium.bio.address == "1 Patriot Place, Foxborough MA 02035"

    def test_years_active(self, stadium):
        assert stadium.bio.years_active == "2002-2025"

    def test_total_games(self, stadium):
        assert stadium.bio.total_games == 219

    def test_surfaces(self, stadium):
        assert stadium.bio.surfaces == "grass (2002-2005), fieldturf (2006-2025)"

    def test_teams_count(self, stadium):
        assert len(stadium.bio.teams) == 1

    def test_team_is_model(self, stadium):
        assert isinstance(stadium.bio.teams[0], StadiumTeam)

    def test_team_name(self, stadium):
        assert stadium.bio.teams[0].name == "New England Patriots"

    def test_team_href(self, stadium):
        assert stadium.bio.teams[0].team_href == "/teams/nwe/"

    def test_team_years(self, stadium):
        assert stadium.bio.teams[0].years == "2002-2025"

    def test_team_regular_season_record(self, stadium):
        assert stadium.bio.teams[0].regular_season_record == "143-51-0"

    def test_team_playoff_record(self, stadium):
        assert stadium.bio.teams[0].playoff_record == "21-4"


# ---------------------------------------------------------------------------
# Career Leaders (leaders table)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseLeaders:
    def test_leader_count(self, stadium):
        assert len(stadium.leaders) == 3

    def test_leader_is_model(self, stadium):
        assert isinstance(stadium.leaders[0], StadiumLeader)

    # -- Passing leader (row 0) --

    def test_passing_leader_name(self, stadium):
        assert stadium.leaders[0].player == "Tom Brady"

    def test_passing_leader_id(self, stadium):
        assert stadium.leaders[0].player_id == "BradTo00"

    def test_passing_leader_href(self, stadium):
        assert stadium.leaders[0].player_href == "/players/B/BradTo00.htm"

    def test_passing_leader_games(self, stadium):
        assert stadium.leaders[0].g == 135

    def test_passing_leader_stats(self, stadium):
        assert "35,426 yards" in stadium.leaders[0].stats
        assert "258 TD" in stadium.leaders[0].stats

    # -- Rushing leader (row 1) --

    def test_rushing_leader_name(self, stadium):
        assert stadium.leaders[1].player == "Rhamondre Stevenson"

    def test_rushing_leader_id(self, stadium):
        assert stadium.leaders[1].player_id == "StevRh00"

    def test_rushing_leader_games(self, stadium):
        assert stadium.leaders[1].g == 32

    def test_rushing_leader_stats(self, stadium):
        assert "1,713 yards" in stadium.leaders[1].stats

    # -- Receiving leader (row 2) --

    def test_receiving_leader_name(self, stadium):
        assert stadium.leaders[2].player == "Rob Gronkowski"

    def test_receiving_leader_id(self, stadium):
        assert stadium.leaders[2].player_id == "GronRo00"

    def test_receiving_leader_games(self, stadium):
        assert stadium.leaders[2].g == 59

    def test_receiving_leader_stats(self, stadium):
        assert "3,836 yards" in stadium.leaders[2].stats
        assert "41 TD" in stadium.leaders[2].stats

    # -- Type checks --

    def test_games_is_int(self, stadium):
        assert isinstance(stadium.leaders[0].g, int)


# ---------------------------------------------------------------------------
# Best Games (games table)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseBestGames:
    def test_best_game_count(self, stadium):
        assert len(stadium.best_games) == 3

    def test_best_game_is_model(self, stadium):
        assert isinstance(stadium.best_games[0], StadiumBestGame)

    # -- Best passing game (row 0) --

    def test_best_passing_player(self, stadium):
        assert stadium.best_games[0].player == "Dak Prescott"

    def test_best_passing_player_id(self, stadium):
        assert stadium.best_games[0].player_id == "PresDa01"

    def test_best_passing_team(self, stadium):
        assert stadium.best_games[0].team == "DAL"

    def test_best_passing_team_href(self, stadium):
        assert stadium.best_games[0].team_href == "/teams/dal/2021.htm"

    def test_best_passing_stats(self, stadium):
        assert "445 yards" in stadium.best_games[0].stats

    def test_best_passing_boxscore_word(self, stadium):
        assert stadium.best_games[0].boxscore_word == "Oct 17, 2021"

    def test_best_passing_boxscore_href(self, stadium):
        assert stadium.best_games[0].boxscore_href == "/boxscores/202110170nwe.htm"

    # -- Best rushing game (row 1) --

    def test_best_rushing_player(self, stadium):
        assert stadium.best_games[1].player == "Knowshon Moreno"

    def test_best_rushing_stats(self, stadium):
        assert "224 yards" in stadium.best_games[1].stats

    # -- Best receiving game (row 2) --

    def test_best_receiving_player(self, stadium):
        assert stadium.best_games[2].player == "Wes Welker"

    def test_best_receiving_stats(self, stadium):
        assert "192 yards" in stadium.best_games[2].stats


# ---------------------------------------------------------------------------
# Best Playoff Games (playoff_games table)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseBestPlayoffGames:
    def test_playoff_game_count(self, stadium):
        assert len(stadium.best_playoff_games) == 3

    def test_playoff_game_is_model(self, stadium):
        assert isinstance(stadium.best_playoff_games[0], StadiumBestGame)

    # -- Best playoff passing game (row 0) --

    def test_playoff_passing_player(self, stadium):
        assert stadium.best_playoff_games[0].player == "Tom Brady"

    def test_playoff_passing_player_id(self, stadium):
        assert stadium.best_playoff_games[0].player_id == "BradTo00"

    def test_playoff_passing_team(self, stadium):
        assert stadium.best_playoff_games[0].team == "NWE"

    def test_playoff_passing_stats(self, stadium):
        assert "384 yards" in stadium.best_playoff_games[0].stats

    def test_playoff_passing_boxscore_word(self, stadium):
        assert stadium.best_playoff_games[0].boxscore_word == "Jan 22, 2017"

    def test_playoff_passing_boxscore_href(self, stadium):
        assert (
            stadium.best_playoff_games[0].boxscore_href == "/boxscores/201701220nwe.htm"
        )

    # -- Best playoff rushing game (row 1) --

    def test_playoff_rushing_player(self, stadium):
        assert stadium.best_playoff_games[1].player == "Derrick Henry"

    def test_playoff_rushing_stats(self, stadium):
        assert "182 yards" in stadium.best_playoff_games[1].stats

    # -- Best playoff receiving game (row 2) --

    def test_playoff_receiving_player(self, stadium):
        assert stadium.best_playoff_games[2].player == "Chris Hogan"

    def test_playoff_receiving_stats(self, stadium):
        assert "180 yards" in stadium.best_playoff_games[2].stats


# ---------------------------------------------------------------------------
# Game Summaries (notable games section)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseGameSummaries:
    def test_summary_count(self, stadium):
        assert len(stadium.game_summaries) == 3

    def test_summary_is_model(self, stadium):
        assert isinstance(stadium.game_summaries[0], StadiumGameSummary)

    # -- Most recent game (summary 0, no label) --

    def test_recent_game_no_label(self, stadium):
        assert stadium.game_summaries[0].label is None

    def test_recent_game_team_1(self, stadium):
        assert stadium.game_summaries[0].team_1 == "Seattle Seahawks"

    def test_recent_game_team_1_score(self, stadium):
        assert stadium.game_summaries[0].team_1_score == 29

    def test_recent_game_team_2(self, stadium):
        assert stadium.game_summaries[0].team_2 == "New England Patriots"

    def test_recent_game_team_2_score(self, stadium):
        assert stadium.game_summaries[0].team_2_score == 13

    def test_recent_game_boxscore_href(self, stadium):
        assert stadium.game_summaries[0].boxscore_href == "/boxscores/202602080nwe.htm"

    def test_recent_game_leaders_count(self, stadium):
        assert len(stadium.game_summaries[0].leaders) == 3

    def test_recent_game_leader_is_model(self, stadium):
        assert isinstance(stadium.game_summaries[0].leaders[0], StadiumGameLeader)

    def test_recent_game_leader_stat(self, stadium):
        assert stadium.game_summaries[0].leaders[0].stat_name == "PassYds"

    def test_recent_game_leader_player(self, stadium):
        assert "Maye" in stadium.game_summaries[0].leaders[0].player

    def test_recent_game_leader_value(self, stadium):
        assert stadium.game_summaries[0].leaders[0].value == "295"

    # -- First game (summary 1) --

    def test_first_game_label(self, stadium):
        assert stadium.game_summaries[1].label == "First Game"

    def test_first_game_date(self, stadium):
        assert stadium.game_summaries[1].date == "Mon, Sep 9, 2002"

    def test_first_game_team_1(self, stadium):
        assert stadium.game_summaries[1].team_1 == "Pittsburgh Steelers"

    def test_first_game_team_1_score(self, stadium):
        assert stadium.game_summaries[1].team_1_score == 14

    def test_first_game_team_2(self, stadium):
        assert stadium.game_summaries[1].team_2 == "New England Patriots"

    def test_first_game_team_2_score(self, stadium):
        assert stadium.game_summaries[1].team_2_score == 30

    def test_first_game_boxscore_href(self, stadium):
        assert stadium.game_summaries[1].boxscore_href == "/boxscores/200209090nwe.htm"

    # -- Last game (summary 2) --

    def test_last_game_label(self, stadium):
        assert stadium.game_summaries[2].label == "Last Game"

    def test_last_game_date(self, stadium):
        assert stadium.game_summaries[2].date == "Sun, Jan 18, 2026"

    def test_last_game_team_1(self, stadium):
        assert stadium.game_summaries[2].team_1 == "Houston Texans"

    def test_last_game_team_1_score(self, stadium):
        assert stadium.game_summaries[2].team_1_score == 16

    def test_last_game_team_2(self, stadium):
        assert stadium.game_summaries[2].team_2 == "New England Patriots"

    def test_last_game_team_2_score(self, stadium):
        assert stadium.game_summaries[2].team_2_score == 28

    # -- Score type checks --

    def test_scores_are_int(self, stadium):
        for gs in stadium.game_summaries:
            if gs.team_1_score is not None:
                assert isinstance(gs.team_1_score, int)
            if gs.team_2_score is not None:
                assert isinstance(gs.team_2_score, int)


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestJsonSerialization:
    def test_serializes_to_json(self, stadium):
        output = stadium.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert loaded["bio"]["name"] == "Gillette Stadium"

    def test_model_dump_round_trip(self, stadium):
        dumped = stadium.model_dump()
        assert dumped["bio"]["name"] == "Gillette Stadium"
        assert len(dumped["leaders"]) == 3
        assert len(dumped["best_games"]) == 3
        assert len(dumped["best_playoff_games"]) == 3
        assert len(dumped["game_summaries"]) == 3


# ---------------------------------------------------------------------------
# Stadiums endpoint (get_stadium)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestStadiumsEndpoint:
    def test_get_stadium_returns_model(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.stadiums.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            result = pfr.stadiums.get_stadium(stadium_id="BOS00")

        mock_fetch.assert_called_once()
        assert isinstance(result, StadiumProfile)
        assert result.bio.name == "Gillette Stadium"
        assert len(result.leaders) == 3

    def test_url_construction(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.stadiums.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.stadiums.get_stadium(stadium_id="BOS00")

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/stadiums/BOS00.htm"

    def test_wait_for_element(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.stadiums.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.stadiums.get_stadium(stadium_id="BOS00")

        assert mock_fetch.call_args[1]["wait_for_element"] == "#leaders"

    def test_lazy_loading(self):
        pfr = GriddyPFR()
        assert "stadiums" in pfr._sub_sdk_map
        assert pfr.stadiums is not None
        assert pfr.stadiums is pfr.stadiums
