"""Season overview page HTML parser for Pro Football Reference.

Parses PFR ``/years/{year}/`` pages into structured dicts containing
conference standings, playoff results, and team stats.

Also parses ``/years/{year}/{category}.htm`` stat category pages into
per-player stat dicts.
"""

import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int

# Columns in standings tables that should be cast to int.
_STANDINGS_INT_COLS = {"wins", "losses", "points", "points_opp", "points_diff"}

# Columns in playoff standings tables that should be cast to int.
_PLAYOFF_STANDINGS_INT_COLS = {"wins", "losses", "ties"}

# Columns in playoff results tables that should be cast to int.
_PLAYOFF_RESULTS_INT_COLS = {"pts_win", "pts_lose"}

# Columns in playoff results with hrefs to extract.
_PLAYOFF_RESULTS_LINK_COLS = {"winner", "loser", "boxscore_word"}

# Team stat table IDs on the main season page.
_TEAM_STAT_TABLE_IDS = (
    "team_stats",
    "passing",
    "rushing",
    "returns",
    "kicking",
    "punting",
    "team_scoring",
    "team_conversions",
    "drives",
)


class SeasonOverviewParser:
    """Parses PFR season overview and stat category pages."""

    def parse(self, html: str) -> Dict[str, Any]:
        """Parse a PFR season overview page into a JSON-serializable dict.

        Args:
            html: Raw HTML string of a PFR ``/years/{year}/`` page.

        Returns:
            A dict with keys: afc_standings, nfc_standings, playoff_results,
            afc_playoff_standings, nfc_playoff_standings, and team stat tables.
        """
        cleaned = re.sub(r"<!--(.*?)-->", r"\1", html, flags=re.DOTALL)
        soup = BeautifulSoup(cleaned, "html.parser")

        result: Dict[str, Any] = {}
        result["afc_standings"] = self._parse_standings(soup, "AFC")
        result["nfc_standings"] = self._parse_standings(soup, "NFC")
        result["playoff_results"] = self._parse_playoff_results(soup)
        result["afc_playoff_standings"] = self._parse_playoff_standings(
            soup, "afc_playoff_standings"
        )
        result["nfc_playoff_standings"] = self._parse_playoff_standings(
            soup, "nfc_playoff_standings"
        )

        for table_id in _TEAM_STAT_TABLE_IDS:
            result[table_id] = self._parse_generic_table(soup, table_id)

        return result

    def parse_stats(self, html: str) -> Dict[str, Any]:
        """Parse a PFR stat category page into a JSON-serializable dict.

        Args:
            html: Raw HTML string of a PFR ``/years/{year}/{category}.htm`` page.

        Returns:
            A dict with keys: regular_season, postseason — each a list of
            per-player stat dicts.
        """
        cleaned = re.sub(r"<!--(.*?)-->", r"\1", html, flags=re.DOTALL)
        soup = BeautifulSoup(cleaned, "html.parser")

        result: Dict[str, Any] = {"regular_season": [], "postseason": []}

        # Find all stat tables (they have data-stat columns in their rows).
        for table in soup.find_all("table", id=True):
            table_id = table.get("id", "")
            if not table_id:
                continue

            rows = self._parse_player_table(table)
            if not rows:
                continue

            if table_id.endswith("_post"):
                result["postseason"] = rows
            else:
                result["regular_season"] = rows

        return result

    # ------------------------------------------------------------------
    # Conference standings (AFC / NFC)
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_standings(soup: BeautifulSoup, table_id: str) -> List[Dict[str, Any]]:
        """Parse an AFC or NFC standings table.

        Division separator rows (class ``thead``) are used to assign a
        ``division`` field to each team row that follows them.
        """
        table = soup.find("table", id=table_id)
        if table is None:
            return []

        tbody = table.find("tbody")
        if tbody is None:
            return []

        records: List[Dict[str, Any]] = []
        current_division: Optional[str] = None

        for tr in tbody.find_all("tr"):
            classes = tr.get("class") or []

            # Division separator row.
            if "thead" in classes:
                td = tr.find("td")
                if td:
                    current_division = td.get_text(strip=True)
                continue

            if "over_header" in classes:
                continue

            row: Dict[str, Any] = {}
            if current_division:
                row["division"] = current_division

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat")
                if not stat:
                    continue

                text = cell.get_text(strip=True)

                if stat == "team":
                    row["team"] = text
                    a = cell.find("a")
                    if a and a.get("href"):
                        row["team_href"] = a["href"]
                elif stat in _STANDINGS_INT_COLS:
                    row[stat] = safe_int(text)
                else:
                    row[stat] = text

            if row:
                records.append(row)

        return records

    # ------------------------------------------------------------------
    # Playoff results
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_playoff_results(soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse the ``playoff_results`` table."""
        table = soup.find("table", id="playoff_results")
        if table is None:
            return []

        tbody = table.find("tbody")
        if tbody is None:
            return []

        records: List[Dict[str, Any]] = []

        for tr in tbody.find_all("tr"):
            classes = tr.get("class") or []
            if "thead" in classes or "over_header" in classes:
                continue

            row: Dict[str, Any] = {}

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat")
                if not stat:
                    continue

                text = cell.get_text(strip=True)

                if stat in _PLAYOFF_RESULTS_INT_COLS:
                    row[stat] = safe_int(text)
                else:
                    row[stat] = text

                # Extract hrefs from link columns.
                if stat in _PLAYOFF_RESULTS_LINK_COLS:
                    a = cell.find("a")
                    if a and a.get("href"):
                        if stat == "boxscore_word":
                            row["boxscore_href"] = a["href"]
                        else:
                            row[f"{stat}_href"] = a["href"]

            if row:
                records.append(row)

        return records

    # ------------------------------------------------------------------
    # Playoff standings
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_playoff_standings(
        soup: BeautifulSoup, table_id: str
    ) -> List[Dict[str, Any]]:
        """Parse an AFC or NFC playoff standings table."""
        table = soup.find("table", id=table_id)
        if table is None:
            return []

        tbody = table.find("tbody")
        if tbody is None:
            return []

        records: List[Dict[str, Any]] = []

        for tr in tbody.find_all("tr"):
            classes = tr.get("class") or []
            if "thead" in classes or "over_header" in classes:
                continue

            row: Dict[str, Any] = {}

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat")
                if not stat:
                    continue

                text = cell.get_text(strip=True)

                if stat == "team":
                    row["team"] = text
                    a = cell.find("a")
                    if a and a.get("href"):
                        row["team_href"] = a["href"]
                elif stat in _PLAYOFF_STANDINGS_INT_COLS:
                    row[stat] = safe_int(text)
                else:
                    row[stat] = text

            if row:
                records.append(row)

        return records

    # ------------------------------------------------------------------
    # Generic team stat tables
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_generic_table(
        soup: BeautifulSoup, table_id: str
    ) -> List[Dict[str, Any]]:
        """Parse any team stat table generically, preserving all data-stat
        column values and extracting hrefs from the ``team`` column."""
        table = soup.find("table", id=table_id)
        if table is None:
            return []

        tbody = table.find("tbody")
        if tbody is None:
            return []

        records: List[Dict[str, Any]] = []

        for tr in tbody.find_all("tr"):
            classes = tr.get("class") or []
            if "thead" in classes or "over_header" in classes:
                continue

            row: Dict[str, Any] = {}

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat")
                if not stat or stat == "ranker":
                    continue

                text = cell.get_text(strip=True)
                row[stat] = text

                # Extract href from team column.
                if stat == "team":
                    a = cell.find("a")
                    if a and a.get("href"):
                        row["team_href"] = a["href"]

            if row:
                records.append(row)

        return records

    # ------------------------------------------------------------------
    # Player stat tables (for category pages)
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_player_table(table: Tag) -> List[Dict[str, Any]]:
        """Parse a player stat table, extracting all data-stat values,
        player IDs, and hrefs."""
        tbody = table.find("tbody")
        if tbody is None:
            return []

        records: List[Dict[str, Any]] = []

        for tr in tbody.find_all("tr"):
            classes = tr.get("class") or []
            if "thead" in classes or "over_header" in classes:
                continue

            row: Dict[str, Any] = {}

            # Track whether this is a partial (multi-team) row.
            if "partial_table" in classes:
                row["is_partial"] = True

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat")
                if not stat or stat == "ranker":
                    continue

                text = cell.get_text(strip=True)
                row[stat] = text

                # Player name/ID.
                if stat == "name_display":
                    player_id = cell.get("data-append-csv")
                    if player_id:
                        row["player_id"] = player_id
                    a = cell.find("a")
                    if a and a.get("href"):
                        row["player_href"] = a["href"]

                # Team href.
                elif stat == "team_name_abbr":
                    a = cell.find("a")
                    if a and a.get("href"):
                        row["team_href"] = a["href"]

            if row:
                records.append(row)

        return records
