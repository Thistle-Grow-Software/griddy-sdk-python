"""Parser for PFR career/single-season/single-game leader pages.

Handles ``/leaders/{stat}_{scope}.htm`` pages, extracting the leaders
table into a list of entry dicts suitable for Pydantic validation.
"""

import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup

from ._helpers import safe_int


class LeadersParser:
    """Parses PFR leader pages into structured data dicts."""

    def parse(self, html: str, *, stat: str, scope: str) -> Dict[str, Any]:
        """Parse a leaders page and return a dict ready for model validation.

        Args:
            html: Raw HTML content of the leaders page.
            stat: The stat key (e.g. ``"pass_yds"``).
            scope: The scope (e.g. ``"career"``, ``"single_season"``).

        Returns:
            A dict with keys ``stat``, ``scope``, ``title``, ``entries``.
        """
        soup = BeautifulSoup(html, "html.parser")

        title = None
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)

        entries = self._parse_entries(soup, stat)

        return {
            "stat": stat,
            "scope": scope,
            "title": title,
            "entries": entries,
        }

    @staticmethod
    def _parse_entries(soup: BeautifulSoup, stat: str) -> List[Dict[str, Any]]:
        """Extract all leader entries from the main table.

        The table ID follows the pattern ``{stat}_leaders``
        (e.g. ``pass_yds_leaders``).
        """
        table = soup.find("table", id=f"{stat}_leaders")
        if table is None:
            table = soup.find("table", class_="stats_table")
        if table is None:
            return []

        tbody = table.find("tbody")
        if tbody is None:
            return []

        entries: List[Dict[str, Any]] = []

        for tr in tbody.find_all("tr"):
            classes = tr.get("class") or []
            if "thead" in classes or "over_header" in classes:
                continue

            row: Dict[str, Any] = {}

            # Rank (in <th>)
            rank_cell = tr.find("th", {"data-stat": "rank"})
            if rank_cell:
                rank_text = rank_cell.get_text(strip=True)
                row["rank"] = safe_int(rank_text)

            # Player
            player_cell = tr.find("td", {"data-stat": "player"})
            if player_cell:
                player_id = player_cell.get("data-append-csv")
                if player_id:
                    row["player_id"] = player_id

                link = player_cell.find("a")
                if link:
                    row["player"] = link.get_text(strip=True)
                    row["player_href"] = link.get("href")

                # Active players are wrapped in <strong>
                row["is_active"] = player_cell.find("strong") is not None

                # HOF indicator: "+" text outside the <a> tag
                full_text = player_cell.get_text(strip=True)
                row["is_hof"] = "+" in full_text and (
                    not link or "+" not in link.get_text(strip=True)
                )

            # Stat value column (data-stat matches the stat key)
            stat_cell = tr.find(["td", "th"], {"data-stat": stat})
            if stat_cell:
                row["stat_value"] = stat_cell.get_text(strip=True)

            # Year (single-season pages)
            year_cell = tr.find("td", {"data-stat": "year"})
            if year_cell:
                year_text = year_cell.get_text(strip=True)
                row["year"] = year_text
                year_link = year_cell.find("a")
                if year_link:
                    row["year_href"] = year_link.get("href")

            # Years (career pages)
            years_cell = tr.find("td", {"data-stat": "years"})
            if years_cell:
                row["years"] = years_cell.get_text(strip=True)

            # Team
            team_cell = tr.find("td", {"data-stat": "team"})
            if team_cell:
                row["team"] = team_cell.get_text(strip=True)
                team_link = team_cell.find("a")
                if team_link:
                    row["team_href"] = team_link.get("href")

            if row:
                entries.append(row)

        return entries
