"""
Quadratic Solver
Category: Math/Number

Solves ax^2 + bx + c = 0.

Example:
    x^2 - 5x + 6 -> 2, 3
"""

import cmath


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
    a = ask_number("a: ", "float")
    b = ask_number("b: ", "float")
    c = ask_number("c: ", "float")

    if a == 0:
        print("Error: a cannot be zero.")
    else:
        d = b * b - 4 * a * c
        x1 = (-b + cmath.sqrt(d)) / (2 * a)
        x2 = (-b - cmath.sqrt(d)) / (2 * a)
        print(f"Roots: {x1} and {x2}")


if __name__ == "__main__":
    main()
