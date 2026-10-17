"""
Lcm Two
Category: Math/Number

Finds the least common multiple of two numbers.

Example:
    lcm(4,6) = 12
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
    a = ask_number("First number: ", "int")
    b = ask_number("Second number: ", "int")

    g = math.gcd(a, b)
    lcm = abs(a * b) // g if g else 0
    print(f"LCM({a}, {b}) = {lcm}")


if __name__ == "__main__":
    main()
