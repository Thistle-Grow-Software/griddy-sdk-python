---
icon: lucide/rocket
---

# Griddy SDK Python

A Python SDK providing programmatic access to several American Football data sources.

## Overview

The Griddy SDK gives you a unified interface to three major football data sources:

- **[NFL.com API](guides/nfl-regular-api.md)** — Game schedules, box scores, play-by-play, rosters, standings, draft data, and more from the public NFL.com API
- **[NFL Pro Stats](guides/nfl-pro-stats.md)** — Advanced passing, rushing, receiving, and defensive statistics from NFL Pro
- **[Next Gen Stats](guides/nfl-ngs.md)** — Player tracking data, speed leaders, completion probability, and other NGS metrics
- **[Pro Football Reference](guides/pfr.md)** — Historical stats, player profiles, season schedules, and game details scraped from PFR

Every endpoint provides both **synchronous** and **asynchronous** methods, and all responses are validated through **Pydantic models** with full type annotations.

## Quick Start

```python
from griddy.nfl import GriddyNFL

# Initialize with an access token
nfl = GriddyNFL(nfl_auth={"accessToken": "your_token"})

# Fetch Week 1 games
games = nfl.games.get_games(
    season=2025,
    season_type="REG",
    week=1,
)

# Get passing stats for the season
passing = nfl.stats.passing.get_season_summary(
    season=2025,
    season_type="REG",
)
```

See the [Getting Started](getting-started.md) guide for installation and authentication setup.

## Guides

| Guide | Description |
|-------|-------------|
| [Getting Started](getting-started.md) | Installation, authentication, and your first API call |
| [NFL Regular API](guides/nfl-regular-api.md) | Games, rosters, standings, draft, combine, and more |
| [NFL Pro Stats](guides/nfl-pro-stats.md) | Advanced passing, rushing, receiving, and defense stats |
| [Next Gen Stats](guides/nfl-ngs.md) | Player tracking data, speed leaders, and NGS metrics |
| [Pro Football Reference](guides/pfr.md) | Historical stats via HTML scraping with Browserless |
| [Authentication](guides/authentication.md) | Detailed auth flow: browser login vs. direct token |
| [Error Handling](guides/error-handling.md) | Exception hierarchy, retries, and recovery patterns |
| [Async Usage](guides/async.md) | async/await patterns and concurrency |
| [Architecture](guides/architecture.md) | Lazy-loaded sub-SDKs, hooks, and endpoint patterns |
| [Advanced Usage](guides/advanced.md) | Custom hooks, request manipulation, and extending the SDK |

## API Reference

Browse the auto-generated [API Reference](reference/) for detailed documentation of all
modules, classes, and methods.
