# =============================================================================
# start-musa-server.ps1
# 在 Windows 11 26H2 上启动 WSL2 中的 MUSA 加速 llama-server，并配置 LM Studio 连接
#
# 前置条件：
#   1. 已在 WSL2 (Ubuntu) 中运行 build-llama-musa-wsl2.sh 完成编译
#   2. 已安装摩尔线程 Windows 驱动（WSL2 GPU 透传需要）
#   3. 已有 GGUF 模型文件
#
# 用法：
#   .\start-musa-server.ps1 -ModelPath "C:\models\qwen3-8b-q4.gguf"
#   .\start-musa-server.ps1 -ModelPath "C:\models\qwen3-8b-q4.gguf" -GpuLayers 999 -Port 1234
# =============================================================================
param(
    [Parameter(Mandatory=$true)]
    [string]$ModelPath,

    [int]$GpuLayers = 999,
    [int]$Port = 1234,
    [int]$ContextSize = 8192,
    [string]$WslDistro = "Ubuntu",
    [string]$BuildDir = "$HOME/llama-musa-dist"
)

$ErrorActionPreference = "Stop"

Write-Host "=== LM Studio MUSA 后端启动器 ===" -ForegroundColor Cyan
Write-Host ""

# ---- 检查 WSL ----
$wsl = Get-Command wsl -ErrorAction SilentlyContinue
if (-not $wsl) {
    Write-Host "[ERROR] 未找到 wsl 命令。请先安装 WSL2: wsl --install" -ForegroundColor Red
    exit 1
}

# ---- 检查模型路径 ----
if (-not (Test-Path $ModelPath)) {
    Write-Host "[ERROR] 模型文件不存在: $ModelPath" -ForegroundColor Red
    exit 1
}

# 将 Windows 路径转换为 WSL 路径
$wslModelPath = wsl wslpath -a ($ModelPath -replace '\\', '/')
$wslModelPath = $wslModelPath.Trim()
Write-Host "[INFO] 模型 WSL 路径: $wslModelPath"

# ---- 检查编译产物 ----
$serverCheck = wsl -d $WslDistro bash -c "test -f '$BuildDir/bin/llama-server' && echo 'OK' || echo 'MISSING'"
if ($serverCheck.Trim() -ne "OK") {
    Write-Host "[ERROR] 未找到 llama-server 二进制: $BuildDir/bin/llama-server" -ForegroundColor Red
    Write-Host "        请先在 WSL2 中运行 build-llama-musa-wsl2.sh" -ForegroundColor Red
    exit 1
}

# ---- 检查端口占用 ----
$portInUse = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "[WARN] 端口 $Port 已被占用，尝试释放..." -ForegroundColor Yellow
    $proc = $portInUse | Select-Object -First 1 -ExpandProperty OwningProcess
    if ($proc) {
        Write-Host "       占用进程 PID: $proc"
        $choice = Read-Host "是否终止该进程? (y/N)"
        if ($choice -eq 'y' -or $choice -eq 'Y') {
            Stop-Process -Id $proc -Force
            Start-Sleep -Seconds 1
        } else {
            Write-Host "[ERROR] 端口被占用，无法启动。请使用 -Port 指定其他端口。" -ForegroundColor Red
            exit 1
        }
    }
}

# ---- 启动 MUSA llama-server ----
Write-Host ""
Write-Host "[INFO] 启动 MUSA 加速的 llama-server..." -ForegroundColor Green
Write-Host "       GPU 层数: $GpuLayers"
Write-Host "       上下文: $ContextSize"
Write-Host "       端口: $Port"
Write-Host ""

# 在 WSL2 中设置 LD_LIBRARY_PATH 并启动
$wslCmd = @"
export LD_LIBRARY_PATH='$BuildDir/lib':`$LD_LIBRARY_PATH
'$BuildDir/bin/llama-server' \
  --model '$wslModelPath' \
  --n-gpu-layers $GpuLayers \
  --ctx-size $ContextSize \
  --port $Port \
  --host 0.0.0.0 \
  --api-key lm-studio
"@

# 使用后台进程启动
$process = Start-Process -FilePath "wsl" `
    -ArgumentList "-d", $WslDistro, "bash", "-c", $wslCmd `
    -NoNewWindow `
    -PassThru

Write-Host "[INFO] llama-server 进程已启动 (PID: $($process.Id))" -ForegroundColor Green
Write-Host ""

# ---- 等待服务器就绪 ----
Write-Host "[INFO] 等待服务器就绪..." -ForegroundColor Yellow
$ready = $false
$maxWait = 60
$waited = 0
while (-not $ready -and $waited -lt $maxWait) {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:$Port/health" -TimeoutSec 2 -ErrorAction Stop
        if ($response.status -eq "ok" -or $response) {
            $ready = $true
        }
    } catch {
        Start-Sleep -Seconds 2
        $waited += 2
    }
}

if ($ready) {
    Write-Host "[SUCCESS] MUSA llama-server 已就绪!" -ForegroundColor Green
} else {
    Write-Host "[WARN] 服务器可能仍在加载模型，请稍候..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== LM Studio 连接配置 ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "在 LM Studio 中安装并配置 openai-compat-endpoint 插件:"
Write-Host "  1. 打开 LM Studio → 左侧栏 Plugins (拼图图标)"
Write-Host "  2. 搜索 openai-compat-endpoint 并安装 (推荐 nm-z/openai-compat-endpoint)"
Write-Host "  3. 插件设置中填写:"
Write-Host "     Base URL : http://localhost:$Port/v1"
Write-Host "     API Key  : lm-studio"
Write-Host "  4. 在聊天界面选择该 provider 即可使用 MUSA 加速推理"
Write-Host ""
Write-Host "服务地址: http://localhost:$Port"
Write-Host "健康检查: http://localhost:$Port/health"
Write-Host ""
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Yellow

# 保持进程运行，等待用户中断
try {
    $process.WaitForExit()
} catch {
    Write-Host ""
    Write-Host "[INFO] 正在停止服务器..." -ForegroundColor Yellow
    Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
    wsl -d $WslDistro bash -c "pkill -f 'llama-server' 2>/dev/null || true"
    Write-Host "[INFO] 服务器已停止。" -ForegroundColor Green
}
