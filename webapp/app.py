"""
PyLab Studio - Website
=======================

A local web application that lists every program in the project and runs it
safely in the browser.

Pages
    /            Dashboard (stats + quick start)
    /programs    Browse / search / filter every program
    /run/<id>    Run one program (input form + live output)
    /categories  Category overview
    /setup       Install + run instructions, download package
    /about       About the project
    /api-docs    REST API reference
    /status      System status and self-test runner

JSON API
    GET  /api/programs      list every program
    GET  /api/program/<id>  one program
    POST /api/run           run a program
    GET  /health            liveness + program count
    GET  /api/stats         catalogue statistics

Run:
    py webapp/app.py
    py webapp/app.py --selftest     # run every program, report results
    py webapp/app.py --build-zip    # create the downloadable package

Then open: http://127.0.0.1:5001
"""

import os
import subprocess
import sys
import zipfile
from datetime import datetime

from flask import (Flask, Response, jsonify, render_template, request, send_file)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from program_registry import category_for, description_for  # noqa: E402

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(APP_DIR, "build")

SITE_NAME = "PyLab Studio"
SITE_TAGLINE = "Every Python program, one click away"

# folder, display group
PROGRAM_ROOTS = [
    (os.path.join("programs", "general"), "General"),
    (os.path.join("programs", "utilities"), "Utility"),
]

RUN_TIMEOUT = 12          # seconds per program run
SAMPLE_INPUT = "\n".join(["1"] * 12)
MAX_INPUT = 4000          # characters accepted from the browser
MAX_OUTPUT = 100_000      # characters of stdout/stderr returned to the browser


def _cap(text):
    """Trim runaway program output so one run cannot flood the page."""
    text = text or ""
    if len(text) <= MAX_OUTPUT:
        return text
    return text[:MAX_OUTPUT] + f"\n... [truncated at {MAX_OUTPUT:,} characters]"

# Prefilled examples for the "Fill sample" button, keyed by slug.
SAMPLE_INPUTS = {
    "add_two_numbers": "2\n3", "subtract_two_numbers": "5\n2",
    "multiply_two_numbers": "4\n3", "divide_two_numbers": "10\n2",
    "power": "2\n10", "square_root": "81", "factorial": "5",
    "factorial_table": "6", "prime_check": "7", "prime_list": "20",
    "fibonacci_inline": "8", "fibonacci_series": "8",
    "gcd_two": "12\n8", "gcd_range": "12\n4", "lcm_two": "4\n6",
    "lcm_range": "4\n3", "average": "2 4 6 8", "minimum": "5 2 9",
    "maximum": "5 2 9", "percentage": "20\n80",
    "area_circle": "5", "area_rectangle": "4\n3", "area_triangle": "6\n4",
    "perimeter_circle": "5", "volume_cube": "3", "volume_sphere": "3",
    "distance_formula": "0\n0\n3\n4", "quadratic_solver": "1\n-5\n6",
    "digit_sum": "123", "armstrong": "153", "perfect_number": "28",
    "strong_number": "145", "harshad": "18", "automorphic": "25",
    "neon": "9", "spy_number": "123", "tech_number": "3025",
    "divisors": "12", "factor_pairs": "12", "multiples": "3\n5",
    "even_odd": "4", "is_even": "8", "is_odd": "7", "absolute": "-5",
    "round_num": "3.6", "floor": "3.9", "ceil": "3.1",
    "natural_log": "2.718281828", "log10": "1000", "exp": "1",
    "sin_deg": "30", "cos_deg": "60", "tan_deg": "45",
    "sum_natural": "10", "sum_squares": "10", "sum_cubes": "10",
    "multiplication_table": "5", "pyramid": "4", "diamond": "4",
    "pascal_triangle": "5",
    "celsius_to_fahrenheit": "100", "fahrenheit_to_celsius": "212",
    "temperature_converter_extended": "0",
    "km_to_miles": "10", "miles_to_km": "6.21", "kg_to_pounds": "70",
    "pounds_to_kg": "154", "meters_to_feet": "100", "feet_to_meters": "328",
    "hours_to_minutes": "2", "minutes_to_seconds": "5",
    "binary_to_decimal": "1010", "decimal_to_binary": "10",
    "decimal_to_hex": "255", "hex_to_decimal": "ff", "number_to_words": "123",
    "reverse_string": "hello world", "palindrome_check": "level",
    "word_count": "the quick brown fox", "char_count": "hello",
    "uppercase": "hello world", "lowercase": "HELLO WORLD",
    "title_case": "hello world", "remove_spaces": "a b c",
    "count_vowels": "education", "sort_words": "banana apple cherry",
    "remove_duplicates": "a b a c b", "caesar_encrypt": "abc\n3",
    "caesar_decrypt": "def\n3", "base64_encode": "hi", "base64_decode": "aGk=",
    "simple_interest": "1000\n5\n2", "compound_interest": "1000\n10\n2\n4",
    "compound_interest_schedule": "1000\n10\n3", "loan_emi": "500000\n8\n240",
    "discount": "1000\n20", "profit_loss": "100\n120", "tax": "1000\n10",
    "bmi_calculator": "70\n1.75", "water_intake": "70",
    "heart_rate_zones": "30", "calorie_estimate": "70\n175\n30\nm",
    "dice_roll_d6": "3", "dice_roll_custom": "20\n2", "coin_tosses": "5",
    "password_generator": "16\n5", "quick_password": "12",
    "random_number": "1\n100", "random_string": "8",
    "tip_calculator": "1000\n15\n2", "age_calculator": "2005\n6\n15",
    "leap_year": "2024", "day_of_week": "2024\n1\n1",
    "days_between": "2024-01-01\n2024-01-10", "mad_libs": "cat\nruns\nhappy",
}

