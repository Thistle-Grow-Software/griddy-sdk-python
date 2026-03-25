# NFL Pro Stats

The Pro Stats API (`pro.nfl.com`) provides advanced player and team statistics. These endpoints are accessed through `nfl.stats`, `nfl.betting`, and other pro-level sub-SDKs on the [`GriddyNFL`][griddy.nfl.sdk.GriddyNFL] client.

## Setup

```python
from griddy.nfl import GriddyNFL

nfl = GriddyNFL(nfl_auth={"accessToken": "your_token"})
```

## Passing Stats

Access passing statistics through `nfl.stats.passing`:

### Season Summary

```python
passing = nfl.stats.passing.get_season_summary(
    season=2025,
    season_type="REG",
    qualified_passer=True,
    limit=35,
)

for player in passing:
    print(f"{player.player_name}: {player.yards} yards, {player.touchdowns} TDs")
```

### Weekly Summary

```python
weekly_passing = nfl.stats.passing.get_weekly_summary(
    season=2025,
    season_type="REG",
    week="REG1",
    qualified_passer=True,
)
```

### Sorting and Filtering

All pro stats endpoints support sorting and team filtering:

```python
# Sort by touchdowns, descending
passing = nfl.stats.passing.get_season_summary(
    season=2025,
    season_type="REG",
    sort_key="tds",
    sort_value="DESC",
    qualified_passer=True,
)

# Filter by specific teams
passing = nfl.stats.passing.get_season_summary(
    season=2025,
    season_type="REG",
    team_offense=["PHI", "KC"],
)
```

## Rushing Stats

Access rushing statistics through `nfl.stats.rushing`:

```python
rushing = nfl.stats.rushing.get_season_summary(
    season=2025,
    season_type="REG",
    qualified_rusher=True,
    sort_key="yds",
    sort_value="DESC",
)

for player in rushing:
    print(f"{player.player_name}: {player.yards} yards")
```

### Weekly Rushing

```python
weekly_rushing = nfl.stats.rushing.get_weekly_summary(
    season=2025,
    season_type="REG",
    week="REG1",
)
```

## Receiving Stats

Access receiving statistics through `nfl.stats.receiving`:

```python
receiving = nfl.stats.receiving.get_season_summary(
    season=2025,
    season_type="REG",
    qualified_receiver=True,
)
```

### Weekly Receiving

```python
weekly_receiving = nfl.stats.receiving.get_weekly_summary(
    season=2025,
    season_type="REG",
    week="REG5",
    sort_key="rec",
    sort_value="DESC",
)
```

## Defense Stats

Defensive statistics are available through `nfl.stats.defense` and include overview stats, pass rush metrics, and nearest defender data.

### Defensive Overview

```python
# Season overview
defense = nfl.stats.defense.get_season_summary(
    season=2025,
    season_type="REG",
    qualified_defender=True,
    sort_key="snap",
)

# Weekly overview
weekly_defense = nfl.stats.defense.get_weekly_summary(
    season=2025,
    season_type="REG",
    week="REG10",
)
```

### Pass Rush Stats

```python
pass_rush = nfl.stats.defense.get_season_pass_rush_summary(
    season=2025,
    season_type="REG",
    sort_key="pr",
    sort_value="DESC",
)

weekly_pass_rush = nfl.stats.defense.get_weekly_pass_rush_summary(
    season=2025,
    season_type="REG",
    week="REG5",
)
```

### Nearest Defender Stats

```python
nearest_defender = nfl.stats.defense.get_season_nearest_defender_summary(
    season=2025,
    season_type="REG",
    sort_key="cov",
)

weekly_nearest = nfl.stats.defense.get_weekly_nearest_defender_summary(
    season=2025,
    season_type="REG",
    week="REG8",
)
```

## Team Stats

Team-level offensive and defensive statistics:

```python
# Team offense stats
team_offense = nfl.stats.team_offense.get_season_summary(
    season=2025,
    season_type="REG",
)

# Team defense stats
team_defense = nfl.stats.team_defense.get_season_summary(
    season=2025,
    season_type="REG",
)
```

## Fantasy Stats

```python
fantasy = nfl.stats.fantasy.get_season_summary(
    season=2025,
    season_type="REG",
)
```

## Betting Odds

Weekly betting odds are available through `nfl.betting`:

```python
odds = nfl.betting.get_weekly_betting_odds(
    season=2025,
    season_type="REG",
    week=1,
)
```

## Pagination

Pro Stats endpoints support pagination for large result sets:

```python
# First page
page1 = nfl.stats.passing.get_season_summary(
    season=2025,
    season_type="REG",
    limit=50,
    offset=0,
    page=1,
)

# Second page
page2 = nfl.stats.passing.get_season_summary(
    season=2025,
    season_type="REG",
    limit=50,
    offset=50,
    page=2,
)
```

## Common Parameters

Pro Stats endpoints share these parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `season` | `int` | NFL season year |
| `season_type` | `str` | `"REG"`, `"PRE"`, or `"POST"` |
| `week` | `str` | Week slug (e.g., `"REG1"`, `"POST1"`) — weekly endpoints only |
| `limit` | `int` | Results per page (default varies by endpoint) |
| `offset` | `int` | Number of records to skip |
| `page` | `int` | Page number |
| `sort_key` | `str` | Field to sort by (varies by stat type) |
| `sort_value` | `str` | `"ASC"` or `"DESC"` |
| `qualified_passer` | `bool` | Filter to qualified passers only |
| `qualified_rusher` | `bool` | Filter to qualified rushers only |
| `qualified_receiver` | `bool` | Filter to qualified receivers only |
| `qualified_defender` | `bool` | Filter to qualified defenders only |
| `team_offense` | `list[str]` | Filter by team abbreviations (e.g., `["PHI", "KC"]`) |
| `team_defense` | `list[str]` | Filter by defensive team abbreviations |

## Error Handling

```python
from griddy.core.exceptions import AuthenticationError, RateLimitError

try:
    stats = nfl.stats.passing.get_season_summary(
        season=2025, season_type="REG"
    )
except AuthenticationError:
    print("Token expired — re-authenticate")
except RateLimitError as e:
    print(f"Rate limited — retry after {e.retry_after}s")
```
