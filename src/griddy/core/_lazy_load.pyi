"""Type stub for LazySubSDKMixin.

This stub intentionally omits ``__getattr__`` so that type checkers rely on
the class-level annotations declared by each SDK subclass (e.g.,
``authentication: "Authentication"`` on ``GriddyNFL``).  Without a fallback
``__getattr__``, accessing an undeclared attribute on an SDK instance is
correctly flagged as a type error.
"""

from typing import ClassVar

class LazySubSDKMixin:
    _sub_sdk_map: ClassVar[dict[str, tuple[str, str]]]
    def __dir__(self) -> list[str]: ...
