import re
from collections import defaultdict
from datetime import date, datetime
from typing import Mapping

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from griddy.core.utils.converters import multi_replace, safe_numberify, snakify
from griddy.pfr.models.entities.player_profile import PlayerProfile


class PlayerProfileParser:
    def __init__(self):
        self.soup: BeautifulSoup | None = None

    def _extract_names(self, name_tag: Tag) -> dict:

        full_name, *nicknames = (
            name_tag.get_text(strip=True).replace("\xa0", "").splitlines()
        )

        full_name_parts = full_name.split()
        suffix = ""
        # Hopefully We never encounter more than a VI
        if full_name_parts[-1].lower() in ["sr.", "jr.", "ii", "iii", "iv", "v", "vi"]:
            suffix = full_name_parts[-1]
            full_name_parts = full_name_parts[:-1]

        first_name = full_name_parts[0]
        middle_name = " ".join(full_name_parts[1:-1])
        last_name = full_name_parts[-1]

        if nicknames:
            nicknames_str = " ".join(nicknames)
            nicknames_list = [
                name.strip()
                for name in nicknames_str.replace("(", "")
                .replace(")", "")
                .replace(" or ", ",")
                .split(",")
            ]
        else:
            nicknames_list = []

        return {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "suffix": suffix,
            "nicknames": nicknames_list,
        }

    def _extract_pos(self, pos_tag: Tag) -> dict:
        # This will give a list like ["Position", "QB", "Throws", "Right"]
        text_vals = [
            val.strip()
            for val in pos_tag.get_text()
            .replace("\t", "")
            .replace(":", "\n")
            .splitlines()
            if val
        ]

        raw = dict(zip(text_vals[::2], text_vals[1::2]))

        # Transformed will look like
        transformed = {
            key.lower(): parts if len(parts := value.split("-")) > 1 else value
            for key, value in raw.items()
        }
        return transformed

    def _extract_height_weight(self, tag: Tag) -> dict:
        height, weight = tag.get_text().replace(",", "").split()[:2]
        feet, inches = height.split("-")

        height_inches = (int(feet) * 12) + int(inches.strip())

        return {"height": height_inches, "weight": weight.replace("lbs", "")}

    def _extract_birth_info(self, tag: Tag):
        birth_date_str = tag.find(id="necro-birth")["data-birth"]
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")

        birth_city, birth_state = (
            tag.find("span").get_text(strip=True).replace("in\xa0", "").split(",")
        )

        return {
            # TODO: Will it actually be easier to leave birth_date as a string?
            "birth_date": birth_date,
            "birth_place": {"city": birth_city, "state": birth_state},
        }

    def _parse_draft_info(self, draft_text: str) -> dict:
        reg = r"(\d{1,2})\w{2} round \((\d{1,3})\w{2} overall\)"
        match_ = re.search(reg, draft_text)
        return {"round": int(match_.group(1)), "overall": int(match_.group(2))}

    def _extract_pre_nfl(self, tag: Tag) -> dict:
        text_values = [
            s.strip().replace(":", "") for s in tag.get_text().splitlines() if s.strip()
        ]
        pre_nfl_info = {"college": "", "high_school": "", "draft": {}}
        for idx, value in enumerate(text_values):
            if value.lower() == "college":
                pre_nfl_info["college"] = text_values[idx + 1]
                continue
            elif value.lower() == "high school":
                pre_nfl_info["high_school"] = text_values[idx + 1]
                continue
            elif value.lower().startswith("draft"):
                draft_parts = [s.strip() for s in value.split("the")]
                team = (
                    draft_parts[0]
                    .lower()
                    .replace("draft", "")
                    .replace("in", "")
                    .strip()
                    .title()
                )
                rd_and_ovr = self._parse_draft_info(draft_text=draft_parts[1])
                year = int(re.search(r"^\d{4}", draft_parts[2]).group(0))
                pre_nfl_info["draft"] = {
                    "team": team,
                    "rd_and_ovr": rd_and_ovr,
                    "year": year,
                }
                continue

        return pre_nfl_info

    def _extract_bio_info(self, div: Tag):
        pretty_name = div.find("h1").get_text(strip=True)
        p_tags = div.find_all("p")

        names = self._extract_names(name_tag=p_tags[0])
        names["pretty_name"] = pretty_name

        position_info = self._extract_pos(pos_tag=p_tags[1])
        hgt_wgt_info = self._extract_height_weight(tag=p_tags[2])

        if "team" in p_tags[3].get_text().lower():
            birth_idx = 4
            pre_nfl_idx = 5
        else:
            birth_idx = 3
            pre_nfl_idx = 4

        birth_info = self._extract_birth_info(tag=p_tags[birth_idx])
        pre_nfl_info = self._extract_pre_nfl(tag=p_tags[pre_nfl_idx])

        ret_data = {
            "names": names,
            **position_info,
            **hgt_wgt_info,
            **birth_info,
            **pre_nfl_info,
        }

        return ret_data

    def _parse_meta_panel(self, panel: Tag) -> dict:
        img_tag = panel.find("img")
        photo_url = img_tag["src"] if img_tag else ""

        meta_info_div = panel.find(
            lambda tag: "media-item" not in tag.get("class", []), recursive=False
        )
        return {"photo_url": photo_url, **self._extract_bio_info(div=meta_info_div)}

    def _parse_bling(self, tag: Tag) -> list[str]:
        return [element.get_text(strip=True) for element in tag.find_all("li")]

    def _extract_team_and_years_jersey_num(self, text: str) -> dict:
        # Split on last space to separate team name from year(s).
        # This avoids issues with team names containing digits (e.g. "49ers").
        last_space_idx = text.rfind(" ")
        team = text[:last_space_idx].strip()
        years = text[last_space_idx + 1 :]

        if "-" in years:
            start_year, end_year = [int(y) for y in years.split("-")]
        else:
            start_year = end_year = int(years)

        return {"team": team, "start_year": start_year, "end_year": end_year}

    def _parse_jersey_numbers(self, tag: Tag) -> list[dict]:
        number_info = []
        number_elements = tag.find_all("a")

        for element in number_elements:
            team_and_years = element["data-tip"]
            # Ideally we could make this an int, but Jim Otto wearing #00 ruins that
            number_text = element.find("text").get_text(strip=True)
            number_info.append(
                {
                    "number": number_text,
                    **self._extract_team_and_years_jersey_num(text=team_and_years),
                }
            )

        return number_info

    def _parse_stats_summary(self, tag: Tag) -> dict:
        # noinspection PyTypeChecker
        summary_headers = [
            element.get_text(strip=True)
            for element in tag.find_all(
                "strong",
                string=lambda t: t and t.strip().lower() not in ["summary", "career"],
            )
        ]
        # noinspection PyTypeChecker
        values = [
            element.get_text(strip=True)
            for element in tag.find_all(
                "p",
                string=lambda t: t and t.strip().lower() not in ["summary", "career"],
            )
        ]
        values = [safe_numberify(value=v) for v in values]
        return dict(zip(summary_headers, values))

    def _extract_overheader_indices(self, thead: Tag):
        ovr_hdr_indices = {}

        overheader_cells = thead.find_all("th", class_="over_header")
        cur_index = 0
        for cell in overheader_cells:
            if "header_empty" in cell.attrs.get("data-stat", "").lower():
                hdr_value = "general"
            else:
                hdr_value = cell["data-stat"].lower()

            colspan = int(cell["colspan"])
            for idx in range(cur_index, cur_index + colspan):
                ovr_hdr_indices[idx] = hdr_value

        return ovr_hdr_indices

    def _group_by_over_header(self, stats: Mapping, over_header_indices: Mapping):
        grouped_stats = defaultdict(dict)

        for idx, key_value in enumerate(stats.items()):
            ovr_hdr = over_header_indices.get(idx)
            if not ovr_hdr:
                # Sometimes (for Awards columns) there is a blank over_header without "header_empty" in the data-stat attr.
                # For now, we will simply store these under "general" as well.
                ovr_hdr = over_header_indices[0]
            stat_key, value = key_value
            grouped_stats[ovr_hdr][stat_key] = value

        return grouped_stats

    def _parse_stats_table(self, table: Tag) -> list[dict]:
        over_header_indices = None
        if table.find(class_="over_header"):
            over_header_indices = self._extract_overheader_indices(
                thead=table.find("thead")
            )

        # prev_th = None
        # for th in table.find("thead").find_all("th"):
        #     if "data-stat" not in th.attrs:
        #         print(table["id"])
        #         print(prev_th.prettify())
        #     prev_th = th

        column_headers = [
            th["data-stat"]
            for th in table.find("thead").find_all("th")
            if "over_header" not in th.get("class", "") and "data-stat" in th.attrs
        ]
        season_rows = table.find("tbody").find_all("tr")

        seasons = []

        for row in season_rows:
            # PFR puts the season in a th tag instead of td for some reason
            try:
                year = safe_numberify(
                    row.find(attrs={"data-stat": ["year_id", "year"]}).get_text(
                        strip=True
                    )
                )
            except AttributeError as e:
                print(row.prettify())
                raise e
            values = [
                safe_numberify(td.get_text(strip=True)) for td in row.find_all("td")
            ]
            values = [year, *values]
            season_stats = dict(zip(column_headers, values))

            if over_header_indices:
                season_stats = self._group_by_over_header(
                    stats=season_stats, over_header_indices=over_header_indices
                )

            seasons.append(season_stats)

        return seasons

    def _extract_all_stats(self, stats_tables: ResultSet) -> Mapping:
        stats = defaultdict(dict)

        for table in stats_tables:
            tbl_name = table["id"]
            if tbl_name.lower() == "sim_scores":
                continue
            parsed = self._parse_stats_table(table=table)

            if "post" in tbl_name:
                stats["post_season"][tbl_name.replace("_post", "")] = parsed
            else:
                stats["regular_season"][tbl_name] = parsed

        return stats

    def _parse_transactions(self, tag: Tag) -> list[Mapping]:
        date_format_string = "%B %d, %Y"
        transactions = []

        transaction_strings = [
            li.get_text() for li in tag.find_all("li") if ":" in li.get_text()
        ]

        for ts in transaction_strings:
            date_string, description = ts.split(":")
            transactions.append(
                {
                    "date": date.strptime(date_string, date_format_string),
                    "description": description,
                }
            )

        return transactions

    def _parse_bottom_nav(self, tag: Tag) -> Mapping:
        player_links = defaultdict(dict)

        children = tag.find_all(recursive=False)

        overview, general, labels_and_links = children[0], children[1], children[2:]

        player_links["overview"] = {"href": overview.find("a")["href"]}

        for li in general.find_all("li"):
            as_key = multi_replace(
                text=li.get_text(), chars=[" ", "&", "-"], replace="_", dedupe=True
            ).lower()
            anchor = li.find("a")
            href = anchor["href"]
            player_links["general"][as_key] = href

        current_label = None
        for child in labels_and_links:
            if "listhead" in child["class"]:
                current_label = snakify(child.get_text())
                continue
            elif child.name != "ul":
                # TODO: Add logging
                continue
            links_for_label = {}
            # Can only be here if child is a ul tag
            for li in child.find_all("li"):
                key = snakify(li.get_text())
                href = li.find("a")["href"]
                links_for_label[key] = href
            player_links[current_label] = links_for_label

        return player_links

    def _parse_leader_boards(self, tag: Tag) -> Mapping:
        leader_boards = {}

        board_divs = tag.find_all(class_="data_grid_box")

        for div in board_divs:
            key = div["id"].replace("leaderboard_", "")
            leader_boards[key] = [td.get_text() for td in div.find_all("td")]

        return leader_boards

    def parse(self, html: str) -> PlayerProfile:
        cleaned_html = re.sub(r"<!--(.*?)-->", r"\1", html, flags=re.DOTALL)
        self.soup = BeautifulSoup(cleaned_html, features="html.parser")
        bio = self._parse_meta_panel(panel=self.soup.find(id="meta"))
        jersey_numbers = self._parse_jersey_numbers(
            tag=self.soup.find(class_="uni_holder")
        )
        summary_stats = self._parse_stats_summary(
            tag=self.soup.find(class_="stats_pullout")
        )

        stats_tables = self.soup.find_all("table", class_="stats_table")
        full_stats = self._extract_all_stats(stats_tables=stats_tables)

        transactions_div = self.soup.find(id="div_transactions")
        transactions = (
            self._parse_transactions(tag=transactions_div) if transactions_div else []
        )

        bottom_nav_div = self.soup.find(id="bottom_nav_container")
        player_links = (
            self._parse_bottom_nav(tag=bottom_nav_div) if bottom_nav_div else {}
        )

        leaderboard_div = self.soup.find(id="div_leaderboard")
        leader_boards = (
            self._parse_leader_boards(tag=leaderboard_div) if leaderboard_div else {}
        )

        return PlayerProfile.model_validate(
            {
                "bio": bio,
                "jersey_numbers": jersey_numbers,
                "summary_stats": summary_stats,
                "statistics": full_stats,
                "transactions": transactions,
                "links": player_links,
                "leader_boards": leader_boards,
            }
        )
