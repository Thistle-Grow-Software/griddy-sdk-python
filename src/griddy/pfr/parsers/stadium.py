"""Stadium page HTML parser for Pro Football Reference.

Parses PFR ``/stadiums/{StadiumId}.htm`` pages into structured dicts
containing stadium bio, career leaders, best games, and notable game summaries.
"""

import re
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int


class StadiumParser:
    """Parses PFR stadium pages into comprehensive data dicts."""

    def parse(self, html: str) -> Dict[str, Any]:
        """Parse a PFR stadium page into a JSON-serializable dict.

        Args:
            html: Raw HTML string of a PFR stadium page.

        Returns:
            A dict with keys: bio, leaders, best_games, best_playoff_games,
            game_summaries.
        """
        cleaned = re.sub(r"<!--(.*?)-->", r"\1", html, flags=re.DOTALL)
        soup = BeautifulSoup(cleaned, "html.parser")

        result: Dict[str, Any] = {}
        result["bio"] = self._parse_bio(soup)
        result["leaders"] = self._parse_record_table(soup, "leaders")
        result["best_games"] = self._parse_best_games_table(soup, "games")
        result["best_playoff_games"] = self._parse_best_games_table(
            soup, "playoff_games"
        )
        result["game_summaries"] = self._parse_game_summaries(soup)

        return result

    # ------------------------------------------------------------------
    # Bio / Metadata
    # ------------------------------------------------------------------

    @staticmethod
    def _clean(text: str) -> str:
        """Normalize whitespace and non-breaking spaces in extracted text."""
        cleaned = text.replace("\xa0", " ").strip()
        return re.sub(r"\s+", " ", cleaned)

    @classmethod
    def _parse_bio(cls, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract stadium bio from the ``#meta`` div."""
        meta_div = soup.find("div", id="meta")
        if meta_div is None:
            return {"name": "", "teams": []}

        bio: Dict[str, Any] = {}

        # Stadium name from h1 (strip " History" suffix)
        h1 = meta_div.find("h1")
        if h1:
            name = cls._clean(h1.get_text())
            if name.endswith(" History"):
                name = name[: -len(" History")]
            bio["name"] = name
        else:
            bio["name"] = ""

        # Parse paragraphs for address, years active, surfaces
        paragraphs = meta_div.find_all("p")
        for idx, p_tag in enumerate(paragraphs):
            bold = p_tag.find("b")
            if bold is None:
                # First paragraph without bold is the address
                text = cls._clean(p_tag.get_text())
                if text and "address" not in bio:
                    bio["address"] = text
                continue

            label = bold.get_text(strip=True).rstrip(":")

            if label == "Years Active":
                full_text = cls._clean(p_tag.get_text())
                # Strip "Years Active:" prefix
                val = full_text.replace("Years Active:", "", 1).strip()
                # Extract total games from parenthetical "(N games)"
                games_match = re.search(r"\((\d+)\s+games?\)", val)
                if games_match:
                    bio["total_games"] = int(games_match.group(1))
                    # Years active is the part before the parenthetical
                    bio["years_active"] = val[: games_match.start()].strip()
                else:
                    bio["years_active"] = val

            elif label == "Surfaces":
                full_text = cls._clean(p_tag.get_text())
                val = full_text.replace("Surfaces:", "", 1).strip()
                if val:
                    bio["surfaces"] = val

        # Parse teams list
        bio["teams"] = cls._parse_teams(meta_div)

        return bio

    @classmethod
    def _parse_teams(cls, meta_div: Tag) -> List[Dict[str, Any]]:
        """Parse the teams list from the ``<ul>`` in ``#meta``."""
        ul = meta_div.find("ul")
        if ul is None:
            return []

        items = ul.find_all("li")
        teams: List[Dict[str, Any]] = []

        # Teams appear in groups of 3 LI elements
        idx = 0
        while idx < len(items):
            team: Dict[str, Any] = {}

            # First LI: team name + years
            li_team = items[idx]
            a = li_team.find("a")
            if a:
                team["name"] = a.get_text(strip=True)
                team["team_href"] = a.get("href")
            else:
                team["name"] = cls._clean(li_team.get_text())

            # Extract years from parenthetical
            text = cls._clean(li_team.get_text())
            years_match = re.search(r"\((\d{4}-\d{4})\)", text)
            if years_match:
                team["years"] = years_match.group(1)

            idx += 1

            # Second LI: Regular Season record
            if idx < len(items):
                li_reg = items[idx]
                reg_text = cls._clean(li_reg.get_text())
                if "Regular Season" in reg_text:
                    a = li_reg.find("a")
                    if a:
                        team["regular_season_record"] = a.get_text(strip=True)
                        team["regular_season_href"] = a.get("href")
                    idx += 1

            # Third LI: Playoff record
            if idx < len(items):
                li_play = items[idx]
                play_text = cls._clean(li_play.get_text())
                if "Playoffs" in play_text:
                    a = li_play.find("a")
                    if a:
                        team["playoff_record"] = a.get_text(strip=True)
                        team["playoff_href"] = a.get("href")
                    idx += 1

            teams.append(team)

        return teams

    # ------------------------------------------------------------------
    # Leaders table (career leaders)
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_record_table(soup: BeautifulSoup, table_id: str) -> List[Dict[str, Any]]:
        """Parse a leaders-style table with player, g, stats columns."""
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
                if not stat or stat == "pi":
                    continue

                if stat == "player":
                    row["player"] = cell.get_text(strip=True)
                    row["player_id"] = cell.get("data-append-csv")
                    a = cell.find("a")
                    if a and a.get("href"):
                        row["player_href"] = a["href"]
                elif stat == "g":
                    row["g"] = safe_int(cell.get_text(strip=True))
                else:
                    row[stat] = cell.get_text(strip=True)

            if row:
                records.append(row)

        return records

    # ------------------------------------------------------------------
    # Best games / Best playoff games tables
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_best_games_table(
        soup: BeautifulSoup, table_id: str
    ) -> List[Dict[str, Any]]:
        """Parse a best-games-style table with player, team, stats,
        boxscore columns."""
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
                if not stat or stat == "pi":
                    continue

                text = cell.get_text(strip=True)
                a = cell.find("a")

                if stat == "player":
                    row["player"] = text
                    row["player_id"] = cell.get("data-append-csv")
                    if a and a.get("href"):
                        row["player_href"] = a["href"]
                elif stat == "team":
                    row["team"] = text
                    if a and a.get("href"):
                        row["team_href"] = a["href"]
                elif stat == "boxscore_word":
                    row["boxscore_word"] = text
                    if a and a.get("href"):
                        row["boxscore_href"] = a["href"]
                else:
                    row[stat] = text

            if row:
                records.append(row)

        return records

    # ------------------------------------------------------------------
    # Game summaries (notable games section)
    # ------------------------------------------------------------------

    @classmethod
    def _parse_game_summaries(cls, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse all game_summaries sections with notable games."""
        summaries: List[Dict[str, Any]] = []

        for summaries_div in soup.find_all("div", class_="game_summaries"):
            for gs in summaries_div.find_all("div", class_="game_summary"):
                summary = cls._parse_single_game_summary(gs)
                if summary:
                    summaries.append(summary)

        return summaries

    @classmethod
    def _parse_single_game_summary(cls, gs: Tag) -> Optional[Dict[str, Any]]:
        """Parse a single game_summary div."""
        summary: Dict[str, Any] = {}

        # Teams table
        teams_table = gs.find("table", class_="teams")
        if teams_table is None:
            return None

        team_rows: List[Tag] = []

        for tr in teams_table.find_all("tr"):
            tr_classes = tr.get("class") or []
            if "date" in tr_classes:
                # Extract label and date
                td = tr.find("td")
                if td:
                    br = td.find("br")
                    if br:
                        label_parts: List[str] = []
                        date_parts: List[str] = []
                        found_br = False
                        for child in td.children:
                            if child == br:
                                found_br = True
                                continue
                            text = (
                                child.get_text(strip=True)
                                if hasattr(child, "get_text")
                                else str(child).strip()
                            )
                            if text:
                                if found_br:
                                    date_parts.append(text)
                                else:
                                    label_parts.append(text)
                        label = " ".join(label_parts)
                        date = " ".join(date_parts)
                        if label:
                            summary["label"] = label
                        if date:
                            summary["date"] = date
            else:
                team_rows.append(tr)

        # Parse team rows (first = team_1, second = team_2)
        for i, tr in enumerate(team_rows[:2]):
            prefix = f"team_{i + 1}"
            a = tr.find("a")
            if a:
                summary[f"{prefix}"] = a.get_text(strip=True)
                if a.get("href"):
                    summary[f"{prefix}_href"] = a["href"]

            # Score is in the second td (class="right", not "gamelink")
            tds = tr.find_all("td")
            for td in tds:
                td_classes = td.get("class") or []
                if "right" in td_classes and "gamelink" not in td_classes:
                    score = safe_int(td.get_text(strip=True))
                    if score is not None:
                        summary[f"{prefix}_score"] = score
                    break

            # Boxscore href from gamelink td (only on first team row)
            gl_td = tr.find("td", class_="gamelink")
            if gl_td:
                gl_a = gl_td.find("a")
                if gl_a and gl_a.get("href"):
                    summary["boxscore_href"] = gl_a["href"]

        # Stats table (game leaders)
        leaders: List[Dict[str, Any]] = []
        stats_table = gs.find("table", class_="stats")
        if stats_table:
            for tr in stats_table.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) >= 3:
                    leader: Dict[str, Any] = {}
                    leader["stat_name"] = tds[0].get_text(strip=True)
                    leader["player"] = tds[1].get_text(strip=True)
                    a = tds[1].find("a")
                    if a and a.get("href"):
                        leader["player_href"] = a["href"]
                    leader["value"] = tds[2].get_text(strip=True)
                    leaders.append(leader)

        summary["leaders"] = leaders

        return summary
