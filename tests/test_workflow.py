
import unittest

from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, update_ticket_status


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        self.ticket = create_ticket(
            self.tickets, "Network outage", "Network"
        )

    def test_assign_ticket(self):
        assign_ticket(self.tickets, 1, "Ada")
        self.assertEqual(self.ticket["assigned_to"], "Ada")

    def test_non_string_staff_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, 1, 123)

    def test_blank_staff_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, 1, " ")

    def test_cannot_start_unassigned_ticket(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.tickets, 1, "in_progress")

    def test_assigned_ticket_can_start(self):
        assign_ticket(self.tickets, 1, "Ada")
        update_ticket_status(self.tickets, 1, "in_progress")
        self.assertEqual(self.ticket["status"], "in_progress")

    def test_ticket_can_be_resolved(self):
        assign_ticket(self.tickets, 1, "Ada")
        update_ticket_status(self.tickets, 1, "in_progress")
        update_ticket_status(self.tickets, 1, "resolved")
        self.assertEqual(self.ticket["status"], "resolved")

    def test_invalid_transition_is_rejected(self):
        with self.assertRaises(ValueError):
            update_ticket_status(self.tickets, 1, "resolved")

    def test_unknown_ticket_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, 99, "Ada")


if __name__ == "__main__":
    unittest.main()
