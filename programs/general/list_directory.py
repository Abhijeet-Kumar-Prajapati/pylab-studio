"""
List Directory
Category: Utility

Lists files in a directory.

Example:
    shows files
"""

import os


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
    path = ask_text("Directory (empty = current): ")

    target = path or "."
    try:
        for name in sorted(os.listdir(target)):
            tag = "[DIR] " if os.path.isdir(os.path.join(target, name)) else "[FILE]"
            print(f"{tag} {name}")
    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
