"""
东方智慧智能体 API 服务 - 安全增强版
OpenClaw & Hermes Agent 集成接口
不修改 OpenClaw 和 Hermes 配置的前提下安全集成
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from datetime import datetime
from enum import Enum
from typing import Any
from dataclasses import is_dataclass, fields
import time
import logging
from collections import defaultdict
import threading

from core.agent import OrientalWisdomAgent
from image.system import ImageAndQiSystem
from commercial import RiskLevel

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== 安全配置 ====================

SECURITY_CONFIG = {
    'trusted_ips': ['127.0.0.1', '::1', 'localhost'],
    'enable_ip_whitelist': True,
    'enable_rate_limiting': True,
    'rate_limit': {
        'requests_per_minute': 60,
        'requests_per_hour': 1000,
    },
    'enable_input_validation': True,
    'max_request_size': 1024 * 1024,
    'enable_request_logging': True,
    'enable_security_headers': True,
}

rate_limit_storage = defaultdict(list)
rate_limit_lock = threading.Lock()


def check_rate_limit(ip):
    """检查请求频率限制"""
    if not SECURITY_CONFIG['enable_rate_limiting']:
        return True

    current_time = time.time()

    with rate_limit_lock:
        rate_limit = SECURITY_CONFIG['rate_limit']

        minute_limit = rate_limit['requests_per_minute']
        hour_limit = rate_limit['requests_per_hour']

        recent_requests = [
            t for t in rate_limit_storage[ip]
            if current_time - t < 3600
        ]

        recent_requests_minute = [
            t for t in recent_requests
            if current_time - t < 60
        ]

        if len(recent_requests_minute) >= minute_limit:
            logger.warning(f"Rate limit exceeded for IP {ip} (per minute)")
            return False

        if len(rate_limit_storage[ip]) >= hour_limit:
            logger.warning(f"Rate limit exceeded for IP {ip} (per hour)")
            return False

        rate_limit_storage[ip].append(current_time)
        rate_limit_storage[ip] = [
            t for t in rate_limit_storage[ip]
            if current_time - t < 3600
        ]

        return True


def validate_input(data, max_length=10000):
    """验证和清洗输入数据"""
    if not SECURITY_CONFIG['enable_input_validation']:
        return True, data

    if data is None:
        return True, data

    if isinstance(data, str):
        if len(data) > max_length:
            logger.warning(f"Input too long: {len(data)} chars")
            return False, data[:max_length]
        return True, data

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str) and len(value) > max_length:
                sanitized[key] = value[:max_length]
            else:
                sanitized[key] = value
        return True, sanitized

    if isinstance(data, list):
        if len(data) > 1000:
            logger.warning(f"Input list too long: {len(data)} items")
            return False, data[:1000]

    return True, data


@app.after_request
def add_security_headers(response):
    """添加安全响应头"""
    if not SECURITY_CONFIG['enable_security_headers']:
        return response

    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"

    return response


def log_request_info():
    """记录请求日志"""
    if not SECURITY_CONFIG['enable_request_logging']:
        return

    ip = request.remote_addr
    method = request.method
    path = request.path
    user_agent = request.headers.get('User-Agent', 'Unknown')

    logger.info(f"{ip} - {method} {path} - {user_agent[:50]}")


@app.before_request
def before_request_checks():
    """请求前安全检查"""
    if request.content_length and request.content_length > SECURITY_CONFIG['max_request_size']:
        logger.warning(f"Request too large from {request.remote_addr}: {request.content_length} bytes")
        return jsonify({'error': 'Request too large'}), 413

    if SECURITY_CONFIG['enable_ip_whitelist']:
        client_ip = request.remote_addr
        if client_ip not in SECURITY_CONFIG['trusted_ips']:
            logger.warning(f"Unauthorized IP access attempt: {client_ip}")
            return jsonify({'error': 'Access denied'}), 403

    if not check_rate_limit(request.remote_addr):
        return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429


# ==================== 序列化辅助函数 ====================

def serialize_value(value: Any) -> Any:
    """序列化不可 JSON 序列化的值"""
    if value is None:
        return None
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return serialize_dict(value)
    if is_dataclass(value) and not isinstance(value, type):
        return serialize_dataclass(value)
    if hasattr(value, '__dict__'):
        return serialize_dict(value.__dict__)
    if isinstance(value, (list, tuple)):
        return [serialize_value(item) for item in value]
    if isinstance(value, str):
        try:
            import json
            parsed = json.loads(value)
            return serialize_value(parsed)
        except (json.JSONDecodeError, TypeError):
            return value
    return str(value)


def serialize_dataclass(obj: Any) -> dict:
    """序列化 dataclass 对象"""
    result = {}
    for field_info in fields(obj):
        field_value = getattr(obj, field_info.name)
        result[field_info.name] = serialize_value(field_value)
    return result


def serialize_dict(data: dict) -> dict:
    """递归序列化字典中的不可序列化值"""
    result = {}
    for key, value in data.items():
        key_str = key.value if isinstance(key, Enum) else str(key)
        result[key_str] = serialize_value(value)
    return result


# 全局实例
agent = OrientalWisdomAgent()
img_system = ImageAndQiSystem()


# ==================== 基础接口 ====================

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'service': 'Oriental Wisdom Agent',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'security': {
            'rate_limiting': SECURITY_CONFIG['enable_rate_limiting'],
            'ip_whitelist': SECURITY_CONFIG['enable_ip_whitelist'],
            'input_validation': SECURITY_CONFIG['enable_input_validation']
        }
    })


@app.route('/api/status', methods=['GET'])
def get_status():
    """获取智能体状态"""
    log_request_info()
    state = asyncio.run(agent.get_full_state())
    return jsonify(serialize_dict(state))


# ==================== 商道智能接口 ====================

@app.route('/api/commercial/opportunity', methods=['POST'])
def analyze_opportunity():
    """商机洞察分析"""
    log_request_info()
    data = request.json or {}

    is_valid, sanitized_data = validate_input(data)
    if not is_valid:
        return jsonify({'error': 'Input validation warning', 'data': sanitize_dict(sanitized_data)}), 400

    result = agent.analyze_business_opportunity(sanitized_data)
    return jsonify(serialize_dict(result))


@app.route('/api/commercial/model', methods=['POST'])
def analyze_model():
    """商业模式分析"""
    log_request_info()
    data = request.json or {}

    is_valid, sanitized_data = validate_input(data)
    if not is_valid:
        return jsonify({'error': 'Input validation warning', 'data': sanitize_dict(sanitized_data)}), 400

    result = agent.analyze_business_model(sanitized_data)
    return jsonify(result)


@app.route('/api/commercial/competition', methods=['POST'])
def analyze_competition():
    """竞争分析"""
    log_request_info()
    data = request.json or {}

    is_valid, sanitized_data = validate_input(data)
    if not is_valid:
        return jsonify({'error': 'Input validation warning', 'data': sanitize_dict(sanitized_data)}), 400

    market_data = sanitized_data.pop('market_data', None)
    result = agent.analyze_competition(sanitized_data, market_data)
    return jsonify(result)


@app.route('/api/commercial/investment', methods=['POST'])
def analyze_investment():
    """投资分析"""
    log_request_info()
    data = request.json or {}

    is_valid, sanitized_data = validate_input(data)
    if not is_valid:
        return jsonify({'error': 'Input validation warning', 'data': sanitize_dict(sanitized_data)}), 400

    if 'risk_level' in sanitized_data and isinstance(sanitized_data['risk_level'], str):
        risk_map = {
            'LOW': RiskLevel.LOW,
            'MEDIUM': RiskLevel.MEDIUM,
            'HIGH': RiskLevel.HIGH,
            'EXTREME': RiskLevel.EXTREME
        }
        sanitized_data['risk_level'] = risk_map.get(sanitized_data['risk_level'], RiskLevel.MEDIUM)

    result = agent.analyze_investment(sanitized_data)
    return jsonify(result)


@app.route('/api/commercial/strategy', methods=['POST'])
def formulate_strategy():
    """战略规划"""
    log_request_info()
    data = request.json or {}

    is_valid, sanitized_data = validate_input(data)
    if not is_valid:
        return jsonify({'error': 'Input validation warning', 'data': sanitize_dict(sanitized_data)}), 400

    result = agent.formulate_strategy(sanitized_data)
    return jsonify(result)


@app.route('/api/commercial/report', methods=['POST'])
def generate_report():
    """生成综合商业报告"""
    log_request_info()
    data = request.json or {}

    is_valid, sanitized_data = validate_input(data)
    if not is_valid:
        return jsonify({'error': 'Input validation warning', 'data': sanitize_dict(sanitized_data)}), 400

    report = agent.generate_commercial_report(sanitized_data)
    return jsonify({
        'report_id': report.report_id,
        'title': report.title,
        'executive_summary': report.executive_summary,
        'recommendations': report.recommendations,
        'timestamp': report.timestamp.isoformat()
    })


@app.route('/api/commercial/wisdom', methods=['GET'])
def get_wisdom():
    """获取商道智慧"""
    log_request_info()
    insights = agent.get_shangdao_wisdom()
    return jsonify({'insights': insights})


@app.route('/api/commercial/advice', methods=['GET'])
def get_advice():
    """获取商道建议"""
    log_request_info()
    situation = request.args.get('situation', 'startup')
    advice = agent.get_shangdao_advice(situation)
    return jsonify(advice)


@app.route('/api/commercial/evaluate', methods=['POST'])
def evaluate_decision():
    """评估商业决策"""
    log_request_info()
    data = request.json or {}

    is_valid, sanitized_data = validate_input(data)
    if not is_valid:
        return jsonify({'error': 'Input validation warning', 'data': sanitize_dict(sanitized_data)}), 400

    decision = sanitized_data.get('decision', '')
    context = sanitized_data.get('context', {})
    result = agent.evaluate_business_decision(decision, context)
    return jsonify(result)


# ==================== 形象系统接口 ====================

@app.route('/api/avatar/presets', methods=['GET'])
def list_presets():
    """列出形象预设"""
    log_request_info()
    presets = img_system.list_avatar_presets()
    return jsonify({'presets': presets})


@app.route('/api/avatar/create', methods=['POST'])
def create_avatar():
    """创建形象"""
    log_request_info()
    data = request.json or {}

    is_valid, sanitized_data = validate_input(data)
    if not is_valid:
        return jsonify({'error': 'Input validation warning', 'data': sanitize_dict(sanitized_data)}), 400

    preset_id = sanitized_data.get('preset_id', 'model_a')
    name = sanitized_data.get('name', '东方智慧')
    result = img_system.create_avatar_from_preset(preset_id, name)
    return jsonify(result)


@app.route('/api/avatar/adjust', methods=['POST'])
def adjust_avatar():
    """微调形象特征"""
    log_request_info()
    data = request.json or {}

    is_valid, sanitized_data = validate_input(data)
    if not is_valid:
        return jsonify({'error': 'Input validation warning', 'data': sanitize_dict(sanitized_data)}), 400

    avatar_id = sanitized_data.get('avatar_id')
    feature = sanitized_data.get('feature')
    value = sanitized_data.get('value')

    if not avatar_id or not feature:
        return jsonify({'success': False, 'error': '缺少参数'}), 400

    result = img_system.adjust_feature(avatar_id, feature, value)
    return jsonify(result)


@app.route('/api/avatar/render', methods=['GET'])
def render_avatar():
    """渲染形象SVG"""
    log_request_info()
    avatar_id = request.args.get('avatar_id')
    svg = img_system.render_avatar(avatar_id)
    if svg:
        return app.response_class(
            response=svg.encode('utf-8'),
            status=200,
            mimetype='image/svg+xml'
        )
    return jsonify({'error': '形象不存在'}), 404


@app.route('/api/avatar/export', methods=['GET'])
def export_avatar():
    """导出声像数据"""
    log_request_info()
    avatar_id = request.args.get('avatar_id')
    data = img_system.export_avatar_data(avatar_id)
    if data:
        return jsonify(data)
    return jsonify({'error': '形象不存在'}), 404


@app.route('/api/avatar/import', methods=['POST'])
def import_avatar():
    """导入形象数据"""
    log_request_info()
    data = request.json or {}

    is_valid, sanitized_data = validate_input(data)
    if not is_valid:
        return jsonify({'error': 'Input validation warning', 'data': sanitize_dict(sanitized_data)}), 400

    result = img_system.import_avatar_data(sanitized_data)
    return jsonify(result)


def sanitize_dict(data):
    """递归清洗字典中的字符串"""
    if isinstance(data, dict):
        return {k: sanitize_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_dict(item) for item in data]
    elif isinstance(data, str):
        return data.replace('<', '').replace('>', '')[:10000]
    return data


# ==================== OpenClaw Webhook ====================

@app.route('/webhook/openclaw', methods=['POST'])
def openclaw_webhook():
    """OpenClaw Webhook 接口"""
    log_request_info()

    data = request.json or {}

    message = data.get('text', '') or data.get('message', {}).get('text', '')
    user_id = data.get('user_id') or data.get('from', {}).get('id')
    chat_id = data.get('chat_id') or data.get('chat', {}).get('id')

    if not message:
        return jsonify({'error': 'No message'}), 400

    is_valid, sanitized_message = validate_input(message, max_length=5000)
    if not is_valid:
        logger.warning(f"Input validation warning for message from {user_id}")

    try:
        response = asyncio.run(agent.process(sanitized_message))
        reply = response.response_text if response and response.response_text else "处理完成"
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        reply = f"处理消息时出错: {str(e)}"

    return jsonify({
        'success': True,
        'reply': reply,
        'user_id': user_id,
        'chat_id': chat_id,
        'timestamp': datetime.now().isoformat()
    })


# ==================== Hermes Agent 接口 ====================

@app.route('/hermes/commercial', methods=['POST'])
def hermes_commercial():
    """Hermes Agent 商道接口"""
    log_request_info()
    data = request.json or {}

    is_valid, sanitized_data = validate_input(data)
    if not is_valid:
        return jsonify({'error': 'Input validation warning', 'data': sanitize_dict(sanitized_data)}), 400

    action = sanitized_data.get('action', 'analyze')

    try:
        if action == 'opportunity':
            result = agent.analyze_business_opportunity(sanitized_data.get('data', {}))
        elif action == 'investment':
            result = agent.analyze_investment(sanitized_data.get('data', {}))
        elif action == 'strategy':
            result = agent.formulate_strategy(sanitized_data.get('data', {}))
        elif action == 'advice':
            result = agent.get_shangdao_advice(sanitized_data.get('situation', 'startup'))
        else:
            result = {'error': 'Unknown action'}

        return jsonify(serialize_dict(result))
    except Exception as e:
        logger.error(f"Error in hermes_commercial: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/hermes/avatar', methods=['POST'])
def hermes_avatar():
    """Hermes Agent 形象接口"""
    log_request_info()
    data = request.json or {}

    is_valid, sanitized_data = validate_input(data)
    if not is_valid:
        return jsonify({'error': 'Input validation warning', 'data': sanitize_dict(sanitized_data)}), 400

    action = sanitized_data.get('action', 'list')

    try:
        if action == 'list':
            result = {'presets': img_system.list_avatar_presets()}
        elif action == 'create':
            result = img_system.create_avatar_from_preset(
                sanitized_data.get('preset_id', 'model_a'),
                sanitized_data.get('name', 'Hermes Avatar')
            )
        elif action == 'adjust':
            result = img_system.adjust_feature(
                sanitized_data.get('avatar_id'),
                sanitized_data.get('feature'),
                sanitized_data.get('value')
            )
        else:
            result = {'error': 'Unknown action'}

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in hermes_avatar: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {str(e)}")
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({'error': 'An unexpected error occurred'}), 500


# ==================== 启动 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🛡️  东方智慧智能体 API 服务 - 安全增强版")
    print("=" * 60)
    print("📍 本地地址: http://localhost:5000")
    print("📍 OpenClaw Webhook: http://localhost:5000/webhook/openclaw")
    print("📍 Hermes接口: http://localhost:5000/hermes/commercial")
    print("=" * 60)
    print("🔒 安全特性:")
    print(f"   - IP白名单: {'启用' if SECURITY_CONFIG['enable_ip_whitelist'] else '禁用'}")
    print(f"   - 频率限制: {'启用' if SECURITY_CONFIG['enable_rate_limiting'] else '禁用'}")
    print(f"   - 输入验证: {'启用' if SECURITY_CONFIG['enable_input_validation'] else '禁用'}")
    print(f"   - 请求日志: {'启用' if SECURITY_CONFIG['enable_request_logging'] else '禁用'}")
    print(f"   - 安全头: {'启用' if SECURITY_CONFIG['enable_security_headers'] else '禁用'}")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=True)
