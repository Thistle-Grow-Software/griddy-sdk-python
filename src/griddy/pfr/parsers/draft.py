"""Parser for PFR NFL Draft pages.

Handles three page types:
- ``/years/{year}/draft.htm`` — annual draft results (table ``#drafts``)
- ``/draft/{year}-combine.htm`` — NFL Combine measurements (table ``#combine``)
- ``/teams/{team}/draft.htm`` — team-specific draft history (table ``#draft``)
"""

import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int, safe_numeric, uncomment_tables

# Columns whose text should be cast to int
_INT_COLUMNS = {
    "draft_round",
    "draft_pick",
    "age",
    "year_max",
    "all_pros_first_team",
    "pro_bowls",
    "years_as_primary_starter",
    "career_av",
    "draft_av",
    "g",
    "pass_cmp",
    "pass_att",
    "pass_yds",
    "pass_td",
    "pass_int",
    "rush_att",
    "rush_yds",
    "rush_td",
    "rec",
    "rec_yds",
    "rec_td",
    "tackles_solo",
    "def_int",
    "weight",
    "bench_reps",
    "broad_jump",
}

_FLOAT_COLUMNS = {
    "sacks",
    "forty_yd",
    "vertical",
    "cone",
    "shuttle",
}


def _safe_float(value: str) -> Optional[float]:
    """Convert a string to float, returning None for empty/non-numeric."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


class DraftParser:
    """Parses PFR draft pages into structured data dicts."""

    # ------------------------------------------------------------------
    # Year Draft — /years/{year}/draft.htm
    # ------------------------------------------------------------------

    def parse_year_draft(self, html: str, *, year: int) -> Dict[str, Any]:
        """Parse a year draft page and return a dict for model validation.

        Returns:
            A dict with keys ``year``, ``picks``.
        """
        soup = BeautifulSoup(html, "html.parser")
        uncomment_tables(soup)

        table = soup.find("table", id="drafts")
        if table is None:
            return {"year": year, "picks": []}

        picks = self._parse_year_draft_rows(table)
        return {"year": year, "picks": picks}

    @staticmethod
    def _parse_year_draft_rows(table: Tag) -> List[Dict[str, Any]]:
        """Extract draft pick rows from the year draft table."""
        tbody = table.find("tbody")
        if tbody is None:
            return []

        picks: List[Dict[str, Any]] = []

        for tr in tbody.find_all("tr"):
            if "thead" in (tr.get("class") or []):
                continue

            row: Dict[str, Any] = {}
            all_empty = True

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat", "")
                if not stat:
                    continue

                text = cell.get_text(strip=True)
                if text:
                    all_empty = False

                if stat == "player":
                    row["player"] = text
                    player_id = cell.get("data-append-csv")
                    if player_id:
                        row["player_id"] = player_id
                    link = cell.find("a")
                    if link:
                        row["player_href"] = link.get("href")
                elif stat == "team":
                    row["team"] = text
                    link = cell.find("a")
                    if link:
                        row["team_href"] = link.get("href")
                elif stat == "college_id":
                    row["college"] = text
                    link = cell.find("a")
                    if link:
                        row["college_href"] = link.get("href")
                elif stat == "college_link":
                    link = cell.find("a")
                    if link:
                        row["college_stats_href"] = link.get("href")
                elif stat in _INT_COLUMNS:
                    row[stat] = safe_int(text)
                elif stat in _FLOAT_COLUMNS:
                    row[stat] = _safe_float(text)
                elif stat == "pos":
                    row["pos"] = text or None

            if not all_empty:
                picks.append(row)

        return picks

    # ------------------------------------------------------------------
    # Combine — /draft/{year}-combine.htm
    # ------------------------------------------------------------------

    def parse_combine(self, html: str, *, year: int) -> Dict[str, Any]:
        """Parse a combine page and return a dict for model validation.

        Returns:
            A dict with keys ``year``, ``entries``.
        """
        soup = BeautifulSoup(html, "html.parser")
        uncomment_tables(soup)

        table = soup.find("table", id="combine")
        if table is None:
            return {"year": year, "entries": []}

        entries = self._parse_combine_rows(table)
        return {"year": year, "entries": entries}

    @staticmethod
    def _parse_combine_rows(table: Tag) -> List[Dict[str, Any]]:
        """Extract combine entry rows from the combine table."""
        tbody = table.find("tbody")
        if tbody is None:
            return []

        entries: List[Dict[str, Any]] = []

        for tr in tbody.find_all("tr"):
            if "thead" in (tr.get("class") or []):
                continue

            row: Dict[str, Any] = {}
            all_empty = True

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat", "")
                if not stat:
                    continue

                text = cell.get_text(strip=True)
                if text:
                    all_empty = False

                if stat == "player":
                    row["player"] = text
                    player_id = cell.get("data-append-csv")
                    if player_id:
                        row["player_id"] = player_id
                    link = cell.find("a")
                    if link:
                        row["player_href"] = link.get("href")
                elif stat == "school_name":
                    row["school"] = text
                    link = cell.find("a")
                    if link:
                        row["school_href"] = link.get("href")
                elif stat == "college":
                    link = cell.find("a")
                    if link:
                        row["college_stats_href"] = link.get("href")
                elif stat == "height":
                    row["height"] = text or None
                elif stat == "draft_info":
                    row["draft_info"] = text or None
                    # Parse draft info: "Team Name / Nth / Nth pick / Year"
                    if text:
                        parts = [p.strip() for p in text.split("/")]
                        if len(parts) >= 3:
                            row["drafted_team"] = parts[0]
                            row["drafted_round"] = parts[1]
                            row["drafted_pick"] = parts[2]
                        # Year is in a link inside the cell
                        link = cell.find("a")
                        if link:
                            year_text = link.get_text(strip=True)
                            row["drafted_year"] = safe_int(year_text)
                elif stat == "pos":
                    row["pos"] = text or None
                elif stat in _INT_COLUMNS:
                    row[stat] = safe_int(text)
                elif stat in _FLOAT_COLUMNS:
                    row[stat] = _safe_float(text)

            if not all_empty:
                entries.append(row)

        return entries

    # ------------------------------------------------------------------
    # Team Draft — /teams/{team}/draft.htm
    # ------------------------------------------------------------------

    def parse_team_draft(self, html: str, *, team: str) -> Dict[str, Any]:
        """Parse a team draft page and return a dict for model validation.

        Returns:
            A dict with keys ``team``, ``picks``.
        """
        soup = BeautifulSoup(html, "html.parser")
        uncomment_tables(soup)

        table = soup.find("table", id="draft")
        if table is None:
            return {"team": team, "picks": []}

        picks = self._parse_team_draft_rows(table)
        return {"team": team, "picks": picks}

    @staticmethod
    def _parse_team_draft_rows(table: Tag) -> List[Dict[str, Any]]:
        """Extract draft pick rows from the team draft table."""
        tbody = table.find("tbody")
        if tbody is None:
            return []

        picks: List[Dict[str, Any]] = []

        for tr in tbody.find_all("tr"):
            if "thead" in (tr.get("class") or []):
                continue

            row: Dict[str, Any] = {}
            all_empty = True

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat", "")
                if not stat:
                    continue

                text = cell.get_text(strip=True)
                if text:
                    all_empty = False

                if stat == "year_id":
                    row["year"] = safe_int(text)
                    link = cell.find("a")
                    if link:
                        row["year_href"] = link.get("href")
                elif stat == "player":
                    row["player"] = text
                    player_id = cell.get("data-append-csv")
                    if player_id:
                        row["player_id"] = player_id
                    link = cell.find("a")
                    if link:
                        row["player_href"] = link.get("href")
                elif stat == "college_id":
                    row["college"] = text
                    link = cell.find("a")
                    if link:
                        row["college_href"] = link.get("href")
                elif stat in _INT_COLUMNS:
                    row[stat] = safe_int(text)
                elif stat in _FLOAT_COLUMNS:
                    row[stat] = _safe_float(text)
                elif stat == "pos":
                    row["pos"] = text or None

            if not all_empty:
                picks.append(row)

        return picks
