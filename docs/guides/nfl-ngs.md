# Next Gen Stats

Next Gen Stats (NGS) endpoints (`nextgenstats.nfl.com`) provide player tracking data powered by RFID chips in player shoulder pads. This data includes speed metrics, completion probability, separation distance, and other advanced analytics.

Access NGS data through `nfl.ngs` on the [`GriddyNFL`][griddy.nfl.sdk.GriddyNFL] client.

## Setup

```python
from griddy.nfl import GriddyNFL

nfl = GriddyNFL(nfl_auth={"accessToken": "your_token"})
```

## Player Stats

The `nfl.ngs.stats` sub-SDK provides player-level tracking statistics by category.

### Passing Stats

NGS passing stats include completion probability, air distance, time to throw, and more:

```python
passing = nfl.ngs.stats.get_passing_stats(
    season=2025,
    season_type="REG",
)

# Filter to a specific week
week1_passing = nfl.ngs.stats.get_passing_stats(
    season=2025,
    season_type="REG",
    week=1,
)
```

### Receiving Stats

NGS receiving stats include separation distance, cushion, and yards after catch:

```python
receiving = nfl.ngs.stats.get_receiving_stats(
    season=2025,
    season_type="REG",
)
```

### Rushing Stats

NGS rushing stats include speed at handoff, time behind line of scrimmage, and efficiency metrics:

```python
rushing = nfl.ngs.stats.get_rushing_stats(
    season=2025,
    season_type="REG",
    week=5,
)
```

## Leaders

The `nfl.ngs.leaders` sub-SDK provides leaderboards for standout plays and performances.

### Fastest Ball Carriers

Top ball carrier speeds on plays:

```python
fastest = nfl.ngs.leaders.get_fastest_ball_carriers(
    season=2025,
    season_type="REG",
    limit=20,
)

for play in fastest:
    print(f"{play.player_name}: {play.max_speed} mph")
```

### Fastest Sacks

Quickest pass rushers by time to sack:

```python
sacks = nfl.ngs.leaders.get_fastest_sacks(
    season=2025,
    season_type="REG",
    limit=20,
    week=3,
)
```

### Improbable Completions

Passes completed despite low completion probability:

```python
improbable = nfl.ngs.leaders.get_improbable_completions(
    season=2025,
    season_type="REG",
)
```

### Incredible YAC (Yards After Catch)

Receptions with the most yards after catch expected vs. actual:

```python
yac = nfl.ngs.leaders.get_incredible_yac(
    season=2025,
    season_type="REG",
)
```

### Longest Plays

Longest plays measured by actual distance traveled:

```python
longest = nfl.ngs.leaders.get_longest_plays(
    season=2025,
    season_type="REG",
    limit=20,
)
```

### Longest Tackles

Tackles with the longest distance covered by the defender:

```python
tackles = nfl.ngs.leaders.get_longest_tackles(
    season=2025,
    season_type="REG",
    limit=20,
)
```

### Remarkable Rushes

Rushing plays with the most expected vs. actual yards:

```python
rushes = nfl.ngs.leaders.get_remarkable_rushes(
    season=2025,
    season_type="REG",
)
```

## Games

The `nfl.ngs.games` sub-SDK provides game-level NGS data.

### Live Scores

```python
scores = nfl.ngs.games.get_live_scores(
    season=2025,
    season_type="REG",
    week=1,
)
```

### Game Overview

Get NGS analytics for a specific game:

```python
overview = nfl.ngs.games.get_overview(game_id=2025091400)
```

## Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `season` | `int` | NFL season year |
| `season_type` | `str` | `"REG"`, `"PRE"`, or `"POST"` |
| `week` | `int \| None` | Week number (omit for season-level data) |
| `limit` | `int` | Maximum results for leader endpoints (default `20`) |

## NGS Concepts

Understanding the key NGS metrics:

- **Completion Probability** — The likelihood of a pass being completed based on distance, separation, and pressure
- **Expected Yards After Catch (xYAC)** — Predicted yards after catch based on receiver speed and positioning
- **Time to Throw** — Seconds from snap to pass release
- **Separation** — Distance in yards between receiver and nearest defender at the time of catch
- **Cushion** — Distance between receiver and defender at the snap
- **Max Speed** — Top speed reached during a play in miles per hour

## Error Handling

```python
from griddy.core.exceptions import NotFoundError

try:
    stats = nfl.ngs.stats.get_passing_stats(
        season=2025, season_type="REG", week=25
    )
except NotFoundError:
    print("Week does not exist")
```
