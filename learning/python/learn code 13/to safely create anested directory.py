"""Create a nested directory safely.

Uses a path inside the current project so it works on any machine and does
not depend on a particular user's home directory.
"""

from pathlib import Path

# Relative to this file: creates learning/python/learn code 13/demo/nested/dir
path = Path(__file__).resolve().parent / "demo" / "nested" / "dir"

path.mkdir(parents=True, exist_ok=True)
print(f"Created (or already existed): {path}")