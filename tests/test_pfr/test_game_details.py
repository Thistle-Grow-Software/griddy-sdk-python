"""Tests for griddy.pfr game_details endpoint and parser."""

from pathlib import Path
from unittest.mock import patch

import pytest

from griddy.pfr import GriddyPFR
from griddy.pfr.models import GameDetails
from griddy.pfr.utils.parsers import GameDetailsParser

FIXTURE_PATH = Path(__file__).resolve().parents[2] / "PFR_boxscore_201509100nwe.htm"


@pytest.fixture
def boxscore_html() -> str:
    """Load the 2015 week 1 PIT@NWE boxscore HTML fixture."""
    return FIXTURE_PATH.read_text()


@pytest.fixture
def parser() -> GameDetailsParser:
    return GameDetailsParser()


@pytest.fixture
def game_data(parser: GameDetailsParser, boxscore_html: str) -> dict:
    """Parsed game details dict for reuse across tests."""
    return parser.parse(boxscore_html)


# ------------------------------------------------------------------
# Parser unit tests
# ------------------------------------------------------------------


@pytest.mark.unit
class TestParseGameDetailsScorebox:
    def test_home_team(self, game_data: dict):
        home = game_data["scorebox"]["home"]
        assert home["name"] == "New England Patriots"
        assert home["score"] == 28
        assert home["coach"] == "Bill Belichick"

    def test_away_team(self, game_data: dict):
        away = game_data["scorebox"]["away"]
        assert away["name"] == "Pittsburgh Steelers"
        assert away["score"] == 21
        assert away["coach"] == "Mike Tomlin"

    def test_away_record(self, game_data: dict):
        assert game_data["scorebox"]["away"]["record"] == "0-1"

    def test_home_record(self, game_data: dict):
        assert game_data["scorebox"]["home"]["record"] == "1-0"

    def test_meta_date(self, game_data: dict):
        meta = game_data["scorebox"]["meta"]
        assert "Sep 10, 2015" in meta["date"]

    def test_meta_stadium(self, game_data: dict):
        meta = game_data["scorebox"]["meta"]
        assert "Gillette Stadium" in meta["Stadium"]

    def test_meta_attendance(self, game_data: dict):
        meta = game_data["scorebox"]["meta"]
        assert "66,829" in meta["Attendance"]


@pytest.mark.unit
class TestParseGameDetailsLinescore:
    def test_two_teams_in_linescore(self, game_data: dict):
        assert len(game_data["linescore"]) == 2

    def test_away_final_score(self, game_data: dict):
        away = game_data["linescore"][0]
        assert away["team"] == "Pittsburgh Steelers"
        assert away["quarters"]["Final"] == 21

    def test_home_final_score(self, game_data: dict):
        home = game_data["linescore"][1]
        assert home["team"] == "New England Patriots"
        assert home["quarters"]["Final"] == 28

    def test_quarter_scores(self, game_data: dict):
        away = game_data["linescore"][0]
        assert away["quarters"]["1"] == 0
        assert away["quarters"]["2"] == 3
        assert away["quarters"]["3"] == 8
        assert away["quarters"]["4"] == 10


@pytest.mark.unit
class TestParseGameDetailsScoring:
    def test_scoring_plays_count(self, game_data: dict):
        assert len(game_data["scoring"]) == 8

    def test_first_scoring_play(self, game_data: dict):
        first = game_data["scoring"][0]
        assert first["quarter"] == 2
        assert first["time"] == "11:11"
        assert first["team"] == "Patriots"
        assert "Gronkowski" in first["description"]
        assert first["home_team_score"] == 7


@pytest.mark.unit
class TestParseGameDetailsCommentedTables:
    """Tables that are hidden in HTML comments on PFR."""

    def test_game_info_parsed(self, game_data: dict):
        gi = game_data["game_info"]
        assert gi["Won Toss"] == "Patriots (deferred)"
        assert gi["Roof"] == "outdoors"
        assert gi["Surface"] == "fieldturf"
        assert "65 degrees" in gi["Weather"]
        assert "New England Patriots -7.0" in gi["Vegas Line"]

    def test_officials_parsed(self, game_data: dict):
        officials = game_data["officials"]
        assert officials["Referee"] == "Carl Cheffers"
        assert officials["Umpire"] == "Undrey Wash"
        assert len(officials) == 7

    def test_expected_points_parsed(self, game_data: dict):
        ep = game_data["expected_points"]
        assert len(ep) == 2
        assert ep[0]["team_name"] == "Patriots"
        assert ep[1]["team_name"] == "Steelers"

    def test_team_stats_parsed(self, game_data: dict):
        ts = game_data["team_stats"]
        assert "first_downs" in ts
        assert ts["first_downs"]["PIT"] == "23"
        assert ts["first_downs"]["NWE"] == "26"
        assert "total_yards" in ts
        assert ts["turnovers"]["PIT"] == "1"
        assert ts["turnovers"]["NWE"] == "0"

    def test_player_defense_parsed(self, game_data: dict):
        defense = game_data["player_defense"]
        assert len(defense) > 0
        # Will Allen had a sack.
        allen = next((p for p in defense if p.get("player_id") == "AlleWi21"), None)
        assert allen is not None
        assert allen["sacks"] == 1.0
        assert allen["tackles_combined"] == 8

    def test_returns_parsed(self, game_data: dict):
        returns = game_data["returns"]
        assert len(returns) > 0

    def test_kicking_parsed(self, game_data: dict):
        kicking = game_data["kicking"]
        assert len(kicking) > 0
        scobee = next(
            (p for p in kicking if p.get("player_id") == "scobejos01"),
            None,
        )
        assert scobee is not None
        assert scobee["fgm"] == 2
        assert scobee["fga"] == 4

    def test_home_starters_parsed(self, game_data: dict):
        starters = game_data["home_starters"]
        assert len(starters) == 22
        names = [s.get("player") for s in starters]
        assert "Tom Brady" in names
        assert "Rob Gronkowski" in names

    def test_vis_starters_parsed(self, game_data: dict):
        starters = game_data["vis_starters"]
        assert len(starters) == 22
        names = [s.get("player") for s in starters]
        assert "Ben Roethlisberger" in names
        assert "Antonio Brown" in names

    def test_home_snap_counts_parsed(self, game_data: dict):
        snaps = game_data["home_snap_counts"]
        assert len(snaps) > 0
        brady = next((p for p in snaps if p.get("player_id") == "BradTo00"), None)
        assert brady is not None
        assert brady["offense"] == 61
        assert brady["off_pct"] == "100%"

    def test_vis_snap_counts_parsed(self, game_data: dict):
        snaps = game_data["vis_snap_counts"]
        assert len(snaps) > 0

    def test_home_drives_parsed(self, game_data: dict):
        drives = game_data["home_drives"]
        assert len(drives) == 10
        first_drive = drives[0]
        assert first_drive["drive_num"] == 1
        assert first_drive["end_event"] == "Punt"

    def test_vis_drives_parsed(self, game_data: dict):
        drives = game_data["vis_drives"]
        assert len(drives) == 9
        last_drive = drives[-1]
        assert last_drive["end_event"] == "Touchdown"


