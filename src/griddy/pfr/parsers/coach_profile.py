"""Coach profile page HTML parser for Pro Football Reference.

Parses PFR ``/coaches/{CoachId}.htm`` pages into structured dicts
containing coaching bio, results, ranks, history, and coaching tree.
"""

import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int

# Columns in coaching_results that should be cast to int.
_RESULTS_INT_COLUMNS = {
    "age",
    "g",
    "wins",
    "losses",
    "ties",
    "g_playoffs",
    "wins_playoffs",
    "losses_playoffs",
    "rank_team",
    "chall_num",
    "chall_won",
}

# Columns in coaching_results that should be cast to float.
_RESULTS_FLOAT_COLUMNS = {"srs_total", "srs_offense", "srs_defense"}

# Columns in coaching_results where we extract hrefs.
_RESULTS_LINK_COLUMNS = {
    "year_id": "year_href",
    "team": "team_href",
    "g": "g_href",
}

# Columns in coaching_results footer that should be cast to int.
_RESULTS_FOOTER_INT_COLUMNS = {
    "g",
    "wins",
    "losses",
    "ties",
    "g_playoffs",
    "wins_playoffs",
    "losses_playoffs",
    "chall_num",
    "chall_won",
}

# Columns in coaching_results footer that should be cast to float.
_RESULTS_FOOTER_FLOAT_COLUMNS = {"rank_avg"}

# All rank columns in coaching_ranks (all int).
_RANKS_INT_COLUMNS = {
    "teams_in_league",
    "rank_win_percentage",
    "rank_takeaway_giveaway",
    "rank_points_diff",
    "rank_yds_diff",
    "rank_off_yds",
    "rank_off_pts",
    "rank_off_turnovers",
    "rank_off_rush_att",
    "rank_off_rush_yds",
    "rank_off_rush_td",
    "rank_off_rush_yds_per_att",
    "rank_off_fumbles_lost",
    "rank_off_pass_att",
    "rank_off_pass_yds",
    "rank_off_pass_td",
    "rank_off_pass_int",
    "rank_off_pass_net_yds_per_att",
    "rank_def_yds",
    "rank_def_pts",
    "rank_def_turnovers",
    "rank_def_rush_att",
    "rank_def_rush_yds",
    "rank_def_rush_td",
    "rank_def_rush_yds_per_att",
    "rank_def_fumbles_rec",
    "rank_def_pass_att",
    "rank_def_pass_yds",
    "rank_def_pass_td",
    "rank_def_pass_int",
    "rank_def_pass_net_yds_per_att",
}

# Columns in coaching_history that should be cast to int.
_HISTORY_INT_COLUMNS = {"coach_age"}

# Columns in challenge_results that should be cast to int.
_CHALLENGE_INT_COLUMNS = {"down", "yds_to_go"}

# Meta label -> field name mapping for simple text fields.
_META_LABEL_MAP: Dict[str, str] = {
    "College": "college",
    "As Exec": "as_exec",
    "Relatives": "relatives",
}


