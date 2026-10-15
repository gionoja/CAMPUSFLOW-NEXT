
"""Safe ticket note creation and retrieval."""

from campusflow.validation import validate_note
from campusflow.workflow import _find_ticket


def add_note(tickets, ticket_id, author, message):
    ticket = _find_ticket(tickets, ticket_id)
    note_data = validate_note(author, message)

    note = {
        "author": note_data["author"],
        "message": note_data["message"],
    }

    if "notes" not in ticket:
        ticket["notes"] = []

    if not isinstance(ticket["notes"], list):
        raise ValueError("Ticket notes must be a list.")

    ticket["notes"].append(note)
    return note


def get_notes(tickets, ticket_id):
    ticket = _find_ticket(tickets, ticket_id)
    notes = ticket.get("notes", [])

    if not isinstance(notes, list):
        raise ValueError("Ticket notes must be a list.")

    return [note.copy() if isinstance(note, dict) else note for note in notes]
