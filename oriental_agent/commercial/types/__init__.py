"""
商道智能系统类型定义
基于东方智慧与现代商业理论的融合
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid


class MarketPosition(Enum):
    """市场定位"""
    PIONEER = "先驱者"      # 开路先锋
    FOLLOWER = "追随者"    # 后发制人
    INNOVATOR = "创新者"   # 变革引领
    DEFENDER = "守护者"    # 稳守江山


class OpportunityType(Enum):
    """商机类型"""
    EMERGING = "新兴市场"      # 新领域探索
    GAP = "市场空白"          # 填补空缺
    TRANSFORMATION = "转型机遇" # 产业升级
    INTEGRATION = "整合机遇"   # 资源整合


class RiskLevel(Enum):
    """风险等级"""
    LOW = "低风险"
    MEDIUM = "中风险"
    HIGH = "高风险"
    EXTREME = "极高风险"


@dataclass
class BusinessMetrics:
    """商业指标"""
    revenue: float = 0.0
    growth_rate: float = 0.0
    profit_margin: float = 0.0
    market_share: float = 0.0
    customer_retention: float = 0.0


@dataclass
class Opportunity:
    """商机"""
    opportunity_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    title: str = ""
    description: str = ""
    opportunity_type: OpportunityType = OpportunityType.GAP
    potential_revenue: float = 0.0
    confidence: float = 0.5
    risk_level: RiskLevel = RiskLevel.MEDIUM
    timing_window: str = ""
    required_resources: List[str] = field(default_factory=list)
    competitive_advantage: List[str] = field(default_factory=list)
    market_indicators: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class InvestmentAnalysis:
    """投资分析"""
    project_name: str = ""
    initial_investment: float = 0.0
    expected_return: float = 0.0
    roi: float = 0.0
    payback_period: float = 0.0
    npv: float = 0.0
    irr: float = 0.0
    risk_assessment: RiskLevel = RiskLevel.MEDIUM
    recommendation: str = ""
    factors: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StrategyPlan:
    """战略规划"""
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    name: str = ""
    vision: str = ""
    mission: str = ""
    objectives: List[str] = field(default_factory=list)
    key_strategies: List[str] = field(default_factory=list)
    action_plans: List[Dict[str, Any]] = field(default_factory=list)
    timeline: Dict[str, str] = field(default_factory=dict)
    resource_allocation: Dict[str, float] = field(default_factory=dict)
    kpi_metrics: Dict[str, float] = field(default_factory=dict)
    risk_mitigation: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class CompetitionAnalysis:
    """竞争分析"""
    competitor_name: str = ""
    market_position: MarketPosition = MarketPosition.FOLLOWER
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    market_share: float = 0.0
    threat_level: float = 0.0
    response_strategy: str = ""


@dataclass
class CommercialInsight:
    """商业洞察"""
    insight_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    category: str = ""
    title: str = ""
    content: str = ""
    wisdom_source: str = ""
    business_application: str = ""
    action_recommendations: List[str] = field(default_factory=list)
    confidence: float = 0.5
    timestamp: datetime = field(default_factory=datetime.now)
