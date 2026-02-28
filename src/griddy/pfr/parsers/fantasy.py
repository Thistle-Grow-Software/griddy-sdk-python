"""Parser for PFR Fantasy Rankings pages.

Handles:
- ``/years/{year}/fantasy.htm`` — Top Fantasy Players (table ``#fantasy``)
"""

from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int, safe_numeric


class FantasyParser:
    """Parses PFR Fantasy Rankings pages into structured data dicts."""

    # Columns that should be converted to int.
    _INT_COLUMNS = frozenset(
        {
            "g",
            "gs",
            "pass_cmp",
            "pass_att",
            "pass_yds",
            "pass_td",
            "pass_int",
            "rush_att",
            "rush_yds",
            "rush_td",
            "targets",
            "rec",
            "rec_yds",
            "rec_td",
            "fumbles",
            "fumbles_lost",
            "all_td",
            "two_pt_md",
            "two_pt_pass",
            "vbd",
            "fantasy_rank_pos",
            "fantasy_rank_overall",
        }
    )

    # Columns that may contain float values.
    _FLOAT_COLUMNS = frozenset(
        {
            "rush_yds_per_att",
            "rec_yds_per_rec",
            "fantasy_points",
            "fantasy_points_ppr",
            "draftkings_points",
            "fanduel_points",
        }
    )

    def parse_top_players(self, html: str) -> Dict[str, Any]:
        """Parse the top fantasy players page.

        Returns:
            A dict with key ``players``.
        """
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="fantasy")
        if table is None:
            return {"players": []}

        players = self._parse_player_rows(table)
        return {"players": players}

    def _parse_player_rows(self, table: Tag) -> List[Dict[str, Any]]:
        """Extract player rows from the fantasy table."""
        tbody = table.find("tbody")
        if tbody is None:
            return []

        players: List[Dict[str, Any]] = []

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
                elif stat == "player":
                    row["player"] = text or None
                    if link:
                        row["player_href"] = link.get("href")
                    player_id = cell.get("data-append-csv")
                    if player_id:
                        row["player_id"] = player_id
                elif stat == "team":
                    row["team"] = text or None
                    if link:
                        row["team_href"] = link.get("href")
                elif stat == "fantasy_pos":
                    row["fantasy_pos"] = text or None
                elif stat == "age":
                    row["age"] = safe_int(text)
                elif stat in self._INT_COLUMNS:
                    row[stat] = safe_int(text)
                elif stat in self._FLOAT_COLUMNS:
                    row[stat] = safe_numeric(text)

            if not all_empty:
                players.append(row)

        return players
