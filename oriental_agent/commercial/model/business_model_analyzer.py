"""
商业模式分析器
深度剖析商业模式的核心要素
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from commercial.types import BusinessMetrics, RiskLevel


@dataclass
class BusinessModelCanvas:
    """商业模式画布"""
    customer_segments: List[str] = field(default_factory=list)
    value_propositions: List[str] = field(default_factory=list)
    channels: List[str] = field(default_factory=list)
    customer_relationships: List[str] = field(default_factory=list)
    revenue_streams: List[str] = field(default_factory=list)
    key_resources: List[str] = field(default_factory=list)
    key_activities: List[str] = field(default_factory=list)
    key_partnerships: List[str] = field(default_factory=list)
    cost_structure: List[str] = field(default_factory=list)


@dataclass
class ModelAnalysis:
    """模式分析结果"""
    model_type: str = ""
    model_name: str = ""
    sustainability_score: float = 0.0
    scalability_score: float = 0.0
    defensibility_score: float = 0.0
    profitability_score: float = 0.0
    overall_score: float = 0.0
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class BusinessModelAnalyzer:
    """商业模式分析器"""

    MODEL_TYPES = {
        "subscription": {
            "name": "订阅模式",
            "description": "客户定期支付费用获取持续服务",
            "pros": ["稳定现金流", "可预测收入", "客户粘性高"],
            "cons": ["前期获客成本高", "需要持续提供服务"],
            "key_metrics": ["客户生命周期价值", "月/年经常性收入", "流失率"]
        },
        "marketplace": {
            "name": "平台模式",
            "description": "连接买卖双方，创造交易价值",
            "pros": ["网络效应", "轻资产", "高扩展性"],
            "cons": ["鸡生蛋问题", "平台双方都需要", "监管风险"],
            "key_metrics": ["平台GMV", "活跃买家/卖家", "货币化率"]
        },
        "freemium": {
            "name": "免费增值模式",
            "description": "基础免费，高级付费",
            "pros": ["快速获取用户", "低门槛体验"],
            "cons": ["转化率通常较低", "需要大量服务器资源"],
            "key_metrics": ["免费用户数", "付费转化率", "用户获取成本"]
        },
        "saas": {
            "name": "软件即服务",
            "description": "云端软件按需使用",
            "pros": ["规模化利润高", "订阅收入稳定"],
            "cons": ["研发投入大", "竞争激烈"],
            "key_metrics": ["ARR", "净推荐值", "流失率"]
        },
        "transaction": {
            "name": "交易抽成模式",
            "description": "从每笔交易中抽取佣金",
            "pros": ["收入与交易额挂钩", "低风险"],
            "cons": ["收入波动大", "高度依赖交易量"],
            "key_metrics": ["交易量", "抽成比例", "单位经济模型"]
        },
        "licensing": {
            "name": "授权许可模式",
            "description": "知识产权或技术授权",
            "pros": ["高利润率", "可复制性强"],
            "cons": ["依赖IP价值", "需要持续创新"],
            "key_metrics": ["授权收入", "IP组合价值", "续约率"]
        }
    }

    def __init__(self):
        self._models: Dict[str, BusinessModelCanvas] = {}
        self._analyses: Dict[str, ModelAnalysis] = {}

    def analyze_model(self, model_data: Dict[str, Any]) -> ModelAnalysis:
        """
        分析商业模式
        
        Args:
            model_data: 商业模式数据
            
        Returns:
            分析结果
        """
        model_type = model_data.get("type", "unknown")
        canvas = BusinessModelCanvas(
            customer_segments=model_data.get("customer_segments", []),
            value_propositions=model_data.get("value_propositions", []),
            channels=model_data.get("channels", []),
            customer_relationships=model_data.get("customer_relationships", []),
            revenue_streams=model_data.get("revenue_streams", []),
            key_resources=model_data.get("key_resources", []),
            key_activities=model_data.get("key_activities", []),
            key_partnerships=model_data.get("key_partnerships", []),
            cost_structure=model_data.get("cost_structure", [])
        )
        
        model_info = self.MODEL_TYPES.get(model_type, {
            "name": "未知模式",
            "description": "",
            "pros": [],
            "cons": [],
            "key_metrics": []
        })
        
        analysis = self._calculate_analysis(canvas, model_type, model_info, model_data)
        
        self._models[model_type] = canvas
        self._analyses[model_type] = analysis
        
        return analysis

    def _calculate_analysis(
        self, 
        canvas: BusinessModelCanvas,
        model_type: str,
        model_info: Dict[str, Any],
        raw_data: Dict[str, Any]
    ) -> ModelAnalysis:
        """计算各项评分"""
        
        sustainability = self._assess_sustainability(canvas, raw_data)
        scalability = self._assess_scalability(canvas, raw_data)
        defensibility = self._assess_defensibility(canvas, raw_data)
        profitability = self._assess_profitability(canvas, raw_data)
        
        overall = (sustainability * 0.25 + 
                  scalability * 0.25 + 
                  defensibility * 0.25 + 
                  profitability * 0.25)
        
        strengths = list(model_info.get("pros", []))
        if len(canvas.value_propositions) > 3:
            strengths.append("价值主张清晰明确")
        if len(canvas.key_partnerships) > 2:
            strengths.append("合作伙伴生态完善")
            
        weaknesses = list(model_info.get("cons", []))
        if not canvas.revenue_streams:
            weaknesses.append("收入来源单一")
        if len(canvas.key_resources) < 2:
            weaknesses.append("核心资源不足")
        
        risks = self._identify_risks(canvas, model_type)
        recommendations = self._generate_recommendations(
            sustainability, scalability, defensibility, profitability
        )
        
        return ModelAnalysis(
            model_type=model_type,
            model_name=model_info.get("name", "未知"),
            sustainability_score=sustainability,
            scalability_score=scalability,
            defensibility_score=defensibility,
            profitability_score=profitability,
            overall_score=overall,
            strengths=strengths,
            weaknesses=weaknesses,
            risks=risks,
            recommendations=recommendations
        )

    def _assess_sustainability(self, canvas: BusinessModelCanvas, data: Dict) -> float:
        """评估可持续性"""
        score = 0.5
        
        if len(canvas.revenue_streams) > 1:
            score += 0.15
        if canvas.customer_segments:
            score += 0.15
        if len(canvas.key_activities) >= 3:
            score += 0.1
        if canvas.key_partnerships:
            score += 0.1
            
        return min(score, 1.0)

    def _assess_scalability(self, canvas: BusinessModelCanvas, data: Dict) -> float:
        """评估可扩展性"""
        score = 0.4
        
        if "平台" in canvas.key_activities or "marketplace" in str(canvas.key_activities):
            score += 0.3
        if len(canvas.channels) > 2:
            score += 0.15
        if canvas.key_resources:
            score += 0.15
            
        return min(score, 1.0)

    def _assess_defensibility(self, canvas: BusinessModelCanvas, data: Dict) -> float:
        """评估防御性/护城河"""
        score = 0.4
        
        if len(canvas.value_propositions) > 2:
            score += 0.2
        if canvas.key_partnerships:
            score += 0.2
        if "品牌" in canvas.key_activities or "技术" in canvas.key_resources:
            score += 0.2
            
        return min(score, 1.0)

    def _assess_profitability(self, canvas: BusinessModelCanvas, data: Dict) -> float:
        """评估盈利能力"""
        score = 0.5
        
        if len(canvas.cost_structure) < len(canvas.revenue_streams):
            score += 0.2
        if canvas.revenue_streams:
            score += 0.15
        if len(canvas.channels) <= 3:
            score += 0.15
            
        return min(score, 1.0)

    def _identify_risks(self, canvas: BusinessModelCanvas, model_type: str) -> List[str]:
        """识别商业模式风险"""
        risks = []
        
        if not canvas.revenue_streams or len(canvas.revenue_streams) == 1:
            risks.append("收入来源单一，高度依赖单一业务")
        if not canvas.customer_segments:
            risks.append("目标客户不明确")
        if not canvas.key_partnerships:
            risks.append("缺乏战略合作伙伴，供应链脆弱")
        if not canvas.value_propositions:
            risks.append("缺乏差异化价值主张")
            
        return risks

    def _generate_recommendations(
        self,
        sustainability: float,
        scalability: float,
        defensibility: float,
        profitability: float
    ) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        if sustainability < 0.6:
            recommendations.append("加强收入多元化，降低业务依赖风险")
        if scalability < 0.6:
            recommendations.append("优化运营流程，引入自动化和数字化工具")
        if defensibility < 0.6:
            recommendations.append("构建差异化竞争优势，建立品牌护城河")
        if profitability < 0.6:
            recommendations.append("优化成本结构，提高单位经济模型效率")
            
        if not recommendations:
            recommendations.append("商业模式健康，建议持续优化和创新")
            
        return recommendations

    def compare_models(self, model_types: List[str]) -> Dict[str, ModelAnalysis]:
        """比较多个商业模式"""
        comparisons = {}
        for model_type in model_types:
            if model_type in self._analyses:
                comparisons[model_type] = self._analyses[model_type]
        return comparisons

    def get_model_types(self) -> List[Dict[str, str]]:
        """获取支持的商业模式类型"""
        return [
            {"type": k, "name": v["name"], "description": v["description"]}
            for k, v in self.MODEL_TYPES.items()
        ]
