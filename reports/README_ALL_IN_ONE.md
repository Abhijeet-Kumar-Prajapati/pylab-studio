# PyLab Studio - quick reference

## Console menu (all 132 programs)
```bash
run.bat            # Windows
py main.py         # macOS / Linux
```
Press `0` to exit.

## Local website (runs the real Python)
```bash
run_website.bat    # Windows, opens http://127.0.0.1:5001
py webapp/app.py   # any platform
```

## PayPal clone demo
```bash
run_web_app.bat
```
Then open http://127.0.0.1:5000

## Set up first
```bash
setup.bat          # Windows
py setup.py        # any platform
py setup.py --check    # what is missing?
```

## Notes

- The console menu uses only the Python standard library - no packages needed.
- The website needs Flask: `py -m pip install -r requirements-all.txt`.
- `main.py` is the single source of truth for the console menu.
- Reports live in `reports/`, the static site in `docs/`.