"""Tests for griddy.pfr.parsers.season_overview.parse_week and the get_week endpoint."""

import json
from unittest.mock import patch

import pytest

from griddy.pfr import GriddyPFR
from griddy.pfr.models.entities.season import (
    WeekGame,
    WeekSummary,
)
from griddy.pfr.parsers.season_overview import SeasonOverviewParser
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "seasons"


@pytest.fixture
def parser() -> SeasonOverviewParser:
    return SeasonOverviewParser()


@pytest.fixture(scope="module")
def raw_html() -> str:
    return (FIXTURE_DIR / "2024_week_1.htm").read_text()


@pytest.fixture(scope="module")
def parsed_data(raw_html: str) -> dict:
    return SeasonOverviewParser().parse_week(raw_html)


@pytest.fixture(scope="module")
def summary(parsed_data: dict) -> WeekSummary:
    return WeekSummary.model_validate(parsed_data)


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
            "games",
            "players_of_the_week",
            "top_passers",
            "top_receivers",
            "top_rushers",
            "top_defenders",
        }
        assert set(parsed_data.keys()) == expected_keys

    def test_model_validates_successfully(self, summary):
        assert isinstance(summary, WeekSummary)


# ---------------------------------------------------------------------------
# Games
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGames:
    def test_game_count(self, summary):
        assert len(summary.games) == 16

    def test_game_is_model(self, summary):
        assert isinstance(summary.games[0], WeekGame)

    # First game: BAL @ KC
    def test_first_game_date(self, summary):
        assert summary.games[0].game_date == "Sep 5, 2024"

    def test_first_game_away_team(self, summary):
        assert summary.games[0].away_team == "Baltimore Ravens"

    def test_first_game_away_team_href(self, summary):
        assert summary.games[0].away_team_href == "/teams/rav/2024.htm"

    def test_first_game_away_score(self, summary):
        assert summary.games[0].away_score == 20

    def test_first_game_home_team(self, summary):
        assert summary.games[0].home_team == "Kansas City Chiefs"

    def test_first_game_home_team_href(self, summary):
        assert summary.games[0].home_team_href == "/teams/kan/2024.htm"

    def test_first_game_home_score(self, summary):
        assert summary.games[0].home_score == 27

    def test_first_game_winner(self, summary):
        assert summary.games[0].winner == "home"

    def test_first_game_boxscore_href(self, summary):
        assert summary.games[0].boxscore_href == "/boxscores/202409050kan.htm"

    # Game leaders for first game
    def test_first_game_top_passer(self, summary):
        assert summary.games[0].top_passer == "Mahomes"

    def test_first_game_top_passer_href(self, summary):
        assert summary.games[0].top_passer_href == "/players/M/MahoPa00.htm"

    def test_first_game_top_passer_yds(self, summary):
        assert summary.games[0].top_passer_yds == "291"

    def test_first_game_top_rusher(self, summary):
        assert summary.games[0].top_rusher == "Jackson"

    def test_first_game_top_rusher_href(self, summary):
        assert summary.games[0].top_rusher_href == "/players/J/JackLa00.htm"

    def test_first_game_top_rusher_yds(self, summary):
        assert summary.games[0].top_rusher_yds == "122"

    def test_first_game_top_receiver(self, summary):
        assert summary.games[0].top_receiver == "Likely"

    def test_first_game_top_receiver_href(self, summary):
        assert summary.games[0].top_receiver_href == "/players/L/LikeIs00.htm"

    def test_first_game_top_receiver_yds(self, summary):
        assert summary.games[0].top_receiver_yds == "111"

    # Verify away winner game (PIT @ ATL: PIT won 18-10)
    def test_away_winner(self, summary):
        pit_game = summary.games[2]  # Third game
        assert pit_game.away_team == "Pittsburgh Steelers"
        assert pit_game.home_team == "Atlanta Falcons"
        assert pit_game.winner == "away"

    # Last game: NYJ @ SF
    def test_last_game_date(self, summary):
        assert summary.games[15].game_date == "Sep 9, 2024"

    def test_last_game_away_team(self, summary):
        assert summary.games[15].away_team == "New York Jets"

    def test_last_game_home_team(self, summary):
        assert summary.games[15].home_team == "San Francisco 49ers"

    def test_scores_are_ints(self, summary):
        for game in summary.games:
            if game.away_score is not None:
                assert isinstance(game.away_score, int)
            if game.home_score is not None:
                assert isinstance(game.home_score, int)


