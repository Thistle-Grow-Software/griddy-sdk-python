import os
from pathlib import Path

BROWSERLESS_HOST = os.getenv("BROWSERLESS_HOST")
BROWSERLESS_TOKEN = os.getenv("BROWSERLESS_TOKEN")

FIXTURE_DIR = Path(__file__).resolve().parents[2] / "tests" / "fixtures"

NFL = {
    "api_key": os.getenv("NFL_API_KEY"),
    "sdk_build": os.getenv("NFL_SDK_BUILD", "15170"),
    "clientKey": os.getenv("NFL_CLIENT_KEY"),
    "clientSecret": os.getenv("NFL_CLIENT_SECRET"),
    "auth_url": "https://auth-id.nfl.com/",
    "account_url": "https://auth-id.nfl.com/accounts.getAccountInfo",
    "token_url": "https://api.nfl.com/identity/v3/token",
    "base_api_url": "https://api.nfl.com/football/v2/",
    "pro_api_base_url": "https://pro.nfl.com/api/",
    "login_email": os.getenv("NFL_LOGIN_EMAIL"),
    "login_password": os.getenv("NFL_LOGIN_PASSWORD"),
}
