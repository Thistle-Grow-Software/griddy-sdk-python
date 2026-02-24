"""Tests for griddy.pfr.parsers.player_profile module."""

import json
from pathlib import Path

import pytest

from griddy.pfr.parsers.player_profile import PlayerProfileParser

FIXTURE_DIR = Path(__file__).resolve().parents[2] / "data" / "pfr_examples"


@pytest.fixture
def parser() -> PlayerProfileParser:
    return PlayerProfileParser()


# ---------------------------------------------------------------------------
# Per-player fixtures: load HTML once, parse once, reuse across test classes
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def brady_data() -> dict:
    html = (FIXTURE_DIR / "BradTo00_QB.htm").read_text()
    return PlayerProfileParser().parse(html)


@pytest.fixture(scope="module")
def warner_data() -> dict:
    html = (FIXTURE_DIR / "WarnFr00_LB.htm").read_text()
    return PlayerProfileParser().parse(html)


@pytest.fixture(scope="module")
def pitts_data() -> dict:
    html = (FIXTURE_DIR / "PittKy00_TE.htm").read_text()
    return PlayerProfileParser().parse(html)


@pytest.fixture(scope="module")
def jones_data() -> dict:
    """Broderick Jones — OL with no transactions/leaderboards/bottom_nav."""
    html = (FIXTURE_DIR / "JoneBr09_OL.htm").read_text()
    return PlayerProfileParser().parse(html)


@pytest.fixture(scope="module")
def boswell_data() -> dict:
    """Chris Boswell — K, undrafted, has a nickname."""
    html = (FIXTURE_DIR / "BoswCh00_K.htm").read_text()
    return PlayerProfileParser().parse(html)


@pytest.fixture(scope="module")
def williams_data() -> dict:
    html = (FIXTURE_DIR / "WillJa10_RB.htm").read_text()
    return PlayerProfileParser().parse(html)


# ---------------------------------------------------------------------------
# Full parse — all fixture files
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseAllFixtures:
    """Smoke test: every .htm fixture should parse without errors."""

    @pytest.mark.parametrize(
        "filename",
        sorted(p.name for p in FIXTURE_DIR.glob("*.htm")),
    )
    def test_fixture_parses_successfully(self, parser, filename):
        html = (FIXTURE_DIR / filename).read_text()
        result = parser.parse(html)
        assert isinstance(result, dict)

    @pytest.mark.parametrize(
        "filename",
        sorted(p.name for p in FIXTURE_DIR.glob("*.htm")),
    )
    def test_result_has_expected_top_level_keys(self, parser, filename):
        html = (FIXTURE_DIR / filename).read_text()
        result = parser.parse(html)
        expected_keys = {
            "bio",
            "jersey_numbers",
            "summary_stats",
            "statistics",
            "transactions",
            "links",
            "leader_boards",
        }
        assert set(result.keys()) == expected_keys


