"""Shared constants for the DraftBuzz SDK."""

# ---------------------------------------------------------------------------
# Position Mappings
# ---------------------------------------------------------------------------

POSITION_TO_GROUP_MAP: dict[str, str] = {
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

# ---------------------------------------------------------------------------
# Playwright Browser Defaults
# ---------------------------------------------------------------------------

DEFAULT_SLOW_MO_MS = 150
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

RECOVERABLE_ERROR_PHRASES = ("target closed", "browser has been closed")
