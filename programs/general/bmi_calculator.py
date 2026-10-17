"""
BMI Calculator
Category: Health

Calculates Body Mass Index and category.

Example:
    70kg 1.75m -> 22.9
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
    h = ask_number("Height (m): ", "float")

    if h <= 0:
        print("Height must be greater than zero.")
    else:
        bmi = w / (h * h)
        if bmi < 18.5: cat = "Underweight"
        elif bmi < 25: cat = "Normal"
        elif bmi < 30: cat = "Overweight"
        else: cat = "Obese"
        print(f"BMI = {bmi:.2f} ({cat})")


if __name__ == "__main__":
    main()
