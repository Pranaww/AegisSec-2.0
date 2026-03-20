@echo off
echo === AegisSec v2.0 Launcher ===

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed.
    pause
    exit /b
)

if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo [*] Installing dependencies...
pip install -r requirements.txt -q

echo [*] Launching AegisSec...
python main.py
pause
