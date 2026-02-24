import builtins
from typing import TYPE_CHECKING

from griddy.core._import import dynamic_import

if TYPE_CHECKING:
    from griddy.pfr.models.entities.game_details import (
        Drive,
        DriveTypedDict,
        ExpectedPoints,
        ExpectedPointsTypedDict,
        GameDetails,
        GameDetailsTypedDict,
        LinescoreEntry,
        LinescoreEntryTypedDict,
        PlayerDefense,
        PlayerDefenseTypedDict,
        PlayerKicking,
        PlayerKickingTypedDict,
        PlayerOffense,
        PlayerOffenseTypedDict,
        PlayerReturn,
        PlayerReturnTypedDict,
        Scorebox,
        ScoreboxMeta,
        ScoreboxMetaTypedDict,
        ScoreboxTeam,
        ScoreboxTeamTypedDict,
        ScoreboxTypedDict,
        ScoringPlay,
        ScoringPlayTypedDict,
        SnapCount,
        SnapCountTypedDict,
        Starter,
        StarterTypedDict,
    )
    from griddy.pfr.models.entities.player_profile import (
        BirthPlace,
        BirthPlaceTypedDict,
        DraftInfo,
        DraftInfoTypedDict,
        JerseyNumber,
        JerseyNumberTypedDict,
        PlayerBio,
        PlayerBioTypedDict,
        PlayerNames,
        PlayerNamesTypedDict,
        PlayerProfile,
        PlayerProfileTypedDict,
        PlayerStatistics,
        PlayerStatisticsTypedDict,
        RoundAndOverall,
        RoundAndOverallTypedDict,
        Transaction,
        TransactionTypedDict,
    )
    from griddy.pfr.models.entities.schedule_game import (
        ScheduleGame,
        ScheduleGameTypedDict,
    )
    from griddy.pfr.models.entities.security import Security, SecurityTypedDict

__all__ = [
    "Drive",
    "DriveTypedDict",
    "ExpectedPoints",
    "ExpectedPointsTypedDict",
    "GameDetails",
    "GameDetailsTypedDict",
    "LinescoreEntry",
    "LinescoreEntryTypedDict",
    "PlayerDefense",
    "PlayerDefenseTypedDict",
    "PlayerKicking",
    "PlayerKickingTypedDict",
    "PlayerOffense",
    "PlayerOffenseTypedDict",
    "PlayerReturn",
    "PlayerReturnTypedDict",
    "BirthPlace",
    "BirthPlaceTypedDict",
    "DraftInfo",
    "DraftInfoTypedDict",
    "JerseyNumber",
    "JerseyNumberTypedDict",
    "PlayerBio",
    "PlayerBioTypedDict",
    "PlayerNames",
    "PlayerNamesTypedDict",
    "PlayerProfile",
    "PlayerProfileTypedDict",
    "PlayerStatistics",
    "PlayerStatisticsTypedDict",
    "RoundAndOverall",
    "RoundAndOverallTypedDict",
    "ScheduleGame",
    "ScheduleGameTypedDict",
    "Scorebox",
    "ScoreboxMeta",
    "ScoreboxMetaTypedDict",
    "ScoreboxTeam",
    "ScoreboxTeamTypedDict",
    "ScoreboxTypedDict",
    "ScoringPlay",
    "ScoringPlayTypedDict",
    "Security",
    "SecurityTypedDict",
    "SnapCount",
    "SnapCountTypedDict",
    "Starter",
    "StarterTypedDict",
    "Transaction",
    "TransactionTypedDict",
]

_dynamic_imports: dict[str, str] = {
    "BirthPlace": ".entities.player_profile",
    "BirthPlaceTypedDict": ".entities.player_profile",
    "DraftInfo": ".entities.player_profile",
    "DraftInfoTypedDict": ".entities.player_profile",
    "Drive": ".entities.game_details",
    "DriveTypedDict": ".entities.game_details",
    "ExpectedPoints": ".entities.game_details",
    "ExpectedPointsTypedDict": ".entities.game_details",
    "GameDetails": ".entities.game_details",
    "GameDetailsTypedDict": ".entities.game_details",
    "JerseyNumber": ".entities.player_profile",
    "JerseyNumberTypedDict": ".entities.player_profile",
    "LinescoreEntry": ".entities.game_details",
    "LinescoreEntryTypedDict": ".entities.game_details",
    "PlayerBio": ".entities.player_profile",
    "PlayerBioTypedDict": ".entities.player_profile",
    "PlayerDefense": ".entities.game_details",
    "PlayerDefenseTypedDict": ".entities.game_details",
    "PlayerNames": ".entities.player_profile",
    "PlayerNamesTypedDict": ".entities.player_profile",
    "PlayerKicking": ".entities.game_details",
    "PlayerKickingTypedDict": ".entities.game_details",
    "PlayerOffense": ".entities.game_details",
    "PlayerOffenseTypedDict": ".entities.game_details",
    "PlayerProfile": ".entities.player_profile",
    "PlayerProfileTypedDict": ".entities.player_profile",
    "PlayerReturn": ".entities.game_details",
    "PlayerReturnTypedDict": ".entities.game_details",
    "PlayerStatistics": ".entities.player_profile",
    "PlayerStatisticsTypedDict": ".entities.player_profile",
    "RoundAndOverall": ".entities.player_profile",
    "RoundAndOverallTypedDict": ".entities.player_profile",
    "Scorebox": ".entities.game_details",
    "ScoreboxMeta": ".entities.game_details",
    "ScoreboxMetaTypedDict": ".entities.game_details",
    "ScoreboxTeam": ".entities.game_details",
    "ScoreboxTeamTypedDict": ".entities.game_details",
    "ScoreboxTypedDict": ".entities.game_details",
    "ScoringPlay": ".entities.game_details",
    "ScoringPlayTypedDict": ".entities.game_details",
    "ScheduleGame": ".entities.schedule_game",
    "ScheduleGameTypedDict": ".entities.schedule_game",
    "Security": ".entities.security",
    "SecurityTypedDict": ".entities.security",
    "SnapCount": ".entities.game_details",
    "SnapCountTypedDict": ".entities.game_details",
    "Starter": ".entities.game_details",
    "StarterTypedDict": ".entities.game_details",
    "Transaction": ".entities.player_profile",
    "TransactionTypedDict": ".entities.player_profile",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    if module_name is None:
        raise AttributeError(
            f"No {attr_name} found in _dynamic_imports for module name -> {__name__} "
        )

    try:
        module = dynamic_import(module_name, __package__)
        result = getattr(module, attr_name)
        return result
    except ImportError as e:
        raise ImportError(
            f"Failed to import {attr_name} from {module_name}: {e}"
        ) from e
    except AttributeError as e:
        raise AttributeError(
            f"Failed to get {attr_name} from {module_name}: {e}"
        ) from e


def __dir__():
    lazy_attrs = builtins.list(_dynamic_imports.keys())
    return builtins.sorted(lazy_attrs)
