# Pro Football Reference

The PFR SDK scrapes [Pro Football Reference](https://www.pro-football-reference.com/) pages for historical NFL data. It uses a headless browser via Browserless to render JavaScript-heavy pages and then parses the HTML into Pydantic models.

## Setup

### Browserless Configuration

The PFR client requires a [Browserless](https://www.browserless.io/) instance to render pages. Set the following environment variables:

```bash
export BROWSERLESS_HOST="your-browserless-host.example.com"
export BROWSERLESS_TOKEN="your_browserless_api_token"
```

Then create the client:

```python
from griddy.pfr import GriddyPFR

pfr = GriddyPFR()
```

!!! note
    PFR does not require authentication — Pro Football Reference is a public website. However, it does require a Browserless instance because PFR uses JavaScript to render some tables.

### Custom Browserless Config

You can customize the Browserless connection settings:

```python
from griddy.pfr import GriddyPFR
from griddy.pfr.backends import BrowserlessConfig

pfr = GriddyPFR(
    browserless_config=BrowserlessConfig(
        proxy="residential",
        request_timeout=60000,
        ttl=30000,
    ),
)
```

| Config Field | Default | Description |
|-------------|---------|-------------|
| `proxy` | `"residential"` | Proxy type for Browserless requests |
| `request_timeout` | `60000` | Request timeout in milliseconds |
| `ttl` | `30000` | Time-to-live for browser sessions |

## Game Details

Fetch full box score data for a specific game:

```python
game = pfr.games.get_game_details(game_id="202502090kan")

print(f"Score: {game.home_score} - {game.away_score}")
```

The `game_id` is the PFR game identifier, which follows the format `YYYYMMDD0<team_abbr>` (e.g., `202502090kan` for the Super Bowl on February 9, 2025 at Kansas City).

## Season Schedule

Retrieve the complete schedule for a season:

```python
schedule = pfr.schedule.get_season_schedule(season=2024)

for game in schedule:
    print(f"Week {game.week}: {game.away_team} @ {game.home_team}")
```

## Player Profiles

Look up player profiles by their PFR player ID:

```python
player = pfr.players.get_player_profile(player_id="MahoPa00")
```

Player IDs use PFR's format: first four letters of last name + first two of first name + a two-digit disambiguator (e.g., `MahoPa00` for Patrick Mahomes).

## Team Data

### Team Season Stats

```python
team = pfr.teams.get_team_season(team="kan", year=2024)
```

### Team Franchise History

```python
franchise = pfr.teams.get_team_franchise(team="kan")
```

Team abbreviations use PFR's format (e.g., `kan` for Kansas City, `phi` for Philadelphia, `nwe` for New England).

## Other Endpoints

The PFR SDK provides 17 endpoint categories:

| Sub-SDK | Description |
|---------|-------------|
| `pfr.awards` | NFL awards data |
| `pfr.coaches` | Coach records and history |
| `pfr.draft` | Historical draft data |
| `pfr.executives` | Front office personnel |
| `pfr.fantasy` | Fantasy football data |
| `pfr.frivolities` | Fun stats and records |
| `pfr.games` | Game box scores |
| `pfr.hof` | Hall of Fame data |
| `pfr.leaders` | Statistical leaders |
| `pfr.officials` | Game officials |
| `pfr.players` | Player profiles |
| `pfr.probowl` | Pro Bowl rosters |
| `pfr.schedule` | Season schedules |
| `pfr.schools` | College/school data |
| `pfr.seasons` | Season-level summaries |
| `pfr.stadiums` | Stadium information |
| `pfr.superbowl` | Super Bowl data |
| `pfr.teams` | Team stats and history |

## How It Works

The PFR scraping pipeline follows these steps:

1. **URL Construction** — The endpoint builds a URL from a path template and parameters
2. **HTML Fetching** — Browserless renders the page using a residential proxy and returns the fully-rendered HTML
3. **Preprocessing** — Hidden `<table>` elements (wrapped in HTML comments by PFR) are unmasked
4. **Parsing** — A dedicated parser extracts structured data from the HTML using BeautifulSoup
5. **Validation** — The parsed data is validated into Pydantic models via `model_validate()`

Each endpoint has a dedicated parser in `griddy.pfr.parsers` tailored to the specific HTML structure of that PFR page.

## Rate Limiting

Pro Football Reference has rate limiting in place. The SDK does not implement automatic rate limiting, so keep these guidelines in mind:

- Space requests apart when making many consecutive calls
- Use reasonable timeouts to avoid overloading the service
- Cache responses locally when working with historical data that doesn't change

```python
import time

seasons = [2020, 2021, 2022, 2023, 2024]
schedules = []

for season in seasons:
    schedule = pfr.schedule.get_season_schedule(season=season)
    schedules.append(schedule)
    time.sleep(2)  # Be respectful of PFR's servers
```

## Error Handling

PFR-specific errors live in [`griddy.pfr.errors`][griddy.pfr.errors]:

```python
from griddy.pfr.errors import ParsingError, NoResponseError

try:
    game = pfr.games.get_game_details(game_id="202502090kan")
except ParsingError as e:
    print(f"Failed to parse page at {e.url}: {e}")
except NoResponseError:
    print("Browserless returned an empty response")
```

| Exception | Description |
|-----------|-------------|
| [`GriddyPFRError`][griddy.pfr.errors.GriddyPFRError] | Base exception for all PFR errors |
| [`GriddyPFRDefaultError`][griddy.pfr.errors.GriddyPFRDefaultError] | Default PFR scraping error |
| [`ParsingError`][griddy.pfr.errors.ParsingError] | HTML parser failure (includes the `url` field) |
| [`NoResponseError`][griddy.pfr.errors.NoResponseError] | Empty response from Browserless |
| [`ResponseValidationError`][griddy.pfr.errors.ResponseValidationError] | Pydantic model validation failure |

## Context Manager

Clean up Browserless resources when done:

```python
with GriddyPFR() as pfr:
    schedule = pfr.schedule.get_season_schedule(season=2024)
    game = pfr.games.get_game_details(game_id="202502090kan")
# Resources cleaned up automatically
```
