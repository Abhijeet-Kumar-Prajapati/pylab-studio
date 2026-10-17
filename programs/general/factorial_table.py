"""
Factorial Table
Category: Loops/Pattern

Prints factorials from 1 to N.

Example:
    1! 2! 3!
"""

import math


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
    n = ask_number("N (1-15): ", "int")

    if n > 15:
        print("Please enter 15 or less.")
    else:
        for i in range(1, n + 1):
            print(f"{i}! = {math.factorial(i)}")


if __name__ == "__main__":
    main()
