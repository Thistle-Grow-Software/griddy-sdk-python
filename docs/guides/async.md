# Async Usage

Every endpoint in the Griddy SDK has both a synchronous and an asynchronous version. Async methods have the same name as their sync counterparts with an `_async` suffix.

## Basic Usage

```python
import asyncio
from griddy.nfl import GriddyNFL

async def main():
    nfl = GriddyNFL(nfl_auth={"accessToken": "your_token"})

    games = await nfl.games.get_games_async(
        season=2025,
        season_type="REG",
        week=1,
    )

    for game in games:
        print(f"{game.away_team} @ {game.home_team}")

asyncio.run(main())
```

## Concurrent Requests

Use `asyncio.gather` to fetch multiple resources in parallel:

```python
import asyncio
from griddy.nfl import GriddyNFL

async def fetch_week_data(nfl: GriddyNFL, season: int, week: int):
    games, passing, rushing = await asyncio.gather(
        nfl.games.get_games_async(
            season=season, season_type="REG", week=week
        ),
        nfl.stats.passing.get_weekly_summary_async(
            season=season, season_type="REG", week=f"REG{week}"
        ),
        nfl.stats.rushing.get_weekly_summary_async(
            season=season, season_type="REG", week=f"REG{week}"
        ),
    )
    return games, passing, rushing

async def main():
    nfl = GriddyNFL(nfl_auth={"accessToken": "your_token"})
    games, passing, rushing = await fetch_week_data(nfl, 2025, 1)

asyncio.run(main())
```

## Fetching Multiple Weeks

```python
import asyncio
from griddy.nfl import GriddyNFL

async def fetch_all_weeks(nfl: GriddyNFL, season: int, weeks: list[int]):
    tasks = [
        nfl.games.get_games_async(
            season=season, season_type="REG", week=week
        )
        for week in weeks
    ]
    return await asyncio.gather(*tasks)

async def main():
    nfl = GriddyNFL(nfl_auth={"accessToken": "your_token"})
    all_games = await fetch_all_weeks(nfl, 2025, list(range(1, 19)))

    for week_games in all_games:
        for game in week_games:
            print(game)

asyncio.run(main())
```

## Async PFR

The PFR client also supports async:

```python
import asyncio
from griddy.pfr import GriddyPFR

async def main():
    pfr = GriddyPFR()

    schedule = await pfr.schedule.get_season_schedule_async(season=2024)

    # Fetch game details concurrently (be mindful of rate limits)
    game_ids = [game.game_id for game in schedule[:5]]
    games = await asyncio.gather(*[
        pfr.games.get_game_details_async(game_id=gid)
        for gid in game_ids
    ])

asyncio.run(main())
```

!!! warning "PFR Rate Limiting"
    While async allows concurrent requests, Pro Football Reference has rate limits. Avoid sending too many requests simultaneously. Use `asyncio.Semaphore` to control concurrency:

    ```python
    sem = asyncio.Semaphore(3)  # Max 3 concurrent requests

    async def fetch_game(pfr, game_id):
        async with sem:
            return await pfr.games.get_game_details_async(game_id=game_id)
    ```

## Context Managers

Use async context managers for proper resource cleanup:

```python
async def main():
    async with GriddyNFL(nfl_auth={"accessToken": "token"}) as nfl:
        games = await nfl.games.get_games_async(
            season=2025, season_type="REG", week=1
        )
```

## Error Handling in Async

Exception handling works the same way in both sync and async:

```python
from griddy.core.exceptions import AuthenticationError, RateLimitError

async def safe_fetch(nfl):
    try:
        return await nfl.games.get_games_async(
            season=2025, season_type="REG", week=1
        )
    except AuthenticationError:
        print("Token expired")
    except RateLimitError as e:
        print(f"Rate limited, retry after {e.retry_after}s")
```

## Mixing Sync and Async

You can use both sync and async methods on the same client instance. The SDK maintains separate HTTP clients for each:

```python
nfl = GriddyNFL(nfl_auth={"accessToken": "your_token"})

# Sync call
games = nfl.games.get_games(season=2025, season_type="REG", week=1)

# Async call (in an async context)
stats = await nfl.stats.passing.get_season_summary_async(
    season=2025, season_type="REG"
)
```
