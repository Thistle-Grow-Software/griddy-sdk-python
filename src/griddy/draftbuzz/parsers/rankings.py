"""Parser for NFL Draft Buzz position rankings pages.

Extracts prospect names, positions, schools, and rankings from the
``#positionRankTable`` on each position rankings page.
"""

from typing import Any, Dict, List

from bs4 import BeautifulSoup


class RankingsParser:
    """Parses an NFL Draft Buzz position rankings page into a dict."""

    def parse_position_rankings(
        self,
        html: str,
        *,
        position: str,
        year: int,
        page: int,
    ) -> Dict[str, Any]:
        """Parse a position rankings page.

        Args:
            html: Raw HTML of the rankings page.
            position: The position being ranked (e.g. ``"QB"``).
            year: Draft year.
            page: Page number.

        Returns:
            A dict matching the ``PositionRankings`` schema.
        """
        soup = BeautifulSoup(html, "html.parser")
        entries = self._extract_entries(soup)

        return {
            "position": position,
            "year": year,
            "page": page,
            "entries": entries,
        }

    def _extract_entries(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract ranked prospect entries from the rankings table."""
        entries: List[Dict[str, Any]] = []

        table = soup.find(id="positionRankTable")
        if not table:
            return entries

        tbody = table.find("tbody")
        if not tbody:
            return entries

        for rank, row in enumerate(tbody.find_all("tr"), start=1):
            href = row.get("data-href")
            cells = row.find_all("td")

            name = None
            position = None
            school = None

            if len(cells) >= 1:
                name = cells[0].get_text(strip=True)
            if len(cells) >= 2:
                position = cells[1].get_text(strip=True)
            if len(cells) >= 3:
                school = cells[2].get_text(strip=True)

            entries.append(
                {
                    "name": name,
                    "position": position,
                    "school": school,
                    "rank": rank,
                    "href": href,
                }
            )

        return entries
