"""
Multi Program - All in One
==========================

A single, self-contained, menu-driven console application that bundles
many small utility programs together. It uses only the Python standard
library so it runs on any machine with Python 3.8+ installed.

Run:
    python main.py
"""

import math
import random
import os
import sys
import subprocess
import datetime

# This file lives in docs/ but imports helpers that sit in the project root.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from program_registry import category_for, description_for  # noqa: E402
import json
import statistics


def clear_screen():
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass


def pause():
    try:
        input("\nPress Enter to continue...")
    except (EOFError, KeyboardInterrupt):
        pass


def get_number(prompt="Enter a number: "):
    while True:
        try:
            value = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            return None
        if value.lower() in ("q", "quit", "exit"):
            return None
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            print("Invalid number. Please try again (or type 'q' to cancel).")


def get_int(prompt="Enter an integer: ", min_val=None, max_val=None):
    while True:
        value = get_number(prompt)
        if value is None:
            return None
        if isinstance(value, float) and not value.is_integer():
            print("Please enter a whole number.")
            continue
        value = int(value)
        if min_val is not None and value < min_val:
            print(f"Value must be >= {min_val}.")
            continue
        if max_val is not None and value > max_val:
            print(f"Value must be <= {max_val}.")
            continue
        return value


# ---------------------------- Calculator ----------------------------
def calculator():
    print("\n=== Calculator ===")
    print("Operations: +  -  *  /  //  %  **")
    a = get_number("First number: ")
    if a is None:
        return
    op = input("Operation: ").strip()
    b = get_number("Second number: ")
    if b is None:
        return
    try:
        if op == "+":
            res = a + b
        elif op == "-":
            res = a - b
        elif op == "*":
            res = a * b
        elif op == "/":
            if b == 0:
                print("Cannot divide by zero.")
                return
            res = a / b
        elif op == "//":
            if b == 0:
                print("Cannot divide by zero.")
                return
            res = a // b
        elif op == "%":
            if b == 0:
                print("Cannot divide by zero.")
                return
            res = a % b
        elif op == "**":
            res = a ** b
        else:
            print("Unknown operation.")
            return
        print(f"Result: {res}")
    except Exception as e:
        print(f"Error: {e}")


def scientific_calculator():
    print("\n=== Scientific Calculator ===")
    print("1) sqrt   2) sin   3) cos   4) tan   5) log   6) log10   7) exp   8) factorial")
    choice = get_int("Choice: ", 1, 8)
    if choice is None:
        return
    x = get_number("Value: ")
    if x is None:
        return
    try:
        if choice == 1:
            if x < 0:
                print("sqrt of negative not allowed (real).")
                return
            print(f"sqrt({x}) = {math.sqrt(x)}")
        elif choice == 2:
            print(f"sin({x}) = {math.sin(math.radians(x))}")
        elif choice == 3:
            print(f"cos({x}) = {math.cos(math.radians(x))}")
        elif choice == 4:
            print(f"tan({x}) = {math.tan(math.radians(x))}")
        elif choice == 5:
            if x <= 0:
                print("log requires positive value.")
                return
            print(f"ln({x}) = {math.log(x)}")
        elif choice == 6:
            if x <= 0:
                print("log10 requires positive value.")
                return
            print(f"log10({x}) = {math.log10(x)}")
        elif choice == 7:
            print(f"exp({x}) = {math.exp(x)}")
        elif choice == 8:
            if isinstance(x, float) and not x.is_integer():
                print("Factorial needs an integer.")
                return
            n = int(x)
            if n < 0:
                print("Factorial of negative not defined.")
                return
            print(f"{n}! = {math.factorial(n)}")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------- Number tools ----------------------------
