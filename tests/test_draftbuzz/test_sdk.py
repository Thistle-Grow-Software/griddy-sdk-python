"""Tests for griddy.draftbuzz.sdk module."""

import warnings

import httpx
import pytest

from griddy.core.base_griddy_sdk import BaseGriddySDK
from griddy.draftbuzz import GriddyDraftBuzz


@pytest.mark.unit
class TestGriddyDraftBuzzInit:
    def test_basic_instantiation(self):
        db = GriddyDraftBuzz()
        assert isinstance(db, GriddyDraftBuzz)
        assert db.sdk_configuration is not None

    def test_creates_default_clients(self):
        db = GriddyDraftBuzz()
        assert db.sdk_configuration.client is not None
        assert db.sdk_configuration.async_client is not None
        assert db.sdk_configuration.client_supplied is False
        assert db.sdk_configuration.async_client_supplied is False

    def test_accepts_custom_client(self):
        client = httpx.Client()
        db = GriddyDraftBuzz(client=client)
        assert db.sdk_configuration.client is client
        assert db.sdk_configuration.client_supplied is True

    def test_accepts_custom_async_client(self):
        async_client = httpx.AsyncClient()
        db = GriddyDraftBuzz(async_client=async_client)
        assert db.sdk_configuration.async_client is async_client
        assert db.sdk_configuration.async_client_supplied is True

    def test_no_security_by_default(self):
        db = GriddyDraftBuzz()
        assert db.sdk_configuration.security is None

    def test_with_draftbuzz_auth(self):
        db = GriddyDraftBuzz(draftbuzz_auth={"accessToken": "test_token"})
        assert db.sdk_configuration.security is not None

    def test_custom_timeout(self):
        db = GriddyDraftBuzz(timeout_ms=5000)
        assert db.sdk_configuration.timeout_ms == 5000

    def test_custom_server_url(self):
        db = GriddyDraftBuzz(server_url="https://custom.draftbuzz.com")
        assert db.sdk_configuration.server_url == "https://custom.draftbuzz.com"

    def test_server_url_with_url_params(self):
        db = GriddyDraftBuzz(
            server_url="https://{region}.draftbuzz.com",
            url_params={"region": "us-east"},
        )
        assert db.sdk_configuration.server_url == "https://us-east.draftbuzz.com"

    def test_draftbuzz_auth_without_access_token_key(self):
        db = GriddyDraftBuzz(draftbuzz_auth={"refreshToken": "abc"})
        assert db.sdk_configuration.security is None

    def test_sub_sdk_map_contains_prospects(self):
        db = GriddyDraftBuzz()
        assert "prospects" in db._sub_sdk_map
        assert db._sub_sdk_map["prospects"] == (
            "griddy.draftbuzz.endpoints.prospects",
            "Prospects",
        )

    def test_sub_sdk_map_contains_rankings(self):
        db = GriddyDraftBuzz()
        assert "rankings" in db._sub_sdk_map
        assert db._sub_sdk_map["rankings"] == (
            "griddy.draftbuzz.endpoints.rankings",
            "Rankings",
        )


@pytest.mark.unit
class TestGriddyDraftBuzzContextManager:
    def test_sync_context_manager(self):
        with GriddyDraftBuzz() as db:
            assert isinstance(db, GriddyDraftBuzz)
            assert db.sdk_configuration.client is not None
        assert db.sdk_configuration.client is None

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        async with GriddyDraftBuzz() as db:
            assert isinstance(db, GriddyDraftBuzz)
            assert db.sdk_configuration.async_client is not None
        assert db.sdk_configuration.async_client is None

    def test_sync_context_manager_does_not_close_supplied_client(self):
        client = httpx.Client()
        with GriddyDraftBuzz(client=client) as db:
            pass
        assert db.sdk_configuration.client is None

    def test_exit_does_not_close_supplied_client(self):
        client = httpx.Client()
        db = GriddyDraftBuzz(client=client)
        db.__exit__(None, None, None)
        assert db.sdk_configuration.client is None

    @pytest.mark.asyncio
    async def test_async_exit_does_not_close_supplied_client(self):
        async_client = httpx.AsyncClient()
        db = GriddyDraftBuzz(async_client=async_client)
        await db.__aexit__(None, None, None)
        assert db.sdk_configuration.async_client is None


@pytest.mark.unit
class TestGriddyDraftBuzzLazyLoading:
    def test_unknown_attribute_raises(self):
        db = GriddyDraftBuzz()
        with pytest.raises(AttributeError, match="has no attribute 'nonexistent'"):
            _ = db.nonexistent

    def test_dir_contains_expected_methods(self):
        db = GriddyDraftBuzz()
        d = dir(db)
        assert "sdk_configuration" in d


@pytest.mark.unit
class TestGriddyDraftBuzzBaseGriddySDK:
    def test_isinstance_base_griddy_sdk(self):
        db = GriddyDraftBuzz()
        assert isinstance(db, BaseGriddySDK)

    def test_close_method(self):
        db = GriddyDraftBuzz()
        db.close()
        assert db.sdk_configuration.client is None
        assert db.sdk_configuration.async_client is None

    @pytest.mark.asyncio
    async def test_aclose_method(self):
        db = GriddyDraftBuzz()
        await db.aclose()
        assert db.sdk_configuration.client is None
        assert db.sdk_configuration.async_client is None

    def test_resource_warning_when_unclosed(self):
        db = GriddyDraftBuzz()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            db.__del__()
            assert len(w) == 1
            assert issubclass(w[0].category, ResourceWarning)

    def test_no_resource_warning_after_close(self):
        db = GriddyDraftBuzz()
        db.close()
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            db.__del__()
            assert len(w) == 0

    def test_no_resource_warning_for_supplied_clients(self):
        client = httpx.Client()
        async_client = httpx.AsyncClient()
        db = GriddyDraftBuzz(client=client, async_client=async_client)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            db.__del__()
            assert len(w) == 0
