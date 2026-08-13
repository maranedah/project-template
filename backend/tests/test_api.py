"""API tests: TestClient over the app factory with the in-memory twin injected."""

import unittest

from fastapi.testclient import TestClient

from app.application.item_service import ItemService
from app.infrastructure.api.app import create_app
from app.infrastructure.persistence.repositories import InMemoryItemRepository


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        app = create_app(ItemService(InMemoryItemRepository()))
        self.client = TestClient(app)

    def test_health(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_create_and_list_items(self) -> None:
        created = self.client.post("/api/items", json={"name": "Condor", "source": "api:test"})
        self.assertEqual(created.status_code, 201)
        body = created.json()
        self.assertEqual(body["name"], "Condor")
        self.assertEqual(body["source"], "api:test")

        listed = self.client.get("/api/items")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual([i["name"] for i in listed.json()], ["Condor"])

    def test_empty_name_returns_422_with_detail(self) -> None:
        response = self.client.post("/api/items", json={"name": " ", "source": "api:test"})
        self.assertEqual(response.status_code, 422)
        self.assertIn("non-empty", response.json()["detail"])


class JobQueueTests(unittest.TestCase):
    """Lease-queue semantics on the in-memory twin (Postgres twin runs in prod)."""

    def setUp(self) -> None:
        from app.infrastructure.persistence.job_queue import InMemoryJobQueue

        self.queue = InMemoryJobQueue(max_attempts=2)

    def test_claim_leases_and_second_claim_gets_nothing(self) -> None:
        self.queue.enqueue("noop", "{}")
        first = self.queue.claim()
        self.assertIsNotNone(first)
        self.assertEqual(first.status, "leased")
        self.assertIsNone(self.queue.claim())

    def test_fail_requeues_until_max_attempts(self) -> None:
        job = self.queue.enqueue("noop", "{}")
        self.queue.claim()
        self.queue.fail(job.id)
        self.assertIsNotNone(self.queue.claim())  # attempt 2
        self.queue.fail(job.id)
        self.assertIsNone(self.queue.claim())  # failed for good


if __name__ == "__main__":
    unittest.main()
