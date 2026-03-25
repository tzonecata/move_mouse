@echo off
rem keep_unlock.bat - run keep_unlock.py from the script directory
cd /d "%~dp0"
rem Use the Python launcher if available, otherwise use python from PATH
where py >nul 2>&1
if %ERRORLEVEL%==0 (
    py -3 keep_unlock.py
) else (
    python keep_unlock.py
)