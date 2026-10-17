"""
Rock Paper Scissors
Category: Game

Play rock, paper, scissors.

Example:
    win/lose/draw
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

    choices = ["rock", "paper", "scissors"]
    wins = losses = draws = 0
    while True:
        user = ask_text("Your choice (rock/paper/scissors, q to quit): ").lower()
        if user == "q":
            break
        if user not in choices:
            print("Invalid choice.")
            continue
        comp = random.choice(choices)
        print("Computer chose:", comp)
        beats = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
        if user == comp:
            draws += 1
            print("Draw!")
        elif beats[user] == comp:
            wins += 1
            print("You win!")
        else:
            losses += 1
            print("You lose!")
    print(f"Final score -> wins {wins}, losses {losses}, draws {draws}")


if __name__ == "__main__":
    main()
