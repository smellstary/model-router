#!/bin/bash
# 小缘（桌面 AI 女友）对接启动脚本
# 启动东方智慧智能体 API 服务，默认放开 IP 白名单 + 全量 CORS
# 让任何本地桌面客户端（Electron / Python / C#）都能直接调用

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║     小缘 × 东方智慧智能体 —— 后端启动                 ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ---- 1. 依赖检查 ----
echo "📦 检查依赖..."
python3 -c "import flask, flask_cors" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "   → 安装 flask + flask-cors..."
    pip install flask flask-cors --quiet
fi
echo "   ✅ 依赖就绪"

# ---- 2. 环境变量（桌面开发友好默认值）----
export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-5000}"
export DEBUG="${DEBUG:-false}"
export ENABLE_IP_WHITELIST="${ENABLE_IP_WHITELIST:-false}"
export ALLOW_ALL_ORIGINS="${ALLOW_ALL_ORIGINS:-true}"
export ENABLE_RATE_LIMITING="${ENABLE_RATE_LIMITING:-true}"

echo ""
echo "⚙️  配置:"
echo "   HOST              = $HOST"
echo "   PORT              = $PORT"
echo "   ENABLE_IP_WHITELIST = $ENABLE_IP_WHITELIST"
echo "   ALLOW_ALL_ORIGINS = $ALLOW_ALL_ORIGINS"
echo "   ENABLE_RATE_LIMITING = $ENABLE_RATE_LIMITING"
echo ""
echo "📍 关键接口:"
echo "   健康检查:   GET  http://$HOST:$PORT/health"
echo "   桌面对话:   POST http://$HOST:$PORT/api/dialog    ← 小缘用这个"
echo "   OpenClaw:   POST http://$HOST:$PORT/webhook/openclaw"
echo "   状态:       GET  http://$HOST:$PORT/api/status"
echo "   商道接口:   POST http://$HOST:$PORT/api/commercial/*"
echo "   形象接口:   GET/POST http://$HOST:$PORT/api/avatar/*"
echo ""
echo "👉 小缘调用示例:"
echo "   curl -X POST http://127.0.0.1:${PORT}/api/dialog \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"message\": \"我想创业\", \"user_id\": \"xiaoyuan\"}'"
echo ""
echo "🚀 启动中..."
echo ""

python3 integration/api_server_secure.py
