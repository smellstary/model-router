@echo off
REM === XiaoYuan x Oriental Wisdom Agent - Windows Launcher ===
REM Double-click to start. Close this window to stop.

chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo   XiaoYuan x Oriental Wisdom Agent - Starting Backend
echo ============================================================
echo.

REM ---- Find Python ----
set PY=
where python >nul 2>&1
if %errorlevel%==0 (
    for /f "delims=" %%i in ('where python') do set "PY=%%i" & goto :found_py
)
where python3 >nul 2>&1
if %errorlevel%==0 (
    for /f "delims=" %%i in ('where python3') do set "PY=%%i" & goto :found_py
)
echo [ERROR] Python not found. Install Python 3.10+ from https://www.python.org/downloads/
echo         Remember to check "Add Python to PATH" during install.
pause
exit /b 1

:found_py
for %%P in ("%PY%") do set "PYDIR=%%~dpP"
echo [OK] Python found: %PY%
%PY% --version

REM ---- Change to script directory ----
cd /d "%~dp0"
echo [OK] Working dir: %cd%

REM ---- Virtual env ----
if not exist ".venv\Scripts\python.exe" (
    echo [SETUP] Creating virtual environment .venv ...
    %PY% -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo [OK] Activating .venv ...
call .venv\Scripts\activate.bat
python --version

REM ---- Install deps ----
python -c "import flask, flask_cors" 2>nul
if errorlevel 1 (
    echo [SETUP] Installing dependencies (flask, flask-cors) ...
    python -m pip install --upgrade pip
    python -m pip install flask flask-cors
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo [OK] Dependencies already installed
)

REM ---- Env vars (dev-friendly defaults) ----
set "HOST=0.0.0.0"
set "PORT=5000"
set "DEBUG=false"
set "ENABLE_IP_WHITELIST=false"
set "ALLOW_ALL_ORIGINS=true"
set "ENABLE_RATE_LIMITING=true"

echo.
echo ============================================================
echo   Config:
echo     HOST              = %HOST%
echo     PORT              = %PORT%
echo     IP_WHITELIST      = %ENABLE_IP_WHITELIST%
echo     CORS_OPEN         = %ALLOW_ALL_ORIGINS%
echo     RATE_LIMITING     = %ENABLE_RATE_LIMITING%
echo.
echo   Endpoints:
echo     Health   : GET  http://127.0.0.1:%PORT%/health
echo     Dialog   : POST http://127.0.0.1:%PORT%/api/dialog   ^<-- XiaoYuan uses this
echo     Status   : GET  http://127.0.0.1:%PORT%/api/status
echo     Webhook  : POST http://127.0.0.1:%PORT%/webhook/openclaw
echo.
echo   XiaoYuan call example (PowerShell):
echo     Invoke-RestMethod -Uri "http://127.0.0.1:%PORT%/api/dialog" ^
echo       -Method Post -ContentType "application/json" ^
echo       -Body '{\"message\":\"hello\",\"user_id\":\"xiaoyuan\"}'
echo.
echo   Starting... (close this window to stop the server)
echo ============================================================
echo.

python integration\api_server_secure.py

pause
