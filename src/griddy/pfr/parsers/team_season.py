"""Team season page HTML parser for Pro Football Reference.

Parses PFR ``/teams/{team_abbrev}/{year}.htm`` pages into structured dicts
containing team metadata, stats, game results, conversions, and player stats.
"""

import re
from typing import Any, Dict, List, Optional, Union

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int, safe_numeric, uncomment_tables

# Columns in the games table that should be cast to int.
_GAME_INT_COLUMNS = {
    "pts_off",
    "pts_def",
    "first_down_off",
    "yards_off",
    "pass_yds_off",
    "rush_yds_off",
    "to_off",
    "first_down_def",
    "yards_def",
    "pass_yds_def",
    "rush_yds_def",
    "to_def",
}

# Columns in the games table that should be cast to float.
_GAME_FLOAT_COLUMNS = {"exp_pts_off", "exp_pts_def", "exp_pts_st"}

# Columns where we extract hrefs.
_GAME_LINK_COLUMNS = {"opp", "boxscore_word"}

# Label mapping for metadata <strong> tags -> field names.
_META_LABEL_MAP: Dict[str, str] = {
    "Record:": "record",
    "Coach:": "coach",
    "Points For:": "points_for",
    "Points Against:": "points_against",
    "Expected W-L:": "expected_wl",
    "Playoffs:": "playoffs",
    "Offensive Coordinator:": "offensive_coordinator",
    "Defensive Coordinator:": "defensive_coordinator",
    "Stadium:": "stadium",
    "Offensive Scheme:": "offensive_scheme",
    "Defensive Alignment:": "defensive_alignment",
    "Preseason Odds:": "preseason_odds",
    "Training Camp:": "training_camp",
}

# Meta labels where we also extract a coach/link href.
_META_HREF_LABELS = {
    "Coach:": "coach_href",
    "Offensive Coordinator:": "offensive_coordinator_href",
    "Defensive Coordinator:": "defensive_coordinator_href",
    "Stadium:": "stadium_href",
}


