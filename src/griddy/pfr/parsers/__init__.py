"""PFR HTML parsers package.

Re-exports the individual parser classes for convenient access::

    from griddy.pfr.utils.parsers import ScheduleParser, GameDetailsParser
"""

from .coach_profile import CoachProfileParser
from .game_details import GameDetailsParser
from .player_profile import PlayerProfileParser
from .schedule import ScheduleParser
from .team_franchise import FranchiseParser
from .team_season import TeamSeasonParser

__all__ = [
    "CoachProfileParser",
    "GameDetailsParser",
    "PlayerProfileParser",
    "ScheduleParser",
    "FranchiseParser",
    "TeamSeasonParser",
]
