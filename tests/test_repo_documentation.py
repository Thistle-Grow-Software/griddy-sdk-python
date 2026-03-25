"""Tests to verify repository documentation (README, CONTRIBUTING, CHANGELOG)."""

import re
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
README_PATH = PROJECT_ROOT / "README.md"
CONTRIBUTING_PATH = PROJECT_ROOT / "CONTRIBUTING.md"
CHANGELOG_PATH = PROJECT_ROOT / "CHANGELOG.md"
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
CLIFF_TOML_PATH = PROJECT_ROOT / "cliff.toml"


def _load_pyproject() -> dict:
    with open(PYPROJECT_PATH, "rb") as f:
        return tomllib.load(f)


def _get_pyproject_version() -> str:
    return _load_pyproject()["project"]["version"]


class TestReadmeVersionBadge:
    """README version badge must match pyproject.toml version."""

    def test_version_badge_matches_pyproject(self):
        version = _get_pyproject_version()
        content = README_PATH.read_text()
        expected = f"version-{version}-green"
        assert expected in content, (
            f"README version badge should contain '{expected}', "
            f"but pyproject version is {version}"
        )


class TestReadmeNoStaleReferences:
    """README should not contain stale mkdocs or GitHub Pages references."""

    def test_no_mkdocs_commands(self):
        content = README_PATH.read_text()
        assert "mkdocs serve" not in content
        assert "mkdocs build" not in content

    def test_uses_zensical_commands(self):
        content = README_PATH.read_text()
        assert "zensical serve" in content
        assert "zensical build" in content

    def test_no_github_pages_docs_url(self):
        content = README_PATH.read_text()
        assert "jkgriebel93.github.io" not in content

    def test_docs_url_points_to_thistlegrow(self):
        content = README_PATH.read_text()
        assert "docs.thistlegrow.com" in content

    def test_no_old_formatting_tools(self):
        content = README_PATH.read_text()
        # Should not reference black, isort, or flake8 directly
        assert "black src/" not in content
        assert "isort src/" not in content
        assert "flake8 src/" not in content

    def test_uses_ruff(self):
        content = README_PATH.read_text()
        assert "ruff format" in content or "ruff check" in content

    def test_uses_uv(self):
        content = README_PATH.read_text()
        assert "uv sync" in content

    def test_no_old_clone_url(self):
        content = README_PATH.read_text()
        assert "jkgriebel93/griddy-sdk-python" not in content


class TestContributingExists:
    """CONTRIBUTING.md must exist with required sections."""

    def test_file_exists(self):
        assert CONTRIBUTING_PATH.is_file()

    def test_has_dev_setup_section(self):
        content = CONTRIBUTING_PATH.read_text()
        assert "uv sync" in content
        assert "Python 3.14" in content

    def test_has_testing_section(self):
        content = CONTRIBUTING_PATH.read_text()
        assert "uv run pytest" in content

    def test_has_linting_section(self):
        content = CONTRIBUTING_PATH.read_text()
        assert "ruff format" in content
        assert "ruff check" in content

    def test_has_type_checking_section(self):
        content = CONTRIBUTING_PATH.read_text()
        assert "mypy" in content

    def test_has_branch_conventions(self):
        content = CONTRIBUTING_PATH.read_text()
        assert "feat" in content
        assert "fix" in content

    def test_has_new_endpoint_guide(self):
        content = CONTRIBUTING_PATH.read_text()
        assert (
            "Adding a New NFL Endpoint" in content
            or "new NFL endpoint" in content.lower()
        )

    def test_has_new_pfr_parser_guide(self):
        content = CONTRIBUTING_PATH.read_text()
        assert (
            "Adding a New PFR Parser" in content or "new PFR parser" in content.lower()
        )

    def test_has_docs_workflow(self):
        content = CONTRIBUTING_PATH.read_text()
        assert "zensical serve" in content
        assert "zensical build" in content

    def test_documents_changelog_workflow(self):
        content = CONTRIBUTING_PATH.read_text()
        assert "git-cliff" in content or "changelog" in content.lower()


class TestChangelogExists:
    """CHANGELOG.md must exist with recent release entries."""

    def test_file_exists(self):
        assert CHANGELOG_PATH.is_file()

    def test_has_at_least_two_releases(self):
        content = CHANGELOG_PATH.read_text()
        # Count version headers like ## [0.47.1]
        version_pattern = re.compile(r"^## \[\d+\.\d+\.\d+\]", re.MULTILINE)
        versions = version_pattern.findall(content)
        assert len(versions) >= 2, (
            f"CHANGELOG should have at least 2 release entries, found {len(versions)}"
        )

    def test_contains_current_or_recent_version(self):
        content = CHANGELOG_PATH.read_text()
        version = _get_pyproject_version()
        # Either the current version or one minor version back should be present
        assert version in content or "0.47" in content or "0.46" in content


class TestGitCliffConfig:
    """git-cliff configuration must be present and valid."""

    def test_cliff_toml_exists(self):
        assert CLIFF_TOML_PATH.is_file()

    def test_cliff_toml_is_valid(self):
        with open(CLIFF_TOML_PATH, "rb") as f:
            config = tomllib.load(f)
        assert "changelog" in config
        assert "git" in config

    def test_cliff_toml_uses_conventional_commits(self):
        with open(CLIFF_TOML_PATH, "rb") as f:
            config = tomllib.load(f)
        assert config["git"]["conventional_commits"] is True

    def test_cliff_toml_has_commit_parsers(self):
        with open(CLIFF_TOML_PATH, "rb") as f:
            config = tomllib.load(f)
        parsers = config["git"]["commit_parsers"]
        groups = [p["group"] for p in parsers]
        assert "Features" in groups
        assert "Bug Fixes" in groups
        assert "Documentation" in groups
