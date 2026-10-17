"""
Caesar Decrypt
Category: String/Text

Decrypts text with a Caesar cipher.

Example:
    bcd shift 1 -> abc
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
    s = ask_text("Text: ")
    k = ask_number("Shift (1-25): ", "int")

    def unshift(ch, k):
        if ch.islower():
            return chr((ord(ch) - 97 - k) % 26 + 97)
        if ch.isupper():
            return chr((ord(ch) - 65 - k) % 26 + 65)
        return ch
    k = k % 26
    print("Decrypted:", "".join(unshift(c, k) for c in s))


if __name__ == "__main__":
    main()
