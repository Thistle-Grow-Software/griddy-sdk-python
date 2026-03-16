from typing import Optional

from griddy.core.exceptions import GriddyError


class ParsingError(GriddyError):
    """Raised when DraftBuzz HTML parsing fails to find expected elements.

    Provides context about what was being parsed and where, making it
    easier to diagnose issues with changed page structures.

    Attributes:
        url: The DraftBuzz URL that was fetched.
        selector: The CSS selector or element identifier that was not found.
        html_sample: A truncated sample of the HTML for debugging.
    """

    def __init__(
        self,
        message: str,
        *,
        url: Optional[str] = None,
        selector: Optional[str] = None,
        html_sample: Optional[str] = None,
    ) -> None:
        """Initialize with a message and optional context about the failed parse.

        Args:
            message: Description of the parsing failure.
            url: The DraftBuzz URL that was fetched.
            selector: The CSS selector or element identifier that was not found.
            html_sample: A truncated sample of the HTML for debugging.
        """
        super().__init__(message)
        self.url = url
        self.selector = selector
        self.html_sample = html_sample

    def __str__(self) -> str:
        """Return a pipe-delimited summary including URL and selector when present."""
        parts = [self.message]
        if self.url:
            parts.append(f"url={self.url}")
        if self.selector:
            parts.append(f"selector={self.selector}")
        return " | ".join(parts)
