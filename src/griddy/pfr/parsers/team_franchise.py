"""Team franchise page HTML parser for Pro Football Reference.

Parses PFR ``/teams/{team_abbrev}/`` pages into structured dicts
containing franchise metadata and year-by-year season records.
"""

import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int, safe_numeric

# Columns in the team_index table that should be cast to int.
_INT_COLUMNS = {
    "wins",
    "losses",
    "ties",
    "points",
    "points_opp",
    "points_diff",
    "rank_off_pts",
    "rank_off_yds",
    "rank_def_pts",
    "rank_def_yds",
    "rank_takeaway_giveaway",
    "rank_points_diff",
    "rank_yds_diff",
    "teams_in_league",
}

# Columns in the team_index table that should be cast to float.
_FLOAT_COLUMNS = {"mov", "sos_total", "srs_total", "srs_offense", "srs_defense"}

# Columns where we extract hrefs from links.
_LINK_COLUMNS = {
    "year_id": "year_href",
    "league_id": "league_href",
    "team": "team_href",
    "coaches": "coaches_href",
    "playoff_result": "playoff_result_href",
}

# Columns where we extract the link's title attribute.
_TITLE_COLUMNS = {"av", "passer", "rusher", "receiver"}

# Label mapping for metadata <strong> tags -> field names.
_META_LABEL_MAP: Dict[str, str] = {
    "Team Names:": "team_names",
    "Seasons:": "seasons",
    "Record (W-L-T):": "record",
    "Playoff Record:": "playoff_record",
    "Super Bowls Won:": "super_bowls_won",
    "Championships Won*:": "championships_won",
}

# Leader labels that produce nested dicts with name, href, stats.
_LEADER_LABELS: Dict[str, str] = {
    "All-time Passing Leader": "all_time_passing_leader",
    "All-time Rushing Leader": "all_time_rushing_leader",
    "All-time Receiving Leader": "all_time_receiving_leader",
    "All-time Scoring Leader": "all_time_scoring_leader",
    "All-time AV Leader": "all_time_av_leader",
    "Winningest Coach (including playoffs)": "winningest_coach",
}


class TeamFranchiseParser:
    """Parses PFR team franchise pages into comprehensive data dicts."""

    def parse(self, html: str) -> Dict[str, Any]:
        """Parse a PFR team franchise page into a JSON-serializable dict.

        Args:
            html: Raw HTML string of a PFR team franchise page.

        Returns:
            A dict with keys: meta, team_index.
        """
        cleaned = re.sub(r"<!--(.*?)-->", r"\1", html, flags=re.DOTALL)
        soup = BeautifulSoup(cleaned, "html.parser")

        result: Dict[str, Any] = {}
        result["meta"] = self._parse_meta(soup)
        result["team_index"] = self._parse_team_index(soup)

        return result

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_meta(soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract franchise metadata from the ``#meta`` div."""
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

            # Check simple metadata labels.
            field_name = _META_LABEL_MAP.get(label)
            if field_name:
                value = full_text.replace(label, "", 1).strip().lstrip(":").strip()
                result[field_name] = value
                continue

            # Check leader labels (need name, href, stats).
            leader_field = _LEADER_LABELS.get(label)
            if leader_field:
                link = p_tag.find("a")
                if link:
                    player_name = link.get_text(strip=True)
                    player_href = link.get("href", "")
                    # Stats are everything after the player name in full text.
                    after_label = full_text.replace(label, "", 1).strip()
                    after_label = after_label.lstrip(":").strip()
                    stats_text = after_label.replace(player_name, "", 1).strip()
                    result[leader_field] = {
                        "name": player_name,
                        "href": player_href,
                        "stats": stats_text,
                    }
                continue

        return result

    # ------------------------------------------------------------------
    # Team Index table (year-by-year records)
    # ------------------------------------------------------------------

    def _parse_team_index(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse the ``team_index`` table of year-by-year season records."""
        table = soup.find("table", id="team_index")
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

            row_data: Dict[str, Any] = {}

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat")
                if not stat:
                    continue

                text = cell.get_text(strip=True)

                # Cast numeric columns.
                if stat in _INT_COLUMNS:
                    row_data[stat] = safe_int(text)
                elif stat in _FLOAT_COLUMNS:
                    try:
                        row_data[stat] = float(text) if text else None
                    except (ValueError, TypeError):
                        row_data[stat] = None
                else:
                    row_data[stat] = text

                # Extract links.
                if stat in _LINK_COLUMNS:
                    link = cell.find("a")
                    href_field = _LINK_COLUMNS[stat]
                    row_data[href_field] = (
                        link["href"] if link and link.get("href") else None
                    )

                # Extract title attributes and hrefs for player columns.
                if stat in _TITLE_COLUMNS:
                    link = cell.find("a")
                    if link:
                        row_data[f"{stat}_title"] = link.get("title", "")
                        row_data[f"{stat}_href"] = link.get("href", "")

            if row_data:
                records.append(row_data)

        return records
