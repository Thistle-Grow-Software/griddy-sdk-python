"""Shared helper functions for DraftBuzz HTML parsers."""

import re
from typing import Optional

from bs4 import Tag


def get_tag_with_title_containing(tag: Tag, search_str: str) -> Optional[Tag]:
    """Find a <span> whose ``title`` attribute contains *search_str*."""
    return tag.find("span", title=lambda t: t and search_str in t)


def get_tag_with_text(search_space: Tag, tag_name: str, text: str) -> Optional[Tag]:
    """Find a tag whose text content contains *text* (case-insensitive)."""
    return search_space.find(tag_name, string=lambda s: s and text in s.lower())


def get_text_following_label(
    label_tag: Optional[Tag], expected_sibling_name: str = "span"
) -> Optional[str]:
    """Return the stripped text of the next sibling of *label_tag*."""
    if label_tag is None:
        return None
    sibling = label_tag.find_next_sibling(expected_sibling_name)
    if sibling is None:
        return None
    return sibling.get_text(strip=True)


def safe_int(value: str) -> Optional[int]:
    """Convert a string to int, returning None for empty/non-numeric values."""
    if not value:
        return None
    try:
        return int(value)
    except ValueError, TypeError:
        return None


def safe_float(value: str) -> Optional[float]:
    """Convert a string to float, returning None for empty/non-numeric values."""
    if not value:
        return None
    try:
        return float(value)
    except ValueError, TypeError:
        return None


def extract_jersey_number(tag: Tag) -> str:
    """Extract a jersey number like '#12' from a tag's text content."""
    match = tag.find(string=re.compile(r"#\d+"))
    if match:
        return match.get_text(strip=True)
    return ""
