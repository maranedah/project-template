"""Pattern exemplar: unittest.TestCase + in-memory adapter twin = offline by
construction. Run with `make test` (pytest -n auto, parallel)."""

import unittest

from app.application.item_service import ItemService
from app.domain.models import ValidationError
from app.infrastructure.persistence.repositories import InMemoryItemRepository


class CreateItemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = InMemoryItemRepository()
        self.service = ItemService(self.repo)

    def test_creates_item_with_id_and_source(self) -> None:
        item = self.service.create_item("Condor", "api:inaturalist")
        self.assertEqual(item.id, 1)
        self.assertEqual(item.source, "api:inaturalist")

    def test_strips_whitespace(self) -> None:
        item = self.service.create_item("  Condor  ", " manual:mauro ")
        self.assertEqual(item.name, "Condor")
        self.assertEqual(item.source, "manual:mauro")

    def test_rejects_empty_name(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.create_item("   ", "manual:mauro")

    def test_rejects_missing_source(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.create_item("Condor", "")


class ListItemsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = ItemService(InMemoryItemRepository())

    def test_empty_initially(self) -> None:
        self.assertEqual(self.service.list_items(), [])

    def test_returns_created_items_in_order(self) -> None:
        self.service.create_item("A", "manual:t")
        self.service.create_item("B", "manual:t")
        self.assertEqual([i.name for i in self.service.list_items()], ["A", "B"])


if __name__ == "__main__":
    unittest.main()
