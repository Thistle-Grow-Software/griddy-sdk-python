"""Playwright-based scraping backend for the DraftBuzz SDK.

Provides :class:`PlaywrightBackend`, a synchronous scraping backend
that uses Playwright (Firefox) to fetch fully-rendered HTML pages.
Ported from fbcm's ``PageFetcher`` class.

Requires the ``playwright`` optional dependency::

    pip install griddy[browser-auth]
"""

import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)

_RECOVERABLE_ERROR_PHRASES = ("target closed", "browser has been closed")

# Defaults matching fbcm constants
_DEFAULT_SLOW_MO_MS = 150
_DEFAULT_MAX_RETRIES = 3
_DEFAULT_RETRY_DELAY = 1.0
_DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def _is_recoverable(error: Exception) -> bool:
    """Check if a Playwright error is a recoverable browser crash."""
    msg = str(error).lower()
    return any(phrase in msg for phrase in _RECOVERABLE_ERROR_PHRASES)


class PlaywrightBackend:
    """Synchronous scraping backend using Playwright Firefox.

    Satisfies the :class:`~griddy.draftbuzz.backends.ScrapingBackend`
    protocol. Manages a Playwright browser instance internally and
    handles automatic browser relaunch on recoverable crashes.

    Args:
        headless: Run the browser in headless mode (default ``True``).
        slow_mo: Milliseconds to slow down Playwright operations.
        max_retries: Maximum retry attempts on browser crash.
        retry_delay: Seconds to wait between retries.
    """

    def __init__(
        self,
        headless: bool = True,
        slow_mo: int = _DEFAULT_SLOW_MO_MS,
        max_retries: int = _DEFAULT_MAX_RETRIES,
        retry_delay: float = _DEFAULT_RETRY_DELAY,
    ) -> None:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise ImportError(
                "Playwright is required for the DraftBuzz SDK. "
                "Install it with: pip install griddy[browser-auth]"
            ) from exc

        self._headless = headless
        self._slow_mo = slow_mo
        self._max_retries = max_retries
        self._retry_delay = retry_delay

        self._pw_context = sync_playwright()
        self._pw = self._pw_context.start()
        self._browser = self._launch_browser()

    def _launch_browser(self):  # type: ignore[no-untyped-def]
        """Launch a new Firefox browser instance."""
        return self._pw.firefox.launch(headless=self._headless, slow_mo=self._slow_mo)

    def _ensure_connected(self) -> None:
        """Relaunch browser if disconnected."""
        if not self._browser.is_connected():
            logger.warning("Browser disconnected, relaunching...")
            self._browser = self._launch_browser()

    def get_page_content(self, url: str, wait_for_element: str) -> str:
        """Fetch a page's fully-rendered HTML content.

        Args:
            url: The full URL to fetch.
            wait_for_element: CSS selector to wait for before extracting
                HTML. Used as a readiness signal but failures are
                tolerated (the page content is returned regardless).

        Returns:
            The page's outer HTML as a string.

        Raises:
            PlaywrightError: If all retry attempts are exhausted.
        """
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import TimeoutError as PlaywrightTimeout

        self._ensure_connected()
        last_error: Optional[Exception] = None

        for attempt in range(self._max_retries):
            page = self._browser.new_page()
            try:
                logger.info("Navigating to: %s", url)
                try:
                    page.goto(url)
                except PlaywrightTimeout:
                    logger.warning(
                        "Page load timeout for %s, continuing with partial content...",
                        url,
                    )

                if wait_for_element:
                    try:
                        page.wait_for_selector(wait_for_element, timeout=10000)
                    except PlaywrightTimeout:
                        logger.debug(
                            "Selector %s not found within timeout, continuing...",
                            wait_for_element,
                        )

                return page.content()

            except PlaywrightError as exc:
                if not _is_recoverable(exc):
                    raise
                last_error = exc
                logger.warning(
                    "Browser/target closed (attempt %d/%d), relaunching...",
                    attempt + 1,
                    self._max_retries,
                )
                try:
                    self._browser.close()
                except PlaywrightError, OSError:
                    pass
                self._browser = self._launch_browser()
                time.sleep(self._retry_delay)
            finally:
                try:
                    page.close()
                except Exception:
                    pass

        raise last_error  # type: ignore[misc]

    def close(self) -> None:
        """Shut down the browser and Playwright."""
        try:
            self._browser.close()
        except Exception:
            pass
        try:
            self._pw_context.__exit__(None, None, None)
        except Exception:
            pass


