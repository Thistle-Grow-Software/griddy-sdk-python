from ._version import __user_agent__, __version__
from .backends import AsyncScrapingBackend, ScrapingBackend
from .sdk import GriddyDraftBuzz
from .sdkconfiguration import SERVERS, SDKConfiguration

__all__ = [
    "AsyncScrapingBackend",
    "GriddyDraftBuzz",
    "ScrapingBackend",
    "SDKConfiguration",
    "SERVERS",
    "VERSION",
    "USER_AGENT",
]

VERSION: str = __version__
USER_AGENT: str = __user_agent__