def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def number_tools():
    while True:
        print("\n=== Number Tools ===")
        print("1) Prime check")
        print("2) List primes in range")
        print("3) Factorial")
        print("4) Fibonacci (n terms)")
        print("5) GCD / LCM")
        print("6) Even/Odd")
        print("7) Digit sum")
        print("8) Back")
        c = get_int("Choice: ", 1, 8)
        if c is None or c == 8:
            return
        if c == 1:
            n = get_int("Number: ")
            if n is None:
                continue
            print("Prime" if is_prime(n) else "Not prime")
        elif c == 2:
            lo = get_int("Start: ")
            hi = get_int("End: ")
            if lo is None or hi is None:
                continue
            primes = [n for n in range(max(2, lo), hi + 1) if is_prime(n)]
            print("Primes:", primes)
        elif c == 3:
            n = get_int("Number: ", 0)
            if n is None:
                continue
            print(f"{n}! = {math.factorial(n)}")
        elif c == 4:
            n = get_int("Terms: ", 1)
            if n is None:
                continue
            a, b = 0, 1
            seq = []
            for _ in range(n):
                seq.append(a)
                a, b = b, a + b
            print("Fibonacci:", seq)
        elif c == 5:
            a = get_int("First number: ")
            b = get_int("Second number: ")
            if a is None or b is None:
                continue
            g = math.gcd(a, b)
            l = abs(a * b) // g if g != 0 else 0
            print(f"GCD = {g}, LCM = {l}")
        elif c == 6:
            n = get_int("Number: ")
            if n is None:
                continue
            print("Even" if n % 2 == 0 else "Odd")
        elif c == 7:
            n = get_int("Number: ")
            if n is None:
                continue
            print("Digit sum:", sum(int(d) for d in str(abs(n))))


# ---------------------------- String tools ----------------------------
def string_tools():
    while True:
        print("\n=== String Tools ===")
        print("1) Reverse")
        print("2) Palindrome check")
        print("3) Word count / char count")
        print("4) Upper / Lower / Title case")
        print("5) Remove spaces")
        print("6) Back")
        c = get_int("Choice: ", 1, 6)
        if c is None or c == 6:
            return
        s = input("Enter text: ")
        if c == 1:
            print("Reversed:", s[::-1])
        elif c == 2:
            cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
            print("Palindrome" if cleaned == cleaned[::-1] else "Not palindrome")
        elif c == 3:
            words = s.split()
            print(f"Characters: {len(s)}, Words: {len(words)}, Lines: {s.count(chr(10)) + 1}")
        elif c == 4:
            print("UPPER:", s.upper())
            print("lower:", s.lower())
            print("Title:", s.title())
        elif c == 5:
            print("No spaces:", s.replace(" ", ""))


# ---------------------------- Unit converter ----------------------------
def unit_converter():
    while True:
        print("\n=== Unit Converter ===")
        print("1) Celsius <-> Fahrenheit")
        print("2) Kilometers <-> Miles")
        print("3) Kilograms <-> Pounds")
        print("4) Meters <-> Feet")
        print("5) Back")
        c = get_int("Choice: ", 1, 5)
        if c is None or c == 5:
            return
        x = get_number("Value: ")
        if x is None:
            continue
        if c == 1:
            print(f"{x} C = {x*9/5+32} F")
            print(f"{x} F = {(x-32)*5/9} C")
        elif c == 2:
            print(f"{x} km = {x*0.621371} mi")
            print(f"{x} mi = {x/0.621371} km")
        elif c == 3:
            print(f"{x} kg = {x*2.20462} lb")
            print(f"{x} lb = {x/2.20462} kg")
        elif c == 4:
            print(f"{x} m = {x*3.28084} ft")
            print(f"{x} ft = {x/3.28084} m")


# ---------------------------- Games ----------------------------
def guess_number_game():
    print("\n=== Guess the Number ===")
    low = get_int("Lower bound (default 1): ") or 1
    high = get_int("Upper bound (default 100): ") or 100
    if low > high:
        low, high = high, low
    target = random.randint(low, high)
    attempts = 0
    max_attempts = 10
    while attempts < max_attempts:
        guess = get_int(f"Guess ({attempts+1}/{max_attempts}): ", low, high)
        if guess is None:
            print("Game cancelled.")
            return
        attempts += 1
        if guess == target:
            print(f"Correct! You won in {attempts} attempts.")
            return
        print("Too high!" if guess > target else "Too low!")
    print(f"Out of attempts. The number was {target}.")


def rock_paper_scissors():
    print("\n=== Rock Paper Scissors ===")
    choices = ["rock", "paper", "scissors"]
    wins = losses = draws = 0
    while True:
        user = input("Your choice (rock/paper/scissors, or 'q' to quit): ").strip().lower()
        if user in ("q", "quit", "exit"):
            break
        if user not in choices:
            print("Invalid choice.")
            continue
        comp = random.choice(choices)
        print(f"Computer chose: {comp}")
        if user == comp:
            draws += 1
            print("Draw!")
        elif (user == "rock" and comp == "scissors") or (user == "paper" and comp == "rock") or (user == "scissors" and comp == "paper"):
            wins += 1
            print("You win!")
        else:
            losses += 1
            print("You lose!")
    print(f"Score -> Wins: {wins}, Losses: {losses}, Draws: {draws}")


