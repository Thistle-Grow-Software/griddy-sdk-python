"""Safe type conversion and text cleaning utilities."""

from typing import Any


def clean_text(text: str | None) -> str | None:
    """
    Clean and normalize text data.

    Args:
        text: Text to clean

    Returns:
        Cleaned text or None
    """
    if not text:
        return None

    # Strip whitespace and normalize
    cleaned = text.strip()
    if not cleaned:
        return None

    return cleaned


def safe_int(value: Any) -> int | None:
    """
    Safely convert value to integer.

    Args:
        value: Value to convert

    Returns:
        Integer value or None
    """
    if value is None:
        return None

    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def safe_float(value: Any) -> float | None:
    """
    Safely convert value to float.

    Args:
        value: Value to convert

    Returns:
        Float value or None
    """
    if value is None:
        return None

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def safe_numberify(value: str | None) -> int | float | str | None:
    """
    Attempt to convert a string value to int, then float, falling back to
    the original string if neither conversion succeeds.

    Args:
        value: String value to convert

    Returns:
        int, float, original string, or None
    """
    if value is None:
        return None

    for convert in (int, float):
        try:
            return convert(value)
        except (ValueError, TypeError):
            continue

    return value
