"""Base SDK configuration dataclass shared by all provider-specific SDK configurations."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, Union

from griddy.core.httpclient import AsyncHttpClient, HttpClient
from griddy.core.types import UNSET, OptionalNullable
from griddy.core.utils import Logger, RetryConfig, remove_suffix


@dataclass
class SDKConfiguration:
    """Base SDK configuration. Provider-specific SDKs should subclass this."""

    client: Union[HttpClient, None]
    client_supplied: bool
    async_client: Union[AsyncHttpClient, None]
    async_client_supplied: bool
    debug_logger: Logger
    security: Optional[Any] = None
    server_url: Optional[str] = ""
    server_idx: Optional[int] = 0
    language: str = "python"
    sdk_version: str = "0.0.0"
    user_agent: str = "griddy-sdk-python"
    retry_config: OptionalNullable[RetryConfig] = field(default_factory=lambda: UNSET)
    timeout_ms: Optional[int] = None
    _hooks: Optional[Any] = field(default=None, init=False, repr=False)

    @property
    def hooks(self) -> Any:
        """Return the SDK hooks instance."""
        return self._hooks

    def get_server_details(self) -> Tuple[str, Dict[str, str]]:
        """Return (server_url, url_variables). Subclasses should override."""
        if self.server_url is not None and self.server_url:
            return remove_suffix(self.server_url, "/"), {}
        return "", {}
