"""Tests for griddy.pfr.parsers.season_overview and the Seasons endpoint."""

import json
from unittest.mock import patch

import pytest

from griddy.pfr import GriddyPFR
from griddy.pfr.models.entities.season import (
    ConferenceStanding,
    PlayoffGame,
    PlayoffStanding,
    SeasonOverview,
    SeasonStats,
)
from griddy.pfr.parsers.season_overview import SeasonOverviewParser
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "seasons"


@pytest.fixture
def parser() -> SeasonOverviewParser:
    return SeasonOverviewParser()


@pytest.fixture(scope="module")
def raw_html() -> str:
    return (FIXTURE_DIR / "2024.htm").read_text()


@pytest.fixture(scope="module")
def raw_stats_html() -> str:
    return (FIXTURE_DIR / "2024_passing.htm").read_text()


@pytest.fixture(scope="module")
def parsed_data(raw_html: str) -> dict:
    return SeasonOverviewParser().parse(raw_html)


@pytest.fixture(scope="module")
def parsed_stats(raw_stats_html: str) -> dict:
    return SeasonOverviewParser().parse_stats(raw_stats_html)


@pytest.fixture(scope="module")
def season(parsed_data: dict) -> SeasonOverview:
    return SeasonOverview.model_validate(parsed_data)


@pytest.fixture(scope="module")
def stats(parsed_stats: dict) -> SeasonStats:
    return SeasonStats.model_validate(parsed_stats)


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
            "afc_standings",
            "nfc_standings",
            "playoff_results",
            "afc_playoff_standings",
            "nfc_playoff_standings",
            "team_stats",
            "passing",
            "rushing",
            "returns",
            "kicking",
            "punting",
            "team_scoring",
            "team_conversions",
            "drives",
        }
        assert set(parsed_data.keys()) == expected_keys

    def test_model_validates_successfully(self, season):
        assert isinstance(season, SeasonOverview)


# ---------------------------------------------------------------------------
# AFC Standings
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAFCStandings:
    def test_afc_count(self, season):
        assert len(season.afc_standings) == 16

    def test_afc_entry_is_model(self, season):
        assert isinstance(season.afc_standings[0], ConferenceStanding)

    def test_first_team_division(self, season):
        assert season.afc_standings[0].division == "AFC East"

    def test_first_team_name(self, season):
        assert season.afc_standings[0].team == "Buffalo Bills*"

    def test_first_team_href(self, season):
        assert season.afc_standings[0].team_href == "/teams/buf/2024.htm"

    def test_first_team_wins(self, season):
        assert season.afc_standings[0].wins == 13

    def test_first_team_losses(self, season):
        assert season.afc_standings[0].losses == 4

    def test_first_team_win_loss_perc(self, season):
        assert season.afc_standings[0].win_loss_perc == ".765"

    def test_first_team_points(self, season):
        assert season.afc_standings[0].points == 525

    def test_first_team_points_opp(self, season):
        assert season.afc_standings[0].points_opp == 368

    def test_first_team_points_diff(self, season):
        assert season.afc_standings[0].points_diff == 157

    def test_first_team_mov(self, season):
        assert season.afc_standings[0].mov == "9.2"

    def test_first_team_srs_total(self, season):
        assert season.afc_standings[0].srs_total == "8.1"

    # Verify division transitions
    def test_afc_north_division(self, season):
        # AFC East has 4 teams (index 0-3), so index 4 is first AFC North
        assert season.afc_standings[4].division == "AFC North"

    def test_wins_are_int(self, season):
        for standing in season.afc_standings:
            if standing.wins is not None:
                assert isinstance(standing.wins, int)


# ---------------------------------------------------------------------------
# NFC Standings
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestNFCStandings:
    def test_nfc_count(self, season):
        assert len(season.nfc_standings) == 16

    def test_nfc_entry_is_model(self, season):
        assert isinstance(season.nfc_standings[0], ConferenceStanding)

    def test_first_nfc_division(self, season):
        assert season.nfc_standings[0].division == "NFC East"

    def test_first_nfc_team(self, season):
        assert "Eagles" in season.nfc_standings[0].team


