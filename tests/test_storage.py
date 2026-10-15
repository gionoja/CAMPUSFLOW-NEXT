
import json
import os
import tempfile
import unittest

from campusflow.tickets import create_ticket, generate_ticket_id
from campusflow.storage import load_tickets, save_tickets


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.filepath = os.path.join(
            self.temp_dir.name, "tickets.json"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_file_returns_empty_list(self):
        self.assertEqual(load_tickets(self.filepath), [])

    def test_save_and_load_tickets(self):
        tickets = []
        create_ticket(tickets, "Wi-Fi down", "Network")
        save_tickets(tickets, self.filepath)

        loaded = load_tickets(self.filepath)
        self.assertEqual(loaded, tickets)

    def test_ticket_id_continues_after_reload(self):
        tickets = []
        create_ticket(tickets, "Wi-Fi down", "Network")
        save_tickets(tickets, self.filepath)

        loaded = load_tickets(self.filepath)
        new_ticket = create_ticket(
            loaded, "Broken laptop", "Hardware"
        )
        self.assertEqual(new_ticket["id"], 2)

    def test_duplicate_ids_are_rejected(self):
        tickets = [
            {
                "id": 1, "title": "First", "category": "Network",
                "status": "open", "priority": "high", "notes": [],
            },
            {
                "id": 1, "title": "Second", "category": "Hardware",
                "status": "open", "priority": "low", "notes": [],
            },
        ]
        with self.assertRaises(ValueError):
            save_tickets(tickets, self.filepath)

    def test_invalid_json_is_rejected(self):
        with open(self.filepath, "w", encoding="utf-8") as file:
            file.write("{invalid json")

        with self.assertRaises(ValueError):
            load_tickets(self.filepath)

    def test_non_list_json_is_rejected(self):
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump({"tickets": []}, file)

        with self.assertRaises(ValueError):
            load_tickets(self.filepath)

    def test_invalid_ticket_does_not_save(self):
        tickets = [{
            "id": 1,
            "title": "",
            "category": "Network",
            "status": "open",
            "priority": "high",
            "notes": [],
        }]

        with self.assertRaises(ValueError):
            save_tickets(tickets, self.filepath)

        self.assertFalse(os.path.exists(self.filepath))


if __name__ == "__main__":
    unittest.main()
