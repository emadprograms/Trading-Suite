@echo off
TITLE Trading Suite
CLS

REM 1. Set Working Directory (Crucial for double-click)
REM Calculate project root (assumes this script is in dist/windows/)
CD /D "%~dp0..\.."

ECHO ==================================================
ECHO 🚀 Starting Trading Suite (Windows)...
ECHO ==================================================
ECHO 📂 Project Root: %CD%

REM 2. Check for Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO ❌ Python NOT found in PATH!
    ECHO    Please install Python 3.12 form python.org
    ECHO    Ensure "Add Python to PATH" is checked during installation.
    PAUSE
    EXIT /B
)

REM 3. Check/Create Virtual Environment
IF NOT EXIST "venv" (
    ECHO ⚠️  Virtual environment not found. Creating one...
    python -m venv venv
    IF %ERRORLEVEL% NEQ 0 (
        ECHO ❌ Failed to create venv. Is Python installed correctly?
        PAUSE
        EXIT /B
    )
    ECHO ✅ venv created.
    
    REM Activate and Install
    CALL venv\Scripts\activate
) ELSE (
    CALL venv\Scripts\activate
)

REM Always check/install dependencies
ECHO 📦 Checking dependencies...
python -m pip install -r requirements.txt

REM 4. Launch Application
ECHO ✅ Environment Active.
ECHO 🌟 Launching Home.py...
streamlit run Home.py

REM 5. Keep window open if it crashes
ECHO ❌ App exited.
PAUSE
