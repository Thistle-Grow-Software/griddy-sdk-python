"""Tests for griddy.pfr.endpoints.schedule module."""

from pathlib import Path
from unittest.mock import patch

import pytest

from griddy.pfr import GriddyPFR
from griddy.pfr.models.entities.schedule_game import ScheduleGame

FIXTURE_PATH = Path(__file__).resolve().parents[2] / "pfr_2015_sked.html"


@pytest.fixture
def schedule_html() -> str:
    """Load the 2015 PFR schedule HTML fixture."""
    return FIXTURE_PATH.read_text()


@pytest.mark.unit
class TestScheduleEndpoint:
    def test_get_season_schedule_returns_games(self, schedule_html: str):
        pfr = GriddyPFR()
        with patch.object(
            pfr.schedule.browserless,
            "get_page_content",
            return_value=schedule_html,
        ) as mock_fetch:
            games = pfr.schedule.get_season_schedule(season=2015)

        mock_fetch.assert_called_once()
        call_args = mock_fetch.call_args
        assert "2015" in call_args[0][0]
        assert call_args[1]["wait_for_element"] == "#games"
        assert isinstance(games, list)
        assert len(games) == 267
        assert isinstance(games[0], ScheduleGame)

    def test_get_season_schedule_first_game(self, schedule_html: str):
        pfr = GriddyPFR()
        with patch.object(
            pfr.schedule.browserless,
            "get_page_content",
            return_value=schedule_html,
        ):
            games = pfr.schedule.get_season_schedule(season=2015)

        first = games[0]
        assert first.week_num == "1"
        assert first.winner == "New England Patriots"
        assert first.pts_win == 28

    def test_get_season_schedule_url_construction(self, schedule_html: str):
        pfr = GriddyPFR()
        with patch.object(
            pfr.schedule.browserless,
            "get_page_content",
            return_value=schedule_html,
        ) as mock_fetch:
            pfr.schedule.get_season_schedule(season=2024)

        url = mock_fetch.call_args[0][0]
        assert url == "https://www.pro-football-reference.com/years/2024/games.htm"

    def test_lazy_loading_of_schedule(self):
        """Verify schedule sub-SDK is lazily loaded via _sub_sdk_map."""
        pfr = GriddyPFR()
        assert "schedule" in pfr._sub_sdk_map
        # Accessing .schedule should not raise
        assert pfr.schedule is not None
        # Second access should return the same cached instance
        assert pfr.schedule is pfr.schedule
