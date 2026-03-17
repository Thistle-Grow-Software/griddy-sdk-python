from typing import TYPE_CHECKING

from griddy.core._lazy import dynamic_dir, dynamic_getattr

from .griddydraftbuzzerror import GriddyDraftBuzzError
from .parsing_error import ParsingError

if TYPE_CHECKING:
    from .griddydraftbuzzdefaulterror import GriddyDraftBuzzDefaultError
    from .no_response_error import NoResponseError
    from .responsevalidationerror import ResponseValidationError

__all__ = [
    "GriddyDraftBuzzDefaultError",
    "GriddyDraftBuzzError",
    "NoResponseError",
    "ParsingError",
    "ResponseValidationError",
]

_dynamic_imports: dict[str, str] = {
    "GriddyDraftBuzzDefaultError": ".griddydraftbuzzdefaulterror",
    "NoResponseError": ".no_response_error",
    "ResponseValidationError": ".responsevalidationerror",
}


def __getattr__(attr_name: str) -> object:
    """Lazily import error classes on first access."""
    return dynamic_getattr(attr_name, _dynamic_imports, __package__, __name__)


def __dir__() -> list[str]:
    """List all public error class names available in this package."""
    return dynamic_dir(_dynamic_imports)
