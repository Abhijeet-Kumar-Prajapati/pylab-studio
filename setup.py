#!/usr/bin/env python3
"""
PyLab Studio - project setup
===========================

One command to get the whole project ready:

    py setup.py              # full setup (venv + dependencies + verify)
    py setup.py --check      # just report what is missing, change nothing
    py setup.py --no-venv    # install into the current interpreter
    py setup.py --force      # delete and rebuild the virtual environment
    py setup.py --skip-deps  # set up but do not touch pip

What it does
    1. Checks that a usable Python (3.8+) is running.
    2. Creates a local virtual environment in .venv (unless --no-venv).
    3. Installs the web dependencies, then the optional extras.
    4. Verifies the result: byte-compiles every program and runs the
       built-in self-test across the whole catalogue.
    5. Prints next steps.

Optional dependencies that fail to build (pyaudio needs PortAudio, for
example) are reported but never treated as a fatal error - every program in
programs/ is standard library only.
"""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
STAMP = VENV_DIR / ".pylab-setup-ok"

# Needed for the local website and the PayPal demo.
CORE_REQUIREMENTS = [
    "flask>=3.0",
    "flask-sqlalchemy>=3.1",
    "flask-login>=0.6",
    "flask-wtf>=1.2",
    "werkzeug>=3.0",
    "sqlalchemy>=2.0",
    "wtforms>=3.1",
    "email-validator>=2.0",
]

# Nice-to-have. A failure here never blocks the setup.
EXTRA_REQUIREMENTS = [
    "pyttsx3>=2.90",
    "SpeechRecognition>=3.10",
    "wikipedia>=1.4",
    "pyjokes>=0.8",
    "requests>=2.31",
    "pandas>=2.0",
    "openpyxl>=3.1",
]

MIN_PYTHON = (3, 8)

GREEN, RED, YELLOW, BLUE, DIM, RESET = (
    "\033[92m", "\033[91m", "\033[93m", "\033[96m", "\033[2m", "\033[0m",
)


def colour(text: str, code: str) -> str:
    return f"{code}{text}{RESET}" if sys.stdout.isatty() else text


def say(step: str, message: str) -> None:
    print(colour(f"[{step}]", BLUE), message)


def ok(message: str) -> None:
    print(colour("  OK  ", GREEN), message)


def warn(message: str) -> None:
    print(colour("  !   ", YELLOW), message)


def fail(message: str) -> None:
    print(colour("  X   ", RED), message)


def run(cmd, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)


# ---------------------------------------------------------------------------
# 1. interpreter
# ---------------------------------------------------------------------------
def check_interpreter() -> bool:
    say("1/5", "Checking Python interpreter")
    if sys.version_info < MIN_PYTHON:
        need = ".".join(map(str, MIN_PYTHON))
        have = ".".join(map(str, sys.version_info[:3]))
        fail(f"Python {need}+ required, this is {have}.")
        return False
    ok(f"Python {platform.python_version()} at {sys.executable}")
    if platform.system() == "Windows":
        ok(f"Platform Windows {platform.release()} ({platform.machine()})")
    else:
        ok(f"Platform {platform.system()} {platform.release()} ({platform.machine()})")
    return True


# ---------------------------------------------------------------------------
# 2. virtual environment
# ---------------------------------------------------------------------------
def venv_python(base: Path) -> Path:
    if platform.system() == "Windows":
        return base / "Scripts" / "python.exe"
    return base / "bin" / "python"


def create_venv(force: bool) -> Path | None:
    say("2/5", "Preparing virtual environment (.venv)")
    if force and VENV_DIR.exists():
        import shutil
        shutil.rmtree(VENV_DIR, ignore_errors=True)
        ok("Removed the old .venv")

    if VENV_DIR.exists() and venv_python(VENV_DIR).exists():
        ok(".venv already exists - reusing it")
        return venv_python(VENV_DIR)

    try:
        venv.EnvBuilder(with_pip=True, clear=False, symlinks=platform.system() != "Windows").create(VENV_DIR)
    except Exception as error:  # pragma: no cover - environment dependent
        warn(f"Could not create .venv ({error}). Using the current interpreter.")
        return None

    py = venv_python(VENV_DIR)
    ok(f"Created .venv -> {py}")
    return py


# ---------------------------------------------------------------------------
# 3. dependencies
# ---------------------------------------------------------------------------
def ensure_pip(python: Path) -> bool:
    result = run([str(python), "-m", "pip", "--version"])
    if result.returncode != 0:
        warn("pip is unavailable in this interpreter, skipping dependencies.")
        return False
    ok("pip is available")
    return True