EXCLUDE_FROM_ZIP = {
    "archive", "build", "__pycache__", ".git", ".venv", "venv",
    "node_modules", "site", "multi-program--code-main",
}

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024  # 64 KB is plenty for an input box

# The site never signs a session, but Flask still wants a key. Generating one
# per process avoids shipping a hardcoded secret in a public repository.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(32)

STARTED_AT = datetime.now()


# --------------------------------------------------------------------------
# Security headers
# --------------------------------------------------------------------------
# The runner executes Python files, so the browser side is locked down as well:
# no remote scripts, no framing, no MIME sniffing, no referrer leaking the
# local URL. "unsafe-inline" is required for the small amount of inline CSS
# (progress bars, card sizing) that lives in the templates.
CSP = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data:; "
    "font-src 'self'; "
    "connect-src 'self'; "
    "form-action 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'none'; "
    "object-src 'none'"
)


@app.after_request
def add_security_headers(response):
    response.headers.setdefault("Content-Security-Policy", CSP)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("Permissions-Policy",
                                "geolocation=(), microphone=(), camera=()")
    response.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
    if request.path.startswith(("/api", "/health")):
        response.headers["Cache-Control"] = "no-store"
    return response


# --------------------------------------------------------------------------
# Discovery
# --------------------------------------------------------------------------
def _read_doc(path):
    """Return (title, category, description) parsed from the module docstring."""
    title = category = description = ""
    lines = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            for _ in range(24):
                line = handle.readline()
                if not line:
                    break
                lines.append(line.rstrip("\n"))
    except OSError:
        pass

    if lines and lines[0].lstrip().startswith('"""'):
        block = [lines[0].strip().lstrip('"')]
        for line in lines[1:]:
            if line.rstrip().endswith('"""'):
                block.append(line.rstrip()[:-3].strip())
                break
            block.append(line)
        block = [b.strip() for b in block if b.strip()]
        if block:
            title = block[0]
        for item in block[1:]:
            if item.lower().startswith("category:"):
                category = item.split(":", 1)[1].strip()
            elif not item.lower().startswith("example:") and not item.startswith("    "):
                if not description:
                    description = item
    return title, category, description


