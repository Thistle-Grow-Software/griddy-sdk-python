"""Tests for griddy.pfr.parsers.official_profile and the Officials endpoint."""

import json
from unittest.mock import patch

import pytest

from griddy.pfr import GriddyPFR
from griddy.pfr.models.entities.official_profile import (
    OfficialBio,
    OfficialGame,
    OfficialProfile,
    OfficialSeasonStat,
)
from griddy.pfr.parsers.official_profile import OfficialProfileParser
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "officials"


@pytest.fixture
def parser() -> OfficialProfileParser:
    return OfficialProfileParser()


@pytest.fixture(scope="module")
def raw_html() -> str:
    return (FIXTURE_DIR / "ChefCa0r.htm").read_text()


@pytest.fixture(scope="module")
def parsed_data(raw_html: str) -> dict:
    return OfficialProfileParser().parse(raw_html)


@pytest.fixture(scope="module")
def official(parsed_data: dict) -> OfficialProfile:
    return OfficialProfile.model_validate(parsed_data)


# ---------------------------------------------------------------------------
# Full parse -- smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseSmoke:
    """Smoke test: fixture should parse without errors."""

    def test_parse_returns_dict(self, parsed_data):
        assert isinstance(parsed_data, dict)

    def test_parsed_data_has_all_keys(self, parsed_data):
        expected_keys = {"bio", "official_stats", "games"}
        assert set(parsed_data.keys()) == expected_keys

    def test_model_validates_successfully(self, official):
        assert isinstance(official, OfficialProfile)


# ---------------------------------------------------------------------------
# Official Bio
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseBio:
    def test_bio_is_official_bio(self, official):
        assert isinstance(official.bio, OfficialBio)

    def test_display_name(self, official):
        assert official.bio.name == "Carl Cheffers"

    def test_position(self, official):
        assert official.bio.position == "Referee, Side Judge"


# ---------------------------------------------------------------------------
# Official Stats (season totals)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseOfficialStats:
    def test_season_count(self, official):
        assert len(official.official_stats) == 26

    def test_record_is_model(self, official):
        assert isinstance(official.official_stats[0], OfficialSeasonStat)

    # -- First season (2000) --

    def test_first_season_year(self, official):
        assert official.official_stats[0].year == "2000"

    def test_first_season_games(self, official):
        assert official.official_stats[0].g == 15

    def test_first_season_playoffs(self, official):
        assert official.official_stats[0].g_playoffs == 0

    def test_first_season_pos(self, official):
        assert official.official_stats[0].pos == "Side Judge"

    def test_first_season_home(self, official):
        assert official.official_stats[0].home == 72

    def test_first_season_visitor(self, official):
        assert official.official_stats[0].visitor == 91

    def test_first_season_home_pct(self, official):
        assert official.official_stats[0].home_pct == pytest.approx(44.17, abs=0.01)

    def test_first_season_home_wpct(self, official):
        assert official.official_stats[0].home_wpct == pytest.approx(53.33, abs=0.01)

    def test_first_season_pen_total(self, official):
        assert official.official_stats[0].pen_total == 163

    def test_first_season_pen_yds(self, official):
        assert official.official_stats[0].pen_yds == 1288

    def test_first_season_pen_per_g(self, official):
        assert official.official_stats[0].pen_per_g == pytest.approx(10.87, abs=0.01)

    def test_first_season_pen_yds_per_g(self, official):
        assert official.official_stats[0].pen_yds_per_g == pytest.approx(
            85.87, abs=0.01
        )

    def test_first_season_lg_home_pct(self, official):
        assert official.official_stats[0].lg_home_pct == pytest.approx(49.59, abs=0.01)

    def test_first_season_lg_pen_per_g(self, official):
        assert official.official_stats[0].lg_pen_per_g == pytest.approx(12.62, abs=0.01)

    def test_first_season_rel_home_pct(self, official):
        assert official.official_stats[0].rel_home_pct == pytest.approx(-5.42, abs=0.01)

    def test_first_season_rel_pen_per_g(self, official):
        assert official.official_stats[0].rel_pen_per_g == pytest.approx(
            -1.75, abs=0.01
        )

    # -- Last season (2025) --

    def test_last_season_year(self, official):
        assert official.official_stats[-1].year == "2025"

    def test_last_season_games(self, official):
        assert official.official_stats[-1].g == 17

    def test_last_season_playoffs(self, official):
        assert official.official_stats[-1].g_playoffs == 1

    def test_last_season_pos(self, official):
        assert official.official_stats[-1].pos == "Referee"

    def test_last_season_pen_total(self, official):
        assert official.official_stats[-1].pen_total == 242

    def test_last_season_rel_pen_per_g_positive(self, official):
        """Relative stats can be positive (with '+' prefix in HTML)."""
        assert official.official_stats[-1].rel_pen_per_g == pytest.approx(
            1.73, abs=0.01
        )

    # -- Type checks --

    def test_int_fields_are_int(self, official):
        stat = official.official_stats[0]
        assert isinstance(stat.g, int)
        assert isinstance(stat.pen_total, int)

    def test_float_fields_are_float(self, official):
        stat = official.official_stats[0]
        assert isinstance(stat.home_pct, float)
        assert isinstance(stat.pen_per_g, float)
        assert isinstance(stat.rel_home_pct, float)


