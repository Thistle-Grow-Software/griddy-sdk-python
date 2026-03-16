"""Parser for NFL Draft Buzz prospect profile and stats pages.

Combines the logic from fbcm's BasicInfoParser, RatingExtractor,
SkillsParser, ScoutingReportParser, and StatsParser into a single
SDK-compatible parser that returns plain dicts for Pydantic validation.
"""

import logging
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from ..errors.parsing_error import ParsingError
from ._helpers import (
    get_tag_with_text,
    get_tag_with_title_containing,
    get_text_following_label,
    safe_float,
    safe_int,
)

logger = logging.getLogger(__name__)

# Maps raw positions (and sub-positions) to canonical position groups.
_POSITION_TO_GROUP: dict[str, str] = {
    "QB": "QB",
    "HB": "RB",
    "FB": "RB",
    "RB": "RB",
    "WR": "WR",
    "TE": "TE",
    "OT": "OL",
    "LT": "OL",
    "RT": "OL",
    "OG": "OL",
    "LG": "OL",
    "RG": "OL",
    "C": "OL",
    "DL": "DL",
    "DT": "DL",
    "NT": "DL",
    "NG": "DL",
    "EDGE": "EDGE",
    "LE": "EDGE",
    "RE": "EDGE",
    "DE": "EDGE",
    "LB": "LB",
    "LOLB": "LB",
    "ROLB": "LB",
    "OLB": "LB",
    "MLB": "LB",
    "ILB": "LB",
    "CB": "DB",
    "LCB": "DB",
    "RCB": "DB",
    "S": "DB",
    "FS": "DB",
    "SS": "DB",
    "DB": "DB",
}