def games_menu():
    while True:
        print("\n=== Games ===")
        print("1) Guess the Number")
        print("2) Rock Paper Scissors")
        print("3) Back")
        c = get_int("Choice: ", 1, 3)
        if c is None or c == 3:
            return
        if c == 1:
            guess_number_game()
        elif c == 2:
            rock_paper_scissors()


# ---------------------------- Stats / list tools ----------------------------
def stats_tools():
    print("\n=== Statistics Tools ===")
    raw = input("Enter numbers separated by spaces/commas: ").strip()
    if not raw:
        return
    parts = raw.replace(",", " ").split()
    try:
        nums = [float(p) for p in parts]
    except ValueError:
        print("Invalid input.")
        return
    if not nums:
        return
    print(f"Count: {len(nums)}")
    print(f"Sum: {sum(nums)}")
    print(f"Min: {min(nums)}, Max: {max(nums)}")
    print(f"Mean: {statistics.mean(nums)}")
    if len(nums) > 1:
        print(f"Median: {statistics.median(nums)}")
        print(f"Std dev: {statistics.stdev(nums)}")
    print(f"Sorted: {sorted(nums)}")


# ---------------------------- File tools ----------------------------
def file_tools():
    while True:
        print("\n=== File Tools ===")
        print("1) List files in directory")
        print("2) Read text file")
        print("3) Write text file")
        print("4) Append to text file")
        print("5) File info")
        print("6) Back")
        c = get_int("Choice: ", 1, 6)
        if c is None or c == 6:
            return
        if c == 1:
            path = input("Directory (Enter for current): ").strip() or "."
            try:
                for name in sorted(os.listdir(path)):
                    full = os.path.join(path, name)
                    tag = "[DIR]" if os.path.isdir(full) else "[FILE]"
                    print(f"{tag} {name}")
            except Exception as e:
                print(f"Error: {e}")
        elif c == 2:
            path = input("File path: ").strip()
            try:
                with open(path, "r", encoding="utf-8") as f:
                    print(f.read())
            except Exception as e:
                print(f"Error: {e}")
        elif c == 3:
            path = input("File path: ").strip()
            text = input("Text to write: ")
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
                print("Written.")
            except Exception as e:
                print(f"Error: {e}")
        elif c == 4:
            path = input("File path: ").strip()
            text = input("Text to append: ")
            try:
                with open(path, "a", encoding="utf-8") as f:
                    f.write(text + "\n")
                print("Appended.")
            except Exception as e:
                print(f"Error: {e}")
        elif c == 5:
            path = input("File path: ").strip()
            try:
                st = os.stat(path)
                print(f"Size: {st.st_size} bytes")
                print(f"Modified: {datetime.datetime.fromtimestamp(st.st_mtime)}")
                print(f"Is file: {os.path.isfile(path)}, Is dir: {os.path.isdir(path)}")
            except Exception as e:
                print(f"Error: {e}")


# ---------------------------- Date & time ----------------------------
def date_time_tools():
    now = datetime.datetime.now()
    print("\n=== Date & Time ===")
    print("Current:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print("Day:", now.strftime("%A"))
    try:
        y = get_int("Birth year (for age calc, 0 to skip): ", 0)
        if y and y > 0:
            m = get_int("Birth month (1-12): ", 1, 12)
            d = get_int("Birth day (1-31): ", 1, 31)
            if m is not None and d is not None:
                birth = datetime.date(y, m, d)
                today = datetime.date.today()
                age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
                print(f"Age: {age} years")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------- JSON helper ----------------------------
def json_tools():
    while True:
        print("\n=== JSON Tools ===")
        print("1) Pretty print JSON")
        print("2) Validate JSON")
        print("3) Back")
        c = get_int("Choice: ", 1, 3)
        if c is None or c == 3:
            return
        raw = input("Enter JSON text: ")
        try:
            obj = json.loads(raw)
            print(json.dumps(obj, indent=2, ensure_ascii=False))
            print("Valid JSON.")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")


# ---------------------------- Web app launcher ----------------------------
def start_web_app():
    print("\n=== Start PayPal Clone Web App ===")
    app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "projects", "paypal_clone", "app.py")
    if not os.path.exists(app_path):
        print("PayPal clone app.py not found:", app_path)
        return
    try:
        print("Starting Flask app... open http://127.0.0.1:5000 in your browser.")
        print("Close the server window or press Ctrl+C to stop.")
        subprocess.Popen([sys.executable, app_path],
                         creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0)
    except Exception as e:
        print(f"Failed to start web app: {e}")


