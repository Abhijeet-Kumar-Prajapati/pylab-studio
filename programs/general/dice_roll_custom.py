"""
Dice Roll Custom
Category: Game

Rolls custom dice with N sides.

Example:
    d100
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
    sides = ask_number("Sides per die: ", "int")
    count = ask_number("Number of dice: ", "int")

    rolls = [random.randint(1, sides) for _ in range(count)]
    print("Rolls:", rolls)
    print("Total:", sum(rolls))


if __name__ == "__main__":
    main()
