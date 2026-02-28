"""Tests for PFR Fantasy Rankings endpoints.

Covers:
- Top Fantasy Players (``/years/{year}/fantasy.htm``)
"""

from unittest.mock import patch

import pytest

from griddy.pfr.models import (
    FantasyPlayer,
    TopFantasyPlayers,
)
from griddy.pfr.parsers.fantasy import FantasyParser
from griddy.pfr.sdk import GriddyPFR
from griddy.settings import FIXTURE_DIR

FIXTURE_DIR = FIXTURE_DIR / "pfr" / "fantasy"

_parser = FantasyParser()

# -------------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------------


@pytest.fixture(scope="module")
def top_players_html() -> str:
    return (FIXTURE_DIR / "top_players_2025.htm").read_text()


@pytest.fixture(scope="module")
def top_players_parsed(top_players_html: str) -> dict:
    return _parser.parse_top_players(top_players_html)


@pytest.fixture(scope="module")
def top_players_model(top_players_parsed: dict) -> TopFantasyPlayers:
    return TopFantasyPlayers.model_validate(top_players_parsed)


# =========================================================================
# Smoke tests
# =========================================================================


@pytest.mark.unit
class TestTopPlayersSmoke:
    def test_parse_returns_dict(self, top_players_parsed):
        assert isinstance(top_players_parsed, dict)

    def test_has_players_key(self, top_players_parsed):
        assert "players" in top_players_parsed

    def test_model_validates(self, top_players_model):
        assert isinstance(top_players_model, TopFantasyPlayers)

    def test_player_count(self, top_players_model):
        assert len(top_players_model.players) == 643


# =========================================================================
# Row data — First player (Jonathan Taylor, RB)
# =========================================================================


@pytest.mark.unit
class TestFirstPlayer:
    def test_identity(self, top_players_model):
        first = top_players_model.players[0]
        assert isinstance(first, FantasyPlayer)
        assert first.rank == 1
        assert first.player == "Jonathan Taylor*"
        assert first.player_href == "/players/T/TaylJo02.htm"
        assert first.player_id == "TaylJo02"

    def test_team(self, top_players_model):
        first = top_players_model.players[0]
        assert first.team == "IND"
        assert first.team_href == "/teams/clt/2025.htm"

    def test_position_and_age(self, top_players_model):
        first = top_players_model.players[0]
        assert first.fantasy_pos == "RB"
        assert first.age == 26

    def test_games(self, top_players_model):
        first = top_players_model.players[0]
        assert first.g == 17
        assert first.gs == 17

    def test_passing_zeros(self, top_players_model):
        first = top_players_model.players[0]
        assert first.pass_cmp == 0
        assert first.pass_att == 0
        assert first.pass_yds == 0
        assert first.pass_td == 0
        assert first.pass_int == 0

    def test_rushing(self, top_players_model):
        first = top_players_model.players[0]
        assert first.rush_att == 323
        assert first.rush_yds == 1585
        assert first.rush_yds_per_att == pytest.approx(4.91)
        assert first.rush_td == 18

    def test_receiving(self, top_players_model):
        first = top_players_model.players[0]
        assert first.targets == 55
        assert first.rec == 46
        assert first.rec_yds == 378
        assert first.rec_yds_per_rec == pytest.approx(8.22)
        assert first.rec_td == 2

    def test_fumbles(self, top_players_model):
        first = top_players_model.players[0]
        assert first.fumbles == 2
        assert first.fumbles_lost == 1

    def test_scoring(self, top_players_model):
        first = top_players_model.players[0]
        assert first.all_td == 20
        assert first.two_pt_md == 1

    def test_fantasy_points(self, top_players_model):
        first = top_players_model.players[0]
        assert first.fantasy_points == pytest.approx(316.0)
        assert first.fantasy_points_ppr == pytest.approx(362.3)
        assert first.draftkings_points == pytest.approx(369.3)
        assert first.fanduel_points == pytest.approx(339.3)

    def test_fantasy_rankings(self, top_players_model):
        first = top_players_model.players[0]
        assert first.vbd == 158
        assert first.fantasy_rank_pos == 1
        assert first.fantasy_rank_overall == 1


# =========================================================================
# Row data — QB (Josh Allen, #10)
# =========================================================================


