"""
商道智能系统 (Commercial Agent System)
东方智慧与现代商业的完美融合
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

from commercial.insight.market_insight import MarketInsightEngine, EasternWisdom
from commercial.model.business_model_analyzer import BusinessModelAnalyzer
from commercial.competition.competition_analyzer import CompetitionAnalyzer
from commercial.investment.investment_analyzer import InvestmentAnalyzer
from commercial.strategy.strategy_planner import StrategyPlanner
from commercial.types import (
    Opportunity,
    InvestmentAnalysis,
    StrategyPlan,
    CommercialInsight,
    RiskLevel,
)


@dataclass
class CommercialReport:
    """商业分析报告"""
    report_id: str = field(default_factory=lambda: str(datetime.now().timestamp()))
    title: str = ""
    executive_summary: str = ""
    opportunities: List[Opportunity] = field(default_factory=list)
    investment_analysis: Optional[InvestmentAnalysis] = None
    strategic_plan: Optional[StrategyPlan] = None
    insights: List[CommercialInsight] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CommercialAgentState:
    """智能体状态"""
    analysis_count: int = 0
    opportunities_identified: int = 0
    investments_analyzed: int = 0
    strategies_formulated: int = 0
    insights_generated: int = 0
    last_analysis: Optional[datetime] = None


class CommercialAgent:
    """
    商道智能体
    融合东方智慧与现代商业分析的全方位商业决策助手
    """

    def __init__(self):
        self.insight_engine = MarketInsightEngine()
        self.model_analyzer = BusinessModelAnalyzer()
        self.competition_analyzer = CompetitionAnalyzer()
        self.investment_analyzer = InvestmentAnalyzer()
        self.strategy_planner = StrategyPlanner()
        self._state = CommercialAgentState()
        self._reports: List[CommercialReport] = []

    def analyze_opportunity(
        self,
        market_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        商机分析
        
        Args:
            market_data: 市场数据
            
        Returns:
            商机分析结果
        """
        opportunities = self.insight_engine.analyze_market(market_data)
        
        top_opportunities = self.insight_engine.get_top_opportunities(limit=5)
        wisdom_insights = self.insight_engine.get_wisdom_insights()
        
        self._state.opportunities_identified += len(opportunities)
        self._state.analysis_count += 1
        self._state.last_analysis = datetime.now()
        
        return {
            "opportunities": [
                {
                    "id": o.opportunity_id,
                    "title": o.title,
                    "type": o.opportunity_type.value,
                    "potential_revenue": o.potential_revenue,
                    "confidence": o.confidence,
                    "risk_level": o.risk_level.value,
                    "timing": o.timing_window
                }
                for o in opportunities
            ],
            "top_opportunities": top_opportunities,
            "wisdom_guidance": [w.business_application for w in wisdom_insights[:3]],
            "total_count": len(opportunities)
        }

    def analyze_business_model(
        self,
        model_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        商业模式分析
        
        Args:
            model_data: 商业模式数据
            
        Returns:
            模式分析结果
        """
        analysis = self.model_analyzer.analyze_model(model_data)
        
        return {
            "model_type": analysis.model_type,
            "model_name": analysis.model_name,
            "overall_score": analysis.overall_score,
            "scores": {
                "sustainability": analysis.sustainability_score,
                "scalability": analysis.scalability_score,
                "defensibility": analysis.defensibility_score,
                "profitability": analysis.profitability_score
            },
            "strengths": analysis.strengths,
            "weaknesses": analysis.weaknesses,
            "risks": analysis.risks,
            "recommendations": analysis.recommendations
        }

    def analyze_competition(
        self,
        competitor_data: Dict[str, Any],
        market_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        竞争分析
        
        Args:
            competitor_data: 竞争对手数据
            market_data: 市场数据
            
        Returns:
            竞争分析结果
        """
        competitor = self.competition_analyzer.add_competitor(competitor_data)
        
        if market_data:
            landscape = self.competition_analyzer.analyze_competition(market_data)
        
        comparison = self.competition_analyzer.compare_with_competitors(
            competitor_data.get("my_strengths", []),
            competitor_data.get("my_weaknesses", [])
        )
        
        response_strategy = self.competition_analyzer.generate_response_strategy(
            competitor.competitor_id
        )
        
        return {
            "competitor": competitor.name,
            "threat_level": competitor.threat_level,
            "market_position": competitor.market_position.value,
            "swot": self.competition_analyzer.get_swot_analysis(competitor.competitor_id),
            "comparison": comparison,
            "response_strategy": response_strategy
        }

    def analyze_investment(
        self,
        project_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        投资分析
        
        Args:
            project_data: 项目数据
            
        Returns:
            投资分析结果
        """
        analysis = self.investment_analyzer.analyze_investment(project_data)
        decision = self.investment_analyzer.make_decision(project_data)
        
        self._state.investments_analyzed += 1
        
        return {
            "project_name": analysis.project_name,
            "initial_investment": analysis.initial_investment,
            "expected_return": analysis.expected_return,
            "roi": analysis.roi,
            "payback_period": analysis.payback_period,
            "npv": analysis.npv,
            "irr": analysis.irr,
            "risk_level": analysis.risk_assessment.value,
            "recommendation": analysis.recommendation,
            "decision_rating": decision.investment_rating,
            "key_factors": decision.key_factors,
            "risk_mitigation": decision.risk_mitigation
        }

    def formulate_strategy(
        self,
        business_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        战略规划
        
        Args:
            business_data: 业务数据
            
        Returns:
            战略规划结果
        """
        plan = self.strategy_planner.create_strategic_plan(business_data)
        
        swot = self.strategy_planner.analyze_swot(
            business_data.get("strengths", []),
            business_data.get("weaknesses", []),
            business_data.get("opportunities", []),
            business_data.get("threats", [])
        )
        
        self._state.strategies_formulated += 1
        
        return {
            "plan_name": plan.name,
            "vision": plan.vision,
            "mission": plan.mission,
            "objectives": plan.objectives,
            "key_strategies": plan.key_strategies,
            "action_plans": plan.action_plans,
            "timeline": plan.timeline,
            "resource_allocation": plan.resource_allocation,
            "kpi_metrics": plan.kpi_metrics,
            "swot_analysis": swot
        }

    def generate_comprehensive_report(
        self,
        context: Dict[str, Any]
    ) -> CommercialReport:
        """
        生成综合商业报告
        
        Args:
            context: 分析上下文数据
            
        Returns:
            商业分析报告
        """
        report = CommercialReport(
            title=context.get("title", "商业分析报告")
        )
        
        if "market_data" in context:
            opp_result = self.analyze_opportunity(context["market_data"])
            report.opportunities = self.insight_engine.get_top_opportunities(5)
            report.recommendations.extend(opp_result["wisdom_guidance"])
        
        if "model_data" in context:
            model_result = self.analyze_business_model(context["model_data"])
            report.recommendations.append(
                f"商业模式优化建议：{', '.join(model_result['recommendations'][:2])}"
            )
        
        if "investment_data" in context:
            inv_result = self.analyze_investment(context["investment_data"])
            report.recommendations.append(inv_result["recommendation"])
            report.risks.extend(inv_result.get("risk_mitigation", []))
        
        if "strategy_data" in context:
            strategy_result = self.formulate_strategy(context["strategy_data"])
            report.strategic_plan = self.strategy_planner.get_latest_plan()
        
        report.insights = self.insight_engine.get_wisdom_insights()[:5]
        report.executive_summary = self._generate_summary(report)
        
        self._reports.append(report)
        return report

    def _generate_summary(self, report: CommercialReport) -> str:
        """生成执行摘要"""
        summary_parts = []
        
        if report.opportunities:
            top_opp = report.opportunities[0]
            summary_parts.append(
                f"核心商机：{top_opp.title}，预计收益 {top_opp.potential_revenue:,.0f} 元"
            )
        
        summary_parts.append(
            f"系统生成 {len(report.insights)} 条东方智慧洞察指导"
        )
        
        if report.recommendations:
            summary_parts.append(
                f"关键建议：{report.recommendations[0]}"
            )
        
        return " | ".join(summary_parts)

    def get_wisdom_insights(self) -> List[Dict[str, Any]]:
        """获取东方智慧商业洞察"""
        insights = self.insight_engine.get_wisdom_insights()
        return [
            {
                "category": i.category,
                "title": i.title,
                "insight": i.content,
                "application": i.business_application,
                "actions": i.action_recommendations
            }
            for i in insights
        ]

    def get_state(self) -> Dict[str, Any]:
        """获取智能体状态"""
        return {
            "analysis_count": self._state.analysis_count,
            "opportunities_identified": self._state.opportunities_identified,
            "investments_analyzed": self._state.investments_analyzed,
            "strategies_formulated": self._state.strategies_formulated,
            "insights_generated": len(self.insight_engine.get_wisdom_insights()),
            "last_analysis": self._state.last_analysis.isoformat() if self._state.last_analysis else None,
            "reports_generated": len(self._reports)
        }

    def export_report(self, report: CommercialReport) -> Dict[str, Any]:
        """导出报告为字典"""
        return {
            "report_id": report.report_id,
            "title": report.title,
            "executive_summary": report.executive_summary,
            "timestamp": report.timestamp.isoformat(),
            "opportunities": [
                {"title": o.title, "type": o.opportunity_type.value}
                for o in report.opportunities
            ],
            "insights": [
                {"title": i.title, "content": i.content}
                for i in report.insights
            ],
            "recommendations": report.recommendations
        }


class ShangDaoAdvisor:
    """
    商道顾问
    基于东方智慧的顶级商业咨询AI
    """

    WISDOM_PRINCIPLES = {
        "道法自然": "顺应商业规律，把握市场脉搏",
        "阴阳平衡": "在风险与机遇间寻求平衡",
        "五行相生": "构建商业生态，实现协同发展",
        "天时地利人和": "时机、环境、人心缺一不可",
        "未雨绸缪": "预见风险，提前布局",
        "革故鼎新": "创新突破，超越竞争"
    }

    @classmethod
    def get_advice(cls, situation: str) -> Dict[str, str]:
        """根据情况提供建议"""
        advice_map = {
            "startup": "创业初期宜稳扎稳打，先求生存再谋发展。借鉴'千里之行，始于足下'的智慧。",
            "growth": "成长期应注重团队建设与文化建设，为规模化奠定基础。'上下同欲者胜'。",
            "mature": "成熟期需要创新求变，避免路径依赖。'穷则变，变则通'。",
            "turnaround": "转型期应果断决策，轻装上阵。'置之死地而后生'。",
            "crisis": "危机时刻要冷静分析，抓住核心问题。'危中有机，否极泰来'。"
        }
        
        return {
            "situation": situation,
            "advice": advice_map.get(situation, "审时度势，随机应变。"),
            "wisdom_quote": list(cls.WISDOM_PRINCIPLES.values())[hash(situation) % len(cls.WISDOM_PRINCIPLES)],
            "action_steps": cls._generate_action_steps(situation)
        }

    @classmethod
    def _generate_action_steps(cls, situation: str) -> List[str]:
        """生成行动步骤"""
        base_steps = [
            "深入分析当前形势",
            "识别关键机会与风险",
            "制定切实可行的计划",
            "分阶段推进执行",
            "持续评估与调整"
        ]
        
        if situation == "crisis":
            base_steps.insert(0, "立即止血，稳定局面")
            base_steps.insert(1, "评估最坏情况，制定应对预案")
        
        return base_steps

    @classmethod
    def evaluate_decision(cls, decision: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """评估决策"""
        risk_level = context.get("risk_level", 0.5)
        potential_return = context.get("potential_return", 0.5)
        
        wisdom_score = 0.0
        if risk_level < 0.3 and potential_return > 0.5:
            wisdom_score = 0.9
            assessment = "上佳决策"
        elif risk_level < 0.6:
            wisdom_score = 0.7
            assessment = "合理决策"
        else:
            wisdom_score = 0.5
            assessment = "需谨慎评估"
        
        return {
            "decision": decision,
            "assessment": assessment,
            "wisdom_score": wisdom_score,
            "risk_return_ratio": potential_return / (risk_level + 0.1),
            "recommendations": [
                "确保决策有充分的依据支撑",
                "建立风险监控机制",
                "准备备选方案"
            ]
        }


def create_commercial_agent() -> CommercialAgent:
    """创建商道智能体工厂函数"""
    return CommercialAgent()


def get_quick_insight(topic: str) -> Dict[str, str]:
    """快速获取商道洞察"""
    return ShangDaoAdvisor.get_advice(topic)
