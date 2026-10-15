# Baseline Check — CampusFlow

## 1. Purpose
This check was done to understand what worked in the original CampusFlow application and identify issues before making improvements. Issues were confirmed through tests or code inspection rather than assumed.

## 2. Environment
- Project: CampusFlow Next
- Language: Python
- Testing: `unittest`
- Storage: JSON
- OS: Linux
- Repository: [Insert GitHub URL]
- Baseline commit: [Insert commit SHA]

## 3. Commands Used
```bash
python3 -m unittest discover -s tests -v
```
I also inspected the code and tested the ticket workflow through the CLI.

## 4. Test Results
A later test run reported **71 tests: 70 passed and 1 failed**.

The failing test, `test_reject_custom_category`, showed that `validate_ticket()` accepted `Food` instead of raising a `ValueError`. Inspection revealed that `normalize_category()` allowed custom categories, which conflicts with the requirement to allow only Network, Hardware, Software and Other.

*Note: These results are from after development started, not necessarily from the original baseline commit.*

## 5. Manual Checks
The following checks should be recorded based on what was actually tested:

- **Valid category:** Create a Network ticket and check that it receives the correct priority.
- **Invalid category:** Try creating a ticket with the category `Food` and check that it is rejected.
- **Invalid affected users:** Enter `0` and check that the ticket is not created.

Record the actual results for the original version tested.

## 6. Areas for Improvement
- Validate categories and ticket updates consistently.
- Enforce note rules and ticket status restrictions.
- Handle corrupted JSON safely.
- Verify combined search filters and report calculations.
- Run the full test suite after integration.

## 7. Conclusion
Testing identified a category-validation issue that needed correction. After making changes, the relevant tests and the full test suite should be rerun on the integrated `main` branch.