"""Tests for PFR Executive profile endpoint.

Covers:
- Executive bio parsing
- Team results (exec_results tbody)
- Results totals (exec_results tfoot)
- JSON serialization roundtrip
- Endpoint integration (mocked)
- Lazy loading
"""

import json
from unittest.mock import patch

import pytest

from griddy.pfr.models import (
    ExecutiveBio,
    ExecutiveProfile,
    ExecutiveResult,
    ExecutiveResultsTotal,
)
from griddy.pfr.parsers.executive_profile import ExecutiveProfileParser
from griddy.pfr.sdk import GriddyPFR
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "executives"

_parser = ExecutiveProfileParser()


# -------------------------------------------------------------------------
# Fixtures — Bud Adams (owner, single-team, 54 years)
# -------------------------------------------------------------------------


@pytest.fixture(scope="module")
def adams_html() -> str:
    return (FIXTURE_DIR / "bud_adams.htm").read_text()


@pytest.fixture(scope="module")
def adams_parsed(adams_html: str) -> dict:
    return _parser.parse(adams_html)


@pytest.fixture(scope="module")
def adams(adams_parsed: dict) -> ExecutiveProfile:
    return ExecutiveProfile.model_validate(adams_parsed)


# -------------------------------------------------------------------------
# Fixtures — Scott Pioli (GM, multi-team)
# -------------------------------------------------------------------------


@pytest.fixture(scope="module")
def pioli_html() -> str:
    return (FIXTURE_DIR / "scott_pioli.htm").read_text()


@pytest.fixture(scope="module")
def pioli_parsed(pioli_html: str) -> dict:
    return _parser.parse(pioli_html)


@pytest.fixture(scope="module")
def pioli(pioli_parsed: dict) -> ExecutiveProfile:
    return ExecutiveProfile.model_validate(pioli_parsed)


# =========================================================================
# Smoke tests
# =========================================================================


@pytest.mark.unit
class TestParseSmoke:
    def test_parse_returns_dict(self, adams_parsed):
        assert isinstance(adams_parsed, dict)

    def test_parsed_data_has_all_keys(self, adams_parsed):
        expected_keys = {"bio", "exec_results", "exec_results_totals"}
        assert set(adams_parsed.keys()) == expected_keys

    def test_model_validates_successfully(self, adams):
        assert isinstance(adams, ExecutiveProfile)

    def test_pioli_model_validates(self, pioli):
        assert isinstance(pioli, ExecutiveProfile)


# =========================================================================
# Bio
# =========================================================================


@pytest.mark.unit
class TestBio:
    def test_bio_is_model(self, adams):
        assert isinstance(adams.bio, ExecutiveBio)

    def test_adams_name(self, adams):
        assert adams.bio.name == "Bud Adams"

    def test_pioli_name(self, pioli):
        assert pioli.bio.name == "Scott Pioli"


# =========================================================================
# Executive Results — Bud Adams
# =========================================================================


@pytest.mark.unit
class TestAdamsResults:
    def test_result_count(self, adams):
        assert len(adams.exec_results) == 54

    def test_result_is_model(self, adams):
        assert isinstance(adams.exec_results[0], ExecutiveResult)

    # -- First year (1960) --

    def test_first_year(self, adams):
        assert adams.exec_results[0].year == "1960"

    def test_first_year_href(self, adams):
        assert adams.exec_results[0].year_href == "/years/1960_AFL/"

    def test_first_team(self, adams):
        assert adams.exec_results[0].team == "Houston Oilers"

    def test_first_team_href(self, adams):
        assert adams.exec_results[0].team_href == "/teams/oti/1960.htm"

    def test_first_league(self, adams):
        assert adams.exec_results[0].league == "AFL"

    def test_first_job_title(self, adams):
        assert adams.exec_results[0].job_title == "Founder/Owner/Chairman/President/CEO"

    def test_first_wins(self, adams):
        assert adams.exec_results[0].wins == 10

    def test_first_losses(self, adams):
        assert adams.exec_results[0].losses == 4

    def test_first_ties(self, adams):
        assert adams.exec_results[0].ties == 0

    def test_first_win_loss_pct(self, adams):
        assert adams.exec_results[0].win_loss_pct == ".714"

    def test_first_playoff_wins(self, adams):
        assert adams.exec_results[0].playoff_wins == 1

    def test_first_playoff_losses(self, adams):
        assert adams.exec_results[0].playoff_losses == 0

    def test_first_playoff_result(self, adams):
        assert adams.exec_results[0].playoff_result == "Won Champ"

    def test_first_playoff_result_href(self, adams):
        assert (
            adams.exec_results[0].playoff_result_href == "/boxscores/196101010oti.htm"
        )

    # -- Last year (2013) --

    def test_last_year(self, adams):
        assert adams.exec_results[-1].year == "2013"

    def test_last_team(self, adams):
        assert adams.exec_results[-1].team == "Tennessee Titans"

    def test_last_league(self, adams):
        assert adams.exec_results[-1].league == "NFL"

    def test_last_wins(self, adams):
        assert adams.exec_results[-1].wins == 7

    def test_last_losses(self, adams):
        assert adams.exec_results[-1].losses == 9


# =========================================================================
# Executive Results — Scott Pioli
# =========================================================================


