"""PFR HTML parsers package.

Re-exports the individual parser classes for convenient access::

    from griddy.pfr.utils.parsers import ScheduleParser, GameDetailsParser
"""

from .awards import AwardsParser
from .coach_profile import CoachProfileParser
from .draft import DraftParser
from .game_details import GameDetailsParser
from .leaders import LeadersParser
from .official_profile import OfficialProfileParser
from .player_profile import PlayerProfileParser
from .schedule import ScheduleParser
from .season_overview import SeasonOverviewParser
from .stadium import StadiumParser
from .team_franchise import FranchiseParser
from .team_season import TeamSeasonParser

__all__ = [
    "AwardsParser",
    "CoachProfileParser",
    "DraftParser",
    "GameDetailsParser",
    "LeadersParser",
    "OfficialProfileParser",
    "PlayerProfileParser",
    "ScheduleParser",
    "SeasonOverviewParser",
    "StadiumParser",
    "FranchiseParser",
    "TeamSeasonParser",
]
