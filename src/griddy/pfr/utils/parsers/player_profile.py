import re
from datetime import datetime

from bs4 import BeautifulSoup
from bs4.element import Tag


class PlayerProfileParser:
    def __init__(self):
        self.soup: BeautifulSoup | None = None

    def _extract_names(self, name_tag: Tag) -> dict:
        full_name, nicknames = (
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

        nicknames_list = [
            name.strip()
            for name in nicknames.replace("(", "")
            .replace(")", "")
            .replace("or", ",")
            .split(",")
        ]

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

        return {
            "names": names,
            **self._extract_pos(pos_tag=p_tags[1]),
            **self._extract_height_weight(tag=p_tags[2]),
            **self._extract_birth_info(tag=p_tags[3]),
            **self._extract_pre_nfl(tag=p_tags[4]),
        }

    def _parse_meta_panel(self, panel: Tag) -> dict:
        img_tag = panel.find("img")
        photo_url = img_tag["src"] if img_tag else ""

        meta_info_div = panel.find(
            lambda tag: "media-item" not in tag.get("class", []), recursive=False
        )
        return {"photo_url": photo_url, **self._extract_bio_info(div=meta_info_div)}

    def parse(self, html: str):
        self.soup = BeautifulSoup(html)
        bio = self._parse_meta_panel(panel=self.soup.find(id="meta"))
