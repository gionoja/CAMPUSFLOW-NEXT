
import unittest

from campusflow.tickets import create_ticket
from campusflow.notes import add_note, get_notes


class TestNotes(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        create_ticket(self.tickets, "Network outage", "Network")

    def test_add_note(self):
        note = add_note(self.tickets, 1, "Ada", "Router restarted")
        self.assertEqual(note["author"], "Ada")
        self.assertEqual(note["message"], "Router restarted")

    def test_retrieve_notes(self):
        add_note(self.tickets, 1, "Ada", "Checked router")
        notes = get_notes(self.tickets, 1)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["message"], "Checked router")

    def test_blank_author_is_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, 1, " ", "Checked router")

    def test_blank_message_is_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, 1, "Ada", " ")

    def test_invalid_note_does_not_change_notes(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, 1, "Ada", "")
        self.assertEqual(get_notes(self.tickets, 1), [])

    def test_unknown_ticket_is_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, 99, "Ada", "Test note")


if __name__ == "__main__":
    unittest.main()
