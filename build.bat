@echo off
title PyLab Studio - Build
cd /d "%~dp0"
echo Building: compiling all Python files...
py -c "import compileall,sys,re; ok=compileall.compile_dir('.', force=True, quiet=1, rx=re.compile(r'multi-program--code-main')); sys.exit(0 if ok else 1)"
if errorlevel 1 (
    echo BUILD FAILED: see compile errors above.
    pause
    exit /b 1
)
echo Build OK.
py generate_reports.py
echo Rebuilding the static site and the downloadable package...
py tools\build_site.py
echo Done. See PROGRAM_CATALOGUE.md, AUDIT_REPORT.md and site\.
pause