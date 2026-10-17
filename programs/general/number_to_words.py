"""
Number To Words
Category: String/Text

Converts a number (0-999999) into words.

Example:
    123 -> one hundred twenty three
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
    n = ask_number("Number (0-999999): ", "int")

    ones = ["zero","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
    tens = ["","","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"]
    def under_1000(v):
        parts = []
        if v >= 100:
            parts.append(ones[v // 100] + " hundred")
            v %= 100
        if v >= 20:
            parts.append(tens[v // 10] + (" " + ones[v % 10] if v % 10 else ""))
        elif v > 0:
            parts.append(ones[v])
        return " ".join(parts) or "zero"
    if not 0 <= n <= 999999:
        print("Please enter a number between 0 and 999999.")
    else:
        print(f"{n} = {under_1000(n // 1000) + " thousand " + under_1000(n % 1000)}".strip())


if __name__ == "__main__":
    main()
