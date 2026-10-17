"""Normalise docs/assets/demos.js against the current program slugs.

Idempotent: running it twice changes nothing the second time.

  1. retire the AI chatbot (demo function, CHAT replies, MIXED entry, sample)
  2. rename demo keys that still use the old program slugs
  3. add sample inputs for demos that have none (only the missing ones)
"""
import re
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else "docs/assets/demos.js"

RENAMES = {
    "coin_flip_game": "coin_flip",
    "coin_toss": "coin_tosses",
    "dice_roll": "dice_roll_d6",
    "dice_roller": "dice_roll_custom",
    "fibonacci_n": "fibonacci_inline",
    "random_password_plus": "quick_password",
    "temperature_converter_plus": "temperature_converter_extended",
    "compound_interest_plus": "compound_interest_schedule",
    "uuid_gen": "uuid_generator",
}

# Sample inputs for demos that have none. The runner splits on newlines, so a
# list of numbers has to be one value per line. "\n" is written as an escape.
NEW_SAMPLES = {
    "absolute": "-5", "area_rectangle": "4\n3", "area_triangle": "6\n4",
    "armstrong": "153", "automorphic": "25", "average": "2\n4\n6\n8",
    "ceil": "3.1", "celsius_to_fahrenheit": "100", "char_count": "hello",
    "cos_deg": "60", "decimal_to_binary": "10", "diamond": "4",
    "dice_roll_d6": "3", "digit_sum": "123", "distance_formula": "0\n0\n3\n4",
    "divide_two_numbers": "10\n2", "divisors": "12", "even_odd": "4",
    "exp": "1", "factor_pairs": "12", "factorial": "5",
    "factorial_table": "6", "fahrenheit_to_celsius": "212",
    "feet_to_meters": "328", "fibonacci_inline": "8", "floor": "3.9",
    "gcd_two": "12\n8", "gcd_range": "12\n4", "harshad": "18",
    "kg_to_pounds": "70", "km_to_miles": "10", "lcm_two": "4\n6",
    "lcm_range": "4\n3", "leap_year": "2024", "log10": "1000",
    "lowercase": "HELLO WORLD", "maximum": "5\n2\n9",
    "meters_to_feet": "100", "miles_to_km": "6.21", "minimum": "5\n2\n9",
    "multiples": "3\n5", "multiplication_table": "5",
    "multiply_two_numbers": "4\n3", "natural_log": "2.718281828",
    "neon": "9", "pascal_triangle": "5", "percentage": "20\n80",
    "perfect_number": "28", "perimeter_circle": "5", "pounds_to_kg": "154",
    "power": "2\n10", "prime_check": "7", "prime_list": "20", "pyramid": "4",
    "remove_spaces": "a b c", "round_num": "3.6", "sin_deg": "30",
    "spy_number": "123", "square_root": "81", "subtract_two_numbers": "5\n2",
    "sum_cubes": "10", "sum_natural": "10", "sum_squares": "10",
    "tan_deg": "45", "tech_number": "3025",
    "temperature_converter_extended": "0", "uppercase": "hello world",
    "volume_cube": "3", "volume_sphere": "3",
    "word_count": "the quick brown fox",
    # take no input at all
    "ascii_art": "", "current_time": "", "system_info": "",
    "timestamp": "", "uuid_generator": "",
}

KEY = r"[A-Za-z_][A-Za-z0-9_]*"


def samples_section(src):
    """Return (start, end, existing keys) for the SAMPLES object."""
    start = src.index("const SAMPLES = {")
    end = src.index("\n  };", start)
    body = src[start:end]
    keys = re.findall(r"(?:^|[\s,])(" + KEY + r")\s*:", body)
    return start, end, keys


def main() -> int:
    with open(PATH, encoding="utf-8") as fh:
        src = fh.read()
    before = src

    # 1. retire the AI chatbot - drop each piece on its own so nothing else is
    #    swallowed by a greedy pattern.
    src = re.sub(
        r"[ \t]*computer: \(a\) => \{ const t = String\(a\[0\] \|\| \"\"\)\.toLowerCase\(\);\n"
        r"[ \t]*for \(const key of Object\.keys\(CHAT\)\).*?\n"
        r"[ \t]*put\(\"Computer: I'm not sure how to respond to that\.\"\); \},\n",
        "", src)
    src = re.sub(r"[ \t]*const CHAT = \{.*?\n[ \t]*\};\n", "", src, flags=re.S)
    src = src.replace('"rock_paper_scissors", "computer"', '"rock_paper_scissors"')
    src = src.replace('"rock_paper_scissors", "computer",', '"rock_paper_scissors",')
    src = re.sub(r'computer: "hello",\s*', "", src)
    # "emi" was merged into loan_emi
    src = re.sub(r"[ \t]*emi: \(a\) => \{ const \[p, r, n\] = a; const rate = r / 1200;\n"
                 r"[ \t]*const e = rate \? p \* rate \* Math\.pow\(1 \+ rate, n\) / "
                 r"\(Math\.pow\(1 \+ rate, n\) - 1\) : p / n;\n"
                 r"[ \t]*put\(`Monthly EMI = \$\{e\.toFixed\(2\)\}`\); "
                 r"put\(`Total payment = \$\{\(e \* n\)\.toFixed\(2\)\}`\); \},\n",
                 "", src)
    src = src.replace('emi: "500000\\n8\\n240", ', "")

    # NOINPUT tells the runner which demos take no input. Make sure it exists:
    # removing CHAT above can take its comment line with it.
    if "const NOINPUT" not in src:
        src = re.sub(
            r"([ \t]*const MIXED = \[[^\]]*\];\n)",
            r'\1\n  // Programs that need no input at all, so the runner must not demand any.\n'
            r'  const NOINPUT = ["ascii_art", "current_time", "system_info", '
            r'"timestamp", "uuid_generator"];\n',
            src, count=1)

    # 2. rename stale keys, longest first so no prefix matches another key
    order = sorted(RENAMES, key=len, reverse=True)
    src = re.sub(r"(?<=[\s{,])(" + "|".join(map(re.escape, order)) + r")(?=\s*:)",
                 lambda m: RENAMES[m.group(1)], src)

    # 3. add only the sample keys that are still missing
    start, end, existing = samples_section(src)
    missing = {k: v for k, v in NEW_SAMPLES.items() if k not in existing}
    if missing:
        block = "\n    " + " ".join(
            f'{k}: "{v.replace(chr(10), chr(92) + "n")}",'
            for k, v in missing.items()
        )
        src = src[:end] + block + src[end:]

    with open(PATH, "w", encoding="utf-8", newline="") as fh:
        fh.write(src)

    _, _, final_keys = samples_section(src)
    dupes = sorted({k for k in final_keys if final_keys.count(k) > 1})
    print(f"{PATH}")
    print(f"  changed        : {src != before}")
    print(f"  AI demo gone   : {'computer:' not in src and 'CHAT' not in src}")
    print(f"  stale slugs    : {[k for k in RENAMES if re.search(r'(?<![\\w-])' + re.escape(k) + r'\\s*:', src)]}")
    print(f"  samples added  : {len(missing)}  (total {len(final_keys)})")
    print(f"  duplicate keys : {dupes or 'none'}")
    print(f"  NOINPUT kept   : {'const NOINPUT' in src}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())