"""Tests to verify narrative documentation guides structure and content."""

import re
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"
GUIDES_DIR = DOCS_DIR / "guides"
ZENSICAL_PATH = PROJECT_ROOT / "zensical.toml"

# All guide files that must exist per TGF-259
REQUIRED_GUIDES = [
    "nfl-regular-api.md",
    "nfl-pro-stats.md",
    "nfl-ngs.md",
    "pfr.md",
    "authentication.md",
    "error-handling.md",
    "async.md",
    "architecture.md",
    "advanced.md",
]

# Python code block pattern
CODE_BLOCK_PATTERN = re.compile(r"```python\n(.*?)```", re.DOTALL)


def _load_zensical() -> dict:
    with open(ZENSICAL_PATH, "rb") as f:
        return tomllib.load(f)


def _count_code_examples(filepath: Path) -> int:
    """Count Python code blocks in a markdown file."""
    content = filepath.read_text()
    return len(CODE_BLOCK_PATTERN.findall(content))


class TestGuideFilesExist:
    """All required guide files must exist."""

    def test_getting_started_exists(self):
        assert (DOCS_DIR / "getting-started.md").is_file()

    def test_index_exists(self):
        assert (DOCS_DIR / "index.md").is_file()

    def test_all_guide_files_exist(self):
        for filename in REQUIRED_GUIDES:
            assert (GUIDES_DIR / filename).is_file(), f"Missing guide: {filename}"

    def test_markdown_placeholder_removed(self):
        assert not (DOCS_DIR / "markdown.md").exists(), (
            "Placeholder markdown.md should be removed"
        )


class TestLandingPage:
    """The landing page provides overview and links to guides."""

    def test_landing_page_has_overview(self):
        content = (DOCS_DIR / "index.md").read_text()
        assert "## Overview" in content or "## Quick Start" in content

    def test_landing_page_links_to_guides(self):
        content = (DOCS_DIR / "index.md").read_text()
        assert "getting-started.md" in content
        assert "guides/nfl-regular-api.md" in content
        assert "guides/nfl-pro-stats.md" in content
        assert "guides/nfl-ngs.md" in content
        assert "guides/pfr.md" in content

    def test_landing_page_links_to_api_reference(self):
        content = (DOCS_DIR / "index.md").read_text()
        assert "reference/" in content


class TestGettingStartedGuide:
    """Getting started guide covers install, auth, and first call."""

    def test_has_installation_section(self):
        content = (DOCS_DIR / "getting-started.md").read_text()
        assert "## Installation" in content
        assert "pip install" in content

    def test_has_authentication_section(self):
        content = (DOCS_DIR / "getting-started.md").read_text()
        assert "Authentication" in content

    def test_documents_both_auth_methods(self):
        content = (DOCS_DIR / "getting-started.md").read_text()
        assert "authenticate_via_browser" in content
        assert "accessToken" in content

    def test_has_first_api_call(self):
        content = (DOCS_DIR / "getting-started.md").read_text()
        assert "get_games" in content

    def test_has_code_examples(self):
        count = _count_code_examples(DOCS_DIR / "getting-started.md")
        assert count >= 3, f"Expected at least 3 code examples, got {count}"


class TestNFLRegularGuide:
    """NFL Regular API guide has at least 3 code examples."""

    def test_has_minimum_code_examples(self):
        count = _count_code_examples(GUIDES_DIR / "nfl-regular-api.md")
        assert count >= 3, f"Expected at least 3 code examples, got {count}"

    def test_covers_games(self):
        content = (GUIDES_DIR / "nfl-regular-api.md").read_text()
        assert "get_games" in content

    def test_covers_rosters(self):
        content = (GUIDES_DIR / "nfl-regular-api.md").read_text()
        assert "get_rosters" in content

    def test_covers_standings(self):
        content = (GUIDES_DIR / "nfl-regular-api.md").read_text()
        assert "get_standings" in content

    def test_covers_draft(self):
        content = (GUIDES_DIR / "nfl-regular-api.md").read_text()
        assert "draft" in content.lower()

    def test_covers_combine(self):
        content = (GUIDES_DIR / "nfl-regular-api.md").read_text()
        assert "combine" in content.lower()


class TestNFLProStatsGuide:
    """NFL Pro Stats guide has at least 3 code examples."""

    def test_has_minimum_code_examples(self):
        count = _count_code_examples(GUIDES_DIR / "nfl-pro-stats.md")
        assert count >= 3, f"Expected at least 3 code examples, got {count}"

    def test_covers_passing(self):
        content = (GUIDES_DIR / "nfl-pro-stats.md").read_text()
        assert "passing" in content.lower()

    def test_covers_rushing(self):
        content = (GUIDES_DIR / "nfl-pro-stats.md").read_text()
        assert "rushing" in content.lower()

    def test_covers_receiving(self):
        content = (GUIDES_DIR / "nfl-pro-stats.md").read_text()
        assert "receiving" in content.lower()

    def test_covers_defense(self):
        content = (GUIDES_DIR / "nfl-pro-stats.md").read_text()
        assert "defense" in content.lower()

    def test_covers_betting(self):
        content = (GUIDES_DIR / "nfl-pro-stats.md").read_text()
        assert "betting" in content.lower()


