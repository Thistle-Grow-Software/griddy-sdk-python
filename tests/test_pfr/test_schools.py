"""Tests for PFR Schools & Colleges endpoints.

Covers:
- Colleges list (``/schools/``)
- High Schools list (``/schools/high_schools.cgi``)
"""

from unittest.mock import patch

import pytest

from griddy.pfr.models import (
    College,
    CollegeList,
    HighSchool,
    HighSchoolList,
)
from griddy.pfr.parsers.schools import SchoolsParser
from griddy.pfr.sdk import GriddyPFR
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "schools"

_parser = SchoolsParser()

# -------------------------------------------------------------------------
# Fixtures — Colleges
# -------------------------------------------------------------------------


@pytest.fixture(scope="module")
def colleges_html() -> str:
    return (FIXTURE_DIR / "colleges.htm").read_text()


@pytest.fixture(scope="module")
def colleges_parsed(colleges_html: str) -> dict:
    return _parser.parse_colleges(colleges_html)


@pytest.fixture(scope="module")
def colleges_model(colleges_parsed: dict) -> CollegeList:
    return CollegeList.model_validate(colleges_parsed)


# -------------------------------------------------------------------------
# Fixtures — High Schools
# -------------------------------------------------------------------------


@pytest.fixture(scope="module")
def high_schools_html() -> str:
    return (FIXTURE_DIR / "high_schools.htm").read_text()


@pytest.fixture(scope="module")
def high_schools_parsed(high_schools_html: str) -> dict:
    return _parser.parse_high_schools(high_schools_html)


@pytest.fixture(scope="module")
def high_schools_model(high_schools_parsed: dict) -> HighSchoolList:
    return HighSchoolList.model_validate(high_schools_parsed)


# =========================================================================
# Colleges — Smoke tests
# =========================================================================


@pytest.mark.unit
class TestCollegesSmoke:
    def test_parse_returns_dict(self, colleges_parsed):
        assert isinstance(colleges_parsed, dict)

    def test_has_colleges_key(self, colleges_parsed):
        assert "colleges" in colleges_parsed

    def test_model_validates(self, colleges_model):
        assert isinstance(colleges_model, CollegeList)

    def test_college_count(self, colleges_model):
        assert len(colleges_model.colleges) == 201


# =========================================================================
# Colleges — Row data
# =========================================================================


@pytest.mark.unit
class TestCollegesData:
    def test_first_college_identity(self, colleges_model):
        first = colleges_model.colleges[0]
        assert isinstance(first, College)
        assert first.rank == 1
        assert first.college_name == "Notre Dame"
        assert first.college_href == "/schools/notredame/"

    def test_first_college_state(self, colleges_model):
        first = colleges_model.colleges[0]
        assert first.state == "IN"

    def test_first_college_player_counts(self, colleges_model):
        first = colleges_model.colleges[0]
        assert first.players == 645
        assert first.players_active == 54

    def test_first_college_honors(self, colleges_model):
        first = colleges_model.colleges[0]
        assert first.hofers == 14
        assert first.pro_bowls == 203

    def test_first_college_totals(self, colleges_model):
        first = colleges_model.colleges[0]
        assert first.games == 31726
        assert first.touchdowns == 2035

    def test_first_college_best_career_av(self, colleges_model):
        first = colleges_model.colleges[0]
        assert first.best_career_av_player == "Alan Page"
        assert first.best_career_av_player_href == "/players/P/PageAl00.htm"
        assert first.best_career_av == 144

    def test_first_college_most_td(self, colleges_model):
        first = colleges_model.colleges[0]
        assert first.most_td_player == "Tim Brown"
        assert first.most_td_player_href == "/players/B/BrowTi00.htm"
        assert first.most_td == 105

    def test_first_college_most_games(self, colleges_model):
        first = colleges_model.colleges[0]
        assert first.most_games_player == "John Carney"
        assert first.most_games_player_href == "/players/C/carnejoh01.htm"
        assert first.most_games == 302

    def test_second_college_is_usc(self, colleges_model):
        second = colleges_model.colleges[1]
        assert second.college_name == "USC"
        assert second.college_href == "/schools/usc/"
        assert second.state == "CA"

    def test_last_college(self, colleges_model):
        last = colleges_model.colleges[-1]
        assert last.rank == 201
        assert last.college_name == "Lafayette"


# =========================================================================
# High Schools — Smoke tests
# =========================================================================


@pytest.mark.unit
class TestHighSchoolsSmoke:
    def test_parse_returns_dict(self, high_schools_parsed):
        assert isinstance(high_schools_parsed, dict)

    def test_has_schools_key(self, high_schools_parsed):
        assert "schools" in high_schools_parsed

    def test_model_validates(self, high_schools_model):
        assert isinstance(high_schools_model, HighSchoolList)

    def test_school_count(self, high_schools_model):
        assert len(high_schools_model.schools) == 100


