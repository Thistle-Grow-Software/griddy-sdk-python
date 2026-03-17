"""Pluggable scraping backend protocols for the DraftBuzz SDK.

Defines :class:`ScrapingBackend` and :class:`AsyncScrapingBackend` protocols
that abstract the HTML fetching layer. Any object exposing a
``get_page_content(url, wait_for_element) -> str`` method satisfies the
protocol and can be used as a drop-in replacement for the default
:class:`~griddy.pfr.utils.browserless.Browserless` backend.

Example -- using a custom backend::

    class MyBackend:
        def get_page_content(
            self, url: str, wait_for_element: str
        ) -> str: ...  # fetch HTML however you like


    draftbuzz = GriddyDraftBuzz(scraping_backend=MyBackend())
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class ScrapingBackend(Protocol):
    """Protocol for synchronous HTML scraping backends."""

    def get_page_content(self, url: str, wait_for_element: str) -> str:
        """Fetch a page's HTML content.

        Args:
            url: The full URL to fetch.
            wait_for_element: CSS selector to wait for before extracting HTML.

        Returns:
            The page's outer HTML as a string.
        """
        ...


@runtime_checkable
class AsyncScrapingBackend(Protocol):
    """Protocol for asynchronous HTML scraping backends."""

    async def get_page_content(self, url: str, wait_for_element: str) -> str:
        """Fetch a page's HTML content asynchronously.

        Args:
            url: The full URL to fetch.
            wait_for_element: CSS selector to wait for before extracting HTML.

        Returns:
            The page's outer HTML as a string.
        """
        ...
