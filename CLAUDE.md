# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
The Griddy SDK is a Python library that provides a unified SDK for various American Football data sources. 

- **Python 3.14+**, managed with **uv**
- **Pydantic**

## Environment Variables
The following environment variables are of particular interest to this project:

- `NFL_LOGIN_EMAIL` - Email associated with an NFL.com account that has NFL Pro Access
- `NFL_LOGIN_PASSWORD` - Password for the aforementioned NFL.com account.
- `AWS_CODEARTIFACT_TOKEN` - Authentication token used for interacting with AWS CodeArtifact PyPi repository
- `UV_INDEX_PRIVATE_REGISTRY_USERNAME` - Username used by `uv` when interacting with CodeArtifact
- `UV_INDEX_PRIVATE_REGISTRY_PASSWORD` - Same value as `AWS_CODEARTIFACT_TOKEN`, used by `uv` to interact with CodeArtifact
- `ISSUE_PREFIX` - Used by the `tgf-commit` function (described in the next section) to create commit messages that will be linked to Jira issues properly.

The following environment variables are extracted from real world requests made when browsing NFL.com. At least for now they will always be the same for all environments.

- `NFL_API_KEY`
- `NFL_SDK_BUILD`
- `NFL_CLIENT_KEY`
- `NFL_CLIENT_SECRET`

## Custom Shell Functions and Aliases (from ~/.bashrc and ~/.bash_functions)
- `artifact-token` - Initializes necessary authentication info for interacting with AWS CodeArtifact. Usage: `artifact-token`
- `griddy` - Navigates to the project directory, sets project specific env vars, and invokes `artifact-token`. Usage: `griddy`
- `tgf-format` - Runs `isort` and `black` _in the current directory_. Usage: `tgf-format`
- `tgf-commit` - Stages, commits (signed), and pushes changes in one step. Enforces Conventional Commit formatting derived from the current branch name. Usage: `tgf-commit [-y] [-p|--pull-request] <message>` See `tgf-commit --help` for more.

## Git Conventions

- **Always run `tgf-format` before committing.**
- **Always use `tgf-commit` to commit changes.** It will automatically handle commit message formatting, and can create pull requests for you automatically. 

### Branch Naming Conventions
- All branches should be prefixed with the `<type>` of issue it addresses. Valid types are `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`, `style`, `perf`, and `build`.
- `<type>` should be followed by `/<$ISSUE_PREFIX>-<ISSUE NUMBER>`, and finally end with `-<short-description>`

### Examples

- `feat/TGS-31-player-stats`
- `docs/TGS-50-update-usage-docs`

It is crucial to follow this branch naming convention, as the `tgf-commit` command uses the branch name to form commit messages.

## Working Conventions
- When context usage exceeds 60%, proactively summarize current task state under "## Current Task" in this file
- Run /compact proactively rather than waiting for the context limit
- Always use `tgf-format` before commiting changes and `tgf-commit` to commit changes.
- Ensure that `version` is updated in `pyproject.toml` as part of any pull request.
- Run `uv lock` before committing any time `pyproject.toml` has been modified.

## Build and Test Commands

```bash
uv sync --all-groups                        # Install with all dependencies
uv run pytest                                          # Run all tests (includes coverage)
uv run pytest tests/test_nfl/unit/test_sdk.py          # Run a single test file
uv run pytest tests/test_nfl/unit/test_sdk.py::TestClass::test_name  # Run a single test
uv run pytest -m "not integration"                     # Skip integration tests (hit real APIs)
uv run pytest -m integration                           # Run only integration tests
tgf-format                                      # Format code
```

Coverage is enabled by default in pyproject.toml (`--cov=src/griddy`). Test markers: `unit`, `integration`, `slow`.

## Architecture

The SDK has two main clients: `GriddyNFL` for NFL.com APIs and `GriddyPFR` for Pro Football Reference (HTML scraping).

### Entry Point and Lazy Loading

`GriddyNFL` (in `nfl/sdk.py`) is the main NFL client. `GriddyPFR` (in `pfr/sdk.py`) is the PFR client. Both use `__getattr__` with a `_sub_sdk_map` dict to lazily instantiate sub-SDKs on first attribute access. Each sub-SDK maps an attribute name to a `(module_path, class_name)` tuple. On first access, the module is dynamically imported, the class is instantiated with the shared `SDKConfiguration`, and cached via `setattr`. This same pattern is repeated in `NextGenStats` and `StatsSDK` for their own nested sub-SDKs.

