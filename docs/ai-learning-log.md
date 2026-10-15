# AI Learning Log — CampusFlow Next

## Purpose

This document records how I used AI to understand programming concepts and investigate problems during CampusFlow Next development.

I used AI as a learning and debugging tool, not as a replacement for writing tests, reading my code or making engineering decisions. The entries below should reflect the questions I actually asked and the experiments I actually performed.

## Learning Cycle 1: Understanding Validation

### What I was confused about

I understood basic `if` statements, but I needed to understand how to validate data before allowing the program to change a ticket.

### Question asked

"Explain how to validate a dictionary before mutating it, using a simple example, and show how a failed validation can leave the original data unchanged."

### What I learned

I learned that validation should happen before the program makes changes to important data. If an operation fails halfway through, the ticket may end up in an inconsistent state.

I also learned that checking only whether a value exists is not enough. The program must check whether the value follows the actual business rules.

### How I checked the explanation

I examined the ticket-validation function and used unit tests to check invalid values, including an empty title and an invalid category.

### My decision

I decided to keep common validation rules in the validation module and test rejected inputs instead of relying only on successful ticket creation.

### What I still need to improve

I need more practice identifying every condition that should be checked before a function changes a dictionary.

---

## Learning Cycle 2: Investigating a Failed Test

### What happened

During testing, `test_reject_custom_category` failed. The test expected a `ValueError`, but the function did not raise one.

### Question asked

"Here is my failing unittest assertion. Help me identify possible causes without rewriting the entire function."

### What I learned

A failed test does not always mean the test itself is wrong. The function may be accepting an invalid value, the wrong helper may be responsible, or the code being executed may differ from the code I expected.

### How I investigated it

I used these commands:

```bash
grep -n -A35 "def validate_ticket" campusflow/tickets.py
grep -R -n "normalize_category" campusflow/
grep -n -A20 "def normalize_category" campusflow/validation.py
```

The investigation showed that `validate_ticket()` called `normalize_category()`, which was defined in `campusflow/validation.py`.

That helper accepted any non-empty custom category. This explained why the test rejected the behaviour even though the input was not empty.

### My decision

I identified the category-normalization helper as the place to enforce the four permitted categories. I then needed to rerun both the ticket tests and the full suite to check for regressions.

### What I learned from this mistake

I learned to follow a function call into the helper it uses instead of immediately replacing the whole function. This makes debugging more focused and reduces the risk of breaking working code.

---

## Learning Cycle 3: Understanding Boolean Values and Integers

### What I wanted to understand

I wanted to understand why a program might accidentally accept `True` as a valid number of affected users.

### Question asked

"Why does isinstance(True, int) return True in Python, and how can I validate a positive integer while rejecting booleans?"

### What I learned

In Python, `bool` is a subclass of `int`. This means a simple `isinstance(value, int)` check also accepts boolean values.

For a field such as `affected_users`, accepting `True` would not make sense because the user should provide an actual positive integer count.

### Small experiment

```python
print(isinstance(True, int))
print(type(True) is int)
```

Expected output:

```text
True
False
```

### My decision

For the affected-users field, I used an exact integer type check together with a positive-value check, so booleans, floats, strings, zero and negative values can be rejected.

### How I can verify it

I can use unit tests for `True`, `False`, `0`, `-1`, `2.5` and `"5"` to make sure the validation behaves as expected.

---

## Final Reflection

Before working on these improvements, I mainly focused on getting the program to produce the expected output. I now understand that dependable software also needs clear rules, safe updates, meaningful error handling and tests for invalid inputs.

One important lesson was that a failing test can point to a problem in a helper function rather than the function being tested directly.

I still need to improve my ability to inspect unfamiliar code, design edge-case tests and explain why an implementation is safe. My goal is to be able to defend my decisions and reproduce the results without depending on AI during the project demonstration.
