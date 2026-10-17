@echo off
title PyLab Studio - Tests
cd /d "%~dp0"
echo [1/4] Compile check on all .py files...
py -c "import compileall,sys,re; ok=compileall.compile_dir('.', force=True, quiet=1, rx=re.compile(r'multi-program--code-main')); sys.exit(0 if ok else 1)"
if errorlevel 1 (
    echo Some files failed to compile. See output above.
    pause
    exit /b 1
)
echo All .py files compile OK.

echo [2/4] Smoke-testing every program...
py smoke_test.py

echo [3/4] Running the full catalogue self-test...
py webapp\app.py --selftest

echo [4/4] Generating catalogue and audit report...
py generate_reports.py

echo.
echo Tests complete. See PROGRAM_CATALOGUE.md, AUDIT_REPORT.md, TEST_REPORT.md
pause