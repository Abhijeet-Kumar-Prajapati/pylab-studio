"""
Day Of Week
Category: Utility

Prints the weekday of a date.

Example:
    2024-01-01 -> Monday
"""

import datetime


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
    y = ask_number("Year: ", "int")
    m = ask_number("Month (1-12): ", "int")
    d = ask_number("Day (1-31): ", "int")

    try:
        print("Weekday:", datetime.date(y, m, d).strftime("%A"))
    except ValueError:
        print("That date does not exist.")


if __name__ == "__main__":
    main()
