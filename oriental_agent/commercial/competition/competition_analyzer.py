"""
市场竞争分析器
知己知彼，百战不殆
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid

from commercial.types import MarketPosition, CompetitionAnalysis


@dataclass
class CompetitiveIntelligence:
    """竞争情报"""
    competitor_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    name: str = ""
    market_share: float = 0.0
    revenue: float = 0.0
    growth_rate: float = 0.0
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    strategies: List[str] = field(default_factory=list)
    products: List[str] = field(default_factory=list)
    pricing: Dict[str, float] = field(default_factory=dict)
    market_position: MarketPosition = MarketPosition.FOLLOWER
    threat_level: float = 0.0
    opportunities: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class CompetitiveLandscape:
    """竞争格局"""
    market_concentration: float = 0.0
    market_leader: Optional[str] = None
    market_gaps: List[str] = field(default_factory=list)
    emerging_players: List[str] = field(default_factory=list)
    market_trends: List[str] = field(default_factory=list)
    barrier_to_entry: str = "medium"


class CompetitionAnalyzer:
    """竞争分析器"""

    def __init__(self):
        self._competitors: Dict[str, CompetitiveIntelligence] = {}
        self._landscape: Optional[CompetitiveLandscape] = None

    def add_competitor(self, competitor_data: Dict[str, Any]) -> CompetitiveIntelligence:
        """
        添加竞争对手
        
        Args:
            competitor_data: 竞争对手数据
            
        Returns:
            竞争情报对象
        """
        competitor = CompetitiveIntelligence(
            name=competitor_data.get("name", "未知竞争者"),
            market_share=competitor_data.get("market_share", 0.0),
            revenue=competitor_data.get("revenue", 0.0),
            growth_rate=competitor_data.get("growth_rate", 0.0),
            strengths=competitor_data.get("strengths", []),
            weaknesses=competitor_data.get("weaknesses", []),
            strategies=competitor_data.get("strategies", []),
            products=competitor_data.get("products", []),
            pricing=competitor_data.get("pricing", {}),
            market_position=self._determine_position(competitor_data),
            threat_level=self._calculate_threat_level(competitor_data),
            opportunities=self._identify_opportunities(competitor_data)
        )
        
        self._competitors[competitor.competitor_id] = competitor
        return competitor

    def analyze_competition(self, market_data: Dict[str, Any]) -> CompetitiveLandscape:
        """
        分析竞争格局
        
        Args:
            market_data: 市场数据
            
        Returns:
            竞争格局分析
        """
        total_share = sum(c.market_share for c in self._competitors.values())
        
        market_leader = None
        if self._competitors:
            market_leader = max(
                self._competitors.values(),
                key=lambda x: x.market_share
            ).name
        
        landscape = CompetitiveLandscape(
            market_concentration=min(total_share, 1.0),
            market_leader=market_leader,
            market_gaps=self._find_market_gaps(market_data),
            emerging_players=self._find_emerging_players(),
            market_trends=market_data.get("trends", []),
            barrier_to_entry=market_data.get("barrier", "medium")
        )
        
        self._landscape = landscape
        return landscape

    def get_swot_analysis(self, competitor_id: str) -> Dict[str, Any]:
        """获取SWOT分析"""
        if competitor_id not in self._competitors:
            return {}
        
        competitor = self._competitors[competitor_id]
        
        return {
            "competitor": competitor.name,
            "swot": {
                "strengths": competitor.strengths,
                "weaknesses": competitor.weaknesses,
                "opportunities": competitor.opportunities,
                "threats": self._identify_threats(competitor)
            },
            "strategic_implications": self._derive_strategies(competitor)
        }

    def compare_with_competitors(self, my_strengths: List[str], 
                                  my_weaknesses: List[str]) -> Dict[str, Any]:
        """与竞争对手对比分析"""
        comparison = {
            "competitive_advantages": [],
            "competitive_disadvantages": [],
            "unique_capabilities": [],
            "areas_for_improvement": [],
            "threat_assessment": ""
        }
        
        all_competitor_strengths = []
        all_competitor_weaknesses = []
        
        for comp in self._competitors.values():
            all_competitor_strengths.extend(comp.strengths)
            all_competitor_weaknesses.extend(comp.weaknesses)
        
        for strength in my_strengths:
            if strength in all_competitor_strengths:
                comparison["competitive_advantages"].append(strength)
            else:
                comparison["unique_capabilities"].append(strength)
        
        for weakness in my_weaknesses:
            if weakness in all_competitor_weaknesses:
                comparison["competitive_disadvantages"].append(weakness)
            else:
                comparison["areas_for_improvement"].append(weakness)
        
        high_threat = sum(1 for c in self._competitors.values() if c.threat_level > 0.7)
        if high_threat > len(self._competitors) / 2:
            comparison["threat_assessment"] = "市场竞争激烈，多个强势竞争对手"
        elif high_threat > 0:
            comparison["threat_assessment"] = "存在一定威胁，但有机会差异化"
        else:
            comparison["threat_assessment"] = "竞争威胁较低，适合进入"
        
        return comparison

    def generate_response_strategy(self, competitor_id: str) -> Dict[str, Any]:
        """生成应对策略"""
        if competitor_id not in self._competitors:
            return {}
        
        competitor = self._competitors[competitor_id]
        
        strategies = {
            "defensive": [],
            "offensive": [],
            "collaborative": []
        }
        
        if competitor.threat_level > 0.7:
            strategies["defensive"].extend([
                "强化核心竞争优势",
                "建立客户忠诚度壁垒",
                "差异化产品定位"
            ])
            strategies["offensive"].extend([
                "抢夺竞争对手弱势市场",
                "价格竞争优势"
            ])
        else:
            strategies["defensive"].extend([
                "保持现有市场份额",
                "持续优化产品服务"
            ])
        
        if competitor.weaknesses:
            strategies["offensive"].append(
                f"针对竞争对手弱点：{', '.join(competitor.weaknesses[:2])}"
            )
        
        if competitor.opportunities:
            strategies["collaborative"].append(
                f"潜在合作领域：{', '.join(competitor.opportunities[:2])}"
            )
        
        return {
            "competitor": competitor.name,
            "recommended_strategies": strategies,
            "priority_actions": strategies["defensive"] + strategies["offensive"][:2]
        }

    def _determine_position(self, data: Dict[str, Any]) -> MarketPosition:
        """判断市场定位"""
        market_share = data.get("market_share", 0.0)
        growth_rate = data.get("growth_rate", 0.0)
        is_innovator = data.get("is_innovator", False)
        
        if is_innovator or growth_rate > 0.3:
            return MarketPosition.INNOVATOR
        elif market_share > 0.3:
            return MarketPosition.PIONEER
        elif market_share > 0.1:
            return MarketPosition.FOLLOWER
        else:
            return MarketPosition.DEFENDER

    def _calculate_threat_level(self, data: Dict[str, Any]) -> float:
        """计算威胁等级"""
        threat = 0.0
        
        market_share = data.get("market_share", 0.0)
        threat += market_share * 0.5
        
        growth_rate = data.get("growth_rate", 0.0)
        if growth_rate > 0.2:
            threat += 0.3
        elif growth_rate > 0.1:
            threat += 0.15
        
        if data.get("has_price_advantage", False):
            threat += 0.2
        
        return min(threat, 1.0)

    def _identify_opportunities(self, data: Dict[str, Any]) -> List[str]:
        """识别机会"""
        opportunities = []
        
        if data.get("weaknesses"):
            for weakness in data.get("weaknesses", [])[:2]:
                opportunities.append(f"可利用其{weakness}")
        
        if not data.get("digital_presence", True):
            opportunities.append("数字化布局不足，存在超越机会")
            
        return opportunities

    def _identify_threats(self, competitor: CompetitiveIntelligence) -> List[str]:
        """识别威胁"""
        threats = []
        
        if competitor.threat_level > 0.6:
            threats.append("市场份额大，增长迅速")
        if competitor.growth_rate > 0.3:
            threats.append("高增长可能改变市场格局")
        if "价格战" in competitor.strategies:
            threats.append("可能发动价格竞争")
            
        return threats

    def _find_market_gaps(self, market_data: Dict[str, Any]) -> List[str]:
        """寻找市场空白"""
        gaps = market_data.get("market_gaps", [])
        underserved = market_data.get("underserved_segments", [])
        return gaps + underserved

    def _find_emerging_players(self) -> List[str]:
        """发现新兴玩家"""
        return [
            c.name for c in self._competitors.values()
            if c.market_position == MarketPosition.INNOVATOR
        ]

    def _derive_strategies(self, competitor: CompetitiveIntelligence) -> List[str]:
        """推导战略含义"""
        strategies = []
        
        if competitor.market_position == MarketPosition.PIONEER:
            strategies.append("市场领导者，需差异化竞争或颠覆创新")
        elif competitor.market_position == MarketPosition.INNOVATOR:
            strategies.append("创新者，需关注其技术突破和商业模式创新")
        else:
            strategies.append("可借鉴其成功经验，同时寻找差异化机会")
        
        return strategies

    def get_all_competitors(self) -> List[CompetitiveIntelligence]:
        """获取所有竞争对手"""
        return list(self._competitors.values())

    def get_top_competitors(self, limit: int = 5) -> List[CompetitiveIntelligence]:
        """获取最具威胁的竞争对手"""
        return sorted(
            self._competitors.values(),
            key=lambda x: x.threat_level,
            reverse=True
        )[:limit]
