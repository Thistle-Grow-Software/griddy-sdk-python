"""Tests for griddy.pfr.parsers.coach_profile and the Coaches endpoint."""

import json
from unittest.mock import patch

import pytest

from griddy.pfr import GriddyPFR
from griddy.pfr.models.entities.coach_profile import (
    ChallengeResult,
    CoachBio,
    CoachingHistoryEntry,
    CoachingRank,
    CoachingResult,
    CoachingResultTotal,
    CoachingTreeEntry,
    CoachProfile,
)
from griddy.pfr.parsers.coach_profile import CoachProfileParser
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "coaches"


@pytest.fixture
def parser() -> CoachProfileParser:
    return CoachProfileParser()


@pytest.fixture(scope="module")
def raw_html() -> str:
    return (FIXTURE_DIR / "BeliBi0.htm").read_text()


@pytest.fixture(scope="module")
def parsed_data(raw_html: str) -> dict:
    return CoachProfileParser().parse(raw_html)


@pytest.fixture(scope="module")
def coach(parsed_data: dict) -> CoachProfile:
    return CoachProfile.model_validate(parsed_data)


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
            "coaching_results",
            "coaching_results_totals",
            "coaching_ranks",
            "coaching_history",
            "challenge_results",
            "worked_for",
            "employed",
        }
        assert set(parsed_data.keys()) == expected_keys

    def test_model_validates_successfully(self, coach):
        assert isinstance(coach, CoachProfile)


# ---------------------------------------------------------------------------
# Coach Bio
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseBio:
    def test_bio_is_coach_bio(self, coach):
        assert isinstance(coach.bio, CoachBio)

    def test_display_name(self, coach):
        assert coach.bio.name == "Bill Belichick"

    def test_full_name(self, coach):
        assert coach.bio.full_name == "William Stephen Belichick"

    def test_nicknames(self, coach):
        assert "The Hoodie" in coach.bio.nicknames
        assert "Doom" in coach.bio.nicknames
        assert "Captain Sominex" in coach.bio.nicknames
        assert "Billy" in coach.bio.nicknames

    def test_photo_url(self, coach):
        assert "BeliBi0" in coach.bio.photo_url

    def test_birth_date(self, coach):
        assert coach.bio.birth_date == "1952-04-16"

    def test_birth_city(self, coach):
        assert coach.bio.birth_city == "Nashville"

    def test_birth_state(self, coach):
        assert coach.bio.birth_state == "TN"

    def test_college(self, coach):
        assert coach.bio.college == "Wesleyan"

    def test_college_href(self, coach):
        assert coach.bio.college_href == "/schools/wesleyan/"

    def test_college_coaching_href(self, coach):
        assert "sports-reference.com" in coach.bio.college_coaching_href

    def test_high_schools(self, coach):
        assert "Annapolis" in coach.bio.high_schools
        assert "Phillips Andover Academy" in coach.bio.high_schools

    def test_as_exec(self, coach):
        assert "28 Yrs" in coach.bio.as_exec

    def test_as_exec_href(self, coach):
        assert "/executives/BeliBi0.htm" in coach.bio.as_exec_href

    def test_relatives(self, coach):
        assert "Steve Belichick" in coach.bio.relatives

    def test_relatives_href(self, coach):
        assert "/players/B/BeliSt20.htm" in coach.bio.relatives_href


