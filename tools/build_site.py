"""
Generate the static site for GitHub Pages.

GitHub Pages cannot run Python, so this builds:
  * a catalogue of all 133 programs (real data read from the source files)
  * a browser runner for a large subset, implemented in JavaScript
  * static pages: home, programs, categories, setup, api docs, about

Output: docs/index.html, docs/programs.html, ... and docs/assets/*
"""

import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# GitHub Pages serves a project site (https://<user>.github.io/<repo>/) from
# this folder, so the generated static site has to live in docs/.
SITE = os.path.join(ROOT, "docs")
ASSETS = os.path.join(SITE, "assets")
sys.path.insert(0, os.path.join(ROOT, "webapp"))

from app import discover_programs, catalogue_stats  # noqa: E402

# --- where the project lives -------------------------------------------------
OWNER = "Abhijeet-Kumar-Prajapati"
REPO = "pylab-studio"
REPO_URL = f"https://github.com/{OWNER}/{REPO}"
PAGES_URL = f"https://{OWNER.lower()}.github.io/{REPO}/"
# GitHub Pages cannot host the generated zip (it is git-ignored and Pages only
# serves what is committed), so the public pages always point at GitHub's own
# archive of the branch, which exists by definition.
DOWNLOAD_URL = f"{REPO_URL}/archive/refs/heads/main.zip"

# Local copy produced by build_zip(); handy when serving the site from disk.
ZIP_NAME = "pylab-studio-project.zip"

# Never bundle these: version-control data, caches, virtualenvs, or the
# nested "multi-program--code-main" folder (an accidental unzip of this very
# repository, which would double the archive).
ZIP_EXCLUDE_DIRS = {
    ".git", "__pycache__", "build", "archive", "node_modules",
    "venv", ".venv", "site", "multi-program--code-main",
}

DEMOABLE = {
    # math
    "add_two_numbers", "subtract_two_numbers", "multiply_two_numbers",
    "divide_two_numbers", "power", "square_root", "factorial", "prime_check",
    "fibonacci_inline", "gcd_two", "lcm_two", "average", "minimum", "maximum",
    "percentage", "area_circle", "area_rectangle", "area_triangle",
    "perimeter_circle", "volume_cube", "volume_sphere", "distance_formula",
    "quadratic_solver", "digit_sum", "armstrong", "perfect_number",
    "strong_number", "harshad", "automorphic", "neon", "spy_number",
    "tech_number", "divisors", "factor_pairs", "multiples", "even_odd",
    "absolute", "round_num", "floor", "ceil", "natural_log", "log10", "exp",
    "sin_deg", "cos_deg", "tan_deg", "sum_natural", "sum_squares", "sum_cubes",
    "multiplication_table", "factorial_table", "prime_list", "pyramid",
    "diamond", "pascal_triangle", "ascii_art",
    # converters
    "celsius_to_fahrenheit", "fahrenheit_to_celsius", "temperature_converter_extended",
    "km_to_miles", "miles_to_km", "kg_to_pounds", "pounds_to_kg",
    "meters_to_feet", "feet_to_meters", "hours_to_minutes", "minutes_to_seconds",
    "binary_to_decimal", "decimal_to_binary", "decimal_to_hex", "hex_to_decimal",
    "number_to_words",
    # strings
    "reverse_string", "palindrome_check", "word_count", "char_count", "uppercase",
    "lowercase", "title_case", "remove_spaces", "count_vowels", "sort_words",
    "remove_duplicates", "caesar_encrypt", "caesar_decrypt", "base64_encode",
    "base64_decode",
    # finance
    "simple_interest", "compound_interest", "loan_emi", "discount",
    "profit_loss", "tax",
    # health
    "bmi_calculator", "water_intake", "heart_rate_zones", "calorie_estimate",
    # games
    "coin_tosses", "dice_roll_d6", "dice_roll_custom", "rock_paper_scissors",
    "guess_number_game",
    # utility
    "password_generator", "quick_password", "random_number", "random_string",
    "countdown_timer", "stopwatch", "quote_generator", "tip_calculator",
    "age_calculator", "leap_year", "day_of_week", "days_between", "system_info",
    "current_time", "timestamp", "mad_libs",
    # list_directory reads the local filesystem, so it cannot run in a browser
}


def build_zip():
    """Create the downloadable package next to the generated pages."""
    target = os.path.join(SITE, ZIP_NAME)
    count = 0
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as bundle:
        for dirpath, dirnames, filenames in os.walk(ROOT):
            dirnames[:] = [d for d in dirnames
                           if d not in ZIP_EXCLUDE_DIRS and not d.endswith(".egg-info")]
            for filename in filenames:
                if filename.endswith((".pyc", ".zip")):
                    continue
                full = os.path.join(dirpath, filename)
                bundle.write(full, os.path.relpath(full, ROOT))
                count += 1
    size_mb = os.path.getsize(target) / (1024 * 1024)
    print(f"Package written to {target}  ({count} files, {size_mb:.1f} MB)")
    return target


