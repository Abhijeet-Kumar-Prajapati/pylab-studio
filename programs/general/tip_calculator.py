"""
Tip Calculator
Category: Utility

Splits a bill with tip between people.

Example:
    100 tip 15% split 2
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
    bill = ask_number("Bill amount: ", "float", "1000")
    tip = ask_number("Tip %: ", "float", "15")
    people = ask_number("Split among: ", "int", "2")

    tip_amount = bill * tip / 100
    total = bill + tip_amount
    print(f"Tip: {tip_amount:.2f}")
    print(f"Total: {total:.2f}")
    print(f"Per person: {total / max(people, 1):.2f}")


if __name__ == "__main__":
    main()