def discover_programs():
    """Return the catalogue of runnable programs."""
    catalogue = []
    number = 0
    for relative, group in PROGRAM_ROOTS:
        folder = os.path.join(BASE_DIR, relative)
        if not os.path.isdir(folder):
            continue
        for filename in sorted(os.listdir(folder)):
            if not filename.endswith(".py"):
                continue
            path = os.path.join(folder, filename)
            slug = filename[:-3]
            title, category, description = _read_doc(path)
            number += 1
            catalogue.append({
                "number": number,
                "id": f"{group.lower()}-{slug}",
                "slug": slug,
                "name": title or " ".join(w.capitalize() for w in slug.split("_")),
                "category": category or category_for(slug),
                "description": description or description_for(slug),
                "group": group,
                "path": os.path.relpath(path, BASE_DIR).replace("\\", "/"),
                "size_kb": round(os.path.getsize(path) / 1024, 1),
                "sample": SAMPLE_INPUTS.get(slug, ""),
            })
    return catalogue


def find_program(program_id):
    for item in discover_programs():
        if item["id"] == program_id:
            return item
    return None


def catalogue_stats():
    programs = discover_programs()
    categories = {}
    for item in programs:
        categories[item["category"]] = categories.get(item["category"], 0) + 1
    return {
        "total": len(programs),
        "categories": len(categories),
        "groups": len(PROGRAM_ROOTS),
        "by_category": dict(sorted(categories.items())),
    }


# --------------------------------------------------------------------------
# Runner
# --------------------------------------------------------------------------
def run_program(program_id, stdin_text):
    """Execute one whitelisted program and capture its output."""
    program = find_program(program_id)
    if not program:
        return {"ok": False, "error": "Unknown program."}

    if len(stdin_text or "") > MAX_INPUT:
        return {"ok": False, "error": "Input is too long.", "stdout": "", "returncode": None}

    path = os.path.join(BASE_DIR, program["path"].replace("/", os.sep))
    resolved = os.path.realpath(path)
    if not resolved.startswith(os.path.realpath(BASE_DIR) + os.sep):
        return {"ok": False, "error": "Blocked: path outside project.",
                "stdout": "", "returncode": None}

    started = datetime.now()
    try:
        finished = subprocess.run(
            [sys.executable, resolved],
            cwd=os.path.dirname(resolved),
            input=(stdin_text or "") + "\n",
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT,
            errors="replace",
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Program took too long and was stopped.",
                "stdout": "", "returncode": None,
                "seconds": round((datetime.now() - started).total_seconds(), 2)}
    except Exception as error:  # pragma: no cover - defensive
        return {"ok": False, "error": str(error), "stdout": "", "returncode": None,
                "seconds": round((datetime.now() - started).total_seconds(), 2)}

    return {
        "ok": finished.returncode == 0,
        "stdout": _cap(finished.stdout),
        "stderr": _cap(finished.stderr.strip()),
        "returncode": finished.returncode,
        "seconds": round((datetime.now() - started).total_seconds(), 2),
    }


def self_test():
    """Run every catalogue program with safe input and report the result."""
    passed, failed = [], []
    for program in discover_programs():
        outcome = run_program(program["id"], SAMPLE_INPUT)
        (passed if outcome.get("ok") else failed).append(program["name"])
    print(f"Total: {len(passed) + len(failed)}  Passed: {len(passed)}  Failed: {len(failed)}")
    for name in failed:
        print("  FAIL:", name)
    return 0 if not failed else 1