class AsyncPlaywrightBackend:
    """Asynchronous scraping backend using Playwright Firefox.

    Satisfies the :class:`~griddy.draftbuzz.backends.AsyncScrapingBackend`
    protocol.

    Args:
        headless: Run the browser in headless mode (default ``True``).
        slow_mo: Milliseconds to slow down Playwright operations.
        max_retries: Maximum retry attempts on browser crash.
        retry_delay: Seconds to wait between retries.
    """

    def __init__(
        self,
        headless: bool = True,
        slow_mo: int = _DEFAULT_SLOW_MO_MS,
        max_retries: int = _DEFAULT_MAX_RETRIES,
        retry_delay: float = _DEFAULT_RETRY_DELAY,
    ) -> None:
        self._headless = headless
        self._slow_mo = slow_mo
        self._max_retries = max_retries
        self._retry_delay = retry_delay

        self._pw_context = None
        self._pw = None
        self._browser = None

    async def _ensure_started(self) -> None:
        """Lazily start Playwright and launch the browser."""
        if self._browser is not None and self._browser.is_connected():
            return

        if self._pw is None:
            try:
                from playwright.async_api import async_playwright
            except ImportError as exc:
                raise ImportError(
                    "Playwright is required for the DraftBuzz SDK. "
                    "Install it with: pip install griddy[browser-auth]"
                ) from exc

            self._pw_context = async_playwright()
            self._pw = await self._pw_context.start()

        self._browser = await self._pw.firefox.launch(
            headless=self._headless, slow_mo=self._slow_mo
        )

    async def get_page_content(self, url: str, wait_for_element: str) -> str:
        """Fetch a page's fully-rendered HTML content asynchronously.

        Args:
            url: The full URL to fetch.
            wait_for_element: CSS selector to wait for before extracting HTML.

        Returns:
            The page's outer HTML as a string.
        """
        import asyncio

        from playwright.async_api import Error as PlaywrightError
        from playwright.async_api import TimeoutError as PlaywrightTimeout

        await self._ensure_started()
        last_error: Optional[Exception] = None

        for attempt in range(self._max_retries):
            page = await self._browser.new_page()
            try:
                logger.info("Navigating to: %s", url)
                try:
                    await page.goto(url)
                except PlaywrightTimeout:
                    logger.warning(
                        "Page load timeout for %s, continuing with partial content...",
                        url,
                    )

                if wait_for_element:
                    try:
                        await page.wait_for_selector(wait_for_element, timeout=10000)
                    except PlaywrightTimeout:
                        logger.debug(
                            "Selector %s not found within timeout, continuing...",
                            wait_for_element,
                        )

                return await page.content()

            except PlaywrightError as exc:
                if not _is_recoverable(exc):
                    raise
                last_error = exc
                logger.warning(
                    "Browser/target closed (attempt %d/%d), relaunching...",
                    attempt + 1,
                    self._max_retries,
                )
                try:
                    await self._browser.close()
                except PlaywrightError, OSError:
                    pass
                self._browser = await self._pw.firefox.launch(
                    headless=self._headless, slow_mo=self._slow_mo
                )
                await asyncio.sleep(self._retry_delay)
            finally:
                try:
                    await page.close()
                except Exception:
                    pass

        raise last_error  # type: ignore[misc]

    async def close(self) -> None:
        """Shut down the browser and Playwright."""
        if self._browser:
            try:
                await self._browser.close()
            except Exception:
                pass
        if self._pw_context:
            try:
                await self._pw_context.__aexit__(None, None, None)
            except Exception:
                pass