@pytest.mark.unit
class TestParseGameDetailsPlayerOffense:
    def test_player_offense_count(self, game_data: dict):
        offense = game_data["player_offense"]
        assert len(offense) > 0

    def test_brady_passing(self, game_data: dict):
        offense = game_data["player_offense"]
        brady = next((p for p in offense if p.get("player_id") == "BradTo00"), None)
        assert brady is not None
        assert brady["pass_cmp"] == 25
        assert brady["pass_att"] == 32
        assert brady["pass_yds"] == 288
        assert brady["pass_td"] == 4
        assert brady["pass_int"] == 0
        assert brady["pass_rating"] == 143.7

    def test_williams_rushing(self, game_data: dict):
        offense = game_data["player_offense"]
        williams = next((p for p in offense if p.get("player_id") == "WillDe02"), None)
        assert williams is not None
        assert williams["rush_att"] == 21
        assert williams["rush_yds"] == 127

    def test_gronkowski_receiving(self, game_data: dict):
        offense = game_data["player_offense"]
        gronk = next((p for p in offense if p.get("player_id") == "GronRo00"), None)
        assert gronk is not None
        assert gronk["rec"] == 5
        assert gronk["rec_yds"] == 94
        assert gronk["rec_td"] == 3

    def test_player_href_extracted(self, game_data: dict):
        offense = game_data["player_offense"]
        brady = next((p for p in offense if p.get("player_id") == "BradTo00"), None)
        assert brady is not None
        assert brady["player_href"] == "/players/B/BradTo00.htm"


# ------------------------------------------------------------------
# Endpoint integration tests (with mocked browserless)
# ------------------------------------------------------------------


@pytest.mark.unit
class TestGameDetailsEndpoint:
    def test_get_game_details_returns_model(self, boxscore_html: str):
        pfr = GriddyPFR()
        with patch.object(
            pfr.games.browserless,
            "get_page_content",
            return_value=boxscore_html,
        ) as mock_fetch:
            result = pfr.games.get_game_details(game_id="201509100nwe")

        mock_fetch.assert_called_once()
        call_args = mock_fetch.call_args
        assert "201509100nwe" in call_args[0][0]
        assert call_args[1]["wait_for_element"] == "#scoring"
        assert isinstance(result, GameDetails)
        assert result.scorebox is not None
        assert len(result.scoring) > 0
        assert len(result.player_offense) > 0

    def test_url_construction(self, boxscore_html: str):
        pfr = GriddyPFR()
        with patch.object(
            pfr.games.browserless,
            "get_page_content",
            return_value=boxscore_html,
        ) as mock_fetch:
            pfr.games.get_game_details(game_id="202402110kan")

        url = mock_fetch.call_args[0][0]
        assert (
            url == "https://www.pro-football-reference.com/boxscores/202402110kan.htm"
        )

    def test_lazy_loading(self):
        pfr = GriddyPFR()
        assert "games" in pfr._sub_sdk_map
        assert pfr.games is not None
        assert pfr.games is pfr.games


@pytest.mark.unit
class TestParseGameDetailsReturnStructure:
    """Verify the top-level structure of the returned dict."""

    def test_all_expected_keys_present(self, game_data: dict):
        expected_keys = {
            "scorebox",
            "linescore",
            "scoring",
            "game_info",
            "officials",
            "expected_points",
            "team_stats",
            "player_offense",
            "player_defense",
            "returns",
            "kicking",
            "home_starters",
            "vis_starters",
            "home_snap_counts",
            "vis_snap_counts",
            "home_drives",
            "vis_drives",
        }
        assert expected_keys == set(game_data.keys())
