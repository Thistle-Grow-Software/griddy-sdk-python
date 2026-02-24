"""Schedule HTML parser for Pro Football Reference.

Parses the season-schedule table from PFR ``/years/{season}/games.htm`` pages.
"""

from typing import Any, Dict, List

from bs4 import BeautifulSoup, Tag

from griddy.pfr.models.entities.schedule_game import ScheduleGame

from ._helpers import safe_int

# Columns in the PFR schedule table where the cell value should be cast to int.
_INT_COLUMNS = {"pts_win", "pts_lose", "yards_win", "to_win", "yards_lose", "to_lose"}

# Columns where we also want to extract the ``href`` from a child ``<a>`` tag.
_LINK_COLUMNS = {"winner", "loser", "boxscore_word"}


class ScheduleParser:
    """Parses the PFR season-schedule HTML table."""

    @staticmethod
    def _extract_cell(cell: Tag, stat: str) -> Dict[str, Any]:
        """Extract text and optional href from a single ``<td>`` or ``<th>``.

        Returns a dict with at least ``{stat: text_value}``.  For columns in
        ``_LINK_COLUMNS``, an additional ``{stat}_href`` key is added when a
        link is present.  For columns in ``_INT_COLUMNS`` the value is cast
        to ``int | None``.
        """
        text = cell.get_text(strip=True)
        result: Dict[str, Any] = {}

        if stat in _INT_COLUMNS:
            result[stat] = safe_int(text)
        else:
            result[stat] = text

        if stat in _LINK_COLUMNS:
            link = cell.find("a")
            result[f"{stat}_href"] = link["href"] if link and link.get("href") else None

        return result

    def parse(self, html: str) -> List[ScheduleGame]:
        """Parse the PFR season-schedule table into a list of ScheduleGame models.

        Looks for ``<table id="games">``, iterates over ``<tbody> <tr>`` rows,
        and skips:

        * Separator rows (``class="thead"``)
        * Rows where *all* data cells are empty (e.g. the "Playoffs" label row)

        Args:
            html: Raw HTML string of a PFR ``/years/{season}/games.htm`` page.

        Returns:
            A list of ``ScheduleGame`` models, one per game.

        Raises:
            ValueError: If ``<table id="games">`` is not found in the HTML.
        """
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", id="games")
        if table is None:
            raise ValueError("Could not find <table id='games'> in the HTML.")

        tbody = table.find("tbody")
        if tbody is None:
            raise ValueError("Could not find <tbody> inside the games table.")

        games: List[ScheduleGame] = []

        for row in tbody.find_all("tr"):
            # Skip separator header rows that repeat column names mid-table.
            if "thead" in (row.get("class") or []):
                continue

            game_data: Dict[str, Any] = {}
            cells = row.find_all(["th", "td"])

            all_empty = True
            for cell in cells:
                stat = cell.get("data-stat")
                if not stat:
                    continue
                extracted = self._extract_cell(cell, stat)
                game_data.update(extracted)
                # Check if this cell has meaningful text content.
                text = cell.get_text(strip=True)
                if text and text != "Playoffs":
                    all_empty = False

            # Skip label-only rows (e.g. the "Playoffs" divider).
            if all_empty:
                continue

            games.append(ScheduleGame(**game_data))

        return games
