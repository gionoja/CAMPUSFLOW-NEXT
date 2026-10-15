
import unittest

from campusflow.validation import (
    validate_category,
    validate_priority,
    validate_staff_name,
    validate_status,
    validate_text,
    validate_ticket_data,
)


class TestValidation(unittest.TestCase):
    def test_valid_title_is_trimmed(self):
        self.assertEqual(validate_text("  Internet down  ", "Title"),
                         "Internet down")

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_text("   ", "Title")

    def test_category_is_case_insensitive(self):
        self.assertEqual(validate_category("network"), "Network")

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_category("Electricity")

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_status("in progress")

    def test_invalid_priority_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_priority("urgent")

    def test_blank_staff_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_staff_name(" ")

    def test_valid_ticket_data(self):
        ticket = {
            "id": 1,
            "title": "Wi-Fi failure",
            "category": "Network",
            "status": "open",
            "priority": "high",
        }
        self.assertTrue(validate_ticket_data(ticket))


if __name__ == "__main__":
    unittest.main()