class TeamSeasonParser:
    """Parses PFR team season pages into comprehensive data dicts."""

    def parse(self, html: str) -> Dict[str, Any]:
        """Parse a PFR team season page into a JSON-serializable dict.

        Args:
            html: Raw HTML string of a PFR team season page.

        Returns:
            A dict with keys: meta, team_stats, games, team_conversions,
            passing, passing_post, rushing_and_receiving.
        """
        cleaned = re.sub(r"<!--(.*?)-->", r"\1", html, flags=re.DOTALL)
        soup = BeautifulSoup(cleaned, "html.parser")

        result: Dict[str, Any] = {}
        result["meta"] = self._parse_meta(soup)
        result["team_stats"] = self._parse_labeled_table(soup, "team_stats")
        result["games"] = self._parse_games(soup)
        result["team_conversions"] = self._parse_labeled_table(soup, "team_conversions")
        result["passing"] = self._parse_player_table(soup, "passing")
        result["passing_post"] = self._parse_player_table(soup, "passing_post")
        result["rushing_and_receiving"] = self._parse_player_table(
            soup, "rushing_and_receiving"
        )

        return result

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_meta(soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract team metadata from the ``#meta`` div."""
        meta_div = soup.find("div", id="meta")
        if meta_div is None:
            return {}

        result: Dict[str, Any] = {}

        for p_tag in meta_div.find_all("p"):
            strong = p_tag.find("strong")
            if not strong:
                continue

            label = strong.get_text(strip=True)
            full_text = p_tag.get_text(strip=True)
            value = full_text.replace(label, "", 1).strip().lstrip(":").strip()

            field_name = _META_LABEL_MAP.get(label)
            if not field_name:
                # Try partial matching for SRS/SOS
                if label.startswith("SRS"):
                    srs_match = re.search(r"SRS:\s*([\d.\-]+)", full_text)
                    sos_match = re.search(r"SOS:\s*([\d.\-]+)", full_text)
                    if srs_match:
                        result["srs"] = srs_match.group(1)
                    if sos_match:
                        result["sos"] = sos_match.group(1)
                continue

            result[field_name] = value

            # Extract record: just the W-L-T string.
            if label == "Record:":
                record_match = re.search(r"(\d+-\d+-\d+)", value)
                if record_match:
                    result["record"] = record_match.group(1)
                div_link = p_tag.find("a")
                if div_link:
                    result["division"] = div_link.get_text(strip=True)
                    result["division_href"] = div_link.get("href", "")

            # Extract coach name (strip the appended record in parens).
            if label == "Coach:":
                link = p_tag.find("a")
                if link:
                    result["coach"] = link.get_text(strip=True)

            # Extract hrefs for coach/coordinator/stadium labels.
            if label in _META_HREF_LABELS:
                href_field = _META_HREF_LABELS[label]
                link = p_tag.find("a")
                if link:
                    result[href_field] = link.get("href", "")

        return result

    # ------------------------------------------------------------------
    # Team Stats / Conversions (labeled tables with row labels)
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_labeled_table(
        soup: BeautifulSoup,
        table_id: str,
    ) -> Dict[str, Dict[str, Union[str, int, float, None]]]:
        """Parse a table where the first column (``data-stat='player'``) is a
        row label (e.g. 'Team Stats', 'Opp. Stats', 'Lg Rank Offense').

        Returns a dict keyed by the row label, with each value being a dict
        of ``{data_stat: value}`` for that row.
        """
        table = soup.find("table", id=table_id)
        if table is None:
            return {}

        result: Dict[str, Dict[str, Union[str, int, float, None]]] = {}

        tbody = table.find("tbody")
        if tbody is None:
            return result

        for tr in tbody.find_all("tr"):
            classes = tr.get("class") or []
            if "thead" in classes:
                continue

            row_data: Dict[str, Union[str, int, float, None]] = {}
            row_label: Optional[str] = None

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat")
                if not stat:
                    continue
                text = cell.get_text(strip=True)

                if stat == "player":
                    row_label = text
                    continue

                row_data[stat] = safe_numeric(text)

            if row_label:
                result[row_label] = row_data

        return result

    # ------------------------------------------------------------------
    # Games table
    # ------------------------------------------------------------------

    def _parse_games(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse the schedule/results ``games`` table."""
        table = soup.find("table", id="games")
        if table is None:
            return []

        tbody = table.find("tbody")
        if tbody is None:
            return []

        games: List[Dict[str, Any]] = []

        for tr in tbody.find_all("tr"):
            classes = tr.get("class") or []
            if "thead" in classes:
                continue

            row_data: Dict[str, Any] = {}
            all_empty = True

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat")
                if not stat:
                    continue

                text = cell.get_text(strip=True)

                if text and text != "Playoffs":
                    all_empty = False

                # Cast numeric columns.
                if stat in _GAME_INT_COLUMNS:
                    row_data[stat] = safe_int(text)
                elif stat in _GAME_FLOAT_COLUMNS:
                    row_data[stat] = float(text) if text else None
                else:
                    row_data[stat] = text

                # Extract links.
                if stat in _GAME_LINK_COLUMNS:
                    link = cell.find("a")
                    href = link["href"] if link and link.get("href") else None
                    row_data[f"{stat}_href"] = href

            # Skip label-only rows (e.g. "Playoffs" divider).
            if all_empty:
                continue

            games.append(row_data)

        return games

    # ------------------------------------------------------------------
    # Player stats tables (passing, rushing_and_receiving)
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_player_table(
        soup: BeautifulSoup,
        table_id: str,
    ) -> List[Dict[str, Any]]:
        """Parse a player stats table (passing, rushing_and_receiving).

        Extracts ``data-append-csv`` as ``player_id`` and ``name_display``
        link hrefs as ``player_href``.
        """
        table = soup.find("table", id=table_id)
        if table is None:
            return []

        tbody = table.find("tbody")
        if tbody is None:
            return []

        rows: List[Dict[str, Any]] = []

        for tr in tbody.find_all("tr"):
            classes = tr.get("class") or []
            if "thead" in classes:
                continue

            row_data: Dict[str, Any] = {}

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat")
                if not stat:
                    continue

                text = cell.get_text(strip=True)
                row_data[stat] = safe_numeric(text)

                # Extract player ID and link.
                if stat == "name_display":
                    csv_id = cell.get("data-append-csv")
                    if csv_id:
                        row_data["player_id"] = csv_id
                    link = cell.find("a")
                    if link:
                        row_data["player_href"] = link.get("href", "")

            if row_data:
                rows.append(row_data)

        return rows