# ---------------------------------------------------------------------------
# Coaching Results (year-by-year record)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseCoachingResults:
    def test_season_count(self, coach):
        assert len(coach.coaching_results) == 29

    def test_record_is_model(self, coach):
        assert isinstance(coach.coaching_results[0], CoachingResult)

    # -- First season (1991, Cleveland) --

    def test_first_season_year(self, coach):
        assert coach.coaching_results[0].year_id == "1991"

    def test_first_season_year_href(self, coach):
        assert coach.coaching_results[0].year_href == "/years/1991/"

    def test_first_season_age(self, coach):
        assert coach.coaching_results[0].age == 39

    def test_first_season_team(self, coach):
        assert coach.coaching_results[0].team == "CLE"

    def test_first_season_team_href(self, coach):
        assert coach.coaching_results[0].team_href == "/teams/cle/1991.htm"

    def test_first_season_league(self, coach):
        assert coach.coaching_results[0].league_id == "NFL"

    def test_first_season_games(self, coach):
        assert coach.coaching_results[0].g == 16

    def test_first_season_g_href(self, coach):
        assert "/teams/cle/1991_games.htm" in coach.coaching_results[0].g_href

    def test_first_season_wins(self, coach):
        assert coach.coaching_results[0].wins == 6

    def test_first_season_losses(self, coach):
        assert coach.coaching_results[0].losses == 10

    def test_first_season_ties(self, coach):
        assert coach.coaching_results[0].ties == 0

    def test_first_season_win_loss_perc(self, coach):
        assert coach.coaching_results[0].win_loss_perc == ".375"

    def test_first_season_srs_total(self, coach):
        assert coach.coaching_results[0].srs_total == -0.4

    def test_first_season_srs_offense(self, coach):
        assert coach.coaching_results[0].srs_offense == -0.7

    def test_first_season_srs_defense(self, coach):
        assert coach.coaching_results[0].srs_defense == 0.4

    def test_first_season_no_playoffs(self, coach):
        assert coach.coaching_results[0].g_playoffs is None

    def test_first_season_rank_team(self, coach):
        assert coach.coaching_results[0].rank_team == 3

    # -- Last season (2023, NWE) --

    def test_last_season_year(self, coach):
        assert coach.coaching_results[-1].year_id == "2023"

    def test_last_season_team(self, coach):
        assert coach.coaching_results[-1].team == "NWE"

    def test_last_season_wins(self, coach):
        assert coach.coaching_results[-1].wins == 4

    def test_last_season_losses(self, coach):
        assert coach.coaching_results[-1].losses == 13

    # -- Playoff season --

    def test_playoff_season_exists(self, coach):
        playoff_seasons = [
            r for r in coach.coaching_results if r.g_playoffs and r.g_playoffs > 0
        ]
        assert len(playoff_seasons) >= 10


# ---------------------------------------------------------------------------
# Coaching Results Totals (footer rows)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseCoachingResultsTotals:
    def test_total_count(self, coach):
        assert len(coach.coaching_results_totals) == 3

    def test_total_is_model(self, coach):
        assert isinstance(coach.coaching_results_totals[0], CoachingResultTotal)

    def test_career_total_label(self, coach):
        assert coach.coaching_results_totals[0].label == "29 yrs"

    def test_career_total_wins(self, coach):
        assert coach.coaching_results_totals[0].wins == 302

    def test_career_total_losses(self, coach):
        assert coach.coaching_results_totals[0].losses == 165

    def test_career_total_ties(self, coach):
        assert coach.coaching_results_totals[0].ties == 0

    def test_career_total_win_loss_perc(self, coach):
        assert coach.coaching_results_totals[0].win_loss_perc == ".647"

    def test_career_playoff_wins(self, coach):
        assert coach.coaching_results_totals[0].wins_playoffs == 31

    def test_career_playoff_losses(self, coach):
        assert coach.coaching_results_totals[0].losses_playoffs == 13

    def test_nwe_total_label(self, coach):
        assert coach.coaching_results_totals[1].label == "24 yrs"

    def test_nwe_total_team(self, coach):
        assert coach.coaching_results_totals[1].team == "NWE"

    def test_nwe_total_wins(self, coach):
        assert coach.coaching_results_totals[1].wins == 266

    def test_cle_total_label(self, coach):
        assert coach.coaching_results_totals[2].label == "5 yrs"

    def test_cle_total_team(self, coach):
        assert coach.coaching_results_totals[2].team == "CLE"

    def test_cle_total_wins(self, coach):
        assert coach.coaching_results_totals[2].wins == 36


# ---------------------------------------------------------------------------
# Coaching Ranks
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseCoachingRanks:
    def test_rank_count(self, coach):
        assert len(coach.coaching_ranks) == 38

    def test_rank_is_model(self, coach):
        assert isinstance(coach.coaching_ranks[0], CoachingRank)

    def test_first_rank_year(self, coach):
        assert coach.coaching_ranks[0].year_id == "1985"

    def test_first_rank_team(self, coach):
        assert coach.coaching_ranks[0].team == "NYG"

    def test_first_rank_coordinator_type(self, coach):
        assert coach.coaching_ranks[0].coordinator_type == "DC"

    def test_hc_year_exists(self, coach):
        hc_years = [r for r in coach.coaching_ranks if r.coordinator_type == "HC"]
        assert len(hc_years) >= 29

    def test_rank_fields_are_int_or_none(self, coach):
        rank = coach.coaching_ranks[-1]
        if rank.rank_off_pts is not None:
            assert isinstance(rank.rank_off_pts, int)
        if rank.rank_def_pts is not None:
            assert isinstance(rank.rank_def_pts, int)