# ---------------------------------------------------------------------------
# Bio / Meta panel
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseBio:
    def test_photo_url_present(self, brady_data):
        assert brady_data["bio"]["photo_url"].startswith("https://")

    def test_names_first_name(self, brady_data):
        assert brady_data["bio"]["names"]["first_name"] == "Thomas"

    def test_names_middle_name(self, brady_data):
        assert brady_data["bio"]["names"]["middle_name"] == "Edward Patrick"

    def test_names_last_name(self, brady_data):
        assert brady_data["bio"]["names"]["last_name"] == "Brady"

    def test_names_pretty_name(self, brady_data):
        assert brady_data["bio"]["names"]["pretty_name"] == "Tom Brady"

    def test_names_suffix_empty_when_absent(self, brady_data):
        assert brady_data["bio"]["names"]["suffix"] == ""

    def test_no_nickname_returns_empty_list(self, warner_data):
        assert warner_data["bio"]["names"]["nicknames"] == []

    def test_multiple_nicknames(self, brady_data):
        nicks = brady_data["bio"]["names"]["nicknames"]
        assert isinstance(nicks, list)
        assert len(nicks) > 1
        assert "TB12" in nicks
        assert "GOAT" in nicks

    def test_single_nickname(self, boswell_data):
        nicks = boswell_data["bio"]["names"]["nicknames"]
        assert isinstance(nicks, list)
        assert len(nicks) >= 1

    def test_nickname_containing_or(self, pitts_data):
        """'Unicorn' should not be split by the 'or' separator logic."""
        nicks = pitts_data["bio"]["names"]["nicknames"]
        assert "Unicorn" in nicks

    def test_position(self, brady_data):
        assert brady_data["bio"]["position"] == "QB"

    def test_position_ol(self, jones_data):
        assert jones_data["bio"]["position"] == "T"

    def test_height_is_int_inches(self, brady_data):
        assert isinstance(brady_data["bio"]["height"], int)
        assert brady_data["bio"]["height"] == 76  # 6-4

    def test_weight_present(self, brady_data):
        assert brady_data["bio"]["weight"]

    def test_birth_date_iso_format(self, brady_data):
        bd = brady_data["bio"]["birth_date"]
        # datetime object — verify year
        assert bd.year == 1977

    def test_birth_place(self, brady_data):
        bp = brady_data["bio"]["birth_place"]
        assert "city" in bp
        assert "state" in bp
        assert bp["city"] == "San Mateo"
        assert bp["state"].strip() == "CA"

    def test_college(self, brady_data):
        assert brady_data["bio"]["college"] == "Michigan"

    def test_high_school(self, brady_data):
        assert "Junipero Serra" in brady_data["bio"]["high_school"]

    def test_draft_info_present(self, brady_data):
        draft = brady_data["bio"]["draft"]
        assert draft["team"] == "New England Patriots"
        assert draft["rd_and_ovr"]["round"] == 6
        assert draft["rd_and_ovr"]["overall"] == 199
        assert draft["year"] == 2000

    def test_undrafted_has_empty_draft(self, boswell_data):
        assert boswell_data["bio"]["draft"] == {}


# ---------------------------------------------------------------------------
# Extract names — unit-level tests with crafted HTML
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestExtractNames:
    def _make_tag(self, text: str):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(f"<p>{text}</p>", "html.parser")
        return soup.find("p")

    def test_simple_name(self, parser):
        tag = self._make_tag("John Smith")
        result = parser._extract_names(name_tag=tag)
        assert result["first_name"] == "John"
        assert result["last_name"] == "Smith"
        assert result["middle_name"] == ""
        assert result["suffix"] == ""

    def test_name_with_suffix(self, parser):
        tag = self._make_tag("Odell Beckham Jr.")
        result = parser._extract_names(name_tag=tag)
        assert result["first_name"] == "Odell"
        assert result["last_name"] == "Beckham"
        assert result["suffix"] == "Jr."

    def test_name_with_middle(self, parser):
        tag = self._make_tag("Thomas Edward Brady")
        result = parser._extract_names(name_tag=tag)
        assert result["first_name"] == "Thomas"
        assert result["middle_name"] == "Edward"
        assert result["last_name"] == "Brady"


# ---------------------------------------------------------------------------
# Jersey numbers
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseJerseyNumbers:
    def test_brady_has_two_jersey_entries(self, brady_data):
        assert len(brady_data["jersey_numbers"]) == 2

    def test_brady_first_jersey_number(self, brady_data):
        first = brady_data["jersey_numbers"][0]
        assert first["number"] == "12"
        assert first["team"] == "New England Patriots"
        assert first["start_year"] == 2000
        assert first["end_year"] == 2019

    def test_brady_second_jersey_number(self, brady_data):
        second = brady_data["jersey_numbers"][1]
        assert second["number"] == "12"
        assert second["team"] == "Tampa Bay Buccaneers"
        assert second["start_year"] == 2020
        assert second["end_year"] == 2022

    def test_single_year_jersey(self, warner_data):
        first = warner_data["jersey_numbers"][0]
        assert first["start_year"] == first["end_year"] == 2018

    def test_49ers_team_name_parsed(self, warner_data):
        """Team names with digits (49ers) should parse correctly."""
        first = warner_data["jersey_numbers"][0]
        assert "49ers" in first["team"]


