"""Tests for griddy.core.utils."""

import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

from griddy.core.utils.converters import clean_text, safe_float, safe_int
from griddy.core.utils.cookies import (
    Cookie,
    cookies_to_dict,
    cookies_to_header,
    extract_cookies_for_url,
    parse_cookies_txt,
)
from griddy.core.utils.datetimes import parse_date
from griddy.core.utils.url import build_url


@pytest.mark.unit
class TestParseDate:
    def test_iso_format(self):
        result = parse_date("2024-01-15T12:00:00")
        assert result is not None
        assert result.year == 2024
        assert result.month == 1
        assert result.tzinfo == timezone.utc

    def test_iso_format_with_z(self):
        result = parse_date("2024-01-15T12:00:00Z")
        assert result is not None
        assert result.year == 2024

    def test_iso_with_microseconds(self):
        result = parse_date("2024-01-15T12:00:00.123456")
        assert result is not None

    def test_iso_with_microseconds_z(self):
        result = parse_date("2024-01-15T12:00:00.123456Z")
        assert result is not None

    def test_date_time_space(self):
        result = parse_date("2024-01-15 12:00:00")
        assert result is not None

    def test_date_only(self):
        result = parse_date("2024-01-15")
        assert result is not None
        assert result.day == 15

    def test_us_date_format(self):
        result = parse_date("01/15/2024")
        assert result is not None
        assert result.month == 1

    def test_us_date_time_format(self):
        result = parse_date("01/15/2024 12:00:00")
        assert result is not None

    def test_invalid_string(self):
        result = parse_date("not-a-date")
        assert result is None

    def test_none(self):
        result = parse_date(None)
        assert result is None

    def test_empty(self):
        result = parse_date("")
        assert result is None


@pytest.mark.unit
class TestCleanText:
    def test_normal_text(self):
        assert clean_text("  hello  ") == "hello"

    def test_whitespace_only(self):
        assert clean_text("   ") is None

    def test_none(self):
        assert clean_text(None) is None

    def test_empty(self):
        assert clean_text("") is None

    def test_text_with_tabs(self):
        assert clean_text("\thello\n") == "hello"


@pytest.mark.unit
class TestSafeInt:
    def test_valid_int(self):
        assert safe_int(42) == 42

    def test_valid_string(self):
        assert safe_int("42") == 42

    def test_invalid_string(self):
        assert safe_int("not_a_number") is None

    def test_none(self):
        assert safe_int(None) is None

    def test_float(self):
        assert safe_int(3.14) == 3


@pytest.mark.unit
class TestSafeFloat:
    def test_valid_float(self):
        assert safe_float(3.14) == 3.14

    def test_valid_string(self):
        assert safe_float("3.14") == 3.14

    def test_invalid_string(self):
        assert safe_float("not_a_number") is None

    def test_none(self):
        assert safe_float(None) is None


@pytest.mark.unit
class TestBuildUrl:
    def test_basic(self):
        result = build_url("https://api.nfl.com", "games")
        assert result == "https://api.nfl.com/games"

    def test_with_params(self):
        result = build_url("https://api.nfl.com", "games", {"season": 2024})
        assert "season=2024" in result
        assert result.startswith("https://api.nfl.com/games?")

    def test_trailing_slash(self):
        result = build_url("https://api.nfl.com/", "/games")
        assert result == "https://api.nfl.com/games"

    def test_params_with_none_filtered(self):
        result = build_url(
            "https://api.nfl.com", "games", {"season": 2024, "week": None}
        )
        assert "season=2024" in result
        assert "week" not in result

    def test_empty_path(self):
        result = build_url("https://api.nfl.com", "")
        assert result == "https://api.nfl.com"

    def test_no_params(self):
        result = build_url("https://api.nfl.com", "games")
        assert "?" not in result


@pytest.mark.unit
class TestCookie:
    def test_construction(self):
        cookie = Cookie(
            domain=".nfl.com",
            path="/",
            secure=True,
            expires=None,
            name="session",
            value="abc123",
        )
        assert cookie.domain == ".nfl.com"
        assert cookie.name == "session"
        assert cookie.value == "abc123"

    def test_is_expired_no_expiry(self):
        cookie = Cookie(".nfl.com", "/", False, None, "name", "value")
        assert cookie.is_expired is False

    def test_is_expired_future(self):
        future = int(time.time()) + 3600
        cookie = Cookie(".nfl.com", "/", False, future, "name", "value")
        assert cookie.is_expired is False

    def test_is_expired_past(self):
        past = int(time.time()) - 3600
        cookie = Cookie(".nfl.com", "/", False, past, "name", "value")
        assert cookie.is_expired is True

    def test_matches_domain_exact(self):
        cookie = Cookie("nfl.com", "/", False, None, "name", "value")
        assert cookie.matches_domain("nfl.com") is True

    def test_matches_domain_subdomain(self):
        cookie = Cookie(
            ".nfl.com", "/", False, None, "name", "value", include_subdomains=False
        )
        assert cookie.matches_domain("api.nfl.com") is True

    def test_matches_domain_no_match(self):
        cookie = Cookie("nfl.com", "/", False, None, "name", "value")
        assert cookie.matches_domain("espn.com") is False

    def test_matches_path_root(self):
        cookie = Cookie(".nfl.com", "/", False, None, "name", "value")
        assert cookie.matches_path("/any/path") is True

    def test_matches_path_specific(self):
        cookie = Cookie(".nfl.com", "/api", False, None, "name", "value")
        assert cookie.matches_path("/api/games") is True
        assert cookie.matches_path("/other") is False

    def test_to_dict(self):
        cookie = Cookie(".nfl.com", "/", False, None, "session", "abc123")
        assert cookie.to_dict() == {"session": "abc123"}

    def test_to_header_string(self):
        cookie = Cookie(".nfl.com", "/", False, None, "session", "abc123")
        assert cookie.to_header_string() == "session=abc123"


