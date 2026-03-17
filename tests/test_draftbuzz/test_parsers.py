"""Tests for griddy.draftbuzz.parsers module."""

import pytest

from griddy.draftbuzz.errors.parsing_error import ParsingError
from griddy.draftbuzz.parsers import ProspectProfileParser, RankingsParser

# ---------------------------------------------------------------------------
# HTML Fixtures
# ---------------------------------------------------------------------------

PROSPECT_PROFILE_HTML = """
<html>
<body>
<span class="player-info__first-name">Cam</span>
<span class="player-info__last-name">Ward</span>
<div class="player-info-details">
    <div class="player-info-details__item">
        <h6 class="player-info-details__title">Position</h6>
        <div class="player-info-details__value">QB</div>
    </div>
    <div class="player-info-details__item">
        <h6 class="player-info-details__title">College</h6>
        <div class="player-info-details__value">Miami</div>
    </div>
    <div class="player-info-details__item">
        <h6 class="player-info-details__title">Height</h6>
        <div class="player-info-details__value">6-2</div>
    </div>
    <div class="player-info-details__item">
        <h6 class="player-info-details__title">Weight</h6>
        <div class="player-info-details__value">223</div>
    </div>
    <div class="player-info-details__item">
        <h6 class="player-info-details__title">Age</h6>
        <div class="player-info-details__value">22</div>
    </div>
    <div class="player-info-details__item">
        <h6 class="player-info-details__title">Home Town</h6>
        <div class="player-info-details__value">West Columbia, TX</div>
    </div>
    <div class="player-info-details__item">
        <h6 class="player-info-details__title">Class</h6>
        <div class="player-info-details__value">Senior</div>
    </div>
</div>
<table class="basicInfoTable">
    <span title="Sub-Position">Sub-Position</span>
    <span>Pro Style</span>
    <span title="Last Updated">Last Updated</span>
    <span>Dec 2024</span>
    <span title="Draft Year">Draft Year</span>
    <span>2025</span>
    <span title="40 yard dash time">40 yard dash time</span>
    <span>4.65 sec</span>
</table>
<figure class="player-info__photo">
    <img src="/images/players/cam-ward.jpg" />
</figure>
<table class="starRatingTable">
    <tr><th>Overall Rating</th></tr>
    <tr><td><span>92.5 / 100</span></td></tr>
    <tr><td></td></tr>
    <tr><td><div class="meter" title="Opposition Strength: 85%">85%</div></td></tr>
    <tr><td>Release Speed: 90</td></tr>
    <tr><td>Short Passing: 88</td></tr>
    <tr><td>Medium Passing: 85</td></tr>
    <tr><td>Long Passing: 82</td></tr>
    <tr><td>Rush Scramble: 75</td></tr>
    <tr>
        <td>
            <span>draft projection</span>
            <span>Top 5 Pick</span>
            <span>overall rank</span>
            <span>1</span>
            <span>position rank</span>
            <span>QB1</span>
        </td>
    </tr>
</table>
<div class="rankingBox">
    <div class="rankVal">1.5</div>
    <div class="rankVal">1.0</div>
</div>
<div class="playerDescIntro">Elite quarterback prospect with exceptional arm talent.</div>
<div class="playerDescPro">
Scouting Report Strengths
Strong arm
Pocket presence
</div>
<div class="playerDescNeg">
Scouting Report Weaknesses
Footwork needs work
</div>
<div class="playerDescNeg">Day one starter potential.</div>
</body>
</html>
"""

