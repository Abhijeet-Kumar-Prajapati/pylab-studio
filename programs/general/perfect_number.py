"""
Perfect Number
Category: Math/Number

Checks if a number is a perfect number.

Example:
    28 -> yes
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
    n = ask_number("Number: ", "int")

    if n <= 1:
        print(f"{n} is not a perfect number")
    else:
        total = sum(i for i in range(1, n) if n % i == 0)
        print(f"{n} is", "perfect" if total == n else "not perfect")


if __name__ == "__main__":
    main()
