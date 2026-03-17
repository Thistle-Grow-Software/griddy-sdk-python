"""Tests for griddy.draftbuzz.basesdk module."""

import httpx
import pytest

from griddy.core.utils.logger import get_default_logger
from griddy.draftbuzz.basesdk import BaseSDK, EndpointConfig
from griddy.draftbuzz.sdkconfiguration import SDKConfiguration


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
class TestEndpointConfig:
    def test_default_values(self):
        config = EndpointConfig(
            operation_id="test",
            response_type=dict,
        )
        assert config.path_template == ""
        assert config.wait_for_element == ""
        assert config.path_params == {}
        assert config.query_params == {}

    def test_custom_values(self):
        config = EndpointConfig(
            operation_id="getProspect",
            response_type=dict,
            path_template="/players/{slug}",
            wait_for_element=".player-info",
            path_params={"slug": "cam-ward"},
            query_params={"year": "2025"},
        )
        assert config.path_template == "/players/{slug}"
        assert config.path_params == {"slug": "cam-ward"}


@pytest.mark.unit
class TestBaseSDKBuildUrl:
    def setup_method(self):
        config = _make_config()
        self.sdk = BaseSDK(sdk_config=config)

    def test_simple_path(self):
        endpoint = EndpointConfig(
            operation_id="test",
            response_type=dict,
            path_template="/players/{slug}",
            path_params={"slug": "cam-ward-qb-2025"},
        )
        url = self.sdk._build_url(endpoint)
        assert url == "https://www.nfldraftbuzz.com/players/cam-ward-qb-2025"

    def test_path_with_query_params(self):
        endpoint = EndpointConfig(
            operation_id="test",
            response_type=dict,
            path_template="/positions/{position}/{page}/{year}",
            path_params={"position": "QB", "page": 1, "year": 2026},
            query_params={"sort": "rank"},
        )
        url = self.sdk._build_url(endpoint)
        assert url == "https://www.nfldraftbuzz.com/positions/QB/1/2026?sort=rank"

    def test_empty_path(self):
        endpoint = EndpointConfig(
            operation_id="test",
            response_type=dict,
        )
        url = self.sdk._build_url(endpoint)
        assert url == "https://www.nfldraftbuzz.com"
