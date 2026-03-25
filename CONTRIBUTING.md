# Contributing to Griddy SDK Python

Thank you for your interest in contributing to the Griddy SDK! This guide covers the development setup, coding standards, and workflows you need to know.

## Development Environment

### Prerequisites

- **Python 3.14+**
- **[uv](https://docs.astral.sh/uv/)** — Fast Python package manager and project tool

### Setup

```bash
git clone https://github.com/Thistle-Grow-Software/griddy-sdk-python.git
cd griddy-sdk-python

# Install all dependencies (dev + docs groups)
uv sync --all-groups
```

### Dependency Groups

The project uses uv dependency groups defined in `pyproject.toml`:

| Group | Purpose | Install |
|-------|---------|---------|
| (default) | Runtime dependencies | `uv sync` |
| `dev` | Testing, linting, type checking | `uv sync --group dev` |
| `docs` | Documentation (Zensical, mkdocstrings) | `uv sync --group docs` |

## Running Tests

```bash
# Run all tests (coverage enabled by default, integration tests excluded)
uv run pytest

# Run a single test file
uv run pytest tests/test_nfl/unit/test_sdk.py

# Run a single test
uv run pytest tests/test_nfl/unit/test_sdk.py::TestClass::test_name

# Run integration tests (hits real APIs)
uv run pytest -m integration

# Run with verbose output
uv run pytest -v
```

Test markers:

- `unit` — Unit tests (no external calls)
- `integration` — Integration tests (require network access)
- `slow` — Slow-running tests

Coverage is configured in `pyproject.toml` and runs automatically.

## Linting and Formatting

The project uses **Ruff** for both formatting and linting (replacing Black, isort, and flake8):

```bash
# Format code
ruff format src/ tests/

# Check linting
ruff check src/ tests/

# Auto-fix lint issues
ruff check --fix src/ tests/
```

Ruff configuration (from `pyproject.toml`):
- Line length: 88
- Import sorting: isort-compatible with `griddy` as first-party
- Target: Python 3.14

## Type Checking

The project uses **mypy** with strict settings:

```bash
mypy src/
```

Strict mode means:
- `disallow_untyped_defs` — All functions must have type annotations
- `disallow_incomplete_defs` — No partial annotations
- `warn_return_any` — Warn about `Any` returns
- `strict_equality` — Strict equality checks

## Branch Conventions

All branches must follow this naming convention:

```
<type>/<ISSUE_PREFIX>-<NUMBER>-<short-description>
```

Valid types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`, `style`, `perf`, `build`

Examples:
- `feat/TGS-31-player-stats`
- `docs/TGS-50-update-usage-docs`
- `fix/TGS-42-parsing-error`

The `tgf-commit` script uses the branch name to form Conventional Commit messages.

## Commit and PR Workflow

1. Create a branch following the naming convention above
2. Make your changes
3. Run formatting: `ruff format src/ tests/`
4. Run linting: `ruff check src/ tests/`
5. Run tests: `uv run pytest`
6. Commit using `tgf-commit`:

```bash
# Stage, commit, and push
tgf-commit -a "your commit message"

# Stage, commit, push, and create a PR
tgf-commit -a -p "your commit message"
```

`tgf-commit` automatically:
- Runs formatting before committing
- Prepends the commit type and issue number from the branch name
- Signs the commit
- Pushes to the remote

## Coding Standards

### Models

- Use **Pydantic v2** `BaseModel` classes
- Use `Field(alias="camelCaseKey")` for JSON key mapping
- Use `Annotated` types with `Field` for parameter metadata
- Provide a corresponding `TypedDict` alongside each model
- Use Google-style docstrings

### General

- All public functions must have type annotations
- Use `snake_case` for Python identifiers
- Follow existing patterns — look at similar modules before creating new ones

## Adding a New NFL Endpoint

Each NFL endpoint follows a three-method pattern. Here's how to add one:

### 1. Create the endpoint module

Create a new file in the appropriate tier directory:
- Regular API: `src/griddy/nfl/endpoints/regular/football/`
- Pro API: `src/griddy/nfl/endpoints/pro/`
- NGS: `src/griddy/nfl/endpoints/ngs/`

```python
# src/griddy/nfl/endpoints/regular/football/my_endpoint.py
from griddy.nfl.basesdk import BaseSDK
from griddy.nfl import models
from griddy.nfl.basesdk import EndpointConfig

class MyEndpoint(BaseSDK):
    def _get_data_config(
        self,
        *,
        season: int,
        # ... other parameters
    ) -> EndpointConfig:
        return EndpointConfig(
            method="GET",
            path="/football/v2/my-endpoint",
            operation_id="getMyEndpointData",
            request=models.MyRequest(season=season),
            response_type=models.MyResponse,
            error_status_codes={
                "400": models.ErrorResponse,
                "4XX": models.ErrorResponse,
                "5XX": models.ErrorResponse,
            },
        )

    def get_data(self, **kwargs):
        """Fetch data (sync)."""
        config = self._get_data_config(**kwargs)
        return self._execute_endpoint(config)

    async def get_data_async(self, **kwargs):
        """Fetch data (async)."""
        config = self._get_data_config(**kwargs)
        return await self._execute_endpoint_async(config)
```

### 2. Create request/response models

Add Pydantic models in `src/griddy/nfl/models/entities/`:

```python
# src/griddy/nfl/models/entities/my_model.py
from pydantic import BaseModel, Field

class MyRequest(BaseModel):
    season: int = Field(alias="season")

class MyResponse(BaseModel):
    data: list[dict] = Field(alias="data")
```

### 3. Register the sub-SDK

Add the endpoint to `_sub_sdk_map` in `src/griddy/nfl/sdk.py`:

```python
_sub_sdk_map = {
    # ... existing entries
    "my_endpoint": ("griddy.nfl.endpoints.regular.football.my_endpoint", "MyEndpoint"),
}
```

### 4. Write tests

Create tests in the appropriate `tests/` directory mirroring the `src/` structure.

## Adding a New PFR Parser

PFR parsers extract structured data from Pro Football Reference HTML pages.

### 1. Create the parser

```python
# src/griddy/pfr/parsers/my_parser.py
from bs4 import BeautifulSoup

def parse_my_page(html: str) -> dict:
    """Parse the PFR page and return structured data."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="my_table")
    # ... extract data from HTML
    return {"field": "value"}
```

### 2. Create the model

Add a Pydantic model in `src/griddy/pfr/models/entities/`.

### 3. Create the endpoint

```python
# src/griddy/pfr/endpoints/my_endpoint.py
from griddy.pfr.basesdk import PFRBaseSDK, EndpointConfig
from griddy.pfr.parsers.my_parser import parse_my_page

class MyEndpoint(PFRBaseSDK):
    def _get_data_config(self, *, param: str) -> EndpointConfig:
        return EndpointConfig(
            path_template="/path/{param}.htm",
            wait_for_element="#my_table",
            parser=parse_my_page,
            path_params={"param": param},
            response_type=MyModel,
        )

    def get_data(self, **kwargs):
        config = self._get_data_config(**kwargs)
        return self._execute_endpoint(config)

    async def get_data_async(self, **kwargs):
        config = self._get_data_config(**kwargs)
        return await self._execute_endpoint_async(config)
```

### 4. Register in GriddyPFR

Add to `_sub_sdk_map` in `src/griddy/pfr/sdk.py`.

## Documentation

### Local Preview

```bash
uv sync --group docs
uv run zensical serve
```

This starts a local server at `http://localhost:8000` with live reload.

### Building

```bash
uv run zensical build
```

The built site is output to `site/`.

### Structure

- `docs/index.md` — Landing page
- `docs/getting-started.md` — Getting started guide
- `docs/guides/` — Narrative guides
- `docs/reference/` — Auto-generated API reference (from docstrings via mkdocstrings)
- `zensical.toml` — Documentation configuration

API reference pages use `::: griddy.module.path` directives to auto-generate content from docstrings. When adding new public modules, create a corresponding `.md` file in `docs/reference/` and add it to the `nav` in `zensical.toml`.

## Changelog

The project uses [git-cliff](https://git-cliff.org/) to generate changelogs from Conventional Commit messages.

### Generating the Changelog

```bash
# Generate/update CHANGELOG.md
git cliff -o CHANGELOG.md

# Preview without writing
git cliff --dry-run
```

git-cliff is configured in `cliff.toml` and groups commits by type (Features, Bug Fixes, Documentation, etc.) based on the Conventional Commit prefix.

Since `tgf-commit` automatically formats commit messages as Conventional Commits (derived from the branch name), the changelog is generated automatically from the git history.
