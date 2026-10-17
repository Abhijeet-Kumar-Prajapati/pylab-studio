"""
Profit Loss
Category: Finance

Shows profit or loss percentage.

Example:
    buy 100 sell 120 -> 20% profit
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
    cp = ask_number("Cost price: ", "float")
    sp = ask_number("Selling price: ", "float")

    if cp == 0:
        print("Cost price cannot be zero.")
    else:
        diff = sp - cp
        pct = diff / cp * 100
        label = "Profit" if diff >= 0 else "Loss"
        print(f"{label}: {abs(diff):.2f} ({abs(pct):.2f}%)")


if __name__ == "__main__":
    main()
