"""Parser for PFR Fantasy Rankings pages.

Handles:
- ``/years/{year}/fantasy.htm`` — Top Fantasy Players (table ``#fantasy``)
- ``/fantasy/{position}-fantasy-matchups.htm`` — Fantasy Matchups
  (table ``#fantasy_stats``)
- ``/years/{year}/fantasy-points-against-{position}.htm`` — Fantasy Points
  Allowed (table ``#fantasy_def``)
- ``/years/{year}/redzone-passing.htm`` — Red Zone Passing
  (table ``#fantasy_rz``)
- ``/years/{year}/redzone-receiving.htm`` — Red Zone Receiving
  (table ``#fantasy_rz``)
- ``/years/{year}/redzone-rushing.htm`` — Red Zone Rushing
  (table ``#fantasy_rz``)
"""

from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int, safe_numeric, safe_pct


class FantasyParser:
    """Parses PFR Fantasy Rankings pages into structured data dicts."""

    # ── Top Players (/years/{year}/fantasy.htm) ──────────────────────

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

    # ── Matchups (/fantasy/{position}-fantasy-matchups.htm) ──────────

    # Int columns for the matchups table.
    _MATCHUP_INT_COLUMNS = frozenset(
        {
            "g",
            "gs",
            "fantasy_points_proj_rank",
            "draftkings_points_proj_rank",
            "fanduel_points_proj_rank",
        }
    )

    # Float columns for the matchups table (per-game averages).
    _MATCHUP_FLOAT_COLUMNS = frozenset(
        {
            # Passing (QB only)
            "pass_cmp",
            "pass_att",
            "pass_yds",
            "pass_td",
            "pass_int",
            "pass_sacked",
            # Rushing (QB / RB)
            "rush_att",
            "rush_yds",
            "rush_td",
            # Receiving (WR / RB / TE)
            "targets",
            "rec",
            "rec_yds",
            "rec_td",
            # Fantasy per game
            "fantasy_points_per_game",
            "draftkings_points_per_game",
            "fanduel_points_per_game",
            # Opponent fantasy allowed per game
            "opp_fantasy_points_per_game",
            "opp_draftkings_points_per_game",
            "opp_fanduel_points_per_game",
        }
    )

    def parse_matchups(self, html: str) -> Dict[str, Any]:
        """Parse a fantasy matchups page.

        Works for any position (QB, WR, RB, TE) since the parser reads
        whichever ``data-stat`` columns are present in the table.

        Returns:
            A dict with key ``players``.
        """
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="fantasy_stats")
        if table is None:
            return {"players": []}

        players = self._parse_matchup_rows(table)
        return {"players": players}

    def _parse_matchup_rows(self, table: Tag) -> List[Dict[str, Any]]:
        """Extract player rows from the fantasy_stats matchup table."""
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

                if stat == "player":
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
                elif stat == "opp":
                    row["opp"] = text or None
                    if link:
                        row["opp_href"] = link.get("href")
                elif stat == "injury":
                    row["injury"] = text or None
                elif stat == "snaps":
                    row["snaps"] = text or None
                elif stat == "at_or_vs":
                    row["at_or_vs"] = text or None
                elif stat == "ranker":
                    row["rank"] = safe_int(text)
                elif stat in self._MATCHUP_INT_COLUMNS:
                    row[stat] = safe_int(text)
                elif stat in self._MATCHUP_FLOAT_COLUMNS:
                    row[stat] = safe_numeric(text)

            if not all_empty:
                players.append(row)

        return players

    # ── Points Allowed (/years/{year}/fantasy-points-against-{pos}.htm) ──

    # Int columns for the fantasy_def table (season totals).
    _POINTS_ALLOWED_INT_COLUMNS = frozenset(
        {
            "g",
            # Passing (QB only)
            "pass_cmp",
            "pass_att",
            "pass_yds",
            "pass_td",
            "pass_int",
            "two_pt_pass",
            "pass_sacked",
            # Rushing (QB / RB)
            "rush_att",
            "rush_yds",
            "rush_td",
            # Receiving (WR / RB / TE)
            "targets",
            "rec",
            "rec_yds",
            "rec_td",
            # Scoring (WR / RB / TE)
            "two_pt_md",
            # Fumbles (WR / RB / TE)
            "fumbles_lost",
        }
    )

    # Float columns for the fantasy_def table.
    _POINTS_ALLOWED_FLOAT_COLUMNS = frozenset(
        {
            "fantasy_points",
            "draftkings_points",
            "fanduel_points",
            "fantasy_points_per_game",
            "draftkings_points_per_game",
            "fanduel_points_per_game",
        }
    )

    def parse_points_allowed(self, html: str) -> Dict[str, Any]:
        """Parse a fantasy points allowed page.

        Works for any position (QB, WR, RB, TE) since the parser reads
        whichever ``data-stat`` columns are present in the table.

        Returns:
            A dict with key ``teams``.
        """
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="fantasy_def")
        if table is None:
            return {"teams": []}

        teams = self._parse_points_allowed_rows(table)
        return {"teams": teams}

    def _parse_points_allowed_rows(self, table: Tag) -> List[Dict[str, Any]]:
        """Extract team rows from the fantasy_def table."""
        tbody = table.find("tbody")
        if tbody is None:
            return []

        teams: List[Dict[str, Any]] = []

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

                if stat == "team":
                    row["team"] = text or None
                    if link:
                        row["team_href"] = link.get("href")
                elif stat in self._POINTS_ALLOWED_INT_COLUMNS:
                    row[stat] = safe_int(text)
                elif stat in self._POINTS_ALLOWED_FLOAT_COLUMNS:
                    row[stat] = safe_numeric(text)

            if not all_empty:
                teams.append(row)

        return teams

    # ── Red Zone Passing (/years/{year}/redzone-passing.htm) ───────────

    # Int columns for the red zone passing table.
    _RZ_PASSING_INT_COLUMNS = frozenset(
        {
            "pass_cmp",
            "pass_att",
            "pass_yds",
            "pass_td",
            "pass_int",
            "pass_cmp_in_10",
            "pass_att_in_10",
            "pass_yds_in_10",
            "pass_td_in_10",
            "pass_int_in_10",
        }
    )

    # Float columns for the red zone passing table (completion pct).
    _RZ_PASSING_FLOAT_COLUMNS = frozenset(
        {
            "pass_cmp_perc",
            "pass_cmp_perc_in_10",
        }
    )

    def parse_redzone_passing(self, html: str) -> Dict[str, Any]:
        """Parse the red zone passing page.

        Returns:
            A dict with key ``players``.
        """
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="fantasy_rz")
        if table is None:
            return {"players": []}

        players = self._parse_rz_passing_rows(table)
        return {"players": players}

    def _parse_rz_passing_rows(self, table: Tag) -> List[Dict[str, Any]]:
        """Extract player rows from the red zone passing table."""
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

                if stat == "player":
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
                elif stat == "link":
                    if link:
                        row["link_href"] = link.get("href")
                elif stat in self._RZ_PASSING_INT_COLUMNS:
                    row[stat] = safe_int(text)
                elif stat in self._RZ_PASSING_FLOAT_COLUMNS:
                    row[stat] = safe_numeric(text)

            if not all_empty:
                players.append(row)

        return players

    # ── Red Zone Receiving (/years/{year}/redzone-receiving.htm) ───────

    # Int columns for the red zone receiving table.
    _RZ_RECEIVING_INT_COLUMNS = frozenset(
        {
            "targets",
            "rec",
            "rec_yds",
            "rec_td",
            "targets_in_10",
            "rec_in_10",
            "rec_yds_in_10",
            "rec_td_in_10",
        }
    )

    # Percentage columns for the red zone receiving table (include % sign).
    _RZ_RECEIVING_PCT_COLUMNS = frozenset(
        {
            "catch_pct",
            "targets_pct",
            "catch_pct_in_10",
            "targets_in_10_pct",
        }
    )

    def parse_redzone_receiving(self, html: str) -> Dict[str, Any]:
        """Parse the red zone receiving page.

        Returns:
            A dict with key ``players``.
        """
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="fantasy_rz")
        if table is None:
            return {"players": []}

        players = self._parse_rz_receiving_rows(table)
        return {"players": players}

    def _parse_rz_receiving_rows(self, table: Tag) -> List[Dict[str, Any]]:
        """Extract player rows from the red zone receiving table."""
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

                if stat == "player":
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
                elif stat == "link":
                    if link:
                        row["link_href"] = link.get("href")
                elif stat in self._RZ_RECEIVING_INT_COLUMNS:
                    row[stat] = safe_int(text)
                elif stat in self._RZ_RECEIVING_PCT_COLUMNS:
                    row[stat] = safe_pct(text)

            if not all_empty:
                players.append(row)

        return players

    # ── Red Zone Rushing (/years/{year}/redzone-rushing.htm) ──────────

    # Int columns for the red zone rushing table.
    _RZ_RUSHING_INT_COLUMNS = frozenset(
        {
            "rush_att",
            "rush_yds",
            "rush_td",
            "rush_att_in_10",
            "rush_yds_in_10",
            "rush_td_in_10",
            "rush_att_in_5",
            "rush_yds_in_5",
            "rush_td_in_5",
        }
    )

    # Percentage columns for the red zone rushing table (include % sign).
    _RZ_RUSHING_PCT_COLUMNS = frozenset(
        {
            "rush_att_pct",
            "rush_att_in_10_pct",
            "rush_att_in_5_pct",
        }
    )

    def parse_redzone_rushing(self, html: str) -> Dict[str, Any]:
        """Parse the red zone rushing page.

        Returns:
            A dict with key ``players``.
        """
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="fantasy_rz")
        if table is None:
            return {"players": []}

        players = self._parse_rz_rushing_rows(table)
        return {"players": players}

    def _parse_rz_rushing_rows(self, table: Tag) -> List[Dict[str, Any]]:
        """Extract player rows from the red zone rushing table."""
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

                if stat == "player":
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
                elif stat == "link":
                    if link:
                        row["link_href"] = link.get("href")
                elif stat in self._RZ_RUSHING_INT_COLUMNS:
                    row[stat] = safe_int(text)
                elif stat in self._RZ_RUSHING_PCT_COLUMNS:
                    row[stat] = safe_pct(text)

            if not all_empty:
                players.append(row)

        return players
