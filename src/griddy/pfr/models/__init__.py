import builtins
from typing import TYPE_CHECKING

from griddy.core._import import dynamic_import

if TYPE_CHECKING:
    from griddy.pfr.models.entities.schedule_game import (
        ScheduleGame,
        ScheduleGameTypedDict,
    )
    from griddy.pfr.models.entities.security import Security, SecurityTypedDict

__all__ = [
    "ScheduleGame",
    "ScheduleGameTypedDict",
    "Security",
    "SecurityTypedDict",
]

_dynamic_imports: dict[str, str] = {
    "ScheduleGame": ".entities.schedule_game",
    "ScheduleGameTypedDict": ".entities.schedule_game",
    "Security": ".entities.security",
    "SecurityTypedDict": ".entities.security",
}


def __getattr__(attr_name: str) -> object:
    module_name = _dynamic_imports.get(attr_name)
    if module_name is None:
        raise AttributeError(
            f"No {attr_name} found in _dynamic_imports for module name -> {__name__} "
        )

    try:
        module = dynamic_import(module_name, __package__)
        result = getattr(module, attr_name)
        return result
    except ImportError as e:
        raise ImportError(
            f"Failed to import {attr_name} from {module_name}: {e}"
        ) from e
    except AttributeError as e:
        raise AttributeError(
            f"Failed to get {attr_name} from {module_name}: {e}"
        ) from e


def __dir__():
    lazy_attrs = builtins.list(_dynamic_imports.keys())
    return builtins.sorted(lazy_attrs)
