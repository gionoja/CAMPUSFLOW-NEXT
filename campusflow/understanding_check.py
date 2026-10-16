"""Run a quiz and collect questions for the CampusFlow mentor."""


# Store all quiz questions, answer options, and correct answers.
# Keeping the questions here makes them easier to update without
# changing the code that calculates the user's score.
QUESTIONS = [
    {
        "question": "1. What is CampusFlow used for?",
        "options": {
            "A": "Managing campus helpdesk tickets",
            "B": "Playing games",
            "C": "Editing pictures",
            "D": "Sending social media messages",
        },
        # The letter representing the correct answer.
        "answer": "A",
    },
    {
        "question": "2. What does a ticket's priority describe?",
        "options": {
            "A": "Who created the ticket",
            "B": "How urgently the ticket should be handled",
            "C": "The ticket's file name",
            "D": "The staff member's age",
        },
        "answer": "B",
    },
    {
        "question": "3. Which status means work is currently happening?",
        "options": {
            "A": "resolved",
            "B": "closed",
            "C": "in_progress",
            "D": "deleted",
        },
        "answer": "C",
    },
    {
        "question": "4. Why does CampusFlow use JSON storage?",
        "options": {
            "A": "To permanently delete tickets",
            "B": "To save ticket data between program runs",
            "C": "To create computer hardware",
            "D": "To replace Python",
        },
        "answer": "B",
    },
    {
        "question": (
            "5. What should happen if someone tries to resolve "
            "an open ticket directly?"
        ),
        "options": {
            "A": "The ticket should be resolved immediately",
            "B": "The ticket should be deleted",
            "C": "The workflow should reject the invalid transition",
            "D": "All tickets should be reset",
        },
        "answer": "C",
    },
    {
        "question": "6. Why do we write automated tests?",
        "options": {
            "A": "To check that our code behaves as expected",
            "B": "To make every function longer",
            "C": "To avoid running our program",
            "D": "To automatically write documentation",
        },
        "answer": "A",
    },
]


def ask_question(question_data, input_func=input, print_func=print):
    """Ask one question until the user enters a valid answer."""

    # Display the question to the user.
    # The newline creates some space before the question.
    print_func("\n" + question_data["question"])

    # Loop through the dictionary containing the answer options.
    # 'letter' receives A, B, C, or D.
    # 'option' receives the text associated with that letter.
    for letter, option in question_data["options"].items():
        print_func(f"{letter}. {option}")

    # Keep asking until the user enters a valid answer.
    while True:
        # Read the user's answer, remove surrounding spaces,
        # and convert the answer to uppercase.
        answer = input_func("Your answer (A-D): ").strip().upper()

        # Check whether the answer exists among the available options.
        if answer in question_data["options"]:
            # Return the valid answer to the function that called us.
            return answer

        # Tell the user the answer was invalid and ask again.
        print_func("Invalid answer. Please enter A, B, C, or D.")


def tell_mentor_your_answer(input_func=input, print_func=print):
    """Collect two questions the user wants to discuss with a mentor."""

    # Create an empty list to hold the user's responses.
    # The responses stay in memory and are not saved to a file.
    your_answer = []

    # Display instructions explaining what the user should provide.
    print_func("\n=== Explain Your Answers ===")
    print_func(
        "Explain in your own words why at least TWO of your quiz "
        "answers are correct."
    )

    # Repeat the input process twice to collect two responses.
    for number in range(1, 3):

        # Keep asking until the user enters a nonempty response.
        while True:
            # Collect the user's response and remove surrounding spaces.
            question = input_func(
                f"\nMentor question {number}: "
            ).strip()

            # Only accept a response containing something other than spaces.
            if question:
                # Add the response to the list.
                your_answer.append(question)

                # Stop asking for this response and move to the next one.
                break

            # Explain why the response was rejected.
            print_func(
                "Your question cannot be empty. Please try again."
            )

    # Return the list containing the two responses.
    return your_answer


def run_quiz(
    input_func=input,
    print_func=print,
    collect_mentor_questions=True,
):
    """Run the quiz without saving user data to a file."""

    # Start the score at zero before the quiz begins.
    score = 0

    # Store questions the user answers incorrectly.
    # These will be used for the review section.
    incorrect_questions = []

    # Display the quiz heading.
    print_func("\n=== CampusFlow Understanding Check ===")

    # Go through every question stored in the QUESTIONS list.
    for question_data in QUESTIONS:

        # Display the current question and collect a valid answer.
        # The returned answer is stored in the 'answer' variable.
        answer = ask_question(
            question_data,
            input_func,
            print_func,
        )

        # Compare the user's answer with the correct answer.
        if answer == question_data["answer"]:

            # Inform the user that their answer is correct.
            print_func("Correct!")

            # Increase the score by one for a correct answer.
            score += 1

        else:
            # Get the correct answer's letter.
            correct_answer = question_data["answer"]

            # Get the full text associated with the correct letter.
            correct_option = question_data["options"][correct_answer]

            # Display the correct answer to help the user learn.
            print_func(
                f"Not quite. Correct answer: "
                f"{correct_answer}. {correct_option}"
            )

            # Add the incorrectly answered question to the review list.
            incorrect_questions.append(question_data)

    # Display the final score.
    # len(QUESTIONS) returns the total number of quiz questions.
    print_func(f"\nYour final score: {score}/{len(QUESTIONS)}")

    # Begin the section that helps the user review their answers.
    print_func("\n=== Review and Learn ===")

    # Select up to two incorrectly answered questions.
    # [:2] takes the first two items from the list.
    questions_to_review = incorrect_questions[:2]

    # If the user answered fewer than two questions incorrectly,
    # add other questions so the review can contain two questions.
    if len(questions_to_review) < 2:

        # Examine all quiz questions to find additional review questions.
        for question_data in QUESTIONS:

            # Do not add a question that is already in the review list.
            if question_data not in questions_to_review:
                questions_to_review.append(question_data)

            # Stop once the review list contains two questions.
            if len(questions_to_review) == 2:
                break

    # Display the correct answers for the selected review questions.
    for question_data in questions_to_review:

        # Get the correct answer's letter.
        correct_answer = question_data["answer"]

        # Get the full text of the correct answer.
        correct_option = question_data["options"][correct_answer]

        # Display the question being reviewed.
        print_func(f"\n{question_data['question']}")

        # Display its correct answer.
        print_func(
            f"Correct answer: {correct_answer}. {correct_option}"
        )

    # Allow automated tests to skip the mentor-question section.
    # This is useful because tests should not wait for manual input.
    if not collect_mentor_questions:
        return score

    # Collect two responses for the mentor using the separate function.
    your_answer = tell_mentor_your_answer(
        input_func,
        print_func,
    )

    # Display a heading before showing the collected responses.
    print_func("\n=== Your Mentor Responses ===")

    # enumerate() provides a number and response for each list item.
    # start=1 makes the numbering begin at 1 instead of 0.
    for number, question in enumerate(your_answer, start=1):

        # Display each response with its number.
        print_func(f"{number}. {question}")

    # Inform the user that the quiz results have not been saved.
    print_func("\nYour results have not been saved.")

    # Return the final score to whoever called run_quiz().
    return score


# Check whether this file is being run directly.
# If it is, start the quiz.
# If another Python file imports this module, the quiz will not
# automatically start just because it was imported.
if __name__ == "__main__":
    run_quiz()