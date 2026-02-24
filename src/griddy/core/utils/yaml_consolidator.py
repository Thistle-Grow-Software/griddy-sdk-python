"""OpenAPI YAML spec consolidation utilities."""

import difflib
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import yaml

from .har import html_template


class YAMLConsolidator:

    open_api_doc_keys = [
        "openapi",
        "info",
        "servers",
        "security",
        "tags",
        "paths",
        "components",
    ]

    def __init__(self, spec_dir: str, pattern: str):
        self.spec_dir = Path(spec_dir)
        self.specs = {}
        self.load_specs(pattern=pattern)

        self.open_api = None
        self.info = {}
        self.servers = []
        self.security = []

        self.components = {}
        self.paths = {}
        self.tags = []
        self.diff_counts = defaultdict(int)
        self.cur_spec_name = None

        self.diffs = {
            "components": {"schemas": [], "securitySchemes": []},
            "paths": [],
            "tags": [],
        }

        self.original_entry_source = {}

        self.combined_spec = {}

    def _set_openapi_attr(self, attr: str):
        attr_map = {}
        for spec_name, spec in self.specs.items():
            attr_map[spec_name] = spec.get(attr)

        setattr(self, attr, attr_map)

    def add_diff_entry(self, attr, key, old, new):
        diff_entry = {
            "key": key,
            "existing_value": json.dumps(old, indent=4),
            "existing_source": self.original_entry_source[f"{attr}.{key}"],
            "new_value": json.dumps(new, indent=4),
            "new_source": self.cur_spec_name,
        }
        diff_entry.update(self.compute_diff_info(diff_entry=diff_entry))
        self.diffs[attr].append(diff_entry)

    def add_spec(self, spec_path: str | Path):
        if isinstance(spec_path, str):
            spec_path = Path(spec_path)
        if not spec_path.exists():
            raise FileNotFoundError(f"{spec_path} does not exist.")
        if spec_path.stem in self.specs:
            raise ValueError(f"{spec_path.stem} is already in self.specs.")

        with spec_path.open() as infile:
            self.specs[spec_path.stem] = self.get_sorted_spec(yaml.full_load(infile))

    def combine_all_specs(self):
        for name, spec in self.specs.items():
            print(name)
            self.cur_spec_name = name
            self.integrate_spec(spec=spec)

        self.combined_spec = {
            "openapi": self.open_api,
            "info": self.info,
            "servers": self.servers,
            "security": self.security,
            "tags": self.tags,
            "paths": self.paths,
            "components": self.components,
        }

    def compute_diff_info(self, diff_entry: Dict):
        differ = difflib.HtmlDiff()
        try:
            existing = diff_entry["existing_value"].splitlines()
            new_ = diff_entry["new_value"].splitlines()
        except AttributeError as e:
            from pprint import pprint

            pprint(diff_entry["existing_value"], indent=4)
            pprint(diff_entry["new_value"], indent=4)
            raise e

        diff_html = differ.make_table(existing, new_)
        similarity_matcher = difflib.SequenceMatcher(None, existing, new_)
        return {"html": diff_html, "similarity": similarity_matcher.ratio()}

    def create_full_html_string(self, diffs_list):
        diffs_html = "<div>\n"
        for diff_entry in diffs_list:
            diffs_html += (
                f"<br>\n"
                f"<h3>{diff_entry['key']}</h3>"
                f"<p>Original Source: {diff_entry['existing_source']}</p>"
                f"<p>New Source: {diff_entry['new_source']}</p>"
                f"{diff_entry['html']}\n"
                f"<br>\n"
            )
        diffs_html += f"</div>"
        return diffs_html

    def get_open_api_attr(self, attr: str):
        if getattr(self, attr) is None:
            self._set_openapi_attr(attr=attr)

        return getattr(self, attr)

    def get_sorted_spec(self, spec: Dict) -> Dict:
        sorted_spec = {
            key: spec[key] for key in ["openapi", "info", "servers", "security"]
        }

        for key in ["tags", "paths", "components"]:
            sorted_spec[key] = self.sort_entries_for_attr(spec=spec, attr=key)

        return sorted_spec

    def handle_component_diffs(self):
        schemas_diffs = self.diffs["components"]["schemas"]
        security_schemes_diffs = self.diffs["components"]["securitySchemes"]

        schemas_html = self.create_full_html_string(schemas_diffs)
        security_schemes_html = self.create_full_html_string(security_schemes_diffs)
        return schemas_html, security_schemes_html

    def integrate_attr(self, spec, attr):
        if attr == "components":
            self.integrate_components(spec[attr])
            return
        elif attr == "tags":
            self.integrate_tags(tags=spec.get(attr, []))
            return

        existing_entries = getattr(self, attr)

        for key, new_entry in spec[attr].items():
            if key in existing_entries:
                if new_entry == (old_entry := existing_entries[key]):
                    continue
                else:
                    self.add_diff_entry(
                        attr=attr, key=key, old=old_entry, new=new_entry
                    )
                    self.diff_counts[attr] += 1
            else:
                existing_entries[key] = new_entry
                self.original_entry_source[f"{attr}.{key}"] = self.cur_spec_name

        setattr(self, attr, existing_entries)

    def integrate_components(self, components):
        new_components = {}

        for sub_component in ["schemas", "securitySchemes"]:

            existing = self.components.get(sub_component, {})
            for key, new_entry in components[sub_component].items():

                if key in existing:
                    if new_entry == (old_entry := existing[key]):
                        continue
                    else:
                        original_source = self.original_entry_source[
                            f"components.{sub_component}.{key}"
                        ]
                        diff_entry = {
                            "key": key,
                            "existing_value": json.dumps(old_entry, indent=4),
                            "existing_source": original_source,
                            "new_value": json.dumps(new_entry, indent=4),
                            "new_source": self.cur_spec_name,
                        }
                        diff_entry.update(self.compute_diff_info(diff_entry=diff_entry))

                        self.diffs["components"][sub_component].append(diff_entry)
                        self.diff_counts[f"components.{sub_component}"] += 1
                else:
                    existing[key] = new_entry
                    self.original_entry_source[f"components.{sub_component}.{key}"] = (
                        self.cur_spec_name
                    )
            new_components[sub_component] = existing

        self.components = new_components

    def integrate_spec(self, spec):
        for key in ["tags", "paths", "components"]:
            self.integrate_attr(spec, key)

    def integrate_tags(self, tags):
        existing_tags = {t["name"]: t["description"] for t in self.tags}

        for t in tags:
            if t["name"] in existing_tags:
                if (new_value := t["description"]) != (
                    old_value := existing_tags[t["name"]]
                ):
                    diff_entry = {
                        "key": t["name"],
                        "existing_value": json.dumps(old_value, indent=4),
                        "existing_source": self.original_entry_source[
                            f"tags.{t['name']}"
                        ],
                        "new_value": json.dumps(new_value, indent=4),
                        "new_source": self.cur_spec_name,
                    }
                    diff_entry.update(self.compute_diff_info(diff_entry=diff_entry))

                    self.diffs["tags"].append(diff_entry)
                    self.diff_counts["tags"] += 1
            else:
                self.tags.append(t)
                self.original_entry_source[f"tags.{t['name']}"] = self.cur_spec_name

    def load_specs(self, pattern: str):
        specs = {}
        for spec_file in self.spec_dir.glob(pattern=pattern):
            self.add_spec(spec_path=spec_file)

        return specs

    def output_diff(self):
        full_html = html_template
        for diff_type in self.diffs:
            if diff_type == "components":
                schemas_html, security_schemes_html = self.handle_component_diffs()
                full_html += schemas_html
                full_html += security_schemes_html
            elif diff_type == "paths":
                paths_html = self.create_full_html_string(self.diffs["paths"])
                full_html += paths_html
            elif diff_type == "tags":
                tags_html = self.create_full_html_string(self.diffs["tags"])
                full_html += tags_html

        full_html += "<br>\n" "\t</body>\n" "</html>"
        from pprint import pprint

        pprint(self.diff_counts, indent=4)
        self.write_to_html(file_name="pro-reg-combined.html", html_text=full_html)

    def set_common_info(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def sort_all_specs(self):
        for name, spec in self.specs.items():
            self.specs[name] = self.get_sorted_spec(spec=spec)

    def sort_entries_for_attr(self, spec: Dict, attr: str) -> Dict | List | None:
        sorted_attr_entry = None

        if attr not in spec:
            return sorted_attr_entry

        if attr == "paths":
            sorted_attr_entry = dict(sorted(spec["paths"].items()))
        elif attr == "components":
            schemas_sorted = dict(sorted(spec["components"]["schemas"].items()))
            security_schemes_sorted = dict(
                sorted(spec["components"]["securitySchemes"].items())
            )
            sorted_attr_entry = {
                "schemas": schemas_sorted,
                "securitySchemes": security_schemes_sorted,
            }
        elif attr == "tags":
            sorted_attr_entry = sorted(spec["tags"], key=lambda entry: entry["name"])

        return sorted_attr_entry

    def write_spec_to_disk(self, file_name: str, spec):
        print(f"Writing spec to {file_name}")

        with open(file_name, "w") as outfile:
            yaml.dump(spec, outfile)
            print(f"Success")

    def write_to_disk(self, directory: str = None, suffix: str = ""):
        if directory is None:
            directory = os.getcwd()

        print(f"Writing all specs to directory: {directory}")
        for name, spec in self.specs.items():
            file_name = f"{directory}/{name}{suffix}.yaml"
            self.write_spec_to_disk(file_name=file_name, spec=spec)

    def write_to_html(self, file_name, html_text):
        with open(file_name, "w") as outfile:
            outfile.write(html_text)