def env_check():
    print("\n=== Environment Check ===")
    print(f"Python: {sys.executable}")
    print(f"Version: {sys.version.split()[0]}")
    print(f"Platform: {sys.platform}")
    missing = []
    for mod in ("flask", "sqlalchemy", "requests"):
        try:
            __import__(mod)
            print(f"{mod}: OK")
        except Exception as e:
            print(f"{mod}: MISSING ({e})")
            missing.append(mod)
    if missing:
        print("\nInstall the missing packages with:")
        print(f"  {sys.executable} -m pip install -r requirements-all.txt")


# ---------------------------- Voice assistant launchers ----------------------------
PROJECT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "projects", "charvis_ai")


def start_charvis():
    print("\n=== Start Charvis AI (Voice Assistant GUI) ===")
    script = os.path.join(PROJECT_DIR, "charvis_ai.py")
    if not os.path.exists(script):
        print("charvis_ai.py not found.")
        return
    try:
        subprocess.Popen([sys.executable, script], cwd=PROJECT_DIR, creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0)
        print("Charvis AI started in a new window.")
    except Exception as e:
        print(f"Failed to start Charvis AI: {e}")


def start_voice_assistant():
    print("\n=== Start Voice Assistant (Console) ===")
    script = os.path.join(PROJECT_DIR, "voice_assistant.py")
    if not os.path.exists(script):
        print("voice_assistant.py not found.")
        return
    try:
        subprocess.Popen([sys.executable, script], cwd=PROJECT_DIR, creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0)
        print("Voice Assistant started in a new window.")
    except Exception as e:
        print(f"Failed to start Voice Assistant: {e}")


# ---------------------------- Music library ----------------------------
MUSIC_LIBRARY = {
    "shape of you": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "despacito": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
    "believer": "https://www.youtube.com/watch?v=7wtfhZwyrcc",
    "perfect": "https://www.youtube.com/watch?v=2Vv-BfVoq4g",
    "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA",
}


def music_library():
    print("\n=== Music Library ===")
    print("Available songs:", ", ".join(MUSIC_LIBRARY.keys()))
    song = input("Enter song name (or 'list'): ").strip().lower()
    if song == "list" or not song:
        for name, url in MUSIC_LIBRARY.items():
            print(f"- {name}: {url}")
        return
    url = MUSIC_LIBRARY.get(song)
    if not url:
        print("Song not found.")
        return
    print(f"URL: {url}")
    if input("Open in browser? (y/n): ").strip().lower() == "y":
        import webbrowser
        webbrowser.open(url)


# ---------------------------- Phone number generator ----------------------------
def phone_number_generator():
    print("\n=== Phone Number Generator ===")
    count = get_int("How many numbers? (default 100): ") or 100
    if count is None:
        return
    numbers = [f"{random.randint(60000000, 99999999)}84" for _ in range(count)]
    print(f"Generated {count} numbers ending in 84.")
    print("First 10:", numbers[:10])
    if input("Save to CSV? (y/n): ").strip().lower() == "y":
        path = input("File path (default phone_numbers.csv): ").strip() or "phone_numbers.csv"
        try:
            import csv
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["Phone Numbers"])
                for n in numbers:
                    w.writerow([n])
            print(f"Saved to {path}")
        except Exception as e:
            print(f"Error saving: {e}")


# ---------------------------- Toggle desktop icons ----------------------------
def toggle_desktop_icons():
    print("\n=== Toggle Desktop Icons (Windows) ===")
    try:
        import win32gui
        import win32con
        hwnd = win32gui.FindWindow("Progman", "Program Manager")
        if not hwnd:
            print("Program Manager window not found.")
            return
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        if style & win32con.WS_VISIBLE:
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            print("Desktop icons hidden.")
        else:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            print("Desktop icons shown.")
    except Exception as e:
        print(f"Error (Windows-only feature): {e}")


