"""Griddy SDK - Python SDK for NFL data sources.

Griddy SDK provides a unified, type-safe interface for accessing NFL data
from multiple sources including NFL.com, Next Gen Stats, and the Pro API.

Modules:
    nfl: NFL-specific SDK with access to games, stats, rosters, and more
    core: Shared functionality including HTTP client and exceptions

Basic Usage:
    >>> from griddy.nfl import GriddyNFL
    >>> nfl = GriddyNFL(nfl_auth={"accessToken": "your_token"})
    >>> games = nfl.games.get_games(season=2024, week=1)
    >>> stats = nfl.ngs.stats.get_passing_stats(season=2024)

Error Handling:
    >>> from griddy import GriddyError, RateLimitError
    >>> try:
    ...     games = nfl.games.get_games(season=2024)
    ... except RateLimitError as e:
    ...     print(f"Rate limited. Retry after: {e.retry_after}")
    ... except GriddyError as e:
    ...     print(f"Error: {e.message}")

For more information, see the documentation at:
https://jkgriebel93.github.io/griddy-sdk-python
"""

from . import core
from ._version import __version__

# Main exports
__all__ = [
    "__version__",
    "core",
    "draftbuzz",
    "nfl",
    "pfr",
    # Exceptions
    "GriddyError",
    "APIError",
    "RateLimitError",
    "NotFoundError",
    "AuthenticationError",
    "ValidationError",
]

# Convenience imports for common exceptions
from .core.exceptions import (
    APIError,
    AuthenticationError,
    GriddyError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
