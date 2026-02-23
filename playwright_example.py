"""
Scrape Pro Football Reference 2015 NFL Games using Browserless + Playwright.

Provides two approaches:
  1. Stealth BQL  — Use BrowserQL's stealth mutation to bypass bot detection,
                    then connect Playwright to the returned browser session.
  2. Unblock API  — Call /chromium/unblock to bypass bot detection with a
                    residential proxy, then connect Playwright to the session.

Requirements:
    pip install playwright requests
    Environment variable: BROWSERLESS_API_KEY

Usage:
    # Default (unblock approach)
    python playwright_example.py

    # Choose approach via env var
    BROWSERLESS_APPROACH=stealth python playwright_example.py
"""

import os
import sys

import requests
from playwright.sync_api import sync_playwright

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BROWSERLESS_TOKEN = os.environ.get("BROWSERLESS_API_KEY", "")
BROWSERLESS_HOST = "production-sfo.browserless.io"
TARGET_URL = "https://www.pro-football-reference.com/years/2015/games.htm"
# https://www.pro-football-reference.com/boxscores/201509100nwe.htm
OUTPUT_FILE = "pfr_2015_sked.html"

APPROACH = os.environ.get("BROWSERLESS_APPROACH", "unblock")


# ---------------------------------------------------------------------------
# Approach 1: Stealth BQL
# ---------------------------------------------------------------------------
def connect_stealth_bql(playwright):
    """
    Use BrowserQL's stealth mutation to navigate to the target URL with bot
    detection bypassed, then reconnect Playwright to the browser session.
    """
    bql_url = f"https://{BROWSERLESS_HOST}/stealth/bql?token={BROWSERLESS_TOKEN}"
    payload = {
        "query": """mutation Unblock($url: String!) {
            goto(url: $url, waitUntil: networkIdle) { status }
            reconnect(timeout: 30000) { browserWSEndpoint }
        }""",
        "variables": {"url": TARGET_URL},
    }

    print(f"[stealth-bql] Calling /stealth/bql for {TARGET_URL}...")
    resp = requests.post(
        bql_url, json=payload, headers={"Content-Type": "application/json"}
    )
    resp.raise_for_status()
    data = resp.json()["data"]

    ws_endpoint = data["reconnect"]["browserWSEndpoint"]
    print(f"[stealth-bql] Got browserWSEndpoint, connecting Playwright...")
    browser = playwright.chromium.connect_over_cdp(
        f"{ws_endpoint}?token={BROWSERLESS_TOKEN}"
    )

    # BQL already navigated to the page — find it in the existing context.
    page = None
    for ctx in browser.contexts:
        for p in ctx.pages:
            if TARGET_URL in p.url:
                page = p
                break
        if page:
            break

    if not page:
        print("[stealth-bql] Page not found in contexts, creating new page...")
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()
        page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60_000)

    return browser, page


# ---------------------------------------------------------------------------
# Approach 2: Unblock API
# ---------------------------------------------------------------------------
def connect_unblock(playwright):
    """
    Use the Browserless /chromium/unblock REST API to bypass bot detection on
    the target URL, then connect Playwright to the returned browser WebSocket
    endpoint. The browser already has the page loaded and cookies set.
    """
    unblock_url = f"https://{BROWSERLESS_HOST}/chromium/unblock"
    query_params = {
        "token": BROWSERLESS_TOKEN,
        "proxy": "residential",
        "timeout": 60_000,
    }
    payload = {
        "url": TARGET_URL,
        "browserWSEndpoint": True,
        "cookies": True,
        "content": False,
        "screenshot": False,
        "ttl": 30_000,
    }

    print(f"[unblock] Calling /chromium/unblock for {TARGET_URL}...")
    resp = requests.post(
        unblock_url,
        json=payload,
        params=query_params,
        headers={"Content-Type": "application/json"},
    )
    resp.raise_for_status()
    data = resp.json()

    ws_endpoint = data["browserWSEndpoint"]
    cookies = data.get("cookies", [])

    print(f"[unblock] Got browserWSEndpoint, connecting Playwright...")
    browser = playwright.chromium.connect_over_cdp(ws_endpoint)

    # The unblock API already navigated to TARGET_URL in the first page.
    page = None
    for ctx in browser.contexts:
        for p in ctx.pages:
            if TARGET_URL in p.url:
                page = p
                break
        if page:
            break

    if page:
        print(f"[unblock] Reusing existing page at: {page.url}")
    else:
        print("[unblock] Page not found in contexts, creating new page...")
        context = browser.new_context()
        page = context.new_page()
        if cookies:
            context.add_cookies(cookies)
        page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60_000)

    return browser, page


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if not BROWSERLESS_TOKEN:
        print("Error: BROWSERLESS_API_KEY environment variable is not set.")
        sys.exit(1)

    approach = APPROACH.lower()
    if approach not in ("stealth", "unblock"):
        print(f"Unknown approach '{approach}'. Use 'stealth' or 'unblock'.")
        sys.exit(1)

    with sync_playwright() as pw:
        if approach == "stealth":
            browser, page = connect_stealth_bql(pw)
        else:
            browser, page = connect_unblock(pw)

        # Wait for table to be present in the DOM
        print("Waiting for page content...")
        page.wait_for_selector("table#games", timeout=15_000)

        html = page.content()
        browser.close()

    with open(OUTPUT_FILE, "w") as f:
        f.write(html)
    print(f"Saved HTML to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
