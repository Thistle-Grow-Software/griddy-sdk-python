"""Tests to verify API reference documentation structure and configuration."""

import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"
REFERENCE_DIR = DOCS_DIR / "reference"
ZENSICAL_PATH = PROJECT_ROOT / "zensical.toml"
WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "docs.yml"


def _load_zensical() -> dict:
    with open(ZENSICAL_PATH, "rb") as f:
        return tomllib.load(f)


class TestReferenceDirectoryStructure:
    """Verify all expected API reference directories and files exist."""

    def test_reference_index_exists(self):
        assert (REFERENCE_DIR / "index.md").is_file()

    def test_nfl_reference_pages_exist(self):
        nfl_dir = REFERENCE_DIR / "nfl"
        assert (nfl_dir / "index.md").is_file()
        assert (nfl_dir / "sdk.md").is_file()
        assert (nfl_dir / "models.md").is_file()
        assert (nfl_dir / "errors.md").is_file()

    def test_nfl_regular_endpoint_pages_exist(self):
        regular_dir = REFERENCE_DIR / "nfl" / "endpoints" / "regular"
        assert (regular_dir / "index.md").is_file()
        football_dir = regular_dir / "football"
        for name in (
            "combine",
            "draft",
            "games",
            "rosters",
            "standings",
            "teams",
            "venues",
            "weeks",
        ):
            assert (football_dir / f"{name}.md").is_file(), f"Missing {name}.md"

    def test_nfl_pro_endpoint_pages_exist(self):
        pro_dir = REFERENCE_DIR / "nfl" / "endpoints" / "pro"
        assert (pro_dir / "index.md").is_file()
        for name in (
            "betting",
            "content",
            "games",
            "players",
            "schedules",
            "teams",
            "transactions",
        ):
            assert (pro_dir / f"{name}.md").is_file(), f"Missing {name}.md"

    def test_nfl_pro_stats_pages_exist(self):
        stats_dir = REFERENCE_DIR / "nfl" / "endpoints" / "pro" / "stats"
        for name in (
            "passing",
            "rushing",
            "receiving",
            "defense",
            "fantasy",
            "team_defense",
            "team_offense",
        ):
            assert (stats_dir / f"{name}.md").is_file(), f"Missing {name}.md"

    def test_nfl_ngs_endpoint_pages_exist(self):
        ngs_dir = REFERENCE_DIR / "nfl" / "endpoints" / "ngs"
        assert (ngs_dir / "index.md").is_file()
        for name in ("content", "games", "leaders", "league", "news", "stats"):
            assert (ngs_dir / f"{name}.md").is_file(), f"Missing {name}.md"

    def test_pfr_reference_pages_exist(self):
        pfr_dir = REFERENCE_DIR / "pfr"
        assert (pfr_dir / "index.md").is_file()
        assert (pfr_dir / "sdk.md").is_file()
        assert (pfr_dir / "models.md").is_file()
        assert (pfr_dir / "parsers.md").is_file()
        assert (pfr_dir / "errors.md").is_file()

    def test_pfr_endpoint_pages_exist(self):
        endpoints_dir = REFERENCE_DIR / "pfr" / "endpoints"
        assert (endpoints_dir / "index.md").is_file()
        for name in (
            "awards",
            "coaches",
            "draft",
            "executives",
            "fantasy",
            "frivolities",
            "games",
            "hof",
            "leaders",
            "officials",
            "players",
            "probowl",
            "schedule",
            "schools",
            "seasons",
            "stadiums",
            "superbowl",
            "teams",
        ):
            assert (endpoints_dir / f"{name}.md").is_file(), f"Missing {name}.md"

    def test_draftbuzz_reference_pages_exist(self):
        db_dir = REFERENCE_DIR / "draftbuzz"
        assert (db_dir / "index.md").is_file()
        assert (db_dir / "sdk.md").is_file()
        assert (db_dir / "models.md").is_file()
        assert (db_dir / "errors.md").is_file()
        assert (db_dir / "endpoints" / "prospects.md").is_file()
        assert (db_dir / "endpoints" / "rankings.md").is_file()

    def test_core_reference_pages_exist(self):
        core_dir = REFERENCE_DIR / "core"
        assert (core_dir / "index.md").is_file()
        assert (core_dir / "exceptions.md").is_file()
        assert (core_dir / "httpclient.md").is_file()
        assert (core_dir / "utils.md").is_file()


