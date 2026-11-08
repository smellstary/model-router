"""
战略规划器
运筹帷幄，决胜千里
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from commercial.types import StrategyPlan, RiskLevel


@dataclass
class StrategicObjective:
    """战略目标"""
    objective_id: str = ""
    title: str = ""
    description: str = ""
    kpis: List[Dict[str, Any]] = field(default_factory=list)
    timeline: str = ""
    priority: int = 1


@dataclass
class StrategicInitiative:
    """战略举措"""
    initiative_id: str = ""
    name: str = ""
    description: str = ""
    expected_impact: float = 0.0
    required_resources: List[str] = field(default_factory=list)
    owner: str = ""
    dependencies: List[str] = field(default_factory=list)


class StrategyPlanner:
    """战略规划器"""

    STRATEGIC_FRAMES = {
        "cost_leader": {
            "name": "成本领先战略",
            "wisdom": "开源节流，精打细算",
            "focus": ["规模效应", "成本控制", "效率提升", "供应链优化"],
            "risks": ["价格战", "质量下降", "创新不足"]
        },
        "differentiation": {
            "name": "差异化战略",
            "wisdom": "独树一帜，别具一格",
            "focus": ["创新研发", "品牌建设", "客户体验", "独特价值"],
            "risks": ["被模仿", "成本高", "小众市场"]
        },
        "focus": {
            "name": "聚焦战略",
            "wisdom": "集中力量，重点突破",
            "focus": ["细分市场", "专业能力", "深度服务", "客户忠诚"],
            "risks": ["市场萎缩", "依赖单一客户"]
        },
        "integration": {
            "name": "一体化战略",
            "wisdom": "上下贯通，左右逢源",
            "focus": ["纵向整合", "横向扩张", "生态构建", "平台化"],
            "risks": ["整合难度", "资源分散", "管理复杂"]
        },
        "agile": {
            "name": "敏捷战略",
            "wisdom": "兵贵神速，随机应变",
            "focus": ["快速响应", "迭代创新", "灵活组织", "数据驱动"],
            "risks": ["战略漂移", "资源浪费", "组织疲惫"]
        }
    }

    def __init__(self):
        self._plans: Dict[str, StrategyPlan] = {}
        self._objectives: List[StrategicObjective] = []
        self._initiatives: List[StrategicInitiative] = []

    def create_strategic_plan(
        self,
        business_data: Dict[str, Any]
    ) -> StrategyPlan:
        """
        创建战略规划
        
        Args:
            business_data: 业务数据
            
        Returns:
            战略规划
        """
        strategy_type = business_data.get("strategy_type", "differentiation")
        frame = self.STRATEGIC_FRAMES.get(strategy_type, self.STRATEGIC_FRAMES["differentiation"])
        
        objectives = self._define_objectives(business_data, frame)
        strategies = self._formulate_strategies(frame, business_data)
        actions = self._generate_action_plans(objectives, strategies)
        
        plan = StrategyPlan(
            name=f"{frame['name']}规划",
            vision=self._create_vision(business_data),
            mission=self._create_mission(business_data),
            objectives=[obj.title for obj in objectives],
            key_strategies=strategies,
            action_plans=actions,
            timeline=self._create_timeline(frame),
            resource_allocation=self._allocate_resources(frame),
            kpi_metrics=self._define_kpis(objectives),
            risk_mitigation=self._mitigate_risks(frame)
        )
        
        self._plans[plan.plan_id] = plan
        self._objectives = objectives
        self._initiatives = self._generate_initiatives(actions)
        
        return plan

    def _define_objectives(
        self,
        data: Dict[str, Any],
        frame: Dict[str, Any]
    ) -> List[StrategicObjective]:
        """定义战略目标"""
        objectives = []
        
        objectives.append(StrategicObjective(
            objective_id="obj_1",
            title="提升市场竞争力",
            description="在目标市场建立竞争优势地位",
            kpis=[
                {"name": "市场份额", "target": "20%", "current": "10%"},
                {"name": "客户满意度", "target": "90%", "current": "75%"}
            ],
            timeline="1-2年",
            priority=1
        ))
        
        objectives.append(StrategicObjective(
            objective_id="obj_2",
            title="实现可持续发展",
            description="建立长期稳健的增长模式",
            kpis=[
                {"name": "年增长率", "target": "30%", "current": "15%"},
                {"name": "利润率", "target": "20%", "current": "12%"}
            ],
            timeline="2-3年",
            priority=2
        ))
        
        objectives.append(StrategicObjective(
            objective_id="obj_3",
            title="构建核心能力",
            description="建立不易被复制的核心竞争优势",
            kpis=[
                {"name": "专利数量", "target": "50项", "current": "20项"},
                {"name": "品牌价值", "target": "10亿", "current": "3亿"}
            ],
            timeline="3-5年",
            priority=3
        ))
        
        return objectives

    def _formulate_strategies(
        self,
        frame: Dict[str, Any],
        data: Dict[str, Any]
    ) -> List[str]:
        """制定核心策略"""
        strategies = []
        
        for focus in frame.get("focus", []):
            strategies.append(f"实施{focus}策略")
        
        strategies.extend([
            "建立敏捷组织架构",
            "强化数据驱动决策",
            "培养核心人才梯队",
            "构建合作伙伴生态"
        ])
        
        return strategies

    def _generate_action_plans(
        self,
        objectives: List[StrategicObjective],
        strategies: List[str]
    ) -> List[Dict[str, Any]]:
        """生成行动计划"""
        actions = []
        
        phase_1 = {
            "phase": "第一阶段（0-6个月）",
            "actions": [
                {"action": "市场调研与定位", "owner": "市场部", "kpi": "完成市场报告"},
                {"action": "核心产品开发", "owner": "研发部", "kpi": "MVP上线"},
                {"action": "团队组建", "owner": "人力资源", "kpi": "核心团队到位"}
            ]
        }
        
        phase_2 = {
            "phase": "第二阶段（6-18个月）",
            "actions": [
                {"action": "产品市场推广", "owner": "市场部", "kpi": "获得首批客户"},
                {"action": "商业模式验证", "owner": "运营部", "kpi": "单位经济模型为正"},
                {"action": "持续迭代优化", "owner": "产品部", "kpi": "NPS > 40"}
            ]
        }
        
        phase_3 = {
            "phase": "第三阶段（18个月后）",
            "actions": [
                {"action": "规模化扩张", "owner": "CEO", "kpi": "实现年度目标"},
                {"action": "生态建设", "owner": "战略部", "kpi": "合作伙伴 > 20家"},
                {"action": "资本运作", "owner": "财务部", "kpi": "完成融资目标"}
            ]
        }
        
        actions.extend([phase_1, phase_2, phase_3])
        return actions

    def _create_timeline(self, frame: Dict[str, Any]) -> Dict[str, str]:
        """创建时间线"""
        return {
            "vision": "3-5年成为行业领导者",
            "short_term": "0-6个月：基础建设",
            "medium_term": "6-18个月：市场验证",
            "long_term": "18个月-5年：规模化发展"
        }

    def _allocate_resources(self, frame: Dict[str, Any]) -> Dict[str, float]:
        """资源分配"""
        allocations = {
            "产品研发": 0.35,
            "市场营销": 0.25,
            "人才引进": 0.20,
            "运营管理": 0.15,
            "风险储备": 0.05
        }
        return allocations

    def _define_kpis(self, objectives: List[StrategicObjective]) -> Dict[str, float]:
        """定义KPI指标"""
        kpis = {}
        
        for obj in objectives:
            for kpi in obj.kpis:
                target_str = kpi.get("target", "0")
                if "%" in target_str:
                    kpis[f"{obj.title}_{kpi['name']}"] = float(target_str.replace("%", ""))
                else:
                    kpis[f"{obj.title}_{kpi['name']}"] = float(target_str.replace("亿", "")) * 100000000 if "亿" in target_str else float(target_str.replace("项", ""))
        
        return kpis

    def _mitigate_risks(self, frame: Dict[str, Any]) -> Dict[str, str]:
        """风险缓解措施"""
        mitigations = {}
        
        for risk in frame.get("risks", []):
            mitigations[risk] = f"建立{risk}应对预案"
        
        mitigations.update({
            "市场风险": "多元化市场布局",
            "技术风险": "持续研发投入",
            "资金风险": "稳健的资金管理"
        })
        
        return mitigations

    def _create_vision(self, data: Dict[str, Any]) -> str:
        """创建愿景"""
        industry = data.get("industry", "目标行业")
        return f"成为{industry}领域最具创新力和影响力的企业"

    def _create_mission(self, data: Dict[str, Any]) -> str:
        """创建使命"""
        value = data.get("core_value", "为客户创造独特价值")
        return f"通过创新和服务，{value}"

    def _generate_initiatives(
        self,
        actions: List[Dict[str, Any]]
    ) -> List[StrategicInitiative]:
        """生成战略举措"""
        initiatives = []
        
        initiatives.append(StrategicInitiative(
            initiative_id="init_1",
            name="产品创新计划",
            description="持续推出满足市场需求的新产品",
            expected_impact=0.3,
            required_resources=["研发团队", "研发预算"],
            owner="CTO"
        ))
        
        initiatives.append(StrategicInitiative(
            initiative_id="init_2",
            name="市场拓展计划",
            description="扩大市场份额和品牌影响力",
            expected_impact=0.25,
            required_resources=["市场团队", "推广预算"],
            owner="CMO"
        ))
        
        initiatives.append(StrategicInitiative(
            initiative_id="init_3",
            name="人才发展计划",
            description="吸引和保留核心人才",
            expected_impact=0.2,
            required_resources=["HR团队", "培训预算"],
            owner="CHRO"
        ))
        
        return initiatives

    def analyze_swot(
        self,
        strengths: List[str],
        weaknesses: List[str],
        opportunities: List[str],
        threats: List[str]
    ) -> Dict[str, Any]:
        """SWOT分析"""
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "opportunities": opportunities,
            "threats": threats,
            "so_strategies": self._generate_so_strategies(strengths, opportunities),
            "wo_strategies": self._generate_wo_strategies(weaknesses, opportunities),
            "st_strategies": self._generate_st_strategies(strengths, threats),
            "wt_strategies": self._generate_wt_strategies(weaknesses, threats)
        }

    def _generate_so_strategies(
        self,
        strengths: List[str],
        opportunities: List[str]
    ) -> List[str]:
        """优势-机会策略（进攻型）"""
        return [
            f"利用{strengths[0] if strengths else '核心优势'}抓住{opportunities[0] if opportunities else '市场机会'}",
            "最大化自身优势，扩大市场影响力",
            "建立战略联盟，实现共赢发展"
        ]

    def _generate_wo_strategies(
        self,
        weaknesses: List[str],
        opportunities: List[str]
    ) -> List[str]:
        """劣势-机会策略（改善型）"""
        return [
            f"通过{opportunities[0] if opportunities else '市场机会'}弥补{weaknesses[0] if weaknesses else '自身不足'}",
            "引进外部资源，提升能力短板",
            "聚焦细分市场，避免直接竞争"
        ]

    def _generate_st_strategies(
        self,
        strengths: List[str],
        threats: List[str]
    ) -> List[str]:
        """优势-威胁策略（防御型）"""
        return [
            f"用{strengths[0] if strengths else '核心优势'}对抗{ threats[0] if threats else '外部威胁'}",
            "建立竞争壁垒，提高进入门槛",
            "多元化经营，分散风险"
        ]

    def _generate_wt_strategies(
        self,
        weaknesses: List[str],
        threats: List[str]
    ) -> List[str]:
        """劣势-威胁策略（保守型）"""
        return [
            "收缩战线，聚焦核心业务",
            "控制成本，提高运营效率",
            "寻找被并购或战略合作机会"
        ]

    def get_strategic_frames(self) -> List[Dict[str, Any]]:
        """获取战略框架"""
        return [
            {"type": k, **v}
            for k, v in self.STRATEGIC_FRAMES.items()
        ]

    def get_latest_plan(self) -> Optional[StrategyPlan]:
        """获取最新战略规划"""
        if self._plans:
            return list(self._plans.values())[-1]
        return None

    def get_objectives(self) -> List[StrategicObjective]:
        """获取战略目标"""
        return self._objectives

    def get_initiatives(self) -> List[StrategicInitiative]:
        """获取战略举措"""
        return self._initiatives