# ---------------------------------------------------------------------------
# Playoff Results
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPlayoffResults:
    def test_playoff_count(self, season):
        assert len(season.playoff_results) == 13

    def test_playoff_entry_is_model(self, season):
        assert isinstance(season.playoff_results[0], PlayoffGame)

    def test_first_game_week(self, season):
        assert season.playoff_results[0].week_num == "WildCard"

    def test_first_game_day(self, season):
        assert season.playoff_results[0].game_day_of_week == "Sat"

    def test_first_game_date(self, season):
        assert season.playoff_results[0].game_date == "2025-01-11"

    def test_first_game_winner(self, season):
        assert season.playoff_results[0].winner == "Houston Texans"

    def test_first_game_winner_href(self, season):
        assert season.playoff_results[0].winner_href == "/teams/htx/2024.htm"

    def test_first_game_loser(self, season):
        assert season.playoff_results[0].loser == "Los Angeles Chargers"

    def test_first_game_loser_href(self, season):
        assert season.playoff_results[0].loser_href == "/teams/sdg/2024.htm"

    def test_first_game_pts_win(self, season):
        assert season.playoff_results[0].pts_win == 32

    def test_first_game_pts_lose(self, season):
        assert season.playoff_results[0].pts_lose == 12

    def test_first_game_boxscore_href(self, season):
        assert season.playoff_results[0].boxscore_href == "/boxscores/202501110htx.htm"

    def test_pts_win_is_int(self, season):
        for game in season.playoff_results:
            if game.pts_win is not None:
                assert isinstance(game.pts_win, int)


# ---------------------------------------------------------------------------
# Playoff Standings
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPlayoffStandings:
    def test_afc_playoff_count(self, season):
        assert len(season.afc_playoff_standings) == 16

    def test_nfc_playoff_count(self, season):
        assert len(season.nfc_playoff_standings) == 16

    def test_afc_playoff_entry_is_model(self, season):
        assert isinstance(season.afc_playoff_standings[0], PlayoffStanding)

    def test_afc_first_team(self, season):
        assert "Kansas City Chiefs" in season.afc_playoff_standings[0].team

    def test_afc_first_wins(self, season):
        assert season.afc_playoff_standings[0].wins == 15

    def test_afc_first_losses(self, season):
        assert season.afc_playoff_standings[0].losses == 2

    def test_afc_first_ties(self, season):
        assert season.afc_playoff_standings[0].ties == 0

    def test_afc_first_why(self, season):
        assert season.afc_playoff_standings[0].why == "West Champion"


# ---------------------------------------------------------------------------
# Team Stats Tables (generic dicts)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestTeamStats:
    def test_team_stats_count(self, season):
        assert len(season.team_stats) == 32

    def test_team_stats_is_dict(self, season):
        assert isinstance(season.team_stats[0], dict)

    def test_team_stats_first_team(self, season):
        assert season.team_stats[0]["team"] == "Detroit Lions"

    def test_team_stats_first_team_href(self, season):
        assert season.team_stats[0]["team_href"] == "/teams/det/2024.htm"

    def test_team_stats_first_points(self, season):
        assert season.team_stats[0]["points"] == "564"

    def test_team_stats_first_total_yards(self, season):
        assert season.team_stats[0]["total_yards"] == "6962"

    def test_passing_count(self, season):
        assert len(season.passing) == 32

    def test_rushing_count(self, season):
        assert len(season.rushing) == 32

    def test_returns_count(self, season):
        assert len(season.returns) == 32

    def test_kicking_count(self, season):
        assert len(season.kicking) == 32

    def test_punting_count(self, season):
        assert len(season.punting) == 32

    def test_team_scoring_count(self, season):
        assert len(season.team_scoring) == 32

    def test_team_conversions_count(self, season):
        assert len(season.team_conversions) == 32

    def test_drives_count(self, season):
        assert len(season.drives) == 32

    def test_no_ranker_column(self, season):
        """The ranker column should be excluded from generic table output."""
        for row in season.team_stats:
            assert "ranker" not in row


# ---------------------------------------------------------------------------
# Stat category page -- smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestStatsSmoke:
    def test_parse_stats_returns_dict(self, parsed_stats):
        assert isinstance(parsed_stats, dict)

    def test_stats_has_keys(self, parsed_stats):
        assert set(parsed_stats.keys()) == {"regular_season", "postseason"}

    def test_stats_model_validates(self, stats):
        assert isinstance(stats, SeasonStats)


