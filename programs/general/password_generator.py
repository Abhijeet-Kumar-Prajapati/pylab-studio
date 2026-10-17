"""
Password Generator
Category: Utility

Generates random secure passwords.

Example:
    strong passwords
"""

import random, string


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
    length = ask_number("Length (4-64): ", "int", "16")
    count = ask_number("How many (1-50): ", "int", "5")

    pool = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    for _ in range(count):
        print("".join(random.choice(pool) for _ in range(length)))


if __name__ == "__main__":
    main()
