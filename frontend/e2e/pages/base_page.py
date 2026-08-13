"""Base page object: waits + screenshots. Tests never touch selectors directly —
they go through page objects (docs/03-technical/07-e2e-validation/01-selenium.md)."""

from __future__ import annotations

from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "screenshots"


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def visible(self, testid: str, timeout: float = 10) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-testid='{testid}']"))
        )

    def wait_until(self, condition, timeout: float = 10) -> None:
        WebDriverWait(self.driver, timeout).until(lambda _: condition())

    def screenshot(self, name: str) -> None:
        """Screenshots are the artifacts the UI reviewer analyzes (guidelines 02-review)."""
        SCREENSHOT_DIR.mkdir(exist_ok=True)
        self.driver.save_screenshot(str(SCREENSHOT_DIR / f"{name}.png"))
