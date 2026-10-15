
"""JSON persistence for CampusFlow tickets."""

import json
import os
import tempfile

from campusflow.validation import validate_ticket_data


def validate_tickets(tickets):
    if not isinstance(tickets, list):
        raise ValueError("Stored tickets must be a list.")

    seen_ids = set()

    for ticket in tickets:
        validate_ticket_data(ticket)

        if ticket["id"] in seen_ids:
            raise ValueError(f"Duplicate ticket ID: {ticket['id']}")

        seen_ids.add(ticket["id"])

        if not isinstance(ticket.get("notes", []), list):
            raise ValueError("Ticket notes must be a list.")

    return True


def save_tickets(tickets, filepath="data/tickets.json"):
    validate_tickets(tickets)

    directory = os.path.dirname(os.path.abspath(filepath))
    os.makedirs(directory, exist_ok=True)

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=directory,
            delete=False,
        ) as file:
            temp_path = file.name
            json.dump(tickets, file, indent=4, ensure_ascii=False)
            file.write("\n")

        os.replace(temp_path, filepath)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def load_tickets(filepath="data/tickets.json"):
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError("The ticket JSON file is invalid.") from error

    validate_tickets(tickets)
    return tickets