@pytest.mark.unit
class TestPioliResults:
    def test_result_count(self, pioli):
        assert len(pioli.exec_results) == 13

    def test_first_year(self, pioli):
        assert pioli.exec_results[0].year == "2000"

    def test_first_team(self, pioli):
        assert pioli.exec_results[0].team == "New England Patriots"

    def test_first_job_title(self, pioli):
        assert pioli.exec_results[0].job_title == "Asst. Director of Player Personnel"

    def test_super_bowl_win(self, pioli):
        assert pioli.exec_results[1].playoff_result == "Won SB"

    def test_super_bowl_href(self, pioli):
        assert (
            pioli.exec_results[1].playoff_result_href == "/boxscores/200202030nwe.htm"
        )

    def test_last_team_is_chiefs(self, pioli):
        assert pioli.exec_results[-1].team == "Kansas City Chiefs"

    def test_last_job_title(self, pioli):
        assert pioli.exec_results[-1].job_title == "General Manager"


# =========================================================================
# Results Totals — Bud Adams
# =========================================================================


@pytest.mark.unit
class TestAdamsTotals:
    def test_totals_count(self, adams):
        assert len(adams.exec_results_totals) == 2

    def test_total_is_model(self, adams):
        assert isinstance(adams.exec_results_totals[0], ExecutiveResultsTotal)

    def test_first_total_label(self, adams):
        assert adams.exec_results_totals[0].label == "Total"

    def test_first_total_tenure(self, adams):
        assert adams.exec_results_totals[0].tenure == "54 Years"

    def test_first_total_wins(self, adams):
        assert adams.exec_results_totals[0].wins == 399

    def test_first_total_losses(self, adams):
        assert adams.exec_results_totals[0].losses == 415

    def test_first_total_ties(self, adams):
        assert adams.exec_results_totals[0].ties == 6

    def test_first_total_playoff_wins(self, adams):
        assert adams.exec_results_totals[0].playoff_wins == 14

    def test_first_total_playoff_losses(self, adams):
        assert adams.exec_results_totals[0].playoff_losses == 19


# =========================================================================
# Results Totals — Scott Pioli (multi-team)
# =========================================================================


@pytest.mark.unit
class TestPioliTotals:
    def test_totals_count(self, pioli):
        """Multi-team exec should have overall total + one per team."""
        assert len(pioli.exec_results_totals) == 3

    def test_overall_total(self, pioli):
        assert pioli.exec_results_totals[0].label == "Total"
        assert pioli.exec_results_totals[0].tenure == "13 Years"
        assert pioli.exec_results_totals[0].wins == 125
        assert pioli.exec_results_totals[0].losses == 83

    def test_patriots_total(self, pioli):
        assert pioli.exec_results_totals[1].label == "New England Patriots"
        assert pioli.exec_results_totals[1].tenure == "2000-2008"
        assert pioli.exec_results_totals[1].wins == 102

    def test_chiefs_total(self, pioli):
        assert pioli.exec_results_totals[2].label == "Kansas City Chiefs"
        assert pioli.exec_results_totals[2].tenure == "2009-2012"
        assert pioli.exec_results_totals[2].wins == 23


# =========================================================================
# JSON serialization
# =========================================================================


@pytest.mark.unit
class TestJsonSerialization:
    def test_serializes_to_json(self, adams):
        output = adams.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert loaded["bio"]["name"] == "Bud Adams"

    def test_model_dump_round_trip(self, adams):
        dumped = adams.model_dump()
        rebuilt = ExecutiveProfile.model_validate(dumped)
        assert rebuilt.bio.name == "Bud Adams"
        assert len(rebuilt.exec_results) == 54
        assert len(rebuilt.exec_results_totals) == 2

    def test_pioli_round_trip(self, pioli):
        dumped = pioli.model_dump()
        rebuilt = ExecutiveProfile.model_validate(dumped)
        assert rebuilt.bio.name == "Scott Pioli"
        assert len(rebuilt.exec_results) == 13
        assert len(rebuilt.exec_results_totals) == 3


# =========================================================================
# Endpoint integration (mocked)
# =========================================================================


@pytest.mark.unit
class TestExecutivesEndpoint:
    def test_get_returns_model(self, adams_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.executives.browserless,
            "get_page_content",
            return_value=adams_html,
        ) as mock_fetch:
            result = pfr.executives.get(executive_id="AdamBu0")

        mock_fetch.assert_called_once()
        assert isinstance(result, ExecutiveProfile)
        assert result.bio.name == "Bud Adams"
        assert len(result.exec_results) == 54

    def test_url_construction(self, adams_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.executives.browserless,
            "get_page_content",
            return_value=adams_html,
        ) as mock_fetch:
            pfr.executives.get(executive_id="AdamBu0")

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/executives/AdamBu0.htm"

    def test_wait_for_element(self, adams_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.executives.browserless,
            "get_page_content",
            return_value=adams_html,
        ) as mock_fetch:
            pfr.executives.get(executive_id="AdamBu0")

        assert mock_fetch.call_args[1]["wait_for_element"] == "#exec_results"


# =========================================================================
# Lazy loading
# =========================================================================


@pytest.mark.unit
class TestLazyLoading:
    def test_executives_in_sub_sdk_map(self):
        assert "executives" in GriddyPFR._sub_sdk_map

    def test_executives_lazy_load(self):
        pfr = GriddyPFR()
        from griddy.pfr.endpoints.executives import Executives

        assert isinstance(pfr.executives, Executives)

    def test_executives_cached(self):
        pfr = GriddyPFR()
        assert pfr.executives is pfr.executives
