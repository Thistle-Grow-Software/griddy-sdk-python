"""Parser for NFL Draft Buzz prospect profile and stats pages.

Combines the logic from fbcm's BasicInfoParser, RatingExtractor,
SkillsParser, ScoutingReportParser, and StatsParser into a single
SDK-compatible parser that returns plain dicts for Pydantic validation.
"""

import logging
from typing import Any, Optional

from bs4 import BeautifulSoup, Tag

from ..constants import POSITION_TO_GROUP_MAP
from ..errors.parsing_error import ParsingError
from ._helpers import (
    get_tag_with_text,
    get_tag_with_title_containing,
    get_text_following_label,
    safe_float,
    safe_int,
)

logger = logging.getLogger(__name__)


class ProspectProfileParser:
    """Parses an NFL Draft Buzz prospect profile page into a dict.

    The returned dict matches the ``ProspectProfile`` Pydantic model schema.
    Stats are parsed from a separate stats page and merged in.
    """

    def parse_profile(self, html: str, *, position: str) -> dict[str, Any]:
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

        result: dict[str, Any] = {
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
    ) -> Optional[list[dict[str, Any]]]:
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

    def _parse_basic_info(self, soup: BeautifulSoup) -> dict[str, Any]:
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

        info: dict[str, Any] = {
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
            groups = [POSITION_TO_GROUP_MAP.get(p.strip().upper()) for p in parts]
            valid = [g for g in groups if g]
            if valid:
                return "/".join(dict.fromkeys(valid))
            return value
        return POSITION_TO_GROUP_MAP.get(value.strip().upper(), value)

    def _parse_basic_info_table(self, tag: Tag) -> dict[str, Any]:
        """Extract jersey, play style, draft year, forty time from the info table."""
        result: dict[str, Any] = {}

        jersey_tag = get_tag_with_title_containing(tag, "#")
        if jersey_tag:
            result["jersey"] = jersey_tag.get_text(strip=True)

        sub_pos_label = get_tag_with_title_containing(tag, "Sub-Position")
        result["play_style"] = get_text_following_label(sub_pos_label)

        updated_label = get_tag_with_title_containing(tag, "Last Updated")
        result["last_updated"] = get_text_following_label(updated_label)

        draft_yr_label = get_tag_with_title_containing(tag, "Draft Year")
        result["draft_year"] = get_text_following_label(draft_yr_label)

        forty_label = get_tag_with_title_containing(tag, "40 yard dash time")
        forty_val = get_text_following_label(forty_label) or ""
        if forty_val:
            result["forty"] = forty_val.split()[0]

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

    def _parse_ratings(self, soup: BeautifulSoup, table: Tag) -> dict[str, Any]:
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

        proj_ranks = self._extract_proj_and_rankings(rows)
        avg_ranks = self._extract_average_ranks(soup)
        outlets = self._extract_outlet_ratings(table)

        return {
            "overall_rating": overall,
            "opposition_rating": opposition,
            **proj_ranks,
            **avg_ranks,
            **outlets,
        }

    def _extract_proj_and_rankings(self, rows: list[Tag]) -> dict[str, Any]:
        """Extract draft projection, overall rank, and position rank."""
        result: dict[str, Any] = {}
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

    def _extract_average_ranks(self, soup: BeautifulSoup) -> dict[str, Any]:
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

    def _extract_outlet_ratings(self, table: Tag) -> dict[str, Optional[float]]:
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
        parts = raw.split(":")
        if len(parts) < 2:
            return None
        num_part = parts[-1].strip().split("/")[0].strip().split()[0]
        return safe_float(num_part)

    # ------------------------------------------------------------------
    # Skills
    # ------------------------------------------------------------------

    def _parse_skills(self, table: Tag, position: str) -> Optional[dict[str, Any]]:
        """Extract position-specific skill ratings from the ratings table."""
        rows = table.find_all("tr")
        skill_rows: list[Tag] = []
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

        skills: dict[str, Any] = {}
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

    def _parse_comparisons(self, table: Tag) -> list[dict[str, Any]]:
        """Extract player comparisons from the comparisons table."""
        comparisons: list[dict[str, Any]] = []
        tbody = table.find("tbody")
        if not tbody:
            return comparisons

        for row in tbody.find_all("tr"):
            text_parts = row.get_text().split()
            if len(text_parts) < 4:
                continue
            comparisons.append(
                {
                    "name": f"{text_parts[0]} {text_parts[1]}",
                    "school": text_parts[3],
                    "similarity": safe_int(text_parts[-1].replace("%", "")),
                }
            )

        return comparisons

    # ------------------------------------------------------------------
    # Scouting Report
    # ------------------------------------------------------------------

    def _parse_scouting_report(self, soup: BeautifulSoup) -> dict[str, Any]:
        """Extract scouting report (bio, strengths, weaknesses, summary)."""
        intro_div = soup.find("div", class_="playerDescIntro")
        if not intro_div:
            return {}

        bio = intro_div.get_text(strip=True)

        strengths_div = soup.find("div", class_="playerDescPro")
        strengths = self._extract_report_lines(strengths_div) if strengths_div else []

        weak_divs = soup.find_all("div", class_="playerDescNeg")
        weaknesses = self._extract_report_lines(weak_divs[0]) if weak_divs else []
        summary = weak_divs[1].get_text(strip=True) if len(weak_divs) > 1 else None

        return {
            "bio": bio,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "summary": summary,
        }

    @staticmethod
    def _extract_report_lines(div: Tag) -> list[str]:
        """Extract non-header text lines from a scouting report section."""
        return [
            line
            for line in div.get_text().splitlines()
            if line.strip() and "scouting report" not in line.lower()
        ]

    # ------------------------------------------------------------------
    # Stats (from separate stats page)
    # ------------------------------------------------------------------

    def _parse_stats_page(
        self, soup: BeautifulSoup, position: str
    ) -> Optional[list[dict[str, Any]]]:
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

        seasons: list[dict[str, Any]] = []
        for row in stats_table.tbody.find_all("tr"):
            cells = [td.get_text(strip=True) for td in row.find_all("td")]
            stat_dict = self._build_stat_dict(
                position, header_values, cells, gp_and_snaps
            )
            if stat_dict:
                seasons.append(stat_dict)

        seasons.sort(key=lambda s: s.get("year", 0) or 0, reverse=True)
        return seasons if seasons else None

    def _extract_games_and_snaps(self, soup: BeautifulSoup) -> dict[str, int]:
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
        headers: list[str],
        cells: list[str],
        gp_and_snaps: dict[str, int],
    ) -> Optional[dict[str, Any]]:
        """Build a position-appropriate stat dict from a table row."""
        if not cells:
            return None

        if position == "QB":
            return self._build_passing_stats(headers, cells, gp_and_snaps)
        elif position in ("RB", "WR", "TE"):
            return self._build_skill_player_stats(position, cells, gp_and_snaps)
        elif position in ("DL", "EDGE", "LB", "DB"):
            return self._build_defense_stats(cells, gp_and_snaps)
        return None

    def _build_passing_stats(
        self,
        headers: list[str],
        cells: list[str],
        gp_and_snaps: dict[str, int],
    ) -> dict[str, Any]:
        """Build QB passing stats dict."""
        raw = dict(zip(headers, cells))
        year_str = raw.get("year", "").split()[0] if raw.get("year") else ""

        return {
            "year": safe_int(year_str),
            **gp_and_snaps,
            "cmp": safe_int(raw.get("cmp", "")),
            "att": safe_int(raw.get("att", "")),
            "cmp_pct": safe_float(raw.get("cmp%", "")),
            "yds": safe_int(raw.get("yds", "")),
            "td": safe_int(raw.get("td", "")),
            "ints": safe_int(raw.get("int", "")),
            "sack": safe_int(raw.get("sack", "")),
            "qb_rtg": safe_float(raw.get("pro rat", "")),
        }

    def _build_skill_player_stats(
        self, position: str, cells: list[str], gp_and_snaps: dict[str, int]
    ) -> dict[str, Any]:
        """Build RB/WR/TE stats with rushing and receiving sub-dicts."""
        rushing = self._extract_sub_stats(cells, start=1)
        receiving = self._extract_sub_stats(cells, start=5, include_rec=True)

        # RBs lead with rushing; WR/TE lead with receiving
        if position == "RB":
            primary, secondary = "rushing", "receiving"
        else:
            primary, secondary = "receiving", "rushing"
            rushing, receiving = receiving, rushing

        return {
            "year": safe_int(cells[0].split()[0] if cells[0] else ""),
            **gp_and_snaps,
            primary: rushing,
            secondary: receiving,
        }

    def _extract_sub_stats(
        self, cells: list[str], *, start: int, include_rec: bool = False
    ) -> dict[str, Any]:
        """Extract a 4-field rushing/receiving sub-dict from table cells."""

        def _cell(offset: int) -> Optional[str]:
            idx = start + offset
            return cells[idx] if idx < len(cells) else None

        if include_rec:
            return {
                "rec": safe_int(_cell(0)),
                "yds": safe_int(_cell(1)),
                "avg": safe_float(_cell(2)),
                "td": safe_int(_cell(3)),
            }
        return {
            "att": safe_int(_cell(0)),
            "yds": safe_int(_cell(1)),
            "avg": safe_float(_cell(2)),
            "td": safe_int(_cell(3)),
        }

    def _build_defense_stats(
        self, cells: list[str], gp_and_snaps: dict[str, int]
    ) -> dict[str, Any]:
        """Build defensive stats dict with tackle and interception sub-dicts."""

        def _cell(idx: int) -> Optional[str]:
            return cells[idx] if idx < len(cells) else None

        return {
            "year": safe_int(cells[0].split()[0] if cells[0] else ""),
            **gp_and_snaps,
            "tackle": {
                "total": safe_int(_cell(1)),
                "solo": safe_int(_cell(2)),
                "ff": safe_int(_cell(3)),
                "sacks": safe_float(_cell(4)),
            },
            "interception": {
                "ints": safe_int(_cell(5)),
                "yds": safe_int(_cell(6)),
                "td": safe_int(_cell(7)),
                "pds": safe_int(_cell(8)),
            },
        }