@pytest.mark.unit
class TestParseCookiesTxt:
    def test_valid_file(self, tmp_path):
        cookies_file = tmp_path / "cookies.txt"
        cookies_file.write_text(
            "# Comment line\n"
            ".nfl.com\tTRUE\t/\tTRUE\t0\tsession\tabc123\n"
            ".nfl.com\tFALSE\t/api\tFALSE\t1893456000\ttoken\txyz789\n"
        )
        cookies = parse_cookies_txt(str(cookies_file))
        assert len(cookies) == 2
        assert cookies[0].name == "session"
        assert cookies[0].domain == ".nfl.com"
        assert cookies[0].include_subdomains is True
        assert cookies[1].name == "token"
        assert cookies[1].expires == 1893456000

    def test_missing_file(self):
        with pytest.raises(FileNotFoundError):
            parse_cookies_txt("/nonexistent/path/cookies.txt")

    def test_comments_and_blank_lines(self, tmp_path):
        cookies_file = tmp_path / "cookies.txt"
        cookies_file.write_text(
            "# Netscape HTTP Cookie File\n"
            "\n"
            "# Another comment\n"
            ".nfl.com\tTRUE\t/\tFALSE\t0\ttest\tvalue\n"
        )
        cookies = parse_cookies_txt(str(cookies_file))
        assert len(cookies) == 1

    def test_wrong_field_count_skipped(self, tmp_path):
        cookies_file = tmp_path / "cookies.txt"
        cookies_file.write_text(
            ".nfl.com\tTRUE\t/\n" ".nfl.com\tTRUE\t/\tFALSE\t0\ttest\tvalue\n"
        )
        cookies = parse_cookies_txt(str(cookies_file))
        assert len(cookies) == 1


@pytest.mark.unit
class TestExtractCookiesForUrl:
    def test_matching_domain(self, tmp_path):
        cookies_file = tmp_path / "cookies.txt"
        cookies_file.write_text(".nfl.com\tTRUE\t/\tFALSE\t0\tsession\tabc123\n")
        cookies = extract_cookies_for_url(str(cookies_file), "http://api.nfl.com/games")
        assert len(cookies) == 1

    def test_secure_cookie_on_http(self, tmp_path):
        cookies_file = tmp_path / "cookies.txt"
        cookies_file.write_text(".nfl.com\tTRUE\t/\tTRUE\t0\tsecure_cookie\tabc123\n")
        cookies = extract_cookies_for_url(str(cookies_file), "http://api.nfl.com/games")
        assert len(cookies) == 0

    def test_secure_cookie_on_https(self, tmp_path):
        cookies_file = tmp_path / "cookies.txt"
        cookies_file.write_text(".nfl.com\tTRUE\t/\tTRUE\t0\tsecure_cookie\tabc123\n")
        cookies = extract_cookies_for_url(
            str(cookies_file), "https://api.nfl.com/games"
        )
        assert len(cookies) == 1

    def test_expired_cookie_excluded(self, tmp_path):
        past = int(time.time()) - 3600
        cookies_file = tmp_path / "cookies.txt"
        cookies_file.write_text(f".nfl.com\tTRUE\t/\tFALSE\t{past}\texpired\tvalue\n")
        cookies = extract_cookies_for_url(str(cookies_file), "http://api.nfl.com/games")
        assert len(cookies) == 0


@pytest.mark.unit
class TestCookieConversions:
    def test_cookies_to_dict(self):
        cookies = [
            Cookie(".nfl.com", "/", False, None, "a", "1"),
            Cookie(".nfl.com", "/", False, None, "b", "2"),
        ]
        result = cookies_to_dict(cookies)
        assert result == {"a": "1", "b": "2"}

    def test_cookies_to_header(self):
        cookies = [
            Cookie(".nfl.com", "/", False, None, "a", "1"),
            Cookie(".nfl.com", "/", False, None, "b", "2"),
        ]
        result = cookies_to_header(cookies)
        assert result == "a=1; b=2"

    def test_cookies_to_header_empty(self):
        assert cookies_to_header([]) == ""
