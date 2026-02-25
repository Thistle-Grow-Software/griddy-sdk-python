"""Tests for griddy.pfr.parsers.team_franchise and the Teams endpoint."""

import json
from unittest.mock import patch

import pytest

from griddy.pfr import GriddyPFR
from griddy.pfr.models.entities.team_franchise import (
    FranchiseLeader,
    FranchiseMeta,
    FranchiseSeasonRecord,
    TeamFranchise,
)
from griddy.pfr.parsers.team_franchise import TeamFranchiseParser
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "teams"


@pytest.fixture
def parser() -> TeamFranchiseParser:
    return TeamFranchiseParser()


@pytest.fixture(scope="module")
def raw_html() -> str:
    html = (FIXTURE_DIR / "nwe_franchise.htm").read_text()
    return html.replace('\\"', '"')


@pytest.fixture(scope="module")
def parsed_data(raw_html: str) -> dict:
    return TeamFranchiseParser().parse(raw_html)


@pytest.fixture(scope="module")
def franchise(parsed_data: dict) -> TeamFranchise:
    return TeamFranchise.model_validate(parsed_data)


# ---------------------------------------------------------------------------
# Full parse -- smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseSmoke:
    """Smoke test: fixture should parse without errors."""

    def test_parse_returns_dict(self, parsed_data):
        assert isinstance(parsed_data, dict)

    def test_parsed_data_has_all_keys(self, parsed_data):
        expected_keys = {"meta", "team_index"}
        assert set(parsed_data.keys()) == expected_keys

    def test_model_validates_successfully(self, franchise):
        assert isinstance(franchise, TeamFranchise)


# ---------------------------------------------------------------------------
# Franchise Metadata
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseMeta:
    def test_meta_is_franchise_meta(self, franchise):
        assert isinstance(franchise.meta, FranchiseMeta)

    def test_team_names(self, franchise):
        assert "Boston Patriots" in franchise.meta.team_names
        assert "New England Patriots" in franchise.meta.team_names

    def test_seasons(self, franchise):
        assert "66" in franchise.meta.seasons
        assert "1960" in franchise.meta.seasons

    def test_record(self, franchise):
        assert "559-449-9" in franchise.meta.record

    def test_playoff_record(self, franchise):
        assert "40-23" in franchise.meta.playoff_record

    def test_super_bowls_won(self, franchise):
        assert "6" in franchise.meta.super_bowls_won
        assert "12 Appearances" in franchise.meta.super_bowls_won

    def test_championships_won(self, franchise):
        assert "6" in franchise.meta.championships_won

    # -- Leaders --

    def test_passing_leader_name(self, franchise):
        assert franchise.meta.all_time_passing_leader.name == "Tom Brady"

    def test_passing_leader_href(self, franchise):
        assert "/players/B/BradTo00.htm" in franchise.meta.all_time_passing_leader.href

    def test_passing_leader_stats(self, franchise):
        stats = franchise.meta.all_time_passing_leader.stats
        assert "74,571 yds" in stats
        assert "541 TD" in stats

    def test_rushing_leader_name(self, franchise):
        assert franchise.meta.all_time_rushing_leader.name == "Sam Cunningham"

    def test_rushing_leader_stats(self, franchise):
        stats = franchise.meta.all_time_rushing_leader.stats
        assert "5,453 yds" in stats
        assert "43 TD" in stats

    def test_receiving_leader_name(self, franchise):
        assert franchise.meta.all_time_receiving_leader.name == "Stanley Morgan"

    def test_receiving_leader_stats(self, franchise):
        stats = franchise.meta.all_time_receiving_leader.stats
        assert "10,352 yds" in stats
        assert "67 TD" in stats

    def test_scoring_leader_name(self, franchise):
        assert franchise.meta.all_time_scoring_leader.name == "Stephen Gostkowski"

    def test_scoring_leader_stats(self, franchise):
        assert "1,775 points" in franchise.meta.all_time_scoring_leader.stats

    def test_av_leader_name(self, franchise):
        assert franchise.meta.all_time_av_leader.name == "Tom Brady"

    def test_av_leader_stats(self, franchise):
        assert "285 AV" in franchise.meta.all_time_av_leader.stats

    def test_winningest_coach_name(self, franchise):
        assert franchise.meta.winningest_coach.name == "Bill Belichick"

    def test_winningest_coach_href(self, franchise):
        assert "/coaches/BeliBi0.htm" in franchise.meta.winningest_coach.href

    def test_winningest_coach_stats(self, franchise):
        assert "296-133-0" in franchise.meta.winningest_coach.stats

    def test_leader_is_model(self, franchise):
        assert isinstance(franchise.meta.all_time_passing_leader, FranchiseLeader)


