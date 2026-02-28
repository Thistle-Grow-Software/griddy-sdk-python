"""Shared helper functions for PFR HTML parsers."""

from typing import Any, Optional

from bs4 import BeautifulSoup, Comment


def safe_int(value: str) -> Optional[int]:
    """Convert a string to int, returning None for empty/non-numeric values."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def safe_numeric(value: str) -> Any:
    """Try to convert a string to int or float; return the string
    unchanged if conversion fails.
    """
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def safe_pct(value: str) -> Optional[float]:
    """Convert a percentage string (e.g. ``'63.46%'``) to a float.

    Strips a trailing ``%`` sign before conversion.  Returns ``None``
    for empty or non-numeric values.
    """
    if not value:
        return None
    cleaned = value.rstrip("%").strip()
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return None


def uncomment_tables(soup: BeautifulSoup) -> None:
    """Replace HTML comment nodes that contain ``<table`` tags with
    their parsed content so that subsequent ``soup.find`` calls can
    locate them.
    """
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        if "<table" in comment:
            fragment = BeautifulSoup(comment, "html.parser")
            comment.replace_with(fragment)
