"""Tests for griddy.draftbuzz.errors module."""

import pytest

from griddy.core.exceptions import GriddyError
from griddy.draftbuzz.errors import GriddyDraftBuzzError, ParsingError


@pytest.mark.unit
class TestGriddyDraftBuzzError:
    def test_is_subclass_of_griddy_error(self):
        assert issubclass(GriddyDraftBuzzError, Exception)


@pytest.mark.unit
class TestParsingError:
    def test_basic_message(self):
        err = ParsingError("could not find element")
        assert str(err) == "could not find element"
        assert err.url is None
        assert err.selector is None

    def test_with_url(self):
        err = ParsingError("failed", url="https://example.com")
        assert "url=https://example.com" in str(err)

    def test_with_selector(self):
        err = ParsingError("failed", selector=".my-class")
        assert "selector=.my-class" in str(err)

    def test_with_all_context(self):
        err = ParsingError(
            "failed",
            url="https://example.com",
            selector=".my-class",
            html_sample="<div>...</div>",
        )
        result = str(err)
        assert "failed" in result
        assert "url=https://example.com" in result
        assert "selector=.my-class" in result
        assert err.html_sample == "<div>...</div>"

    def test_is_griddy_error(self):
        err = ParsingError("test")
        assert isinstance(err, GriddyError)
