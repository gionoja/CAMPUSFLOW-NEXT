
"""Ticket creation and ID generation."""

from campusflow.validation import (
    validate_category,
    validate_priority,
    validate_text,
)


def generate_ticket_id(tickets):
    if not isinstance(tickets, list):
        raise ValueError("Tickets must be a list.")

    ids = []
    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Every ticket must be a dictionary.")
        ticket_id = ticket.get("id")
        if isinstance(ticket_id, bool) or not isinstance(ticket_id, int) or ticket_id < 1:
            raise ValueError("Every ticket must have a positive integer ID.")
        ids.append(ticket_id)

    return max(ids, default=0) + 1


def create_ticket(
    tickets,
    title,
    category,
    urgency="medium",
    affected_users=1,
):
    if not isinstance(tickets, list):
        raise ValueError("Tickets must be a list.")

    title = validate_text(title, "Title")
    category = validate_category(category)
    urgency = validate_priority(urgency)

    if (
        isinstance(affected_users, bool)
        or not isinstance(affected_users, int)
        or affected_users < 1
    ):
        raise ValueError("Affected users must be a positive integer.")

    # Higher impact raises the ticket priority.
    if urgency == "critical" or (urgency == "high" and affected_users >= 10):
        priority = "critical"
    elif urgency == "high" or affected_users >= 5:
        priority = "high"
    elif urgency == "medium":
        priority = "medium"
    else:
        priority = "low"

    ticket = {
        "id": generate_ticket_id(tickets),
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }

    tickets.append(ticket)
    return ticket