def render(html):
    """Fill in the repository links.

    HEAD.format() has already run by the time a page constant exists, so the
    placeholders inside the page *body* still need substituting here.
    """
    return (html
            .replace("{DOWNLOAD_URL}", DOWNLOAD_URL)
            .replace("{REPO_URL}", REPO_URL)
            .replace("{PAGES_URL}", PAGES_URL)
            .replace("{REPO}", REPO))


def page(title, body):
    """Render one page: substitute into the shared HEAD, then into the body."""
    return render(HEAD.format(
        title=title,
        body=body,
        REPO_URL=REPO_URL,
        DOWNLOAD_URL=DOWNLOAD_URL,
        PAGES_URL=PAGES_URL,
        REPO=REPO,
    ))


def main():
    os.makedirs(ASSETS, exist_ok=True)
    programs = discover_programs()
    stats = catalogue_stats()

    payload = []
    for item in programs:
        payload.append({
            "n": item["number"],
            "id": item["id"],
            "slug": item["slug"],
            "name": item["name"],
            "cat": item["category"],
            "desc": item["description"],
            "group": item["group"],
            "path": item["path"],
            "web": item["slug"] in DEMOABLE,
        })

    with open(os.path.join(ASSETS, "data.js"), "w", encoding="utf-8") as f:
        f.write("// Auto-generated from the Python source catalogue.\n")
        f.write("window.PROGRAMS = " + json.dumps(payload, ensure_ascii=False, indent=0) + ";\n")
        f.write("window.STATS = " + json.dumps(stats, ensure_ascii=False) + ";\n")

    for filename, template in (
        ("index.html", INDEX_HTML),
        ("programs.html", PROGRAMS_HTML),
        ("categories.html", CATEGORIES_HTML),
        ("setup.html", SETUP_HTML),
        ("api.html", API_HTML),
        ("about.html", ABOUT_HTML),
        ("run.html", RUN_HTML),
    ):
        with open(os.path.join(SITE, filename), "w", encoding="utf-8") as f:
            f.write(render(template))

    # assets/style.css, site.js and demos.js are hand-written and kept as real files.
    build_zip()
    print("Static site written to", SITE)
    print("Public URL:", PAGES_URL)
    print("Programs in catalogue:", len(payload))
    print("Runnable in browser:", sum(1 for p in payload if p["web"]))


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="133 Python programs - maths, converters, strings, games, finance and health. Run them in the browser, no installation needed.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-theme="dark">
<header class="topbar"><div class="wrap bar">
  <a class="brand" href="index.html"><span class="logo">Py</span><span>PyLab<strong>Studio</strong></span></a>
  <nav>
    <a href="index.html">Home</a>
    <a href="programs.html">Programs</a>
    <a href="run.html">Runner</a>
    <a href="categories.html">Categories</a>
    <a href="setup.html">Setup</a>
    <a href="api.html">API</a>
    <a href="about.html">About</a>
    <a class="dl" href="{DOWNLOAD_URL}" download>Download</a>
  </nav>
  <button class="theme" id="themeBtn" title="Toggle theme">&#9681;</button>
</div></header>
<main>{body}</main>
<footer class="footer"><div class="wrap foot">
  <div><p><strong>PyLab Studio</strong></p>
  <p class="dim">Runs in your browser. No server, no installation.</p></div>
  <div class="dim">
    <a href="{REPO_URL}">GitHub</a> &middot;
    <a href="{REPO_URL}/blob/main/README.md">README</a>
  </div>
</div></footer>
<script src="assets/data.js"></script>
<script src="assets/demos.js"></script>
<script src="assets/site.js"></script>
</body></html>
"""

INDEX_HTML = page("PyLab Studio", body="""
<section class="hero"><div class="wrap">
  <span class="pill">133 Python programs &middot; runs in your browser</span>
  <h1>Every program,<br>right in the browser.</h1>
  <p class="lead">Maths, converters, string tools, games, finance and health.
     No install, no server, no internet needed.</p>
  <div class="cta">
    <a class="btn big" href="run.html">Open the runner</a>
    <a class="btn ghost big" href="programs.html">Browse all programs</a>
    <a class="btn ghost big" href="{DOWNLOAD_URL}" download>&#11015; Download project (.zip)</a>
  </div>
</div></section>

