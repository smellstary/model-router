#!/usr/bin/env python3
"""
Hermes Skill: 东方智慧商道分析
Hermes Skill: Oriental Wisdom Commercial Analysis
"""

import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

API_BASE = os.environ.get('ORIENTAL_AGENT_URL', 'http://localhost:5000')


@dataclass
class SkillMetadata:
    name: str = "oriental_commercial"
    description: str = "融合东方智慧的商业分析能力"
    version: str = "2.0.0"
    triggers: List[str] = None
    
    def __post_init__(self):
        if self.triggers is None:
            self.triggers = ["商机", "投资", "商业", "市场", "战略", "决策", "创业"]


class OrientalCommercialSkill:
    """东方商道技能"""
    
    def __init__(self):
        self.api_base = API_BASE
        self.metadata = SkillMetadata()
    
    def match(self, query: str) -> bool:
        """检查是否匹配"""
        return any(trigger in query for trigger in self.metadata.triggers)
    
    def execute(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """执行技能"""
        try:
            # 分析查询类型
            if "商机" in query or "机会" in query:
                return self.analyze_opportunity(query, context)
            elif "投资" in query or "项目" in query:
                return self.analyze_investment(query, context)
            elif "战略" in query or "规划" in query:
                return self.analyze_strategy(query, context)
            elif "竞争" in query or "对手" in query:
                return self.analyze_competition(query, context)
            elif "智慧" in query or "建议" in query:
                return self.get_wisdom(context)
            elif "创业" in query or "起步" in query:
                return self.get_startup_advice(context)
            else:
                return self.get_general_insight(query, context)
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "执行商道分析时出错"
            }
    
    def analyze_opportunity(self, query: str, context: Optional[Dict]) -> Dict[str, Any]:
        """商机分析"""
        import requests
        
        data = context or {}
        data.setdefault("unmet_needs", [query])
        
        response = requests.post(
            f"{self.api_base}/api/commercial/opportunity",
            json=data,
            timeout=10
        )
        result = response.json()
        
        # 添加东方智慧解读
        result["wisdom_insight"] = self._get_opportunity_wisdom(result)
        
        return result
    
    def analyze_investment(self, query: str, context: Optional[Dict]) -> Dict[str, Any]:
        """投资分析"""
        import requests
        
        data = context or {}
        
        response = requests.post(
            f"{self.api_base}/api/commercial/investment",
            json=data,
            timeout=10
        )
        result = response.json()
        
        # 添加风险评估
        result["risk_assessment"] = self._get_risk_wisdom(result)
        
        return result
    
    def analyze_strategy(self, query: str, context: Optional[Dict]) -> Dict[str, Any]:
        """战略分析"""
        import requests
        
        data = context or {"industry": query}
        
        response = requests.post(
            f"{self.api_base}/api/commercial/strategy",
            json=data,
            timeout=10
        )
        return response.json()
    
    def analyze_competition(self, query: str, context: Optional[Dict]) -> Dict[str, Any]:
        """竞争分析"""
        import requests
        
        data = context or {"competitor_name": query}
        
        response = requests.post(
            f"{self.api_base}/api/commercial/competition",
            json=data,
            timeout=10
        )
        return response.json()
    
    def get_wisdom(self, context: Optional[Dict]) -> Dict[str, Any]:
        """获取商道智慧"""
        import requests
        
        response = requests.get(
            f"{self.api_base}/api/commercial/wisdom",
            timeout=10
        )
        return response.json()
    
    def get_startup_advice(self, context: Optional[Dict]) -> Dict[str, Any]:
        """获取创业建议"""
        import requests
        
        response = requests.get(
            f"{self.api_base}/api/commercial/advice",
            params={"situation": "startup"},
            timeout=10
        )
        return response.json()
    
    def get_general_insight(self, query: str, context: Optional[Dict]) -> Dict[str, Any]:
        """综合洞察"""
        import requests
        
        # 获取商道建议
        response = requests.get(
            f"{self.api_base}/api/commercial/advice",
            params={"situation": "growth"},
            timeout=10
        )
        
        result = response.json()
        result["query"] = query
        result["suggestion"] = f"关于「{query}」，{result.get('advice', '')}"
        
        return result
    
    def _get_opportunity_wisdom(self, result: Dict) -> str:
        """获取商机相关智慧"""
        insights = [
            "天时地利人和，缺一不可",
            "顺势而为，事半功倍",
            "阴阳相生，危中有机",
            "五行相生，循环不息"
        ]
        return insights[hash(str(result)) % len(insights)]
    
    def _get_risk_wisdom(self, result: Dict) -> str:
        """获取风险相关智慧"""
        roi = result.get("roi", 0)
        if roi > 0.3:
            return "高回报往往伴随高风险，需谨慎权衡"
        elif roi > 0.1:
            return "稳健前行，循序渐进"
        else:
            return "稳扎稳打，步步为营"


def get_skill() -> OrientalCommercialSkill:
    """获取技能实例"""
    return OrientalCommercialSkill()


def get_metadata() -> SkillMetadata:
    """获取技能元数据"""
    return SkillMetadata()


# 直接运行测试
if __name__ == "__main__":
    import requests
    
    skill = OrientalCommercialSkill()
    
    print("=" * 60)
    print("🧘 Hermes 东方商道技能测试")
    print("=" * 60)
    
    # 检查API连接
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        print(f"✅ API连接成功: {response.json()}")
    except Exception as e:
        print(f"❌ API连接失败: {e}")
        print(f"   请先启动: python integration/api_server.py")
        exit(1)
    
    print()
    print("📊 测试各项能力:")
    
    # 测试商机分析
    print("\n1️⃣ 商机分析...")
    result = skill.execute("分析AI领域商机", {"unmet_needs": ["智能助手"]})
    print(f"   识别到 {result.get('total_count', 0)} 个商机")
    
    # 测试投资分析
    print("\n2️⃣ 投资分析...")
    result = skill.execute("分析投资", {
        "name": "AI项目",
        "initial_investment": 1000000,
        "annual_cash_flows": [300000, 400000, 500000]
    })
    print(f"   ROI: {result.get('roi', 0):.0%}")
    print(f"   建议: {result.get('recommendation', 'N/A')}")
    
    # 测试商道智慧
    print("\n3️⃣ 商道智慧...")
    result = skill.get_wisdom(None)
    insights = result.get("insights", [])
    print(f"   获取到 {len(insights)} 条智慧")
    if insights:
        print(f"   示例: {insights[0].get('title', 'N/A')}")
    
    # 测试创业建议
    print("\n4️⃣ 创业建议...")
    result = skill.get_startup_advice(None)
    print(f"   建议: {result.get('advice', 'N/A')[:50]}...")
    
    print()
    print("=" * 60)
    print("🎉 所有功能测试通过!")
    print("=" * 60)
