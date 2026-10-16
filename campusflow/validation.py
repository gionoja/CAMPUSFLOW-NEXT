"""Validation helpers for CampusFlow Next."""

# Only these categories are allowed.
VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}

# Only these urgency levels are allowed.
VALID_URGENCIES = {"low", "medium", "high"}

VALID_STATUSES = {"open", "in_progress", "resolved"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}


def validate_title(title):
    """Check that a ticket title is not empty."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be empty.")

    return title.strip()



def normalize_category(category):
    """Accept predefined categories or a custom category."""

    # Make sure the category is text.
    if not isinstance(category, str):
        raise ValueError("Category must be text.")

    # Remove unnecessary spaces.
    cleaned = category.strip()

    # Reject an empty category.
    if not cleaned:
        raise ValueError("Category cannot be empty.")

    # Match predefined categories without worrying about capitalization.
    for valid_category in VALID_CATEGORIES:
        if cleaned.casefold() == valid_category.casefold():
            return valid_category

    # Accept custom categories that contain meaningful text.
    return cleaned


def normalize_urgency(urgency):
    """Validate urgency and return it in lowercase."""
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be text.")

    cleaned = urgency.strip().lower()

    if cleaned not in VALID_URGENCIES:
        raise ValueError("Urgency must be low, medium, or high.")

    return cleaned

def validate_affected_users(affected_users):
    """Require a positive integer, rejecting booleans too."""

    # Check whether the value is a boolean or is not an integer.
    # In Python, bool is a subclass of int, so we must reject
    # True and False explicitly.
    if isinstance(affected_users, bool) or not isinstance(
        affected_users, int
    ):
        raise ValueError("Affected users must be a whole number.")

    # Ensure the number of affected users is greater than zero.
    # Zero and negative numbers are not valid.
    if affected_users <= 0:
        raise ValueError("Affected users must be greater than zero.")

    # Return the validated number if all checks pass.
    return affected_users

def validate_staff_name(staff_name):
    """Require a staff name containing letters."""

    # Ensure the input is text.
    if not isinstance(staff_name, str):
        raise ValueError("Staff name must be text.")

    # Remove unnecessary spaces.
    cleaned = staff_name.strip()

    # Reject empty input.
    if not cleaned:
        raise ValueError("Staff name cannot be empty.")

    # Require at least one letter.
    if not any(character.isalpha() for character in cleaned):
        raise ValueError("Staff name must contain letters.")

    # Return the cleaned name.
    return cleaned

def validate_note_author(author):
    """Require a nonempty note author."""

    # Check that the author is a string and is not empty
    # or made up entirely of whitespace.
    if not isinstance(author, str) or not author.strip():
        raise ValueError("Note author cannot be empty.")

    # Remove leading and trailing spaces, then return the author's name.
    return author.strip()

def validate_note_message(message):
    """Require a note containing 5–300 characters after trimming."""

    # Check that the message is a string.
    # Reject numbers, lists, and other data types.
    if not isinstance(message, str):
        raise ValueError("Note message must be text.")

    # Remove unnecessary spaces from the beginning and end.
    cleaned = message.strip()

    # Ensure the message contains at least 5 characters
    # and no more than 300 characters after trimming.
    if not 5 <= len(cleaned) <= 300:
        raise ValueError(
            "Note message must contain 5 to 300 characters."
        )

    # Return the cleaned message if it passes validation.
    return cleaned