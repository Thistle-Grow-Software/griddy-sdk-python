# Architecture

This guide explains the internal architecture of the Griddy SDK for developers who want to understand how the SDK works or contribute to it.

## Client Structure

The SDK provides three main clients:

- [`GriddyNFL`][griddy.nfl.sdk.GriddyNFL] — NFL.com API client
- [`GriddyPFR`][griddy.pfr.sdk.GriddyPFR] — Pro Football Reference scraping client
- `GriddyDraftBuzz` — Draft prospect scraping client

Each client follows the same architectural patterns described below.

## Lazy-Loaded Sub-SDKs

All three clients use lazy loading to defer sub-SDK instantiation until first access. This keeps import time fast and memory usage low.

Each client defines a `_sub_sdk_map` dictionary mapping attribute names to `(module_path, class_name)` tuples:

```python
# From GriddyNFL
_sub_sdk_map = {
    "games": ("griddy.nfl.endpoints.regular.football.games", "Games"),
    "stats": ("griddy.nfl.endpoints.pro.stats", "StatsSDK"),
    "ngs": ("griddy.nfl.endpoints.ngs", "NextGenStats"),
    # ...
}
```

When you access `nfl.games`, Python's `__getattr__` triggers dynamic import of the module, instantiation of the class with the shared `SDKConfiguration`, and caching via `setattr`. Subsequent access returns the cached instance.

### Nested Sub-SDKs

Some sub-SDKs contain their own nested sub-SDKs:

- `nfl.stats` is a `StatsSDK` that lazily loads `passing`, `rushing`, `receiving`, `defense`, `team_offense`, `team_defense`, and `fantasy`
- `nfl.ngs` is a `NextGenStats` SDK that lazily loads `stats`, `leaders`, `games`, `league`, and `content`

This means `nfl.stats.passing.get_season_summary(...)` triggers two lazy loads: first `stats`, then `passing`.

## Three API Tiers

The NFL SDK communicates with three different NFL API servers:

| Tier | Base URL | SDK Base Class | Access Pattern |
|------|----------|---------------|----------------|
| Regular | `api.nfl.com` | `BaseSDK` | `nfl.games`, `nfl.rosters`, etc. |
| Pro | `pro.nfl.com` | `ProSDK` | `nfl.stats`, `nfl.betting`, etc. |
| NGS | `nextgenstats.nfl.com` | `NgsBaseSDK` | `nfl.ngs.stats`, `nfl.ngs.leaders`, etc. |

The `server_type` field on `SDKConfiguration` determines which base URL is used.

## Endpoint Pattern

Every endpoint follows a three-method pattern:

### 1. Config Method

Builds an `EndpointConfig` dataclass with the request metadata:

```python
def _get_games_config(self, *, season, season_type, week, **kwargs):
    return EndpointConfig(
        method="GET",
        path="/football/v2/games",
        request=models.GetGamesRequest(
            season=season,
            season_type=season_type,
            week=week,
        ),
        response_type=List[models.Game],
        error_status_codes={...},
    )
```

### 2. Sync Method

Calls the config method, then executes:

```python
def get_games(self, **kwargs):
    config = self._get_games_config(**kwargs)
    return self._execute_endpoint(config)
```

### 3. Async Method

Same pattern, but awaitable:

```python
async def get_games_async(self, **kwargs):
    config = self._get_games_config(**kwargs)
    return await self._execute_endpoint_async(config)
```

The `_execute_endpoint` and `_execute_endpoint_async` methods in `basesdk.py` handle URL resolution, request building, hook execution, retries, and response unmarshalling. New endpoints only need to define the config and the two thin wrappers.

## Hooks System

The SDK provides lifecycle hooks for intercepting requests and responses:

| Hook | When It Runs |
|------|-------------|
| `SDKInitHook` | When the SDK is initialized |
| `BeforeRequestHook` | Before every HTTP request is sent |
| `AfterSuccessHook` | After a successful response |
| `AfterErrorHook` | After an error response |

Hooks are registered in `_hooks/registration.py`. The primary built-in hook is `HackAuthHook`, which:

- Adds required browser-like headers to every request
- Auto-refreshes expired auth tokens before the request is sent

### Hook Context

Each hook receives a context object with metadata about the current operation:

```python
class BeforeRequestContext:
    operation_id: str       # Unique endpoint identifier
    security_source: Any    # Auth configuration
```

## PFR Scraping Pipeline

The PFR SDK follows a different flow than the NFL API:

1. **URL Construction** — Build URL from `path_template` and `path_params`
2. **HTML Fetching** — Browserless renders the page with a residential proxy
3. **Preprocessing** — Hidden `<table>` elements are uncommented
4. **Parsing** — Dedicated BeautifulSoup parsers extract structured data
5. **Validation** — Parsed dicts are validated into Pydantic models

Each PFR endpoint has:

- A `path_template` (e.g., `/years/{season}/games.htm`)
- A `wait_for_element` CSS selector (e.g., `#scoring`)
- A dedicated `parser` callable

## Models

All request and response models are Pydantic v2 `BaseModel` classes:

- **NFL models** live in `griddy.nfl.models`
- **PFR models** live in `griddy.pfr.models`
- Each model module also provides a corresponding `TypedDict` for flexibility

Key model patterns:

- `Field(alias="camelCaseKey")` for mapping JSON keys to snake_case Python attributes
- `Annotated` types with `Field` for query parameter metadata
- Lazy loading via `_dynamic_imports` dictionaries in `__init__.py` files

## Configuration

`SDKConfiguration` holds shared state across all sub-SDKs:

- HTTP client instances (sync and async)
- Authentication data
- Server URLs and type
- Retry configuration
- Debug logger
- Hook registrations