# ---------------------------- Help & Cheat Sheet ----------------------------
def help_cheat_sheet():
    print("\n=== HELP & CHEAT SHEET ===")
    print("Run: py main.py  (or SETUP_AND_RUN.bat)")
    print("Menu: type number + Enter. 0 = Exit.")
    print("Cancel any prompt: type 'q'.")
    print("")
    print("Calculator ops: + - * / // % **")
    print("Scientific: sqrt, sin, cos, tan, log, log10, exp, factorial (degrees for trig).")
    print("Number tools: prime check/list, factorial, fibonacci, gcd/lcm, even/odd, digit sum.")
    print("String tools: reverse, palindrome, counts, case change, remove spaces.")
    print("Converter: C/F, km/mi, kg/lb, m/ft.")
    print("Games: Guess Number (10 tries), Rock-Paper-Scissors.")
    print("Stats: enter numbers separated by space/comma.")
    print("File tools: list/read/write/append/info.")
    print("Date & Time: shows now; enter birth date for age.")
    print("JSON: paste JSON to validate/pretty print.")
    print("Music: type song name (or 'list').")
    print("Phone gen: count + save CSV.")
    print("Web app: starts Flask on http://127.0.0.1:5000")
    print("Charvis/Voice: start in new window.")
    print("Env check: shows python path & module status.")
    print("Cheat keys: Ctrl+C to interrupt; type q to cancel prompts.")


# ---------------------------- Extra programs ----------------------------
EXTRA_PROGRAMS = {
    "1": ("Password Generator", "programs/general/password_generator.py"),
    "2": ("BMI Calculator", "programs/general/bmi_calculator.py"),
    "3": ("Tip Calculator", "programs/general/tip_calculator.py"),
    "4": ("Quote Generator", "programs/general/quote_generator.py"),
    "5": ("Countdown Timer", "programs/general/countdown_timer.py"),
    "6": ("Dice Roller", "programs/general/dice_roll_custom.py"),
    "7": ("Notes App", "programs/utilities/notes_app.py"),
    "8": ("Contact Book", "programs/utilities/contact_book.py"),
}


def extra_programs_menu():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    while True:
        print("\n=== Extra Programs ===")
        for k, (name, _) in EXTRA_PROGRAMS.items():
            print(f"{k}) {name}")
        print("0) Back")
        c = input("Choice: ").strip()
        if c == "0":
            return
        if c in EXTRA_PROGRAMS:
            name, rel = EXTRA_PROGRAMS[c]
            path = os.path.join(base, rel)
            if not os.path.exists(path):
                print(f"File not found: {path}")
                continue
            print(f"Running {name}...")
            try:
                subprocess.run([sys.executable, path], cwd=base)
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Invalid choice.")


# ---------------------------- New 100 programs menu ----------------------------
def new_100_programs_menu():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NEW_PROGRAMS_100")
    if not os.path.isdir(base):
        print("Folder not found:", base)
        return
    files = sorted(f for f in os.listdir(base) if f.endswith(".py"))
    if not files:
        print("No programs found.")
        return
    page_size = 20
    page = 0
    while True:
        print(f"\n=== New 100 Programs (page {page+1}) ===")
        start = page * page_size
        chunk = files[start:start+page_size]
        for i, name in enumerate(chunk, start+1):
            print(f"{i}) {name}")
        print("n) Next page  p) Prev page  r) Run by number  0) Back")
        c = input("Choice: ").strip().lower()
        if c == "0":
            return
        if c == "n":
            if start + page_size < len(files):
                page += 1
            continue
        if c == "p":
            if page > 0:
                page -= 1
            continue
        if c == "r":
            try:
                num = int(input("Program number: "))
            except ValueError:
                print("Invalid.")
                continue
            if 1 <= num <= len(files):
                path = os.path.join(base, files[num-1])
                print(f"Running {files[num-1]}...")
                try:
                    subprocess.run([sys.executable, path], cwd=base)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Out of range.")
            continue
        # allow direct number
        try:
            num = int(c)
            if 1 <= num <= len(files):
                path = os.path.join(base, files[num-1])
                print(f"Running {files[num-1]}...")
                subprocess.run([sys.executable, path], cwd=base)
            else:
                print("Out of range.")
        except ValueError:
            print("Invalid choice.")


# ---------------------------- Main menu ----------------------------
CORE_MAX = 20


def _new_program_files():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NEW_PROGRAMS_100")
    if not os.path.isdir(base):
        return base, []
    files = sorted(f for f in os.listdir(base) if f.endswith(".py"))
    return base, files


