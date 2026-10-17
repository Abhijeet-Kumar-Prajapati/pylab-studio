"""Program registry: assigns category and description to each program automatically."""

CATEGORY_RULES = [
    ("Math/Number", ["add", "subtract", "multiply", "divide", "power", "square_root", "factorial",
                     "prime", "fibonacci", "gcd", "lcm", "average", "minimum", "maximum",
                     "percentage", "area", "perimeter", "volume", "distance", "quadratic",
                     "digit_sum", "armstrong", "perfect", "strong", "harshad", "automorphic",
                     "neon", "spy", "tech", "divisor", "factor", "multiple", "even", "odd",
                     "log", "exp", "sin", "cos", "tan", "floor", "ceil", "round", "absolute",
                     "sum_", "natural", "pascal", "pyramid", "diamond", "is_"]),
    ("Converter", ["celsius", "fahrenheit", "km_", "miles", "kg_", "pounds", "meters", "feet",
                   "hours", "minutes", "binary", "hex", "temperature", "currency"]),
    ("String/Text", ["string", "palindrome", "word_count", "char_count", "uppercase", "lowercase",
                     "title_case", "remove_spaces", "vowel", "sort_words", "duplicates", "caesar",
                     "base64", "reverse"]),
    ("Finance", ["interest", "emi", "discount", "profit", "tax", "loan"]),
    ("Health", ["bmi", "water", "heart_rate", "calorie"]),
    ("Game", ["guess", "rock_paper", "coin", "dice", "trivia", "mad_libs", "ascii", "game"]),
    ("Utility", ["password", "uuid", "random", "quote", "timer", "countdown", "stopwatch",
                 "system_info", "time", "day_of", "days_between", "leap", "age", "file_",
                 "list_directory", "note", "contact"]),
    ("Loop/Pattern", ["multiplication_table", "factorial_table", "prime_list", "fibonacci_series"]),
]

DEFAULT_CATEGORY = "General"

DESCRIPTIONS = {
    "password_generator": "Generates random secure passwords.",
    "bmi_calculator": "Calculates Body Mass Index.",
    "tip_calculator": "Splits bill and tip among people.",
    "quote_generator": "Prints random motivational quotes.",
    "countdown_timer": "Counts down given seconds.",
    "dice_roll_custom": "Rolls dice and shows total.",
    "notes_app": "Save/list/delete notes (JSON).",
    "contact_book": "Save/list/search contacts (JSON).",
    "absolute": "Returns absolute value of a number.",
    "pyramid": "Prints a star pyramid.",
    "diamond": "Prints a diamond pattern.",
    "ascii_art": "Prints small ASCII art.",
    "mad_libs": "Simple fill-in-the-blank sentence.",
    "pascal_triangle": "Prints Pascal triangle.",
    "fibonacci_series": "Prints Fibonacci series.",
    "fibonacci_inline": "Prints N Fibonacci numbers.",
}


def category_for(name):
    n = name.lower()
    for cat, keys in CATEGORY_RULES:
        for k in keys:
            if k in n:
                return cat
    return DEFAULT_CATEGORY


def description_for(name):
    if name in DESCRIPTIONS:
        return DESCRIPTIONS[name]
    words = name.replace("_", " ")
    return words.capitalize() + " program."