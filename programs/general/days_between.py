"""
Days Between
Category: Utility

Counts days between two dates.

Example:
    2024-01-01 to 2024-01-10
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
    d1 = ask_text("First date (YYYY-MM-DD): ")
    d2 = ask_text("Second date (YYYY-MM-DD): ")

    try:
        start = datetime.date.fromisoformat(d1)
        end = datetime.date.fromisoformat(d2)
        print("Days between:", abs((end - start).days))
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")


if __name__ == "__main__":
    main()
