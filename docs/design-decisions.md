# Design Decisions — CampusFlow Next

## 1. Overviewai-learning-log.md

CampusFlow Next is an improvement of our original CampusFlow command-line application. The goal is to make the existing system more reliable and easier to maintain without changing the basic technologies used in the project.

We decided to keep using Python, dictionaries, lists, JSON files and the unittest module. We did not introduce a database or any external framework because the project requirements focus on understanding Python fundamentals and software reliability.

## 2. Keeping the Existing Ticket Structure

We kept the original ticket fields instead of creating a completely new ticket format. These include the ticket ID, title, category, urgency, affected users, priority, status and assigned staff.

We added a `notes` field to each ticket. It starts as an empty list and stores follow-up notes as dictionaries containing a note ID, author and message.

This approach allows us to add the new features without losing the existing ticket information.

## 3. Centralized Validation

We decided to keep common validation rules in one place so that different parts of the application follow the same rules.

For example, ticket categories must be Network, Hardware, Software or Other. Urgency must be low, medium or high, and affected users must be a positive integer.

We also reject boolean values for affected users because Python treats `bool` as a subclass of `int`. Without checking the type carefully, `True` could accidentally be accepted as the number 1.

Centralizing validation makes it easier to test the rules and reduces the chance of different modules behaving differently.

## 4. Safe Ticket Updates

We want invalid actions to fail without partially changing a ticket.

For example, an unassigned ticket should not move from open to in_progress. A resolved ticket should not accept a new note or an assignment change until it has been reopened through the permitted workflow.

Our approach is to validate the requested action before applying the change. We test both the expected error and whether the ticket data remains unchanged after a rejected action.

## 5. Search and Filtering

Search is designed to read ticket information without modifying it. Title searches ignore capitalization and use substring matching.

When the user supplies multiple filters, such as category and status, every supplied filter must match. We chose this AND-based behaviour because it gives more precise results.

We also keep the original Open Work Queue separate from the search feature. The original queue must continue to show only open tickets in the required priority order.

## 6. Reports

Reports calculate totals, counts by status, priority and category, unresolved tickets, resolved tickets and the resolution percentage.

An empty ticket collection should produce a resolution percentage of 0% instead of causing a division-by-zero error.

We also ensure that a reopened ticket is counted according to its current status.

## 7. JSON Storage

We kept JSON because it is part of the original project and does not require an external database.

When loading data, the application should validate the decoded records before replacing the existing ticket collection. If the file contains invalid data or duplicate ticket IDs, the load should fail without destroying the valid data already in memory.

Ticket notes must also be saved and loaded so that their IDs can continue correctly after restarting the application.

## 8. Testing Decisions

We use Python's unittest module to check both valid and invalid inputs. We include tests for normal behaviour, boundary values and rejected operations.

We do not consider a feature complete just because it works with one example. We also check what happens when users provide invalid input or when stored data is damaged.

## 9. Known Limitations

CampusFlow Next is a command-line learning project. It is not designed as a production campus support platform, and it does not include a database, web interface or authentication system.

Any remaining failing tests or incomplete requirements will be documented rather than treated as completed work.

## 10. Future Improvements

If the project is extended, we would first improve test coverage, simplify any duplicated logic and verify that a fresh clone can run the application and its tests using the documented commands.
