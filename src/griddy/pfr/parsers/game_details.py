"""Game details (boxscore) HTML parser for Pro Football Reference.

Parses PFR ``/boxscores/{game_id}.htm`` pages into structured dicts
containing scorebox, linescore, scoring plays, team stats, player stats,
drives, and more.
"""

import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int, safe_numeric, uncomment_tables


class GameDetailsParser:
    """Parses PFR boxscore pages into comprehensive game data dicts."""

    def parse(self, html: str) -> Dict[str, Any]:
        """Parse a PFR boxscore page into a comprehensive JSON-serializable dict.

        Extracts all game-specific data from
        ``/boxscores/{game_id}.htm`` pages, including:

        * Scorebox metadata (teams, final scores, records, coaches)
        * Quarter-by-quarter linescore
        * Scoring plays
        * Game info (coin toss, weather, surface, vegas line, etc.)
        * Officials
        * Expected points summary
        * Team stats (first downs, yards, turnovers, etc.)
        * Player offense (passing, rushing, receiving)
        * Player defense (interceptions, tackles, sacks)
        * Kick/punt returns
        * Kicking & punting
        * Home/visitor starters
        * Home/visitor snap counts
        * Home/visitor drives

        Many tables on PFR boxscore pages are hidden inside HTML comments
        as an anti-scraping measure.  This parser extracts and parses those
        commented-out tables as well.

        Args:
            html: Raw HTML string of a PFR boxscore page.

        Returns:
            A dict with all extracted game data.
        """
        soup = BeautifulSoup(html, "html.parser")

        result: Dict[str, Any] = {}

        result["scorebox"] = self._parse_scorebox(soup)
        result["linescore"] = self._parse_linescore(soup)

        # Uncomment hidden HTML so all tables become visible to BS4.
        uncomment_tables(soup)

        result["scoring"] = self._parse_table_rows(soup, "scoring")
        result["game_info"] = self._parse_kv_table(soup, "game_info")
        result["officials"] = self._parse_kv_table(soup, "officials")
        result["expected_points"] = self._parse_table_rows(soup, "expected_points")
        result["team_stats"] = self._parse_team_stats(soup)
        result["player_offense"] = self._parse_table_rows(soup, "player_offense")
        result["player_defense"] = self._parse_table_rows(soup, "player_defense")
        result["returns"] = self._parse_table_rows(soup, "returns")
        result["kicking"] = self._parse_table_rows(soup, "kicking")
        result["home_starters"] = self._parse_table_rows(soup, "home_starters")
        result["vis_starters"] = self._parse_table_rows(soup, "vis_starters")
        result["home_snap_counts"] = self._parse_table_rows(soup, "home_snap_counts")
        result["vis_snap_counts"] = self._parse_table_rows(soup, "vis_snap_counts")
        result["home_drives"] = self._parse_table_rows(soup, "home_drives")
        result["vis_drives"] = self._parse_table_rows(soup, "vis_drives")

        return result

    # ------------------------------------------------------------------
    # Private helpers (in call order)
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_scorebox(soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract team names, scores, records, and coaches from the
        ``div.scorebox`` section, plus date/stadium/attendance metadata
        from ``div.scorebox_meta``.
        """
        scorebox = soup.find("div", class_="scorebox")
        if scorebox is None:
            return {}

        teams: List[Dict[str, Any]] = []
        for team_div in scorebox.find_all("div", class_="scorebox_team", limit=2):
            team_data: Dict[str, Any] = {}
            # Team name from the <strong><a> inside the first child div.
            strong = team_div.find("strong")
            if strong:
                link = strong.find("a")
                if link:
                    team_data["name"] = link.get_text(strip=True)
                    team_data["href"] = link.get("href", "")

            # Final score.
            score_div = team_div.find("div", class_="score")
            if score_div:
                team_data["score"] = safe_int(score_div.get_text(strip=True))

            # Record (e.g. "1-0") — text node directly after scores div.
            scores_div = team_div.find("div", class_="scores")
            if scores_div:
                record_div = scores_div.find_next_sibling("div")
                if record_div and "scorebox" not in (record_div.get("class") or []):
                    team_data["record"] = record_div.get_text(strip=True)

            # Coach.
            coach_dp = team_div.find("div", class_="datapoint")
            if coach_dp:
                coach_link = coach_dp.find("a")
                if coach_link:
                    team_data["coach"] = coach_link.get_text(strip=True)
                    team_data["coach_href"] = coach_link.get("href", "")

            teams.append(team_data)

        result: Dict[str, Any] = {}
        if len(teams) >= 2:
            result["away"] = teams[0]
            result["home"] = teams[1]

        # Scorebox metadata (date, start time, stadium, attendance, etc.)
        meta_div = scorebox.find("div", class_="scorebox_meta")
        if meta_div:
            meta: Dict[str, str] = {}
            for div in meta_div.find_all("div", recursive=False):
                strong = div.find("strong")
                if strong:
                    key = strong.get_text(strip=True).rstrip(":")
                    # Value is everything after the <strong> tag.
                    val_parts = []
                    for sibling in strong.next_siblings:
                        if isinstance(sibling, Tag):
                            val_parts.append(sibling.get_text(strip=True))
                        else:
                            val_parts.append(str(sibling).strip())
                    meta[key] = " ".join(val_parts).strip().lstrip(": ")
                elif not div.find("em"):
                    # Plain text div (e.g. "Thursday Sep 10, 2015").
                    text = div.get_text(strip=True)
                    if text:
                        meta["date"] = text
            result["meta"] = meta

        return result

    @staticmethod
    def _parse_linescore(soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse the quarter-by-quarter linescore table."""
        table = soup.find("table", class_="linescore")
        if table is None:
            return []

        # Read header to determine quarter labels.
        header_row = table.find("thead")
        headers: List[str] = []
        if header_row:
            for th in header_row.find_all("th"):
                text = th.get_text(strip=True)
                if text:
                    headers.append(text)

        rows: List[Dict[str, Any]] = []
        tbody = table.find("tbody")
        if tbody is None:
            return rows

        for tr in tbody.find_all("tr"):
            cells = tr.find_all("td")
            if len(cells) < 3:
                continue
            row_data: Dict[str, Any] = {}
            # Second <td> has team name/link.
            team_cell = cells[1]
            link = team_cell.find("a")
            if link:
                row_data["team"] = link.get_text(strip=True)
                row_data["team_href"] = link.get("href", "")
            else:
                row_data["team"] = team_cell.get_text(strip=True)

            # Quarter scores start at cells[2].
            quarters: List[Optional[int]] = []
            for cell in cells[2:]:
                quarters.append(safe_int(cell.get_text(strip=True)))

            # Map quarter scores to header labels (skip first 2 blanks).
            quarter_headers = [h for h in headers if h not in ("", "\xa0")]
            if quarter_headers and len(quarters) == len(quarter_headers):
                row_data["quarters"] = dict(zip(quarter_headers, quarters))
            else:
                row_data["quarters"] = quarters

            rows.append(row_data)

        return rows

    def _parse_table_rows(
        self,
        soup: BeautifulSoup,
        table_id: str,
    ) -> List[Dict[str, Any]]:
        """Generic parser for any PFR stats table identified by *table_id*.

        Iterates ``<tbody> <tr>`` rows, reads each cell's ``data-stat``
        attribute as the key, and extracts the text value.  Player cells
        (``data-stat="player"``) also get a ``player_href`` and
        ``player_id`` (from ``data-append-csv``).

        Skips mid-table header rows (``class="thead"``).
        """
        table = soup.find("table", id=table_id)
        if table is None:
            return []

        tbody = table.find("tbody")
        if tbody is None:
            # Some tables (game_info, officials) have no <tbody>; rows are
            # direct children of <table>.
            tbody = table

        rows: List[Dict[str, Any]] = []
        for tr in tbody.find_all("tr", recursive=False):
            classes = tr.get("class") or []
            if "thead" in classes or "over_header" in classes:
                continue
            # Skip one-cell header rows.
            onecell = tr.find("td", class_="onecell")
            if onecell:
                continue

            row_data: Dict[str, Any] = {}
            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat")
                if not stat:
                    continue
                text = cell.get_text(strip=True)
                row_data[stat] = safe_numeric(text)

                # Extract player link and PFR ID.
                if stat == "player":
                    link = cell.find("a")
                    if link:
                        row_data["player_href"] = link.get("href", "")
                    csv_id = cell.get("data-append-csv")
                    if csv_id:
                        row_data["player_id"] = csv_id

                # Extract any other links (team names, official names, etc.)
                elif cell.find("a"):
                    link = cell.find("a")
                    if link and link.get("href"):
                        row_data[f"{stat}_href"] = link["href"]

            if row_data:
                rows.append(row_data)

        return rows

    @staticmethod
    def _parse_kv_table(
        soup: BeautifulSoup,
        table_id: str,
    ) -> Dict[str, Any]:
        """Parse a two-column key/value table (game_info, officials)."""
        table = soup.find("table", id=table_id)
        if table is None:
            return {}

        result: Dict[str, Any] = {}
        for tr in table.find_all("tr"):
            cells = tr.find_all(["th", "td"])
            if len(cells) < 2:
                continue
            key_cell, val_cell = cells[0], cells[1]
            # Skip header rows.
            if key_cell.get("data-stat") in ("onecell", None):
                continue
            key = key_cell.get_text(strip=True)
            if not key:
                continue
            val = val_cell.get_text(strip=True)
            result[key] = val

        return result

    @staticmethod
    def _parse_team_stats(soup: BeautifulSoup) -> Dict[str, Any]:
        """Parse the three-column team stats table into a structured dict.

        The table has rows like "First Downs | 23 | 26" with columns
        stat, vis_stat, home_stat.
        """
        table = soup.find("table", id="team_stats")
        if table is None:
            return {}

        # Read team abbreviations from header.
        vis_team = "vis"
        home_team = "home"
        thead = table.find("thead")
        if thead:
            headers = thead.find_all("th")
            for h in headers:
                ds = h.get("data-stat")
                if ds == "vis_stat":
                    vis_team = h.get_text(strip=True)
                elif ds == "home_stat":
                    home_team = h.get_text(strip=True)

        stats: Dict[str, Dict[str, str]] = {}
        for tr in table.find_all("tr"):
            cells = tr.find_all(["th", "td"])
            if len(cells) < 3:
                continue
            stat_name = cells[0].get_text(strip=True)
            if not stat_name:
                continue
            vis_val = cells[1].get_text(strip=True)
            home_val = cells[2].get_text(strip=True)
            # Use a snake_case key derived from the stat label.
            key = re.sub(r"[^a-z0-9]+", "_", stat_name.lower()).strip("_")
            stats[key] = {vis_team: vis_val, home_team: home_val}

        return stats
