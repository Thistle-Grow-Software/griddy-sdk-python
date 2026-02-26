"""Tests for griddy.pfr.parsers.awards and the awards/hof/probowl endpoints."""

import json
from unittest.mock import patch

import pytest

from griddy.pfr import GriddyPFR
from griddy.pfr.models.entities.awards import (
    AwardHistory,
    AwardWinner,
    HallOfFame,
    HofPlayer,
    ProBowlPlayer,
    ProBowlRoster,
)
from griddy.pfr.parsers.awards import AwardsParser
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "awards"


@pytest.fixture
def parser() -> AwardsParser:
    return AwardsParser()


# ---------------------------------------------------------------------------
# Award fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def award_html() -> str:
    return (FIXTURE_DIR / "ap_nfl_mvp_award.htm").read_text()


@pytest.fixture(scope="module")
def award_parsed(award_html: str) -> dict:
    return AwardsParser().parse_award(award_html, award="ap-nfl-mvp-award")


@pytest.fixture(scope="module")
def award_history(award_parsed: dict) -> AwardHistory:
    return AwardHistory.model_validate(award_parsed)


# ---------------------------------------------------------------------------
# HOF fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def hof_html() -> str:
    return (FIXTURE_DIR / "hof.htm").read_text()


@pytest.fixture(scope="module")
def hof_parsed(hof_html: str) -> dict:
    return AwardsParser().parse_hof(hof_html)


@pytest.fixture(scope="module")
def hall_of_fame(hof_parsed: dict) -> HallOfFame:
    return HallOfFame.model_validate(hof_parsed)


# ---------------------------------------------------------------------------
# Pro Bowl fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def probowl_html() -> str:
    return (FIXTURE_DIR / "2024_probowl.htm").read_text()


@pytest.fixture(scope="module")
def probowl_parsed(probowl_html: str) -> dict:
    return AwardsParser().parse_probowl(probowl_html, year=2024)


@pytest.fixture(scope="module")
def probowl_roster(probowl_parsed: dict) -> ProBowlRoster:
    return ProBowlRoster.model_validate(probowl_parsed)


# ---------------------------------------------------------------------------
# Award parse -- smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAwardSmoke:
    """Smoke test: award fixture should parse without errors."""

    def test_parse_returns_dict(self, award_parsed):
        assert isinstance(award_parsed, dict)

    def test_parsed_data_has_all_keys(self, award_parsed):
        expected_keys = {"award", "winners"}
        assert set(award_parsed.keys()) == expected_keys

    def test_model_validates_successfully(self, award_history):
        assert isinstance(award_history, AwardHistory)

    def test_award_is_set(self, award_history):
        assert award_history.award == "ap-nfl-mvp-award"


# ---------------------------------------------------------------------------
# Award winners
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAwardWinners:
    def test_winner_count(self, award_history):
        assert len(award_history.winners) == 70

    def test_winner_is_model(self, award_history):
        assert isinstance(award_history.winners[0], AwardWinner)

    # First winner: Matthew Stafford (2025)
    def test_first_year(self, award_history):
        assert award_history.winners[0].year == 2025

    def test_first_year_href(self, award_history):
        assert award_history.winners[0].year_href == "/years/2025/"

    def test_first_league(self, award_history):
        assert award_history.winners[0].league == "NFL"

    def test_first_pos(self, award_history):
        assert award_history.winners[0].pos == "QB"

    def test_first_player(self, award_history):
        assert award_history.winners[0].player == "Matthew Stafford"

    def test_first_player_id(self, award_history):
        assert award_history.winners[0].player_id == "StafMa00"

    def test_first_player_href(self, award_history):
        assert award_history.winners[0].player_href == "/players/S/StafMa00.htm"

    def test_first_team(self, award_history):
        assert award_history.winners[0].team == "Los Angeles Rams"

    def test_first_team_href(self, award_history):
        assert award_history.winners[0].team_href == "/teams/ram/2025.htm"

    def test_first_voting_href(self, award_history):
        assert (
            award_history.winners[0].voting_href
            == "/awards/awards_2025.htm#voting_apmvp"
        )

    # Last winner should be from an older year
    def test_last_winner_older_year(self, award_history):
        assert award_history.winners[-1].year < award_history.winners[0].year


# ---------------------------------------------------------------------------
# HOF parse -- smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestHofSmoke:
    """Smoke test: HOF fixture should parse without errors."""

    def test_parse_returns_dict(self, hof_parsed):
        assert isinstance(hof_parsed, dict)

    def test_parsed_data_has_all_keys(self, hof_parsed):
        expected_keys = {"players"}
        assert set(hof_parsed.keys()) == expected_keys

    def test_model_validates_successfully(self, hall_of_fame):
        assert isinstance(hall_of_fame, HallOfFame)


