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
from integration.config_secure import SECURITY_CONFIG as CONFIG_SECURE_CONFIG

app = Flask(__name__)

# CORS: 开发场景放开（ALLOW_ALL_ORIGINS=true），生产环境通过 ORIGINS 精确控制
import os
_ALLOW_ALL_ORIGINS = os.environ.get('ALLOW_ALL_ORIGINS', 'false').lower() == 'true'
if _ALLOW_ALL_ORIGINS:
    CORS(app, supports_credentials=True)
else:
    _allowed_origins = os.environ.get(
        'ORIGINS',
        'http://localhost:5000,http://127.0.0.1:5000,http://localhost:19000'
    ).split(',')
    CORS(app, origins=[o.strip() for o in _allowed_origins], supports_credentials=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== 安全配置 ====================

_TRUSTED_IPS_FROM_ENV = os.environ.get(
    'TRUSTED_IPS',
    '127.0.0.1,::1,localhost,0.0.0.0'
).split(',')
_ENABLE_IP_WHITELIST = os.environ.get('ENABLE_IP_WHITELIST', 'false').lower() == 'true'

SECURITY_CONFIG = {
    'trusted_ips': [ip.strip() for ip in _TRUSTED_IPS_FROM_ENV],
    'enable_ip_whitelist': _ENABLE_IP_WHITELIST,
    'enable_rate_limiting': os.environ.get('ENABLE_RATE_LIMITING', 'true').lower() == 'true',
    'rate_limit': {
        'requests_per_minute': int(os.environ.get('RATE_LIMIT_PER_MINUTE', '120')),
        'requests_per_hour': int(os.environ.get('RATE_LIMIT_PER_HOUR', '2000')),
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

        # 只保留最近一小时内的记录
        recent_requests = [
            t for t in rate_limit_storage[ip]
            if current_time - t < 3600
        ]
        rate_limit_storage[ip] = recent_requests

        recent_requests_minute = [
            t for t in recent_requests
            if current_time - t < 60
        ]

        if len(recent_requests_minute) >= minute_limit:
            logger.warning(f"Rate limit exceeded for IP {ip} (per minute)")
            return False

        # 小时判断也基于已清理的最近一小时窗口，而不是未清理的原始列表
        if len(recent_requests) >= hour_limit:
            logger.warning(f"Rate limit exceeded for IP {ip} (per hour)")
            return False

        rate_limit_storage[ip].append(current_time)

        # 额外清理：整体存储超过 500 个 IP 时，移除空闲 IP
        if len(rate_limit_storage) > 500:
            expired = [
                k for k, v in rate_limit_storage.items()
                if not v or (current_time - v[-1]) > 7200
            ]
            for k in expired:
                del rate_limit_storage[k]

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


# ==================== Emotion / 动画提示推断 ====================

# ==================== Emotion / 动画提示推断 ====================

# 12 种意图 → 最贴合的情绪（主信号，权重最高）
_INTENT_EMOTION_MAP = {
    'hello':                  'happy',     # 问候 → 开心
    'introduce_self':         'thinking',  # 自我介绍 → 思考（介绍中）
    'commercial_opportunity': 'happy',     # 商机 → 看好/喜悦
    'investment':              'thinking',  # 投资 → 深思熟虑
    'strategy':                'thinking',  # 战略 → 深谋远虑
    'competition':             'alert',     # 竞争 → 警觉/戒备
    'prediction':              'thinking',  # 预测 → 推演思考
    'body_health':             'calm',      # 养生 → 平和安稳
    'cultivation':             'calm',      # 修炼 → 宁静入定
    'emotion_support':        'gentle',    # 情绪支持 → 温柔安抚
    'relationship':            'gentle',    # 人际 → 温和
    'wisdom_advice':           'thinking',  # 智慧建议 → 思考中
}

# 用户输入里的负面词 → sadness 微调
_USER_NEGATIVE_KEYWORDS = [
    '压力', '焦虑', '崩溃', '抑郁', '痛苦', '难受', '不开心', '失业', '失败', '分手', '失恋', '怕', '怕输', '害怕',
]

# 预测结果里的吉凶词 → happy/sad 微调
_PRED_GOOD_KEYWORDS = ['吉', '利', '好', '顺', '上升', '光明', '成', '有望']
_PRED_BAD_KEYWORDS  = ['凶', '不利', '坏', '阻', '下', '退', '损', '忌', '慎']

_EMOTION_DEFAULT_ANIMATION = {
    'happy':   'talk',
    'sad':     'idle',
    'calm':    'idle',
    'alert':   'blink',
    'thinking':'blink',
    'gentle':  'talk',
}


def _infer_emotion(reply_text: str, state_changes: dict, user_message: str = '') -> dict:
    """
    三级信号推断情绪:
      L1 (主): primary_intent → 映射表
      L2 (微): reply_text 吉凶 / user_message 负面词
      L3 (底): philosophy contributions 底色
    返回: {'emotion': str, 'animation': str, 'confidence': float}
    """
    reply_text = reply_text or ''
    user_message = user_message or ''
    primary = state_changes.get('primary_intent', '')

    # ========== L1: intent 主信号 ==========
    emotion = _INTENT_EMOTION_MAP.get(primary, 'calm')
    confidence = 0.6  # intent 本身给到 0.6

    # ========== L2: reply_text + user_message 微调 ==========
    # 2a: 用户输入里有负面情绪词 → 如果是 emotion_support 就 sad，否则 alert
    neg_hits = sum(1 for kw in _USER_NEGATIVE_KEYWORDS if kw in user_message)
    if neg_hits >= 2:
        if primary == 'emotion_support':
            emotion = 'sad'
            confidence += 0.2
        else:
            emotion = 'alert'
            confidence += 0.15
    elif neg_hits == 1 and primary == 'emotion_support':
        emotion = 'sad'
        confidence += 0.1

    # 2b: 预测场景看吉凶 → 覆盖 L1
    if primary == 'prediction':
        good = sum(1 for kw in _PRED_GOOD_KEYWORDS if kw in reply_text)
        bad  = sum(1 for kw in _PRED_BAD_KEYWORDS  if kw in reply_text)
        if good > bad:
            emotion = 'happy'
            confidence += 0.25
        elif bad > good:
            emotion = 'alert'
            confidence += 0.25
        else:
            emotion = 'thinking'
            confidence += 0.1

    # 2c: 竞争/投资场景看 reply 里的风险词 → alert
    if primary in ('competition', 'investment', 'strategy'):
        if any(kw in reply_text for kw in ['风险', '警惕', '谨慎', '注意', '挑战']):
            emotion = 'alert'
            confidence += 0.15

    # ========== L3: philosophy 底色 ==========
    philo = state_changes.get('philosophy_contributions', {}) or {}
    fo = float(philo.get('佛家', 0))
    dao = float(philo.get('道家', 0))
    ru  = float(philo.get('儒家', 0))

    # 道家主导 → 偏向 calm（无为、合道）
    if dao >= 0.8 and emotion in ('thinking', 'gentle'):
        emotion = 'calm'
        confidence += 0.1

    # 儒家主导 + emotion_support/relationship → 强化 gentle
    if ru >= 0.8 and emotion == 'gentle':
        confidence += 0.1

    # ========== 兜底 ==========
    if confidence < 0.5:
        confidence = 0.5

    animation = _EMOTION_DEFAULT_ANIMATION.get(emotion, 'idle')

    return {
        'emotion': emotion,
        'animation': animation,
        'confidence': round(min(confidence, 1.0), 2),
    }


# ==================== 桌面客户端友好对话接口 ====================

@app.route('/api/dialog', methods=['POST'])
def desktop_dialog():
    """
    桌面客户端友好的对话接口。
    入参: {"message": "我想创业", "user_id": "xiaoyuan_lover"}
    出参: {
      "reply": "...完整回答...",
      "emotion": "happy|calm|thinking|...",
      "animation": "talk|idle|blink",
      "hexagram": "乾卦 / GUA_1",
      "intent": "commercial_opportunity",
      "confidence": 0.72,
      "philosophy": {"佛家": 0.90, "道家": 0.50, "儒家": 0.30}
    }
    """
    log_request_info()
    data = request.json or {}

    message = (
        data.get('message')
        or data.get('input')
        or data.get('query')
        or ''
    )
    user_id = data.get('user_id', 'anonymous')

    if not message or not isinstance(message, str):
        return jsonify({
            'error': 'message 不能为空',
            'error_code': 'INVALID_INPUT',
        }), 400

    is_valid, sanitized_message = validate_input(message, max_length=5000)
    if not is_valid:
        logger.warning(f"Input validation warning for user {user_id}")

    try:
        response = asyncio.run(agent.process(sanitized_message))
    except Exception as e:
        logger.error(f"Error processing dialog: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'error_code': 'DIALOG_ERROR',
        }), 500

    reply_text = response.response_text if response else ''
    state_changes = response.state_changes if response else {}

    # 提取卦象（如果有的话）
    hexagram = ''
    for act in (response.actions_taken or []):
        pred_res = act.get('prediction_result')
        if pred_res and isinstance(pred_res, dict):
            hexagram = pred_res.get('hexagram', '')
            break

    # emotion & animation 推断
    emotion_info = _infer_emotion(reply_text, state_changes, user_message=sanitized_message)

    return jsonify({
        'reply': reply_text,
        'emotion': emotion_info['emotion'],
        'animation': emotion_info['animation'],
        'animation_confidence': emotion_info['confidence'],
        'hexagram': hexagram,
        'intent': state_changes.get('primary_intent', ''),
        'confidence': state_changes.get('thinking_confidence', 0.5),
        'philosophy': state_changes.get('philosophy_contributions', {}),
        'cycle': state_changes.get('cycle', 0),
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
    })


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
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'reply': '服务内部错误，请稍后再试',
            'error_code': 'INTERNAL_ERROR',
            'timestamp': datetime.now().isoformat()
        }), 500

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
        logger.error(f"Error in hermes_commercial: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'error_code': 'HERMES_COMMERCIAL_ERROR'}), 500


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
        logger.error(f"Error in hermes_avatar: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'error_code': 'HERMES_AVATAR_ERROR'}), 500


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
    _host = os.environ.get('HOST', '127.0.0.1')
    _port = int(os.environ.get('PORT', '5000'))
    _debug = os.environ.get('DEBUG', 'false').lower() == 'true'

    print("=" * 60)
    print("🛡️  东方智慧智能体 API 服务 - 安全增强版")
    print("=" * 60)
    print(f"📍 监听地址: http://{_host}:{_port}")
    print(f"📍 桌面对话: http://{_host}:{_port}/api/dialog  (小缘用这个)")
    print(f"📍 OpenClaw Webhook: http://{_host}:{_port}/webhook/openclaw")
    print(f"📍 Hermes接口: http://{_host}:{_port}/hermes/commercial")
    print(f"📍 健康检查: http://{_host}:{_port}/health")
    print("=" * 60)
    print("🔒 安全特性:")
    print(f"   - IP白名单: {'启用' if SECURITY_CONFIG['enable_ip_whitelist'] else '禁用'}")
    print(f"   - 频率限制: {'启用' if SECURITY_CONFIG['enable_rate_limiting'] else '禁用'}")
    print(f"   - 输入验证: {'启用' if SECURITY_CONFIG['enable_input_validation'] else '禁用'}")
    print(f"   - 请求日志: {'启用' if SECURITY_CONFIG['enable_request_logging'] else '禁用'}")
    print(f"   - 安全头: {'启用' if SECURITY_CONFIG['enable_security_headers'] else '禁用'}")
    print(f"   - DEBUG: {'启用 (警告: 勿在生产环境开启)' if _debug else '关闭'}")
    print("=" * 60)
    app.run(host=_host, port=_port, debug=_debug)