<section class="wrap">
  <div class="stats">
    <div class="stat"><b id="sTotal">133</b><span>programs</span></div>
    <div class="stat"><b id="sCats">11</b><span>categories</span></div>
    <div class="stat"><b id="sWeb">0</b><span>runnable here</span></div>
    <div class="stat"><b>0</b><span>setup cost</span></div>
  </div>
</section>

<section class="wrap">
  <h2 class="sec">Try it now</h2>
  <div class="grid" id="quickGrid"></div>
</section>

<section class="wrap">
  <h2 class="sec">Why it works offline</h2>
  <div class="grid three">
    <article class="card"><h3>&#9881; Runs client side</h3>
      <p>Every demo is plain JavaScript. Nothing is sent anywhere, nothing is loaded from a server.</p></article>
    <article class="card"><h3>&#128269; Instant</h3>
      <p>Open the runner, type your values, get the answer. No compile step, no waiting.</p></article>
    <article class="card"><h3>&#128203; Full Python too</h3>
      <p>This site mirrors the Python project. Clone it and run all 133 programs locally.</p></article>
  </div>
  <p class="center"><a class="btn ghost" href="{REPO_URL}">View on GitHub &rarr;</a></p>
</section>
""")

PROGRAMS_HTML = page(title="Programs - PyLab Studio", body="""
<section class="wrap">
  <h1 class="sec">All programs</h1>
  <form class="filters" id="filters">
    <input type="search" id="q" placeholder="Search by name, description or file...">
    <select id="cat"><option value="">All categories</option></select>
    <select id="grp"><option value="">All collections</option></select>
    <button type="button" id="go">Search</button>
    <a class="btn ghost" href="programs.html">Reset</a>
  </form>
  <p class="dim" id="count"></p>
  <div class="grid" id="grid"></div>
</section>
""")

CATEGORIES_HTML = page(title="Categories - PyLab Studio", body="""
<section class="wrap">
  <h1 class="sec">Categories</h1>
  <p class="lead" id="intro"></p>
  <div id="cats"></div>
</section>
""")

SETUP_HTML = page(title="Setup - PyLab Studio", body="""
<section class="wrap">
  <h1 class="sec">Setup</h1>
  <p class="lead">This website needs nothing. The full Python project needs Python 3.8+.</p>

  <div class="panel">
    <h3>1. Clone the project</h3>
    <pre class="console">git clone {REPO_URL}.git
cd {REPO}</pre>
  </div>

  <div class="panel">
    <h3>2. Run the console menu</h3>
    <p>Zero dependencies &mdash; only the Python standard library.</p>
    <pre class="console">run.bat            # Windows
py main.py         # any platform</pre>
  </div>

  <div class="panel">
    <h3>3. Run the local website (all 133 programs)</h3>
    <pre class="console">py -m pip install flask
run_website.bat
# -> http://127.0.0.1:5001</pre>
    <p class="dim">The local site can execute the real Python programs. This public site
      runs JavaScript ports of the same algorithms.</p>
  </div>

  <div class="panel">
    <h3>4. Optional extras</h3>
    <pre class="console">py -m pip install -r requirements-all.txt</pre>
  </div>

  <div class="panel">
    <h3>5. Verify</h3>
    <pre class="console">test.bat
py webapp\\app.py --selftest     # Total: 133  Passed: 133  Failed: 0</pre>
  </div>

  <div class="panel">
    <h3>Download</h3>
    <p class="lead">Poora project ek zip me le jao aur offline use karo.</p>
    <a class="btn big" id="dlAll" href="{DOWNLOAD_URL}" download>&#11015; Download project (.zip)</a>
    <p class="dim">Zip me 133 programs + website + launchers sab shamil hai (koi venv nahi).</p>
    <p class="dim">GitHub se bhi: <a target="_blank" rel="noopener"
      href="{DOWNLOAD_URL}">archive/refs/heads/main.zip</a></p>
    <p class="dim">Ek single program bhi &mdash; catalogue page par har card me
      &ldquo;Download .py&rdquo; link hai.</p>
  </div>

  <div class="panel">
    <h3>Launchers</h3>
    <table class="tbl">
      <tr><th>File</th><th>Purpose</th></tr>
      <tr><td>run.bat</td><td>Console menu</td></tr>
      <tr><td>run_website.bat</td><td>Local website + browser</td></tr>
      <tr><td>run_web_app.bat</td><td>PayPal demo (port 5000)</td></tr>
      <tr><td>setup.bat</td><td>Check Python and pip</td></tr>
      <tr><td>test.bat</td><td>Compile + smoke test</td></tr>
      <tr><td>build.bat</td><td>Rebuild reports</td></tr>
      <tr><td>list-programs.bat</td><td>Print the catalogue</td></tr>
    </table>
  </div>
