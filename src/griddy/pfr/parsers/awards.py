"""Parser for PFR Awards, Hall of Fame, and Pro Bowl pages.

Handles three page types:
- ``/awards/{award}.htm`` — award history (table ``#awards``)
- ``/hof/`` — Hall of Fame inductees (table ``#hof_players``)
- ``/years/{year}/probowl.htm`` — Pro Bowl roster (table ``#pro_bowl``)
"""

from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int

# Columns whose text should be cast to int
_INT_COLUMNS = {
    "all_pros_first_team",
    "pro_bowls",
    "years_as_primary_starter",
    "career_av",
    "g",
    "gs",
    "pass_cmp",
    "pass_att",
    "pass_yds",
    "pass_td",
    "pass_long",
    "pass_int",
    "pass_sacked",
    "pass_sacked_yds",
    "rush_att",
    "rush_yds",
    "rush_td",
    "rush_long",
    "rec",
    "rec_yds",
    "rec_td",
    "rec_long",
    "all_purpose_yds",
    "all_td",
    "tackles_combined",
    "tackles_solo",
    "def_int",
    "age",
    "experience",
    "year_min",
    "year_max",
}

_FLOAT_COLUMNS = {
    "sacks",
}


def _safe_float(value: str) -> Optional[float]:
    """Convert a string to float, returning None for empty/non-numeric."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


class AwardsParser:
    """Parses PFR awards, HOF, and Pro Bowl pages into structured data dicts."""

    # ------------------------------------------------------------------
    # Award History — /awards/{award}.htm
    # ------------------------------------------------------------------

    def parse_award(self, html: str, *, award: str) -> Dict[str, Any]:
        """Parse an award history page and return a dict for model validation.

        Returns:
            A dict with keys ``award``, ``winners``.
        """
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="awards")
        if table is None:
            return {"award": award, "winners": []}

        winners = self._parse_award_rows(table)
        return {"award": award, "winners": winners}

    @staticmethod
    def _parse_award_rows(table: Tag) -> List[Dict[str, Any]]:
        """Extract award winner rows from the awards table."""
        tbody = table.find("tbody")
        if tbody is None:
            return []

        winners: List[Dict[str, Any]] = []

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
                elif stat == "league_id":
                    row["league"] = text or None
                elif stat == "pos":
                    row["pos"] = text or None
                elif stat == "player":
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
                elif stat == "voting":
                    link = cell.find("a")
                    if link:
                        row["voting_href"] = link.get("href")

            if not all_empty:
                winners.append(row)

        return winners

    # ------------------------------------------------------------------
    # Hall of Fame — /hof/
    # ------------------------------------------------------------------

    def parse_hof(self, html: str) -> Dict[str, Any]:
        """Parse the Hall of Fame page and return a dict for model validation.

        Returns:
            A dict with key ``players``.
        """
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="hof_players")
        if table is None:
            return {"players": []}

        players = self._parse_hof_rows(table)
        return {"players": players}

    @staticmethod
    def _parse_hof_rows(table: Tag) -> List[Dict[str, Any]]:
        """Extract HOF player rows from the hof_players table."""
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

                text = cell.get_text(strip=True)
                if text:
                    all_empty = False

                if stat == "ranker":
                    row["rank"] = safe_int(text)
                elif stat == "player":
                    row["player"] = text
                    player_id = cell.get("data-append-csv")
                    if player_id:
                        row["player_id"] = player_id
                    link = cell.find("a")
                    if link:
                        row["player_href"] = link.get("href")
                elif stat == "pos":
                    row["pos"] = text or None
                elif stat == "year_induction":
                    row["year_induction"] = safe_int(text)
                    link = cell.find("a")
                    if link:
                        row["year_induction_href"] = link.get("href")
                elif stat in _INT_COLUMNS:
                    row[stat] = safe_int(text)
                elif stat in _FLOAT_COLUMNS:
                    row[stat] = _safe_float(text)

            if not all_empty:
                players.append(row)

        return players

    # ------------------------------------------------------------------
    # Pro Bowl Roster — /years/{year}/probowl.htm
    # ------------------------------------------------------------------

    def parse_probowl(self, html: str, *, year: int) -> Dict[str, Any]:
        """Parse a Pro Bowl roster page and return a dict for model validation.

        Returns:
            A dict with keys ``year``, ``players``.
        """
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="pro_bowl")
        if table is None:
            return {"year": year, "players": []}

        players = self._parse_probowl_rows(table)
        return {"year": year, "players": players}

    @staticmethod
    def _parse_probowl_rows(table: Tag) -> List[Dict[str, Any]]:
        """Extract Pro Bowl player rows from the pro_bowl table."""
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

                text = cell.get_text(strip=True)
                if text:
                    all_empty = False

                if stat == "pos":
                    row["pos"] = text or None
                elif stat == "player":
                    # Player name may have markers: % (did not play), + (replacement)
                    player_id = cell.get("data-append-csv")
                    if player_id:
                        row["player_id"] = player_id

                    link = cell.find("a")
                    if link:
                        row["player"] = link.get_text(strip=True)
                        row["player_href"] = link.get("href")
                    else:
                        row["player"] = text

                    # Bold = starter
                    row["is_starter"] = cell.find("strong") is not None

                    # Check for markers in text outside the <a> tag
                    full_text = cell.get_text(strip=True)
                    link_text = link.get_text(strip=True) if link else ""
                    suffix = full_text[len(link_text) :]
                    row["did_not_play"] = "%" in suffix
                    row["is_replacement"] = "+" in suffix
                elif stat == "conference_id":
                    row["conference"] = text or None
                elif stat == "team":
                    row["team"] = text
                    link = cell.find("a")
                    if link:
                        row["team_href"] = link.get("href")
                elif stat == "all_pro_string":
                    row["all_pro_string"] = text or None
                elif stat in _INT_COLUMNS:
                    row[stat] = safe_int(text)
                elif stat in _FLOAT_COLUMNS:
                    row[stat] = _safe_float(text)

            if not all_empty:
                players.append(row)

        return players