# ---------------------------------------------------------------------------
# Games (individual game log)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseGames:
    def test_game_count(self, official):
        assert len(official.games) == 413

    def test_game_is_model(self, official):
        assert isinstance(official.games[0], OfficialGame)

    # -- First game --

    def test_first_game_date(self, official):
        assert official.games[0].game_date == "September 3, 2000"

    def test_first_game_date_href(self, official):
        assert official.games[0].game_date_href == "/boxscores/200009030kan.htm"

    def test_first_game_team(self, official):
        assert official.games[0].team == "Kansas City Chiefs"

    def test_first_game_team_href(self, official):
        assert official.games[0].team_href == "/teams/kan/2000.htm"

    def test_first_game_opp(self, official):
        assert official.games[0].opp == "Indianapolis Colts"

    def test_first_game_opp_href(self, official):
        assert official.games[0].opp_href == "/teams/clt/2000.htm"

    def test_first_game_pos(self, official):
        assert official.games[0].pos == "Side Judge"

    def test_first_game_points_opp(self, official):
        assert official.games[0].points_opp == 27

    def test_first_game_penalties_opp(self, official):
        assert official.games[0].penalties_opp == 7

    def test_first_game_penalties_yds_opp(self, official):
        assert official.games[0].penalties_yds_opp == 78

    def test_first_game_points(self, official):
        assert official.games[0].points == 14

    def test_first_game_penalties(self, official):
        assert official.games[0].penalties == 6

    def test_first_game_penalties_yds(self, official):
        assert official.games[0].penalties_yds == 50

    # -- Last game --

    def test_last_game_date(self, official):
        assert official.games[-1].game_date == "January 17, 2026"

    def test_last_game_date_href(self, official):
        assert official.games[-1].game_date_href == "/boxscores/202601170den.htm"

    def test_last_game_team(self, official):
        assert official.games[-1].team == "Denver Broncos"

    def test_last_game_opp(self, official):
        assert official.games[-1].opp == "Buffalo Bills"

    def test_last_game_pos(self, official):
        assert official.games[-1].pos == "Referee"

    # -- Type checks --

    def test_int_fields_are_int(self, official):
        game = official.games[0]
        assert isinstance(game.points, int)
        assert isinstance(game.penalties, int)
        assert isinstance(game.penalties_yds, int)


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestJsonSerialization:
    def test_serializes_to_json(self, official):
        output = official.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert loaded["bio"]["name"] == "Carl Cheffers"

    def test_model_dump_round_trip(self, official):
        dumped = official.model_dump()
        assert dumped["bio"]["position"] == "Referee, Side Judge"
        assert len(dumped["official_stats"]) == 26
        assert len(dumped["games"]) == 413


# ---------------------------------------------------------------------------
# Officials endpoint (get_official_profile)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestOfficialsEndpoint:
    def test_get_official_profile_returns_model(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.officials.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            result = pfr.officials.get_official_profile(official_id="ChefCa0r")

        mock_fetch.assert_called_once()
        assert isinstance(result, OfficialProfile)
        assert result.bio.name == "Carl Cheffers"
        assert len(result.official_stats) == 26

    def test_url_construction(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.officials.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.officials.get_official_profile(official_id="ChefCa0r")

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/officials/ChefCa0r.htm"

    def test_wait_for_element(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.officials.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.officials.get_official_profile(official_id="ChefCa0r")

        assert mock_fetch.call_args[1]["wait_for_element"] == "#official_stats"

    def test_lazy_loading(self):
        pfr = GriddyPFR()
        assert "officials" in pfr._sub_sdk_map
        assert pfr.officials is not None
        assert pfr.officials is pfr.officials
