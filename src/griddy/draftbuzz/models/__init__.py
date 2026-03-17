# isort: skip_file

from typing import TYPE_CHECKING

from griddy.core._lazy import dynamic_dir, dynamic_getattr

if TYPE_CHECKING:
    from griddy.draftbuzz.models.base import DraftBuzzBaseModel
    from griddy.draftbuzz.models.entities.prospect import (
        BasicInfo,
        BaseStats,
        Comparison,
        DefenseStats,
        DefensiveBackSkills,
        DefensiveLinemanSkills,
        InterceptionStats,
        LinebackerSkills,
        OffenseSkillPlayerStats,
        OffensiveLinemanSkills,
        PassCatcherSkills,
        PassingSkills,
        PassingStats,
        ProspectProfile,
        RatingsAndRankings,
        ReceivingStats,
        RunningBackSkills,
        RushingStats,
        ScoutingReport,
        TackleStats,
    )
    from griddy.draftbuzz.models.entities.rankings import (
        PositionRankings,
        RankedProspect,
    )
    from griddy.draftbuzz.models.entities.security import Security

__all__ = [
    "BasicInfo",
    "BaseStats",
    "Comparison",
    "DefenseStats",
    "DefensiveBackSkills",
    "DefensiveLinemanSkills",
    "DraftBuzzBaseModel",
    "InterceptionStats",
    "LinebackerSkills",
    "OffenseSkillPlayerStats",
    "OffensiveLinemanSkills",
    "PassCatcherSkills",
    "PassingSkills",
    "PassingStats",
    "PositionRankings",
    "ProspectProfile",
    "RankedProspect",
    "RatingsAndRankings",
    "ReceivingStats",
    "RunningBackSkills",
    "RushingStats",
    "ScoutingReport",
    "Security",
    "TackleStats",
]

_dynamic_imports: dict[str, str] = {
    "BasicInfo": ".entities.prospect",
    "BaseStats": ".entities.prospect",
    "Comparison": ".entities.prospect",
    "DefenseStats": ".entities.prospect",
    "DefensiveBackSkills": ".entities.prospect",
    "DefensiveLinemanSkills": ".entities.prospect",
    "DraftBuzzBaseModel": ".base",
    "InterceptionStats": ".entities.prospect",
    "LinebackerSkills": ".entities.prospect",
    "OffenseSkillPlayerStats": ".entities.prospect",
    "OffensiveLinemanSkills": ".entities.prospect",
    "PassCatcherSkills": ".entities.prospect",
    "PassingSkills": ".entities.prospect",
    "PassingStats": ".entities.prospect",
    "PositionRankings": ".entities.rankings",
    "ProspectProfile": ".entities.prospect",
    "RankedProspect": ".entities.rankings",
    "RatingsAndRankings": ".entities.prospect",
    "ReceivingStats": ".entities.prospect",
    "RunningBackSkills": ".entities.prospect",
    "RushingStats": ".entities.prospect",
    "ScoutingReport": ".entities.prospect",
    "Security": ".entities.security",
    "TackleStats": ".entities.prospect",
}


def __getattr__(attr_name: str) -> object:
    """Lazily import a model class by name from its submodule."""
    return dynamic_getattr(attr_name, _dynamic_imports, __package__, __name__)


def __dir__() -> list[str]:
    """Return the list of all publicly importable model names."""
    return dynamic_dir(_dynamic_imports)
