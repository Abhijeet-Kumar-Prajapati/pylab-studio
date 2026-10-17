"""
Age Calculator
Category: Utility

Calculates age from a birth date.

Example:
    born 2005 -> age
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
    y = ask_number("Birth year: ", "int")
    m = ask_number("Birth month (1-12): ", "int")
    d = ask_number("Birth day (1-31): ", "int")

    try:
        birth = datetime.date(y, m, d)
    except ValueError:
        print("That date does not exist.")
    else:
        today = datetime.date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        print(f"Age: {age} years")
        print(f"Next birthday in: {(birth.replace(year=today.year) - today).days} days")


if __name__ == "__main__":
    main()
