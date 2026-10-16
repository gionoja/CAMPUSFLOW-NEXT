"""Handles staff assignment, ticket status changes, and ticket queues."""

# Import the allowed ticket priorities and statuses.
# These constants help us check whether a value is valid.
from campusflow.validation import (
    VALID_PRIORITIES,
    VALID_STATUSES,
    validate_staff_name,
)


def find_ticket(tickets, ticket_id):
    """Find a ticket by ID or raise an error if it does not exist."""

    # Go through every ticket in the collection.
    for ticket in tickets:

        # Compare the current ticket's ID with the requested ID.
        if ticket["id"] == ticket_id:

            # Return the ticket immediately when a match is found.
            return ticket

    # If the loop finishes without finding a match, raise an error.
    raise ValueError(f"Ticket {ticket_id} was not found.")


def assign_staff(tickets, ticket_id, staff_name):
    """Assign staff to an open or in-progress ticket."""

    # Validate the staff name before changing the ticket.
    # This also removes unnecessary spaces from the name.
    staff_name = validate_staff_name(staff_name)

    # Find the ticket that should receive the staff assignment.
    ticket = find_ticket(tickets, ticket_id)

    # Prevent staff from being assigned to a resolved ticket.
    # The ticket must be reopened before staff can be assigned.
    if ticket["status"] == "resolved":
        raise ValueError("Reopen the ticket before assigning staff.")

    # Save the staff member's name in the ticket.
    ticket["assigned_to"] = staff_name

    # If the ticket was open, move it to in_progress.
    # This indicates that work on the ticket has started.
    if ticket["status"] == "open":
        ticket["status"] = "in_progress"

    # Return the updated ticket.
    return ticket


def update_status(tickets, ticket_id, new_status):
    """Change a ticket's status while enforcing workflow rules."""

    # Ensure the new status is text before processing it.
    if not isinstance(new_status, str):
        raise ValueError("Status must be text.")

    # Remove surrounding spaces and convert the status to lowercase.
    # For example, " OPEN " becomes "open".
    new_status = new_status.strip().lower()

    # Reject statuses that are not in the approved status collection.
    if new_status not in VALID_STATUSES:
        raise ValueError("Status must be open, in_progress, or resolved.")

    # Find the ticket whose status we want to change.
    ticket = find_ticket(tickets, ticket_id)

    # Store the ticket's current status for the workflow checks.
    current_status = ticket["status"]

    # Reject a request to change the status to its existing value.
    if current_status == new_status:
        raise ValueError("The ticket already has this status.")

    # A resolved ticket can only be reopened.
    # It cannot move directly to in_progress or remain resolved.
    if current_status == "resolved":

        # Allow the resolved ticket to return to the open state.
        if new_status == "open":
            ticket["status"] = "open"

            # Return the ticket after successfully reopening it.
            return ticket

        # Reject any other status change from resolved.
        raise ValueError("Reopen the ticket before changing its status.")

    # A ticket can move to in_progress only from the open state.
    if new_status == "in_progress":

        # Prevent tickets in other states from starting work.
        if current_status != "open":
            raise ValueError("Only open tickets can start work.")

        # Check that a staff member has been assigned.
        # ticket.get() safely returns None if the key is missing.
        if not ticket.get("assigned_to"):
            raise ValueError(
                "Assign a staff member before starting the ticket."
            )

    # A ticket must be in progress before it can be resolved.
    if new_status == "resolved" and current_status != "in_progress":
        raise ValueError("Only in-progress tickets can be resolved.")

    # All workflow checks passed, so update the ticket's status.
    ticket["status"] = new_status

    # Return the updated ticket to the caller.
    return ticket


def _priority_sort_key(ticket):
    """Sort by priority first, then by numeric ticket ID."""

    # Assign a numeric ranking to each priority.
    # Lower numbers represent more urgent tickets.
    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    # Read the current ticket's priority.
    priority = ticket["priority"]

    # Reject priorities that are not in the ranking dictionary.
    if priority not in priority_order:
        raise ValueError(f"Invalid ticket priority: {priority}")

    # Return a tuple containing:
    # 1. The priority ranking.
    # 2. The numeric part of the ticket ID.
    #
    # Python sorts by the first value, then uses the second
    # value when two tickets have the same priority.
    #
    # Example: ("critical", T003) is ranked before ("high", T001).
    return priority_order[priority], int(ticket["id"][1:])


def get_unresolved_queue(tickets):
    """Return open and in-progress tickets in priority order."""

    # Build a new list containing only tickets that still need work.
    # Resolved tickets are excluded.
    unresolved_tickets = [
        ticket
        for ticket in tickets
        if ticket["status"] in ("open", "in_progress")
    ]

    # Sort the filtered tickets by priority and then ticket ID.
    # The original tickets collection is not reordered.
    return sorted(unresolved_tickets, key=_priority_sort_key)


def get_open_work_queue(tickets):
    """Return only open tickets in priority order."""

    # Build a new list containing tickets whose status is open.
    open_tickets = [
        ticket
        for ticket in tickets
        if ticket["status"] == "open"
    ]

    # Return the open tickets sorted by priority and ticket ID.
    return sorted(open_tickets, key=_priority_sort_key)