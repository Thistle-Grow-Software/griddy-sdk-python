"""Tests to verify documentation dependencies are properly declared."""

import tomllib
from pathlib import Path

PYPROJECT_PATH = Path(__file__).resolve().parents[1] / "pyproject.toml"


def _load_pyproject() -> dict:
    with open(PYPROJECT_PATH, "rb") as f:
        return tomllib.load(f)


def test_docs_dependency_group_exists():
    """The docs dependency group must be declared in pyproject.toml."""
    data = _load_pyproject()
    groups = data.get("dependency-groups", {})
    assert "docs" in groups, "Missing [dependency-groups] docs in pyproject.toml"


def test_docs_group_contains_required_packages():
    """The docs group must include mkdocs, mkdocs-material, mkdocstrings, and mike."""
    data = _load_pyproject()
    docs_deps = data["dependency-groups"]["docs"]
    dep_names = {
        dep.split(">")[0].split("<")[0].split("[")[0].strip('"') for dep in docs_deps
    }
    for required in ("mkdocs", "mkdocs-material", "mkdocstrings", "mike"):
        assert required in dep_names, f"Missing required doc dependency: {required}"


def test_mkdocstrings_includes_python_extra():
    """mkdocstrings must include the [python] extra."""
    data = _load_pyproject()
    docs_deps = data["dependency-groups"]["docs"]
    mkdocstrings_entries = [d for d in docs_deps if d.startswith("mkdocstrings")]
    assert any("[python]" in entry for entry in mkdocstrings_entries), (
        "mkdocstrings must include [python] extra"
    )