# ---------------------------------------------------------------------------
# HOF players
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestHofPlayers:
    def test_player_count(self, hall_of_fame):
        assert len(hall_of_fame.players) == 332

    def test_player_is_model(self, hall_of_fame):
        assert isinstance(hall_of_fame.players[0], HofPlayer)

    # First player: Drew Brees
    def test_first_rank(self, hall_of_fame):
        assert hall_of_fame.players[0].rank == 1

    def test_first_player(self, hall_of_fame):
        assert hall_of_fame.players[0].player == "Drew Brees"

    def test_first_player_id(self, hall_of_fame):
        assert hall_of_fame.players[0].player_id == "BreeDr00"

    def test_first_pos(self, hall_of_fame):
        assert hall_of_fame.players[0].pos == "QB"

    def test_first_year_induction(self, hall_of_fame):
        assert hall_of_fame.players[0].year_induction == 2026

    def test_first_career_av(self, hall_of_fame):
        assert hall_of_fame.players[0].career_av == 167

    def test_first_g(self, hall_of_fame):
        assert hall_of_fame.players[0].g == 287

    def test_first_pass_yds(self, hall_of_fame):
        assert hall_of_fame.players[0].pass_yds == 80358

    def test_first_pass_td(self, hall_of_fame):
        assert hall_of_fame.players[0].pass_td == 571

    def test_first_pro_bowls(self, hall_of_fame):
        assert hall_of_fame.players[0].pro_bowls == 13

    def test_first_sacks(self, hall_of_fame):
        assert hall_of_fame.players[0].sacks == 0.0

    # Defensive HOF player should have tackle/sack stats
    def test_defensive_hof_player(self, hall_of_fame):
        """Defensive HOF players should have defensive stats."""
        defenders = [
            p
            for p in hall_of_fame.players
            if p.pos in ("DE", "DT", "LB", "CB", "S", "DB")
        ]
        assert len(defenders) > 0
        first_def = defenders[0]
        assert (
            first_def.tackles_combined is not None
            or first_def.def_int is not None
            or first_def.sacks is not None
        )


# ---------------------------------------------------------------------------
# Pro Bowl parse -- smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestProBowlSmoke:
    """Smoke test: Pro Bowl fixture should parse without errors."""

    def test_parse_returns_dict(self, probowl_parsed):
        assert isinstance(probowl_parsed, dict)

    def test_parsed_data_has_all_keys(self, probowl_parsed):
        expected_keys = {"year", "players"}
        assert set(probowl_parsed.keys()) == expected_keys

    def test_model_validates_successfully(self, probowl_roster):
        assert isinstance(probowl_roster, ProBowlRoster)

    def test_year_is_set(self, probowl_roster):
        assert probowl_roster.year == 2024


# ---------------------------------------------------------------------------
# Pro Bowl players
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestProBowlPlayers:
    def test_player_count(self, probowl_roster):
        assert len(probowl_roster.players) == 115

    def test_player_is_model(self, probowl_roster):
        assert isinstance(probowl_roster.players[0], ProBowlPlayer)

    # First player: Lamar Jackson
    def test_first_player(self, probowl_roster):
        assert probowl_roster.players[0].player == "Lamar Jackson"

    def test_first_player_id(self, probowl_roster):
        assert probowl_roster.players[0].player_id == "JackLa00"

    def test_first_player_href(self, probowl_roster):
        assert probowl_roster.players[0].player_href == "/players/J/JackLa00.htm"

    def test_first_pos(self, probowl_roster):
        assert probowl_roster.players[0].pos == "QB"

    def test_first_conference(self, probowl_roster):
        assert probowl_roster.players[0].conference == "AFC"

    def test_first_team(self, probowl_roster):
        assert probowl_roster.players[0].team == "BAL"

    def test_first_is_starter(self, probowl_roster):
        assert probowl_roster.players[0].is_starter is True

    def test_first_did_not_play(self, probowl_roster):
        assert probowl_roster.players[0].did_not_play is True

    def test_first_is_replacement(self, probowl_roster):
        assert probowl_roster.players[0].is_replacement is False

    def test_first_age(self, probowl_roster):
        assert probowl_roster.players[0].age == 27

    def test_first_experience(self, probowl_roster):
        assert probowl_roster.players[0].experience == 6

    def test_first_pass_yds(self, probowl_roster):
        assert probowl_roster.players[0].pass_yds == 4172

    def test_first_pass_td(self, probowl_roster):
        assert probowl_roster.players[0].pass_td == 41

    def test_first_all_pro_string(self, probowl_roster):
        assert probowl_roster.players[0].all_pro_string is not None
        assert "AP: 1st Tm" in probowl_roster.players[0].all_pro_string

    # Replacement player
    def test_replacement_player_exists(self, probowl_roster):
        """Some Pro Bowl players are replacement selections."""
        replacements = [p for p in probowl_roster.players if p.is_replacement]
        assert len(replacements) > 0

    # Non-starter
    def test_non_starter_exists(self, probowl_roster):
        """Some Pro Bowl players are not starters."""
        non_starters = [p for p in probowl_roster.players if not p.is_starter]
        assert len(non_starters) > 0


