"""
商机洞察引擎
运用东方智慧洞察商业机遇
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

from commercial.types import (
    Opportunity, 
    OpportunityType, 
    RiskLevel,
    CommercialInsight
)


class EasternWisdom:
    """东方智慧商道洞察"""

    WISDOM_INSIGHTS = {
        "天时": {
            "insight": "时机把握决定成败，顺势而为事半功倍",
            "application": "市场窗口期识别与把握",
            "indicators": ["market_trends", "consumer_sentiment", "policy_changes"]
        },
        "地利": {
            "insight": "因地制宜制宜，审时度势",
            "application": "区域市场差异化策略",
            "indicators": ["local_demand", "competition_density", "regulatory_env"]
        },
        "人和": {
            "insight": "得人心者得天下，诚信为本",
            "application": "客户关系与品牌忠诚度建设",
            "indicators": ["customer_satisfaction", "brand_reputation", "partnership_quality"]
        },
        "阴阳": {
            "insight": "阴阳相生相克，危中有机",
            "application": "危机中的转型机遇识别",
            "indicators": ["market_disruption", "technology_shift", "consumer_behavior_change"]
        },
        "五行": {
            "insight": "相生相克，循环不息",
            "application": "产业链协同与生态构建",
            "indicators": ["supply_chain", "ecosystem_health", "value_chain_optimization"]
        },
        "八卦": {
            "insight": "万象更新，变化无穷",
            "application": "市场趋势预测与创新方向",
            "indicators": ["innovation_potential", "market_volatilities", "emerging_tech"]
        },
        "中庸": {
            "insight": "过犹不及，恰到好处",
            "application": "平衡风险与收益的决策",
            "indicators": ["risk_adjusted_return", "diversification", "sustainability"]
        },
        "变革": {
            "insight": "穷则变，变则通，通则久",
            "application": "业务转型与升级路径",
            "indicators": ["business_model_innovation", "digital_transformation", "market_repositioning"]
        }
    }

    @classmethod
    def get_insight(cls, wisdom_key: str) -> Dict[str, str]:
        return cls.WISDOM_INSIGHTS.get(wisdom_key, {})

    @classmethod
    def get_all_insights(cls) -> List[CommercialInsight]:
        insights = []
        for key, value in cls.WISDOM_INSIGHTS.items():
            insights.append(CommercialInsight(
                category="东方智慧",
                title=key,
                content=value["insight"],
                wisdom_source="商道易经",
                business_application=value["application"],
                action_recommendations=value["indicators"],
                confidence=0.85
            ))
        return insights


class MarketInsightEngine:
    """市场洞察与商机识别引擎"""

    # 没有这些信号时，不编造商机或收入
    _SIGNAL_KEYS = (
        "unmet_needs",
        "underserved_segments",
        "technology_trends",
        "policy_drivers",
        "industry_disruption",
    )

    def __init__(self):
        self.wisdom = EasternWisdom()
        self._opportunity_pool: List[Opportunity] = []
        self._insights: List[CommercialInsight] = []
        self._market_signals: Dict[str, Any] = {}
        self.last_data_status: str = "ok"

    def analyze_market(self, market_data: Dict[str, Any]) -> List[Opportunity]:
        """
        分析市场数据，识别商机。

        没有可识别的市场信号时返回空列表，并把 last_data_status 标为「数据不足」。
        潜在收益只使用调用方提供的数字，不再用随机数填充。
        """
        market_data = market_data or {}
        if not self._has_market_signals(market_data):
            self.last_data_status = "数据不足"
            return []

        self.last_data_status = "ok"
        opportunities = []
        
        gaps = self._identify_market_gaps(market_data)
        for gap in gaps:
            opportunities.append(gap)
            self._opportunity_pool.append(gap)
        
        emerging = self._identify_emerging_opportunities(market_data)
        for opp in emerging:
            opportunities.append(opp)
            self._opportunity_pool.append(opp)
        
        transformations = self._identify_transformation_opportunities(market_data)
        for trans in transformations:
            opportunities.append(trans)
            self._opportunity_pool.append(trans)

        if not opportunities:
            self.last_data_status = "数据不足"
        
        return opportunities

    def _has_market_signals(self, data: Dict[str, Any]) -> bool:
        for key in self._SIGNAL_KEYS:
            value = data.get(key)
            if isinstance(value, (list, tuple)) and len(value) > 0:
                return True
            if isinstance(value, str) and value.strip():
                return True
        return False

    def _resolve_revenue(self, data: Dict[str, Any]) -> tuple:
        """返回 (金额, 状态)。没有市场收入数据时金额为 0，状态为「数据不足」。"""
        for key in ("potential_revenue", "estimated_revenue", "market_size"):
            value = data.get(key)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return float(value), "已提供"
        return 0.0, "数据不足"

    def _describe(self, base: str, revenue_status: str) -> str:
        if revenue_status == "数据不足":
            return f"{base}。潜在收益：数据不足"
        return base

    def _identify_market_gaps(self, data: Dict[str, Any]) -> List[Opportunity]:
        """识别市场空白"""
        gaps = []
        
        unmet_needs = data.get("unmet_needs", [])
        revenue, revenue_status = self._resolve_revenue(data)
        for need in unmet_needs:
            gaps.append(Opportunity(
                title=f"填补空白：{need}",
                description=self._describe(f"市场存在未被满足的需求：{need}", revenue_status),
                opportunity_type=OpportunityType.GAP,
                potential_revenue=revenue,
                confidence=0.75,
                risk_level=RiskLevel.MEDIUM,
                timing_window="即时",
                required_resources=["研发投入", "市场推广"],
                competitive_advantage=["先发优势", "技术壁垒"],
                market_indicators={"revenue_status": revenue_status},
            ))
        
        underserved_segments = data.get("underserved_segments", [])
        for segment in underserved_segments:
            gaps.append(Opportunity(
                title=f"细分市场：{segment}",
                description=self._describe("目标细分市场服务不足", revenue_status),
                opportunity_type=OpportunityType.GAP,
                potential_revenue=revenue,
                confidence=0.70,
                risk_level=RiskLevel.LOW,
                market_indicators={"revenue_status": revenue_status},
            ))
        
        return gaps

    def _identify_emerging_opportunities(self, data: Dict[str, Any]) -> List[Opportunity]:
        """识别新兴市场机遇"""
        opportunities = []
        
        revenue, revenue_status = self._resolve_revenue(data)
        tech_trends = data.get("technology_trends", [])
        for trend in tech_trends:
            opportunities.append(Opportunity(
                title=f"新技术应用：{trend}",
                description=self._describe("新技术驱动的市场机会", revenue_status),
                opportunity_type=OpportunityType.EMERGING,
                potential_revenue=revenue,
                confidence=0.65,
                risk_level=RiskLevel.HIGH,
                timing_window="1-3年",
                required_resources=["技术创新", "人才储备", "资本投入"],
                competitive_advantage=["技术领先", "创新能力"],
                market_indicators={"revenue_status": revenue_status},
            ))
        
        policy_drivers = data.get("policy_drivers", [])
        for policy in policy_drivers:
            opportunities.append(Opportunity(
                title=f"政策机遇：{policy}",
                description=self._describe("政策导向带来的市场机会", revenue_status),
                opportunity_type=OpportunityType.EMERGING,
                potential_revenue=revenue,
                confidence=0.80,
                risk_level=RiskLevel.MEDIUM,
                timing_window="政策周期内",
                market_indicators={"revenue_status": revenue_status},
            ))
        
        return opportunities

    def _identify_transformation_opportunities(self, data: Dict[str, Any]) -> List[Opportunity]:
        """识别转型机遇"""
        opportunities = []
        
        revenue, revenue_status = self._resolve_revenue(data)
        disruption_areas = data.get("industry_disruption", [])
        for area in disruption_areas:
            opportunities.append(Opportunity(
                title=f"行业转型：{area}",
                description=self._describe("行业变革期的整合与升级机会", revenue_status),
                opportunity_type=OpportunityType.TRANSFORMATION,
                potential_revenue=revenue,
                confidence=0.60,
                risk_level=RiskLevel.HIGH,
                timing_window="3-5年",
                required_resources=["资本实力", "并购能力", "整合经验"],
                competitive_advantage=["规模优势", "资源整合能力"],
                market_indicators={"revenue_status": revenue_status},
            ))
        
        return opportunities

    def get_wisdom_insights(self) -> List[CommercialInsight]:
        """获取东方智慧商业洞察"""
        return self.wisdom.get_all_insights()

    def assess_opportunity(self, opportunity_id: str) -> Dict[str, Any]:
        """评估特定商机的投资价值"""
        for opp in self._opportunity_pool:
            if opp.opportunity_id == opportunity_id:
                return {
                    "opportunity": opp,
                    "investment_rating": self._calculate_rating(opp),
                    "wisdom_guidance": self._get_wisdom_guidance(opp),
                    "action_plan": self._generate_action_plan(opp)
                }
        return {}

    def _calculate_rating(self, opp: Opportunity) -> str:
        """计算投资评级"""
        score = opp.confidence * 0.4
        
        if opp.risk_level == RiskLevel.LOW:
            score += 0.3
        elif opp.risk_level == RiskLevel.MEDIUM:
            score += 0.2
        elif opp.risk_level == RiskLevel.HIGH:
            score += 0.1
        else:
            score += 0.0
        
        potential_score = min(opp.potential_revenue / 10000000, 1.0) * 0.3
        score += potential_score
        
        if score >= 0.8:
            return "AAAAA"
        elif score >= 0.6:
            return "AAAA"
        elif score >= 0.4:
            return "AAA"
        else:
            return "AA"

    def _get_wisdom_guidance(self, opp: Opportunity) -> str:
        """获取智慧指导"""
        guidances = {
            OpportunityType.GAP: "以柔克刚，以弱胜强。先满足需求，再建立壁垒。",
            OpportunityType.EMERGING: "把握天时，顺势而为。抢占先机，引领潮流。",
            OpportunityType.TRANSFORMATION: "穷则思变，变中求进。以攻为守，主动变革。",
            OpportunityType.INTEGRATION: "阴阳相济，协同共生。资源整合，价值共创。"
        }
        return guidances.get(opp.opportunity_type, "审时度势，量力而行。")

    def _generate_action_plan(self, opp: Opportunity) -> List[str]:
        """生成行动方案"""
        plans = [
            "进行深入市场调研，验证商机真实性",
            "评估自身资源与能力匹配度",
            "制定阶段性目标和里程碑",
            "建立风险监测与应对机制",
            "组建专业团队或寻找合作伙伴"
        ]
        
        if opp.opportunity_type == OpportunityType.EMERGING:
            plans.insert(0, "快速迭代，小步快跑，抢占市场份额")
        elif opp.opportunity_type == OpportunityType.TRANSFORMATION:
            plans.insert(0, "稳扎稳打，充分论证后再大规模投入")
        
        return plans

    def get_opportunities_by_type(self, opp_type: OpportunityType) -> List[Opportunity]:
        """按类型筛选商机"""
        return [o for o in self._opportunity_pool if o.opportunity_type == opp_type]

    def get_top_opportunities(self, limit: int = 5) -> List[Opportunity]:
        """获取最具价值的商机"""
        sorted_opps = sorted(
            self._opportunity_pool,
            key=lambda x: x.confidence * 0.5 + (x.potential_revenue / 100000000) * 0.5,
            reverse=True
        )
        return sorted_opps[:limit]
