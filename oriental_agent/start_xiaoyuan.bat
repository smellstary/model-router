@echo off
REM ============================================================
REM  小缘 × 东方智慧智能体  ——  Windows 一键启动
REM  用法：双击本文件，或在 cmd / PowerShell 里运行
REM ============================================================

chcp 65001 >nul
setlocal

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║     小缘 × 东方智慧智能体 —— 后端启动                 ║
echo ╚══════════════════════════════════════════════════════╝
echo.

REM ---- 1. 找 Python ----
where python >nul 2>&1
if %errorlevel%==0 (
    set "PY=python"
) else (
    where python3 >nul 2>&1
    if %errorlevel%==0 (
        set "PY=python3"
    ) else (
        echo ❌ 找不到 Python，请先安装 Python 3.10+（^<https://www.python.org/downloads/^>）
        echo    安装时记得勾选 "Add Python to PATH"
        pause
        exit /b 1
    )
)

echo 🐍 Python 版本:
%PY% --version
echo.

REM ---- 2. 切换到脚本所在目录 ----
cd /d "%~dp0"

REM ---- 3. 检查/创建虚拟环境 ----
if not exist ".venv\Scripts\python.exe" (
    echo 📦 首次运行，创建虚拟环境 .venv ...
    %PY% -m venv .venv
    if errorlevel 1 (
        echo ❌ 创建虚拟环境失败
        pause
        exit /b 1
    )
)

echo 📦 激活虚拟环境...
call .venv\Scripts\activate.bat

REM ---- 4. 安装依赖（如果没装过 flask）----
%PY% -c "import flask, flask_cors" 2>nul
if errorlevel 1 (
    echo 📦 安装依赖...
    python -m pip install --upgrade pip
    python -m pip install flask flask-cors
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
) else (
    echo 📦 依赖已就绪
)

REM ---- 5. 环境变量（桌面开发友好默认值）----
set "HOST=0.0.0.0"
set "PORT=5000"
set "DEBUG=false"
set "ENABLE_IP_WHITELIST=false"
set "ALLOW_ALL_ORIGINS=true"
set "ENABLE_RATE_LIMITING=true"

echo.
echo ⚙️  配置:
echo    HOST               = %HOST%
echo    PORT               = %PORT%
echo    ENABLE_IP_WHITELIST = %ENABLE_IP_WHITELIST%
echo    ALLOW_ALL_ORIGINS   = %ALLOW_ALL_ORIGINS%
echo    ENABLE_RATE_LIMITING = %ENABLE_RATE_LIMITING%
echo.
echo 📍 关键接口:
echo    健康检查:   GET  http://127.0.0.1:%PORT%/health
echo    桌面对话:   POST http://127.0.0.1:%PORT%/api/dialog   ← 小缘用这个
echo    OpenClaw:   POST http://127.0.0.1:%PORT%/webhook/openclaw
echo    状态:       GET  http://127.0.0.1:%PORT%/api/status
echo.
echo 👉 小缘调用示例 (PowerShell):
echo    Invoke-RestMethod -Uri "http://127.0.0.1:%PORT%/api/dialog" ^
echo      -Method Post -ContentType "application/json" ^
echo      -Body '{\"message\":\"我想创业\",\"user_id\":\"xiaoyuan\"}'
echo.
echo 🚀 启动中... （关闭本窗口 = 停止服务）
echo.

python integration\api_server_secure.py

pause
