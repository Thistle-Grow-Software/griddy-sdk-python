from dataclasses import dataclass
from typing import Optional

import httpx

from griddy.core.errors.sdkerror import SDKError


@dataclass(frozen=True)
class GriddyDraftBuzzError(SDKError):
    """The base class for all DraftBuzz SDK HTTP error responses."""

    def __init__(
        self, message: str, raw_response: httpx.Response, body: Optional[str] = None
    ):
        """Initialize with a message, raw HTTP response, and optional body text."""
        super().__init__(message, raw_response, body)