# ---------------------------------------------------------------------------
# JSON serialization
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestJsonSerialization:
    def test_award_serializes(self, award_history):
        output = award_history.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert len(loaded["winners"]) == 70

    def test_award_round_trip(self, award_history):
        dumped = award_history.model_dump()
        assert len(dumped["winners"]) == 70
        assert dumped["award"] == "ap-nfl-mvp-award"

    def test_hof_serializes(self, hall_of_fame):
        output = hall_of_fame.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert len(loaded["players"]) == 332

    def test_probowl_serializes(self, probowl_roster):
        output = probowl_roster.model_dump_json()
        assert isinstance(output, str)
        loaded = json.loads(output)
        assert len(loaded["players"]) == 115


# ---------------------------------------------------------------------------
# Awards endpoint
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestAwardsEndpoint:
    def test_get_returns_model(self, award_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.awards.browserless,
            "get_page_content",
            return_value=award_html,
        ) as mock_fetch:
            result = pfr.awards.get(award="ap-nfl-mvp-award")

        mock_fetch.assert_called_once()
        assert isinstance(result, AwardHistory)
        assert len(result.winners) == 70

    def test_get_url_construction(self, award_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.awards.browserless,
            "get_page_content",
            return_value=award_html,
        ) as mock_fetch:
            pfr.awards.get(award="ap-nfl-mvp-award")

        url = mock_fetch.call_args[0][0]
        assert (
            url == "https://www.pro-football-reference.com/awards/ap-nfl-mvp-award.htm"
        )

    def test_get_wait_for_element(self, award_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.awards.browserless,
            "get_page_content",
            return_value=award_html,
        ) as mock_fetch:
            pfr.awards.get(award="ap-nfl-mvp-award")

        assert mock_fetch.call_args[1]["wait_for_element"] == "#awards"


# ---------------------------------------------------------------------------
# HOF endpoint
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestHofEndpoint:
    def test_list_returns_model(self, hof_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.hof.browserless,
            "get_page_content",
            return_value=hof_html,
        ) as mock_fetch:
            result = pfr.hof.list()

        mock_fetch.assert_called_once()
        assert isinstance(result, HallOfFame)
        assert len(result.players) == 332

    def test_list_url_construction(self, hof_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.hof.browserless,
            "get_page_content",
            return_value=hof_html,
        ) as mock_fetch:
            pfr.hof.list()

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/hof/"

    def test_list_wait_for_element(self, hof_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.hof.browserless,
            "get_page_content",
            return_value=hof_html,
        ) as mock_fetch:
            pfr.hof.list()

        assert mock_fetch.call_args[1]["wait_for_element"] == "#hof_players"


# ---------------------------------------------------------------------------
# Pro Bowl endpoint
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestProBowlEndpoint:
    def test_year_returns_model(self, probowl_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.probowl.browserless,
            "get_page_content",
            return_value=probowl_html,
        ) as mock_fetch:
            result = pfr.probowl.year(year=2024)

        mock_fetch.assert_called_once()
        assert isinstance(result, ProBowlRoster)
        assert len(result.players) == 115

    def test_year_url_construction(self, probowl_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.probowl.browserless,
            "get_page_content",
            return_value=probowl_html,
        ) as mock_fetch:
            pfr.probowl.year(year=2024)

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/years/2024/probowl.htm"

    def test_year_wait_for_element(self, probowl_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.probowl.browserless,
            "get_page_content",
            return_value=probowl_html,
        ) as mock_fetch:
            pfr.probowl.year(year=2024)

        assert mock_fetch.call_args[1]["wait_for_element"] == "#pro_bowl"


# ---------------------------------------------------------------------------
# Lazy loading
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestLazyLoading:
    def test_awards_in_sub_sdk_map(self):
        pfr = GriddyPFR()
        assert "awards" in pfr._sub_sdk_map

    def test_awards_is_cached(self):
        pfr = GriddyPFR()
        assert pfr.awards is pfr.awards

    def test_hof_in_sub_sdk_map(self):
        pfr = GriddyPFR()
        assert "hof" in pfr._sub_sdk_map

    def test_hof_is_cached(self):
        pfr = GriddyPFR()
        assert pfr.hof is pfr.hof

    def test_probowl_in_sub_sdk_map(self):
        pfr = GriddyPFR()
        assert "probowl" in pfr._sub_sdk_map

    def test_probowl_is_cached(self):
        pfr = GriddyPFR()
        assert pfr.probowl is pfr.probowl