class CoachProfileParser:
    """Parses PFR coach profile pages into comprehensive data dicts."""

    def parse(self, html: str) -> Dict[str, Any]:
        """Parse a PFR coach profile page into a JSON-serializable dict.

        Args:
            html: Raw HTML string of a PFR coach profile page.

        Returns:
            A dict with keys: bio, coaching_results, coaching_results_totals,
            coaching_ranks, coaching_history, challenge_results, worked_for,
            employed.
        """
        cleaned = re.sub(r"<!--(.*?)-->", r"\1", html, flags=re.DOTALL)
        soup = BeautifulSoup(cleaned, "html.parser")

        result: Dict[str, Any] = {}
        result["bio"] = self._parse_bio(soup)

        results, totals = self._parse_coaching_results(soup)
        result["coaching_results"] = results
        result["coaching_results_totals"] = totals

        result["coaching_ranks"] = self._parse_coaching_ranks(soup)
        result["coaching_history"] = self._parse_coaching_history(soup)
        result["challenge_results"] = self._parse_challenge_results(soup)
        result["worked_for"] = self._parse_coaching_tree_table(soup, "worked_for")
        result["employed"] = self._parse_coaching_tree_table(soup, "employed")

        return result

    # ------------------------------------------------------------------
    # Bio / Metadata
    # ------------------------------------------------------------------

    # Known metadata labels (used to distinguish from the full-name paragraph).
    _KNOWN_LABELS = frozenset(
        {
            "Born:",
            "College",
            "College Coaching",
            "High School",
            "As Exec",
            "Relatives",
        }
    )

    @classmethod
    def _clean(cls, text: str) -> str:
        """Normalize whitespace and non-breaking spaces in extracted text."""
        # Replace non-breaking spaces, then collapse internal whitespace.
        cleaned = text.replace("\xa0", " ").strip()
        return re.sub(r"\s+", " ", cleaned)

    @classmethod
    def _parse_bio(cls, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract coach bio from the ``#meta`` div."""
        meta_div = soup.find("div", id="meta")
        if meta_div is None:
            return {"name": ""}

        bio: Dict[str, Any] = {}

        # Display name from h1
        h1 = meta_div.find("h1")
        bio["name"] = cls._clean(h1.get_text()) if h1 else ""

        # Photo URL
        img = meta_div.find("img")
        bio["photo_url"] = img.get("src", "") if img else None

        for p_tag in meta_div.find_all("p"):
            strong = p_tag.find("strong")
            if not strong:
                continue

            label = strong.get_text(strip=True)
            full_text = cls._clean(p_tag.get_text())

            # Full name + nicknames: the first <p> whose <strong> label
            # does NOT match any known metadata label.
            if label and label not in cls._KNOWN_LABELS:
                raw = cls._clean(label)
                if "(" in raw:
                    name_part, nick_part = raw.split("(", 1)
                    bio["full_name"] = name_part.strip()
                    nick_part = nick_part.rstrip(")").strip()
                    bio["nicknames"] = [
                        n.strip()
                        for n in nick_part.replace(" or ", ",").split(",")
                        if n.strip()
                    ]
                else:
                    bio["full_name"] = raw
                    bio["nicknames"] = []
                continue

            # Born: the necro-birth span often has a malformed tag
            # (e.g. ``<span"``), so fall back to searching by
            # ``data-birth`` attribute across the raw HTML of the <p>.
            if label == "Born:":
                birth_span = p_tag.find(attrs={"data-birth": True})
                if birth_span:
                    bio["birth_date"] = birth_span["data-birth"]
                else:
                    # Fallback: extract from raw HTML with regex
                    p_html = str(p_tag)
                    m = re.search(r'data-birth="(\d{4}-\d{2}-\d{2})"', p_html)
                    if m:
                        bio["birth_date"] = m.group(1)

                if "in " in full_text:
                    location = full_text.split("in ", 1)[1]
                    if "(" in location:
                        location = location.split("(")[0]
                    location = location.strip()
                    if "," in location:
                        city, state = location.rsplit(",", 1)
                        bio["birth_city"] = city.strip()
                        bio["birth_state"] = state.strip()
                continue

            # College
            if label == "College":
                link = p_tag.find("a")
                if link:
                    bio["college"] = link.get_text(strip=True)
                    bio["college_href"] = link.get("href", "")
                continue

            # College Coaching
            if label == "College Coaching":
                link = p_tag.find("a")
                if link:
                    bio["college_coaching_href"] = link.get("href", "")
                continue

            # High School
            if label == "High School":
                schools = []
                for link in p_tag.find_all("a"):
                    href = link.get("href", "")
                    if "high_schools.cgi?id=" in href:
                        schools.append(link.get_text(strip=True))
                bio["high_schools"] = schools
                continue

            # As Exec
            if label == "As Exec":
                after = cls._clean(
                    full_text.replace(label, "", 1).strip().lstrip(":").strip()
                )
                bio["as_exec"] = after
                link = p_tag.find("a")
                if link:
                    bio["as_exec_href"] = link.get("href", "")
                continue

            # Relatives
            if label == "Relatives":
                after = cls._clean(
                    full_text.replace(label, "", 1).strip().lstrip(":").strip()
                )
                bio["relatives"] = after
                link = p_tag.find("a")
                if link:
                    bio["relatives_href"] = link.get("href", "")
                continue

        return bio

    # ------------------------------------------------------------------
    # Coaching Results table
    # ------------------------------------------------------------------

    def _parse_coaching_results(
        self, soup: BeautifulSoup
    ) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Parse the ``coaching_results`` table body and footer."""
        table = soup.find("table", id="coaching_results")
        if table is None:
            return [], []

        rows = self._parse_table_body(
            table,
            int_columns=_RESULTS_INT_COLUMNS,
            float_columns=_RESULTS_FLOAT_COLUMNS,
            link_columns=_RESULTS_LINK_COLUMNS,
        )

        totals = self._parse_coaching_results_footer(table)

        return rows, totals

    @staticmethod
    def _parse_coaching_results_footer(
        table: Tag,
    ) -> List[Dict[str, Any]]:
        """Parse the footer rows of the coaching_results table."""
        tfoot = table.find("tfoot")
        if tfoot is None:
            return []

        totals: List[Dict[str, Any]] = []

        for tr in tfoot.find_all("tr"):
            row_data: Dict[str, Any] = {}
            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat")
                if not stat:
                    continue
                text = cell.get_text(strip=True)

                # The year_id cell in the footer contains the label (e.g. "29 yrs")
                if stat == "year_id":
                    row_data["label"] = text
                elif stat in _RESULTS_FOOTER_INT_COLUMNS:
                    row_data[stat] = safe_int(text)
                elif stat in _RESULTS_FOOTER_FLOAT_COLUMNS:
                    try:
                        row_data[stat] = float(text) if text else None
                    except (ValueError, TypeError):
                        row_data[stat] = None
                elif stat == "team":
                    row_data[stat] = text if text else None
                else:
                    if text:
                        row_data[stat] = text

            if row_data:
                totals.append(row_data)

        return totals

    # ------------------------------------------------------------------
    # Coaching Ranks table
    # ------------------------------------------------------------------

    def _parse_coaching_ranks(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse the ``coaching_ranks`` table."""
        table = soup.find("table", id="coaching_ranks")
        if table is None:
            return []

        return self._parse_table_body(
            table,
            int_columns=_RANKS_INT_COLUMNS,
        )

    # ------------------------------------------------------------------
    # Coaching History table
    # ------------------------------------------------------------------

    def _parse_coaching_history(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse the ``coaching_history`` table."""
        table = soup.find("table", id="coaching_history")
        if table is None:
            return []

        return self._parse_table_body(
            table,
            int_columns=_HISTORY_INT_COLUMNS,
            link_columns={"coach_employer": "coach_employer_href"},
        )

    # ------------------------------------------------------------------
    # Challenge Results table
    # ------------------------------------------------------------------

    def _parse_challenge_results(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse the ``challenge_results`` table."""
        table = soup.find("table", id="challenge_results")
        if table is None:
            return []

        return self._parse_table_body(
            table,
            int_columns=_CHALLENGE_INT_COLUMNS,
            link_columns={"game_date": "game_date_href"},
        )

    # ------------------------------------------------------------------
    # Coaching Tree tables (worked_for, employed)
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_coaching_tree_table(
        soup: BeautifulSoup, table_id: str
    ) -> List[Dict[str, Any]]:
        """Parse a coaching tree table (``worked_for`` or ``employed``)."""
        table = soup.find("table", id=table_id)
        if table is None:
            return []

        tbody = table.find("tbody")
        if tbody is None:
            return []

        entries: List[Dict[str, Any]] = []

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
                row_data[stat] = text

                # Extract href for coach_name
                if stat == "coach_name":
                    link = cell.find("a")
                    if link:
                        row_data["coach_href"] = link.get("href", "")

            if row_data:
                entries.append(row_data)

        return entries

    # ------------------------------------------------------------------
    # Generic table body parser
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_table_body(
        table: Tag,
        *,
        int_columns: Optional[set] = None,
        float_columns: Optional[set] = None,
        link_columns: Optional[Dict[str, str]] = None,
    ) -> List[Dict[str, Any]]:
        """Parse a table's tbody rows with type casting and link extraction.

        Args:
            table: The BeautifulSoup ``<table>`` tag.
            int_columns: Column names to cast to int.
            float_columns: Column names to cast to float.
            link_columns: Mapping of column name -> href field name.
        """
        int_columns = int_columns or set()
        float_columns = float_columns or set()
        link_columns = link_columns or {}

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

                if stat in int_columns:
                    row_data[stat] = safe_int(text)
                elif stat in float_columns:
                    try:
                        row_data[stat] = float(text) if text else None
                    except (ValueError, TypeError):
                        row_data[stat] = None
                else:
                    row_data[stat] = text

                # Extract links.
                if stat in link_columns:
                    link = cell.find("a")
                    href_field = link_columns[stat]
                    row_data[href_field] = (
                        link["href"] if link and link.get("href") else None
                    )

            if row_data:
                records.append(row_data)

        return records
