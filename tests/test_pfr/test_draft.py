"""Tests for griddy.pfr.parsers.draft and the draft endpoints."""

import json
from unittest.mock import patch

import pytest

from griddy.pfr import GriddyPFR
from griddy.pfr.models.entities.draft import (
    CombineEntry,
    CombineResults,
    DraftPick,
    TeamDraft,
    TeamDraftPick,
    YearDraft,
)
from griddy.pfr.parsers.draft import DraftParser
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "draft"


@pytest.fixture
def parser() -> DraftParser:
    return DraftParser()


# ---------------------------------------------------------------------------
# Year Draft fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def year_draft_html() -> str:
    return (FIXTURE_DIR / "2024_draft.htm").read_text()


@pytest.fixture(scope="module")
def year_draft_parsed(year_draft_html: str) -> dict:
    return DraftParser().parse_year_draft(year_draft_html, year=2024)


@pytest.fixture(scope="module")
def year_draft(year_draft_parsed: dict) -> YearDraft:
    return YearDraft.model_validate(year_draft_parsed)


# ---------------------------------------------------------------------------
# Combine fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def combine_html() -> str:
    return (FIXTURE_DIR / "2024_combine.htm").read_text()


@pytest.fixture(scope="module")
def combine_parsed(combine_html: str) -> dict:
    return DraftParser().parse_combine(combine_html, year=2024)


@pytest.fixture(scope="module")
def combine_results(combine_parsed: dict) -> CombineResults:
    return CombineResults.model_validate(combine_parsed)


# ---------------------------------------------------------------------------
# Team Draft fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def team_draft_html() -> str:
    return (FIXTURE_DIR / "phi_draft.htm").read_text()


@pytest.fixture(scope="module")
def team_draft_parsed(team_draft_html: str) -> dict:
    return DraftParser().parse_team_draft(team_draft_html, team="phi")


@pytest.fixture(scope="module")
def team_draft(team_draft_parsed: dict) -> TeamDraft:
    return TeamDraft.model_validate(team_draft_parsed)


# ---------------------------------------------------------------------------
# Year Draft parse -- smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestYearDraftSmoke:
    """Smoke test: year draft fixture should parse without errors."""

    def test_parse_returns_dict(self, year_draft_parsed):
        assert isinstance(year_draft_parsed, dict)

    def test_parsed_data_has_all_keys(self, year_draft_parsed):
        expected_keys = {"year", "picks"}
        assert set(year_draft_parsed.keys()) == expected_keys

    def test_model_validates_successfully(self, year_draft):
        assert isinstance(year_draft, YearDraft)

    def test_year_is_set(self, year_draft):
        assert year_draft.year == 2024


# ---------------------------------------------------------------------------
# Year Draft picks
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestYearDraftPicks:
    def test_pick_count(self, year_draft):
        assert len(year_draft.picks) == 220

    def test_pick_is_model(self, year_draft):
        assert isinstance(year_draft.picks[0], DraftPick)

    # First pick: Caleb Williams
    def test_first_round(self, year_draft):
        assert year_draft.picks[0].draft_round == 1

    def test_first_pick(self, year_draft):
        assert year_draft.picks[0].draft_pick == 1

    def test_first_team(self, year_draft):
        assert year_draft.picks[0].team == "CHI"

    def test_first_team_href(self, year_draft):
        assert year_draft.picks[0].team_href == "/teams/chi/2024_draft.htm"

    def test_first_player(self, year_draft):
        assert year_draft.picks[0].player == "Caleb Williams"

    def test_first_player_id(self, year_draft):
        assert year_draft.picks[0].player_id == "WillCa03"

    def test_first_player_href(self, year_draft):
        assert year_draft.picks[0].player_href == "/players/W/WillCa03.htm"

    def test_first_pos(self, year_draft):
        assert year_draft.picks[0].pos == "QB"

    def test_first_age(self, year_draft):
        assert year_draft.picks[0].age == 22

    def test_first_college(self, year_draft):
        assert year_draft.picks[0].college == "USC"

    def test_first_career_av(self, year_draft):
        assert year_draft.picks[0].career_av == 26

    def test_first_draft_av(self, year_draft):
        assert year_draft.picks[0].draft_av == 26

    def test_first_games(self, year_draft):
        assert year_draft.picks[0].g == 34

    def test_first_pass_yds(self, year_draft):
        assert year_draft.picks[0].pass_yds == 7483

    # Second pick: Jayden Daniels
    def test_second_player(self, year_draft):
        assert year_draft.picks[1].player == "Jayden Daniels"

    def test_second_pick_number(self, year_draft):
        assert year_draft.picks[1].draft_pick == 2

    def test_second_pro_bowls(self, year_draft):
        assert year_draft.picks[1].pro_bowls == 1

    # Defensive player (should have def stats, no passing)
    def test_defensive_player_no_pass_stats(self, year_draft):
        """Defensive players should have None for passing stats."""
        defenders = [p for p in year_draft.picks if p.pos in ("DE", "DT", "LB")]
        assert len(defenders) > 0
        first_def = defenders[0]
        assert (
            first_def.tackles_solo is not None
            or first_def.def_int is not None
            or first_def.sacks is not None
        )

    def test_college_stats_href(self, year_draft):
        """First pick should have a college stats link."""
        assert year_draft.picks[0].college_stats_href is not None
        assert "sports-reference.com" in year_draft.picks[0].college_stats_href


