<div align="center">

# PyLab Studio

### 132 Python Programs · Console Menu + Local Website + Live Web Demo

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black.svg)](https://flask.palletsprojects.com/)
[![Programs](https://img.shields.io/badge/programs-132%20%7C%209%20categories-informational.svg)]()

**Live demo:** <https://abhijeet-kumar-prajapati.github.io/pylab-studio/>

</div>

---

## What this is

A single project holding **132 small Python programs**, collected so they can be run
three different ways:

| | What it is | Needs a server? |
|---|---|---|
| **Console menu** | One terminal app listing every program | No |
| **Local website** | A Flask app that *actually executes* the Python files | Yes (you run it) |
| **Live web demo** | A static site where 118 programs run as JavaScript | No |

Everything runs **locally and offline**. No cloud services, no accounts, no tracking.

---

## Quick start

```bash
git clone https://github.com/Abhijeet-Kumar-Prajapati/pylab-studio.git
cd pylab-studio

# One command: makes .venv, installs packages, then verifies every program
setup.bat          # Windows
py setup.py        # macOS / Linux
```

Already set up? Ask what is missing:

```bash
py setup.py --check
```

Then pick how you want to run things:

```bash
run.bat            # console menu (no dependencies needed at all)
run_website.bat    # PyLab Studio website -> http://127.0.0.1:5001
test.bat           # compile + smoke test + full self test
```

The console menu needs **zero** third-party packages — it uses only the Python
standard library. Flask is required for the local website alone.

---

## Setup options

```bash
py setup.py              # full setup
py setup.py --check      # report status, change nothing
py setup.py --no-venv    # install into the current interpreter
py setup.py --force      # rebuild .venv from scratch
py setup.py --skip-deps  # set up but do not touch pip
```

Setup runs five steps: check the interpreter, create `.venv`, install the core
packages, install the optional extras (a failure here is never fatal), then
byte-compile everything and run the catalogue self-test.

---

## The 132 programs

| Category | Count | Examples |
|---|--:|---|
| Math / Number | 47 | prime check, factorial, Fibonacci, GCD/LCM, quadratic solver |
| Utility | 21 | password generator, quotes, water intake, stopwatch |
| String / Text | 16 | palindrome, Caesar cipher, Base64, word count |
| Converter | 15 | temperature, km↔miles, kg↔pounds, binary ↔ decimal |
| Loops / Pattern | 11 | pyramids, diamonds, Pascal's triangle, multiplication table |
| Game | 8 | rock-paper-scissors, dice, coin tosses, guess the number |
| Finance | 7 | EMI, compound interest, discount, profit/loss, tax |
| Health | 4 | BMI, heart-rate zones, calorie estimate, water intake |
| Conditionals | 3 | even/odd, is even, is odd |

Every program has a docstring, input validation and a clean exit. Many accept a
default: press **Enter** at the prompt to use it.

---

## Local website features

| Feature | Details |
|---|---|
| Dashboard | Live statistics and popular programs |
| Browse | Search plus category and collection filters |
| Favourites | Star programs, then filter down to just those |
| Run | Input form, **Fill sample**, output console, copy, exit code, timing |
| Recent runs | Last 25 runs kept in your browser |
| Categories | Programs grouped by category |
| Source view | Read any program's `.py` in the browser |
| Download | Whole project as `.zip`, or one program as `.py`, or the catalogue as CSV |
| REST API | JSON endpoints for listing, fetching and running |
| Shortcuts | <kbd>/</kbd> search · <kbd>c</kbd> input · <kbd>r</kbd> run · <kbd>p</kbd> programs · <kbd>?</kbd> help |
| Theming | Dark and light mode, remembered in the browser |

### Safety model

The local website **executes Python code**, so it is built to be hard to abuse:

- Only files inside whitelisted folders can ever run
- Every path is resolved with `realpath` and verified to be inside the project
- Each run starts a **separate process** — programs cannot affect each other
- **12-second timeout** per run
- Input capped at 4000 characters, output at 100 000 characters
- **Binds to `127.0.0.1` only** by default, so nothing on your network can reach it
- The Werkzeug debugger can never be switched on from a non-loopback host

---

## Project layout

```
pylab-studio/
├── setup.py               one-command setup (venv + deps + verification)
├── main.py                console menu entry point
├── program_registry.py    assigns category + description to each program
├── smoke_test.py          runs every program, writes reports/TEST_REPORT.md
├── generate_reports.py    rebuilds reports/PROGRAM_CATALOGUE.md + AUDIT_REPORT.md
├── programs/
│   ├── general/           130 standalone programs
│   └── utilities/         notes app, contact book
├── webapp/                Flask website (runs real Python)
│   ├── app.py
│   ├── templates/
│   └── static/
├── docs/                  generated static site -> GitHub Pages
├── reports/               catalogue, audit report, test report
├── tools/                 build_site.py, build_programs.py
├── projects/
│   ├── paypal_clone/      Flask demo app (accounts, transfers)
│   └── charvis_ai/        voice assistant
├── learning/              earlier practice exercises
├── web/, android/         HTML and mobile projects
└── site assets, batch launchers
```

---

## Console menu

| Option | Description |
|--------|-------------|
| `1`–`10` | Calculator, string tools, unit converter, games, file tools, JSON |
| `11` | Launch the Flask PayPal demo (port 5000) |
| `12` | Environment check |
| `13`–`14` | Charvis voice assistant (GUI and console) |
| `15`–`17` | Music library, phone generator, desktop icon toggle |
| `18` | Help and cheat sheet |
| `19` | Extra apps (password, BMI, timer, notes, contacts) |
| `20` | Browse all 130 general programs |
| `21` | Launch the website |
| `n` / `p` | Next / previous page |
| `0` | Exit |

---

## Testing

```bash
test.bat                          # compile + smoke test + self test
py webapp/app.py --selftest       # run all 132 programs, print pass/fail
py smoke_test.py                  # smoke test only, writes reports/TEST_REPORT.md
```

Current status: **132/132 self test**, **0 compile failures**.

---

## Regenerating

The catalogue, the static site and the console programs are generated from source
of truth, so edit the generator rather than the output:

```bash
py tools/build_programs.py   # regenerate programs/general from SPECS
py tools/build_site.py       # regenerate docs/ + build the downloadable zip
py generate_reports.py       # regenerate reports/
```

---

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `WEBSITE_HOST` | `127.0.0.1` | Bind address for the local website |
| `WEBSITE_PORT` | `5001` | Port for the local website |
| `SECRET_KEY` | random per process | Session signing key |
| `FLASK_DEBUG` | `0` | Debug mode (loopback only) |

---

## Requirements

- Python 3.8+
- Flask (website only) — `pip install -r requirements-all.txt`
- Everything else is standard library