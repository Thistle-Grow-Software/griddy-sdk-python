"""Tests for griddy.pfr.utils.browserless module."""

from unittest.mock import MagicMock, Mock, patch

import pytest
import requests

from griddy.pfr.utils.browserless import Browserless, BrowserlessError


@pytest.fixture
def browserless():
    return Browserless()


@pytest.fixture
def browserless_custom_timeout():
    return Browserless(default_timeout_ms=30000)


@pytest.mark.unit
class TestBrowserlessInit:
    def test_default_timeout(self, browserless):
        assert browserless.timeout == 60000

    def test_custom_timeout(self, browserless_custom_timeout):
        assert browserless_custom_timeout.timeout == 30000

    def test_data_initially_none(self, browserless):
        assert browserless.data is None


@pytest.mark.unit
class TestFetchData:
    def test_returns_json_on_success(self, browserless):
        mock_resp = Mock()
        mock_resp.json.return_value = {
            "browserWSEndpoint": "ws://localhost:3000",
            "cookies": [{"name": "a", "value": "b"}],
        }

        with patch(
            "griddy.pfr.utils.browserless.requests.post", return_value=mock_resp
        ) as mock_post:
            result = browserless.fetch_data("https://example.com/page")

        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["json"]["url"] == "https://example.com/page"
        assert call_kwargs[1]["json"]["browserWSEndpoint"] is True
        assert call_kwargs[1]["params"]["proxy"] == "residential"
        assert result["browserWSEndpoint"] == "ws://localhost:3000"

    def test_calls_raise_for_status(self, browserless):
        mock_resp = Mock()
        mock_resp.json.return_value = {}

        with patch(
            "griddy.pfr.utils.browserless.requests.post", return_value=mock_resp
        ):
            browserless.fetch_data("https://example.com")

        mock_resp.raise_for_status.assert_called_once()

    def test_raises_browserless_error_on_request_exception(self, browserless):
        with patch(
            "griddy.pfr.utils.browserless.requests.post",
            side_effect=requests.RequestException("connection refused"),
        ):
            with pytest.raises(BrowserlessError, match="request failed"):
                browserless.fetch_data("https://example.com")

    def test_raises_browserless_error_on_http_error(self, browserless):
        mock_resp = Mock()
        mock_resp.raise_for_status.side_effect = requests.HTTPError("503 Server Error")

        with patch(
            "griddy.pfr.utils.browserless.requests.post", return_value=mock_resp
        ):
            with pytest.raises(BrowserlessError, match="request failed"):
                browserless.fetch_data("https://example.com")


@pytest.mark.unit
class TestHandlePageNavigation:
    def _make_page(self, url: str, content: str = "<html></html>"):
        page = MagicMock()
        page.url = url
        page.content.return_value = content
        return page

    def _make_browser(self, pages=None):
        browser = MagicMock()
        if pages is not None:
            ctx = MagicMock()
            ctx.pages = pages
            browser.contexts = [ctx]
        else:
            browser.contexts = []
        return browser

    def test_finds_existing_page_by_url(self, browserless):
        page = self._make_page("https://example.com/games", "<table>data</table>")
        browser = self._make_browser(pages=[page])

        result = browserless._handle_page_navigation(
            browser, "https://example.com/games", cookies={}, element="#games"
        )

        assert result == "<table>data</table>"
        page.locator.assert_called_once_with("#games")
        page.locator("#games").wait_for.assert_called_once_with(
            timeout=browserless.timeout
        )
        # Should not create a new context since the page was found.
        browser.new_context.assert_not_called()

    def test_creates_new_page_when_not_found(self, browserless):
        browser = self._make_browser(pages=[])
        new_page = self._make_page("https://example.com/games", "<html>new</html>")
        new_context = MagicMock()
        new_context.new_page.return_value = new_page
        browser.new_context.return_value = new_context

        result = browserless._handle_page_navigation(
            browser, "https://example.com/games", cookies={}, element="#tbl"
        )

        assert result == "<html>new</html>"
        browser.new_context.assert_called_once()
        new_context.new_page.assert_called_once()
        new_page.goto.assert_called_once_with(
            "https://example.com/games",
            wait_until="domcontentloaded",
            timeout=browserless.timeout,
        )

    def test_creates_new_page_when_no_contexts(self, browserless):
        browser = self._make_browser()  # empty contexts
        new_page = self._make_page("https://example.com", "<html/>")
        new_context = MagicMock()
        new_context.new_page.return_value = new_page
        browser.new_context.return_value = new_context

        browserless._handle_page_navigation(
            browser, "https://example.com", cookies={}, element="#el"
        )

        browser.new_context.assert_called_once()

    def test_adds_cookies_when_present(self, browserless):
        browser = self._make_browser(pages=[])
        new_page = self._make_page("https://example.com", "<html/>")
        new_context = MagicMock()
        new_context.new_page.return_value = new_page
        browser.new_context.return_value = new_context
        cookies = [{"name": "sid", "value": "abc123"}]

        browserless._handle_page_navigation(
            browser, "https://example.com", cookies=cookies, element="#el"
        )

        new_context.add_cookies.assert_called_once_with(cookies)

    def test_skips_cookies_when_empty(self, browserless):
        browser = self._make_browser(pages=[])
        new_page = self._make_page("https://example.com", "<html/>")
        new_context = MagicMock()
        new_context.new_page.return_value = new_page
        browser.new_context.return_value = new_context

        browserless._handle_page_navigation(
            browser, "https://example.com", cookies={}, element="#el"
        )

        new_context.add_cookies.assert_not_called()

    def test_uses_custom_timeout(self, browserless_custom_timeout):
        page = self._make_page("https://example.com/page", "<html/>")
        browser = self._make_browser(pages=[page])

        browserless_custom_timeout._handle_page_navigation(
            browser, "https://example.com/page", cookies={}, element="#tbl"
        )

        page.locator("#tbl").wait_for.assert_called_once_with(timeout=30000)

    def test_finds_page_across_multiple_contexts(self, browserless):
        wrong_page = self._make_page("https://other.com/page")
        right_page = self._make_page("https://example.com/games", "<table/>")

        ctx1 = MagicMock()
        ctx1.pages = [wrong_page]
        ctx2 = MagicMock()
        ctx2.pages = [right_page]

        browser = MagicMock()
        browser.contexts = [ctx1, ctx2]

        result = browserless._handle_page_navigation(
            browser, "https://example.com/games", cookies={}, element="#games"
        )

        assert result == "<table/>"
        browser.new_context.assert_not_called()


