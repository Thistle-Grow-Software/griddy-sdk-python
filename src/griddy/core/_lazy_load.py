"""Mixin for lazy-loading sub-SDKs via a _sub_sdk_map dict.

Sub-SDK aggregator classes (FootballStatsSDK, StatsSDK, GriddyNFL) all need
the same pattern: a ``_sub_sdk_map`` dict mapping attribute names to
``(module_path, class_name)`` tuples, with ``__getattr__`` that dynamically
imports and caches sub-SDK instances on first access.

This mixin provides that behaviour so each class only needs to define its
``_sub_sdk_map``.
"""

from typing import Dict, List, Tuple

from ._import import dynamic_import


class LazySubSDKMixin:
    """Mixin that enables lazy-loading of sub-SDKs from ``_sub_sdk_map``.

    On first attribute access, the mixin dynamically imports the sub-SDK
    module, instantiates the class with the parent's ``sdk_configuration``
    and ``parent_ref``, and caches the instance via ``setattr`` so that
    subsequent accesses return the same object without re-importing.

    The ``__dir__`` override ensures sub-SDK names appear in
    ``dir()`` and IDE autocompletion even before they are instantiated.

    Requirements for using this mixin:

    1. Define a class-level ``_sub_sdk_map`` dict mapping attribute names
       to ``(module_path, class_name)`` tuples.
    2. Ensure the class has ``sdk_configuration`` and ``parent_ref``
       attributes (typically inherited from ``BaseSDK``).
    3. Each sub-SDK class referenced in ``_sub_sdk_map`` must accept
       ``(sdk_configuration, *, parent_ref)`` as its constructor signature.

    Example::

        class MySDK(LazySubSDKMixin, BaseSDK):
            _sub_sdk_map: Dict[str, Tuple[str, str]] = {
                "games": (
                    "griddy.nfl.endpoints.regular.football.games",
                    "Games",
                ),
            }


        sdk = MySDK(config)
        sdk.games  # first access: imports module, instantiates Games, caches it
        sdk.games  # subsequent access: returns cached instance
    """

    _sub_sdk_map: Dict[str, Tuple[str, str]] = {}

    def __getattr__(self, name: str) -> object:
        """Lazily import, instantiate, and cache a sub-SDK on first access.

        When *name* matches a key in ``_sub_sdk_map``, the corresponding
        module is imported, the class is instantiated with
        ``(self.sdk_configuration, parent_ref=self.parent_ref)``, and the
        resulting instance is stored on ``self`` so future lookups bypass
        ``__getattr__`` entirely.

        Args:
            name: The attribute name being accessed.

        Returns:
            The cached sub-SDK instance.

        Raises:
            AttributeError: If *name* is not in ``_sub_sdk_map`` or if the
                module/class cannot be found.
        """
        if name in self._sub_sdk_map:
            module_path, class_name = self._sub_sdk_map[name]
            try:
                module = dynamic_import(module_path)
                klass = getattr(module, class_name)
                instance = klass(self.sdk_configuration, parent_ref=self.parent_ref)
                setattr(self, name, instance)
                return instance
            except ImportError as e:
                raise AttributeError(
                    f"Failed to import module {module_path} for attribute {name}: {e}"
                ) from e
            except AttributeError as e:
                raise AttributeError(
                    f"Failed to find class {class_name} in module {module_path}: {e}"
                ) from e

        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'"
        )

    def __dir__(self) -> List[str]:
        """Return default attributes plus all lazy-loadable sub-SDK names.

        This ensures sub-SDK names appear in ``dir()`` output and IDE
        autocompletion even before they have been accessed and instantiated.
        """
        default_attrs = list(super().__dir__())
        lazy_attrs = list(self._sub_sdk_map.keys())
        return sorted(list(set(default_attrs + lazy_attrs)))