def install(python: Path, packages: list[str], label: str) -> bool:
    say("3/5", f"Installing {label}")
    if not packages:
        return True
    result = run([str(python), "-m", "pip", "install", "--disable-pip-version-check",
                  "--quiet", *packages])
    if result.returncode == 0:
        ok(f"{len(packages)} {label} installed")
        return True
    warn(f"{label}: some packages could not be installed")
    tail = (result.stderr or result.stdout or "").strip().splitlines()[-4:]
    for line in tail:
        print(colour(f"       {line}", DIM))
    return False


# ---------------------------------------------------------------------------
# 4. verification
# ---------------------------------------------------------------------------
def verify(python: Path) -> bool:
    say("4/5", "Verifying every program byte-compiles")
    result = run([str(python), "-c",
                  "import compileall,sys;"
                  "sys.exit(0 if compileall.compile_dir('.', quiet=2,"
                  " rx=__import__('re').compile(r'(\\.venv|build|node_modules)')) else 1)"],
                 cwd=str(ROOT))
    if result.returncode != 0:
        fail("Some files failed to compile - see the output above.")
        return False
    ok("All Python files compile")

    say("5/5", "Running the catalogue self-test")
    result = run([str(python), str(ROOT / "webapp" / "app.py"), "--selftest"], cwd=str(ROOT))
    output = (result.stdout or "").strip()
    for line in output.splitlines()[:12]:
        print(colour(f"       {line}", DIM))
    if result.returncode != 0:
        fail("Self-test reported failures.")
        return False
    ok("Self-test passed")
    return True


def build_reports(python: Path) -> None:
    try:
        run([str(python), str(ROOT / "generate_reports.py")], cwd=str(ROOT))
    except Exception:
        pass


# ---------------------------------------------------------------------------
def report_missing() -> None:
    """--check mode: report what is absent without changing anything."""
    print()
    say("check", "Dependency status")
    try:
        import importlib.util
    except ImportError:
        fail("importlib is unavailable.")
        return

    required = {
        "flask": "local website",
        "flask_sqlalchemy": "PayPal demo",
        "flask_login": "PayPal demo",
        "pandas": "phone number tool",
        "requests": "Charvis AI",
        "pyttsx3": "voice assistant",
    }
    missing = []
    for module, purpose in required.items():
        found = importlib.util.find_spec(module) is not None
        print(f"  {'yes' if found else ' no'}  {module:<20} {purpose}")
        if not found:
            missing.append(module)

    print()
    if missing:
        warn(f"{len(missing)} package(s) missing. Run:  py setup.py")
    else:
        ok("Everything needed is installed.")

    catalogue = sorted(
        p.stem for folder in ("programs/general", "programs/utilities")
        for p in (ROOT / folder).glob("*.py")
    )
    print()
    say("check", f"Catalogue: {len(catalogue)} programs")
    print("       run.bat            console menu")
    print("       run_website.bat    PyLab Studio website on http://127.0.0.1:5001")


def main() -> int:
    parser = argparse.ArgumentParser(description="Set up PyLab Studio.")
    parser.add_argument("--check", action="store_true",
                        help="report status only, change nothing")
    parser.add_argument("--no-venv", action="store_true",
                        help="install into the current interpreter instead of .venv")
    parser.add_argument("--force", action="store_true",
                        help="delete and rebuild .venv first")
    parser.add_argument("--skip-deps", action="store_true",
                        help="do not install anything with pip")
    args = parser.parse_args()

    print()
    print(colour("  PyLab Studio", GREEN), colour("- project setup", DIM))
    print(colour("  " + "-" * 54, DIM))

    if args.check:
        report_missing()
        return 0

    if not check_interpreter():
        return 1

    python = sys.executable if args.no_venv else create_venv(args.force)
    if python is None:
        python = Path(sys.executable)

    if not args.skip_deps:
        if ensure_pip(python):
            install(python, CORE_REQUIREMENTS, "core packages")
            install(python, EXTRA_REQUIREMENTS, "optional packages")
    else:
        say("3/5", "Skipping dependency installation (--skip-deps)")

    healthy = verify(python)
    if healthy:
        build_reports(python)
        STAMP.parent.mkdir(parents=True, exist_ok=True)
        STAMP.write_text("ok", encoding="utf-8")

    print()
    print(colour("  " + "-" * 54, DIM))
    if healthy:
        print(colour("  Setup complete.", GREEN))
        print()
        print("    run.bat            console menu for every program")
        print("    run_website.bat    PyLab Studio in your browser")
        print("    test.bat           re-run the full test suite")
        print()
        print(colour(f"    Interpreter: {python}", DIM))
        print()
        return 0

    print(colour("  Setup finished with warnings.", YELLOW))
    print(colour("  The console programs need no dependencies and still work.", DIM))
    print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())