@pytest.mark.unit
class TestGetPageContent:
    def test_orchestrates_fetch_navigate_and_close(self, browserless):
        mock_browser = MagicMock()
        mock_pw = MagicMock()
        mock_pw.chromium.connect_over_cdp.return_value = mock_browser

        with (
            patch.object(
                browserless,
                "fetch_data",
                return_value={
                    "browserWSEndpoint": "ws://host:3000/devtools",
                    "cookies": [{"name": "c", "value": "v"}],
                },
            ),
            patch("griddy.pfr.utils.browserless.sync_playwright") as mock_sp,
            patch.object(
                browserless,
                "_handle_page_navigation",
                return_value="<html>content</html>",
            ) as mock_nav,
        ):
            mock_sp.return_value.__enter__ = Mock(return_value=mock_pw)
            mock_sp.return_value.__exit__ = Mock(return_value=False)

            result = browserless.get_page_content(
                "https://pfr.com/page", wait_for_element="#tbl"
            )

        assert result == "<html>content</html>"
        mock_pw.chromium.connect_over_cdp.assert_called_once_with(
            "ws://host:3000/devtools"
        )
        mock_nav.assert_called_once_with(
            browser=mock_browser,
            url="https://pfr.com/page",
            cookies=[{"name": "c", "value": "v"}],
            element="#tbl",
        )
        mock_browser.close.assert_called_once()

    def test_defaults_cookies_to_empty_list(self, browserless):
        mock_browser = MagicMock()
        mock_pw = MagicMock()
        mock_pw.chromium.connect_over_cdp.return_value = mock_browser

        with (
            patch.object(
                browserless,
                "fetch_data",
                return_value={"browserWSEndpoint": "ws://host"},
            ),
            patch("griddy.pfr.utils.browserless.sync_playwright") as mock_sp,
            patch.object(
                browserless,
                "_handle_page_navigation",
                return_value="<html/>",
            ) as mock_nav,
        ):
            mock_sp.return_value.__enter__ = Mock(return_value=mock_pw)
            mock_sp.return_value.__exit__ = Mock(return_value=False)

            browserless.get_page_content("https://pfr.com", wait_for_element="#el")

        assert mock_nav.call_args[1]["cookies"] == []

    def test_raises_browserless_error_on_cdp_failure(self, browserless):
        mock_pw = MagicMock()
        mock_pw.chromium.connect_over_cdp.side_effect = RuntimeError("CDP refused")

        with (
            patch.object(
                browserless,
                "fetch_data",
                return_value={"browserWSEndpoint": "ws://host"},
            ),
            patch("griddy.pfr.utils.browserless.sync_playwright") as mock_sp,
        ):
            mock_sp.return_value.__enter__ = Mock(return_value=mock_pw)
            mock_sp.return_value.__exit__ = Mock(return_value=False)

            with pytest.raises(BrowserlessError, match="Failed to connect Playwright"):
                browserless.get_page_content("https://pfr.com", wait_for_element="#el")
