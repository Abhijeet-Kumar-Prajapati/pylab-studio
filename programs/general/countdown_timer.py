"""
Countdown Timer
Category: Utility

Counts down and shows time remaining.

Example:
    10 -> 0
"""

import time


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
    seconds = ask_number("Seconds (1-3600): ", "int")

    for remaining in range(seconds, 0, -1):
        print(f"\rTime left: {remaining:>4d}s", end="", flush=True)
        time.sleep(1)
    print("\rTime is up!        ")


if __name__ == "__main__":
    main()
