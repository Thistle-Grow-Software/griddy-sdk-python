# Error Handling

The Griddy SDK uses a structured exception hierarchy so you can catch errors at the right level of granularity.

## Exception Hierarchy

All SDK exceptions inherit from [`GriddyError`][griddy.core.exceptions.GriddyError]:

```
GriddyError
├── APIError                  # General API request failures
├── RateLimitError            # Rate limit exceeded (429)
├── NotFoundError             # Resource not found (404)
├── AuthenticationError       # Auth failed (401)
└── ValidationError           # Request validation failures
```

Each SDK domain also has its own error classes:

```
GriddyNFLError                # Base NFL error
├── GriddyNFLDefaultError     # NFL API response error
├── NoResponseError           # Empty response body
└── ResponseValidationError   # Pydantic validation failure

GriddyPFRError                # Base PFR error
├── GriddyPFRDefaultError     # PFR scraping error
├── ParsingError              # HTML parser failure
├── NoResponseError           # Empty response body
└── ResponseValidationError   # Pydantic validation failure
```

## Core Exceptions

### GriddyError

The base class for all SDK exceptions. Every exception includes:

```python
from griddy.core.exceptions import GriddyError

try:
    result = nfl.games.get_games(season=2025, season_type="REG", week=1)
except GriddyError as e:
    print(f"Message: {e.message}")
    print(f"Status code: {e.status_code}")
    print(f"Response data: {e.response_data}")
```

| Attribute | Type | Description |
|-----------|------|-------------|
| `message` | `str` | Human-readable error description |
| `status_code` | `int \| None` | HTTP status code, if applicable |
| `response_data` | `dict \| None` | Raw API response body, if available |

### AuthenticationError

Raised when authentication fails (HTTP 401) or when token refresh fails:

```python
from griddy.core.exceptions import AuthenticationError

try:
    games = nfl.games.get_games(season=2025, season_type="REG", week=1)
except AuthenticationError:
    # Re-authenticate
    nfl = GriddyNFL.authenticate_via_browser(
        login_email=email,
        login_password=password,
        headless=True,
    )
```

### RateLimitError

Raised when you hit the API rate limit (HTTP 429). Includes a `retry_after` field:

```python
import time
from griddy.core.exceptions import RateLimitError

try:
    stats = nfl.stats.passing.get_season_summary(
        season=2025, season_type="REG"
    )
except RateLimitError as e:
    if e.retry_after:
        print(f"Rate limited. Retry after {e.retry_after} seconds.")
        time.sleep(e.retry_after)
```

### NotFoundError

Raised when a resource is not found (HTTP 404):

```python
from griddy.core.exceptions import NotFoundError

try:
    box_score = nfl.games.get_box_score(game_id="invalid_id")
except NotFoundError:
    print("Game not found")
```

### ValidationError

Raised when request parameters fail validation:

```python
from griddy.core.exceptions import ValidationError

try:
    result = nfl.stats.passing.get_season_summary(
        season=-1, season_type="INVALID"
    )
except ValidationError as e:
    print(f"Invalid parameters: {e}")
```

## NFL-Specific Errors

```python
from griddy.nfl.errors import (
    GriddyNFLDefaultError,
    NoResponseError,
    ResponseValidationError,
)
```

- **`GriddyNFLDefaultError`** — Wraps non-success API responses with the full response body
- **`NoResponseError`** — The API returned an empty response body
- **`ResponseValidationError`** — The API response didn't match the expected Pydantic model schema

## PFR-Specific Errors

```python
from griddy.pfr.errors import (
    ParsingError,
    NoResponseError,
    ResponseValidationError,
)
```

[`ParsingError`][griddy.pfr.errors.ParsingError] is unique to PFR and includes the URL that failed:

```python
from griddy.pfr.errors import ParsingError

try:
    game = pfr.games.get_game_details(game_id="invalid")
except ParsingError as e:
    print(f"Failed to parse: {e.url}")
```

## Catching Errors at Different Levels

Catch broadly or narrowly depending on your needs:

```python
from griddy.core.exceptions import GriddyError, AuthenticationError, RateLimitError

try:
    games = nfl.games.get_games(season=2025, season_type="REG", week=1)
except AuthenticationError:
    # Handle auth specifically
    pass
except RateLimitError:
    # Handle rate limits specifically
    pass
except GriddyError:
    # Catch everything else from the SDK
    pass
```

## Retry Configuration

Override the default retry behavior per request:

```python
from griddy.core.types import RetryConfig

games = nfl.games.get_games(
    season=2025,
    season_type="REG",
    week=1,
    retries=RetryConfig(
        strategy="backoff",
        backoff={"initial_interval": 500, "max_interval": 60000, "exponent": 1.5},
        retry_connection_errors=True,
    ),
)
```

Or configure it SDK-wide at initialization:

```python
nfl = GriddyNFL(
    nfl_auth={"accessToken": "token"},
    retry_config=RetryConfig(
        strategy="backoff",
        backoff={"initial_interval": 1000, "max_interval": 30000, "exponent": 1.5},
    ),
)
```
