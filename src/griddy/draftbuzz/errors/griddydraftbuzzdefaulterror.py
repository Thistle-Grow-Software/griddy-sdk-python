from dataclasses import dataclass
from typing import Optional

import httpx

from griddy.core.errors._formatting import format_error_message

from ..errors import GriddyDraftBuzzError


@dataclass(frozen=True)
class GriddyDraftBuzzDefaultError(GriddyDraftBuzzError):
    """The fallback error class if no more specific error class is matched."""

    def __init__(
        self, message: str, raw_response: httpx.Response, body: Optional[str] = None
    ):
        """Initialize with a formatted error message, raw HTTP response, and optional body text."""
        message = format_error_message(message, raw_response, body)
        super().__init__(message, raw_response, body)