# ---------------------------------------------------------------------------
# Team Index table
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseTeamIndex:
    def test_season_count(self, franchise):
        # 66 seasons (1960-2025)
        assert len(franchise.team_index) == 66

    def test_first_season_year(self, franchise):
        assert franchise.team_index[0].year_id == "2025"

    def test_first_season_year_href(self, franchise):
        assert franchise.team_index[0].year_href == "/teams/nwe/2025.htm"

    def test_first_season_league(self, franchise):
        assert franchise.team_index[0].league_id == "NFL"

    def test_first_season_team_name(self, franchise):
        # Includes '*' for playoff appearance
        assert "New England Patriots" in franchise.team_index[0].team

    def test_first_season_wins(self, franchise):
        assert franchise.team_index[0].wins == 14

    def test_first_season_losses(self, franchise):
        assert franchise.team_index[0].losses == 3

    def test_first_season_ties(self, franchise):
        assert franchise.team_index[0].ties == 0

    def test_first_season_div_finish(self, franchise):
        assert franchise.team_index[0].div_finish == "1st of 4"

    def test_first_season_playoff_result(self, franchise):
        assert franchise.team_index[0].playoff_result == "Lost SB"

    def test_first_season_points(self, franchise):
        assert franchise.team_index[0].points == 490

    def test_first_season_points_opp(self, franchise):
        assert franchise.team_index[0].points_opp == 320

    def test_first_season_points_diff(self, franchise):
        assert franchise.team_index[0].points_diff == 170

    def test_first_season_coaches(self, franchise):
        assert franchise.team_index[0].coaches == "Vrabel"

    def test_first_season_coaches_href(self, franchise):
        assert "/coaches/VrabMi0.htm" in franchise.team_index[0].coaches_href

    # -- Top Players columns --

    def test_first_season_av(self, franchise):
        assert franchise.team_index[0].av == "Maye"

    def test_first_season_av_title(self, franchise):
        assert "Drake Maye" in franchise.team_index[0].av_title

    def test_first_season_passer(self, franchise):
        assert franchise.team_index[0].passer == "Maye"

    def test_first_season_passer_title(self, franchise):
        assert "4394 yds" in franchise.team_index[0].passer_title

    def test_first_season_rusher(self, franchise):
        assert franchise.team_index[0].rusher == "Henderson"

    def test_first_season_receiver(self, franchise):
        assert franchise.team_index[0].receiver == "Diggs"

    # -- Rankings --

    def test_first_season_rank_off_pts(self, franchise):
        assert franchise.team_index[0].rank_off_pts == 2

    def test_first_season_rank_off_yds(self, franchise):
        assert franchise.team_index[0].rank_off_yds == 3

    def test_first_season_rank_def_pts(self, franchise):
        assert franchise.team_index[0].rank_def_pts == 4

    def test_first_season_rank_def_yds(self, franchise):
        assert franchise.team_index[0].rank_def_yds == 8

    def test_first_season_teams_in_league(self, franchise):
        assert franchise.team_index[0].teams_in_league == 32

    # -- SRS columns --

    def test_first_season_mov(self, franchise):
        assert franchise.team_index[0].mov == 10.0

    def test_first_season_sos_total(self, franchise):
        assert franchise.team_index[0].sos_total == -4.5

    def test_first_season_srs_total(self, franchise):
        assert franchise.team_index[0].srs_total == 5.5

    def test_first_season_srs_offense(self, franchise):
        assert franchise.team_index[0].srs_offense == 3.7

    def test_first_season_srs_defense(self, franchise):
        assert franchise.team_index[0].srs_defense == 1.8

    # -- Last season (oldest) --

    def test_last_season_year(self, franchise):
        assert franchise.team_index[-1].year_id == "1960"

    def test_last_season_league(self, franchise):
        assert franchise.team_index[-1].league_id == "AFL"

    def test_last_season_team_name(self, franchise):
        assert "Boston Patriots" in franchise.team_index[-1].team

    def test_last_season_wins(self, franchise):
        assert franchise.team_index[-1].wins == 5

    def test_last_season_losses(self, franchise):
        assert franchise.team_index[-1].losses == 9

    # -- Non-playoff year --

    def test_non_playoff_year_exists(self, franchise):
        non_playoff = [r for r in franchise.team_index if not r.playoff_result]
        assert len(non_playoff) >= 30

    # -- Model type checks --

    def test_record_is_season_record_model(self, franchise):
        assert isinstance(franchise.team_index[0], FranchiseSeasonRecord)


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestJsonSerialization:
    def test_serializes_to_json(self, franchise):
        output = franchise.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert "Boston Patriots" in loaded["meta"]["team_names"]

    def test_model_dump_round_trip(self, franchise):
        dumped = franchise.model_dump()
        assert dumped["meta"]["winningest_coach"]["name"] == "Bill Belichick"
        assert len(dumped["team_index"]) == 66


# ---------------------------------------------------------------------------
# Teams endpoint (get_team_franchise)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestTeamFranchiseEndpoint:
    def test_get_team_franchise_returns_model(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.teams.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            result = pfr.teams.get_team_franchise(team="nwe")

        mock_fetch.assert_called_once()
        assert isinstance(result, TeamFranchise)
        assert "Boston Patriots" in result.meta.team_names
        assert len(result.team_index) == 66

    def test_url_construction(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.teams.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.teams.get_team_franchise(team="nwe")

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/teams/nwe/"

    def test_url_construction_uppercase_team(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.teams.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.teams.get_team_franchise(team="NWE")

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/teams/nwe/"

    def test_wait_for_element(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.teams.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.teams.get_team_franchise(team="nwe")

        assert mock_fetch.call_args[1]["wait_for_element"] == "#team_index"

    def test_lazy_loading(self):
        pfr = GriddyPFR()
        assert "teams" in pfr._sub_sdk_map
        assert pfr.teams is not None
        assert pfr.teams is pfr.teams
