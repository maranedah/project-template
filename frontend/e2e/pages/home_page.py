from __future__ import annotations

from pages.base_page import BasePage


class HomePage(BasePage):
    def open(self, base_url: str) -> None:
        self.driver.get(base_url)
        self.visible("item-form")

    def add_item(self, name: str) -> None:
        self.visible("item-name").send_keys(name)
        self.visible("item-submit").click()

    def item_names(self) -> list[str]:
        rows = self.driver.find_elements("css selector", "[data-testid='item-row']")
        return [row.text for row in rows]

    def wait_for_item(self, name: str) -> None:
        self.wait_until(lambda: any(name in text for text in self.item_names()))

    def error_text(self) -> str:
        return self.visible("item-error").text