### NFL SDK: Three API Tiers with Different Base URLs

The NFL SDK talks to three different NFL API servers, configured in `nfl/sdkconfiguration.py:SERVERS`:
- **regular** (`api.nfl.com`) - Public endpoints. Endpoint classes extend `BaseSDK` directly.
- **pro** (`pro.nfl.com`) - Advanced stats. Endpoint classes extend `ProSDK`, which sets `server_type = "pro"` on init.
- **ngs** (`nextgenstats.nfl.com`) - Next Gen Stats. Endpoint classes extend `NgsBaseSDK`, which overrides `_resolve_base_url`.

The `server_type` field on `SDKConfiguration` determines which base URL is used via `get_server_details()`.

### NFL Endpoint Implementation Pattern

Every NFL endpoint follows a three-method pattern (see `nfl/endpoints/pro/stats/passing.py` for a complete example):
1. `_get_<name>_config()` - Builds an `EndpointConfig` dataclass with method, path, request model, response type, and error codes.
2. `get_<name>()` - Sync version: calls `_get_<name>_config()` then `self._execute_endpoint(config)`.
3. `get_<name>_async()` - Async version: calls `_get_<name>_config()` then `await self._execute_endpoint_async(config)`.

`_execute_endpoint` / `_execute_endpoint_async` in `nfl/basesdk.py` handle URL resolution, request building, hooks, retries, and response unmarshalling. New endpoints only need to define the config and the two thin wrappers.

### PFR SDK Architecture

`GriddyPFR` (in `pfr/sdk.py`) scrapes Pro Football Reference HTML pages via Browserless + Playwright. Sub-SDKs: `games` (boxscores) and `schedule` (season schedules).

PFR endpoints follow a similar pattern to NFL endpoints but use a PFR-specific `EndpointConfig` (in `pfr/basesdk.py`) with `path_template`, `wait_for_element` (CSS selector), and a `parser` callable. `_execute_endpoint` builds the URL, fetches HTML via Browserless, and runs the parser. The endpoint method then validates the parsed dict into a Pydantic model via `model_validate()`.

PFR models live in `pfr/models/entities/` with the same Pydantic BaseModel + TypedDict pattern as NFL models. Key models: `GameDetails` (full boxscore data), `ScheduleGame` (season schedule entries).

### Request/Response Hooks

The `_hooks/` system provides lifecycle hooks (SDKInit, BeforeRequest, AfterSuccess, AfterError). Hooks are registered in `_hooks/registration.py`. Currently `HackAuthHook` is the only registered hook for the NFL SDK - it runs before every request to add required headers (referer, sec-fetch-*) and auto-refreshes expired auth tokens using the refresh token.

### Models

All request/response models are Pydantic v2 models in `nfl/models/` and `pfr/models/`. Each model module has both a Pydantic `BaseModel` class and a corresponding `TypedDict` class. Models use `Field(alias=...)` where JSON keys differ from Python field names. The `models/__init__.py` files use dynamic imports via `_dynamic_imports` dicts for lazy loading. Request models use `Annotated` types with `Field` for query parameter metadata. Shared error code constants live in `_constants.py`.

### Authentication

NFL: pass `nfl_auth={"accessToken": ..., "refreshToken": ..., "expiresIn": ...}` directly, or provide `login_email`/`login_password` for Playwright-based browser auth. The `HackAuthHook` handles token refresh automatically when the token is within 30 seconds of expiring.

PFR: currently does not require authentication.

### Error Hierarchy

`core/exceptions.py` defines: `GriddyError` (base) -> `APIError`, `RateLimitError`, `NotFoundError`, `AuthenticationError`, `ValidationError`. The NFL SDK also has `errors.GriddyNFLDefaultError` used by `basesdk.py` for API response errors. The PFR SDK has `errors.GriddyPFRDefaultError` and `errors.NoResponseError`.

## Code Style

- Black (line-length 88), isort (black profile), mypy strict (`disallow_untyped_defs`)
- `Annotated` types with Pydantic `Field` for model metadata
- Tests in `tests/` mirror `src/` structure; fixtures in `tests/conftest.py`

## Environment Variables

- `NFL_API_KEY`, `NFL_CLIENT_KEY`, `NFL_CLIENT_SECRET` - API credentials (loaded in `settings.py`)
- `NFL_LOGIN_EMAIL`, `NFL_LOGIN_PASSWORD` - For browser-based auth