# --------------------------------------------------------------------------
# Downloadable package
# --------------------------------------------------------------------------
def build_zip(target=None):
    """Create a downloadable zip of the whole project (excluding archives)."""
    target = target or os.path.join(BUILD_DIR, "pylab-studio-project.zip")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as bundle:
        for dirpath, dirnames, filenames in os.walk(BASE_DIR):
            dirnames[:] = [d for d in dirnames
                           if d not in EXCLUDE_FROM_ZIP and not d.endswith(".egg-info")]
            for filename in filenames:
                if filename.endswith((".pyc", ".zip")):
                    continue
                full = os.path.join(dirpath, filename)
                bundle.write(full, os.path.relpath(full, BASE_DIR))
    return target


def safe_program_path(program_id):
    """Resolve a catalogue id to a real path inside the project, or None."""
    program = find_program(program_id)
    if not program:
        return None
    path = os.path.join(BASE_DIR, program["path"].replace("/", os.sep))
    resolved = os.path.realpath(path)
    root = os.path.realpath(BASE_DIR)
    if not resolved.startswith(root + os.sep) or not os.path.isfile(resolved):
        return None
    return resolved, program


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
@app.route("/")
def index():
    stats = catalogue_stats()
    catalogue = discover_programs()
    featured = catalogue[:8]
    # Highest numbered programs are the newest additions; show those first.
    newest = list(reversed(catalogue[-6:]))
    return render_template("index.html", stats=stats, featured=featured,
                           newest=newest, site=SITE_NAME,
                           tagline=SITE_TAGLINE,
                           uptime=str(datetime.now() - STARTED_AT).split(".")[0])


@app.route("/programs")
def programs():
    catalogue = discover_programs()
    query = (request.args.get("q") or "").strip().lower()
    category = (request.args.get("category") or "").strip()
    group = (request.args.get("group") or "").strip()
    favourites = request.args.get("favourites")

    if query:
        catalogue = [p for p in catalogue
                     if query in p["name"].lower()
                     or query in p["description"].lower()
                     or query in p["path"].lower()]
    if category:
        catalogue = [p for p in catalogue if p["category"] == category]
    if group:
        catalogue = [p for p in catalogue if p["group"].lower() == group.lower()]

    categories = sorted({p["category"] for p in discover_programs()})
    groups = sorted({p["group"] for p in discover_programs()})

    if favourites:
        wanted = set(favourites)
        catalogue = [p for p in catalogue if p["id"] in wanted]

    return render_template(
        "programs.html",
        programs=catalogue,
        categories=categories,
        groups=groups,
        query=request.args.get("q", ""),
        category=category,
        group=group,
        favourites_only=favourites,
        site=SITE_NAME,
        total=len(discover_programs()),
    )


@app.route("/run/<program_id>", methods=["GET", "POST"])
def run(program_id):
    program = find_program(program_id)
    if not program:
        return render_template("missing.html", program_id=program_id), 404

    result = None
    if request.method == "POST":
        result = run_program(program_id, request.form.get("input", ""))

    related = [p for p in discover_programs()
               if p["category"] == program["category"] and p["id"] != program_id][:6]

    return render_template("run.html", program=program, result=result,
                           related=related, site=SITE_NAME)


@app.route("/categories")
def categories():
    stats = catalogue_stats()
    catalogue = discover_programs()
    by_category = {}
    for item in catalogue:
        by_category.setdefault(item["category"], []).append(item)
    return render_template("categories.html", stats=stats, by_category=by_category,
                           site=SITE_NAME)


@app.route("/setup")
def setup():
    zip_path = os.path.join(BUILD_DIR, "pylab-studio-project.zip")
    return render_template("setup.html", zip_ready=os.path.exists(zip_path),
                           zip_path=zip_path, stats=catalogue_stats(),
                           site=SITE_NAME)


@app.route("/about")
def about():
    return render_template("about.html", stats=catalogue_stats(), site=SITE_NAME)


@app.route("/api-docs")
def api_docs():
    return render_template("api_docs.html", stats=catalogue_stats(), site=SITE_NAME)


