import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# Folders that must never be counted or compiled: virtualenvs, caches,
# build output, and "multi-program--code-main" (an accidental unzip of this
# repository that duplicates every program).
SKIP_DIRS = {
    ".venv", "venv", "__pycache__", "site-packages", ".git",
    "archive", "build", "node_modules", "multi-program--code-main",
}

def walk_py():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # skip venv and site-packages and pycache
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".py"):
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, ROOT)
                if "site-packages" in rel or "\\.venv\\" in rel:
                    continue
                out.append((rel, full))
    return sorted(out)

def compile_check(path):
    """Byte-compile the file in-process.

    A `py -m py_compile` subprocess per file used to take ~3 minutes for the
    whole project; compile() does the same job in-process in a second.
    """
    try:
        with open(path, "rb") as handle:
            compile(handle.read(), path, "exec")
        return True
    except (SyntaxError, ValueError, OSError):
        return False

def classify(rel):
    if rel.startswith("programs"):
        return "New"
    if rel in ("main.py", "generate_reports.py", "create_100_programs.py", "smoke_test.py", "program_registry.py"):
        return "New/Fixed"
    if rel.startswith("projects"):
        return "Original"
    if rel.startswith("learning"):
        return "Original/Fixed"
    return "Original"

py_files = walk_py()
rows = []
for rel, full in py_files:
    ok = compile_check(full)
    rows.append({"no": None, "name": os.path.splitext(os.path.basename(rel))[0], "path": rel, "status": classify(rel), "test": "Pass" if ok else "Fail"})

# assign numbers
for i, r in enumerate(rows, 1):
    r["no"] = i

# counts
total_files = 0
total_dirs = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    total_dirs += len(dirnames)
    total_files += len(filenames)

# write catalogue
with open(os.path.join(ROOT, "reports", "PROGRAM_CATALOGUE.md"), "w", encoding="utf-8") as f:
    f.write("# Program Catalogue\n\n")
    f.write(f"Total Python programs: {len(rows)}\n")
    f.write(f"Total files (excl. venv/site-packages): {total_files}\n")
    f.write(f"Total folders (excl. venv/site-packages): {total_dirs}\n\n")
    f.write("| No. | Program Name | File Path | Status | Test Result |\n")
    f.write("|---|---|---|---|---|\n")
    for r in rows:
        f.write(f"| {r['no']} | {r['name']} | {r['path']} | {r['status']} | {r['test']} |\n")

# write audit report
new_count = sum(1 for r in rows if r["status"].startswith("New"))
orig_count = sum(1 for r in rows if r["status"].startswith("Original"))
fail_count = sum(1 for r in rows if r["test"] == "Fail")
with open(os.path.join(ROOT, "reports", "AUDIT_REPORT.md"), "w", encoding="utf-8") as f:
    f.write("# Audit Report\n\n")
    f.write(f"- Total Python programs: {len(rows)}\n")
    f.write(f"- Original programs: {orig_count}\n")
    f.write(f"- New programs: {new_count}\n")
    f.write(f"- Compile failures: {fail_count}\n")
    f.write(f"- Total files (excl. venv): {total_files}\n")
    f.write(f"- Total folders (excl. venv): {total_dirs}\n\n")
    f.write("## Removed / Renamed\n")
    f.write("- `.pytest_cache` removed (junk).\n")
    f.write("- `pd.html` removed (empty).\n")
    f.write("- `98.py` -> `98.jsx` (React code).\n")
    f.write("- `pw.py` -> `pw.jsx` (React code).\n")
    f.write("- `ga.py` -> `ga.cs` (C#/Unity code).\n")
    f.write("- `m.py` -> `m_snippet.txt` (incomplete snippet).\n")
    f.write("- `app.py` trailing pip output removed.\n\n")
    f.write("## Missing Dependencies (installed globally)\n")
    f.write("- pandas, openpyxl, instaloader, pywin32, customtkinter, comtypes, pycaw, SpeechRecognition, pyttsx3, wolframalpha, setuptools<82.\n\n")
    f.write("## Remaining Limitations\n")
    f.write("- `.venv` is broken (points to missing WindowsApps Python); using global Python.\n")
    f.write("- `auro.py`, `d.py` depend on Instagram APIs; may fail at runtime.\n")
    f.write("- Voice programs need a microphone.\n")
    f.write("- toggle_desktop_icons.py is Windows-only.\n")
    f.write("- Some programs need network (wolframalpha, pytube).\n")

print("Generated PROGRAM_CATALOGUE.md and AUDIT_REPORT.md")
print("Total programs:", len(rows), "New:", new_count, "Original:", orig_count, "Fail:", fail_count)