# ---------------------------------------------------------------------------
# Stat category page -- regular season
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestStatsRegularSeason:
    def test_regular_season_count(self, stats):
        assert len(stats.regular_season) == 112

    def test_first_player_name(self, stats):
        assert stats.regular_season[0]["name_display"] == "Joe Burrow"

    def test_first_player_id(self, stats):
        assert stats.regular_season[0]["player_id"] == "BurrJo01"

    def test_first_player_href(self, stats):
        assert stats.regular_season[0]["player_href"] == "/players/B/BurrJo01.htm"

    def test_first_player_team(self, stats):
        assert stats.regular_season[0]["team_name_abbr"] == "CIN"

    def test_first_player_team_href(self, stats):
        assert stats.regular_season[0]["team_href"] == "/teams/cin/2024.htm"

    def test_first_player_pass_yds(self, stats):
        assert stats.regular_season[0]["pass_yds"] == "4918"

    def test_first_player_pass_td(self, stats):
        assert stats.regular_season[0]["pass_td"] == "43"

    def test_first_player_pass_rating(self, stats):
        assert stats.regular_season[0]["pass_rating"] == "108.5"

    def test_first_player_games(self, stats):
        assert stats.regular_season[0]["games"] == "17"

    def test_partial_row_flagged(self, stats):
        """Multi-team player rows should have is_partial=True."""
        partial_rows = [r for r in stats.regular_season if r.get("is_partial")]
        assert len(partial_rows) == 2

    def test_league_average_row(self, stats):
        """The League Average row should be included (no player_id)."""
        avg_rows = [
            r for r in stats.regular_season if r.get("name_display") == "League Average"
        ]
        assert len(avg_rows) == 1
        assert "player_id" not in avg_rows[0]


# ---------------------------------------------------------------------------
# Stat category page -- postseason
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestStatsPostseason:
    def test_postseason_count(self, stats):
        assert len(stats.postseason) == 22

    def test_first_postseason_player(self, stats):
        assert stats.postseason[0]["name_display"] == "Jayden Daniels"

    def test_first_postseason_player_id(self, stats):
        assert stats.postseason[0]["player_id"] == "DaniJa02"

    def test_first_postseason_pass_yds(self, stats):
        assert stats.postseason[0]["pass_yds"] == "822"


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestJsonSerialization:
    def test_overview_serializes(self, season):
        output = season.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert len(loaded["afc_standings"]) == 16

    def test_overview_round_trip(self, season):
        dumped = season.model_dump()
        assert len(dumped["afc_standings"]) == 16
        assert len(dumped["playoff_results"]) == 13
        assert len(dumped["team_stats"]) == 32

    def test_stats_serializes(self, stats):
        output = stats.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert len(loaded["regular_season"]) == 112

    def test_stats_round_trip(self, stats):
        dumped = stats.model_dump()
        assert len(dumped["regular_season"]) == 112
        assert len(dumped["postseason"]) == 22


# ---------------------------------------------------------------------------
# Seasons endpoint (get_season)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSeasonsEndpoint:
    def test_get_season_returns_model(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.seasons.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            result = pfr.seasons.get_season(year=2024)

        mock_fetch.assert_called_once()
        assert isinstance(result, SeasonOverview)
        assert len(result.afc_standings) == 16

    def test_get_season_url_construction(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.seasons.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.seasons.get_season(year=2024)

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/years/2024/"

    def test_get_season_wait_for_element(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.seasons.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.seasons.get_season(year=2024)

        assert mock_fetch.call_args[1]["wait_for_element"] == "#AFC"

    def test_get_season_stats_returns_model(self, raw_stats_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.seasons.browserless,
            "get_page_content",
            return_value=raw_stats_html,
        ) as mock_fetch:
            result = pfr.seasons.get_season_stats(year=2024, category="passing")

        mock_fetch.assert_called_once()
        assert isinstance(result, SeasonStats)
        assert len(result.regular_season) == 112

    def test_get_season_stats_url_construction(self, raw_stats_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.seasons.browserless,
            "get_page_content",
            return_value=raw_stats_html,
        ) as mock_fetch:
            pfr.seasons.get_season_stats(year=2024, category="passing")

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/years/2024/passing.htm"

    def test_lazy_loading(self):
        pfr = GriddyPFR()
        assert "seasons" in pfr._sub_sdk_map
        assert pfr.seasons is not None
        assert pfr.seasons is pfr.seasons
