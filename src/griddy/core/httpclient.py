"""HTTP client protocol definitions and implementations for sync and async requests."""

# pyright: reportReturnType = false
import asyncio
from typing import Any, Optional, Union

import httpx
from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class HttpClient(Protocol):
    """Protocol defining the sync HTTP client interface used by the SDK."""

    def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        """Send a request and return a response."""
        pass

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        """Build an HTTP request object from the given parameters."""
        pass

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        pass


@runtime_checkable
class AsyncHttpClient(Protocol):
    """Protocol defining the async HTTP client interface used by the SDK."""

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        """Send a request asynchronously and return a response."""
        pass

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        """Build an HTTP request object from the given parameters."""
        pass

    async def aclose(self) -> None:
        """Close the async HTTP client and release resources."""
        pass


class ClientOwner(Protocol):
    """Protocol for objects that own sync and async HTTP clients."""

    client: Union[HttpClient, None]
    async_client: Union[AsyncHttpClient, None]


def close_clients(
    owner: ClientOwner,
    sync_client: Union[HttpClient, None],
    sync_client_supplied: bool,
    async_client: Union[AsyncHttpClient, None],
    async_client_supplied: bool,
) -> None:
    """
    A finalizer function that is meant to be used with weakref.finalize to close
    httpx clients used by an SDK so that underlying resources can be garbage
    collected.
    """

    # Unset the client/async_client properties so there are no more references
    # to them from the owning SDK instance and they can be reaped.
    owner.client = None
    owner.async_client = None
    if sync_client is not None and not sync_client_supplied:
        try:
            sync_client.close()
        except Exception:
            pass

    if async_client is not None and not async_client_supplied:
        try:
            loop = asyncio.get_running_loop()
            asyncio.run_coroutine_threadsafe(async_client.aclose(), loop)
        except RuntimeError:
            try:
                asyncio.run(async_client.aclose())
            except RuntimeError:
                # best effort
                pass