class TestReferencePageContent:
    """Verify reference pages contain mkdocstrings directives."""

    def test_reference_pages_contain_mkdocstrings_directives(self):
        """Every .md file under docs/reference/ (except index) should have a ::: directive."""
        for md_file in REFERENCE_DIR.rglob("*.md"):
            if md_file.name == "index.md" and md_file.parent == REFERENCE_DIR:
                continue
            content = md_file.read_text()
            assert ":::" in content, (
                f"{md_file.relative_to(PROJECT_ROOT)} is missing a ::: mkdocstrings directive"
            )

    def test_nfl_sdk_page_references_correct_module(self):
        content = (REFERENCE_DIR / "nfl" / "sdk.md").read_text()
        assert "::: griddy.nfl.sdk" in content

    def test_pfr_sdk_page_references_correct_module(self):
        content = (REFERENCE_DIR / "pfr" / "sdk.md").read_text()
        assert "::: griddy.pfr.sdk" in content

    def test_draftbuzz_sdk_page_references_correct_module(self):
        content = (REFERENCE_DIR / "draftbuzz" / "sdk.md").read_text()
        assert "::: griddy.draftbuzz.sdk" in content

    def test_core_exceptions_page_references_correct_module(self):
        content = (REFERENCE_DIR / "core" / "exceptions.md").read_text()
        assert "::: griddy.core.exceptions" in content


class TestZensicalConfiguration:
    """Verify zensical.toml is correctly configured for API reference generation."""

    def test_repo_url_configured(self):
        config = _load_zensical()
        assert "repo_url" in config["project"]
        assert "github.com" in config["project"]["repo_url"]

    def test_edit_uri_configured(self):
        config = _load_zensical()
        assert "edit_uri" in config["project"]

    def test_content_action_edit_enabled(self):
        config = _load_zensical()
        features = config["project"]["theme"]["features"]
        assert "content.action.edit" in features

    def test_mkdocstrings_plugin_configured(self):
        config = _load_zensical()
        plugins = config["project"]["plugins"]
        assert "mkdocstrings" in plugins

    def test_mkdocstrings_python_handler_configured(self):
        config = _load_zensical()
        handlers = config["project"]["plugins"]["mkdocstrings"]["handlers"]
        assert "python" in handlers
        assert handlers["python"]["paths"] == ["src"]

    def test_mkdocstrings_handler_options(self):
        config = _load_zensical()
        options = config["project"]["plugins"]["mkdocstrings"]["handlers"]["python"][
            "options"
        ]
        assert options["docstring_style"] == "google"
        assert options["show_source"] is True
        assert options["show_root_heading"] is True

    def test_nav_contains_api_reference(self):
        config = _load_zensical()
        nav = config["project"]["nav"]
        nav_keys = []
        for item in nav:
            nav_keys.extend(item.keys())
        assert "API Reference" in nav_keys


class TestDocsWorkflow:
    """Verify the docs CI workflow includes src/** in path filters."""

    def test_workflow_includes_src_path(self):
        content = WORKFLOW_PATH.read_text()
        assert '"src/**"' in content

    def test_workflow_uses_uv_sync(self):
        content = WORKFLOW_PATH.read_text()
        assert "uv sync --group docs" in content

    def test_workflow_uses_uv_run_zensical(self):
        content = WORKFLOW_PATH.read_text()
        assert "uv run zensical build" in content
