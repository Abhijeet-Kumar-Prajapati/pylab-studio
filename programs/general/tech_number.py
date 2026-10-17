"""
Tech Number
Category: Math/Number

Checks if a number is a Tech number.

Example:
    3025 -> yes
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

    s = str(n)
    h = len(s) // 2
    if len(s) % 2 or h == 0:
        print(f"{n} is not a Tech number")
    else:
        total = int(s[:h]) + int(s[h:])
        print(f"{n} is", "a Tech number" if total * total == n else "not a Tech number")


if __name__ == "__main__":
    main()
