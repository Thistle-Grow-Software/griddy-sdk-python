"""HAR (HTTP Archive) file processing utilities."""

import json
from collections import defaultdict
from typing import Dict, List

html_template = """
<head>
    <meta http-equiv="Content-Type"
          content="text/html; charset=utf-8" />
    <title></title>
    <style type="text/css">
        table.diff {font-family: Menlo, Consolas, Monaco, Liberation Mono, Lucida Console, monospace; border:medium}
        .diff_header {background-color:#e0e0e0}
        td.diff_header {text-align:right}
        .diff_next {background-color:#c0c0c0}
        .diff_add {background-color:#aaffaa}
        .diff_chg {background-color:#ffff77}
        .diff_sub {background-color:#ffaaaa}
    </style>
</head>
<body>
"""


def extract_minified_har_entry(har_entry: Dict):
    response_json = json.loads(har_entry["response"]["content"]["text"])
    request_info = {
        key: value
        for key, value in har_entry["request"].items()
        if key in ["url", "headers", "queryString", "method", "path"]
    }

    url = request_info.pop("url")
    path_with_params = url.split(".com")[-1]
    path_only = path_with_params.split("?")[0]

    request_info["path"] = path_only

    return {"request": request_info, "response": response_json}


class HarEntryPathManager:
    def __init__(self, path: str, filename_prefix: str):
        self.path = path
        self.headers = {}
        self.query_params = defaultdict(set)
        # Not sure if we'll use this
        self.cookies = {}

        # Can we get away with just one?
        # if not, do we need to map params to the response?
        self.response_example = None
        self.filename_prefix = filename_prefix

    @property
    def filename(self):
        sub_name = ""
        for node in self.path.split("/"):
            if node == "api":
                continue
            sub_name += "_" + node.title()

        name = f"{self.filename_prefix}{sub_name}.json"
        return name.replace("-", "").replace("__", "_")

    def as_dict(self, exclude: List[str]) -> Dict:
        obj_dict = {}

        for attr in ["path", "headers", "query_params", "response_example"]:
            if attr in exclude:
                continue
            value = getattr(self, attr)
            if attr == "query_params":
                value = {
                    name: list(param_values) for name, param_values in value.items()
                }

            obj_dict[attr] = value

        return obj_dict

    def add_entry(self, entry: Dict):
        if entry["request"]["path"] != self.path:
            raise ValueError(
                f"Entry path {entry['request']['path']} "
                f"does not match the class path {self.path}"
            )

        for req_header in entry["request"]["headers"]:
            header = req_header["name"]
            value = req_header["value"]
            self.headers[header] = value

        for qp in entry["request"]["queryString"]:
            name = qp["name"]
            val = qp["value"]
            self.query_params[name].add(val)

        if entry["response"]:
            self.response_example = entry["response"]


def consolidate_minified_entries(entries: List[Dict]) -> Dict[str, HarEntryPathManager]:
    consolidated = {}

    for entry in entries:
        api_path = entry["request"]["path"]
        if api_path not in consolidated:
            consolidated[api_path] = HarEntryPathManager(
                path=api_path, filename_prefix="FiddlerSnapshots/ProNFL"
            )

        consolidated[api_path].add_entry(entry=entry)

    return consolidated


def write_consolidated_to_files(
    consolidated: Dict[str, HarEntryPathManager], exclude: List[str]
):
    for path, entries in consolidated.items():
        with open(entries.filename, "w") as outfile:
            jsonified = entries.as_dict(exclude=exclude)
            json.dump(jsonified, outfile, indent=4)


def minify_har(har_file: str):
    with open(har_file, mode="r", encoding="utf-8-sig") as infile:
        har_entries = json.load(infile)["log"]["entries"]

    minified_entries = []
    for entry in har_entries:
        minified_entries.append(extract_minified_har_entry(entry))

    return minified_entries
