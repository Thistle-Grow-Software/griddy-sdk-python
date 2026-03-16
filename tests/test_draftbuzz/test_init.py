"""Tests for griddy.draftbuzz package exports."""

import pytest


@pytest.mark.unit
class TestDraftBuzzPackageExports:
    def test_import_griddy_draftbuzz(self):
        from griddy.draftbuzz import GriddyDraftBuzz

        assert GriddyDraftBuzz is not None

    def test_import_sdk_configuration(self):
        from griddy.draftbuzz import SDKConfiguration

        assert SDKConfiguration is not None

    def test_import_servers(self):
        from griddy.draftbuzz import SERVERS

        assert "default" in SERVERS

    def test_import_backends(self):
        from griddy.draftbuzz import AsyncScrapingBackend, ScrapingBackend

        assert ScrapingBackend is not None
        assert AsyncScrapingBackend is not None

    def test_import_version(self):
        from griddy.draftbuzz import VERSION

        assert isinstance(VERSION, str)

    def test_griddy_root_exports_draftbuzz(self):
        import griddy

        assert "draftbuzz" in griddy.__all__

    def test_import_models(self):
        from griddy.draftbuzz.models import (
            BasicInfo,
            ProspectProfile,
            RatingsAndRankings,
        )

        assert BasicInfo is not None
        assert ProspectProfile is not None
        assert RatingsAndRankings is not None

    def test_import_errors(self):
        from griddy.draftbuzz.errors import (
            GriddyDraftBuzzError,
            ParsingError,
        )

        assert GriddyDraftBuzzError is not None
        assert ParsingError is not None