@app.route("/status")
def status():
    return render_template("status.html", stats=catalogue_stats(),
                           uptime=str(datetime.now() - STARTED_AT).split(".")[0],
                           python=sys.version.split()[0], site=SITE_NAME)


# --------------------------------------------------------------------------
# JSON API
# --------------------------------------------------------------------------
@app.route("/api/programs")
def api_programs():
    return jsonify(discover_programs())


@app.route("/api/program/<program_id>")
def api_program(program_id):
    program = find_program(program_id)
    if not program:
        return jsonify({"error": "not found"}), 404
    return jsonify(program)


@app.route("/api/run", methods=["POST"])
def api_run():
    payload = request.get_json(silent=True) or {}
    program_id = payload.get("id")
    if not program_id:
        return jsonify({"ok": False, "error": "Missing id."}), 400
    return jsonify(run_program(program_id, payload.get("input", "")))


@app.route("/api/stats")
def api_stats():
    return jsonify(catalogue_stats())


@app.route("/health")
def health():
    return jsonify({"status": "ok", "programs": len(discover_programs()),
                    "uptime": str(datetime.now() - STARTED_AT).split(".")[0],
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})


@app.route("/source/<program_id>")
def source(program_id):
    """Show the Python source of one program."""
    found = safe_program_path(program_id)
    if not found:
        return render_template("missing.html", program_id=program_id), 404
    resolved, program = found
    with open(resolved, "r", encoding="utf-8", errors="replace") as handle:
        code = handle.read()
    return render_template("source.html", program=program, code=code)


@app.route("/download/<program_id>")
def download_program(program_id):
    """Download a single program as a .py file."""
    found = safe_program_path(program_id)
    if not found:
        return render_template("missing.html", program_id=program_id), 404
    resolved, program = found
    return send_file(resolved, as_attachment=True,
                     download_name=os.path.basename(resolved))


@app.route("/export.csv")
def export_csv():
    """Export the whole catalogue as CSV."""
    import csv
    import io

    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer)
    writer.writerow(["Number", "ID", "Name", "Category", "Group", "Description", "Path"])
    for item in discover_programs():
        writer.writerow([item["number"], item["id"], item["name"], item["category"],
                         item["group"], item["description"], item["path"]])
    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=pylab-studio-catalogue.csv"},
    )


@app.route("/download")
def download():
    """Build the project package and send it."""
    path = build_zip()
    return send_file(path, as_attachment=True,
                     download_name="pylab-studio-project.zip")


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(self_test())
    if "--build-zip" in sys.argv:
        print("Package written to:", build_zip())
        raise SystemExit(0)

    # Loopback by default: this server can execute Python programs, so it must
    # not be reachable from the network unless you explicitly ask for it.
    #   set WEBSITE_HOST=0.0.0.0 to expose it on your LAN.
    host = os.environ.get("WEBSITE_HOST", "127.0.0.1")
    port = int(os.environ.get("WEBSITE_PORT", "5001"))
    stats = catalogue_stats()
    print("=" * 58)
    print(f"  {SITE_NAME.upper()}  |  {SITE_TAGLINE}")
    print("=" * 58)
    print(f"  Programs : {stats['total']}  |  Categories: {stats['categories']}")
    print(f"  Local    : http://127.0.0.1:{port}")
    print(f"  Download : http://127.0.0.1:{port}/download")
    if host not in ("127.0.0.1", "localhost"):
        print(f"  WARNING  : bound to {host} - your whole network can run code here.")
    print("  Stop     : Ctrl+C in this window")
    print("=" * 58)
    # Never enable the Werkzeug debugger here: it allows remote code execution.
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    if debug and host not in ("127.0.0.1", "localhost", "::1"):
        print("  ERROR    : FLASK_DEBUG=1 is only allowed on loopback.")
        raise SystemExit(1)
    app.run(host=host, port=port, debug=debug, threaded=True)