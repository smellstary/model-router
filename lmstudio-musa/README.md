# LM Studio 0.4.28 (Build 2) — MUSA 原生后端集成方案

## 概述

为 **Windows 11 26H2** 上的 **LM Studio 0.4.28 (Build 2)** 接入 llama.cpp 的 **MUSA 原生后端**（摩尔线程 GPU 加速）。

LM Studio 0.4.28 Build 2 内置的 llama.cpp 运行时版本为 **2.50.0**（upstream `b11337`）。本方案编译同版本 llama.cpp 并启用 `GGML_MUSA=ON`，通过 WSL2 桥接至 Windows 上的 LM Studio。

## ⚠️ 重要前提：为什么需要 WSL2？

| 项目 | 状态 |
|------|------|
| 摩尔线程 **MUSA SDK** | **仅 Linux**（Ubuntu / Kylin / Debian 等），无 Windows 版本 |
| llama.cpp `GGML_MUSA` 后端 | 上游 CMake 仅支持 Linux 路径（`/opt/musa`、`.so` 库） |
| 摩尔线程 **Windows 驱动** | ✅ 支持（提供图形与 Vulkan） |
| LM Studio 运行时模块 | Windows 原生 `.exe` / `.dll` |

因此 **MUSA 加速的 llama-server 必须在 WSL2 (Linux) 中编译和运行**，再通过网络端口供 Windows 上的 LM Studio 调用。

---

## 硬件支持矩阵

| GPU 型号 | MUSA 架构 | `MUSA_ARCHITECTURES` | MUSA SDK 版本 |
|----------|-----------|----------------------|---------------|
| MTT S80 / S3000 | CC 2.1 | `21` | 4.3.0 CC2.1+ |
| MTT S4000 | CC 2.2 | `22` | 4.3.0 CC2.2+ |
| MTT S5000 | CC 3.1 | `31` | 5.1.0 CC3.1+ |

> 架构 `21` 在新版 llama.cpp 中标记为 deprecated（不再测试），但仍可编译。

---

## 完整流程

### 第一步：安装 WSL2 与 Ubuntu

以**管理员身份**打开 PowerShell：

```powershell
wsl --install -d Ubuntu
```

安装完成后重启，设置 Ubuntu 用户名和密码。

### 第二步：在 WSL2 Ubuntu 中安装 MUSA SDK 与驱动

1. 从 <https://developer.mthreads.com/sdk/download/musa> 下载匹配你 GPU 的 **DEB** 包。
2. 传入 WSL2 并安装：

```bash
# 假设下载到 Windows 的 Downloads 文件夹
cd /mnt/c/Users/<你的用户名>/Downloads
sudo dpkg -i MUSA_SDK_*.deb
sudo apt-get install -f
```

3. 验证安装：

```bash
musaInfo          # 应输出 GPU 信息
ls /opt/musa/bin  # 应包含 clang、clang++
```

4. 安装编译依赖：

```bash
sudo apt update && sudo apt install -y git cmake build-essential clang pkg-config
```

### 第三步：编译 llama.cpp (MUSA 后端)

将 `build-llama-musa-wsl2.sh` 复制到 WSL2 中并执行：

```bash
# MTT S80 / S3000
bash build-llama-musa-wsl2.sh 21

# MTT S4000
bash build-llama-musa-wsl2.sh 22

# MTT S5000
bash build-llama-musa-wsl2.sh 31
```

编译产物位于 `~/llama-musa-dist/`：
- `bin/llama-server` — MUSA 加速推理服务器
- `bin/llama-cli` — 命令行推理
- `lib/` — 运行时库（含 MUSA 运行时）

### 第四步：在 Windows 端启动 MUSA 推理服务

```powershell
.\start-musa-server.ps1 -ModelPath "C:\models\Qwen3-8B-Q4_K_M.gguf"
```

参数说明：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-ModelPath` | 必填 | GGUF 模型的 Windows 路径 |
| `-GpuLayers` | `999` | 卸载到 GPU 的层数（999 = 全部） |
| `-Port` | `1234` | 服务监听端口 |
| `-ContextSize` | `8192` | 上下文窗口大小 |
| `-WslDistro` | `Ubuntu` | WSL 发行版名称 |

启动后服务监听 `http://localhost:1234`。

### 第五步：在 LM Studio 中连接（两种方案）

#### 方案 A（推荐）：openai-compat-endpoint 插件

1. 打开 LM Studio → 左侧栏 **Plugins**（拼图图标）。
2. 搜索并安装 **`nm-z/openai-compat-endpoint`**。
3. 插件设置中填写：
   - **Base URL**: `http://localhost:1234/v1`
   - **API Key**: `lm-studio`
4. 在聊天界面选择该 provider，即可使用 MUSA 加速推理。

#### 方案 B（实验性）：注册为 LM Studio 运行时模块

```powershell
.\install-lmstudio-runtime.ps1
```

这会在 `~/.lmstudio/runtimes/llama.cpp/` 下创建 `llama.cpp-win-x86_64-musa-avx2@2.50.0` 模块。重启 LM Studio 后在硬件设置中选择 `musa` 后端。

> ⚠️ 此方案依赖 LM Studio 接受 `.cmd` 包装器，不同版本行为可能不同。如不识别请使用方案 A。

---

## 验证 MUSA 加速生效

启动后观察 llama-server 日志，应出现类似输出：

```
MUSA: found 1 device(s)
MUSA: device 0: MTT S80 (16.0 GB, compute 2.1, ...)
```

同时可查看 GPU 占用：

```bash
# WSL2 中
musa-smi  # 或 mthreads-gmi
```

## 文件清单

| 文件 | 用途 |
|------|------|
| `build-llama-musa-wsl2.sh` | WSL2 中编译 llama.cpp 2.50.0 (MUSA) |
| `start-musa-server.ps1` | Windows 端启动 MUSA llama-server 并配置端口 |
| `install-lmstudio-runtime.ps1` | 将 MUSA 注册为 LM Studio 运行时模块（实验性） |
| `README.md` | 本文档 |

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| `MUSA Toolkit not found` | 设置 `export MUSA_PATH=/opt/musa` 后重试 |
| `musaInfo` 命令不存在 | 确认 MUSA 驱动已安装：`dpkg -l | grep musa` |
| LM Studio 无法连接 localhost | 确认 WSL2 端口转发正常（Windows 11 默认开启） |
| 模型加载慢 / OOM | 降低 `-GpuLayers` 或使用更小量化的模型 |
| 编译报错 `architecture 21 is deprecated` | 可忽略警告；或升级到 MTT S4000/S5000 使用 22/31 |

## 版本对应关系

- **LM Studio**: 0.4.28 (Build 2)
- **llama.cpp**: 2.50.0 (upstream commit `b11337`)
- **MUSA 后端**: `GGML_MUSA=ON`
