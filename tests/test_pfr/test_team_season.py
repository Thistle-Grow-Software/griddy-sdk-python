"""Tests for griddy.pfr.parsers.team_season and the Teams endpoint."""

import json
from unittest.mock import patch

import pytest

from griddy.pfr import GriddyPFR
from griddy.pfr.models.entities.team_season import (
    SeasonGame,
    TeamSeason,
    TeamSeasonMeta,
)
from griddy.pfr.parsers.team_season import TeamSeasonParser
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "teams"


@pytest.fixture
def parser() -> TeamSeasonParser:
    return TeamSeasonParser()


@pytest.fixture(scope="module")
def raw_html() -> str:
    html = (FIXTURE_DIR / "nwe_2015_team_season.htm").read_text()
    return html.replace('\\"', '"')


@pytest.fixture(scope="module")
def parsed_data(raw_html: str) -> dict:
    return TeamSeasonParser().parse(raw_html)


@pytest.fixture(scope="module")
def team_season(parsed_data: dict) -> TeamSeason:
    return TeamSeason.model_validate(parsed_data)


# ---------------------------------------------------------------------------
# Full parse — smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseSmoke:
    """Smoke test: fixture should parse without errors."""

    def test_parse_returns_dict(self, parsed_data):
        assert isinstance(parsed_data, dict)

    def test_parsed_data_has_all_keys(self, parsed_data):
        expected_keys = {
            "meta",
            "team_stats",
            "games",
            "team_conversions",
            "passing",
            "passing_post",
            "rushing_and_receiving",
        }
        assert set(parsed_data.keys()) == expected_keys

    def test_model_validates_successfully(self, team_season):
        assert isinstance(team_season, TeamSeason)


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseMeta:
    def test_record(self, team_season):
        assert team_season.meta.record == "12-4-0"

    def test_division(self, team_season):
        assert team_season.meta.division == "AFC East Division"

    def test_division_href(self, team_season):
        assert team_season.meta.division_href == "/years/2015"

    def test_coach(self, team_season):
        assert team_season.meta.coach == "Bill Belichick"

    def test_coach_href(self, team_season):
        assert team_season.meta.coach_href == "/coaches/BeliBi0.htm"

    def test_points_for(self, team_season):
        assert "465" in team_season.meta.points_for

    def test_points_against(self, team_season):
        assert "315" in team_season.meta.points_against

    def test_expected_wl(self, team_season):
        assert team_season.meta.expected_wl == "11.5-4.5"

    def test_srs(self, team_season):
        assert team_season.meta.srs == "6.97"

    def test_sos(self, team_season):
        assert team_season.meta.sos == "-2.41"

    def test_playoffs(self, team_season):
        assert "Kansas City Chiefs" in team_season.meta.playoffs
        assert "Denver Broncos" in team_season.meta.playoffs

    def test_offensive_coordinator(self, team_season):
        assert team_season.meta.offensive_coordinator == "Josh McDaniels"

    def test_defensive_coordinator(self, team_season):
        assert team_season.meta.defensive_coordinator == "Matt Patricia"

    def test_stadium(self, team_season):
        assert team_season.meta.stadium == "Gillette Stadium"

    def test_stadium_href(self, team_season):
        assert team_season.meta.stadium_href == "/stadiums/BOS00.htm"

    def test_offensive_scheme(self, team_season):
        assert team_season.meta.offensive_scheme == "Erhardt-Perkins"

    def test_defensive_alignment(self, team_season):
        assert team_season.meta.defensive_alignment == "4-3"

    def test_preseason_odds(self, team_season):
        assert "800" in team_season.meta.preseason_odds

    def test_training_camp(self, team_season):
        assert "Gillette Stadium" in team_season.meta.training_camp


# ---------------------------------------------------------------------------
# Team Stats table
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseTeamStats:
    def test_has_four_rows(self, team_season):
        assert len(team_season.team_stats) == 4

    def test_has_team_stats_row(self, team_season):
        assert "Team Stats" in team_season.team_stats

    def test_has_opp_stats_row(self, team_season):
        assert "Opp. Stats" in team_season.team_stats

    def test_has_lg_rank_offense_row(self, team_season):
        assert "Lg Rank Offense" in team_season.team_stats

    def test_has_lg_rank_defense_row(self, team_season):
        assert "Lg Rank Defense" in team_season.team_stats

    def test_team_stats_points(self, team_season):
        assert team_season.team_stats["Team Stats"]["points"] == 465

    def test_team_stats_total_yards(self, team_season):
        assert team_season.team_stats["Team Stats"]["total_yards"] == 5991

    def test_team_stats_pass_td(self, team_season):
        assert team_season.team_stats["Team Stats"]["pass_td"] == 36

    def test_opp_stats_points(self, team_season):
        assert team_season.team_stats["Opp. Stats"]["points"] == 315

    def test_lg_rank_offense_points(self, team_season):
        assert team_season.team_stats["Lg Rank Offense"]["points"] == 3

    def test_lg_rank_defense_points(self, team_season):
        assert team_season.team_stats["Lg Rank Defense"]["points"] == 10


