from dataclasses import dataclass
from typing import Optional

import httpx

from ..errors import GriddyDraftBuzzError


@dataclass(frozen=True)
class ResponseValidationError(GriddyDraftBuzzError):
    """Error raised when there is a type mismatch between the response data and the expected Pydantic model."""

    def __init__(
        self,
        message: str,
        raw_response: httpx.Response,
        cause: Exception,
        body: Optional[str] = None,
    ):
        """Initialize with a message, raw HTTP response, causal exception, and optional body text."""
        message = f"{message}: {cause}"
        super().__init__(message, raw_response, body)

    @property
    def cause(self) -> BaseException | None:
        """Normally the Pydantic ValidationError"""
        return self.__cause__
