# =============================================================================
# install-lmstudio-runtime.ps1
# 将 MUSA 后端注册为 LM Studio 0.4.28 的自定义 llama.cpp 运行时模块
#
# 原理：在 LM Studio 的 runtimes 目录下创建一个名为
#       llama.cpp-win-x86_64-musa-avx2@2.50.0 的模块，
#       其中 llama-server 通过 WSL2 调用 MUSA 加速的 Linux 二进制。
#
# 注意：此方法为实验性功能。LM Studio 原生期望 Windows .exe，
#       本脚本使用 .cmd 包装器转发到 WSL2。如不生效，请使用
#       start-musa-server.ps1 + openai-compat-endpoint 插件方案。
# =============================================================================
param(
    [string]$WslDistro = "Ubuntu",
    [string]$BuildDir = "$HOME/llama-musa-dist",
    [string]$LlamaVersion = "2.50.0"
)

$ErrorActionPreference = "Stop"

Write-Host "=== LM Studio MUSA 运行时模块安装器 ===" -ForegroundColor Cyan
Write-Host ""

# ---- 定位 LM Studio runtimes 目录 ----
$lmstudioHome = Join-Path $env:USERPROFILE ".lmstudio"
$runtimesRoot = Join-Path $lmstudioHome "runtimes"
$llamaRuntimes = Join-Path $runtimesRoot "llama.cpp"

if (-not (Test-Path $lmstudioHome)) {
    Write-Host "[ERROR] 未找到 LM Studio 数据目录: $lmstudioHome" -ForegroundColor Red
    Write-Host "        请先安装并启动一次 LM Studio 0.4.28。" -ForegroundColor Red
    exit 1
}

New-Item -ItemType Directory -Force -Path $llamaRuntimes | Out-Null
Write-Host "[INFO] LM Studio runtimes 目录: $llamaRuntimes"

# ---- 创建 MUSA 运行时模块目录 ----
$moduleName = "llama.cpp-win-x86_64-musa-avx2@$LlamaVersion"
$modulePath = Join-Path $llamaRuntimes $moduleName

if (Test-Path $modulePath) {
    Write-Host "[WARN] 模块已存在，将覆盖: $moduleName" -ForegroundColor Yellow
    Remove-Item -Recurse -Force $modulePath
}
New-Item -ItemType Directory -Force -Path $modulePath | Out-Null
Write-Host "[INFO] 创建模块目录: $modulePath"

# ---- 创建 llama-server 包装器 (.cmd) ----
$wrapperContent = @"
@echo off
REM LM Studio MUSA 运行时 - llama-server WSL2 包装器
REM 将 LM Studio 的参数转发到 WSL2 中的 MUSA llama-server

setlocal enabledelayedexpansion

set "WSL_DISTRO=$WslDistro"
set "BUILD_DIR=$BuildDir"
set "LD_LIB=%BUILD_DIR%/lib"

REM 将 Windows 路径参数转换为 WSL 路径
set "ARGS="
:parse_args
if "%~1"=="" goto run
set "ARG=%~1"
REM 如果参数是 Windows 路径，转换为 WSL 路径
echo !ARG! | findstr /R "^[A-Za-z]:\\.*" >nul 2>&1
if !errorlevel! equ 0 (
    for /f "delims=" %%i in ('wsl -d %WSL_DISTRO% wslpath -a "!ARG:\=/!"') do set "ARG=%%i"
)
set "ARGS=!ARGS! !ARG!"
shift
goto parse_args

:run
wsl -d %WSL_DISTRO% bash -c "export LD_LIBRARY_PATH='%LD_LIB%':\$LD_LIBRARY_PATH && '%BUILD_DIR%/bin/llama-server'!ARGS!"
endlocal
"@

$wrapperPath = Join-Path $modulePath "llama-server.cmd"
Set-Content -Path $wrapperPath -Value $wrapperContent -Encoding ASCII
Write-Host "[INFO] 创建 llama-server 包装器: llama-server.cmd"

# ---- 创建 package.json 元数据 ----
$packageJson = @{
    name = "llama.cpp-win-x86_64-musa-avx2"
    version = $LlamaVersion
    description = "llama.cpp MUSA backend (Moore Threads) via WSL2"
    os = "win32"
    arch = "x64"
    backend = "musa"
    features = @("avx2")
    entry = "llama-server.cmd"
    supported_formats = @("gguf")
} | ConvertTo-Json -Depth 5

$packagePath = Join-Path $modulePath "package.json"
Set-Content -Path $packagePath -Value $packageJson -Encoding UTF8
Write-Host "[INFO] 创建 package.json"

# ---- 创建 VERSION 信息 ----
$versionInfo = @"
llama.cpp MUSA runtime for LM Studio 0.4.28 (Build 2)
=====================================================
llama.cpp version : $LlamaVersion
backend           : musa (Moore Threads)
architecture      : win-x86_64
features          : avx2
bridge            : WSL2 -> $BuildDir/bin/llama-server
created           : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
"@
Set-Content -Path (Join-Path $modulePath "VERSION.txt") -Value $versionInfo -Encoding UTF8

# ---- 创建一个空的 .dll 占位（部分 LM Studio 版本会检查） ----
# 实际运行时库在 WSL2 中，此处仅创建占位以满足目录结构期望
New-Item -ItemType Directory -Force -Path (Join-Path $modulePath "lib") | Out-Null

Write-Host ""
Write-Host "[SUCCESS] MUSA 运行时模块已安装!" -ForegroundColor Green
Write-Host "  模块名: $moduleName"
Write-Host "  路径:   $modulePath"
Write-Host ""
Write-Host "=== 启用方法 ===" -ForegroundColor Cyan
Write-Host "1. 重启 LM Studio"
Write-Host "2. 进入 Settings → Hardware (或 Runtime)"
Write-Host "3. 在 llama.cpp 运行时列表中查找 'musa' 后端"
Write-Host "4. 选择该后端并加载模型"
Write-Host ""
Write-Host "如果 LM Studio 未识别该模块，请改用 start-musa-server.ps1 + openai-compat-endpoint 插件方案。" -ForegroundColor Yellow