RANKINGS_HTML = """
<html>
<body>
<table id="positionRankTable">
    <tbody>
        <tr data-href="/players/cam-ward-qb-2025">
            <td>Cam Ward</td>
            <td>QB</td>
            <td>Miami</td>
        </tr>
        <tr data-href="/players/shedeur-sanders-qb-2025">
            <td>Shedeur Sanders</td>
            <td>QB</td>
            <td>Colorado</td>
        </tr>
    </tbody>
</table>
<ul class="pagination">
    <li class="page-item"><a class="page-link" href="/positions/QB/1/2026">1</a></li>
    <li class="page-item"><a class="page-link" href="/positions/QB/2/2026">2</a></li>
    <li class="page-item"><a class="page-link" href="/positions/QB/3/2026">3</a></li>
</ul>
</body>
</html>
"""

RANKINGS_SINGLE_PAGE_HTML = """
<html>
<body>
<table id="positionRankTable">
    <tbody>
        <tr data-href="/players/cam-ward-qb-2025">
            <td>Cam Ward</td>
            <td>QB</td>
            <td>Miami</td>
        </tr>
    </tbody>
</table>
</body>
</html>
"""

STATS_HTML_QB = """
<html>
<body>
<span title="College Games Played">College Games Played</span>
<span>13</span>
<span title="College Snap Count">College Snap Count</span>
<span>850</span>
<div id="QBstats">
    <table>
        <thead>
            <tr>
                <th class="player-season-avg__stat">Year</th>
                <th class="player-season-avg__stat">CMP</th>
                <th class="player-season-avg__stat">ATT</th>
                <th class="player-season-avg__stat">CMP%</th>
                <th class="player-season-avg__stat">YDS</th>
                <th class="player-season-avg__stat">TD</th>
                <th class="player-season-avg__stat">INT</th>
                <th class="player-season-avg__stat">SACK</th>
                <th class="player-season-avg__stat">Avg</th>
                <th class="player-season-avg__stat">Pro Rat</th>
                <th class="player-season-avg__stat">Rat</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>2024 Season</td>
                <td>280</td>
                <td>420</td>
                <td>66.7</td>
                <td>3800</td>
                <td>32</td>
                <td>8</td>
                <td>15</td>
                <td>9.0</td>
                <td>92.3</td>
                <td>85</td>
            </tr>
        </tbody>
    </table>
</div>
</body>
</html>
"""

