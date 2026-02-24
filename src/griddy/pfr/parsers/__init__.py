"""PFR HTML parsers package.

Re-exports the individual parser classes for convenient access::

    from griddy.pfr.utils.parsers import ScheduleParser, GameDetailsParser
"""

from .game_details import GameDetailsParser
from .schedule import ScheduleParser

__all__ = ["GameDetailsParser", "ScheduleParser"]
