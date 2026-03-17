"""Tests for PEP 561 type information and annotation accuracy.

Verifies that:
- The ``py.typed`` marker exists at the correct package root location.
- A ``.pyi`` stub ships for ``LazySubSDKMixin``.
- Every lazy-loaded attribute in ``_sub_sdk_map`` has a corresponding
  class-level annotation on each SDK aggregator class.
"""

from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Package root — resolved relative to the installed ``griddy`` package so
# the assertions are valid whether running against the source tree or an
# installed wheel.
# ---------------------------------------------------------------------------

_GRIDDY_ROOT = Path(__file__).resolve().parents[2] / "src" / "griddy"


@pytest.mark.unit
class TestPyTypedMarker:
    """The PEP 561 ``py.typed`` marker must live at the package root."""

    def test_py_typed_exists_at_package_root(self):
        assert (_GRIDDY_ROOT / "py.typed").exists()

    def test_py_typed_not_at_project_root(self):
        project_root = _GRIDDY_ROOT.parents[1]
        assert not (project_root / "py.typed").exists()


@pytest.mark.unit
class TestPyiStubs:
    """Inline ``.pyi`` stubs must exist for modules with dynamic attributes."""

    def test_lazy_load_stub_exists(self):
        stub = _GRIDDY_ROOT / "core" / "_lazy_load.pyi"
        assert stub.exists(), f"Expected stub at {stub}"

    def test_lazy_load_stub_omits_getattr(self):
        """The stub should NOT define ``__getattr__`` so type checkers use
        class-level annotations instead."""
        stub = _GRIDDY_ROOT / "core" / "_lazy_load.pyi"
        content = stub.read_text()
        assert "def __getattr__" not in content

    def test_lazy_load_stub_declares_dir(self):
        stub = _GRIDDY_ROOT / "core" / "_lazy_load.pyi"
        content = stub.read_text()
        assert "__dir__" in content


@pytest.mark.unit
class TestAnnotationsAccuracy:
    """Every key in ``_sub_sdk_map`` must have a matching class annotation."""

    @staticmethod
    def _assert_annotations_cover_map(cls):
        annotations = cls.__annotations__
        for attr_name in cls._sub_sdk_map:
            assert attr_name in annotations, (
                f"{cls.__name__}.__annotations__ is missing '{attr_name}' "
                f"(present in _sub_sdk_map)"
            )

    def test_griddy_nfl(self):
        from griddy.nfl.sdk import GriddyNFL

        self._assert_annotations_cover_map(GriddyNFL)

    def test_griddy_pfr(self):
        from griddy.pfr.sdk import GriddyPFR

        self._assert_annotations_cover_map(GriddyPFR)

    def test_griddy_draftbuzz(self):
        from griddy.draftbuzz.sdk import GriddyDraftBuzz

        self._assert_annotations_cover_map(GriddyDraftBuzz)

    def test_stats_sdk(self):
        from griddy.nfl.endpoints.pro.stats import StatsSDK

        self._assert_annotations_cover_map(StatsSDK)

    def test_football_stats_sdk(self):
        from griddy.nfl.endpoints.regular.football.stats import FootballStatsSDK

        self._assert_annotations_cover_map(FootballStatsSDK)

    def test_next_gen_stats(self):
        from griddy.nfl.endpoints.ngs import NextGenStats

        self._assert_annotations_cover_map(NextGenStats)


@pytest.mark.unit
class TestModuleLevelTypeChecking:
    """Module-level ``__init__.py`` files with ``_dynamic_imports`` must have
    matching ``TYPE_CHECKING`` imports for every dynamically importable name."""

    @staticmethod
    def _get_type_checking_names(module):
        """Return names visible under TYPE_CHECKING (the __all__ list)."""
        return set(getattr(module, "__all__", []))

    @staticmethod
    def _get_dynamic_imports(module):
        """Return keys from the _dynamic_imports dict."""
        return set(getattr(module, "_dynamic_imports", {}).keys())

    def test_nfl_models_dynamic_imports_in_all(self):
        import griddy.nfl.models as m

        assert self._get_dynamic_imports(m) <= self._get_type_checking_names(m)

    def test_pfr_models_dynamic_imports_in_all(self):
        import griddy.pfr.models as m

        assert self._get_dynamic_imports(m) <= self._get_type_checking_names(m)

    def test_draftbuzz_models_dynamic_imports_in_all(self):
        import griddy.draftbuzz.models as m

        assert self._get_dynamic_imports(m) <= self._get_type_checking_names(m)

    def test_nfl_errors_dynamic_imports_in_all(self):
        import griddy.nfl.errors as m

        assert self._get_dynamic_imports(m) <= self._get_type_checking_names(m)

    def test_pfr_errors_dynamic_imports_in_all(self):
        import griddy.pfr.errors as m

        assert self._get_dynamic_imports(m) <= self._get_type_checking_names(m)

    def test_draftbuzz_errors_dynamic_imports_in_all(self):
        import griddy.draftbuzz.errors as m

        assert self._get_dynamic_imports(m) <= self._get_type_checking_names(m)

    def test_core_errors_dynamic_imports_in_all(self):
        import griddy.core.errors as m

        assert self._get_dynamic_imports(m) <= self._get_type_checking_names(m)

    def test_core_utils_dynamic_imports_in_all(self):
        import griddy.core.utils as m

        assert self._get_dynamic_imports(m) <= self._get_type_checking_names(m)
