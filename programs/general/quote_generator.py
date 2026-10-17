"""
Quote Generator
Category: Utility

Prints random motivational quotes.

Example:
    inspiration
"""

import random


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
    count = ask_number("How many quotes (1-10): ", "int", "3")

    quotes = [
        "Simplicity is the soul of efficiency. - Austin Freeman",
        "First, solve the problem. Then write the code. - John Johnson",
        "Experience is the name everyone gives to their mistakes. - Oscar Wilde",
        "Talk is cheap. Show me the code. - Linus Torvalds",
        "Stay hungry, stay foolish. - Steve Jobs",
        "Knowledge is power. - Francis Bacon",
        "Code is like humor. When you have to explain it, it is bad. - Cory House",
    ]
    for _ in range(min(count, len(quotes))):
        print(" -", random.choice(quotes))


if __name__ == "__main__":
    main()
