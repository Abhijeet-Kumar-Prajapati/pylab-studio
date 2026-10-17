"""
Trivia
Category: Game

Simple programming trivia quiz.

Example:
    score out of 5
"""


def ask_number(prompt, kind="float", default=None):
    """Keep asking until a valid number is entered.

    Pressing Enter accepts `default` when the spec provides one.
    """
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                if default is None:
                    continue
                return float(default) if kind == "float" else int(default)
            return float(value) if kind == "float" else int(value)
        except ValueError:
            print("  ! Please enter a valid number.")
        except (EOFError, KeyboardInterrupt):
            print()
            raise SystemExit


def ask_text(prompt, default=None):
    """Read a non-empty line of text.

    Pressing Enter accepts `default` when the spec provides one.
    """
    while True:
        try:
            value = input(prompt).strip()
            if value:
                return value
            if default is not None:
                return default
        except (EOFError, KeyboardInterrupt):
            print()
            raise SystemExit


def main():

    questions = {
        "Which keyword defines a function?": "def",
        "Which symbol starts a comment?": "#",
        "What is 2 ** 3?": "8",
        "Which keyword makes a class?": "class",
        "Which list method adds an item?": "append",
    }
    score = 0
    for question, answer in questions.items():
        reply = ask_text(question + " ").lower()
        if reply == answer.lower():
            score += 1
            print("  Correct!")
        else:
            print(f"  Wrong! Answer: {answer}")
    print(f"Final score: {score}/{len(questions)}")


if __name__ == "__main__":
    main()
