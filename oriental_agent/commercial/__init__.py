"""
商道智能系统核心模块
东方智慧与现代商业的融合
"""

from commercial.types import (
    MarketPosition,
    OpportunityType,
    RiskLevel,
    BusinessMetrics,
    Opportunity,
    InvestmentAnalysis,
    StrategyPlan,
    CompetitionAnalysis,
    CommercialInsight,
)

from commercial.insight.market_insight import MarketInsightEngine
from commercial.model.business_model_analyzer import BusinessModelAnalyzer
from commercial.competition.competition_analyzer import CompetitionAnalyzer
from commercial.investment.investment_analyzer import InvestmentAnalyzer
from commercial.strategy.strategy_planner import StrategyPlanner
from commercial.agent import CommercialAgent, ShangDaoAdvisor, create_commercial_agent, get_quick_insight

__all__ = [
    "MarketPosition",
    "OpportunityType", 
    "RiskLevel",
    "BusinessMetrics",
    "Opportunity",
    "InvestmentAnalysis",
    "StrategyPlan",
    "CompetitionAnalysis",
    "CommercialInsight",
    "MarketInsightEngine",
    "BusinessModelAnalyzer",
    "CompetitionAnalyzer",
    "InvestmentAnalyzer",
    "StrategyPlanner",
    "CommercialAgent",
    "ShangDaoAdvisor",
    "create_commercial_agent",
    "get_quick_insight",
]
