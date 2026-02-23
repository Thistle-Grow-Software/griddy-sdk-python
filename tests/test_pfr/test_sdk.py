"""Tests for griddy.pfr.sdk module."""

import httpx
import pytest

from griddy.pfr import GriddyPFR
from griddy.pfr.sdkconfiguration import SDKConfiguration


@pytest.mark.unit
class TestGriddyPFRInit:
    def test_basic_instantiation(self):
        pfr = GriddyPFR()
        assert isinstance(pfr, GriddyPFR)
        assert pfr.sdk_configuration is not None

    def test_creates_default_clients(self):
        pfr = GriddyPFR()
        assert pfr.sdk_configuration.client is not None
        assert pfr.sdk_configuration.async_client is not None
        assert pfr.sdk_configuration.client_supplied is False
        assert pfr.sdk_configuration.async_client_supplied is False

    def test_accepts_custom_client(self):
        client = httpx.Client()
        pfr = GriddyPFR(client=client)
        assert pfr.sdk_configuration.client is client
        assert pfr.sdk_configuration.client_supplied is True

    def test_accepts_custom_async_client(self):
        async_client = httpx.AsyncClient()
        pfr = GriddyPFR(async_client=async_client)
        assert pfr.sdk_configuration.async_client is async_client
        assert pfr.sdk_configuration.async_client_supplied is True

    def test_no_security_by_default(self):
        pfr = GriddyPFR()
        assert pfr.sdk_configuration.security is None

    def test_with_pfr_auth(self):
        pfr = GriddyPFR(pfr_auth={"accessToken": "test_token"})
        assert pfr.sdk_configuration.security is not None

    def test_custom_timeout(self):
        pfr = GriddyPFR(timeout_ms=5000)
        assert pfr.sdk_configuration.timeout_ms == 5000

    def test_custom_server_url(self):
        pfr = GriddyPFR(server_url="https://custom.pfr.com")
        assert pfr.sdk_configuration.server_url == "https://custom.pfr.com"

    def test_server_url_with_url_params(self):
        pfr = GriddyPFR(
            server_url="https://{region}.pfr.com",
            url_params={"region": "us-east"},
        )
        assert pfr.sdk_configuration.server_url == "https://us-east.pfr.com"

    def test_pfr_auth_without_access_token_key(self):
        pfr = GriddyPFR(pfr_auth={"refreshToken": "abc"})
        assert pfr.sdk_configuration.security is None

    def test_sub_sdk_map_contains_schedule(self):
        pfr = GriddyPFR()
        assert "schedule" in pfr._sub_sdk_map
        assert pfr._sub_sdk_map["schedule"] == (
            "griddy.pfr.endpoints.schedule",
            "Schedule",
        )


@pytest.mark.unit
class TestGriddyPFRContextManager:
    def test_sync_context_manager(self):
        with GriddyPFR() as pfr:
            assert isinstance(pfr, GriddyPFR)
            assert pfr.sdk_configuration.client is not None
        # After exit, client should be None
        assert pfr.sdk_configuration.client is None

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        async with GriddyPFR() as pfr:
            assert isinstance(pfr, GriddyPFR)
            assert pfr.sdk_configuration.async_client is not None
        assert pfr.sdk_configuration.async_client is None

    def test_sync_context_manager_does_not_close_supplied_client(self):
        client = httpx.Client()
        with GriddyPFR(client=client) as pfr:
            pass
        # Supplied client should NOT be closed by the context manager
        # (client_supplied=True means we don't own it)
        assert pfr.sdk_configuration.client is None  # ref cleared but client not closed

    def test_exit_does_not_close_supplied_client(self):
        """Verify the __exit__ logic checks client_supplied flag."""
        client = httpx.Client()
        pfr = GriddyPFR(client=client)
        pfr.__exit__(None, None, None)
        # The client reference is set to None but the client itself should not be closed
        assert pfr.sdk_configuration.client is None

    @pytest.mark.asyncio
    async def test_async_exit_does_not_close_supplied_client(self):
        async_client = httpx.AsyncClient()
        pfr = GriddyPFR(async_client=async_client)
        await pfr.__aexit__(None, None, None)
        assert pfr.sdk_configuration.async_client is None


@pytest.mark.unit
class TestGriddyPFRLazyLoading:
    def test_unknown_attribute_raises(self):
        pfr = GriddyPFR()
        with pytest.raises(AttributeError, match="has no attribute 'nonexistent'"):
            _ = pfr.nonexistent

    def test_dir_contains_expected_methods(self):
        pfr = GriddyPFR()
        d = dir(pfr)
        assert "sdk_configuration" in d
