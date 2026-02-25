"""Official profile page HTML parser for Pro Football Reference.

Parses PFR ``/officials/{OfficialId}.htm`` pages into structured dicts
containing official bio, season penalty stats, and individual game logs.
"""

import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int

# Columns in official_stats that should be cast to int.
_STATS_INT_COLUMNS = {
    "g",
    "g_playoffs",
    "home",
    "visitor",
    "pen_total",
    "pen_yds",
}

# Columns in official_stats that should be cast to float (values may have %).
_STATS_FLOAT_COLUMNS = {
    "home_pct",
    "home_wpct",
    "pen_per_g",
    "pen_yds_per_g",
    "lg_home_pct",
    "lg_home_wpct",
    "lg_pen_per_g",
    "lg_pen_yds_per_g",
    "rel_home_pct",
    "rel_home_wpct",
    "rel_pen_per_g",
    "rel_pen_yds_per_g",
}

# Columns in games that should be cast to int.
_GAMES_INT_COLUMNS = {
    "points_opp",
    "penalties_opp",
    "penalties_yds_opp",
    "points",
    "penalties",
    "penalties_yds",
}

# Columns in games where we extract hrefs.
_GAMES_LINK_COLUMNS = {
    "game_date": "game_date_href",
    "team": "team_href",
    "opp": "opp_href",
}


def _safe_float(value: str) -> Optional[float]:
    """Convert a string to float, stripping trailing ``%`` if present."""
    if not value:
        return None
    cleaned = value.rstrip("%")
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return None


class OfficialProfileParser:
    """Parses PFR official profile pages into comprehensive data dicts."""

    def parse(self, html: str) -> Dict[str, Any]:
        """Parse a PFR official profile page into a JSON-serializable dict.

        Args:
            html: Raw HTML string of a PFR official profile page.

        Returns:
            A dict with keys: bio, official_stats, games.
        """
        cleaned = re.sub(r"<!--(.*?)-->", r"\1", html, flags=re.DOTALL)
        soup = BeautifulSoup(cleaned, "html.parser")

        result: Dict[str, Any] = {}
        result["bio"] = self._parse_bio(soup)
        result["official_stats"] = self._parse_official_stats(soup)
        result["games"] = self._parse_games(soup)

        return result

    # ------------------------------------------------------------------
    # Bio / Metadata
    # ------------------------------------------------------------------

    @staticmethod
    def _clean(text: str) -> str:
        """Normalize whitespace and non-breaking spaces in extracted text."""
        cleaned = text.replace("\xa0", " ").strip()
        return re.sub(r"\s+", " ", cleaned)

    @classmethod
    def _parse_bio(cls, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract official bio from the ``#meta`` div."""
        meta_div = soup.find("div", id="meta")
        if meta_div is None:
            return {"name": ""}

        bio: Dict[str, Any] = {}

        # Display name from h1
        h1 = meta_div.find("h1")
        bio["name"] = cls._clean(h1.get_text()) if h1 else ""

        # Position from the <p> with <strong>Position</strong>
        for p_tag in meta_div.find_all("p"):
            strong = p_tag.find("strong")
            if not strong:
                continue
            label = strong.get_text(strip=True)
            if label == "Position":
                full_text = cls._clean(p_tag.get_text())
                # Strip "Position:" prefix
                pos = full_text.replace("Position", "", 1).strip().lstrip(":").strip()
                if pos:
                    bio["position"] = pos
                break

        return bio

    # ------------------------------------------------------------------
    # Official Stats table (season totals)
    # ------------------------------------------------------------------

    def _parse_official_stats(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse the ``official_stats`` table."""
        table = soup.find("table", id="official_stats")
        if table is None:
            return []

        return self._parse_table_body(
            table,
            int_columns=_STATS_INT_COLUMNS,
            float_columns=_STATS_FLOAT_COLUMNS,
        )

    # ------------------------------------------------------------------
    # Games table (individual game log)
    # ------------------------------------------------------------------

    def _parse_games(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse the ``games`` table."""
        table = soup.find("table", id="games")
        if table is None:
            return []

        return self._parse_table_body(
            table,
            int_columns=_GAMES_INT_COLUMNS,
            link_columns=_GAMES_LINK_COLUMNS,
        )

    # ------------------------------------------------------------------
    # Generic table body parser
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_table_body(
        table: Tag,
        *,
        int_columns: Optional[set] = None,
        float_columns: Optional[set] = None,
        link_columns: Optional[Dict[str, str]] = None,
    ) -> List[Dict[str, Any]]:
        """Parse a table's tbody rows with type casting and link extraction."""
        int_columns = int_columns or set()
        float_columns = float_columns or set()
        link_columns = link_columns or {}

        tbody = table.find("tbody")
        if tbody is None:
            return []

        records: List[Dict[str, Any]] = []

        for tr in tbody.find_all("tr"):
            classes = tr.get("class") or []
            if "thead" in classes or "over_header" in classes:
                continue

            row_data: Dict[str, Any] = {}

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat")
                if not stat:
                    continue

                text = cell.get_text(strip=True)

                if stat in int_columns:
                    row_data[stat] = safe_int(text)
                elif stat in float_columns:
                    row_data[stat] = _safe_float(text)
                else:
                    row_data[stat] = text

                # Extract links.
                if stat in link_columns:
                    link = cell.find("a")
                    href_field = link_columns[stat]
                    row_data[href_field] = (
                        link["href"] if link and link.get("href") else None
                    )

            if row_data:
                records.append(row_data)

        return records