# =========================================================================
# High Schools — Row data
# =========================================================================


@pytest.mark.unit
class TestHighSchoolsData:
    def test_first_school_identity(self, high_schools_model):
        first = high_schools_model.schools[0]
        assert isinstance(first, HighSchool)
        assert first.name == "Fork Union Military Academy"
        assert first.name_href == "high_schools.cgi?id=93b82c1b"

    def test_first_school_location(self, high_schools_model):
        first = high_schools_model.schools[0]
        assert first.city == "Fork Union"
        assert first.state == "VA"

    def test_first_school_counts(self, high_schools_model):
        first = high_schools_model.schools[0]
        assert first.num_players == 68
        assert first.num_active == 3

    def test_second_school(self, high_schools_model):
        second = high_schools_model.schools[1]
        assert second.name == "Long Beach Polytechnic"
        assert second.city == "Long Beach"
        assert second.state == "CA"
        assert second.num_players == 61

    def test_last_school(self, high_schools_model):
        last = high_schools_model.schools[-1]
        assert last.name == "David W. Carter"
        assert last.city == "Dallas"
        assert last.state == "TX"


# =========================================================================
# JSON serialization
# =========================================================================


@pytest.mark.unit
class TestJsonSerialization:
    def test_colleges_roundtrip(self, colleges_model):
        data = colleges_model.model_dump()
        rebuilt = CollegeList.model_validate(data)
        assert len(rebuilt.colleges) == len(colleges_model.colleges)

    def test_colleges_data_preserved(self, colleges_model):
        data = colleges_model.model_dump()
        rebuilt = CollegeList.model_validate(data)
        assert rebuilt.colleges[0].college_name == "Notre Dame"
        assert rebuilt.colleges[0].best_career_av_player == "Alan Page"

    def test_high_schools_roundtrip(self, high_schools_model):
        data = high_schools_model.model_dump()
        rebuilt = HighSchoolList.model_validate(data)
        assert len(rebuilt.schools) == len(high_schools_model.schools)

    def test_high_schools_data_preserved(self, high_schools_model):
        data = high_schools_model.model_dump()
        rebuilt = HighSchoolList.model_validate(data)
        assert rebuilt.schools[0].name == "Fork Union Military Academy"
        assert rebuilt.schools[0].city == "Fork Union"


# =========================================================================
# Endpoint integration tests (mocked)
# =========================================================================


@pytest.mark.unit
class TestListEndpoint:
    def test_list_returns_model(self, colleges_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.schools.browserless,
            "get_page_content",
            return_value=colleges_html,
        ) as mock_fetch:
            result = pfr.schools.list()

        mock_fetch.assert_called_once()
        assert isinstance(result, CollegeList)
        assert len(result.colleges) == 201

    def test_list_url_construction(self, colleges_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.schools.browserless,
            "get_page_content",
            return_value=colleges_html,
        ) as mock_fetch:
            pfr.schools.list()

        call_args = mock_fetch.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get("url", "")
        assert "/schools/" in url

    def test_list_wait_for_element(self, colleges_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.schools.browserless,
            "get_page_content",
            return_value=colleges_html,
        ) as mock_fetch:
            pfr.schools.list()

        call_args = mock_fetch.call_args
        wait_for = (
            call_args[1].get("wait_for_element") if call_args[1] else call_args[0][1]
        )
        assert wait_for == "#college_stats_table"


@pytest.mark.unit
class TestHighSchoolsEndpoint:
    def test_high_schools_returns_model(self, high_schools_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.schools.browserless,
            "get_page_content",
            return_value=high_schools_html,
        ) as mock_fetch:
            result = pfr.schools.high_schools()

        mock_fetch.assert_called_once()
        assert isinstance(result, HighSchoolList)
        assert len(result.schools) == 100

    def test_high_schools_url_construction(self, high_schools_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.schools.browserless,
            "get_page_content",
            return_value=high_schools_html,
        ) as mock_fetch:
            pfr.schools.high_schools()

        call_args = mock_fetch.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get("url", "")
        assert "/schools/high_schools.cgi" in url

    def test_high_schools_wait_for_element(self, high_schools_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.schools.browserless,
            "get_page_content",
            return_value=high_schools_html,
        ) as mock_fetch:
            pfr.schools.high_schools()

        call_args = mock_fetch.call_args
        wait_for = (
            call_args[1].get("wait_for_element") if call_args[1] else call_args[0][1]
        )
        assert wait_for == "#high_schools"


# =========================================================================
# Lazy loading
# =========================================================================


@pytest.mark.unit
class TestLazyLoading:
    def test_schools_in_sub_sdk_map(self):
        assert "schools" in GriddyPFR._sub_sdk_map

    def test_schools_lazy_load(self):
        pfr = GriddyPFR()
        from griddy.pfr.endpoints.schools import Schools

        assert isinstance(pfr.schools, Schools)
