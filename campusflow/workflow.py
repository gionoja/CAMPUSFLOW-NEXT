
"""Ticket assignment and status transitions."""

from campusflow.validation import validate_staff_name, validate_status

ALLOWED_TRANSITIONS = {
    "open": {"in_progress"},
    "in_progress": {"resolved", "open"},
    "resolved": {"open"},
}


def _find_ticket(tickets, ticket_id):
    if not isinstance(tickets, list):
        raise ValueError("Tickets must be a list.")

    for ticket in tickets:
        if isinstance(ticket, dict) and ticket.get("id") == ticket_id:
            return ticket

    raise ValueError(f"Ticket {ticket_id} was not found.")


def assign_ticket(tickets, ticket_id, staff_name):
    if not isinstance(staff_name, str):
        raise ValueError("Staff name must be a string.")

    staff_name = validate_staff_name(staff_name)
    ticket = _find_ticket(tickets, ticket_id)

    if ticket.get("status") == "resolved":
        raise ValueError("Cannot assign a resolved ticket.")

    ticket["assigned_to"] = staff_name
    return ticket


def update_ticket_status(tickets, ticket_id, new_status):
    new_status = validate_status(new_status)
    ticket = _find_ticket(tickets, ticket_id)
    current_status = ticket.get("status")

    if current_status not in ALLOWED_TRANSITIONS:
        raise ValueError("Ticket has an invalid current status.")

    if new_status not in ALLOWED_TRANSITIONS[current_status]:
        raise ValueError(
            f"Cannot change status from {current_status} to {new_status}."
        )

    if new_status == "in_progress" and not ticket.get("assigned_to"):
        raise ValueError("Assign the ticket before starting work.")

    ticket["status"] = new_status
    return ticket