def main_menu():
    base, new_files = _new_program_files()
    # cap to 100 new programs for numbering 21..120
    new_files = new_files[:100]
    total = CORE_MAX + len(new_files)
    page_size = 20
    page = 0
    while True:
        clear_screen()
        print("=" * 60)
        print("        MULTI PROGRAM - ALL IN ONE")
        print("=" * 60)
        start = page * page_size
        end = min(start + page_size, total)
        for i in range(start + 1, end + 1):
            if i <= CORE_MAX:
                core = {
                    1: ("Calculator", "Basic math calculator."),
                    2: ("Scientific Calculator", "sqrt/sin/cos/log etc."),
                    3: ("Number Tools", "prime/factorial/fibonacci/gcd."),
                    4: ("String Tools", "reverse/palindrome/counts."),
                    5: ("Unit Converter", "temp/length/weight."),
                    6: ("Games", "Guess number, rock-paper-scissors."),
                    7: ("Statistics Tools", "mean/median/std dev."),
                    8: ("File Tools", "list/read/write files."),
                    9: ("Date & Time / Age", "current time and age."),
                    10: ("JSON Tools", "validate/pretty JSON."),
                    11: ("Start PayPal Clone Web App", "Flask app on :5000."),
                    12: ("Environment Check", "python and module status."),
                    13: ("Start Charvis AI (GUI)", "voice assistant window."),
                    14: ("Start Voice Assistant", "console voice assistant."),
                    15: ("Music Library", "find/open songs."),
                    16: ("Phone Number Generator", "generate & save CSV."),
                    17: ("Toggle Desktop Icons", "Windows only."),
                    18: ("Help & Cheat Sheet", "quick usage guide."),
                    19: ("Extra Programs (9 apps)", "password/BMI/timer/notes etc."),
                    20: ("New 100 Programs (browse)", "list & run all new programs."),
                }
                nm, desc = core.get(i, ("Program", ""))
                print(f"{i:3d}) {nm}  [Core]")
                print(f"      -> {desc}")
            else:
                idx = i - CORE_MAX - 1
                if idx < len(new_files):
                    base_name = new_files[idx][:-3]
                    nm = base_name.replace("_", " ").title()
                    cat = category_for(base_name)
                    desc = description_for(base_name)
                    print(f"{i:3d}) {nm}  [{cat}]")
                    print(f"      -> {desc}")
                else:
                    print(f"{i:3d}) Program")
        print("  0) Exit")
        print(" n) Next page  p) Prev page")
        print("=" * 60)
        raw = input("Enter number (or n/p/0): ").strip().lower()
        if raw == "0":
            print("Goodbye!")
            break
        if raw == "n":
            if (page + 1) * page_size < total:
                page += 1
            continue
        if raw == "p":
            if page > 0:
                page -= 1
            continue
        try:
            choice = int(raw)
        except ValueError:
            print("Invalid.")
            pause()
            continue
        if choice < 0 or choice > total:
            print("Out of range.")
            pause()
            continue
        if choice == 0:
            print("Goodbye!")
            break
        # dispatch core
        if choice == 1:
            calculator()
        elif choice == 2:
            scientific_calculator()
        elif choice == 3:
            number_tools()
        elif choice == 4:
            string_tools()
        elif choice == 5:
            unit_converter()
        elif choice == 6:
            games_menu()
        elif choice == 7:
            stats_tools()
        elif choice == 8:
            file_tools()
        elif choice == 9:
            date_time_tools()
        elif choice == 10:
            json_tools()
        elif choice == 11:
            start_web_app()
        elif choice == 12:
            env_check()
        elif choice == 13:
            start_charvis()
        elif choice == 14:
            start_voice_assistant()
        elif choice == 15:
            music_library()
        elif choice == 16:
            phone_number_generator()
        elif choice == 17:
            toggle_desktop_icons()
        elif choice == 18:
            help_cheat_sheet()
        elif choice == 19:
            extra_programs_menu()
        elif choice == 20:
            new_100_programs_menu()
        else:
            idx = choice - CORE_MAX - 1
            if 0 <= idx < len(new_files):
                path = os.path.join(base, new_files[idx])
                print(f"Running {new_files[idx]}...")
                try:
                    subprocess.run([sys.executable, path], cwd=base)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Program not found.")
        pause()


def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
