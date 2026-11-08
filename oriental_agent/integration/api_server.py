"""
东方智慧智能体 API 服务
OpenClaw & Hermes Agent 集成接口
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import asyncio
from datetime import datetime
from enum import Enum
from typing import Any, get_origin, get_args
from dataclasses import is_dataclass, fields

from core.agent import OrientalWisdomAgent
from image.system import ImageAndQiSystem
from commercial import RiskLevel

app = Flask(__name__)
CORS(app)


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
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/status', methods=['GET'])
def get_status():
    """获取智能体状态"""
    state = asyncio.run(agent.get_full_state())
    return jsonify(serialize_dict(state))


# ==================== 商道智能接口 ====================

@app.route('/api/commercial/opportunity', methods=['POST'])
def analyze_opportunity():
    """商机洞察分析"""
    data = request.json or {}
    result = agent.analyze_business_opportunity(data)
    return jsonify(serialize_dict(result))


@app.route('/api/commercial/model', methods=['POST'])
def analyze_model():
    """商业模式分析"""
    data = request.json or {}
    result = agent.analyze_business_model(data)
    return jsonify(result)


@app.route('/api/commercial/competition', methods=['POST'])
def analyze_competition():
    """竞争分析"""
    data = request.json or {}
    market_data = data.pop('market_data', None)
    result = agent.analyze_competition(data, market_data)
    return jsonify(result)


@app.route('/api/commercial/investment', methods=['POST'])
def analyze_investment():
    """投资分析"""
    data = request.json or {}
    if 'risk_level' in data and isinstance(data['risk_level'], str):
        risk_map = {
            'LOW': RiskLevel.LOW,
            'MEDIUM': RiskLevel.MEDIUM,
            'HIGH': RiskLevel.HIGH,
            'EXTREME': RiskLevel.EXTREME
        }
        data['risk_level'] = risk_map.get(data['risk_level'], RiskLevel.MEDIUM)
    result = agent.analyze_investment(data)
    return jsonify(result)


@app.route('/api/commercial/strategy', methods=['POST'])
def formulate_strategy():
    """战略规划"""
    data = request.json or {}
    result = agent.formulate_strategy(data)
    return jsonify(result)


@app.route('/api/commercial/report', methods=['POST'])
def generate_report():
    """生成综合商业报告"""
    data = request.json or {}
    report = agent.generate_commercial_report(data)
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
    insights = agent.get_shangdao_wisdom()
    return jsonify({'insights': insights})


@app.route('/api/commercial/advice', methods=['GET'])
def get_advice():
    """获取商道建议"""
    situation = request.args.get('situation', 'startup')
    advice = agent.get_shangdao_advice(situation)
    return jsonify(advice)


@app.route('/api/commercial/evaluate', methods=['POST'])
def evaluate_decision():
    """评估商业决策"""
    data = request.json or {}
    decision = data.get('decision', '')
    context = data.get('context', {})
    result = agent.evaluate_business_decision(decision, context)
    return jsonify(result)


# ==================== 形象系统接口 ====================

@app.route('/api/avatar/presets', methods=['GET'])
def list_presets():
    """列出形象预设"""
    presets = img_system.list_avatar_presets()
    return jsonify({'presets': presets})


@app.route('/api/avatar/create', methods=['POST'])
def create_avatar():
    """创建形象"""
    data = request.json or {}
    preset_id = data.get('preset_id', 'model_a')
    name = data.get('name', '东方智慧')
    result = img_system.create_avatar_from_preset(preset_id, name)
    return jsonify(result)


@app.route('/api/avatar/adjust', methods=['POST'])
def adjust_avatar():
    """微调形象特征"""
    data = request.json or {}
    avatar_id = data.get('avatar_id')
    feature = data.get('feature')
    value = data.get('value')
    
    if not avatar_id or not feature:
        return jsonify({'success': False, 'error': '缺少参数'}), 400
    
    result = img_system.adjust_feature(avatar_id, feature, value)
    return jsonify(result)


@app.route('/api/avatar/render', methods=['GET'])
def render_avatar():
    """渲染形象SVG"""
    avatar_id = request.args.get('avatar_id')
    svg = img_system.render_avatar(avatar_id)
    if svg:
        from io import BytesIO
        return app.response_class(
            response=svg.encode('utf-8'),
            status=200,
            mimetype='image/svg+xml'
        )
    return jsonify({'error': '形象不存在'}), 404


@app.route('/api/avatar/export', methods=['GET'])
def export_avatar():
    """导出声像数据"""
    avatar_id = request.args.get('avatar_id')
    data = img_system.export_avatar_data(avatar_id)
    if data:
        return jsonify(data)
    return jsonify({'error': '形象不存在'}), 404


@app.route('/api/avatar/import', methods=['POST'])
def import_avatar():
    """导入形象数据"""
    data = request.json or {}
    result = img_system.import_avatar_data(data)
    return jsonify(result)


# ==================== OpenClaw Webhook ====================

@app.route('/webhook/openclaw', methods=['POST'])
def openclaw_webhook():
    """OpenClaw Webhook 接口"""
    data = request.json or {}
    
    message = data.get('text', '') or data.get('message', {}).get('text', '')
    user_id = data.get('user_id') or data.get('from', {}).get('id')
    chat_id = data.get('chat_id') or data.get('chat', {}).get('id')
    
    if not message:
        return jsonify({'error': 'No message'}), 400
    
    try:
        response = asyncio.run(agent.process(message))
        reply = response.response_text if response else "处理完成"
    except Exception as e:
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
    data = request.json or {}
    action = data.get('action', 'analyze')
    
    if action == 'opportunity':
        result = agent.analyze_business_opportunity(data.get('data', {}))
    elif action == 'investment':
        result = agent.analyze_investment(data.get('data', {}))
    elif action == 'strategy':
        result = agent.formulate_strategy(data.get('data', {}))
    elif action == 'advice':
        result = agent.get_shangdao_advice(data.get('situation', 'startup'))
    else:
        result = {'error': 'Unknown action'}
    
    return jsonify(serialize_dict(result))


@app.route('/hermes/avatar', methods=['POST'])
def hermes_avatar():
    """Hermes Agent 形象接口"""
    data = request.json or {}
    action = data.get('action', 'list')
    
    if action == 'list':
        result = {'presets': img_system.list_avatar_presets()}
    elif action == 'create':
        result = img_system.create_avatar_from_preset(
            data.get('preset_id', 'model_a'),
            data.get('name', 'Hermes Avatar')
        )
    elif action == 'adjust':
        result = img_system.adjust_feature(
            data.get('avatar_id'),
            data.get('feature'),
            data.get('value')
        )
    else:
        result = {'error': 'Unknown action'}
    
    return jsonify(result)


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


# ==================== 启动 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🧘 东方智慧智能体 API 服务")
    print("=" * 60)
    print("📍 本地地址: http://localhost:5000")
    print("📍 OpenClaw Webhook: http://localhost:5000/webhook/openclaw")
    print("📍 Hermes接口: http://localhost:5000/hermes/commercial")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
