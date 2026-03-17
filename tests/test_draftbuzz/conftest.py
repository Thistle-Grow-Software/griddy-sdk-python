"""Shared fixtures for DraftBuzz tests."""

from unittest.mock import patch

import pytest


class MockScrapingBackend:
    """A mock scraping backend that satisfies the ScrapingBackend protocol."""

    def get_page_content(self, url: str, wait_for_element: str) -> str:
        return "<html><body></body></html>"


class MockAsyncScrapingBackend:
    """A mock async scraping backend that satisfies the AsyncScrapingBackend protocol."""

    async def get_page_content(self, url: str, wait_for_element: str) -> str:
        return "<html><body></body></html>"


@pytest.fixture(autouse=True)
def _mock_playwright_backend():
    """Prevent real Playwright browsers from launching in unit tests.

    Patches the PlaywrightBackend and AsyncPlaywrightBackend classes
    at their source module so that the lazy imports in basesdk.py
    pick up the mocks.
    """
    with (
        patch(
            "griddy.draftbuzz.utils.playwright.PlaywrightBackend",
            return_value=MockScrapingBackend(),
        ),
        patch(
            "griddy.draftbuzz.utils.playwright.AsyncPlaywrightBackend",
            return_value=MockAsyncScrapingBackend(),
        ),
    ):
        yield
