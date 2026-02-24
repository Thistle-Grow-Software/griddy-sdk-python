import sys
from datetime import datetime, timezone


def parse_datetime(datetime_string: str) -> datetime:
    """
    Convert a RFC 3339 / ISO 8601 formatted string into a datetime object.
    Python versions 3.11 and later support parsing RFC 3339 directly with
    datetime.fromisoformat(), but for earlier versions, this function
    encapsulates the necessary extra logic.
    """
    # Python 3.11 and later can parse RFC 3339 directly
    if sys.version_info >= (3, 11):
        return datetime.fromisoformat(datetime_string)

    # For Python 3.10 and earlier, a common ValueError is trailing 'Z' suffix,
    # so fix that upfront.
    if datetime_string.endswith("Z"):
        datetime_string = datetime_string[:-1] + "+00:00"

    return datetime.fromisoformat(datetime_string)


def parse_date(date_str: str | None) -> datetime | None:
    """
    Parse date string into datetime object.

    Args:
        date_str: Date string in various formats

    Returns:
        Parsed datetime object or None
    """
    if not date_str:
        return None

    # Common date formats to try
    formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m/%d/%Y %H:%M:%S",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            # Add timezone info if not present
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue

    # If no format matches, return None
    return None
