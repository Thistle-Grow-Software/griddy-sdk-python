from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

from griddy.core.sdkconfiguration import SDKConfiguration as CoreSDKConfiguration

from ._version import __user_agent__, __version__
from .utils import remove_suffix

SERVERS = {
    "default": "https://www.nfldraftbuzz.com",
}


@dataclass
class SDKConfiguration(CoreSDKConfiguration):
    """DraftBuzz-specific SDK configuration with server URL resolution."""

    sdk_version: str = __version__
    user_agent: str = __user_agent__
    server_type: str = "default"
    scraping_backend: Optional[Any] = field(default=None, repr=False)
    async_scraping_backend: Optional[Any] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Set default server index to 0 if not provided."""
        if self.server_idx is None:
            self.server_idx = 0

    def get_server_details(self) -> Tuple[str, Dict[str, str]]:
        """Return the base URL and params for the configured server type."""
        if self.server_url is not None and self.server_url:
            return remove_suffix(self.server_url, "/"), {}

        server_url = SERVERS.get(self.server_type, SERVERS["default"])
        return server_url, {}
