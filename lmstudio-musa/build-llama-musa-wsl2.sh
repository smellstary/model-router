#!/usr/bin/env bash
# =============================================================================
# build-llama-musa-wsl2.sh
# 在 WSL2 (Ubuntu) 中编译 llama.cpp 2.50.0 (upstream b11337) 的 MUSA 原生后端
# 目标：为 Windows 11 26H2 上的 LM Studio 0.4.28 (Build 2) 提供摩尔线程 GPU 加速
#
# 前置条件（必须在 WSL2 Ubuntu 中已安装）：
#   1. MUSA SDK（从 https://developer.mthreads.com/sdk/download/musa 下载 DEB 包）
#      - MTT S80/S3000:  CC2.1 系列，MUSA_ARCHITECTURES=21
#      - MTT S4000:       CC2.2 系列，MUSA_ARCHITECTURES=22
#      - MTT S5000:       CC3.1 系列，MUSA_ARCHITECTURES=31
#   2. 摩尔线程 Linux 驱动（与 MUSA SDK 版本匹配）
#   3. build-essential, cmake, git, pkg-config
#
# 用法：
#   bash build-llama-musa-wsl2.sh [MUSA_ARCH]
#   例如：bash build-llama-musa-wsl2.sh 21    # MTT S80/S3000
#         bash build-llama-musa-wsl2.sh 22    # MTT S4000
#         bash build-llama-musa-wsl2.sh 31    # MTT S5000
# =============================================================================
set -euo pipefail

# ---- 配置 ----
LLAMA_VERSION="b11337"              # LM Studio 0.4.28 对应的 llama.cpp 上游 commit
LLAMA_VERSION_DISPLAY="2.50.0"      # LM Studio 内部版本号
BUILD_DIR="${HOME}/llama-musa-build"
OUTPUT_DIR="${HOME}/llama-musa-dist"
MUSA_ARCH="${1:-21}"                # 默认 S80/S3000 (compute 2.1)

# MUSA SDK 路径检测
if [ -n "${MUSA_PATH:-}" ] && [ -d "${MUSA_PATH}" ]; then
    :
elif [ -d "/opt/musa" ]; then
    export MUSA_PATH="/opt/musa"
elif [ -d "/usr/local/musa" ]; then
    export MUSA_PATH="/usr/local/musa"
else
    echo "[ERROR] 未找到 MUSA SDK。请先安装 MUSA SDK，或设置 MUSA_PATH 环境变量。"
    echo "        下载地址: https://developer.mthreads.com/sdk/download/musa"
    exit 1
fi

echo "[INFO] MUSA_PATH = ${MUSA_PATH}"
echo "[INFO] MUSA_ARCHITECTURES = ${MUSA_ARCH}"
echo "[INFO] llama.cpp 版本 = ${LLAMA_VERSION_DISPLAY} (upstream ${LLAMA_VERSION})"

# ---- 检查依赖 ----
for cmd in git cmake make clang++; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "[ERROR] 缺少依赖: $cmd"
        echo "        安装: sudo apt update && sudo apt install -y git cmake build-essential clang"
        exit 1
    fi
done

# 验证 MUSA 编译器
if [ ! -x "${MUSA_PATH}/bin/clang++" ]; then
    echo "[ERROR] ${MUSA_PATH}/bin/clang++ 不存在或不可执行。"
    echo "        请确认 MUSA SDK 安装完整。"
    exit 1
fi

# 验证 MUSA 运行时
if ! command -v musaInfo >/dev/null 2>&1; then
    echo "[WARN] 未找到 musaInfo 命令，请确认 MUSA 驱动已安装。"
fi

# ---- 下载 llama.cpp ----
echo "[INFO] 克隆 llama.cpp (${LLAMA_VERSION})..."
if [ -d "${BUILD_DIR}/llama.cpp" ]; then
    echo "[INFO] 目录已存在，执行更新..."
    cd "${BUILD_DIR}/llama.cpp"
    git fetch --all --tags
else
    mkdir -p "${BUILD_DIR}"
    git clone https://github.com/ggerganov/llama.cpp.git "${BUILD_DIR}/llama.cpp"
    cd "${BUILD_DIR}/llama.cpp"
fi

git checkout "${LLAMA_VERSION}" 2>/dev/null || {
    echo "[WARN] 未找到 tag ${LLAMA_VERSION}，尝试 fetch 后重试..."
    git fetch origin tag "${LLAMA_VERSION}" || true
    git checkout "${LLAMA_VERSION}"
}

# ---- 编译 ----
echo "[INFO] 开始 CMake 配置 (GGML_MUSA=ON)..."
cmake -B build-musa -S . \
    -DCMAKE_BUILD_TYPE=Release \
    -DGGML_MUSA=ON \
    -DMUSA_ARCHITECTURES="${MUSA_ARCH}" \
    -DGGML_CUDA_FORCE_MMQ=ON \
    -DGGML_NATIVE=OFF

echo "[INFO] 开始编译 (核心数: $(nproc))..."
cmake --build build-musa --config Release -j"$(nproc)"

# ---- 打包输出 ----
echo "[INFO] 打包产物到 ${OUTPUT_DIR}..."
rm -rf "${OUTPUT_DIR}"
mkdir -p "${OUTPUT_DIR}/bin"
mkdir -p "${OUTPUT_DIR}/lib"

# 复制可执行文件
for exe in llama-server llama-cli llama-bench llama-perplexity llama-gguf; do
    if [ -f "build-musa/bin/${exe}" ]; then
        cp "build-musa/bin/${exe}" "${OUTPUT_DIR}/bin/"
    fi
done

# 复制共享库
cp -a build-musa/lib/*.so* "${OUTPUT_DIR}/lib/" 2>/dev/null || true

# 复制 MUSA 运行时库（用于分发，避免目标机缺失）
for musa_lib in libmusart.so libmublas.so libmudnn.so libmusa.so; do
    if [ -f "${MUSA_PATH}/lib/${musa_lib}" ]; then
        cp -a "${MUSA_PATH}/lib/${musa_lib}"* "${OUTPUT_DIR}/lib/" 2>/dev/null || true
    fi
done

# 生成版本信息
cat > "${OUTPUT_DIR}/VERSION.txt" <<EOF
llama.cpp MUSA 后端构建信息
============================
llama.cpp 上游版本 : ${LLAMA_VERSION}
LM Studio 对应版本 : ${LLAMA_VERSION_DISPLAY}
MUSA 架构         : ${MUSA_ARCH}
构建平台          : $(uname -m) $(uname -s)
编译器            : $(${MUSA_PATH}/bin/clang++ --version | head -1)
构建时间          : $(date -u '+%Y-%m-%d %H:%M:%S UTC')
EOF

echo ""
echo "[SUCCESS] 构建完成！"
echo "  输出目录: ${OUTPUT_DIR}"
echo "  关键文件:"
echo "    ${OUTPUT_DIR}/bin/llama-server   (MUSA 加速的推理服务器)"
echo "    ${OUTPUT_DIR}/bin/llama-cli      (命令行推理)"
echo "    ${OUTPUT_DIR}/lib/                (运行时库)"
echo ""
echo "下一步: 在 Windows 端运行 setup-lmstudio-musa.ps1 配置 LM Studio 集成。"
