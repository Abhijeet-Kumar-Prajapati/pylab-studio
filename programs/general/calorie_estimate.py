"""
Calorie Estimate
Category: Health

Estimates daily calories (BMR).

Example:
    M 70kg 175cm 30
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
    w = ask_number("Weight (kg): ", "float")
    h = ask_number("Height (cm): ", "float")
    a = ask_number("Age: ", "int")
    g = ask_text("Gender (m/f): ")

    bmr = 10 * w + 6.25 * h - 5 * a + (5 if g.lower().startswith("m") else -161)
    print(f"Estimated BMR = {bmr:.0f} kcal/day")


if __name__ == "__main__":
    main()