STATS_HTML_DEFENSE = """
<html>
<body>
<span title="College Games Played">College Games Played</span>
<span>12</span>
<span title="College Snap Count">College Snap Count</span>
<span>700</span>
<div id="DBLBDL-stats">
    <table>
        <thead>
            <tr>
                <th class="player-season-avg__stat">Year</th>
                <th class="player-season-avg__stat">Total</th>
                <th class="player-season-avg__stat">Solo</th>
                <th class="player-season-avg__stat">FF</th>
                <th class="player-season-avg__stat">Sacks</th>
                <th class="player-season-avg__stat">INTs</th>
                <th class="player-season-avg__stat">YDS</th>
                <th class="player-season-avg__stat">TD</th>
                <th class="player-season-avg__stat">PDs</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>2024 Season</td>
                <td>85</td>
                <td>50</td>
                <td>3</td>
                <td>8.5</td>
                <td>2</td>
                <td>30</td>
                <td>1</td>
                <td>10</td>
            </tr>
        </tbody>
    </table>
</div>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# ProspectProfileParser Tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestProspectProfileParser:
    def setup_method(self):
        self.parser = ProspectProfileParser()

    def test_parse_profile_basic_info(self):
        result = self.parser.parse_profile(PROSPECT_PROFILE_HTML, position="QB")
        info = result["basic_info"]
        assert info["first_name"] == "Cam"
        assert info["last_name"] == "Ward"
        assert info["full_name"] == "Cam Ward"
        assert info["position"] == "QB"
        assert info["college"] == "miami"
        assert info["height"] == "6-2"

    def test_parse_profile_photo_url(self):
        result = self.parser.parse_profile(PROSPECT_PROFILE_HTML, position="QB")
        info = result["basic_info"]
        assert (
            info["photo_url"]
            == "https://www.nfldraftbuzz.com/images/players/cam-ward.jpg"
        )

    def test_parse_profile_ratings(self):
        result = self.parser.parse_profile(PROSPECT_PROFILE_HTML, position="QB")
        ratings = result["ratings"]
        assert ratings["overall_rating"] == 92.5
        assert ratings["opposition_rating"] == 85
        assert ratings["avg_overall_rank"] == 1.5
        assert ratings["avg_position_rank"] == 1.0

    def test_parse_profile_skills(self):
        result = self.parser.parse_profile(PROSPECT_PROFILE_HTML, position="QB")
        skills = result["skills"]
        assert skills is not None
        assert skills["release_speed"] == 90
        assert skills["short_passing"] == 88
        assert skills["rush_scramble"] == 75

    def test_parse_profile_scouting_report(self):
        result = self.parser.parse_profile(PROSPECT_PROFILE_HTML, position="QB")
        sr = result["scouting_report"]
        assert "Elite quarterback" in sr["bio"]
        assert any("Strong arm" in s for s in sr["strengths"])
        assert any("Footwork" in s for s in sr["weaknesses"])
        assert sr["summary"] == "Day one starter potential."

    def test_parse_profile_missing_name_raises(self):
        with pytest.raises(ParsingError, match="Could not find player name"):
            self.parser.parse_profile("<html><body></body></html>", position="QB")

    def test_parse_stats_qb(self):
        stats = self.parser.parse_stats(STATS_HTML_QB, position="QB")
        assert stats is not None
        assert len(stats) == 1
        s = stats[0]
        assert s["year"] == 2024
        assert s["cmp"] == 280
        assert s["att"] == 420
        assert s["td"] == 32
        assert s["ints"] == 8
        assert s["qb_rtg"] == 92.3
        assert s["games_played"] == 13
        assert s["snap_count"] == 850

    def test_parse_stats_defense(self):
        stats = self.parser.parse_stats(STATS_HTML_DEFENSE, position="LB")
        assert stats is not None
        assert len(stats) == 1
        s = stats[0]
        assert s["year"] == 2024
        assert s["tackle"]["total"] == 85
        assert s["tackle"]["sacks"] == 8.5
        assert s["interception"]["ints"] == 2
        assert s["interception"]["pds"] == 10

    def test_parse_stats_no_table(self):
        stats = self.parser.parse_stats("<html><body></body></html>", position="QB")
        assert stats is None


# ---------------------------------------------------------------------------
# RankingsParser Tests
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRankingsParser:
    def setup_method(self):
        self.parser = RankingsParser()

    def test_parse_position_rankings(self):
        result = self.parser.parse_position_rankings(
            RANKINGS_HTML, position="QB", year=2026, page=1
        )
        assert result["position"] == "QB"
        assert result["year"] == 2026
        assert result["page"] == 1
        assert len(result["entries"]) == 2

    def test_parse_position_rankings_entries(self):
        result = self.parser.parse_position_rankings(
            RANKINGS_HTML, position="QB", year=2026, page=1
        )
        first = result["entries"][0]
        assert first["name"] == "Cam Ward"
        assert first["position"] == "QB"
        assert first["school"] == "Miami"
        assert first["rank"] == 1
        assert first["href"] == "/players/cam-ward-qb-2025"

    def test_parse_total_pages_multi_page(self):
        result = self.parser.parse_position_rankings(
            RANKINGS_HTML, position="QB", year=2026, page=1
        )
        assert result["total_pages"] == 3

    def test_parse_total_pages_single_page(self):
        result = self.parser.parse_position_rankings(
            RANKINGS_SINGLE_PAGE_HTML, position="QB", year=2026, page=1
        )
        assert result["total_pages"] == 1

    def test_parse_empty_page(self):
        result = self.parser.parse_position_rankings(
            "<html><body></body></html>", position="QB", year=2026, page=1
        )
        assert result["entries"] == []
        assert result["total_pages"] == 1
