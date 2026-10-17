# Troubleshooting

## `python` command not found / opens Microsoft Store
Use the `py` launcher instead of `python`, or double-click `run.bat`.

## `.venv` / `venv` errors
The bundled `.venv` is broken (it points to a removed WindowsApps Python).
Use the global Python 3.13 with the `py` launcher. All dependencies are
already installed there.

## ModuleNotFoundError (e.g. win32api, customtkinter, pandas)
Install with:  `py -m pip install -r requirements-all.txt`
Or individually: `py -m pip install pandas pywin32 customtkinter`

## win10toast / pkg_resources error
setuptools>=82 removed pkg_resources. Fix with: `py -m pip install "setuptools<82"`

## Charvis / Voice Assistant not starting
Needs a working microphone and the packages above. Run option 12 (Environment
Check) to verify modules.

## Flask app (PayPal Clone)
Run option 11 or `run_web_app.bat`, then open http://127.0.0.1:5000
If database errors occur, delete `instance/paypal_clone.db` and run again.

## auro.py / d.py failures
These use Instagram endpoints and may be blocked or require a session.
They are not essential to the all-in-one.

## toggle_desktop_icons.py
Windows-only; needs pywin32.

## Menu shows "Out of range"
Use number (1-142), n = next page, p = prev page, 0 = exit.

## Compile check
Run `test.bat` or `build.bat` to recompile everything and regenerate reports.
See PROGRAM_CATALOGUE.md and TEST_REPORT.md.