---
icon: lucide/rocket
---

# Griddy SDK Python

A Python SDK providing programmatic access to several American Football data sources.

## Features

- **NFL.com API** — Access public endpoints, advanced stats (NFL Pro), and Next Gen Stats
- **Pro Football Reference** — Scrape historical stats, player profiles, and game data
- **DraftBuzz** — Access draft prospect data and rankings
- **Async support** — Both sync and async methods for all endpoints
- **Type-safe** — Full Pydantic model validation with type annotations

## Installation

```bash
pip install griddy
```

## Quick Start

```python
from griddy.nfl import GriddyNFL

sdk = GriddyNFL()

# Access public NFL data
games = sdk.football.get_games(season=2025, week=1)
```

## API Reference

Browse the auto-generated [API Reference](reference/) for detailed documentation of all
modules, classes, and methods.
