import os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
NEW = os.path.join(ROOT, "programs", "general")
PROGS = os.path.join(ROOT, "programs", "utilities")

def run_test(path, name):
    # feed a few safe inputs, bounded by timeout
    try:
        r = subprocess.run(
            [PY, os.path.basename(path)],
            cwd=os.path.dirname(path),
            input="1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n",
            capture_output=True, text=True, timeout=8,
        )
        return r.returncode == 0, r.stderr.strip()[:120]
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except Exception as e:
        return False, str(e)[:120]

def collect(folder):
    if not os.path.isdir(folder):
        return []
    return sorted(os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".py"))

rows = []
for folder in (NEW, PROGS):
    for path in collect(folder):
        name = os.path.splitext(os.path.basename(path))[0]
        ok, err = run_test(path, name)
        rows.append((name, os.path.relpath(path, ROOT), ok, err))

passed = sum(1 for r in rows if r[2])
failed = [(r[0], r[3]) for r in rows if not r[2]]

REPORTS = os.path.join(ROOT, "reports")
os.makedirs(REPORTS, exist_ok=True)

with open(os.path.join(REPORTS, "TEST_REPORT.md"), "w", encoding="utf-8") as f:
    f.write("# Test Report (automated smoke test)\n\n")
    f.write(f"- Total tested: {len(rows)}\n- Passed: {passed}\n- Failed: {len(failed)}\n\n")
    f.write("| Program | Path | Result | Note |\n|---|---|---|---|\n")
    for name, path, ok, err in rows:
        f.write(f"| {name} | {path} | {'Pass' if ok else 'Fail'} | {err if err else ''} |\n")

print("Tested:", len(rows), "Passed:", passed, "Failed:", len(failed))
for n, e in failed:
    print("FAIL", n, e)