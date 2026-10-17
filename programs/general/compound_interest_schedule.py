"""
Compound Interest Schedule
Category: Finance

Compound interest with growth summary.

Example:
    shows yearly growth
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
    p = ask_number("Principal: ", "float")
    r = ask_number("Rate %: ", "float")
    t = ask_number("Time (years): ", "int")

    for year in range(1, t + 1):
        amount = p * (1 + r / 100) ** year
        print(f"Year {year}: {amount:.2f}")


if __name__ == "__main__":
    main()
