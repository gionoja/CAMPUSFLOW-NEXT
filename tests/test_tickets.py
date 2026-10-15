
import unittest

from campusflow.tickets import create_ticket, generate_ticket_id


class TestTickets(unittest.TestCase):
    def setUp(self):
        self.tickets = []

    def test_first_ticket_gets_id_one(self):
        self.assertEqual(generate_ticket_id(self.tickets), 1)

    def test_next_id_follows_highest_existing_id(self):
        self.tickets = [{"id": 2}, {"id": 7}]
        self.assertEqual(generate_ticket_id(self.tickets), 8)

    def test_ticket_is_created_with_expected_fields(self):
        ticket = create_ticket(
            self.tickets, "Wi-Fi down", "Network", "high", 2
        )
        self.assertEqual(ticket["id"], 1)
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(len(self.tickets), 1)

    def test_invalid_category_does_not_add_ticket(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Broken laptop", "Electricity")
        self.assertEqual(self.tickets, [])

    def test_invalid_affected_users_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "Wi-Fi down", "Network",
                          affected_users=0)
        self.assertEqual(self.tickets, [])

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(self.tickets, "  ", "Network")
        self.assertEqual(self.tickets, [])


if __name__ == "__main__":
    unittest.main()
