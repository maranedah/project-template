"""Smoke suite: exercises the primary UI workflow end-to-end against the compose
stack (make up && make e2e). unittest classes; each test gets its own driver and
unique data — safe under pytest-xdist parallelism."""

import unittest
import uuid

from conftest import BASE_URL, build_driver
from pages.home_page import HomePage


class CreateItemWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = build_driver()
        self.addCleanup(self.driver.quit)
        self.page = HomePage(self.driver)

    def test_create_item_appears_in_list(self) -> None:
        name = f"e2e-{uuid.uuid4().hex[:8]}"
        self.page.open(BASE_URL)
        self.page.add_item(name)
        self.page.wait_for_item(name)
        self.page.screenshot("create-item-listed")

    def test_empty_name_shows_backend_error(self) -> None:
        self.page.open(BASE_URL)
        self.page.add_item("   ")
        self.assertIn("non-empty", self.page.error_text())
        self.page.screenshot("create-item-validation-error")


if __name__ == "__main__":
    unittest.main()
