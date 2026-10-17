"""
Tool: regenerate every program in programs/general with clean, modern,
consistent source code (docstring, validation, main(), no one-liners).

Usage:  py tools/build_programs.py
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "programs", "general")

HELPERS = '''

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
'''

SPECS = [
    # ---------------- Math / Numbers ----------------
    ("add_two_numbers", "Math/Number", "Adds two numbers together.", "2 + 3 = 5",
     [("a", "First number: ", "float"), ("b", "Second number: ", "float")],
     ['print(f"Result: {a} + {b} = {a + b}")']),
    ("subtract_two_numbers", "Math/Number", "Subtracts the second number from the first.", "5 - 2 = 3",
     [("a", "First number: ", "float"), ("b", "Second number: ", "float")],
     ['print(f"Result: {a} - {b} = {a - b}")']),
    ("multiply_two_numbers", "Math/Number", "Multiplies two numbers.", "4 * 3 = 12",
     [("a", "First number: ", "float"), ("b", "Second number: ", "float")],
     ['print(f"Result: {a} * {b} = {a * b}")']),
    ("divide_two_numbers", "Math/Number", "Divides the first number by the second.", "10 / 2 = 5",
     [("a", "Dividend: ", "float"), ("b", "Divisor: ", "float")],
     ['if b == 0:', '    print("Error: cannot divide by zero.")', 'else:',
      '    print(f"Result: {a} / {b} = {a / b}")']),
    ("power", "Math/Number", "Raises a base to an exponent.", "2 ** 10 = 1024",
     [("a", "Base: ", "float"), ("b", "Exponent: ", "float")],
     ['print(f"Result: {a} ** {b} = {a ** b}")']),
    ("square_root", "Math/Number", "Calculates the square root of a number.", "sqrt(81) = 9",
     [("x", "Number: ", "float")], ['import math',
      'if x < 0:', '    print("Error: square root of a negative number is not real.")',
      'else:', '    print(f"sqrt({x}) = {math.sqrt(x)}")']),
    ("factorial", "Math/Number", "Calculates factorial using a loop.", "5! = 120",
     [("n", "Number (0-20): ", "int")], ['import math',
      'if n < 0 or n > 20:', '    print("Error: enter a number between 0 and 20.")',
      'else:', '    print(f"{n}! = {math.factorial(n)}")']),
    ("prime_check", "Math/Number", "Checks whether a number is prime.", "7 is prime",
     [("n", "Number: ", "int")], ['import math',
      'is_prime = n > 1 and all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))',
      'print(f"{n} is", "PRIME" if is_prime else "NOT prime")']),
    ("fibonacci_inline", "Loops/Pattern", "Prints the first N Fibonacci numbers.", "1 1 2 3 5",
     [("n", "How many terms (1-50): ", "int")], ['a, b = 0, 1', 'for _ in range(n):',
      '    print(a, end=" ")', '    a, b = b, a + b', 'print()']),
    ("fibonacci_series", "Loops/Pattern", "Prints the Fibonacci series one per line.", "0 1 1 2",
     [("n", "How many terms (1-50): ", "int")], ['a, b = 0, 1', 'for _ in range(n):',
      '    print(a)', '    a, b = b, a + b']),
    ("gcd_two", "Math/Number", "Finds the greatest common divisor of two numbers.", "gcd(12,8) = 4",
     [("a", "First number: ", "int"), ("b", "Second number: ", "int")], ['import math',
      'print(f"GCD({a}, {b}) = {math.gcd(a, b)}")']),
    ("lcm_two", "Math/Number", "Finds the least common multiple of two numbers.", "lcm(4,6) = 12",
     [("a", "First number: ", "int"), ("b", "Second number: ", "int")], ['import math',
      'g = math.gcd(a, b)', 'lcm = abs(a * b) // g if g else 0',
      'print(f"LCM({a}, {b}) = {lcm}")']),
    ("average", "Math/Number", "Calculates the average of a list of numbers.", "avg of 2,4,6 = 4",
     [("nums", "Numbers (space separated): ", "numbers")],
     ['print(f"Average of {len(nums)} numbers = {sum(nums) / len(nums):.4f}")']),
    ("minimum", "Math/Number", "Finds the smallest number in a list.", "min of 5,2,9 = 2",
     [("nums", "Numbers (space separated): ", "numbers")],
     ['print(f"Minimum = {min(nums)}")']),
    ("maximum", "Math/Number", "Finds the largest number in a list.", "max of 5,2,9 = 9",
     [("nums", "Numbers (space separated): ", "numbers")],
     ['print(f"Maximum = {max(nums)}")']),
    ("percentage", "Math/Number", "Calculates a value as a percentage of a whole.", "20 of 80 = 25%",
     [("part", "Part value: ", "float"), ("whole", "Whole value: ", "float")],
     ['if whole == 0:', '    print("Error: whole value cannot be zero.")',
      'else:', '    print(f"{part} is {part / whole * 100:.2f}% of {whole}")']),
    ("area_circle", "Math/Number", "Calculates the area of a circle.", "r=5 -> 78.54",
     [("r", "Radius: ", "float")], ['import math', 'if r < 0:',
      '    print("Error: radius cannot be negative.")', 'else:',
      '    print(f"Area = {math.pi * r * r:.4f}")']),
    ("area_rectangle", "Math/Number", "Calculates the area of a rectangle.", "4 x 3 = 12",
     [("w", "Width: ", "float"), ("h", "Height: ", "float")],
     ['print(f"Area = {w * h}")']),
    ("area_triangle", "Math/Number", "Calculates the area of a triangle.", "base 6 height 4 = 12",
     [("b", "Base: ", "float"), ("h", "Height: ", "float")],
     ['print(f"Area = {0.5 * b * h}")']),
    ("perimeter_circle", "Math/Number", "Calculates the circumference of a circle.", "r=5 -> 31.42",
     [("r", "Radius: ", "float")], ['import math',
      'print(f"Circumference = {2 * math.pi * r:.4f}")']),
    ("volume_cube", "Math/Number", "Calculates the volume of a cube.", "side 3 -> 27",
     [("s", "Side length: ", "float")], ['print(f"Volume = {s ** 3}")']),
    ("volume_sphere", "Math/Number", "Calculates the volume of a sphere.", "r=3 -> 113.10",
     [("r", "Radius: ", "float")], ['import math',
      'print(f"Volume = {4 / 3 * math.pi * r ** 3:.4f}")']),
    ("distance_formula", "Math/Number", "Distance between two points on a plane.", "(0,0)-(3,4) = 5",
     [("x1", "x1: ", "float"), ("y1", "y1: ", "float"), ("x2", "x2: ", "float"), ("y2", "y2: ", "float")],
     ['import math', 'print(f"Distance = {math.hypot(x2 - x1, y2 - y1):.4f}")']),
    ("quadratic_solver", "Math/Number", "Solves ax^2 + bx + c = 0.", "x^2 - 5x + 6 -> 2, 3",
     [("a", "a: ", "float"), ("b", "b: ", "float"), ("c", "c: ", "float")],
     ['import cmath', 'if a == 0:', '    print("Error: a cannot be zero.")', 'else:',
      '    d = b * b - 4 * a * c', '    x1 = (-b + cmath.sqrt(d)) / (2 * a)',
      '    x2 = (-b - cmath.sqrt(d)) / (2 * a)', '    print(f"Roots: {x1} and {x2}")']),
    ("digit_sum", "Math/Number", "Sums the digits of a number.", "123 -> 6",
     [("n", "Number: ", "int")], ['print("Digit sum =", sum(int(d) for d in str(abs(n))))']),
    ("armstrong", "Math/Number", "Checks if a number is an Armstrong number.", "153 -> yes",
     [("n", "Number: ", "int")], ['digits = [int(d) for d in str(n)]',
      'total = sum(d ** len(digits) for d in digits)',
      'print(f"{n} is", "an Armstrong number" if total == n else "not an Armstrong number")']),
    ("perfect_number", "Math/Number", "Checks if a number is a perfect number.", "28 -> yes",
     [("n", "Number: ", "int")], ['if n <= 1:', '    print(f"{n} is not a perfect number")',
      'else:', '    total = sum(i for i in range(1, n) if n % i == 0)',
      '    print(f"{n} is", "perfect" if total == n else "not perfect")']),
    ("strong_number", "Math/Number", "Checks if a number is a strong number.", "145 -> yes",
     [("n", "Number: ", "int")], ['import math',
      'total = sum(math.factorial(int(d)) for d in str(n))',
      'print(f"{n} is", "strong" if total == n else "not strong")']),
    ("harshad", "Math/Number", "Checks if a number is a Harshad (Niven) number.", "18 -> yes",
     [("n", "Number: ", "int")], ['s = sum(int(d) for d in str(n))',
      'print(f"{n} is", "a Harshad number" if s and n % s == 0 else "not a Harshad number")']),
    ("automorphic", "Math/Number", "Checks if a number is automorphic.", "25 -> yes",
     [("n", "Number: ", "int")], ['print(f"{n} is", "automorphic" if str(n * n).endswith(str(n)) else "not automorphic")']),
    ("neon", "Math/Number", "Checks if a number is a neon number.", "9 -> yes",
     [("n", "Number: ", "int")], ['s = sum(int(d) for d in str(n * n))',
      'print(f"{n} is", "a neon number" if s == n else "not a neon number")']),
    ("spy_number", "Math/Number", "Checks if a number is a spy number.", "123 -> yes",
     [("n", "Number: ", "int")], ['import math', 'digits = [int(d) for d in str(n)]',
      'print(f"{n} is", "a spy number" if sum(digits) == math.prod(digits) else "not a spy number")']),
    ("tech_number", "Math/Number", "Checks if a number is a Tech number.", "3025 -> yes",
     [("n", "Number: ", "int")], ['s = str(n)', 'h = len(s) // 2',
      'if len(s) % 2 or h == 0:', '    print(f"{n} is not a Tech number")', 'else:',
      '    total = int(s[:h]) + int(s[h:])',
      '    print(f"{n} is", "a Tech number" if total * total == n else "not a Tech number")']),
    ("divisors", "Math/Number", "Lists all divisors of a number.", "12 -> 1 2 3 4 6 12",
     [("n", "Number: ", "int")], ['print("Divisors:", [i for i in range(1, n + 1) if n % i == 0])']),
    ("factor_pairs", "Math/Number", "Lists all factor pairs of a number.", "12 -> (1,12)(2,6)",
     [("n", "Number: ", "int")], ['pairs = [(i, n // i) for i in range(1, n + 1) if n % i == 0]',
      'print("Factor pairs:", pairs)']),
    ("multiples", "Math/Number", "Prints the first N multiples of a number.", "3 -> 3 6 9",
     [("n", "Number: ", "int"), ("count", "How many: ", "int")],
     ['print("Multiples:", [n * i for i in range(1, count + 1)])']),
    ("even_odd", "Conditionals", "Checks whether a number is even or odd.", "4 -> even",
     [("n", "Number: ", "int")], ['print(f"{n} is", "even" if n % 2 == 0 else "odd")']),
    ("is_even", "Conditionals", "Returns True when a number is even.", "8 -> True",
     [("n", "Number: ", "int")], ['print("Even" if n % 2 == 0 else "Odd")']),
    ("is_odd", "Conditionals", "Returns True when a number is odd.", "7 -> True",
     [("n", "Number: ", "int")], ['print("Odd" if n % 2 != 0 else "Even")']),
    ("absolute", "Math/Number", "Returns the absolute value of a number.", "-5 -> 5",
     [("x", "Number: ", "float")], ['print(f"|{x}| = {abs(x)}")']),
    ("round_num", "Math/Number", "Rounds a number to the nearest integer.", "3.6 -> 4",
     [("x", "Number: ", "float")], ['print(f"{x} rounded = {round(x)}")']),
    ("floor", "Math/Number", "Rounds a number down to the nearest integer.", "3.9 -> 3",
     [("x", "Number: ", "float")], ['import math', 'print(f"floor({x}) = {math.floor(x)}")']),
    ("ceil", "Math/Number", "Rounds a number up to the nearest integer.", "3.1 -> 4",
     [("x", "Number: ", "float")], ['import math', 'print(f"ceil({x}) = {math.ceil(x)}")']),
    ("natural_log", "Math/Number", "Calculates the natural logarithm.", "ln(e) = 1",
     [("x", "Number (>0): ", "float")], ['import math',
      'if x <= 0:', '    print("Error: log needs a positive number.")',
      'else:', '    print(f"ln({x}) = {math.log(x)}")']),
    ("log10", "Math/Number", "Calculates the base-10 logarithm.", "log10(1000) = 3",
     [("x", "Number (>0): ", "float")], ['import math',
      'if x <= 0:', '    print("Error: log10 needs a positive number.")',
      'else:', '    print(f"log10({x}) = {math.log10(x)}")']),
    ("exp", "Math/Number", "Calculates e raised to a power.", "exp(1) = 2.718",
     [("x", "Number: ", "float")], ['import math', 'print(f"exp({x}) = {math.exp(x)}")']),
    ("sin_deg", "Math/Number", "Sine of an angle in degrees.", "sin(30) = 0.5",
     [("x", "Angle in degrees: ", "float")], ['import math',
      'print(f"sin({x} deg) = {math.sin(math.radians(x)):.6f}")']),
    ("cos_deg", "Math/Number", "Cosine of an angle in degrees.", "cos(60) = 0.5",
     [("x", "Angle in degrees: ", "float")], ['import math',
      'print(f"cos({x} deg) = {math.cos(math.radians(x)):.6f}")']),
    ("tan_deg", "Math/Number", "Tangent of an angle in degrees.", "tan(45) = 1",
     [("x", "Angle in degrees: ", "float")], ['import math',
      'print(f"tan({x} deg) = {math.tan(math.radians(x)):.6f}")']),
    ("sum_natural", "Loops/Pattern", "Sums the first N natural numbers.", "sum(10) = 55",
     [("n", "N: ", "int")], ['print(f"Sum of 1..{n} = {n * (n + 1) // 2}")']),
    ("sum_squares", "Loops/Pattern", "Sums the squares of the first N numbers.", "sumsq(3) = 14",
     [("n", "N: ", "int")], ['print(f"Sum of squares 1..{n} = {n * (n + 1) * (2 * n + 1) // 6}")']),
    ("sum_cubes", "Loops/Pattern", "Sums the cubes of the first N numbers.", "sumcube(3) = 36",
     [("n", "N: ", "int")], ['s = n * (n + 1) // 2', 'print(f"Sum of cubes 1..{n} = {s * s}")']),
    ("multiplication_table", "Loops/Pattern", "Prints the multiplication table of a number.", "table of 5",
     [("n", "Number (1-20): ", "int")], ['for i in range(1, 11):',
      '    print(f"{n} x {i:2d} = {n * i}")']),
    ("factorial_table", "Loops/Pattern", "Prints factorials from 1 to N.", "1! 2! 3!",
     [("n", "N (1-15): ", "int")], ['import math', 'if n > 15:', '    print("Please enter 15 or less.")',
      'else:', '    for i in range(1, n + 1):', '        print(f"{i}! = {math.factorial(i)}")']),
    ("prime_list", "Math/Number", "Lists all prime numbers up to a limit.", "primes <= 20",
     [("n", "Limit: ", "int")], ['import math',
      'primes = [x for x in range(2, n + 1) if all(x % i for i in range(2, int(math.sqrt(x)) + 1))]',
      'print("Primes:", primes)']),
    ("pyramid", "Loops/Pattern", "Prints a star pyramid.", "4 rows",
     [("n", "Rows (1-20): ", "int")], ['for i in range(1, n + 1):',
      '    print(" " * (n - i) + "*" * (2 * i - 1))']),
    ("diamond", "Loops/Pattern", "Prints a star diamond shape.", "4 rows",
     [("n", "Half rows (1-15): ", "int")], ['for i in range(1, n + 1):',
      '    print(" " * (n - i) + "*" * (2 * i - 1))',
      'for i in range(n - 1, 0, -1):', '    print(" " * (n - i) + "*" * (2 * i - 1))']),
    ("pascal_triangle", "Loops/Pattern", "Prints Pascal's triangle.", "3 rows",
     [("n", "Rows (1-12): ", "int")], ['if n > 12:', '    print("Please enter 12 or less.")',
      'else:', '    row = [1]',
      '    for _ in range(n):', '        print(row)',
      '        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]']),
    # (ascii_art is written manually - see ascii_art.py)

    # ---------------- Converters ----------------
    ("celsius_to_fahrenheit", "Converter", "Converts Celsius to Fahrenheit.", "100 C = 212 F",
     [("c", "Celsius: ", "float")], ['print(f"{c} C = {c * 9 / 5 + 32} F")']),
    ("fahrenheit_to_celsius", "Converter", "Converts Fahrenheit to Celsius.", "212 F = 100 C",
     [("f", "Fahrenheit: ", "float")], ['print(f"{f} F = {(f - 32) * 5 / 9} C")']),
    ("temperature_converter_extended", "Converter", "Converts Celsius to Fahrenheit and Kelvin.", "0 C = 32 F = 273.15 K",
     [("c", "Celsius: ", "float")], ['print(f"{c} C = {c * 9 / 5 + 32} F = {c + 273.15} K")']),
    ("km_to_miles", "Converter", "Converts kilometres to miles.", "10 km = 6.21 mi",
     [("k", "Kilometres: ", "float")], ['print(f"{k} km = {k * 0.621371:.4f} miles")']),
    ("miles_to_km", "Converter", "Converts miles to kilometres.", "6.21 mi = 10 km",
     [("m", "Miles: ", "float")], ['print(f"{m} miles = {m / 0.621371:.4f} km")']),
    ("kg_to_pounds", "Converter", "Converts kilograms to pounds.", "70 kg = 154 lb",
     [("k", "Kilograms: ", "float")], ['print(f"{k} kg = {k * 2.20462:.4f} lb")']),
    ("pounds_to_kg", "Converter", "Converts pounds to kilograms.", "154 lb = 70 kg",
     [("p", "Pounds: ", "float")], ['print(f"{p} lb = {p / 2.20462:.4f} kg")']),
    ("meters_to_feet", "Converter", "Converts meters to feet.", "100 m = 328 ft",
     [("m", "Meters: ", "float")], ['print(f"{m} m = {m * 3.28084:.4f} ft")']),
    ("feet_to_meters", "Converter", "Converts feet to meters.", "328 ft = 100 m",
     [("f", "Feet: ", "float")], ['print(f"{f} ft = {f / 3.28084:.4f} m")']),
    ("hours_to_minutes", "Converter", "Converts hours to minutes.", "2 h = 120 min",
     [("h", "Hours: ", "float")], ['print(f"{h} h = {h * 60:g} minutes")']),
    ("minutes_to_seconds", "Converter", "Converts minutes to seconds.", "5 min = 300 s",
     [("m", "Minutes: ", "float")], ['print(f"{m} min = {m * 60:g} seconds")']),
    ("binary_to_decimal", "Converter", "Converts a binary number to decimal.", "1010 = 10",
     [("b", "Binary: ", "string")], ['if all(c in "01" for c in b) and b:',
      '    print(f"{b} in binary = {int(b, 2)} in decimal")',
      'else:', '    print("Invalid binary number.")']),
    ("decimal_to_binary", "Converter", "Converts a decimal number to binary.", "10 = 1010",
     [("n", "Decimal: ", "int")], ['print(f"{n} in decimal = {bin(n)[2:]} in binary")']),
    ("decimal_to_hex", "Converter", "Converts a decimal number to hexadecimal.", "255 = ff",
     [("n", "Decimal: ", "int")], ['print(f"{n} in decimal = {hex(n)[2:].upper()} in hex")']),
    ("hex_to_decimal", "Converter", "Converts hexadecimal to decimal.", "ff = 255",
     [("h", "Hex: ", "string")], ['try:', '    print(f"{h} in hex = {int(h, 16)} in decimal")',
      'except ValueError:', '    print("Invalid hex number.")']),
    ("number_to_words", "String/Text", "Converts a number (0-999999) into words.", "123 -> one hundred twenty three",
     [("n", "Number (0-999999): ", "int")],
     ['ones = ["zero","one","two","three","four","five","six","seven","eight","nine","ten",'
      '"eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]',
      'tens = ["","","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"]',
      'def under_1000(v):', '    parts = []',
      '    if v >= 100:', '        parts.append(ones[v // 100] + " hundred")', '        v %= 100',
      '    if v >= 20:', '        parts.append(tens[v // 10] + (" " + ones[v % 10] if v % 10 else ""))',
      '    elif v > 0:', '        parts.append(ones[v])',
      '    return " ".join(parts) or "zero"',
      'if not 0 <= n <= 999999:', '    print("Please enter a number between 0 and 999999.")',
      'else:', '    print(f"{n} = {under_1000(n // 1000) + \" thousand \" + under_1000(n % 1000)}".strip())']),

    # ---------------- Strings ----------------
    ("reverse_string", "String/Text", "Reverses a string.", "abc -> cba",
     [("s", "Text: ", "string")], ['print("Reversed:", s[::-1])']),
    ("palindrome_check", "String/Text", "Checks if a string is a palindrome.", "level -> yes",
     [("s", "Text: ", "string")],
     ['clean = "".join(c.lower() for c in s if c.isalnum())',
      'print(f"\\"{s}\\" is", "a palindrome" if clean == clean[::-1] else "not a palindrome")']),
    ("word_count", "String/Text", "Counts words in a sentence.", "4 words",
     [("s", "Text: ", "string")], ['print("Word count:", len(s.split()))']),
    ("char_count", "String/Text", "Counts characters in a string.", "abc -> 3",
     [("s", "Text: ", "string")], ['print("Characters:", len(s))']),
    ("uppercase", "String/Text", "Converts text to uppercase.", "abc -> ABC",
     [("s", "Text: ", "string")], ['print("Uppercase:", s.upper())']),
    ("lowercase", "String/Text", "Converts text to lowercase.", "ABC -> abc",
     [("s", "Text: ", "string")], ['print("Lowercase:", s.lower())']),
    ("title_case", "String/Text", "Converts text to title case.", "hello world -> Hello World",
     [("s", "Text: ", "string")], ['print("Title case:", s.title())']),
    ("remove_spaces", "String/Text", "Removes all spaces from text.", "a b c -> abc",
     [("s", "Text: ", "string")], ['print("Without spaces:", s.replace(" ", ""))']),
    ("count_vowels", "String/Text", "Counts vowels in a string.", "education -> 5",
     [("s", "Text: ", "string")],
     ['print("Vowels:", sum(1 for c in s.lower() if c in "aeiou"))']),
    ("sort_words", "String/Text", "Sorts the words of a sentence.", "b a -> a b",
     [("s", "Text: ", "string")], ['print("Sorted:", " ".join(sorted(s.split())))']),
    ("remove_duplicates", "String/Text", "Removes duplicate words.", "a b a -> a b",
     [("s", "Text: ", "string")], ['print("Unique:", " ".join(dict.fromkeys(s.split())))']),
    ("caesar_encrypt", "String/Text", "Encrypts text with a Caesar cipher.", "abc shift 1 -> bcd",
     [("s", "Text: ", "string"), ("k", "Shift (1-25): ", "int")],
     ['def shift_char(ch, k):',
      '    if ch.islower():', '        return chr((ord(ch) - 97 + k) % 26 + 97)',
      '    if ch.isupper():', '        return chr((ord(ch) - 65 + k) % 26 + 65)',
      '    return ch',
      'k = k % 26',
      'print("Encrypted:", "".join(shift_char(c, k) for c in s))']),
    ("caesar_decrypt", "String/Text", "Decrypts text with a Caesar cipher.", "bcd shift 1 -> abc",
     [("s", "Text: ", "string"), ("k", "Shift (1-25): ", "int")],
     ['def unshift(ch, k):',
      '    if ch.islower():', '        return chr((ord(ch) - 97 - k) % 26 + 97)',
      '    if ch.isupper():', '        return chr((ord(ch) - 65 - k) % 26 + 65)',
      '    return ch',
      'k = k % 26',
      'print("Decrypted:", "".join(unshift(c, k) for c in s))']),
    ("base64_encode", "String/Text", "Encodes text to Base64.", "hi -> aGk=",
     [("s", "Text: ", "string")], ['import base64',
      'print("Base64:", base64.b64encode(s.encode()).decode())']),
    ("base64_decode", "String/Text", "Decodes a Base64 string.", "aGk= -> hi",
     [("s", "Base64: ", "string")], ['import base64',
      'try:', '    print("Decoded:", base64.b64decode(s).decode(errors="replace"))',
      'except Exception:', '    print("Invalid Base64 input.")']),

    # ---------------- Finance ----------------
    ("simple_interest", "Finance", "Calculates simple interest.", "P=1000 R=5 T=2 -> 100",
     [("p", "Principal: ", "float"), ("r", "Rate %: ", "float"), ("t", "Time (years): ", "float")],
     ['si = p * r * t / 100', 'print(f"Simple interest = {si:.2f}")', 'print(f"Total amount = {p + si:.2f}")']),
    ("compound_interest", "Finance", "Calculates compound interest.", "P=1000 R=10 T=2 -> 210",
     [("p", "Principal: ", "float"), ("r", "Rate %: ", "float"), ("t", "Time (years): ", "float"), ("n", "Compounds per year: ", "int")],
     ['amount = p * (1 + r / (100 * n)) ** (n * t)', 'print(f"Compound amount = {amount:.2f}")']),
    ("compound_interest_schedule", "Finance", "Compound interest with growth summary.", "shows yearly growth",
     [("p", "Principal: ", "float"), ("r", "Rate %: ", "float"), ("t", "Time (years): ", "int")],
     ['for year in range(1, t + 1):', '    amount = p * (1 + r / 100) ** year',
      '    print(f"Year {year}: {amount:.2f}")']),
    ("loan_emi", "Finance", "Loan EMI with total interest breakdown.", "shows interest",
     [("p", "Loan amount: ", "float", "500000"), ("r", "Annual rate %: ", "float", "8"),
      ("n", "Months: ", "int", "240")],
     ['rate = r / 1200', 'emi = p * rate * (1 + rate) ** n / ((1 + rate) ** n - 1) if rate else p / n',
      'interest = emi * n - p', 'print(f"EMI = {emi:.2f}")',
      'print(f"Total interest = {interest:.2f}")', 'print(f"Total payment = {emi * n:.2f}")']),
    ("discount", "Finance", "Calculates a discount price.", "1000 at 20% -> 800",
     [("price", "Original price: ", "float"), ("d", "Discount %: ", "float")],
     ['final = price * (1 - d / 100)', 'print(f"Final price = {final:.2f}")', 'print(f"You save = {price - final:.2f}")']),
    ("profit_loss", "Finance", "Shows profit or loss percentage.", "buy 100 sell 120 -> 20% profit",
     [("cp", "Cost price: ", "float"), ("sp", "Selling price: ", "float")],
     ['if cp == 0:', '    print("Cost price cannot be zero.")', 'else:',
      '    diff = sp - cp', '    pct = diff / cp * 100',
      '    label = "Profit" if diff >= 0 else "Loss"',
      '    print(f"{label}: {abs(diff):.2f} ({abs(pct):.2f}%)")']),
    ("tax", "Finance", "Calculates tax and final amount.", "1000 at 10% -> 100",
     [("amount", "Amount: ", "float"), ("t", "Tax %: ", "float")],
     ['tax = amount * t / 100', 'print(f"Tax = {tax:.2f}")', 'print(f"Total = {amount + tax:.2f}")']),

    # ---------------- Health ----------------
    ("bmi_calculator", "Health", "Calculates Body Mass Index and category.", "70kg 1.75m -> 22.9",
     [("w", "Weight (kg): ", "float"), ("h", "Height (m): ", "float")],
     ['if h <= 0:', '    print("Height must be greater than zero.")', 'else:',
      '    bmi = w / (h * h)',
      '    if bmi < 18.5: cat = "Underweight"',
      '    elif bmi < 25: cat = "Normal"',
      '    elif bmi < 30: cat = "Overweight"',
      '    else: cat = "Obese"',
      '    print(f"BMI = {bmi:.2f} ({cat})")']),
    ("water_intake", "Health", "Estimates daily water intake in ml.", "70kg -> 2450 ml",
     [("w", "Weight (kg): ", "float")], ['print(f"Recommended water: {w * 35:.0f} ml per day")']),
    ("heart_rate_zones", "Health", "Shows target heart-rate zones.", "age 30 -> zones",
     [("age", "Age: ", "int")], ['max_hr = 220 - age',
      'print(f"Maximum heart rate: {max_hr} bpm")',
      'print(f"Moderate zone: {max_hr * 0.5:.0f} - {max_hr * 0.7:.0f} bpm")',
      'print(f"Vigorous zone: {max_hr * 0.7:.0f} - {max_hr * 0.85:.0f} bpm")']),
    ("calorie_estimate", "Health", "Estimates daily calories (BMR).", "M 70kg 175cm 30",
     [("w", "Weight (kg): ", "float"), ("h", "Height (cm): ", "float"), ("a", "Age: ", "int"), ("g", "Gender (m/f): ", "string")],
     ['bmr = 10 * w + 6.25 * h - 5 * a + (5 if g.lower().startswith("m") else -161)',
      'print(f"Estimated BMR = {bmr:.0f} kcal/day")']),

    # ---------------- Games ----------------
    ("guess_number_game", "Game", "Guess the secret number between 1-100.", "10 tries",
     [], ['import random', 'target = random.randint(1, 100)',
      'for attempt in range(1, 11):',
      '    guess = ask_number(f"Guess {attempt}/10: ", "int")',
      '    if guess == target:', '        print(f"Correct! You won in {attempt} tries.")', '        break',
      '    print("Too high!" if guess > target else "Too low!")',
      'else:', '    print(f"Out of tries. The number was {target}.")']),
    ("rock_paper_scissors", "Game", "Play rock, paper, scissors.", "win/lose/draw",
     [], ['import random', 'choices = ["rock", "paper", "scissors"]',
      'wins = losses = draws = 0',
      'while True:',
      '    user = ask_text("Your choice (rock/paper/scissors, q to quit): ").lower()',
      '    if user == "q":', '        break',
      '    if user not in choices:', '        print("Invalid choice.")', '        continue',
      '    comp = random.choice(choices)', '    print("Computer chose:", comp)',
      '    beats = {"rock": "scissors", "paper": "rock", "scissors": "paper"}',
      '    if user == comp:', '        draws += 1', '        print("Draw!")',
      '    elif beats[user] == comp:', '        wins += 1', '        print("You win!")',
      '    else:', '        losses += 1', '        print("You lose!")',
      'print(f"Final score -> wins {wins}, losses {losses}, draws {draws}")']),
    ("coin_tosses", "Game", "Tosses a coin one or more times.", "H T H",
     [("n", "How many tosses (1-100): ", "int")], ['import random',
      'results = [random.choice(["Heads", "Tails"]) for _ in range(n)]',
      'print("Results:", results)',
      'print("Heads:", results.count("Heads"), " Tails:", results.count("Tails"))']),
    ("coin_flip", "Game", "Flips a single coin.", "Heads or Tails",
     [], ['import random', 'print("Result:", random.choice(["Heads", "Tails"]))']),
    ("dice_roll_d6", "Game", "Rolls one or more dice.", "2 dice total",
     [("count", "How many dice (1-6): ", "int")],
     ['import random', 'rolls = [random.randint(1, 6) for _ in range(count)]',
      'print("Rolls:", rolls)', 'print("Total:", sum(rolls))']),
    ("dice_roll_custom", "Game", "Rolls custom dice with N sides.", "d100",
     [("sides", "Sides per die: ", "int"), ("count", "Number of dice: ", "int")],
     ['import random', 'rolls = [random.randint(1, sides) for _ in range(count)]',
      'print("Rolls:", rolls)', 'print("Total:", sum(rolls))']),
    ("trivia", "Game", "Simple programming trivia quiz.", "score out of 5",
     [], ['questions = {', '    "Which keyword defines a function?": "def",',
      '    "Which symbol starts a comment?": "#",',
      '    "What is 2 ** 3?": "8",', '    "Which keyword makes a class?": "class",',
      '    "Which list method adds an item?": "append",', '}',
      'score = 0',
      'for question, answer in questions.items():',
      '    reply = ask_text(question + " ").lower()',
      '    if reply == answer.lower():', '        score += 1', '        print("  Correct!")',
      '    else:', '        print(f"  Wrong! Answer: {answer}")',
      'print(f"Final score: {score}/{len(questions)}")']),
    ("mad_libs", "Game", "Fill in blanks to build a sentence.", "fun sentence",
     [("noun", "Noun: ", "string"), ("verb", "Verb: ", "string"), ("adj", "Adjective: ", "string")],
     ['print(f"The {adj} {noun} likes to {verb} every single day.")']),

    # ---------------- Utilities ----------------
    ("password_generator", "Utility", "Generates random secure passwords.", "strong passwords",
     [("length", "Length (4-64): ", "int", "16"), ("count", "How many (1-50): ", "int", "5")],
     ['import random, string',
      'pool = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"',
      'for _ in range(count):',
      '    print("".join(random.choice(pool) for _ in range(length)))']),
    ("quick_password", "Utility", "Quick random password generator.", "12 char password",
     [("length", "Length: ", "int")], ['import random, string',
      'pool = string.ascii_letters + string.digits + "!@#$%"',
      'print("Password:", "".join(random.choice(pool) for _ in range(length)))']),
    ("random_number", "Utility", "Generates a random number in a range.", "1-100",
     [("lo", "Minimum: ", "int"), ("hi", "Maximum: ", "int")], ['import random',
      'if lo > hi:', '    lo, hi = hi, lo', 'print("Random number:", random.randint(lo, hi))']),
    ("random_string", "Utility", "Generates a random alphanumeric string.", "8 chars",
     [("n", "Length: ", "int")], ['import random, string',
      'pool = string.ascii_letters + string.digits',
      'print("Random string:", "".join(random.choice(pool) for _ in range(n)))']),
    ("uuid_generator", "Utility", "Generates a UUID v4.", "unique id",
     [], ['import uuid', 'print("UUID:", uuid.uuid4())']),
    ("countdown_timer", "Utility", "Counts down and shows time remaining.", "10 -> 0",
     [("seconds", "Seconds (1-3600): ", "int")], ['import time',
      'for remaining in range(seconds, 0, -1):',
      '    print(f"\\rTime left: {remaining:>4d}s", end="", flush=True)',
      '    time.sleep(1)', 'print("\\rTime is up!        ")']),
    ("stopwatch", "Utility", "Measures elapsed time with Enter presses.", "elapsed seconds",
     [], ['import time', 'ask_text("Press Enter to start...")',
      'start = time.perf_counter()', 'ask_text("Press Enter to stop...")',
      'print(f"Elapsed: {time.perf_counter() - start:.2f} seconds")']),
    ("quote_generator", "Utility", "Prints random motivational quotes.", "inspiration",
     [("count", "How many quotes (1-10): ", "int", "3")],
     ['import random', 'quotes = [',
      '    "Simplicity is the soul of efficiency. - Austin Freeman",',
      '    "First, solve the problem. Then write the code. - John Johnson",',
      '    "Experience is the name everyone gives to their mistakes. - Oscar Wilde",',
      '    "Talk is cheap. Show me the code. - Linus Torvalds",',
      '    "Stay hungry, stay foolish. - Steve Jobs",',
      '    "Knowledge is power. - Francis Bacon",',
      '    "Code is like humor. When you have to explain it, it is bad. - Cory House",',
      ']',
      'for _ in range(min(count, len(quotes))):', '    print(" -", random.choice(quotes))']),
    ("tip_calculator", "Utility", "Splits a bill with tip between people.", "100 tip 15% split 2",
     [("bill", "Bill amount: ", "float", "1000"), ("tip", "Tip %: ", "float", "15"),
      ("people", "Split among: ", "int", "2")],
     ['tip_amount = bill * tip / 100', 'total = bill + tip_amount',
      'print(f"Tip: {tip_amount:.2f}")', 'print(f"Total: {total:.2f}")',
      'print(f"Per person: {total / max(people, 1):.2f}")']),
    ("age_calculator", "Utility", "Calculates age from a birth date.", "born 2005 -> age",
     [("y", "Birth year: ", "int"), ("m", "Birth month (1-12): ", "int"), ("d", "Birth day (1-31): ", "int")],
     ['import datetime',
      'try:', '    birth = datetime.date(y, m, d)',
      'except ValueError:', '    print("That date does not exist.")',
      'else:',
      '    today = datetime.date.today()',
      '    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))',
      '    print(f"Age: {age} years")',
      '    print(f"Next birthday in: {(birth.replace(year=today.year) - today).days} days")']),
    ("leap_year", "Utility", "Checks if a year is a leap year.", "2024 -> leap",
     [("y", "Year: ", "int")],
     ['leap = (y % 4 == 0 and y % 100 != 0) or y % 400 == 0',
      'print(f"{y} is", "a leap year" if leap else "not a leap year")']),
    ("day_of_week", "Utility", "Prints the weekday of a date.", "2024-01-01 -> Monday",
     [("y", "Year: ", "int"), ("m", "Month (1-12): ", "int"), ("d", "Day (1-31): ", "int")],
     ['import datetime',
      'try:', '    print("Weekday:", datetime.date(y, m, d).strftime("%A"))',
      'except ValueError:', '    print("That date does not exist.")']),
    ("days_between", "Utility", "Counts days between two dates.", "2024-01-01 to 2024-01-10",
     [("d1", "First date (YYYY-MM-DD): ", "string"), ("d2", "Second date (YYYY-MM-DD): ", "string")],
     ['import datetime',
      'try:',
      '    start = datetime.date.fromisoformat(d1)',
      '    end = datetime.date.fromisoformat(d2)',
      '    print("Days between:", abs((end - start).days))',
      'except ValueError:', '    print("Invalid date. Use YYYY-MM-DD.")']),
    ("system_info", "Utility", "Shows Python and OS information.", "version details",
     [], ['import platform, sys',
      'print("Python:", sys.version.split()[0])',
      'print("Platform:", platform.system(), platform.release())',
      'print("Machine:", platform.machine())']),
    ("current_time", "Utility", "Shows the current date and time.", "live clock",
     [], ['import datetime', 'now = datetime.datetime.now()',
      'print("Date:", now.strftime("%Y-%m-%d"))', 'print("Time:", now.strftime("%H:%M:%S"))',
      'print("Full:", now.strftime("%A, %d %B %Y %H:%M:%S"))']),
    ("timestamp", "Utility", "Shows the current Unix timestamp.", "1730000000",
     [], ['import time', 'print("Unix timestamp:", int(time.time()))']),
    ("file_line_count", "Utility", "Counts lines in a text file.", "counts lines",
     [("path", "File path: ", "string")], ['import os',
      'if os.path.isfile(path):', '    with open(path, encoding="utf-8", errors="replace") as f:',
      '        print("Lines:", sum(1 for _ in f))', 'else:', '    print("File not found.")']),
    ("file_word_count", "Utility", "Counts words in a text file.", "counts words",
     [("path", "File path: ", "string")], ['import os',
      'if os.path.isfile(path):', '    with open(path, encoding="utf-8", errors="replace") as f:',
      '        print("Words:", len(f.read().split()))', 'else:', '    print("File not found.")']),
    ("list_directory", "Utility", "Lists files in a directory.", "shows files",
     [("path", "Directory (empty = current): ", "string")], ['import os',
      'target = path or "."',
      'try:',
      '    for name in sorted(os.listdir(target)):',
      '        tag = "[DIR] " if os.path.isdir(os.path.join(target, name)) else "[FILE]"',
      '        print(f"{tag} {name}")',
      'except Exception as error:', '    print("Error:", error)']),
]

TITLE_FIX = {}

# Words that must not be Title-Cased, so the docstring reads well
# ("uuid_generator" -> "UUID Generator", not "Uuid Generator").
ACRONYMS = {
    "uuid": "UUID", "bmi": "BMI", "emi": "EMI", "ascii": "ASCII",
    "base64": "Base64", "url": "URL", "api": "API", "cpu": "CPU",
    "id": "ID", "ip": "IP", "pdf": "PDF", "csv": "CSV", "json": "JSON",
}


def title_for(name):
    """Build a human-readable title from a program slug."""
    return " ".join(
        ACRONYMS.get(word.lower(), word.capitalize()) for word in name.split("_")
    )


def build(name, category, description, example, inputs, body):
    title = TITLE_FIX.get(name) or title_for(name)
    lines = ['"""', f"{title}", f"Category: {category}", "",
             f"{description}", "",
             "Example:", f"    {example}", '"""', ""]

    # hoist any "import x" statements to module level for clean style
    imports = []
    body_clean = []
    for line in body:
        stripped = line.strip()
        if stripped.startswith("import ") and stripped == line:
            if stripped not in imports:
                imports.append(stripped)
        else:
            body_clean.append(line)
    body = body_clean

    if imports:
        lines.extend(imports)
        lines.append("")

    needs_helpers = bool(inputs)
    body_text = "\n".join(body)
    if needs_helpers or "ask_" in body_text:
        lines.append("")
        lines.append(HELPERS.strip("\n"))
        lines.append("")

    lines.append("")
    lines.append("def main():")
    if not inputs and "ask_" not in body_text:
        lines.append('    """Entry point."""')
    for entry in inputs:
        # (var, prompt, kind) or (var, prompt, kind, default)
        var, prompt, kind = entry[0], entry[1], entry[2]
        dflt = "" if len(entry) < 4 else f', "{entry[3]}"'
        if kind == "float":
            lines.append(f'    {var} = ask_number("{prompt}", "float"{dflt})')
        elif kind == "int":
            lines.append(f'    {var} = ask_number("{prompt}", "int"{dflt})')
        elif kind == "string":
            lines.append(f'    {var} = ask_text("{prompt}"{dflt})')
        elif kind == "numbers":
            lines.append(f'    raw = ask_text("{prompt}"{dflt})')
            lines.append('    nums = [float(x) for x in raw.replace(",", " ").split()]')
    if inputs or body:
        lines.append("")
    for line in body:
        lines.append(("    " + line) if line.strip() else "")
    lines.append("")
    lines.append("")
    lines.append('if __name__ == "__main__":')
    lines.append("    main()")
    return "\n".join(lines) + "\n"


def main():
    os.makedirs(OUT, exist_ok=True)
    written = []
    for spec in SPECS:
        path = os.path.join(OUT, spec[0] + ".py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build(*spec))
        written.append(spec[0])
    print(f"Regenerated {len(written)} programs in {OUT}")


if __name__ == "__main__":
    main()