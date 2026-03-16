"""Tests for griddy.draftbuzz.sdkconfiguration module."""

import httpx
import pytest

from griddy.core.utils.logger import get_default_logger
from griddy.draftbuzz.sdkconfiguration import SERVERS, SDKConfiguration


def _make_config(**kwargs):
    """Create an SDKConfiguration with required fields filled in."""
    defaults = {
        "client": httpx.Client(),
        "client_supplied": False,
        "async_client": httpx.AsyncClient(),
        "async_client_supplied": False,
        "debug_logger": get_default_logger(),
    }
    defaults.update(kwargs)
    return SDKConfiguration(**defaults)


@pytest.mark.unit
class TestSDKConfiguration:
    def test_default_server(self):
        config = _make_config()
        url, params = config.get_server_details()
        assert url == "https://www.nfldraftbuzz.com"
        assert params == {}

    def test_custom_server_url(self):
        config = _make_config(server_url="https://custom.example.com/")
        url, params = config.get_server_details()
        assert url == "https://custom.example.com"
        assert params == {}

    def test_custom_server_url_no_trailing_slash(self):
        config = _make_config(server_url="https://custom.example.com")
        url, params = config.get_server_details()
        assert url == "https://custom.example.com"

    def test_default_server_idx(self):
        config = _make_config()
        assert config.server_idx == 0

    def test_servers_dict(self):
        assert "default" in SERVERS
        assert SERVERS["default"] == "https://www.nfldraftbuzz.com"
