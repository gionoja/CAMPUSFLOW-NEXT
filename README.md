# CampusFlow

## 1. Project Overview

CampusFlow is a command-line helpdesk ticket management system
built with Python.

It helps campus staff record, organize, track, and resolve
technical problems reported by students and staff.

Examples of problems include:
- Wi-Fi and network failures.
- Faulty laptops and hardware.
- Software problems.
- Other campus technical issues.

## 2. Project Objectives

The objectives of CampusFlow are to:

- Create and manage helpdesk tickets.
- Calculate ticket priority automatically.
- Assign tickets to staff members.
- Track ticket status from open to resolved.
- Reopen resolved tickets when necessary.
- Add and view notes on tickets.
- Search and filter tickets.
- Generate reports about tickets.
- Save ticket data using JSON.
- Test the application using automated tests.

## 3. Technologies Used

- Python
- JSON for data persistence
- Python unittest for automated testing
- Git and GitHub for version control and collaboration

## 4. Main Features

### Ticket Management

Users can create tickets with a title, category, urgency,
and number of affected users.

Each ticket receives a unique ID.

### Automatic Priority Calculation

CampusFlow calculates priority using the following rules:

- Critical: High urgency and at least 10 affected users.
- High: High urgency or at least 10 affected users.
- Medium: Medium urgency or at least 3 affected users.
- Low: All other valid tickets.

### Assignment and Status Management

Tickets can be assigned to staff members.

The normal workflow is:

open -> in_progress -> resolved

Resolved tickets can be reopened and returned to the open status.

### Notes

Users can add notes to tickets and view existing notes.

Resolved tickets must be reopened before new notes can be added.

### Search and Filtering

Users can search tickets by title and filter results by
category, status, and priority.

When multiple filters are supplied, all filters must match.

Users can also choose to sort search results by priority.

### Ticket Queues

CampusFlow provides two ticket queues:

- Unresolved queue: Displays open and in-progress tickets.
- Open-work queue: Displays only open tickets waiting for work.

Tickets are sorted by priority, with higher-priority tickets first.

### Reports

CampusFlow generates reports showing ticket totals,
statuses, priorities, categories, and resolution statistics.

### Data Persistence

Tickets are stored in JSON so that data can be loaded again
when the application restarts.

Ticket data is validated before it is saved or loaded.

If saved data is invalid, the application reports the problem
instead of automatically replacing the saved file.

### Understanding Check

The application includes a six-question quiz that checks
the user's understanding of CampusFlow.

The quiz displays the user's score after completion.

Quiz results are not saved to a file.

## 5. Project Structure

campusflow/
    __init__.py
    tickets.py
    validation.py
    workflow.py
    notes.py
    storage.py
    search.py
    reports.py
    understanding_check.py

tests/
    test_tickets.py
    test_validation.py
    test_workflow.py
    test_notes.py
    test_storage.py
    test_search.py
    test_reports.py
    test_understanding_check.py

data/
    tickets.json

docs/
    baseline-check.md
    ai-learning-log.md
    design-decisions.md

main.py
README.md

## 6. Requirements

- Python 3
- A terminal or command-line application
- Git for version control and collaboration

The application uses Python's standard library for its core
functionality.

No external Python packages are required.

## 7. How to Run CampusFlow

Open a terminal in the project directory.

Run:

python3 main.py

## 8. How to Run the Tests

Run the complete test suite with:

python3 -m unittest discover -s tests -v

The tests check ticket creation, validation, workflow rules,
notes, storage, search, reports, and the understanding check.

## 9. Data Storage

CampusFlow uses JSON to store ticket information.

The ticket data file is:

data/tickets.json

This file allows tickets to be loaded again when the application
restarts.

The application creates the data directory when saving tickets
if the directory does not already exist.

The understanding quiz does not save quiz scores or learning notes.

## 10. Team Responsibilities

### Engineer A: Ticket Safety and Storage

Responsible for validation, ticket workflow protections,
note business logic, JSON storage, and ID continuity.

### Engineer B: Search, Reports, and CLI

Responsible for search and filtering, reports, CLI interaction,
the understanding check, and related tests.

Both engineers contribute to testing, documentation,
code review, and verification of AI suggestions.

## 11. Testing and Quality

The project uses automated tests to verify expected behavior.

Invalid operations should produce helpful errors without
leaving ticket data partially changed.

Test results should be recorded accurately and updated
when the code changes.

## 12. Learning and Documentation

The docs directory contains:

- baseline-check.md: Records the original project test results.
- ai-learning-log.md: Records AI-assisted learning and verification.
- design-decisions.md: Explains important technical decisions.

These documents support the team's learning, collaboration,
and engineering decisions.

## 13. Project Status

CampusFlow is being developed collaboratively as part of
an AI-Native Engineering Sprint.

Features and documentation should be verified against the
current implementation before the project is submitted.