# ---------------------------------------------------------------------------
# Extract team and years — unit-level tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestExtractTeamAndYearsJerseyNum:
    def test_single_year(self, parser):
        result = parser._extract_team_and_years_jersey_num("Dallas Cowboys 2020")
        assert result["team"] == "Dallas Cowboys"
        assert result["start_year"] == 2020
        assert result["end_year"] == 2020

    def test_year_range(self, parser):
        result = parser._extract_team_and_years_jersey_num(
            "New England Patriots 2000-2019"
        )
        assert result["team"] == "New England Patriots"
        assert result["start_year"] == 2000
        assert result["end_year"] == 2019

    def test_team_name_with_digits(self, parser):
        result = parser._extract_team_and_years_jersey_num("San Francisco 49ers 2018")
        assert result["team"] == "San Francisco 49ers"
        assert result["start_year"] == 2018
        assert result["end_year"] == 2018

    def test_team_name_with_digits_and_range(self, parser):
        result = parser._extract_team_and_years_jersey_num(
            "San Francisco 49ers 2019-2025"
        )
        assert result["team"] == "San Francisco 49ers"
        assert result["start_year"] == 2019
        assert result["end_year"] == 2025


# ---------------------------------------------------------------------------
# Summary stats
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseSummaryStats:
    def test_brady_summary_stats_has_keys(self, brady_data):
        ss = brady_data["summary_stats"]
        assert "G" in ss
        assert "TD" in ss
        assert "Int" in ss

    def test_brady_games_count(self, brady_data):
        assert brady_data["summary_stats"]["G"] == 335

    def test_brady_td_count(self, brady_data):
        assert brady_data["summary_stats"]["TD"] == 649

    def test_summary_stats_numeric(self, brady_data):
        ss = brady_data["summary_stats"]
        assert isinstance(ss["G"], int)
        assert isinstance(ss["Cmp%"], float)

    def test_kicker_summary_stats(self, boswell_data):
        ss = boswell_data["summary_stats"]
        assert "FGM" in ss or "FGA" in ss


# ---------------------------------------------------------------------------
# Statistics tables
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseStatistics:
    def test_has_regular_season(self, brady_data):
        assert "regular_season" in brady_data["statistics"]

    def test_has_post_season(self, brady_data):
        assert "post_season" in brady_data["statistics"]

    def test_regular_season_has_passing(self, brady_data):
        assert "passing" in brady_data["statistics"]["regular_season"]

    def test_regular_season_passing_is_list(self, brady_data):
        passing = brady_data["statistics"]["regular_season"]["passing"]
        assert isinstance(passing, list)
        assert len(passing) > 0

    def test_ol_has_stats(self, jones_data):
        stats = jones_data["statistics"]
        assert "regular_season" in stats


# ---------------------------------------------------------------------------
# Transactions
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseTransactions:
    def test_brady_has_transactions(self, brady_data):
        assert isinstance(brady_data["transactions"], list)
        assert len(brady_data["transactions"]) > 0

    def test_transaction_has_date_and_description(self, brady_data):
        txn = brady_data["transactions"][0]
        assert "date" in txn
        assert "description" in txn

    def test_missing_transactions_returns_empty_list(self, jones_data):
        assert jones_data["transactions"] == []


# ---------------------------------------------------------------------------
# Bottom nav / links
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseBottomNav:
    def test_brady_has_links(self, brady_data):
        assert isinstance(brady_data["links"], dict)
        assert len(brady_data["links"]) > 0

    def test_jones_has_links(self, jones_data):
        """Even OL players have bottom nav links."""
        assert isinstance(jones_data["links"], dict)
        assert "overview" in jones_data["links"]


# ---------------------------------------------------------------------------
# Leaderboards
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestParseLeaderBoards:
    def test_brady_has_leader_boards(self, brady_data):
        lb = brady_data["leader_boards"]
        assert isinstance(lb, dict)
        assert len(lb) > 0

    def test_leader_board_values_are_lists(self, brady_data):
        for key, val in brady_data["leader_boards"].items():
            assert isinstance(val, list), f"leader_boards[{key}] should be a list"

    def test_missing_leaderboards_returns_empty_dict(self, jones_data):
        assert jones_data["leader_boards"] == {}


