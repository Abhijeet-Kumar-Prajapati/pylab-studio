"""
Average
Category: Math/Number

Calculates the average of a list of numbers.

Example:
    avg of 2,4,6 = 4
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
    raw = ask_text("Numbers (space separated): ")
    nums = [float(x) for x in raw.replace(",", " ").split()]

    print(f"Average of {len(nums)} numbers = {sum(nums) / len(nums):.4f}")


if __name__ == "__main__":
    main()