class TestNFLNgsGuide:
    """NGS guide has at least 3 code examples."""

    def test_has_minimum_code_examples(self):
        count = _count_code_examples(GUIDES_DIR / "nfl-ngs.md")
        assert count >= 3, f"Expected at least 3 code examples, got {count}"

    def test_covers_stats(self):
        content = (GUIDES_DIR / "nfl-ngs.md").read_text()
        assert "nfl.ngs.stats" in content

    def test_covers_leaders(self):
        content = (GUIDES_DIR / "nfl-ngs.md").read_text()
        assert "nfl.ngs.leaders" in content

    def test_covers_ngs_concepts(self):
        content = (GUIDES_DIR / "nfl-ngs.md").read_text()
        assert (
            "Completion Probability" in content or "completion probability" in content
        )


class TestPFRGuide:
    """PFR guide documents Browserless setup, rate limiting, and has code examples."""

    def test_has_minimum_code_examples(self):
        count = _count_code_examples(GUIDES_DIR / "pfr.md")
        assert count >= 2, f"Expected at least 2 code examples, got {count}"

    def test_documents_browserless_setup(self):
        content = (GUIDES_DIR / "pfr.md").read_text()
        assert "BROWSERLESS_HOST" in content
        assert "BROWSERLESS_TOKEN" in content

    def test_documents_rate_limiting(self):
        content = (GUIDES_DIR / "pfr.md").read_text()
        assert "rate limit" in content.lower() or "Rate Limiting" in content


class TestAuthenticationGuide:
    """Auth guide documents both auth methods and env vars."""

    def test_documents_direct_token(self):
        content = (GUIDES_DIR / "authentication.md").read_text()
        assert "accessToken" in content

    def test_documents_browser_auth(self):
        content = (GUIDES_DIR / "authentication.md").read_text()
        assert "authenticate_via_browser" in content

    def test_documents_environment_variables(self):
        content = (GUIDES_DIR / "authentication.md").read_text()
        assert "NFL_LOGIN_EMAIL" in content or "environment variable" in content.lower()

    def test_documents_token_refresh(self):
        content = (GUIDES_DIR / "authentication.md").read_text()
        assert "refreshToken" in content or "refresh" in content.lower()


class TestErrorHandlingGuide:
    """Error handling guide references exception classes."""

    def test_documents_exception_hierarchy(self):
        content = (GUIDES_DIR / "error-handling.md").read_text()
        assert "GriddyError" in content
        assert "APIError" in content
        assert "RateLimitError" in content
        assert "NotFoundError" in content
        assert "AuthenticationError" in content

    def test_references_nfl_errors(self):
        content = (GUIDES_DIR / "error-handling.md").read_text()
        assert "GriddyNFLDefaultError" in content

    def test_references_pfr_errors(self):
        content = (GUIDES_DIR / "error-handling.md").read_text()
        assert "ParsingError" in content

    def test_has_code_examples(self):
        count = _count_code_examples(GUIDES_DIR / "error-handling.md")
        assert count >= 2, f"Expected at least 2 code examples, got {count}"


class TestCodeExamplesSyntax:
    """All code examples should be syntactically valid Python."""

    @staticmethod
    def _dedent_block(block: str) -> str:
        """Remove common leading whitespace (handles admonition-indented blocks)."""
        import textwrap

        return textwrap.dedent(block)

    @staticmethod
    def _wrap_for_compile(block: str) -> str:
        """Wrap block in async def if it contains await, so compile succeeds."""
        if "await " in block or "async with " in block or "async for " in block:
            indented = "\n".join("    " + line for line in block.splitlines())
            return f"async def _wrapper():\n{indented}\n"
        return block

    def test_all_code_examples_are_valid_python(self):
        all_files = [DOCS_DIR / "index.md", DOCS_DIR / "getting-started.md"]
        all_files.extend(GUIDES_DIR / f for f in REQUIRED_GUIDES)

        errors = []
        for filepath in all_files:
            content = filepath.read_text()
            blocks = CODE_BLOCK_PATTERN.findall(content)
            for i, block in enumerate(blocks):
                cleaned = self._dedent_block(block).strip()
                if not cleaned:
                    continue
                compilable = self._wrap_for_compile(cleaned)
                try:
                    compile(compilable, f"{filepath.name}:block{i}", "exec")
                except SyntaxError as e:
                    errors.append(f"{filepath.name} block {i}: {e}")

        assert not errors, "Syntax errors in code examples:\n" + "\n".join(errors)


class TestZensicalNavigation:
    """zensical.toml navigation includes all new pages."""

    def _flatten_nav_values(self, nav_items: list) -> list[str]:
        """Recursively extract all string values from nav structure."""
        values = []
        for item in nav_items:
            if isinstance(item, dict):
                for v in item.values():
                    if isinstance(v, str):
                        values.append(v)
                    elif isinstance(v, list):
                        values.extend(self._flatten_nav_values(v))
        return values

    def test_nav_includes_getting_started(self):
        config = _load_zensical()
        values = self._flatten_nav_values(config["project"]["nav"])
        assert "getting-started.md" in values

    def test_nav_includes_all_guides(self):
        config = _load_zensical()
        values = self._flatten_nav_values(config["project"]["nav"])
        for guide in REQUIRED_GUIDES:
            expected = f"guides/{guide}"
            assert expected in values, f"Missing from nav: {expected}"

    def test_nav_has_guides_section(self):
        config = _load_zensical()
        nav = config["project"]["nav"]
        nav_keys = []
        for item in nav:
            nav_keys.extend(item.keys())
        assert "Guides" in nav_keys
