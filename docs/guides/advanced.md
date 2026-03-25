# Advanced Usage

This guide covers custom hooks, request manipulation, and extending the SDK for advanced use cases.

## Custom Hooks

The SDK's hook system lets you intercept and modify requests and responses. Hooks implement one of four interfaces:

| Interface | Method | When It Runs |
|-----------|--------|-------------|
| `SDKInitHook` | `sdk_init()` | SDK initialization |
| `BeforeRequestHook` | `before_request()` | Before every HTTP request |
| `AfterSuccessHook` | `after_success()` | After a successful response |
| `AfterErrorHook` | `after_error()` | After an error response |

### Creating a Custom Hook

Implement the hook interface and register it:

```python
import httpx
from griddy.core.hooks import BeforeRequestHook, BeforeRequestContext

class LoggingHook(BeforeRequestHook):
    def before_request(
        self,
        hook_ctx: BeforeRequestContext,
        request: httpx.Request,
    ) -> httpx.Request:
        print(f"[{hook_ctx.operation_id}] {request.method} {request.url}")
        return request
```

### Registering Hooks

Hooks are registered through the SDK's hook system at initialization time. The built-in `HackAuthHook` is automatically registered for NFL requests and handles authentication headers and token refresh.

## Custom HTTP Headers

Pass additional headers per request:

```python
games = nfl.games.get_games(
    season=2025,
    season_type="REG",
    week=1,
    http_headers={"X-Custom-Header": "value"},
)
```

## Request Timeouts

Override the default timeout for individual requests:

```python
# Per-request timeout (milliseconds)
games = nfl.games.get_games(
    season=2025,
    season_type="REG",
    week=1,
    timeout_ms=30000,
)
```

Or set it SDK-wide:

```python
nfl = GriddyNFL(
    nfl_auth={"accessToken": "token"},
    timeout_ms=60000,
)
```

## Custom Server URLs

Override the default API server URL:

```python
# Per-request override
games = nfl.games.get_games(
    season=2025,
    season_type="REG",
    week=1,
    server_url="https://custom-api.example.com",
)
```

Or at initialization:

```python
nfl = GriddyNFL(
    nfl_auth={"accessToken": "token"},
    server_url="https://custom-api.example.com",
)
```

## Custom HTTP Client

Provide your own `httpx` client for full control over connection settings:

```python
import httpx
from griddy.nfl import GriddyNFL

client = httpx.Client(
    timeout=httpx.Timeout(30.0),
    limits=httpx.Limits(max_connections=10),
    follow_redirects=True,
)

nfl = GriddyNFL(
    nfl_auth={"accessToken": "token"},
    client=client,
)
```

For async, provide an async client:

```python
async_client = httpx.AsyncClient(
    timeout=httpx.Timeout(30.0),
    limits=httpx.Limits(max_connections=10),
)

nfl = GriddyNFL(
    nfl_auth={"accessToken": "token"},
    async_client=async_client,
)
```

## Debug Logging

Enable debug logging to see request and response details:

```python
import logging

logger = logging.getLogger("griddy")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

nfl = GriddyNFL(
    nfl_auth={"accessToken": "token"},
    debug_logger=logger,
)
```

You can also enable debug logging via environment variables:

```bash
export GRIDDY_DEBUG=1         # NFL SDK debug logging
export GRIDDY_PFR_DEBUG=1     # PFR SDK debug logging
export GRIDDY_DRAFTBUZZ_DEBUG=1  # DraftBuzz SDK debug logging
```

## Retry Configuration

Customize retry behavior for transient failures:

```python
from griddy.core.types import RetryConfig

nfl = GriddyNFL(
    nfl_auth={"accessToken": "token"},
    retry_config=RetryConfig(
        strategy="backoff",
        backoff={
            "initial_interval": 500,
            "max_interval": 60000,
            "exponent": 1.5,
            "max_elapsed_time": 300000,
        },
        retry_connection_errors=True,
    ),
)
```

Override retries per request:

```python
games = nfl.games.get_games(
    season=2025,
    season_type="REG",
    week=1,
    retries=RetryConfig(strategy="none"),  # Disable retries
)
```

## PFR Scraping Backend

The PFR SDK allows injecting custom scraping backends:

```python
from griddy.pfr import GriddyPFR

pfr = GriddyPFR(
    scraping_backend=my_custom_sync_backend,
    async_scraping_backend=my_custom_async_backend,
)
```

This is useful for testing, caching, or using alternative rendering services.
