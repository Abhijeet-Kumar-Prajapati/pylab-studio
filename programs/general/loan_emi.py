"""
Loan EMI
Category: Finance

Loan EMI with total interest breakdown.

Example:
    shows interest
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
    p = ask_number("Loan amount: ", "float", "500000")
    r = ask_number("Annual rate %: ", "float", "8")
    n = ask_number("Months: ", "int", "240")

    rate = r / 1200
    emi = p * rate * (1 + rate) ** n / ((1 + rate) ** n - 1) if rate else p / n
    interest = emi * n - p
    print(f"EMI = {emi:.2f}")
    print(f"Total interest = {interest:.2f}")
    print(f"Total payment = {emi * n:.2f}")


if __name__ == "__main__":
    main()