# ---------------------------------------------------------------------------
# Games table
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseGames:
    def test_game_count(self, team_season):
        # 16 regular season + 1 bye + 2 playoff = 19
        assert len(team_season.games) == 19

    def test_first_game_week(self, team_season):
        assert team_season.games[0].week_num == "1"

    def test_first_game_opponent(self, team_season):
        assert team_season.games[0].opp == "Pittsburgh Steelers"

    def test_first_game_outcome(self, team_season):
        assert team_season.games[0].game_outcome == "W"

    def test_first_game_pts_off(self, team_season):
        assert team_season.games[0].pts_off == 28

    def test_first_game_pts_def(self, team_season):
        assert team_season.games[0].pts_def == 21

    def test_first_game_boxscore_href(self, team_season):
        assert team_season.games[0].boxscore_word_href == "/boxscores/201509100nwe.htm"

    def test_first_game_opp_href(self, team_season):
        assert team_season.games[0].opp_href == "/teams/pit/2015.htm"

    def test_away_game_location(self, team_season):
        # Week 2 @ Buffalo
        assert team_season.games[1].game_location == "@"

    def test_home_game_location_empty(self, team_season):
        # Week 1 home game
        assert team_season.games[0].game_location == ""

    def test_bye_week_included(self, team_season):
        bye_weeks = [g for g in team_season.games if g.opp == "Bye Week"]
        assert len(bye_weeks) == 1

    def test_bye_week_no_stats(self, team_season):
        bye = next(g for g in team_season.games if g.opp == "Bye Week")
        assert bye.pts_off is None
        assert bye.pts_def is None
        assert bye.game_outcome is None or bye.game_outcome == ""

    def test_playoff_games_present(self, team_season):
        playoff_games = [
            g for g in team_season.games if g.week_num in ("Division", "Conf. Champ.")
        ]
        assert len(playoff_games) == 2

    def test_playoff_divisional_opponent(self, team_season):
        div_game = next(g for g in team_season.games if g.week_num == "Division")
        assert div_game.opp == "Kansas City Chiefs"

    def test_expected_points(self, team_season):
        first = team_season.games[0]
        assert first.exp_pts_off is not None
        assert isinstance(first.exp_pts_off, float)

    def test_game_is_season_game_model(self, team_season):
        assert isinstance(team_season.games[0], SeasonGame)

    def test_loss_game_outcome(self, team_season):
        losses = [g for g in team_season.games if g.game_outcome == "L"]
        # 4 regular season + 1 playoff (Conf. Championship)
        assert len(losses) == 5


# ---------------------------------------------------------------------------
# Team Conversions table
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseTeamConversions:
    def test_has_four_rows(self, team_season):
        assert len(team_season.team_conversions) == 4

    def test_team_third_down_att(self, team_season):
        assert team_season.team_conversions["Team Stats"]["third_down_att"] == 215

    def test_team_third_down_pct(self, team_season):
        assert team_season.team_conversions["Team Stats"]["third_down_pct"] == "40.9%"

    def test_team_red_zone_att(self, team_season):
        assert team_season.team_conversions["Team Stats"]["red_zone_att"] == 61


# ---------------------------------------------------------------------------
# Passing table
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParsePassing:
    def test_passing_has_rows(self, team_season):
        assert len(team_season.passing) >= 1

    def test_first_passer_is_brady(self, team_season):
        assert team_season.passing[0]["name_display"] == "Tom Brady"

    def test_brady_player_id(self, team_season):
        assert team_season.passing[0]["player_id"] == "BradTo00"

    def test_brady_pass_yds(self, team_season):
        assert team_season.passing[0]["pass_yds"] == 4770

    def test_brady_pass_td(self, team_season):
        assert team_season.passing[0]["pass_td"] == 36

    def test_brady_pass_int(self, team_season):
        assert team_season.passing[0]["pass_int"] == 7

    def test_brady_games(self, team_season):
        assert team_season.passing[0]["games"] == 16

    def test_player_href(self, team_season):
        assert "BradTo00" in team_season.passing[0].get("player_href", "")


# ---------------------------------------------------------------------------
# Passing Postseason
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParsePassingPost:
    def test_passing_post_has_rows(self, team_season):
        assert len(team_season.passing_post) >= 1


# ---------------------------------------------------------------------------
# Rushing and Receiving
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseRushingAndReceiving:
    def test_rushing_receiving_has_rows(self, team_season):
        # SOC tables may only have 1 row initially
        assert len(team_season.rushing_and_receiving) >= 1


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestJsonSerialization:
    def test_serializes_to_json(self, team_season):
        output = team_season.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert loaded["meta"]["record"] == "12-4-0"

    def test_model_dump_round_trip(self, team_season):
        dumped = team_season.model_dump()
        assert dumped["meta"]["coach"] == "Bill Belichick"
        assert len(dumped["games"]) == 19


# ---------------------------------------------------------------------------
# Teams endpoint
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestTeamsEndpoint:
    def test_get_team_season_returns_model(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.teams.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            result = pfr.teams.get_team_season(team="nwe", year=2015)

        mock_fetch.assert_called_once()
        assert isinstance(result, TeamSeason)
        assert result.meta.record == "12-4-0"
        assert len(result.games) == 19

    def test_url_construction(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.teams.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.teams.get_team_season(team="nwe", year=2015)

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/teams/nwe/2015.htm"

    def test_url_construction_uppercase_team(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.teams.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.teams.get_team_season(team="NWE", year=2015)

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/teams/nwe/2015.htm"

    def test_wait_for_element(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.teams.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.teams.get_team_season(team="nwe", year=2015)

        assert mock_fetch.call_args[1]["wait_for_element"] == "#games"

    def test_lazy_loading(self):
        pfr = GriddyPFR()
        assert "teams" in pfr._sub_sdk_map
        assert pfr.teams is not None
        assert pfr.teams is pfr.teams
