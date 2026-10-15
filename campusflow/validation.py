
"""Validation helpers for CampusFlow tickets."""

CATEGORIES = ("Network", "Hardware", "Software", "Other")
STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")


def validate_text(value, field_name="Value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")
    return value.strip()


def validate_category(category):
    category = validate_text(category, "Category")
    for valid_category in CATEGORIES:
        if category.lower() == valid_category.lower():
            return valid_category
    raise ValueError("Invalid category.")


def validate_status(status):
    status = validate_text(status, "Status").lower()
    if status not in STATUSES:
        raise ValueError("Invalid status.")
    return status


def validate_priority(priority):
    priority = validate_text(priority, "Priority").lower()
    if priority not in PRIORITIES:
        raise ValueError("Invalid priority.")
    return priority


def validate_staff_name(staff_name):
    return validate_text(staff_name, "Staff name")


def validate_note(author, message):
    return {
        "author": validate_text(author, "Author"),
        "message": validate_text(message, "Note message"),
    }


def validate_ticket_data(ticket):
    if not isinstance(ticket, dict):
        raise ValueError("Ticket must be a dictionary.")

    validate_text(ticket.get("title"), "Title")
    validate_category(ticket.get("category"))
    validate_status(ticket.get("status"))
    validate_priority(ticket.get("priority"))

    ticket_id = ticket.get("id")
    if isinstance(ticket_id, bool) or not isinstance(ticket_id, int) or ticket_id < 1:
        raise ValueError("Ticket ID must be a positive integer.")

    return True