# ---------------------------------------------------------------------------
# Coaching History
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseCoachingHistory:
    def test_history_count(self, coach):
        assert len(coach.coaching_history) == 50

    def test_history_is_model(self, coach):
        assert isinstance(coach.coaching_history[0], CoachingHistoryEntry)

    def test_first_entry_year(self, coach):
        assert coach.coaching_history[0].year_id == "1975"

    def test_first_entry_age(self, coach):
        assert coach.coaching_history[0].coach_age == 23

    def test_first_entry_level(self, coach):
        assert coach.coaching_history[0].coach_level == "NFL"

    def test_first_entry_employer(self, coach):
        assert "Baltimore Colts" in coach.coaching_history[0].coach_employer

    def test_first_entry_employer_href(self, coach):
        assert "/teams/clt/1975.htm" in coach.coaching_history[0].coach_employer_href

    def test_first_entry_role(self, coach):
        assert coach.coaching_history[0].coach_role == "Special Assistant"

    def test_last_entry_year(self, coach):
        assert coach.coaching_history[-1].year_id == "2025"

    def test_last_entry_level(self, coach):
        assert "College" in coach.coaching_history[-1].coach_level

    def test_last_entry_employer(self, coach):
        assert "North Carolina" in coach.coaching_history[-1].coach_employer

    def test_last_entry_role(self, coach):
        assert coach.coaching_history[-1].coach_role == "Head Coach"


# ---------------------------------------------------------------------------
# Challenge Results
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseChallengeResults:
    def test_challenge_count(self, coach):
        assert len(coach.challenge_results) == 6

    def test_challenge_is_model(self, coach):
        assert isinstance(coach.challenge_results[0], ChallengeResult)

    def test_first_challenge_has_date(self, coach):
        assert coach.challenge_results[0].game_date is not None

    def test_first_challenge_has_ruling(self, coach):
        assert coach.challenge_results[0].challenge_ruling is not None


# ---------------------------------------------------------------------------
# Coaching Tree (worked_for / employed)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseCoachingTree:
    def test_worked_for_count(self, coach):
        assert len(coach.worked_for) == 6

    def test_worked_for_is_model(self, coach):
        assert isinstance(coach.worked_for[0], CoachingTreeEntry)

    def test_worked_for_first_name(self, coach):
        assert coach.worked_for[0].coach_name == "Rick Forzano"

    def test_worked_for_first_href(self, coach):
        assert "/coaches/ForzRi0.htm" in coach.worked_for[0].coach_href

    def test_worked_for_parcells(self, coach):
        parcells = [w for w in coach.worked_for if "Parcells" in w.coach_name]
        assert len(parcells) == 1
        assert "Defensive Coordinator" in parcells[0].roles

    def test_employed_count(self, coach):
        assert len(coach.employed) == 16

    def test_employed_is_model(self, coach):
        assert isinstance(coach.employed[0], CoachingTreeEntry)

    def test_employed_first_has_href(self, coach):
        assert coach.employed[0].coach_href is not None

    def test_employed_crennel(self, coach):
        crennel = [e for e in coach.employed if "Crennel" in e.coach_name]
        assert len(crennel) == 1
        assert "Defensive Coordinator" in crennel[0].roles

    def test_employed_daboll(self, coach):
        daboll = [e for e in coach.employed if "Daboll" in e.coach_name]
        assert len(daboll) == 1


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestJsonSerialization:
    def test_serializes_to_json(self, coach):
        output = coach.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert loaded["bio"]["name"] == "Bill Belichick"

    def test_model_dump_round_trip(self, coach):
        dumped = coach.model_dump()
        assert dumped["bio"]["full_name"] == "William Stephen Belichick"
        assert len(dumped["coaching_results"]) == 29
        assert len(dumped["coaching_history"]) == 50


# ---------------------------------------------------------------------------
# Coaches endpoint (get_coach_profile)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCoachesEndpoint:
    def test_get_coach_profile_returns_model(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.coaches.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            result = pfr.coaches.get_coach_profile(coach_id="BeliBi0")

        mock_fetch.assert_called_once()
        assert isinstance(result, CoachProfile)
        assert result.bio.name == "Bill Belichick"
        assert len(result.coaching_results) == 29

    def test_url_construction(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.coaches.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.coaches.get_coach_profile(coach_id="BeliBi0")

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/coaches/BeliBi0.htm"

    def test_wait_for_element(self, raw_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.coaches.browserless,
            "get_page_content",
            return_value=raw_html,
        ) as mock_fetch:
            pfr.coaches.get_coach_profile(coach_id="BeliBi0")

        assert mock_fetch.call_args[1]["wait_for_element"] == "#coaching_results"

    def test_lazy_loading(self):
        pfr = GriddyPFR()
        assert "coaches" in pfr._sub_sdk_map
        assert pfr.coaches is not None
        assert pfr.coaches is pfr.coaches
