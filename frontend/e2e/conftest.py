"""Selenium E2E config. Headless Chrome via Selenium Manager (built into Selenium 4 —
resolves a matching chromedriver automatically, nothing to install).

Env (SSOT: ../.env.example): E2E_BASE_URL (target stack), E2E_HEADLESS (0 to watch).
Tests run in parallel (`make e2e` → pytest -n auto): each test builds its own driver
and uses unique data, so worker order never matters.
"""

from __future__ import annotations

import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = os.environ.get("E2E_BASE_URL", "http://localhost:3100")
HEADLESS = os.environ.get("E2E_HEADLESS", "1") != "0"


def build_driver() -> webdriver.Chrome:
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,900")
    # Required inside CI containers; harmless locally.
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)
