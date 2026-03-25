# NFL Regular API

The regular NFL.com API (`api.nfl.com`) provides public endpoints for games, rosters, standings, draft data, combine results, and more. These endpoints are accessed through the top-level attributes on the [`GriddyNFL`][griddy.nfl.sdk.GriddyNFL] client.

## Setup

```python
from griddy.nfl import GriddyNFL

nfl = GriddyNFL(nfl_auth={"accessToken": "your_token"})
```

## Games

The `games` sub-SDK provides access to game schedules, box scores, and play-by-play data.

### Fetching Scheduled Games

```python
games = nfl.games.get_games(
    season=2025,
    season_type="REG",
    week=1,
    with_external_ids=True,
)

for game in games:
    print(f"Week {game.week}: {game.away_team} @ {game.home_team}")
```

### Box Scores

Retrieve detailed box score data for a specific game:

```python
box_score = nfl.games.get_box_score(game_id="game_id_here")
```

### Play-by-Play

Get granular play-by-play data, optionally including penalty and formation details:

```python
plays = nfl.games.get_play_by_play(
    game_id="game_id_here",
    include_penalties=True,
    include_formations=True,
)
```

### Weekly Game Details

Fetch enriched game details for an entire week, with optional drive charts and replays:

```python
details = nfl.games.get_weekly_game_details(
    season=2025,
    type_="REG",
    week=1,
    include_drive_chart=True,
    include_replays=True,
    include_standings=True,
)
```

### Live Game Stats

Get real-time game statistics during live games:

```python
live = nfl.games.get_live_game_stats(
    season=2025,
    season_type="REG",
    week=1,
)
```

## Rosters

Fetch team rosters for a given season:

```python
rosters = nfl.rosters.get_rosters(
    season=2025,
    limit=20,
)
```

## Standings

Get division and conference standings:

```python
standings = nfl.standings.get_standings(
    season=2025,
    season_type="REG",
    week=18,
)
```

## Draft

### Draft Picks

Retrieve all draft picks for a given year:

```python
picks = nfl.draft.get_picks_report(
    year=2025,
    limit=1000,
)

for pick in picks:
    print(f"Round {pick.round}, Pick {pick.pick}: {pick.player_name}")
```

### Team Needs

Get team draft needs analysis:

```python
needs = nfl.draft.get_teamneeds(year=2025)
```

## Combine

### Participant Profiles

Fetch NFL Combine participant profiles:

```python
profiles = nfl.combine.get_profiles(
    year=2025,
    limit=1000,
)
```

### Combine Rankings

Get rankings sorted by a specific event attribute:

```python
rankings = nfl.combine.get_rankings(
    rank_attribute="FORTY_YARD_DASH",
    sort_order="ASC",
    year=2025,
)
```

## Teams and Venues

### Teams

```python
teams = nfl.football_teams.get_teams()
```

### Venues

```python
venues = nfl.venues.get_venues()
```

## Weeks

Get information about season weeks:

```python
weeks = nfl.weeks.get_weeks(season=2025)
```

## Experience and Content

### Game Experience

Fetch rich game detail pages by slug or ID:

```python
experience = nfl.experience.get_game_details(slug="game-slug-here")
```

### Video Content

Access game replay videos:

```python
videos = nfl.video_content.get_game_replays(game_id="game_id_here")
```

## Common Parameters

Most regular API endpoints share these parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `season` | `int` | NFL season year (e.g., `2025`) |
| `season_type` | `str` | Season type: `"REG"`, `"PRE"`, `"POST"` |
| `week` | `int` | Week number |
| `limit` | `int` | Maximum number of results to return |
| `retries` | `RetryConfig` | Override default retry behavior |
| `timeout_ms` | `int` | Request timeout in milliseconds |

## Error Handling

Regular API endpoints raise [`GriddyNFLDefaultError`][griddy.nfl.errors.GriddyNFLDefaultError] for API-level errors:

```python
from griddy.nfl.errors import GriddyNFLDefaultError
from griddy.core.exceptions import NotFoundError

try:
    games = nfl.games.get_games(season=2025, season_type="REG", week=1)
except NotFoundError:
    print("No games found for this week")
except GriddyNFLDefaultError as e:
    print(f"API error: {e}")
```

See the [Error Handling Guide](error-handling.md) for the full exception hierarchy.