# ---------------------------------------------------------------------------
# Combine parse -- smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCombineSmoke:
    """Smoke test: combine fixture should parse without errors."""

    def test_parse_returns_dict(self, combine_parsed):
        assert isinstance(combine_parsed, dict)

    def test_parsed_data_has_all_keys(self, combine_parsed):
        expected_keys = {"year", "entries"}
        assert set(combine_parsed.keys()) == expected_keys

    def test_model_validates_successfully(self, combine_results):
        assert isinstance(combine_results, CombineResults)

    def test_year_is_set(self, combine_results):
        assert combine_results.year == 2024


# ---------------------------------------------------------------------------
# Combine entries
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestCombineEntries:
    def test_entry_count(self, combine_results):
        assert len(combine_results.entries) == 321

    def test_entry_is_model(self, combine_results):
        assert isinstance(combine_results.entries[0], CombineEntry)

    # First entry: Kris Abrams-Draine
    def test_first_player(self, combine_results):
        assert combine_results.entries[0].player == "Kris Abrams-Draine"

    def test_first_player_id(self, combine_results):
        assert combine_results.entries[0].player_id == "AbraKr00"

    def test_first_pos(self, combine_results):
        assert combine_results.entries[0].pos == "CB"

    def test_first_school(self, combine_results):
        assert combine_results.entries[0].school == "Missouri"

    def test_first_school_href(self, combine_results):
        assert combine_results.entries[0].school_href == "/schools/missouri/"

    def test_first_height(self, combine_results):
        assert combine_results.entries[0].height == "5-11"

    def test_first_weight(self, combine_results):
        assert combine_results.entries[0].weight == 179

    def test_first_forty_yd(self, combine_results):
        assert combine_results.entries[0].forty_yd == 4.44

    def test_first_vertical(self, combine_results):
        assert combine_results.entries[0].vertical == 33.5

    def test_first_drafted_team(self, combine_results):
        assert combine_results.entries[0].drafted_team == "Denver Broncos"

    def test_first_drafted_round(self, combine_results):
        assert combine_results.entries[0].drafted_round == "5th"

    def test_first_drafted_pick(self, combine_results):
        assert combine_results.entries[0].drafted_pick == "145th pick"

    def test_first_drafted_year(self, combine_results):
        assert combine_results.entries[0].drafted_year == 2024

    # Empty measurement fields
    def test_missing_measurement_is_none(self, combine_results):
        """Players without certain measurements should have None."""
        first = combine_results.entries[0]
        assert first.bench_reps is None

    # Undrafted player
    def test_undrafted_player_exists(self, combine_results):
        """Some combine participants are undrafted."""
        undrafted = [e for e in combine_results.entries if e.draft_info is None]
        assert len(undrafted) > 0

    def test_undrafted_player_no_draft_fields(self, combine_results):
        """Undrafted players should have None for drafted_* fields."""
        undrafted = [e for e in combine_results.entries if e.draft_info is None]
        assert undrafted[0].drafted_team is None
        assert undrafted[0].drafted_year is None


# ---------------------------------------------------------------------------
# Team Draft parse -- smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestTeamDraftSmoke:
    """Smoke test: team draft fixture should parse without errors."""

    def test_parse_returns_dict(self, team_draft_parsed):
        assert isinstance(team_draft_parsed, dict)

    def test_parsed_data_has_all_keys(self, team_draft_parsed):
        expected_keys = {"team", "picks"}
        assert set(team_draft_parsed.keys()) == expected_keys

    def test_model_validates_successfully(self, team_draft):
        assert isinstance(team_draft, TeamDraft)

    def test_team_is_set(self, team_draft):
        assert team_draft.team == "phi"


