# Authentication

The NFL.com API requires authentication for most endpoints. This guide covers both authentication methods, token lifecycle management, and best practices.

## Authentication Methods

### Direct Token

Pass a token you already have (e.g., extracted from browser DevTools):

```python
from griddy.nfl import GriddyNFL

nfl = GriddyNFL(nfl_auth={"accessToken": "your_access_token"})
```

The `nfl_auth` parameter accepts a dictionary or an [`NFLAuth`][griddy.nfl.models.NFLAuth] model with these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `accessToken` | `str` | Yes | Bearer token for API requests |
| `refreshToken` | `str` | No | Token used to generate new access tokens |
| `expiresIn` | `int` | No | Unix timestamp when the access token expires |
| `deviceId` | `str` | No | Device identifier (auto-generated if omitted) |

### Browser Authentication (Playwright)

Automate the full NFL.com login flow:

```python
from griddy.nfl import GriddyNFL

nfl = GriddyNFL.authenticate_via_browser(
    login_email="your_email@example.com",
    login_password="your_password",
    headless=True,
    save_credentials_path="credentials.json",
)
```

This method:

1. Launches a Chromium browser via Playwright
2. Navigates to the NFL.com login page
3. Fills in the email and password fields
4. Captures the authentication tokens from the response
5. Optionally saves the credentials to a JSON file

!!! warning "Playwright Dependency"
    Browser authentication requires the `browser-auth` extra:

    ```bash
    pip install "griddy[browser-auth]"
    playwright install chromium
    ```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `login_email` | `str` | — | NFL.com account email |
| `login_password` | `str` | — | NFL.com account password |
| `headless` | `bool` | `False` | Run browser without a visible window |
| `save_credentials_path` | `str \| None` | `None` | File path to save credentials JSON |

## Environment Variables

Store sensitive credentials as environment variables:

```bash
# NFL.com account credentials (for browser auth)
export NFL_LOGIN_EMAIL="your_email@example.com"
export NFL_LOGIN_PASSWORD="your_password"

# NFL API configuration (extracted from real requests)
export NFL_API_KEY="your_api_key"
export NFL_SDK_BUILD="your_sdk_build"
export NFL_CLIENT_KEY="your_client_key"
export NFL_CLIENT_SECRET="your_client_secret"
```

Then use them in your code:

```python
import os
from griddy.nfl import GriddyNFL

nfl = GriddyNFL.authenticate_via_browser(
    login_email=os.environ["NFL_LOGIN_EMAIL"],
    login_password=os.environ["NFL_LOGIN_PASSWORD"],
    headless=True,
)
```

## Token Refresh

When you provide a `refreshToken` and `expiresIn`, the SDK's [`HackAuthHook`][griddy.nfl._hooks.hack_auth.HackAuthHook] automatically handles token refresh:

- Before every request, the hook checks whether the access token is within **30 seconds** of expiring
- If expiring soon, it calls the NFL identity refresh endpoint to obtain a new token
- The new token is injected into the request transparently

```python
nfl = GriddyNFL(
    nfl_auth={
        "accessToken": "your_access_token",
        "refreshToken": "your_refresh_token",
        "expiresIn": 1735689600,
    }
)

# Even if the token expires mid-session, requests continue working
games = nfl.games.get_games(season=2025, season_type="REG", week=1)
```

!!! note
    If the refresh token itself is expired or invalid, the SDK raises an [`AuthenticationError`][griddy.core.exceptions.AuthenticationError].

## Credential Persistence

Save credentials to disk for reuse across sessions:

```python
import json
from pathlib import Path

# First run: authenticate and save
nfl = GriddyNFL.authenticate_via_browser(
    login_email="email@example.com",
    login_password="password",
    headless=True,
    save_credentials_path="credentials.json",
)

# Subsequent runs: load saved credentials
creds = json.loads(Path("credentials.json").read_text())
nfl = GriddyNFL(nfl_auth=creds)
```

!!! warning "Security"
    Never commit credential files to version control. Add `credentials.json` to your `.gitignore`.

## Required Headers

The SDK automatically adds the following headers to every NFL API request via the auth hook:

- `referer` — Set to the NFL.com origin
- `authority` — Set to the API host
- `sec-fetch-dest`, `sec-fetch-mode`, `sec-fetch-site` — Browser security headers
- `x-override-env` — Environment override header

You do not need to set these manually.

## PFR Authentication

The Pro Football Reference client does not require authentication:

```python
from griddy.pfr import GriddyPFR

pfr = GriddyPFR()  # No auth needed
schedule = pfr.schedule.get_season_schedule(season=2024)
```

PFR is a public website, but it does require a Browserless instance for rendering. See the [PFR Guide](pfr.md) for setup details.