</section>
""")

API_HTML = page(title="REST API - PyLab Studio", body="""
<section class="wrap">
  <h1 class="sec">REST API</h1>
  <p class="lead">Available when you run the project locally: <code>http://127.0.0.1:5001</code></p>

  <div class="panel"><h3>GET /api/programs</h3>
    <pre class="console">curl http://127.0.0.1:5001/api/programs</pre>
    <pre class="console">[{ "number":1, "id":"general-absolute",
   "name":"Absolute", "category":"Math/Number",
   "description":"Returns the absolute value of a number.",
   "group":"General", "path":"programs/general/absolute.py" }]</pre></div>

  <div class="panel"><h3>GET /api/program/&lt;id&gt;</h3>
    <pre class="console">curl http://127.0.0.1:5001/api/program/general-area_circle</pre></div>

  <div class="panel"><h3>POST /api/run</h3>
    <pre class="console">curl -X POST http://127.0.0.1:5001/api/run \\
  -H "Content-Type: application/json" \\
  -d '{"id":"general-area_circle","input":"5"}'</pre>
    <pre class="console">{"ok":true,"returncode":0,"seconds":0.04,
 "stderr":"","stdout":"Radius: Area = 78.5398"}</pre></div>

  <div class="panel"><h3>GET /health &nbsp;&middot;&nbsp; /api/stats &nbsp;&middot;&nbsp; /download</h3>
    <pre class="console">curl http://127.0.0.1:5001/health
{"status":"ok","programs":133,"uptime":"0:04:12"}</pre></div>

  <div class="panel"><h3>Limits</h3>
    <ul class="steps">
      <li>Input max 4000 characters</li>
      <li>12 second timeout per run</li>
      <li>Only whitelisted folders can execute</li>
      <li>One process per run</li>
    </ul></div>
</section>
""")

ABOUT_HTML = page(title="About - PyLab Studio", body="""
<section class="wrap">
  <h1 class="sec">About</h1>
  <p class="lead">A personal Python project collected into one runnable place.</p>

  <div class="panel"><h3>What this is</h3>
    <p>133 small Python programs plus two front ends: a console menu and a local Flask website
       that can execute any program. This public page is the static mirror, with JavaScript
       ports so the demos work without any installation.</p></div>

  <div class="panel"><h3>Layout</h3>
    <table class="tbl">
      <tr><th>Path</th><th>Contents</th></tr>
      <tr><td><code>main.py</code></td><td>All-in-one console menu</td></tr>
      <tr><td><code>webapp/</code></td><td>Flask website that runs Python programs</td></tr>
      <tr><td><code>programs/general/</code></td><td>130 standalone programs</td></tr>
      <tr><td><code>programs/utilities/</code></td><td>Notes, contacts, timers, generators</td></tr>
      <tr><td><code>projects/</code></td><td>PayPal demo, Charvis voice assistant</td></tr>
      <tr><td><code>learning/</code>, <code>web/</code>, <code>android/</code></td><td>Earlier projects</td></tr>
    </table></div>

  <div class="panel"><h3>Design choices</h3>
    <ul class="steps">
      <li>Console programs use only the Python standard library</li>
      <li>Every program has a docstring, validation and a clean exit</li>
      <li>The local site runs each program in a fresh process with a timeout</li>
      <li>This public site runs entirely in the browser</li>
    </ul></div>
</section>
""")

RUN_HTML = page(title="Runner - PyLab Studio", body=""")
<section class="wrap">
  <h1 class="sec">Program runner</h1>
  <p class="lead">Pick a program, enter your values, get the result. Runs entirely in this browser.</p>
  <div class="filters">
    <input type="search" id="rq" placeholder="Search runnable programs...">
    <select id="rcat"><option value="">All categories</option></select>
  </div>
  <div class="runwrap">
    <div class="panel">
      <label for="picker">Program</label>
      <select id="picker"></select>
      <p class="dim" id="pdesc"></p>
      <label for="input">Input <span class="hint">(one value per line)</span></label>
      <textarea id="input" rows="6" placeholder="Example:&#10;5&#10;3"></textarea>
      <button class="btn big" id="runBtn">&#9654; Run</button>
      <button class="btn ghost" id="sampleBtn">Fill sample</button>
    </div>
    <div class="panel">
      <div class="outhead"><h3>Output</h3><button class="btn ghost sm" id="copyBtn">Copy</button></div>
      <pre class="console" id="out">Pick a program and press Run.</pre>
    </div>
  </div>
</section>
""")


if __name__ == "__main__":
    main()