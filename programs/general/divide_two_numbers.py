"""
Divide Two Numbers
Category: Math/Number

Divides the first number by the second.

Example:
    10 / 2 = 5
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
    a = ask_number("Dividend: ", "float")
    b = ask_number("Divisor: ", "float")

    if b == 0:
        print("Error: cannot divide by zero.")
    else:
        print(f"Result: {a} / {b} = {a / b}")


if __name__ == "__main__":
    main()
