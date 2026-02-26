"""Parser for PFR Executive profile pages.

Handles ``/executives/{ExecutiveId}.htm`` — bio, team results, and totals.
"""

from typing import Any, Dict, List

from bs4 import BeautifulSoup, Tag

from ._helpers import safe_int, uncomment_tables


class ExecutiveProfileParser:
    """Parses a PFR executive profile page into structured data dicts."""

    def parse(self, html: str) -> Dict[str, Any]:
        """Parse a full executive profile page.

        Returns:
            A dict with keys ``bio``, ``exec_results``, and
            ``exec_results_totals``.
        """
        soup = BeautifulSoup(html, "html.parser")
        uncomment_tables(soup)

        bio = self._parse_bio(soup)

        table = soup.find("table", id="exec_results")
        if table is None:
            return {
                "bio": bio,
                "exec_results": [],
                "exec_results_totals": [],
            }

        results = self._parse_results(table)
        totals = self._parse_totals(table)

        return {
            "bio": bio,
            "exec_results": results,
            "exec_results_totals": totals,
        }

    # ------------------------------------------------------------------
    # Bio
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_bio(soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract the executive name from the ``#meta`` div."""
        bio: Dict[str, Any] = {"name": ""}

        h1 = soup.find("h1")
        if h1:
            name = h1.get_text(strip=True).replace("\xa0", " ")
            bio["name"] = name

        return bio

    # ------------------------------------------------------------------
    # Team Results (tbody)
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_results(table: Tag) -> List[Dict[str, Any]]:
        """Extract executive result rows from the exec_results tbody."""
        tbody = table.find("tbody")
        if tbody is None:
            return []

        results: List[Dict[str, Any]] = []

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

                if stat == "year_id":
                    row["year"] = text or None
                    if link:
                        row["year_href"] = link.get("href")
                elif stat == "team":
                    row["team"] = text or None
                    if link:
                        row["team_href"] = link.get("href")
                elif stat == "league_id":
                    row["league"] = text or None
                elif stat == "job_title":
                    row["job_title"] = text or None
                elif stat == "wins":
                    row["wins"] = safe_int(text)
                elif stat == "losses":
                    row["losses"] = safe_int(text)
                elif stat == "ties":
                    row["ties"] = safe_int(text)
                elif stat == "win_loss_perc":
                    row["win_loss_pct"] = text or None
                elif stat == "wins_playoffs":
                    row["playoff_wins"] = safe_int(text)
                elif stat == "losses_playoffs":
                    row["playoff_losses"] = safe_int(text)
                elif stat == "playoff_result":
                    row["playoff_result"] = text or None
                    if link:
                        row["playoff_result_href"] = link.get("href")

            if not all_empty:
                results.append(row)

        return results

    # ------------------------------------------------------------------
    # Totals (tfoot)
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_totals(table: Tag) -> List[Dict[str, Any]]:
        """Extract summary total rows from the exec_results tfoot."""
        tfoot = table.find("tfoot")
        if tfoot is None:
            return []

        totals: List[Dict[str, Any]] = []

        for tr in tfoot.find_all("tr"):
            row: Dict[str, Any] = {}

            for cell in tr.find_all(["th", "td"]):
                stat = cell.get("data-stat", "")
                if not stat:
                    continue

                text = cell.get_text(strip=True).replace("\xa0", " ")

                if stat == "team":
                    row["label"] = text or None
                elif stat == "job_title":
                    row["tenure"] = text or None
                elif stat == "wins":
                    row["wins"] = safe_int(text)
                elif stat == "losses":
                    row["losses"] = safe_int(text)
                elif stat == "ties":
                    row["ties"] = safe_int(text)
                elif stat == "wins_playoffs":
                    row["playoff_wins"] = safe_int(text)
                elif stat == "losses_playoffs":
                    row["playoff_losses"] = safe_int(text)

            if row:
                totals.append(row)

        return totals
