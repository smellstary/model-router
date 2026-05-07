#!/bin/bash
# 统一模型路由网关 - 启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 检查 Python 版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装 Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "🐍 Python 版本: $PYTHON_VERSION"

# 检查并安装依赖
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

echo "📦 激活虚拟环境..."
source venv/bin/activate

echo "📦 安装依赖..."
pip install -q -r requirements.txt

# 检查配置文件
if [ ! -f "config.json" ]; then
    echo "❌ 未找到 config.json 配置文件"
    exit 1
fi

# 检查必要的环境变量
check_env() {
    local var_name=$1
    local var_value=${!var_name}
    if [ -z "$var_value" ]; then
        echo "⚠️  环境变量 $var_name 未设置（如果配置中使用了 \${$var_name}，请设置）"
    fi
}

check_env XIAOMI_API_KEY
check_env OPENROUTER_API_KEY
check_env DASHSCOPE_API_KEY
check_env DEEPSEEK_API_KEY
check_env ZHIPU_API_KEY

# 启动服务
echo ""
echo "🚀 启动统一模型路由网关..."
echo "📖 API 端点: http://0.0.0.0:19000/v1/chat/completions"
echo "📖 API 文档: http://0.0.0.0:19000/docs"
echo "🔧 状态面板: http://0.0.0.0:19000/v1/status"
echo ""

python3 server.py
