"""Parser for PFR Super Bowl pages.

Handles three page types:
- ``/super-bowl/`` — Super Bowl history (table ``#super_bowls``)
- ``/super-bowl/leaders.htm`` — Super Bowl leaders (leaderboard tables)
- ``/super-bowl/standings.htm`` — franchise standings (table ``#standings``)
"""

import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int


class SuperBowlParser:
    """Parses PFR Super Bowl pages into structured data dicts."""

    # ------------------------------------------------------------------
    # History — /super-bowl/
    # ------------------------------------------------------------------

    def parse_history(self, html: str) -> Dict[str, Any]:
        """Parse the Super Bowl history page.

        Returns:
            A dict with key ``games``.
        """
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="super_bowls")
        if table is None:
            return {"games": []}

        games = self._parse_history_rows(table)
        return {"games": games}

    @staticmethod
    def _parse_history_rows(table: Tag) -> List[Dict[str, Any]]:
        """Extract Super Bowl game rows from the super_bowls table."""
        tbody = table.find("tbody")
        if tbody is None:
            return []

        games: List[Dict[str, Any]] = []

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

                if stat == "game_date":
                    row["game_date"] = text or None
                elif stat == "superbowl":
                    # Format: "LX(60)" — extract roman numeral and number
                    if link:
                        row["superbowl"] = link.get_text(strip=True)
                        row["boxscore_href"] = link.get("href")
                    else:
                        row["superbowl"] = text or None
                    # Extract number from parentheses
                    match = re.search(r"\((\d+)\)", text)
                    if match:
                        row["superbowl_number"] = int(match.group(1))
                elif stat == "sb_winner":
                    row["winner"] = text or None
                    if link:
                        row["winner_href"] = link.get("href")
                elif stat == "sb_winner_points":
                    row["winner_points"] = safe_int(text)
                elif stat == "sb_loser":
                    row["loser"] = text or None
                    if link:
                        row["loser_href"] = link.get("href")
                elif stat == "sb_loser_points":
                    row["loser_points"] = safe_int(text)
                elif stat == "sb_mvp":
                    # MVP name may have "+" suffix in the text
                    if link:
                        row["mvp"] = link.get_text(strip=True)
                        row["mvp_href"] = link.get("href")
                    else:
                        row["mvp"] = text or None
                elif stat == "stadium":
                    row["stadium"] = text or None
                    if link:
                        row["stadium_href"] = link.get("href")
                elif stat == "city":
                    row["city"] = text or None
                elif stat == "state":
                    row["state"] = text or None

            if not all_empty:
                games.append(row)

        return games

    # ------------------------------------------------------------------
    # Leaders — /super-bowl/leaders.htm
    # ------------------------------------------------------------------

    def parse_leaders(self, html: str) -> Dict[str, Any]:
        """Parse the Super Bowl leaders page.

        Returns:
            A dict with key ``tables``.
        """
        soup = BeautifulSoup(html, "html.parser")

        tables_data: List[Dict[str, Any]] = []

        for table in soup.find_all("table"):
            caption = table.find("caption")
            if caption is None:
                continue

            category = caption.get_text(strip=True)
            entries = self._parse_leader_rows(table)
            tables_data.append({"category": category, "entries": entries})

        return {"tables": tables_data}

    @staticmethod
    def _parse_leader_rows(table: Tag) -> List[Dict[str, Any]]:
        """Extract leader entries from a leaderboard table."""
        tbody = table.find("tbody")
        rows = tbody.find_all("tr") if tbody else table.find_all("tr")

        entries: List[Dict[str, Any]] = []

        for tr in rows:
            entry: Dict[str, Any] = {}

            for td in tr.find_all("td"):
                css_classes = td.get("class", [])

                if "rank" in css_classes:
                    rank_text = td.get_text(strip=True).rstrip(".")
                    entry["rank"] = safe_int(rank_text)
                elif "who" in css_classes:
                    link = td.find("a")
                    if link:
                        entry["player"] = link.get_text(strip=True)
                        entry["player_href"] = link.get("href")
                    desc = td.find("span", class_="desc")
                    if desc:
                        entry["description"] = desc.get_text(strip=True)
                elif "value" in css_classes:
                    entry["value"] = td.get_text(strip=True)

            if entry:
                entries.append(entry)

        return entries

    # ------------------------------------------------------------------
    # Standings — /super-bowl/standings.htm
    # ------------------------------------------------------------------

    def parse_standings(self, html: str) -> Dict[str, Any]:
        """Parse the Super Bowl standings page.

        Returns:
            A dict with key ``teams``.
        """
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="standings")
        if table is None:
            return {"teams": []}

        teams = self._parse_standings_rows(table)
        return {"teams": teams}

    @staticmethod
    def _parse_standings_rows(table: Tag) -> List[Dict[str, Any]]:
        """Extract franchise standings rows."""
        tbody = table.find("tbody")
        if tbody is None:
            return []

        teams: List[Dict[str, Any]] = []

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

                if stat == "ranker":
                    row["rank"] = safe_int(text)
                elif stat == "team":
                    row["team"] = text or None
                    if link:
                        row["team_href"] = link.get("href")
                elif stat == "g":
                    row["games"] = safe_int(text)
                elif stat == "wins":
                    row["wins"] = safe_int(text)
                elif stat == "losses":
                    row["losses"] = safe_int(text)
                elif stat == "win_loss_perc":
                    row["win_loss_pct"] = text or None
                elif stat == "points":
                    row["points"] = safe_int(text)
                elif stat == "points_opp":
                    row["points_opp"] = safe_int(text)
                elif stat == "points_diff":
                    row["points_diff"] = text or None
                elif stat == "sb_qbs":
                    row["qbs"] = _parse_qbs(cell)

            if not all_empty:
                teams.append(row)

        return teams


def _parse_qbs(cell: Tag) -> List[Dict[str, Optional[str]]]:
    """Parse the sb_qbs cell into a list of QB dicts with name, href, record."""
    qbs: List[Dict[str, Optional[str]]] = []

    for link in cell.find_all("a"):
        qb: Dict[str, Optional[str]] = {
            "player": link.get_text(strip=True),
            "player_href": link.get("href"),
        }
        # The record appears in parentheses after the link text
        # e.g., '<a>Terry Bradshaw</a> (4-0), <a>...'
        next_sibling = link.next_sibling
        if next_sibling and isinstance(next_sibling, str):
            match = re.search(r"\((\d+-\d+)\)", next_sibling)
            if match:
                qb["record"] = match.group(1)
        qbs.append(qb)

    return qbs