# ---------------------------------------------------------------------------
# JSON serialization with DateTimeEncoder
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestJsonSerialization:
    """Verify parsed data round-trips through JSON with DateTimeEncoder."""

    def test_brady_serializes_to_json(self, brady_data):
        from griddy.core.utils.serializers import DateTimeEncoder

        output = json.dumps(brady_data, cls=DateTimeEncoder)
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert loaded["bio"]["names"]["first_name"] == "Thomas"

    def test_birth_date_serialized_as_iso(self, brady_data):
        from griddy.core.utils.serializers import DateTimeEncoder

        output = json.dumps(brady_data, cls=DateTimeEncoder)
        loaded = json.loads(output)
        assert "1977-08-03" in loaded["bio"]["birth_date"]


# ---------------------------------------------------------------------------
# Pydantic model validation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestPydanticModelValidation:
    """Verify parsed data validates into Pydantic models."""

    @pytest.mark.parametrize(
        "filename",
        sorted(p.name for p in FIXTURE_DIR.glob("*.htm")),
    )
    def test_all_fixtures_validate(self, parser, filename):
        from griddy.pfr.models.entities.player_profile import PlayerProfile

        html = (FIXTURE_DIR / filename).read_text()
        result = parser.parse(html)
        profile = PlayerProfile.model_validate(result)
        assert profile.bio.names.first_name

    def test_brady_model_fields(self, brady_data):
        from griddy.pfr.models.entities.player_profile import PlayerProfile

        profile = PlayerProfile.model_validate(brady_data)
        assert profile.bio.names.pretty_name == "Tom Brady"
        assert profile.bio.position == "QB"
        assert profile.bio.throws == "Right"
        assert profile.bio.height == 76
        assert profile.bio.birth_date.year == 1977
        assert profile.bio.birth_place.city == "San Mateo"
        assert profile.bio.college == "Michigan"
        assert profile.bio.draft is not None
        assert profile.bio.draft.team == "New England Patriots"
        assert profile.bio.draft.rd_and_ovr.round == 6
        assert profile.bio.draft.rd_and_ovr.overall == 199
        assert profile.bio.draft.year == 2000
        assert len(profile.jersey_numbers) == 2
        assert profile.jersey_numbers[0].number == "12"
        assert profile.summary_stats["G"] == 335
        assert "passing" in profile.statistics.regular_season
        assert len(profile.transactions) > 0
        assert len(profile.links) > 0
        assert len(profile.leader_boards) > 0

    def test_undrafted_player_draft_is_none(self, boswell_data):
        from griddy.pfr.models.entities.player_profile import PlayerProfile

        profile = PlayerProfile.model_validate(boswell_data)
        assert profile.bio.draft is None

    def test_no_throws_field(self, jones_data):
        from griddy.pfr.models.entities.player_profile import PlayerProfile

        profile = PlayerProfile.model_validate(jones_data)
        assert profile.bio.throws is None

    def test_empty_transactions(self, jones_data):
        from griddy.pfr.models.entities.player_profile import PlayerProfile

        profile = PlayerProfile.model_validate(jones_data)
        assert profile.transactions == []

    def test_empty_leader_boards(self, jones_data):
        from griddy.pfr.models.entities.player_profile import PlayerProfile

        profile = PlayerProfile.model_validate(jones_data)
        assert profile.leader_boards == {}

    def test_model_serialization_round_trip(self, brady_data):
        from griddy.pfr.models.entities.player_profile import PlayerProfile

        profile = PlayerProfile.model_validate(brady_data)
        dumped = profile.model_dump()
        assert dumped["bio"]["names"]["pretty_name"] == "Tom Brady"
        assert dumped["bio"]["draft"]["team"] == "New England Patriots"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEdgeCases:
    def test_parser_reuse_across_files(self, parser):
        """Parser should be reusable across multiple HTML files."""
        for htm in list(FIXTURE_DIR.glob("*.htm"))[:3]:
            html = htm.read_text()
            result = parser.parse(html)
            assert "bio" in result

    def test_parse_clears_previous_soup(self, parser):
        """Each call to parse() should set a fresh soup."""
        html1 = (FIXTURE_DIR / "BradTo00_QB.htm").read_text()
        html2 = (FIXTURE_DIR / "WarnFr00_LB.htm").read_text()

        result1 = parser.parse(html1)
        result2 = parser.parse(html2)

        assert result1["bio"]["names"]["last_name"] == "Brady"
        assert result2["bio"]["names"]["last_name"] == "Warner"
