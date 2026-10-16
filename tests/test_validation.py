"""Unit tests for CampusFlow Next validation helpers."""

import unittest

# Import the functions we want to test.
from campusflow.validation import (
    validate_title,
    normalize_category,
    normalize_urgency,
    validate_affected_users,
    validate_staff_name,
    validate_note_author,
    validate_note_message,
)


class TestValidateTitle(unittest.TestCase):
    """Tests for ticket title validation."""

    def test_valid_title(self):
        self.assertEqual(
            validate_title("Network problem"),
            "Network problem",
        )

    def test_removes_extra_spaces(self):
        self.assertEqual(
            validate_title("  Network problem  "),
            "Network problem",
        )

    def test_rejects_empty_title(self):
        with self.assertRaises(ValueError):
            validate_title("")

    def test_rejects_whitespace_title(self):
        with self.assertRaises(ValueError):
            validate_title("   ")

    def test_rejects_non_string_title(self):
        with self.assertRaises(ValueError):
            validate_title(123)


class TestNormalizeCategory(unittest.TestCase):
    """Tests for predefined and custom ticket categories."""

    def test_valid_category(self):
        self.assertEqual(normalize_category("Network"), "Network")

    def test_normalizes_category_capitalization(self):
        self.assertEqual(normalize_category("network"), "Network")
        self.assertEqual(normalize_category("HARDWARE"), "Hardware")
        self.assertEqual(normalize_category("software"), "Software")

    def test_accepts_custom_category(self):
        self.assertEqual(
            normalize_category("Electricity"),
            "Electricity",
        )

    def test_removes_extra_spaces(self):
        self.assertEqual(
            normalize_category("  Water Supply  "),
            "Water Supply",
        )

    def test_rejects_empty_category(self):
        with self.assertRaises(ValueError):
            normalize_category("")

    def test_rejects_non_string_category(self):
        with self.assertRaises(ValueError):
            normalize_category(123)


class TestNormalizeUrgency(unittest.TestCase):
    """Tests for ticket urgency validation."""

    def test_accepts_valid_urgencies(self):
        for urgency in ("low", "medium", "high"):
            with self.subTest(urgency=urgency):
                self.assertEqual(
                    normalize_urgency(urgency),
                    urgency,
                )

    def test_normalizes_urgency(self):
        self.assertEqual(normalize_urgency(" HIGH "), "high")
        self.assertEqual(normalize_urgency("Medium"), "medium")

    def test_rejects_invalid_urgency(self):
        with self.assertRaises(ValueError):
            normalize_urgency("urgent")

    def test_rejects_empty_urgency(self):
        with self.assertRaises(ValueError):
            normalize_urgency("")

    def test_rejects_non_string_urgency(self):
        with self.assertRaises(ValueError):
            normalize_urgency(123)


class TestValidateAffectedUsers(unittest.TestCase):
    """Tests for affected-user count validation."""

    def test_accepts_positive_integer(self):
        self.assertEqual(validate_affected_users(5), 5)

    def test_accepts_one(self):
        self.assertEqual(validate_affected_users(1), 1)

    def test_rejects_zero(self):
        with self.assertRaises(ValueError):
            validate_affected_users(0)

    def test_rejects_negative_number(self):
        with self.assertRaises(ValueError):
            validate_affected_users(-2)

    def test_rejects_string_number(self):
        with self.assertRaises(ValueError):
            validate_affected_users("5")

    def test_rejects_float(self):
        with self.assertRaises(ValueError):
            validate_affected_users(5.0)

    def test_rejects_true(self):
        with self.assertRaises(ValueError):
            validate_affected_users(True)

    def test_rejects_false(self):
        with self.assertRaises(ValueError):
            validate_affected_users(False)


class TestValidateStaffName(unittest.TestCase):
    """Tests for staff member name validation."""

    def test_accepts_staff_name(self):
        self.assertEqual(
            validate_staff_name("Daniel"),
            "Daniel",
        )

    def test_removes_extra_spaces(self):
        self.assertEqual(
            validate_staff_name("  Daniel Akpa  "),
            "Daniel Akpa",
        )

    def test_accepts_name_with_numbers(self):
        # The current function accepts digits if the name
        # also contains at least one letter.
        self.assertEqual(
            validate_staff_name("Daniel22"),
            "Daniel22",
        )

    def test_rejects_empty_name(self):
        with self.assertRaises(ValueError):
            validate_staff_name("")

    def test_rejects_whitespace_name(self):
        with self.assertRaises(ValueError):
            validate_staff_name("   ")

    def test_rejects_digits_only_name(self):
        with self.assertRaises(ValueError):
            validate_staff_name("22")

    def test_rejects_non_string_name(self):
        with self.assertRaises(ValueError):
            validate_staff_name(22)


class TestValidateNoteAuthor(unittest.TestCase):
    """Tests for ticket note author validation."""

    def test_accepts_author(self):
        self.assertEqual(
            validate_note_author("Daniel"),
            "Daniel",
        )

    def test_removes_extra_spaces(self):
        self.assertEqual(
            validate_note_author("  Daniel  "),
            "Daniel",
        )

    def test_rejects_empty_author(self):
        with self.assertRaises(ValueError):
            validate_note_author("")

    def test_rejects_whitespace_author(self):
        with self.assertRaises(ValueError):
            validate_note_author("   ")

    def test_rejects_non_string_author(self):
        with self.assertRaises(ValueError):
            validate_note_author(123)


class TestValidateNoteMessage(unittest.TestCase):
    """Tests for ticket note message validation."""

    def test_accepts_valid_message(self):
        self.assertEqual(
            validate_note_message("Network issue fixed"),
            "Network issue fixed",
        )

    def test_removes_extra_spaces(self):
        self.assertEqual(
            validate_note_message("  Issue has been fixed  "),
            "Issue has been fixed",
        )

    def test_accepts_exactly_five_characters(self):
        self.assertEqual(
            validate_note_message("12345"),
            "12345",
        )

    def test_accepts_exactly_three_hundred_characters(self):
        message = "x" * 300

        self.assertEqual(
            validate_note_message(message),
            message,
        )

    def test_rejects_message_too_short(self):
        with self.assertRaises(ValueError):
            validate_note_message("abcd")

    def test_rejects_message_too_long(self):
        with self.assertRaises(ValueError):
            validate_note_message("x" * 301)

    def test_rejects_empty_message(self):
        with self.assertRaises(ValueError):
            validate_note_message("")

    def test_rejects_whitespace_message(self):
        with self.assertRaises(ValueError):
            validate_note_message("     ")

    def test_rejects_non_string_message(self):
        with self.assertRaises(ValueError):
            validate_note_message(12345)


# Run the tests when this file is executed directly.
if __name__ == "__main__":
    unittest.main()