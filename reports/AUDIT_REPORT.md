# Audit Report

- Total Python programs: 297
- Original programs: 161
- New programs: 136
- Compile failures: 0
- Total files (excl. venv): 396
- Total folders (excl. venv): 51

## Removed / Renamed
- `.pytest_cache` removed (junk).
- `pd.html` removed (empty).
- `98.py` -> `98.jsx` (React code).
- `pw.py` -> `pw.jsx` (React code).
- `ga.py` -> `ga.cs` (C#/Unity code).
- `m.py` -> `m_snippet.txt` (incomplete snippet).
- `app.py` trailing pip output removed.

## Missing Dependencies (installed globally)
- pandas, openpyxl, instaloader, pywin32, customtkinter, comtypes, pycaw, SpeechRecognition, pyttsx3, wolframalpha, setuptools<82.

## Remaining Limitations
- `.venv` is broken (points to missing WindowsApps Python); using global Python.
- `auro.py`, `d.py` depend on Instagram APIs; may fail at runtime.
- Voice programs need a microphone.
- toggle_desktop_icons.py is Windows-only.
- Some programs need network (wolframalpha, pytube).
