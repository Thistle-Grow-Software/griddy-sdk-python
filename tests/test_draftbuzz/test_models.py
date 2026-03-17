"""Tests for griddy.draftbuzz.models module."""

import pytest

from griddy.draftbuzz.models import (
    BasicInfo,
    Comparison,
    DefenseStats,
    InterceptionStats,
    PassingSkills,
    PassingStats,
    PositionRankings,
    ProspectProfile,
    RankedProspect,
    RatingsAndRankings,
    ScoutingReport,
    TackleStats,
)


@pytest.mark.unit
class TestBasicInfo:
    def test_defaults(self):
        info = BasicInfo()
        assert info.first_name is None
        assert info.position is None
        assert info.photo_url is None

    def test_full_construction(self):
        info = BasicInfo(
            first_name="Cam",
            last_name="Ward",
            full_name="Cam Ward",
            position="QB",
            college="miami",
            height="6-2",
            weight="223",
        )
        assert info.full_name == "Cam Ward"
        assert info.position == "QB"


@pytest.mark.unit
class TestRatingsAndRankings:
    def test_defaults(self):
        r = RatingsAndRankings()
        assert r.overall_rating is None

    def test_full_construction(self):
        r = RatingsAndRankings(
            overall_rating=92.5,
            opposition_rating=85,
            draft_projection="Top 5",
            overall_rank=1,
            position_rank="QB1",
        )
        assert r.overall_rating == 92.5
        assert r.overall_rank == 1


@pytest.mark.unit
class TestPassingSkills:
    def test_construction(self):
        s = PassingSkills(
            release_speed=90,
            short_passing=88,
            medium_passing=85,
            long_passing=82,
            rush_scramble=75,
        )
        assert s.release_speed == 90


@pytest.mark.unit
class TestPassingStats:
    def test_construction(self):
        s = PassingStats(
            year=2024,
            games_played=13,
            cmp=280,
            att=420,
            cmp_pct=66.7,
            yds=3800,
            td=32,
            ints=8,
            sack=15,
            qb_rtg=92.3,
        )
        assert s.year == 2024
        assert s.td == 32

    def test_inherits_base_stats_fields(self):
        s = PassingStats(year=2024, games_played=13, snap_count=850)
        assert s.games_played == 13
        assert s.snap_count == 850


@pytest.mark.unit
class TestDefenseStats:
    def test_nested_construction(self):
        s = DefenseStats(
            year=2024,
            tackle=TackleStats(total=85, solo=50, ff=3, sacks=8.5),
            interception=InterceptionStats(ints=2, yds=30, td=1, pds=10),
        )
        assert s.tackle.total == 85
        assert s.interception.ints == 2

    def test_empty_dicts_to_none(self):
        s = DefenseStats.model_validate(
            {"year": 2024, "tackle": {}, "interception": {}}
        )
        assert s.tackle is None
        assert s.interception is None


@pytest.mark.unit
class TestScoutingReport:
    def test_defaults(self):
        sr = ScoutingReport()
        assert sr.bio is None
        assert sr.strengths is None
        assert sr.weaknesses is None
        assert sr.summary is None

    def test_construction(self):
        sr = ScoutingReport(
            bio="Elite quarterback prospect.",
            strengths=["Arm strength", "Pocket presence"],
            weaknesses=["Footwork"],
            summary="Day 1 starter.",
        )
        assert len(sr.strengths) == 2


@pytest.mark.unit
class TestComparison:
    def test_construction(self):
        c = Comparison(name="Patrick Mahomes", school="Texas Tech", similarity=85)
        assert c.name == "Patrick Mahomes"
        assert c.similarity == 85


@pytest.mark.unit
class TestProspectProfile:
    def test_defaults(self):
        p = ProspectProfile()
        assert p.basic_info is None
        assert p.ratings is None
        assert p.stats is None

    def test_full_construction(self):
        p = ProspectProfile(
            basic_info=BasicInfo(full_name="Cam Ward", position="QB"),
            ratings=RatingsAndRankings(overall_rating=92.5),
            scouting_report=ScoutingReport(bio="Elite QB."),
            comparisons=[Comparison(name="Patrick Mahomes", similarity=85)],
        )
        assert p.basic_info.full_name == "Cam Ward"
        assert p.ratings.overall_rating == 92.5


@pytest.mark.unit
class TestPositionRankings:
    def test_defaults(self):
        r = PositionRankings()
        assert r.entries == []

    def test_construction(self):
        r = PositionRankings(
            position="QB",
            year=2026,
            page=1,
            entries=[
                RankedProspect(name="Cam Ward", position="QB", school="Miami", rank=1),
                RankedProspect(
                    name="Shedeur Sanders", position="QB", school="Colorado", rank=2
                ),
            ],
        )
        assert len(r.entries) == 2
        assert r.entries[0].name == "Cam Ward"
        assert r.entries[1].rank == 2
