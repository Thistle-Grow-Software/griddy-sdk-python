"""Tests for PFR Fantasy Rankings endpoints.

Covers:
- Top Fantasy Players (``/years/{year}/fantasy.htm``)
- Fantasy Matchups (``/fantasy/{position}-fantasy-matchups.htm``)
"""

from unittest.mock import patch

import pytest

from griddy.pfr.models import (
    FantasyMatchupPlayer,
    FantasyMatchups,
    FantasyPlayer,
    FantasyPointsAllowed,
    FantasyPointsAllowedTeam,
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


# #########################################################################
# MATCHUPS TESTS
# #########################################################################

# -------------------------------------------------------------------------
# Matchup fixtures
# -------------------------------------------------------------------------


@pytest.fixture(scope="module")
def qb_matchups_html() -> str:
    return (FIXTURE_DIR / "qb_matchups.htm").read_text()


@pytest.fixture(scope="module")
def wr_matchups_html() -> str:
    return (FIXTURE_DIR / "wr_matchups.htm").read_text()


@pytest.fixture(scope="module")
def rb_matchups_html() -> str:
    return (FIXTURE_DIR / "rb_matchups.htm").read_text()


@pytest.fixture(scope="module")
def te_matchups_html() -> str:
    return (FIXTURE_DIR / "te_matchups.htm").read_text()


@pytest.fixture(scope="module")
def qb_matchups_parsed(qb_matchups_html: str) -> dict:
    return _parser.parse_matchups(qb_matchups_html)


@pytest.fixture(scope="module")
def wr_matchups_parsed(wr_matchups_html: str) -> dict:
    return _parser.parse_matchups(wr_matchups_html)


@pytest.fixture(scope="module")
def rb_matchups_parsed(rb_matchups_html: str) -> dict:
    return _parser.parse_matchups(rb_matchups_html)


@pytest.fixture(scope="module")
def te_matchups_parsed(te_matchups_html: str) -> dict:
    return _parser.parse_matchups(te_matchups_html)


@pytest.fixture(scope="module")
def qb_matchups_model(qb_matchups_parsed: dict) -> FantasyMatchups:
    return FantasyMatchups.model_validate(qb_matchups_parsed)


@pytest.fixture(scope="module")
def wr_matchups_model(wr_matchups_parsed: dict) -> FantasyMatchups:
    return FantasyMatchups.model_validate(wr_matchups_parsed)


@pytest.fixture(scope="module")
def rb_matchups_model(rb_matchups_parsed: dict) -> FantasyMatchups:
    return FantasyMatchups.model_validate(rb_matchups_parsed)


@pytest.fixture(scope="module")
def te_matchups_model(te_matchups_parsed: dict) -> FantasyMatchups:
    return FantasyMatchups.model_validate(te_matchups_parsed)


# =========================================================================
# Matchup smoke tests
# =========================================================================


@pytest.mark.unit
class TestMatchupsSmoke:
    def test_qb_parse_returns_dict(self, qb_matchups_parsed):
        assert isinstance(qb_matchups_parsed, dict)
        assert "players" in qb_matchups_parsed

    def test_wr_parse_returns_dict(self, wr_matchups_parsed):
        assert isinstance(wr_matchups_parsed, dict)
        assert "players" in wr_matchups_parsed

    def test_rb_parse_returns_dict(self, rb_matchups_parsed):
        assert isinstance(rb_matchups_parsed, dict)
        assert "players" in rb_matchups_parsed

    def test_te_parse_returns_dict(self, te_matchups_parsed):
        assert isinstance(te_matchups_parsed, dict)
        assert "players" in te_matchups_parsed

    def test_qb_model_validates(self, qb_matchups_model):
        assert isinstance(qb_matchups_model, FantasyMatchups)

    def test_qb_player_count(self, qb_matchups_model):
        assert len(qb_matchups_model.players) == 67

    def test_wr_player_count(self, wr_matchups_model):
        assert len(wr_matchups_model.players) == 161

    def test_rb_player_count(self, rb_matchups_model):
        assert len(rb_matchups_model.players) == 101

    def test_te_player_count(self, te_matchups_model):
        assert len(te_matchups_model.players) == 98


# =========================================================================
# QB matchup — first player (Jalen Hurts)
# =========================================================================


@pytest.mark.unit
class TestQBMatchupFirstPlayer:
    def test_identity(self, qb_matchups_model):
        first = qb_matchups_model.players[0]
        assert isinstance(first, FantasyMatchupPlayer)
        assert first.player == "Jalen Hurts"
        assert first.player_href == "/players/H/HurtJa00.htm"
        assert first.player_id == "HurtJa00"

    def test_team(self, qb_matchups_model):
        first = qb_matchups_model.players[0]
        assert first.team == "PHI"
        assert first.team_href == "/teams/phi/2025.htm"

    def test_games(self, qb_matchups_model):
        first = qb_matchups_model.players[0]
        assert first.g == 15
        assert first.gs == 15

    def test_snaps(self, qb_matchups_model):
        first = qb_matchups_model.players[0]
        assert first.snaps == "1190 (92.11%)"

    def test_passing(self, qb_matchups_model):
        first = qb_matchups_model.players[0]
        assert first.pass_cmp == pytest.approx(16.5)
        assert first.pass_att == pytest.approx(24.1)
        assert first.pass_yds == pytest.approx(193.5)
        assert first.pass_td == pytest.approx(1.2)
        assert first.pass_int == pytest.approx(0.3)
        assert first.pass_sacked == pytest.approx(2.5)

    def test_rushing(self, qb_matchups_model):
        first = qb_matchups_model.players[0]
        assert first.rush_att == pytest.approx(10.0)
        assert first.rush_yds == pytest.approx(42.0)
        assert first.rush_td == pytest.approx(0.9)

    def test_fantasy_per_game(self, qb_matchups_model):
        first = qb_matchups_model.players[0]
        assert first.fantasy_points_per_game == pytest.approx(21.0)
        assert first.draftkings_points_per_game == pytest.approx(21.9)
        assert first.fanduel_points_per_game == pytest.approx(21.3)

    def test_matchup(self, qb_matchups_model):
        first = qb_matchups_model.players[0]
        assert first.opp == "DAL"
        assert first.opp_href == "/teams/dal/2025.htm"
        assert first.rank == 32

    def test_opp_fantasy_allowed(self, qb_matchups_model):
        first = qb_matchups_model.players[0]
        assert first.opp_fantasy_points_per_game == pytest.approx(20.9)
        assert first.opp_draftkings_points_per_game == pytest.approx(22.5)
        assert first.opp_fanduel_points_per_game == pytest.approx(21.7)

    def test_proj_ranks(self, qb_matchups_model):
        first = qb_matchups_model.players[0]
        assert first.fantasy_points_proj_rank == 1
        assert first.draftkings_points_proj_rank == 2
        assert first.fanduel_points_proj_rank == 2

    def test_qb_has_no_receiving(self, qb_matchups_model):
        first = qb_matchups_model.players[0]
        assert first.targets is None
        assert first.rec is None
        assert first.rec_yds is None
        assert first.rec_td is None


# =========================================================================
# WR matchup — first player (Ja'Marr Chase)
# =========================================================================


@pytest.mark.unit
class TestWRMatchupFirstPlayer:
    def test_identity(self, wr_matchups_model):
        first = wr_matchups_model.players[0]
        assert first.player == "Ja'Marr Chase"
        assert first.player_id == "ChasJa00"

    def test_receiving(self, wr_matchups_model):
        first = wr_matchups_model.players[0]
        assert first.targets == pytest.approx(10.3)
        assert first.rec == pytest.approx(7.5)
        assert first.rec_yds == pytest.approx(100.5)
        assert first.rec_td == pytest.approx(1.0)

    def test_wr_has_no_passing(self, wr_matchups_model):
        first = wr_matchups_model.players[0]
        assert first.pass_cmp is None
        assert first.pass_att is None
        assert first.pass_yds is None
        assert first.pass_td is None
        assert first.pass_int is None
        assert first.pass_sacked is None

    def test_wr_has_no_rushing(self, wr_matchups_model):
        first = wr_matchups_model.players[0]
        assert first.rush_att is None
        assert first.rush_yds is None
        assert first.rush_td is None

    def test_fantasy_per_game(self, wr_matchups_model):
        first = wr_matchups_model.players[0]
        assert first.fantasy_points_per_game == pytest.approx(16.2)
        assert first.draftkings_points_per_game == pytest.approx(24.6)
        assert first.fanduel_points_per_game == pytest.approx(20.0)


# =========================================================================
# RB matchup — first player (Saquon Barkley)
# =========================================================================


@pytest.mark.unit
class TestRBMatchupFirstPlayer:
    def test_identity(self, rb_matchups_model):
        first = rb_matchups_model.players[0]
        assert first.player == "Saquon Barkley"
        assert first.player_id == "BarkSa00"

    def test_rushing(self, rb_matchups_model):
        first = rb_matchups_model.players[0]
        assert first.rush_att == pytest.approx(21.6)
        assert first.rush_yds == pytest.approx(125.3)
        assert first.rush_td == pytest.approx(0.8)

    def test_receiving(self, rb_matchups_model):
        first = rb_matchups_model.players[0]
        assert first.targets == pytest.approx(2.7)
        assert first.rec == pytest.approx(2.1)
        assert first.rec_yds == pytest.approx(17.4)
        assert first.rec_td == pytest.approx(0.1)

    def test_rb_has_no_passing(self, rb_matchups_model):
        first = rb_matchups_model.players[0]
        assert first.pass_cmp is None
        assert first.pass_att is None


# =========================================================================
# TE matchup — first player (George Kittle)
# =========================================================================


@pytest.mark.unit
class TestTEMatchupFirstPlayer:
    def test_identity(self, te_matchups_model):
        first = te_matchups_model.players[0]
        assert first.player == "George Kittle"
        assert first.player_id == "KittGe00"

    def test_receiving(self, te_matchups_model):
        first = te_matchups_model.players[0]
        assert first.targets == pytest.approx(6.3)
        assert first.rec == pytest.approx(5.2)
        assert first.rec_yds == pytest.approx(73.7)
        assert first.rec_td == pytest.approx(0.5)

    def test_matchup(self, te_matchups_model):
        first = te_matchups_model.players[0]
        assert first.opp == "SEA"
        assert first.rank == 13


# =========================================================================
# Matchup JSON serialization
# =========================================================================


@pytest.mark.unit
class TestMatchupsJsonSerialization:
    def test_roundtrip(self, qb_matchups_model):
        data = qb_matchups_model.model_dump()
        rebuilt = FantasyMatchups.model_validate(data)
        assert len(rebuilt.players) == len(qb_matchups_model.players)

    def test_data_preserved(self, qb_matchups_model):
        data = qb_matchups_model.model_dump()
        rebuilt = FantasyMatchups.model_validate(data)
        assert rebuilt.players[0].player == "Jalen Hurts"
        assert rebuilt.players[0].pass_yds == pytest.approx(193.5)


# =========================================================================
# Matchup endpoint integration tests (mocked)
# =========================================================================


@pytest.mark.unit
class TestGetMatchupsEndpoint:
    def test_returns_model(self, qb_matchups_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.fantasy.browserless,
            "get_page_content",
            return_value=qb_matchups_html,
        ) as mock_fetch:
            result = pfr.fantasy.get_matchups(position="qb")

        mock_fetch.assert_called_once()
        assert isinstance(result, FantasyMatchups)
        assert len(result.players) == 67

    def test_url_construction(self, qb_matchups_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.fantasy.browserless,
            "get_page_content",
            return_value=qb_matchups_html,
        ) as mock_fetch:
            pfr.fantasy.get_matchups(position="qb")

        call_args = mock_fetch.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get("url", "")
        assert "/fantasy/qb-fantasy-matchups.htm" in url

    def test_wait_for_element(self, qb_matchups_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.fantasy.browserless,
            "get_page_content",
            return_value=qb_matchups_html,
        ) as mock_fetch:
            pfr.fantasy.get_matchups(position="qb")

        call_args = mock_fetch.call_args
        wait_for = (
            call_args[1].get("wait_for_element") if call_args[1] else call_args[0][1]
        )
        assert wait_for == "#fantasy_stats"

    def test_rb_position_url(self, rb_matchups_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.fantasy.browserless,
            "get_page_content",
            return_value=rb_matchups_html,
        ) as mock_fetch:
            pfr.fantasy.get_matchups(position="rb")

        call_args = mock_fetch.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get("url", "")
        assert "/fantasy/rb-fantasy-matchups.htm" in url


# #########################################################################
# POINTS ALLOWED TESTS
# #########################################################################

# -------------------------------------------------------------------------
# Points allowed fixtures
# -------------------------------------------------------------------------


@pytest.fixture(scope="module")
def qb_points_allowed_html() -> str:
    return (FIXTURE_DIR / "qb_points_allowed.htm").read_text()


@pytest.fixture(scope="module")
def wr_points_allowed_html() -> str:
    return (FIXTURE_DIR / "wr_points_allowed.htm").read_text()


@pytest.fixture(scope="module")
def rb_points_allowed_html() -> str:
    return (FIXTURE_DIR / "rb_points_allowed.htm").read_text()


@pytest.fixture(scope="module")
def te_points_allowed_html() -> str:
    return (FIXTURE_DIR / "te_points_allowed.htm").read_text()


@pytest.fixture(scope="module")
def qb_points_allowed_parsed(qb_points_allowed_html: str) -> dict:
    return _parser.parse_points_allowed(qb_points_allowed_html)


@pytest.fixture(scope="module")
def wr_points_allowed_parsed(wr_points_allowed_html: str) -> dict:
    return _parser.parse_points_allowed(wr_points_allowed_html)


@pytest.fixture(scope="module")
def rb_points_allowed_parsed(rb_points_allowed_html: str) -> dict:
    return _parser.parse_points_allowed(rb_points_allowed_html)


@pytest.fixture(scope="module")
def te_points_allowed_parsed(te_points_allowed_html: str) -> dict:
    return _parser.parse_points_allowed(te_points_allowed_html)


@pytest.fixture(scope="module")
def qb_points_allowed_model(qb_points_allowed_parsed: dict) -> FantasyPointsAllowed:
    return FantasyPointsAllowed.model_validate(qb_points_allowed_parsed)


@pytest.fixture(scope="module")
def wr_points_allowed_model(wr_points_allowed_parsed: dict) -> FantasyPointsAllowed:
    return FantasyPointsAllowed.model_validate(wr_points_allowed_parsed)


@pytest.fixture(scope="module")
def rb_points_allowed_model(rb_points_allowed_parsed: dict) -> FantasyPointsAllowed:
    return FantasyPointsAllowed.model_validate(rb_points_allowed_parsed)


@pytest.fixture(scope="module")
def te_points_allowed_model(te_points_allowed_parsed: dict) -> FantasyPointsAllowed:
    return FantasyPointsAllowed.model_validate(te_points_allowed_parsed)


# =========================================================================
# Points allowed smoke tests
# =========================================================================


@pytest.mark.unit
class TestPointsAllowedSmoke:
    def test_qb_parse_returns_dict(self, qb_points_allowed_parsed):
        assert isinstance(qb_points_allowed_parsed, dict)
        assert "teams" in qb_points_allowed_parsed

    def test_wr_parse_returns_dict(self, wr_points_allowed_parsed):
        assert isinstance(wr_points_allowed_parsed, dict)
        assert "teams" in wr_points_allowed_parsed

    def test_rb_parse_returns_dict(self, rb_points_allowed_parsed):
        assert isinstance(rb_points_allowed_parsed, dict)
        assert "teams" in rb_points_allowed_parsed

    def test_te_parse_returns_dict(self, te_points_allowed_parsed):
        assert isinstance(te_points_allowed_parsed, dict)
        assert "teams" in te_points_allowed_parsed

    def test_qb_model_validates(self, qb_points_allowed_model):
        assert isinstance(qb_points_allowed_model, FantasyPointsAllowed)

    def test_qb_team_count(self, qb_points_allowed_model):
        assert len(qb_points_allowed_model.teams) == 32

    def test_wr_team_count(self, wr_points_allowed_model):
        assert len(wr_points_allowed_model.teams) == 32

    def test_rb_team_count(self, rb_points_allowed_model):
        assert len(rb_points_allowed_model.teams) == 32

    def test_te_team_count(self, te_points_allowed_model):
        assert len(te_points_allowed_model.teams) == 32


# =========================================================================
# QB points allowed — first team (Dallas Cowboys)
# =========================================================================


@pytest.mark.unit
class TestQBPointsAllowedFirstTeam:
    def test_identity(self, qb_points_allowed_model):
        first = qb_points_allowed_model.teams[0]
        assert isinstance(first, FantasyPointsAllowedTeam)
        assert first.team == "Dallas Cowboys"
        assert first.team_href == "/teams/dal/2025.htm"

    def test_games(self, qb_points_allowed_model):
        first = qb_points_allowed_model.teams[0]
        assert first.g == 17

    def test_passing(self, qb_points_allowed_model):
        first = qb_points_allowed_model.teams[0]
        assert first.pass_cmp == 381
        assert first.pass_att == 555
        assert first.pass_yds == 4521
        assert first.pass_td == 35
        assert first.pass_int == 6

    def test_scoring_and_sacked(self, qb_points_allowed_model):
        first = qb_points_allowed_model.teams[0]
        assert first.two_pt_pass == 2
        assert first.pass_sacked == 34

    def test_rushing(self, qb_points_allowed_model):
        first = qb_points_allowed_model.teams[0]
        assert first.rush_att == 88
        assert first.rush_yds == 398
        assert first.rush_td == 8

    def test_fantasy_totals(self, qb_points_allowed_model):
        first = qb_points_allowed_model.teams[0]
        assert first.fantasy_points == pytest.approx(397.04)
        assert first.draftkings_points == pytest.approx(416.6)
        assert first.fanduel_points == pytest.approx(402.6)

    def test_fantasy_per_game(self, qb_points_allowed_model):
        first = qb_points_allowed_model.teams[0]
        assert first.fantasy_points_per_game == pytest.approx(23.4)
        assert first.draftkings_points_per_game == pytest.approx(24.5)
        assert first.fanduel_points_per_game == pytest.approx(23.7)

    def test_qb_has_no_receiving(self, qb_points_allowed_model):
        first = qb_points_allowed_model.teams[0]
        assert first.targets is None
        assert first.rec is None
        assert first.rec_yds is None
        assert first.rec_td is None


# =========================================================================
# WR points allowed — first team (Dallas Cowboys)
# =========================================================================


@pytest.mark.unit
class TestWRPointsAllowedFirstTeam:
    def test_identity(self, wr_points_allowed_model):
        first = wr_points_allowed_model.teams[0]
        assert first.team == "Dallas Cowboys"
        assert first.team_href == "/teams/dal/2025.htm"

    def test_games(self, wr_points_allowed_model):
        first = wr_points_allowed_model.teams[0]
        assert first.g == 17

    def test_receiving(self, wr_points_allowed_model):
        first = wr_points_allowed_model.teams[0]
        assert first.targets == 302
        assert first.rec == 206
        assert first.rec_yds == 2907
        assert first.rec_td == 26

    def test_fantasy_totals(self, wr_points_allowed_model):
        first = wr_points_allowed_model.teams[0]
        assert first.fantasy_points == pytest.approx(460.30)
        assert first.draftkings_points == pytest.approx(685.3)
        assert first.fanduel_points == pytest.approx(563.3)

    def test_fantasy_per_game(self, wr_points_allowed_model):
        first = wr_points_allowed_model.teams[0]
        assert first.fantasy_points_per_game == pytest.approx(27.1)
        assert first.draftkings_points_per_game == pytest.approx(40.3)
        assert first.fanduel_points_per_game == pytest.approx(33.1)

    def test_wr_has_no_passing(self, wr_points_allowed_model):
        first = wr_points_allowed_model.teams[0]
        assert first.pass_cmp is None
        assert first.pass_att is None
        assert first.pass_yds is None
        assert first.pass_td is None
        assert first.pass_int is None
        assert first.pass_sacked is None

    def test_wr_has_no_rushing(self, wr_points_allowed_model):
        first = wr_points_allowed_model.teams[0]
        assert first.rush_att is None
        assert first.rush_yds is None
        assert first.rush_td is None


# =========================================================================
# RB points allowed — first team (New York Jets)
# =========================================================================


@pytest.mark.unit
class TestRBPointsAllowedFirstTeam:
    def test_identity(self, rb_points_allowed_model):
        first = rb_points_allowed_model.teams[0]
        assert first.team == "New York Jets"
        assert first.team_href == "/teams/nyj/2025.htm"

    def test_games(self, rb_points_allowed_model):
        first = rb_points_allowed_model.teams[0]
        assert first.g == 17

    def test_rushing(self, rb_points_allowed_model):
        first = rb_points_allowed_model.teams[0]
        assert first.rush_att == 430
        assert first.rush_yds == 1873
        assert first.rush_td == 17

    def test_receiving(self, rb_points_allowed_model):
        first = rb_points_allowed_model.teams[0]
        assert first.targets == 80
        assert first.rec == 62
        assert first.rec_yds == 587
        assert first.rec_td == 11

    def test_fantasy_totals(self, rb_points_allowed_model):
        first = rb_points_allowed_model.teams[0]
        assert first.fantasy_points == pytest.approx(414.30)
        assert first.draftkings_points == pytest.approx(491.0)
        assert first.fanduel_points == pytest.approx(445.0)

    def test_fantasy_per_game(self, rb_points_allowed_model):
        first = rb_points_allowed_model.teams[0]
        assert first.fantasy_points_per_game == pytest.approx(24.4)
        assert first.draftkings_points_per_game == pytest.approx(28.9)
        assert first.fanduel_points_per_game == pytest.approx(26.2)

    def test_rb_has_no_passing(self, rb_points_allowed_model):
        first = rb_points_allowed_model.teams[0]
        assert first.pass_cmp is None
        assert first.pass_att is None


# =========================================================================
# TE points allowed — first team (Cincinnati Bengals)
# =========================================================================


@pytest.mark.unit
class TestTEPointsAllowedFirstTeam:
    def test_identity(self, te_points_allowed_model):
        first = te_points_allowed_model.teams[0]
        assert first.team == "Cincinnati Bengals"
        assert first.team_href == "/teams/cin/2025.htm"

    def test_games(self, te_points_allowed_model):
        first = te_points_allowed_model.teams[0]
        assert first.g == 17

    def test_receiving(self, te_points_allowed_model):
        first = te_points_allowed_model.teams[0]
        assert first.targets == 165
        assert first.rec == 116
        assert first.rec_yds == 1444
        assert first.rec_td == 16

    def test_fantasy_totals(self, te_points_allowed_model):
        first = te_points_allowed_model.teams[0]
        assert first.fantasy_points == pytest.approx(239.00)
        assert first.draftkings_points == pytest.approx(366.0)
        assert first.fanduel_points == pytest.approx(297.0)

    def test_fantasy_per_game(self, te_points_allowed_model):
        first = te_points_allowed_model.teams[0]
        assert first.fantasy_points_per_game == pytest.approx(14.1)
        assert first.draftkings_points_per_game == pytest.approx(21.5)
        assert first.fanduel_points_per_game == pytest.approx(17.5)


# =========================================================================
# Points allowed JSON serialization
# =========================================================================


@pytest.mark.unit
class TestPointsAllowedJsonSerialization:
    def test_roundtrip(self, qb_points_allowed_model):
        data = qb_points_allowed_model.model_dump()
        rebuilt = FantasyPointsAllowed.model_validate(data)
        assert len(rebuilt.teams) == len(qb_points_allowed_model.teams)

    def test_data_preserved(self, qb_points_allowed_model):
        data = qb_points_allowed_model.model_dump()
        rebuilt = FantasyPointsAllowed.model_validate(data)
        assert rebuilt.teams[0].team == "Dallas Cowboys"
        assert rebuilt.teams[0].pass_yds == 4521
        assert rebuilt.teams[0].fantasy_points == pytest.approx(397.04)


# =========================================================================
# Points allowed endpoint integration tests (mocked)
# =========================================================================


@pytest.mark.unit
class TestGetPointsAllowedEndpoint:
    def test_returns_model(self, qb_points_allowed_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.fantasy.browserless,
            "get_page_content",
            return_value=qb_points_allowed_html,
        ) as mock_fetch:
            result = pfr.fantasy.get_points_allowed(year=2025, position="qb")

        mock_fetch.assert_called_once()
        assert isinstance(result, FantasyPointsAllowed)
        assert len(result.teams) == 32

    def test_url_construction(self, qb_points_allowed_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.fantasy.browserless,
            "get_page_content",
            return_value=qb_points_allowed_html,
        ) as mock_fetch:
            pfr.fantasy.get_points_allowed(year=2025, position="qb")

        call_args = mock_fetch.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get("url", "")
        assert "/years/2025/fantasy-points-against-qb.htm" in url

    def test_wait_for_element(self, qb_points_allowed_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.fantasy.browserless,
            "get_page_content",
            return_value=qb_points_allowed_html,
        ) as mock_fetch:
            pfr.fantasy.get_points_allowed(year=2025, position="qb")

        call_args = mock_fetch.call_args
        wait_for = (
            call_args[1].get("wait_for_element") if call_args[1] else call_args[0][1]
        )
        assert wait_for == "#fantasy_def"

    def test_te_position_url(self, te_points_allowed_html):
        pfr = GriddyPFR()
        with patch.object(
            pfr.fantasy.browserless,
            "get_page_content",
            return_value=te_points_allowed_html,
        ) as mock_fetch:
            pfr.fantasy.get_points_allowed(year=2025, position="te")

        call_args = mock_fetch.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get("url", "")
        assert "/years/2025/fantasy-points-against-te.htm" in url