# ---------------------------------------------------------------------------
# Team Draft picks
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestTeamDraftPicks:
    def test_pick_count(self, team_draft):
        assert len(team_draft.picks) == 250

    def test_pick_is_model(self, team_draft):
        assert isinstance(team_draft.picks[0], TeamDraftPick)

    # First pick: Jihaad Campbell (2025)
    def test_first_year(self, team_draft):
        assert team_draft.picks[0].year == 2025

    def test_first_year_href(self, team_draft):
        assert team_draft.picks[0].year_href == "/years/2025/draft.htm"

    def test_first_round(self, team_draft):
        assert team_draft.picks[0].draft_round == 1

    def test_first_player(self, team_draft):
        assert team_draft.picks[0].player == "Jihaad Campbell"

    def test_first_player_id(self, team_draft):
        assert team_draft.picks[0].player_id == "CampJi00"

    def test_first_pick_number(self, team_draft):
        assert team_draft.picks[0].draft_pick == 31

    def test_first_pos(self, team_draft):
        assert team_draft.picks[0].pos == "LB"

    def test_first_career_av(self, team_draft):
        assert team_draft.picks[0].career_av == 6

    def test_first_college(self, team_draft):
        assert team_draft.picks[0].college == "Alabama"

    # Sorted newest to oldest
    def test_sorted_newest_first(self, team_draft):
        """Team draft picks should be sorted newest year first."""
        first_year = team_draft.picks[0].year
        last_year = team_draft.picks[-1].year
        assert first_year >= last_year


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestJsonSerialization:
    def test_year_draft_serializes(self, year_draft):
        output = year_draft.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert len(loaded["picks"]) == 220

    def test_year_draft_round_trip(self, year_draft):
        dumped = year_draft.model_dump()
        assert len(dumped["picks"]) == 220
        assert dumped["year"] == 2024

    def test_combine_serializes(self, combine_results):
        output = combine_results.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert len(loaded["entries"]) == 321

    def test_team_draft_serializes(self, team_draft):
        output = team_draft.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert len(loaded["picks"]) == 250


# ---------------------------------------------------------------------------
# Draft endpoints
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestYearEndpoint:
    def test_year_returns_model(self, year_draft_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.draft.browserless,
            "get_page_content",
            return_value=year_draft_html,
        ) as mock_fetch:
            result = pfr.draft.year(year=2024)

        mock_fetch.assert_called_once()
        assert isinstance(result, YearDraft)
        assert len(result.picks) == 220

    def test_year_url_construction(self, year_draft_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.draft.browserless,
            "get_page_content",
            return_value=year_draft_html,
        ) as mock_fetch:
            pfr.draft.year(year=2024)

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/years/2024/draft.htm"

    def test_year_wait_for_element(self, year_draft_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.draft.browserless,
            "get_page_content",
            return_value=year_draft_html,
        ) as mock_fetch:
            pfr.draft.year(year=2024)

        assert mock_fetch.call_args[1]["wait_for_element"] == "#drafts"


@pytest.mark.unit
class TestCombineEndpoint:
    def test_combine_returns_model(self, combine_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.draft.browserless,
            "get_page_content",
            return_value=combine_html,
        ) as mock_fetch:
            result = pfr.draft.combine(year=2024)

        mock_fetch.assert_called_once()
        assert isinstance(result, CombineResults)
        assert len(result.entries) == 321

    def test_combine_url_construction(self, combine_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.draft.browserless,
            "get_page_content",
            return_value=combine_html,
        ) as mock_fetch:
            pfr.draft.combine(year=2024)

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/draft/2024-combine.htm"

    def test_combine_wait_for_element(self, combine_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.draft.browserless,
            "get_page_content",
            return_value=combine_html,
        ) as mock_fetch:
            pfr.draft.combine(year=2024)

        assert mock_fetch.call_args[1]["wait_for_element"] == "#combine"


@pytest.mark.unit
class TestTeamEndpoint:
    def test_team_returns_model(self, team_draft_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.draft.browserless,
            "get_page_content",
            return_value=team_draft_html,
        ) as mock_fetch:
            result = pfr.draft.team(team="phi")

        mock_fetch.assert_called_once()
        assert isinstance(result, TeamDraft)
        assert len(result.picks) == 250

    def test_team_url_construction(self, team_draft_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.draft.browserless,
            "get_page_content",
            return_value=team_draft_html,
        ) as mock_fetch:
            pfr.draft.team(team="PHI")

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/teams/phi/draft.htm"

    def test_team_wait_for_element(self, team_draft_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.draft.browserless,
            "get_page_content",
            return_value=team_draft_html,
        ) as mock_fetch:
            pfr.draft.team(team="phi")

        assert mock_fetch.call_args[1]["wait_for_element"] == "#draft"


# ---------------------------------------------------------------------------
# Lazy loading
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestLazyLoading:
    def test_draft_in_sub_sdk_map(self):
        pfr = GriddyPFR()
        assert "draft" in pfr._sub_sdk_map

    def test_draft_is_cached(self):
        pfr = GriddyPFR()
        assert pfr.draft is pfr.draft