class ProspectProfileParser:
    """Parses an NFL Draft Buzz prospect profile page into a dict.

    The returned dict matches the ``ProspectProfile`` Pydantic model schema.
    Stats are parsed from a separate stats page and merged in.
    """

    def parse_profile(self, html: str, *, position: str) -> Dict[str, Any]:
        """Parse the main prospect profile page.

        Args:
            html: Raw HTML of the prospect profile page.
            position: Canonical position group (e.g. ``"QB"``, ``"WR"``).

        Returns:
            A dict matching the ``ProspectProfile`` schema (without stats).
        """
        soup = BeautifulSoup(html, "html.parser")

        basic_info = self._parse_basic_info(soup)
        rtgs_table, comps_table = self._extract_ratings_comps_tables(soup)

        ratings = self._parse_ratings(soup, rtgs_table)
        skills = self._parse_skills(rtgs_table, position)
        comparisons = self._parse_comparisons(comps_table) if comps_table else None
        scouting_report = self._parse_scouting_report(soup)

        result: Dict[str, Any] = {
            "basic_info": basic_info,
            "ratings": ratings,
            "skills": skills,
            "scouting_report": scouting_report,
        }
        if comparisons is not None:
            result["comparisons"] = comparisons

        return result

    def parse_stats(
        self, html: str, *, position: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Parse the prospect stats page.

        Args:
            html: Raw HTML of the prospect stats page.
            position: Canonical position group.

        Returns:
            A list of stat dicts (one per season), or None if no stats found.
        """
        soup = BeautifulSoup(html, "html.parser")
        return self._parse_stats_page(soup, position)

    # ------------------------------------------------------------------
    # Basic Info
    # ------------------------------------------------------------------

    def _parse_basic_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract basic biographical information."""
        first_name_tag = soup.find("span", class_="player-info__first-name")
        last_name_tag = soup.find("span", class_="player-info__last-name")

        if not first_name_tag or not last_name_tag:
            raise ParsingError(
                "Could not find player name elements",
                selector="span.player-info__first-name / span.player-info__last-name",
            )

        first_name = first_name_tag.get_text(strip=True)
        last_name = last_name_tag.get_text(strip=True)

        info: Dict[str, Any] = {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
        }

        # Parse player-info-details div
        info_div = soup.find("div", class_="player-info-details")
        if info_div:
            for attr_div in info_div.find_all(
                "div", class_="player-info-details__item"
            ):
                field_tag = attr_div.find("h6", class_="player-info-details__title")
                value_tag = attr_div.find("div", class_="player-info-details__value")
                if field_tag and value_tag:
                    field = field_tag.get_text(strip=True).lower()
                    value = value_tag.get_text(strip=True).lower()
                    if field == "position":
                        value = self._normalize_position(value)
                    info[field] = value

        # Parse basicInfoTable
        basic_info_table = soup.find("table", class_="basicInfoTable")
        if basic_info_table:
            info.update(self._parse_basic_info_table(basic_info_table))

        # Remap field names to match model
        if "class" in info:
            info["class_"] = info.pop("class")
        if "home town" in info:
            info["hometown"] = info.pop("home town")

        # Extract image URL
        figure_tag = soup.find("figure", class_="player-info__photo")
        if figure_tag:
            img = figure_tag.find("img")
            if img and img.get("src"):
                src = img["src"]
                if src.startswith("/"):
                    info["photo_url"] = f"https://www.nfldraftbuzz.com{src}"
                else:
                    info["photo_url"] = src

        return info

    def _normalize_position(self, value: str) -> str:
        """Normalize a position string to its canonical group."""
        if "/" in value:
            parts = value.split("/")
            groups = [_POSITION_TO_GROUP.get(p.strip().upper()) for p in parts]
            valid = [g for g in groups if g]
            if valid:
                return "/".join(dict.fromkeys(valid))  # deduplicate preserving order
            return value
        return _POSITION_TO_GROUP.get(value.strip().upper(), value)

    def _parse_basic_info_table(self, tag: Tag) -> Dict[str, Any]:
        """Extract jersey, play style, draft year, forty time from the info table."""
        result: Dict[str, Any] = {}

        jersey_tag = get_tag_with_title_containing(tag, "#")
        if jersey_tag:
            result["jersey"] = jersey_tag.get_text(strip=True)

        sub_pos_label = get_tag_with_title_containing(tag, "Sub-Position")
        result["play_style"] = get_text_following_label(sub_pos_label) or ""

        updated_label = get_tag_with_title_containing(tag, "Last Updated")
        result["last_updated"] = get_text_following_label(updated_label) or ""

        draft_yr_label = get_tag_with_title_containing(tag, "Draft Year")
        result["draft_year"] = get_text_following_label(draft_yr_label) or ""

        forty_label = get_tag_with_title_containing(tag, "40 yard dash time")
        forty_val = get_text_following_label(forty_label) or ""
        if forty_val:
            result["forty"] = forty_val.split()[0]
        else:
            result["forty"] = ""

        return result

    # ------------------------------------------------------------------
    # Ratings & Rankings
    # ------------------------------------------------------------------

    def _extract_ratings_comps_tables(
        self, soup: BeautifulSoup
    ) -> tuple[Tag, Optional[Tag]]:
        """Find the ratings table and optional comparisons table."""
        tables = [
            table
            for table in soup.find_all("table", class_="starRatingTable")
            if not table.find("th", string=lambda s: s and "measurables" in s.lower())
        ]
        if not tables:
            raise ParsingError(
                "Could not find ratings table",
                selector="table.starRatingTable",
            )
        ratings = tables[0]
        comparisons = tables[1] if len(tables) > 1 else None
        return ratings, comparisons

    def _parse_ratings(self, soup: BeautifulSoup, table: Tag) -> Dict[str, Any]:
        """Extract ratings, rankings, and outlet grades."""
        rows = table.find_all("tr")

        # Find the row containing the overall rating span
        overall = None
        for row in rows:
            span = row.find("span")
            if span and "/ 100" in span.get_text():
                overall = safe_float(span.get_text(strip=True).replace(" / 100", ""))
                break

        # Find opposition rating from meter div
        opposition = None
        for row in rows:
            meter_div = row.find("div", class_="meter")
            if meter_div and meter_div.get("title"):
                opp_str = meter_div["title"].split(":")[-1].strip().replace("%", "")
                opposition = safe_int(opp_str)
                break

        # Draft projection & ranks
        proj_ranks = self._extract_proj_and_rankings(rows)

        # Average ranks from rankingBox
        avg_ranks = self._extract_average_ranks(soup)

        # Outlet ratings
        outlets = self._extract_outlet_ratings(table)

        return {
            "overall_rating": overall,
            "opposition_rating": opposition,
            **proj_ranks,
            **avg_ranks,
            **outlets,
        }

    def _extract_proj_and_rankings(self, rows: List[Tag]) -> Dict[str, Any]:
        """Extract draft projection, overall rank, and position rank."""
        result: Dict[str, Any] = {}
        proj_row = None
        for row in rows:
            if "draft projection" in row.get_text().lower():
                proj_row = row
                break

        if proj_row is None:
            return result

        proj_label = get_tag_with_text(proj_row, "span", "draft projection")
        result["draft_projection"] = get_text_following_label(proj_label)

        ovr_label = get_tag_with_text(proj_row, "span", "overall rank")
        ovr_text = get_text_following_label(ovr_label)
        result["overall_rank"] = safe_int(ovr_text) if ovr_text else None

        pos_label = get_tag_with_text(proj_row, "span", "position rank")
        result["position_rank"] = get_text_following_label(pos_label)

        return result

    def _extract_average_ranks(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract average overall and position ranks from the ranking box."""
        rankings_div = soup.find("div", class_="rankingBox")
        if not rankings_div:
            return {}
        rank_vals = rankings_div.find_all("div", class_="rankVal")
        if len(rank_vals) < 2:
            return {}
        return {
            "avg_overall_rank": safe_float(rank_vals[0].get_text(strip=True)),
            "avg_position_rank": safe_float(rank_vals[1].get_text(strip=True)),
        }

    def _extract_outlet_ratings(self, table: Tag) -> Dict[str, Optional[float]]:
        """Extract ESPN, Rivals, and 247 ratings."""
        return {
            "espn": self._extract_outlet_value(table, "espn"),
            "rivals": self._extract_outlet_value(table, "rivals"),
            "rtg_247": self._extract_outlet_value(table, "247 rating"),
        }

    def _extract_outlet_value(self, table: Tag, text: str) -> Optional[float]:
        """Extract a single outlet rating value."""
        tag = get_tag_with_text(table, "span", text)
        if not tag:
            return None
        raw = tag.get_text(strip=True)
        # Format is like "ESPN: 85 / 100" or "Rivals: 5.8"
        parts = raw.split(":")
        if len(parts) < 2:
            return None
        num_part = parts[-1].strip().split("/")[0].strip().split()[0]
        return safe_float(num_part)

    # ------------------------------------------------------------------
    # Skills
    # ------------------------------------------------------------------

    def _parse_skills(self, table: Tag, position: str) -> Optional[Dict[str, Any]]:
        """Extract position-specific skill ratings from the ratings table."""
        rows = table.find_all("tr")
        # Skill rows contain ":" (e.g., "Release Speed: 90") and appear
        # before the "draft projection" row.
        skill_rows: List[Tag] = []
        for row in rows:
            text = row.get_text().lower()
            if "draft projection" in text:
                break
            if (
                ":" in text
                and "overall rating" not in text
                and "opposition" not in text
            ):
                skill_rows.append(row)

        if not skill_rows:
            return None

        skills: Dict[str, Any] = {}
        for row in skill_rows:
            text = row.get_text(strip=True).lower().replace(" ", "_").replace("%", "")
            parts = text.split(":")
            if len(parts) != 2:
                continue
            skill_name = parts[0].replace("/", "_")
            rating_str = parts[1]
            if "/" in rating_str:
                rating_str = rating_str.split("/")[0]
            rating_str = rating_str.replace("_", "")
            rating = safe_float(rating_str)
            if rating is not None:
                skills[skill_name] = int(rating)

        return skills if skills else None

    # ------------------------------------------------------------------
    # Comparisons
    # ------------------------------------------------------------------

    def _parse_comparisons(self, table: Tag) -> List[Dict[str, Any]]:
        """Extract player comparisons from the comparisons table."""
        comparisons: List[Dict[str, Any]] = []
        tbody = table.find("tbody")
        if not tbody:
            return comparisons

        for row in tbody.find_all("tr"):
            text_parts = row.get_text().split()
            if len(text_parts) < 4:
                continue
            name = f"{text_parts[0]} {text_parts[1]}"
            school = text_parts[3]
            similarity_str = text_parts[-1].replace("%", "")
            similarity = safe_int(similarity_str)
            comparisons.append(
                {
                    "name": name,
                    "school": school,
                    "similarity": similarity,
                }
            )

        return comparisons

    # ------------------------------------------------------------------
    # Scouting Report
    # ------------------------------------------------------------------

    def _parse_scouting_report(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract scouting report (bio, strengths, weaknesses, summary)."""
        intro_div = soup.find("div", class_="playerDescIntro")
        if not intro_div:
            return {"bio": "", "strengths": [], "weaknesses": []}

        bio = intro_div.get_text(strip=True)

        strengths_div = soup.find("div", class_="playerDescPro")
        strengths: List[str] = []
        if strengths_div:
            strengths = [
                line
                for line in strengths_div.get_text().splitlines()
                if line.strip() and "scouting report" not in line.lower()
            ]

        weak_divs = soup.find_all("div", class_="playerDescNeg")
        weaknesses: List[str] = []
        summary: Optional[str] = None
        if weak_divs:
            weaknesses = [
                line
                for line in weak_divs[0].get_text().splitlines()
                if line.strip() and "scouting report" not in line.lower()
            ]
            if len(weak_divs) > 1:
                summary = weak_divs[1].get_text(strip=True)

        return {
            "bio": bio,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "summary": summary,
        }

    # ------------------------------------------------------------------
    # Stats (from separate stats page)
    # ------------------------------------------------------------------

    def _parse_stats_page(
        self, soup: BeautifulSoup, position: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Parse the stats page and return a list of season stat dicts."""
        table_div = None
        match position:
            case "QB":
                table_div = soup.find(id="QBstats")
            case "RB" | "WR" | "TE":
                table_div = soup.find(id="RB-Rush-stats")
            case "OL":
                pass
            case "DL" | "EDGE" | "LB" | "DB":
                table_div = soup.find(id="DBLBDL-stats")

        if table_div is None:
            return None

        gp_and_snaps = self._extract_games_and_snaps(soup)
        stats_table = table_div.find("table")
        if not stats_table or not stats_table.thead:
            return None

        header_values = [
            th.get_text(strip=True).lower()
            for th in stats_table.thead.find_all("th", class_="player-season-avg__stat")
            if th.get_text(strip=True)
        ]

        seasons: List[Dict[str, Any]] = []
        for row in stats_table.tbody.find_all("tr"):
            cells = [td.get_text(strip=True) for td in row.find_all("td")]
            stat_dict = self._build_stat_dict(
                position, header_values, cells, gp_and_snaps
            )
            if stat_dict:
                seasons.append(stat_dict)

        seasons.sort(key=lambda s: s.get("year", 0) or 0, reverse=True)
        return seasons if seasons else None

    def _extract_games_and_snaps(self, soup: BeautifulSoup) -> Dict[str, int]:
        """Extract games played and snap count from the stats page."""
        gp_label = get_tag_with_title_containing(soup, "College Games Played")
        gp_text = get_text_following_label(gp_label)
        games_played = safe_int(gp_text) or 0

        snaps_label = get_tag_with_title_containing(soup, "College Snap Count")
        snaps_text = get_text_following_label(snaps_label)
        snap_count = safe_int(snaps_text) or 0

        return {"games_played": games_played, "snap_count": snap_count}

    def _build_stat_dict(
        self,
        position: str,
        headers: List[str],
        cells: List[str],
        gp_and_snaps: Dict[str, int],
    ) -> Optional[Dict[str, Any]]:
        """Build a position-appropriate stat dict from a table row."""
        if not cells:
            return None

        if position == "QB":
            return self._build_passing_stats(headers, cells, gp_and_snaps)
        elif position in ("RB",):
            return self._build_rb_stats(cells, gp_and_snaps)
        elif position in ("WR", "TE"):
            return self._build_wr_te_stats(cells, gp_and_snaps)
        elif position in ("DL", "EDGE", "LB", "DB"):
            return self._build_defense_stats(cells, gp_and_snaps)
        return None

    def _build_passing_stats(
        self,
        headers: List[str],
        cells: List[str],
        gp_and_snaps: Dict[str, int],
    ) -> Dict[str, Any]:
        """Build QB passing stats dict."""
        raw = dict(zip(headers, cells))

        year_str = raw.get("year", "").split()[0] if raw.get("year") else ""

        return {
            "year": safe_int(year_str),
            "games_played": gp_and_snaps.get("games_played"),
            "snap_count": gp_and_snaps.get("snap_count"),
            "cmp": safe_int(raw.get("cmp", "")),
            "att": safe_int(raw.get("att", "")),
            "cmp_pct": safe_float(raw.get("cmp%", "")),
            "yds": safe_int(raw.get("yds", "")),
            "td": safe_int(raw.get("td", "")),
            "ints": safe_int(raw.get("int", "")),
            "sack": safe_int(raw.get("sack", "")),
            "qb_rtg": safe_float(raw.get("pro rat", "")),
        }

    def _build_rb_stats(
        self, cells: List[str], gp_and_snaps: Dict[str, int]
    ) -> Dict[str, Any]:
        """Build RB stats dict with rushing and receiving sub-dicts."""
        return {
            "year": safe_int(cells[0].split()[0] if cells[0] else ""),
            "games_played": gp_and_snaps.get("games_played"),
            "snap_count": gp_and_snaps.get("snap_count"),
            "rushing": {
                "att": safe_int(cells[1]) if len(cells) > 1 else None,
                "yds": safe_int(cells[2]) if len(cells) > 2 else None,
                "avg": safe_float(cells[3]) if len(cells) > 3 else None,
                "td": safe_int(cells[4]) if len(cells) > 4 else None,
            },
            "receiving": {
                "rec": safe_int(cells[5]) if len(cells) > 5 else None,
                "yds": safe_int(cells[6]) if len(cells) > 6 else None,
                "avg": safe_float(cells[7]) if len(cells) > 7 else None,
                "td": safe_int(cells[8]) if len(cells) > 8 else None,
            },
        }

    def _build_wr_te_stats(
        self, cells: List[str], gp_and_snaps: Dict[str, int]
    ) -> Dict[str, Any]:
        """Build WR/TE stats dict with receiving and rushing sub-dicts."""
        return {
            "year": safe_int(cells[0].split()[0] if cells[0] else ""),
            "games_played": gp_and_snaps.get("games_played"),
            "snap_count": gp_and_snaps.get("snap_count"),
            "receiving": {
                "rec": safe_int(cells[1]) if len(cells) > 1 else None,
                "yds": safe_int(cells[2]) if len(cells) > 2 else None,
                "avg": safe_float(cells[3]) if len(cells) > 3 else None,
                "td": safe_int(cells[4]) if len(cells) > 4 else None,
            },
            "rushing": {
                "att": safe_int(cells[5]) if len(cells) > 5 else None,
                "yds": safe_int(cells[6]) if len(cells) > 6 else None,
                "avg": safe_float(cells[7]) if len(cells) > 7 else None,
                "td": safe_int(cells[8]) if len(cells) > 8 else None,
            },
        }

    def _build_defense_stats(
        self, cells: List[str], gp_and_snaps: Dict[str, int]
    ) -> Dict[str, Any]:
        """Build defensive stats dict with tackle and interception sub-dicts."""
        return {
            "year": safe_int(cells[0].split()[0] if cells[0] else ""),
            "games_played": gp_and_snaps.get("games_played"),
            "snap_count": gp_and_snaps.get("snap_count"),
            "tackle": {
                "total": safe_int(cells[1]) if len(cells) > 1 else None,
                "solo": safe_int(cells[2]) if len(cells) > 2 else None,
                "ff": safe_int(cells[3]) if len(cells) > 3 else None,
                "sacks": safe_float(cells[4]) if len(cells) > 4 else None,
            },
            "interception": {
                "ints": safe_int(cells[5]) if len(cells) > 5 else None,
                "yds": safe_int(cells[6]) if len(cells) > 6 else None,
                "td": safe_int(cells[7]) if len(cells) > 7 else None,
                "pds": safe_int(cells[8]) if len(cells) > 8 else None,
            },
        }
