# Getting Started

This guide walks you through installing the Griddy SDK, authenticating, and making your first API calls.

## Installation

Install the SDK with pip:

```bash
pip install griddy
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add griddy
```

### Browser Authentication Extra

If you want to authenticate via automated browser login (Playwright), install with the `browser-auth` extra:

```bash
pip install "griddy[browser-auth]"
```

This installs [Playwright](https://playwright.dev/python/) and its browser binaries. After installing, run:

```bash
playwright install chromium
```

## Authentication

The NFL.com API requires an access token. The Griddy SDK supports two authentication methods.

### Method 1: Direct Token

If you already have an NFL.com access token (e.g., from a browser session), pass it directly:

```python
from griddy.nfl import GriddyNFL

nfl = GriddyNFL(nfl_auth={"accessToken": "your_access_token"})
```

You can also provide a refresh token and expiration for automatic token renewal:

```python
nfl = GriddyNFL(
    nfl_auth={
        "accessToken": "your_access_token",
        "refreshToken": "your_refresh_token",
        "expiresIn": 1735689600,  # Unix timestamp
    }
)
```

When a refresh token is provided, the SDK automatically refreshes the access token before it expires.

### Method 2: Browser Authentication

Automate the login flow using Playwright:

```python
from griddy.nfl import GriddyNFL

nfl = GriddyNFL.authenticate_via_browser(
    login_email="your_email@example.com",
    login_password="your_password",
    headless=True,
    save_credentials_path="credentials.json",
)
```

This opens a headless browser, logs in to NFL.com, captures the auth tokens, and optionally saves them to a file for reuse.

!!! tip "Environment Variables"
    Store credentials as environment variables to avoid hardcoding them:

    ```bash
    export NFL_LOGIN_EMAIL="your_email@example.com"
    export NFL_LOGIN_PASSWORD="your_password"
    ```

    ```python
    import os
    from griddy.nfl import GriddyNFL

    nfl = GriddyNFL.authenticate_via_browser(
        login_email=os.environ["NFL_LOGIN_EMAIL"],
        login_password=os.environ["NFL_LOGIN_PASSWORD"],
        headless=True,
    )
    ```

See the [Authentication Guide](guides/authentication.md) for more details on token refresh, credential persistence, and environment variable configuration.

## Your First API Call

Once authenticated, access NFL data through the SDK's sub-SDKs:

```python
from griddy.nfl import GriddyNFL

nfl = GriddyNFL(nfl_auth={"accessToken": "your_token"})

# Get scheduled games for Week 1 of the 2025 regular season
games = nfl.games.get_games(
    season=2025,
    season_type="REG",
    week=1,
)

# Iterate over the results
for game in games:
    print(f"{game.away_team} @ {game.home_team}")
```

### Fetching Pro Stats

Advanced stats live under `nfl.stats`:

```python
# Season passing leaders
passing = nfl.stats.passing.get_season_summary(
    season=2025,
    season_type="REG",
    qualified_passer=True,
)
```

### Using Pro Football Reference

The PFR client scrapes Pro Football Reference for historical data:

```python
from griddy.pfr import GriddyPFR

pfr = GriddyPFR()

# Get the 2024 season schedule
schedule = pfr.schedule.get_season_schedule(season=2024)

# Get a specific game's box score
game = pfr.games.get_game_details(game_id="202502090kan")
```

!!! note
    The PFR client requires a [Browserless](https://www.browserless.io/) instance for rendering JavaScript-heavy pages. See the [PFR Guide](guides/pfr.md) for setup instructions.

## Context Manager Support

All SDK clients support the context manager protocol for resource cleanup:

```python
with GriddyNFL(nfl_auth={"accessToken": "your_token"}) as nfl:
    games = nfl.games.get_games(season=2025, season_type="REG", week=1)
# HTTP client resources are cleaned up automatically
```

## Next Steps

- [NFL Regular API Guide](guides/nfl-regular-api.md) — Games, rosters, standings, and more
- [NFL Pro Stats Guide](guides/nfl-pro-stats.md) — Advanced player and team statistics
- [Next Gen Stats Guide](guides/nfl-ngs.md) — Player tracking and NGS metrics
- [PFR Guide](guides/pfr.md) — Historical data via HTML scraping
- [Error Handling](guides/error-handling.md) — Working with SDK exceptions