# ---------------------------------------------------------------------------
# Players of the Week
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPlayersOfTheWeek:
    def test_potw_count(self, summary):
        assert len(summary.players_of_the_week) == 2

    def test_potw_is_dict(self, summary):
        assert isinstance(summary.players_of_the_week[0], dict)

    def test_afc_conference(self, summary):
        assert summary.players_of_the_week[0]["conference_id"] == "AFC"

    def test_afc_offense(self, summary):
        assert summary.players_of_the_week[0]["offense"] == "Joe Mixon"

    def test_afc_offense_href(self, summary):
        assert (
            summary.players_of_the_week[0]["offense_href"] == "/players/M/MixoJo00.htm"
        )

    def test_afc_defense(self, summary):
        assert summary.players_of_the_week[0]["defense"] == "Gregory Rousseau"

    def test_afc_st(self, summary):
        assert summary.players_of_the_week[0]["st"] == "Chris Boswell"

    def test_nfc_conference(self, summary):
        assert summary.players_of_the_week[1]["conference_id"] == "NFC"

    def test_nfc_offense(self, summary):
        assert summary.players_of_the_week[1]["offense"] == "Saquon Barkley"


# ---------------------------------------------------------------------------
# Top Passers
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestTopPassers:
    def test_count(self, summary):
        assert len(summary.top_passers) == 5

    def test_first_player(self, summary):
        assert summary.top_passers[0]["player"] == "Baker Mayfield"

    def test_first_player_href(self, summary):
        assert summary.top_passers[0]["player_href"] == "/players/M/MayfBa00.htm"

    def test_first_game_date(self, summary):
        assert summary.top_passers[0]["game_date"] == "2024-09-08"

    def test_first_boxscore_href(self, summary):
        assert summary.top_passers[0]["boxscore_href"] == "/boxscores/202409080tam.htm"

    def test_first_team(self, summary):
        assert summary.top_passers[0]["team"] == "TAM"

    def test_first_team_href(self, summary):
        assert summary.top_passers[0]["team_href"] == "/teams/tam/2024.htm"

    def test_first_opp(self, summary):
        assert summary.top_passers[0]["opp"] == "WAS"

    def test_first_pass_yds(self, summary):
        assert summary.top_passers[0]["pass_yds"] == "289"

    def test_first_pass_td(self, summary):
        assert summary.top_passers[0]["pass_td"] == "4"

    def test_first_pass_rating(self, summary):
        assert summary.top_passers[0]["pass_rating"] == "146.4"


# ---------------------------------------------------------------------------
# Top Receivers
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestTopReceivers:
    def test_count(self, summary):
        assert len(summary.top_receivers) == 5

    def test_first_player(self, summary):
        assert summary.top_receivers[0]["player"] == "Jayden Reed"

    def test_first_rec_yds(self, summary):
        assert summary.top_receivers[0]["rec_yds"] == "138"


# ---------------------------------------------------------------------------
# Top Rushers
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestTopRushers:
    def test_count(self, summary):
        assert len(summary.top_rushers) == 5

    def test_first_player(self, summary):
        assert summary.top_rushers[0]["player"] == "Joe Mixon"

    def test_first_rush_yds(self, summary):
        assert summary.top_rushers[0]["rush_yds"] == "159"


# ---------------------------------------------------------------------------
# Top Defenders
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestTopDefenders:
    def test_count(self, summary):
        assert len(summary.top_defenders) == 5

    def test_first_player(self, summary):
        assert summary.top_defenders[0]["player"] == "Andrew Van Ginkel"

    def test_first_sacks(self, summary):
        assert summary.top_defenders[0]["sacks"] == "1.0"


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestJsonSerialization:
    def test_serializes(self, summary):
        output = summary.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert len(loaded["games"]) == 16

    def test_round_trip(self, summary):
        dumped = summary.model_dump()
        assert len(dumped["games"]) == 16
        assert len(dumped["players_of_the_week"]) == 2
        assert len(dumped["top_passers"]) == 5


# ---------------------------------------------------------------------------
# Seasons endpoint (get_week)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGetWeekEndpoint:
    def test_get_week_returns_model(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.seasons.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            result = pfr.seasons.get_week(year=2024, week=1)

        mock_fetch.assert_called_once()
        assert isinstance(result, WeekSummary)
        assert len(result.games) == 16

    def test_get_week_url_construction(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.seasons.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.seasons.get_week(year=2024, week=1)

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/years/2024/week_1.htm"

    def test_get_week_wait_for_element(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.seasons.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.seasons.get_week(year=2024, week=1)

        assert mock_fetch.call_args[1]["wait_for_element"] == "div.game_summaries"