@pytest.mark.unit
class TestQBPlayer:
    def test_josh_allen_identity(self, top_players_model):
        allen = top_players_model.players[9]
        assert allen.rank == 10
        assert allen.player == "Josh Allen*"
        assert allen.player_id == "AlleJo02"
        assert allen.fantasy_pos == "QB"

    def test_josh_allen_passing(self, top_players_model):
        allen = top_players_model.players[9]
        assert allen.pass_cmp == 319
        assert allen.pass_att == 460
        assert allen.pass_yds == 3668
        assert allen.pass_td == 25
        assert allen.pass_int == 10

    def test_josh_allen_rushing(self, top_players_model):
        allen = top_players_model.players[9]
        assert allen.rush_att == 112
        assert allen.rush_yds == 579
        assert allen.rush_td == 14

    def test_josh_allen_fantasy(self, top_players_model):
        allen = top_players_model.players[9]
        assert allen.fantasy_points == pytest.approx(365.0)
        assert allen.fantasy_rank_pos == 1
        assert allen.fantasy_rank_overall == 10


# =========================================================================
# Row data — TE (Trey McBride, #12)
# =========================================================================


@pytest.mark.unit
class TestTEPlayer:
    def test_trey_mcbride_identity(self, top_players_model):
        mcbride = top_players_model.players[11]
        assert mcbride.rank == 12
        assert mcbride.player == "Trey McBride*+"
        assert mcbride.fantasy_pos == "TE"

    def test_trey_mcbride_receiving(self, top_players_model):
        mcbride = top_players_model.players[11]
        assert mcbride.targets == 169
        assert mcbride.rec == 126
        assert mcbride.rec_yds == 1239
        assert mcbride.rec_td == 11


# =========================================================================
# JSON serialization
# =========================================================================


@pytest.mark.unit
class TestJsonSerialization:
    def test_roundtrip(self, top_players_model):
        data = top_players_model.model_dump()
        rebuilt = TopFantasyPlayers.model_validate(data)
        assert len(rebuilt.players) == len(top_players_model.players)

    def test_data_preserved(self, top_players_model):
        data = top_players_model.model_dump()
        rebuilt = TopFantasyPlayers.model_validate(data)
        assert rebuilt.players[0].player == "Jonathan Taylor*"
        assert rebuilt.players[0].rush_yds == 1585
        assert rebuilt.players[0].fantasy_points == pytest.approx(316.0)


# =========================================================================
# Endpoint integration tests (mocked)
# =========================================================================


@pytest.mark.unit
class TestGetTopPlayersEndpoint:
    def test_returns_model(self, top_players_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.fantasy.browserless,
            "get_page_content",
            return_value=top_players_html,
        ) as mock_fetch:
            result = pfr.fantasy.get_top_players(year=2025)

        mock_fetch.assert_called_once()
        assert isinstance(result, TopFantasyPlayers)
        assert len(result.players) == 643

    def test_url_construction(self, top_players_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.fantasy.browserless,
            "get_page_content",
            return_value=top_players_html,
        ) as mock_fetch:
            pfr.fantasy.get_top_players(year=2025)

        call_args = mock_fetch.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get("url", "")
        assert "/years/2025/fantasy.htm" in url

    def test_wait_for_element(self, top_players_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.fantasy.browserless,
            "get_page_content",
            return_value=top_players_html,
        ) as mock_fetch:
            pfr.fantasy.get_top_players(year=2025)

        call_args = mock_fetch.call_args
        wait_for = (
            call_args[1].get("wait_for_element") if call_args[1] else call_args[0][1]
        )
        assert wait_for == "#fantasy"


# =========================================================================
# Lazy loading
# =========================================================================


@pytest.mark.unit
class TestLazyLoading:
    def test_fantasy_in_sub_sdk_map(self):
        assert "fantasy" in GriddyPFR._sub_sdk_map

    def test_fantasy_lazy_load(self):
        pfr = GriddyPFR()
        from griddy.pfr.endpoints.fantasy import Fantasy

        assert isinstance(pfr.fantasy, Fantasy)

    def test_fantasy_cached(self):
        pfr = GriddyPFR()
        assert pfr.fantasy is pfr.fantasy
