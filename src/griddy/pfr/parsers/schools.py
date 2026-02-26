"""Parser for PFR Schools & Colleges pages.

Handles two page types:
- ``/schools/`` — All Player Colleges (table ``#college_stats_table``)
- ``/schools/high_schools.cgi`` — High Schools (table ``#high_schools``)
"""

from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int


class SchoolsParser:
    """Parses PFR Schools & Colleges pages into structured data dicts."""

    # ------------------------------------------------------------------
    # Colleges — /schools/
    # ------------------------------------------------------------------

    def parse_colleges(self, html: str) -> Dict[str, Any]:
        """Parse the colleges / universities index page.

        Returns:
            A dict with key ``colleges``.
        """
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="college_stats_table")
        if table is None:
            return {"colleges": []}

        colleges = self._parse_college_rows(table)
        return {"colleges": colleges}

    @staticmethod
    def _parse_college_rows(table: Tag) -> List[Dict[str, Any]]:
        """Extract college rows from the college_stats_table."""
        tbody = table.find("tbody")
        if tbody is None:
            return []

        colleges: List[Dict[str, Any]] = []

        for tr in tbody.find_all("tr"):
            if "thead" in (tr.get("class") or []):
                continue

            row: Dict[str, Any] = {}
            all_empty = True

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat", "")
                if not stat:
                    continue

                text = cell.get_text(strip=True).replace("\xa0", " ")
                if text:
                    all_empty = False

                link = cell.find("a")

                if stat == "ranker":
                    row["rank"] = safe_int(text)
                elif stat == "college_name":
                    row["college_name"] = text or None
                    if link:
                        row["college_href"] = link.get("href")
                elif stat == "state":
                    row["state"] = text or None
                elif stat == "players":
                    row["players"] = safe_int(text)
                elif stat == "players_active":
                    row["players_active"] = safe_int(text)
                elif stat == "hofers":
                    row["hofers"] = safe_int(text)
                elif stat == "pro_bowls":
                    row["pro_bowls"] = safe_int(text)
                elif stat == "g":
                    row["games"] = safe_int(text)
                elif stat == "td":
                    row["touchdowns"] = safe_int(text)
                elif stat == "player_best_career_av":
                    row["best_career_av_player"] = text or None
                    if link:
                        row["best_career_av_player_href"] = link.get("href")
                elif stat == "best_career_av":
                    row["best_career_av"] = safe_int(text)
                elif stat == "player_most_td":
                    row["most_td_player"] = text or None
                    if link:
                        row["most_td_player_href"] = link.get("href")
                elif stat == "most_td":
                    row["most_td"] = safe_int(text)
                elif stat == "player_most_g":
                    row["most_games_player"] = text or None
                    if link:
                        row["most_games_player_href"] = link.get("href")
                elif stat == "most_g":
                    row["most_games"] = safe_int(text)

            if not all_empty:
                colleges.append(row)

        return colleges

    # ------------------------------------------------------------------
    # High Schools — /schools/high_schools.cgi
    # ------------------------------------------------------------------

    def parse_high_schools(self, html: str) -> Dict[str, Any]:
        """Parse the high schools index page.

        Returns:
            A dict with key ``schools``.
        """
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="high_schools")
        if table is None:
            return {"schools": []}

        schools = self._parse_high_school_rows(table)
        return {"schools": schools}

    @staticmethod
    def _parse_high_school_rows(table: Tag) -> List[Dict[str, Any]]:
        """Extract high school rows from the high_schools table."""
        tbody = table.find("tbody")
        if tbody is None:
            return []

        schools: List[Dict[str, Any]] = []

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

                link = cell.find("a")

                if stat == "high_school_name":
                    row["name"] = text or None
                    if link:
                        row["name_href"] = link.get("href")
                elif stat == "hs_city":
                    row["city"] = text or None
                elif stat == "hs_state":
                    row["state"] = text or None
                elif stat == "num_players":
                    row["num_players"] = safe_int(text)
                elif stat == "num_active":
                    row["num_active"] = safe_int(text)

            if not all_empty:
                schools.append(row)

        return schools
