"""
Guess Number Game
Category: Game

Guess the secret number between 1-100.

Example:
    10 tries
"""

import random


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

    target = random.randint(1, 100)
    for attempt in range(1, 11):
        guess = ask_number(f"Guess {attempt}/10: ", "int")
        if guess == target:
            print(f"Correct! You won in {attempt} tries.")
            break
        print("Too high!" if guess > target else "Too low!")
    else:
        print(f"Out of tries. The number was {target}.")


if __name__ == "__main__":
    main()
