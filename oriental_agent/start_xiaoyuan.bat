@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo   XiaoYuan x Oriental Wisdom Agent - Starting Backend
echo ============================================================
echo.

rem ---- Find Python ----
set "PY_CMD="
where python >nul 2>&1 && set "PY_CMD=python"
if not defined PY_CMD (
    where py >nul 2>&1 && set "PY_CMD=py -3"
)
if not defined PY_CMD (
    echo [FAIL] Python 3 not found in PATH.
    echo        Install from https://www.python.org and check "Add to PATH".
    pause
    exit /b 1
)

rem ---- Work dir ----
cd /d "%~dp0"
echo [OK] Work dir: %CD%

rem ---- Virtualenv ----
if exist ".venv\Scripts\python.exe" (
    set "PY_CMD=.venv\Scripts\python.exe"
    echo [OK] Using .venv
) else (
    rem Try create
    %PY_CMD% -m venv .venv 2>nul
    if exist ".venv\Scripts\python.exe" (
        set "PY_CMD=.venv\Scripts\python.exe"
        echo [OK] Created .venv
    )
)

rem ---- Install deps ----
"%PY_CMD%" -c "import flask, flask_cors, yaml, requests" >nul 2>&1
if errorlevel 1 (
    echo [..] Installing dependencies (flask, flask-cors, pyyaml, requests)...
    "%PY_CMD%" -m pip install flask flask-cors pyyaml requests --quiet
    if errorlevel 1 (
        echo [FAIL] pip install failed. Try: python -m pip install flask flask-cors pyyaml requests
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo [OK] Dependencies OK
)

rem ---- Clear Python caches ----
if exist "__pycache__" rmdir /s /q __pycache__ 2>nul
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" 2>nul

rem ---- Env ----
rem 唯一 HTTP 入口：integration\api_server_secure.py（对话内核是 core\agent.py）
if not defined DEBUG set "DEBUG=false"
if not defined ENABLE_IP_WHITELIST set "ENABLE_IP_WHITELIST=false"
if not defined ALLOW_ALL_ORIGINS set "ALLOW_ALL_ORIGINS=true"
if not defined HOST set "HOST=127.0.0.1"
if not defined PORT set "PORT=5000"

if "%API_KEYS%"=="" if "%API_KEY%"=="" if "%API_AUTH_TOKEN%"=="" if "%BEARER_TOKEN%"=="" (
    echo [FAIL] Set API_KEYS or API_AUTH_TOKEN before start. See integration\.env.example
    echo        DEBUG defaults to false.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Config:
echo     HOST              = %HOST%
echo     PORT              = %PORT%
echo     DEBUG             = %DEBUG%
echo     IP whitelist      = %ENABLE_IP_WHITELIST%
echo     CORS all origins  = %ALLOW_ALL_ORIGINS%
echo     Entry             = integration\api_server_secure.py
echo     Python            = %PY_CMD%
echo ============================================================
echo.
echo   XiaoYuan API:  http://127.0.0.1:%PORT%/api/dialog
echo   Health check:  http://127.0.0.1:%PORT%/health
echo.
echo   Press Ctrl+C to stop.
echo ============================================================
echo.

rem ---- Start with UTF-8 mode ----
"%PY_CMD%" -X utf8 integration\api_server_secure.py

pause
