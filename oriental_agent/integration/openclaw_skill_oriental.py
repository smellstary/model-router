#!/usr/bin/env python3
"""
OpenClaw 技能: 东方智慧商道分析
Skill: Oriental Wisdom Commercial Analysis

OpenAPI：仓库没有单独的 OpenAPI 规范文件。HTTP 契约以
integration/api_server_secure.py 的路由为准，主要是：
  POST /api/commercial/opportunity
  POST /api/commercial/investment
  POST /api/commercial/strategy
  POST /api/commercial/competition
  GET  /api/commercial/wisdom
认证：Authorization: Bearer <API_AUTH_TOKEN>，或 X-API-Key: <API_KEYS 中的一项>。
超时：客户端 REQUEST_TIMEOUT_SECONDS=30，与 config_secure.ORIENTAL_AGENT_CONFIG
里 openclaw/hermes 的 timeout 以及 openclaw_config.json 的 backend.timeout（30000 毫秒）对齐。
服务端 Flask 不另设请求超时，调用方必须自己设置 timeout，避免挂起。
"""

import requests
import json
import os
from typing import Dict, Any, Optional

API_BASE = os.environ.get('ORIENTAL_AGENT_URL', 'http://localhost:5000')
# 秒。与 integration/config_secure.py 的 integration.*.timeout 一致。
REQUEST_TIMEOUT_SECONDS = 30


def _auth_headers() -> Dict[str, str]:
    """带上 API Key 或 Bearer。两者都空时仍发出请求，由服务端返回 401。"""
    headers = {'Content-Type': 'application/json'}
    token = (os.environ.get('API_AUTH_TOKEN') or os.environ.get('BEARER_TOKEN') or '').strip()
    if token:
        headers['Authorization'] = f'Bearer {token}'
    key = (os.environ.get('API_KEY') or '').strip()
    if not key:
        raw_keys = os.environ.get('API_KEYS') or ''
        key = raw_keys.split(',')[0].strip()
    if key:
        headers['X-API-Key'] = key
    return headers


class OrientalWisdomSkill:
    """东方智慧商道技能"""
    
    name = "oriental_commercial"
    description = "融合东方智慧的商业分析能力"
    triggers = ["商机", "投资", "商业", "市场分析", "战略", "决策"]
    
    def __init__(self):
        self.api_base = API_BASE
    
    def execute(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """执行商道分析"""
        try:
            # 根据查询类型路由
            if any(k in query for k in ["商机", "机会", "空白"]):
                return self._analyze_opportunity(query, context)
            elif any(k in query for k in ["投资", "项目", "ROI"]):
                return self._analyze_investment(query, context)
            elif any(k in query for k in ["战略", "规划", "布局"]):
                return self._analyze_strategy(query, context)
            elif any(k in query for k in ["竞争", "对手", "分析"]):
                return self._analyze_competition(query, context)
            else:
                return self._general_analysis(query, context)
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _analyze_opportunity(self, query: str, context: Optional[Dict]) -> Dict:
        """商机分析"""
        data = context or {}
        response = requests.post(
            f"{self.api_base}/api/commercial/opportunity",
            json=data,
            headers=_auth_headers(),
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        return response.json()
    
    def _analyze_investment(self, query: str, context: Optional[Dict]) -> Dict:
        """投资分析"""
        data = context or {}
        response = requests.post(
            f"{self.api_base}/api/commercial/investment",
            json=data,
            headers=_auth_headers(),
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        return response.json()
    
    def _analyze_strategy(self, query: str, context: Optional[Dict]) -> Dict:
        """战略分析"""
        data = context or {}
        response = requests.post(
            f"{self.api_base}/api/commercial/strategy",
            json=data,
            headers=_auth_headers(),
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        return response.json()
    
    def _analyze_competition(self, query: str, context: Optional[Dict]) -> Dict:
        """竞争分析"""
        data = context or {}
        response = requests.post(
            f"{self.api_base}/api/commercial/competition",
            json=data,
            headers=_auth_headers(),
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        return response.json()
    
    def _general_analysis(self, query: str, context: Optional[Dict]) -> Dict:
        """综合分析"""
        response = requests.get(
            f"{self.api_base}/api/commercial/wisdom",
            headers=_auth_headers(),
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        return response.json()


def get_skill() -> OrientalWisdomSkill:
    """获取技能实例"""
    return OrientalWisdomSkill()


# 如果直接运行，执行测试
if __name__ == "__main__":
    skill = get_skill()
    
    # 测试商机分析
    print("🧪 测试商机分析...")
    result = skill.execute("分析AI领域的商业机会", {"unmet_needs": ["智能助手"], "technology_trends": ["大模型"]})
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
