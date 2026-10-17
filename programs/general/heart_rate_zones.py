"""
Heart Rate Zones
Category: Health

Shows target heart-rate zones.

Example:
    age 30 -> zones
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
    age = ask_number("Age: ", "int")

    max_hr = 220 - age
    print(f"Maximum heart rate: {max_hr} bpm")
    print(f"Moderate zone: {max_hr * 0.5:.0f} - {max_hr * 0.7:.0f} bpm")
    print(f"Vigorous zone: {max_hr * 0.7:.0f} - {max_hr * 0.85:.0f} bpm")


if __name__ == "__main__":
    main()
