# Contributing

Thanks for looking at this project.

## Run it locally

```bash
git clone https://github.com/Abhijeet-Kumar-Prajapati/pylab-studio.git
cd pylab-studio

# console menu (no dependencies)
run.bat          # Windows
py main.py       # any platform

# website
py -m pip install flask
run_website.bat  # -> http://127.0.0.1:5001
```

## Before you commit

```bash
test.bat                    # compile + smoke test
py webapp\app.py --selftest # expect: Total: 143  Passed: 143  Failed: 0
```

## Code style for the programs

Every program in `programs/general/` follows the same shape:

- module docstring with the title, category, a one-line description and an example
- `ask_number()` / `ask_text()` helpers for input validation
- a `main()` function holding the logic
- `if __name__ == "__main__": main()` at the bottom

Keep it standard library only, and make sure the program exits cleanly on
`q`, `Ctrl+C` or end of input.

## Regenerating things

```bash
py tools/build_programs.py   # rebuild programs/general from the spec table
py tools/build_site.py       # rebuild docs/ for GitHub Pages
py generate_reports.py       # refresh the catalogue and audit report
```

## Ground rules

- Do not commit `archive/`, `__pycache__/`, `*.zip` or virtual environments
- Keep the console programs free of third-party packages
- Add new programs to the catalogue so the menu stays in sync