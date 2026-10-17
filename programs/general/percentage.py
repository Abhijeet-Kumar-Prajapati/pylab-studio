"""
Percentage
Category: Math/Number

Calculates a value as a percentage of a whole.

Example:
    20 of 80 = 25%
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
    part = ask_number("Part value: ", "float")
    whole = ask_number("Whole value: ", "float")

    if whole == 0:
        print("Error: whole value cannot be zero.")
    else:
        print(f"{part} is {part / whole * 100:.2f}% of {whole}")


if __name__ == "__main__":
    main()
