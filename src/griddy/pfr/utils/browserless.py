"""Browserless fetch utility for bypassing bot detection on PFR pages.

Uses the Browserless /chromium/unblock API with a residential proxy to fetch
HTML content from Pro Football Reference pages that are protected by bot
detection.

Requires:
    - BROWSERLESS_API_KEY environment variable
    - playwright and requests packages
"""

import requests
from playwright.sync_api import sync_playwright

from griddy.settings import BROWSERLESS_HOST, BROWSERLESS_TOKEN


class BrowserlessError(Exception):
    """Raised when a Browserless API call or browser interaction fails."""


class Browserless:
    def __init__(self, default_timeout_ms: int = 60000):
        self.host = BROWSERLESS_HOST
        self.token = BROWSERLESS_TOKEN
        self.data: dict | None = None
        self.timeout = default_timeout_ms

    def fetch_data(self, url: str):
        unblock_url = f"https://{BROWSERLESS_HOST}/chromium/unblock"
        query_params = {
            "token": BROWSERLESS_TOKEN,
            "proxy": "residential",
            "timeout": 60_000,
        }
        payload = {
            "url": url,
            "browserWSEndpoint": True,
            "cookies": True,
            "content": False,
            "screenshot": False,
            "ttl": 30_000,
        }

        try:
            resp = requests.post(
                unblock_url,
                json=payload,
                params=query_params,
                headers={"Content-Type": "application/json"},
            )
            resp.raise_for_status()
        except requests.RequestException as exc:
            raise BrowserlessError(
                f"Browserless /chromium/unblock request failed: {exc}"
            ) from exc

        return resp.json()

    def _handle_page_navigation(self, browser, url: str, cookies: dict, element: str):
        # The unblock API already navigated to the URL in the first page.
        page = None
        for ctx in browser.contexts:
            for p in ctx.pages:
                if url in p.url:
                    page = p
                    break
            if page:
                break

        if page is None:
            context = browser.new_context()
            page = context.new_page()
            if cookies:
                context.add_cookies(cookies)
            page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)

        page.locator(element).wait_for(timeout=self.timeout)

        return page.content()

    def get_page_content(self, url: str, wait_for_element: str):
        """Fetch a page's HTML via Browserless unblock API + Playwright.

        Calls the Browserless /chromium/unblock endpoint with a residential proxy
        to bypass bot detection, then connects Playwright over CDP to extract the
        fully-rendered page HTML.

        Args:
            url: The full URL to fetch.
            wait_for_element: HTML Element id to wait for before extracting HTML.
            timeout_ms: Milliseconds to wait for the selector.

        Returns:
            The page's outer HTML as a string.

        Raises:
            BrowserlessError: If the API key is missing, the API call fails,
                or the page cannot be loaded.
        """
        browserless_data = self.fetch_data(url=url)

        ws_endpoint = browserless_data.get("browserWSEndpoint")
        cookies = browserless_data.get("cookies", [])

        with sync_playwright() as pw:
            try:
                browser = pw.chromium.connect_over_cdp(ws_endpoint)
            except Exception as exc:
                raise BrowserlessError(
                    f"Failed to connect Playwright via CDP: {exc}"
                ) from exc

            html = self._handle_page_navigation(
                browser=browser, url=url, cookies=cookies, element=wait_for_element
            )
            browser.close()

        return html
