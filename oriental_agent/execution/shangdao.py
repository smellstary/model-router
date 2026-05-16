"""
Shangdao (Business Way) Strategic System
商道战略系统 - 基于东方商业智慧

融合《管子》《孙子兵法》《货殖列传》等东方商业智慧，
构建战略决策、风险评估、资源配置、时机选择的商道智能层。
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class StrategyType(Enum):
    """战略类型"""
    ATTACK = "进攻"       # 积极扩张
    DEFEND = "防守"       # 稳守固本
    ALLIANCE = "联盟"     # 合作共生
    RETREAT = "退守"      # 收缩蓄力
    OBSERVE = "观望"      # 静观其变
    ADAPT = "变通"        # 随机应变


class RiskLevel(Enum):
    """风险等级"""
    LOW = "低风险"
    MODERATE = "中等风险"
    HIGH = "高风险"
    CRITICAL = "极高风险"


class OpportunityType(Enum):
    """机会类型"""
    MARKET = "市场机会"
    TECH = "技术机会"
    RESOURCE = "资源机会"
    ALLIANCE_OPP = "合作机会"
    TIMING = "时机窗口"


class ResourcePriority(Enum):
    """资源优先级"""
    CRITICAL = "核心资源"
    IMPORTANT = "重要资源"
    SUPPORTING = "辅助资源"
    OPTIONAL = "可选资源"


@dataclass
class StrategicSituation:
    """战略态势"""
    situation_name: str
    strategy: StrategyType
    confidence: float
    rationale: str
    risks: List[str]
    opportunities: List[str]
    resource_needs: Dict[str, float]
    time_sensitivity: float  # 0-1，越高越紧急


@dataclass
class RiskAssessment:
    """风险评估"""
    risk_level: RiskLevel
    risk_score: float  # 0-1
    risk_factors: List[Dict[str, Any]]
    mitigations: List[str]
    worst_case: str
    best_case: str


@dataclass
class ResourceAllocation:
    """资源配置方案"""
    allocations: Dict[str, Dict[str, float]]  # resource -> {amount, priority}
    total_budget: float
    efficiency_score: float
    rationale: str


class SunziAnalyzer:
    """孙子兵法战略分析器
    
    基于《孙子兵法》五事七计框架：
    五事：道、天、地、将、法
    七计：主孰有道、将孰有能、天地孰得、法令孰行、兵众孰强、士卒孰练、赏罚孰明
    """
    
    FIVE_FACTORS = {
        '道': {'weight': 0.25, 'desc': '道义正当性，目标一致性'},
        '天': {'weight': 0.20, 'desc': '天时，时机与环境'},
        '地': {'weight': 0.20, 'desc': '地利，位置与资源'},
        '将': {'weight': 0.20, 'desc': '将领能力，执行力'},
        '法': {'weight': 0.15, 'desc': '法规制度，管理体系'},
    }
    
    def __init__(self):
        self.historical_analyses: List[Dict[str, Any]] = []
    
    def analyze_situation(
        self,
        five_factors: Dict[str, float],  # 五事评分 0-1
        context: Optional[Dict[str, Any]] = None
    ) -> StrategicSituation:
        """基于五事分析战略态势"""
        # 计算综合评分
        total_score = sum(
            five_factors.get(k, 0.5) * v['weight']
            for k, v in self.FIVE_FACTORS.items()
        )
        
        # 识别优势和劣势
        strengths = []
        weaknesses = []
        for factor, score in five_factors.items():
            if score >= 0.7:
                strengths.append(f"{factor}（{self.FIVE_FACTORS[factor]['desc']}）得分 {score:.2f}")
            elif score <= 0.3:
                weaknesses.append(f"{factor}（{self.FIVE_FACTORS[factor]['desc']}）得分 {score:.2f}")
        
        # 根据综合评分推荐战略
        strategy, rationale = self._recommend_strategy(total_score, five_factors)
        
        # 风险评估
        risks = self._identify_risks(five_factors, total_score)
        opportunities = self._identify_opportunities(five_factors, total_score)
        
        # 时间紧迫性（天时得分低则紧迫）
        time_sensitivity = 1.0 - five_factors.get('天', 0.5)
        
        result = StrategicSituation(
            situation_name=self._situation_name(total_score),
            strategy=strategy,
            confidence=min(0.95, total_score + 0.1),
            rationale=rationale,
            risks=risks,
            opportunities=opportunities,
            resource_needs=self._estimate_resources(strategy, total_score),
            time_sensitivity=time_sensitivity
        )
        
        self.historical_analyses.append({
            'timestamp': datetime.now().isoformat(),
            'five_factors': five_factors,
            'total_score': total_score,
            'strategy': strategy.value
        })
        
        return result
    
    def _recommend_strategy(
        self,
        score: float,
        factors: Dict[str, float]
    ) -> Tuple[StrategyType, str]:
        """根据评分推荐战略"""
        if score >= 0.8:
            return (
                StrategyType.ATTACK,
                "五事俱佳，宜积极进取。孙子曰：'胜兵先胜而后求战'，当前态势有利，应果断出击。"
            )
        elif score >= 0.6:
            if factors.get('将', 0.5) >= 0.7:
                return (
                    StrategyType.ALLIANCE,
                    "将领能力强而整体态势中等偏上，宜寻求合作联盟。'上兵伐谋，其次伐交'。"
                )
            else:
                return (
                    StrategyType.ADAPT,
                    "态势尚可但执行力不足，宜灵活变通。'兵无常势，水无常形'。"
                )
        elif score >= 0.4:
            return (
                StrategyType.DEFEND,
                "态势平庸，宜稳守固本。孙子曰：'善守者藏于九地之下'，先立于不败之地。"
            )
        elif score >= 0.2:
            return (
                StrategyType.RETREAT,
                "态势不利，宜收缩蓄力。'少则能逃之，不若则能避之'，保存实力为上。"
            )
        else:
            return (
                StrategyType.OBSERVE,
                "态势极差，宜静观其变。'非利不动，非得不用，非危不战'，等待时机。"
            )
    
    def _identify_risks(self, factors: Dict[str, float], score: float) -> List[str]:
        """识别风险"""
        risks = []
        if factors.get('道', 1.0) < 0.4:
            risks.append("道义不足：目标不够明确或团队共识不够，可能导致执行力低下")
        if factors.get('天', 1.0) < 0.3:
            risks.append("天时不利：外部环境不佳，市场或政策条件不成熟")
        if factors.get('地', 1.0) < 0.3:
            risks.append("地利缺失：资源或位置劣势，缺乏竞争优势")
        if factors.get('将', 1.0) < 0.4:
            risks.append("将领不力：执行能力不足，需要提升团队能力")
        if factors.get('法', 1.0) < 0.3:
            risks.append("法制不严：管理体系松散，流程不规范")
        if score < 0.3:
            risks.append("整体态势危险：五项均薄弱，不宜轻举妄动")
        return risks
    
    def _identify_opportunities(self, factors: Dict[str, float], score: float) -> List[str]:
        """识别机会"""
        opportunities = []
        if factors.get('将', 0.5) >= 0.7:
            opportunities.append("执行力强：可承担更具挑战性的任务")
        if factors.get('天', 0.5) >= 0.7:
            opportunities.append("天时有利：外部环境支持，应抓住窗口期")
        if factors.get('道', 0.5) >= 0.8:
            opportunities.append("道义充沛：团队高度一致，可推进重大变革")
        if score >= 0.5:
            opportunities.append("整体态势可战：具备行动基础条件")
        return opportunities
    
    def _estimate_resources(self, strategy: StrategyType, score: float) -> Dict[str, float]:
        """估算资源需求"""
        base = {'computing': 0.3, 'memory': 0.2, 'network': 0.2, 'storage': 0.1}
        multipliers = {
            StrategyType.ATTACK: 1.5,
            StrategyType.DEFEND: 0.8,
            StrategyType.ALLIANCE: 1.0,
            StrategyType.RETREAT: 0.5,
            StrategyType.OBSERVE: 0.3,
            StrategyType.ADAPT: 1.2,
        }
        m = multipliers.get(strategy, 1.0)
        return {k: min(1.0, v * m) for k, v in base.items()}
    
    def _situation_name(self, score: float) -> str:
        """态势名称"""
        if score >= 0.9:
            return "势如破竹"
        elif score >= 0.7:
            return "乘胜追击"
        elif score >= 0.5:
            return "稳扎稳打"
        elif score >= 0.3:
            return "固本培元"
        else:
            return "韬光养晦"


class GuanziOptimizer:
    """管子资源配置优化器
    
    基于《管子》的经济管理智慧：
    - 轻重之术：资源轻重缓急的配置
    - 四民分业：专业化分工
    - 盐铁之利：核心资源垄断与开放
    """
    
    def __init__(self):
        self.resource_history: List[Dict[str, Any]] = []
    
    def allocate_resources(
        self,
        available_resources: Dict[str, float],  # 可用资源 {name: amount}
        demands: List[Dict[str, Any]],          # 需求列表 [{name, priority, amount}]
        strategy: Optional[StrategyType] = None
    ) -> ResourceAllocation:
        """基于管子轻重之术配置资源"""
        
        # 按优先级排序
        priority_order = {
            ResourcePriority.CRITICAL: 4,
            ResourcePriority.IMPORTANT: 3,
            ResourcePriority.SUPPORTING: 2,
            ResourcePriority.OPTIONAL: 1,
        }
        
        sorted_demands = sorted(
            demands,
            key=lambda d: priority_order.get(d.get('priority', ResourcePriority.SUPPORTING), 0),
            reverse=True
        )
        
        allocations = {}
        remaining = dict(available_resources)
        total_budget = sum(available_resources.values())
        
        for demand in sorted_demands:
            name = demand['name']
            needed = demand.get('amount', 0.5)
            priority = demand.get('priority', ResourcePriority.SUPPORTING)
            
            # 找到对应资源
            best_resource = None
            best_amount = 0.0
            for res_name, res_amount in remaining.items():
                if res_amount > 0:
                    if best_resource is None or res_amount > best_amount:
                        best_resource = res_name
                        best_amount = res_amount
            
            if best_resource:
                allocated = min(needed, best_amount)
                remaining[best_resource] -= allocated
                
                # 根据战略类型调整
                if strategy == StrategyType.ATTACK:
                    allocated *= 1.2
                elif strategy == StrategyType.RETREAT:
                    allocated *= 0.7
                
                allocations[name] = {
                    'amount': min(1.0, allocated),
                    'priority': priority.value if isinstance(priority, ResourcePriority) else priority,
                    'resource': best_resource,
                }
            else:
                allocations[name] = {
                    'amount': 0.0,
                    'priority': priority.value if isinstance(priority, ResourcePriority) else priority,
                    'resource': None,
                }
        
        # 效率评分
        fulfilled = sum(1 for d in demands if allocations.get(d['name'], {}).get('amount', 0) >= d.get('amount', 0.5) * 0.8)
        efficiency = fulfilled / max(1, len(demands))
        
        result = ResourceAllocation(
            allocations=allocations,
            total_budget=total_budget,
            efficiency_score=efficiency,
            rationale=self._allocation_rationale(efficiency, strategy)
        )
        
        self.resource_history.append({
            'timestamp': datetime.now().isoformat(),
            'allocations': allocations,
            'efficiency': efficiency,
            'strategy': strategy.value if strategy else None,
        })
        
        return result
    
    def _allocation_rationale(self, efficiency: float, strategy: Optional[StrategyType]) -> str:
        """配置方案说明"""
        strat_text = strategy.value if strategy else "常规"
        if efficiency >= 0.8:
            return f"资源配置高效（{efficiency:.0%}），{strat_text}战略下资源利用充分"
        elif efficiency >= 0.5:
            return f"资源配置基本满足（{efficiency:.0%}），{strat_text}战略下部分需求未完全满足"
        else:
            return f"资源配置紧张（{efficiency:.0%}），{strat_text}战略下资源严重不足，建议调整"


class HuoZhiAnalyzer:
    """货殖列传时机分析器
    
    基于司马迁《货殖列传》的商业时机判断：
    - 旱则资舟，水则资车：逆向投资思维
    - 贵出如粪土，贱取如珠玉：买卖时机判断
    - 积著之理：囤积与释放的节奏
    """
    
    def __init__(self):
        self.market_observations: List[Dict[str, Any]] = []
    
    def evaluate_timing(
        self,
        market_indicators: Dict[str, float],  # {indicator: value}
        historical_data: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """评估商业时机"""
        
        # 计算市场热度（0=冷，1=热）
        heat = self._calculate_market_heat(market_indicators)
        
        # 逆向思维判断
        if heat > 0.8:
            action = "谨慎观望"
            advice = "市场过热，'贵出如粪土'，宜逢高减仓，等待回调"
            risk = RiskLevel.HIGH
        elif heat > 0.6:
            action = "逐步收缩"
            advice = "市场偏热，可适当获利了结，保留核心仓位"
            risk = RiskLevel.MODERATE
        elif heat > 0.4:
            action = "正常运作"
            advice = "市场平稳，按既定策略执行，关注结构性机会"
            risk = RiskLevel.MODERATE
        elif heat > 0.2:
            action = "逐步布局"
            advice = "市场偏冷，'贱取如珠玉'，宜逢低布局，建仓良机"
            risk = RiskLevel.LOW
        else:
            action = "积极建仓"
            advice = "市场极冷，'旱则资舟'，逆向布局最佳时机"
            risk = RiskLevel.LOW
        
        # 判断趋势
        trend = self._estimate_trend(market_indicators, historical_data)
        
        observation = {
            'timestamp': datetime.now().isoformat(),
            'market_heat': heat,
            'recommended_action': action,
            'advice': advice,
            'risk_level': risk.value,
            'trend': trend,
            'indicators': market_indicators,
        }
        
        self.market_observations.append(observation)
        if len(self.market_observations) > 50:
            self.market_observations = self.market_observations[-50:]
        
        return observation
    
    def _calculate_market_heat(self, indicators: Dict[str, float]) -> float:
        """计算市场热度"""
        if not indicators:
            return 0.5
        
        # 权重：资源使用率、响应延迟、错误率等
        weights = {
            'resource_usage': 0.3,
            'response_latency': 0.2,
            'error_rate': 0.2,
            'throughput': 0.15,
            'queue_depth': 0.15,
        }
        
        heat = 0.0
        total_weight = 0.0
        for indicator, value in indicators.items():
            w = weights.get(indicator, 0.1)
            heat += value * w
            total_weight += w
        
        return heat / max(total_weight, 0.01)
    
    def _estimate_trend(
        self,
        indicators: Dict[str, float],
        historical: Optional[List[Dict]]
    ) -> str:
        """估算趋势"""
        if not historical or len(historical) < 3:
            return "趋势不明，数据不足"
        
        recent_heat = [h.get('market_heat', 0.5) for h in historical[-5:]]
        if len(recent_heat) >= 3:
            avg_3 = sum(recent_heat[-3:]) / 3
            avg_prev = sum(recent_heat[:-3]) / max(1, len(recent_heat) - 3)
            
            if avg_3 > avg_prev + 0.1:
                return "上升"
            elif avg_3 < avg_prev - 0.1:
                return "下降"
            else:
                return "平稳"
        
        return "趋势不明"


class ShangdaoSystem:
    """商道战略系统主类
    
    整合孙子兵法（战略分析）、管子（资源配置）、货殖列传（时机判断），
    为东方智慧智能体提供商业级别的战略决策能力。
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.sunzi = SunziAnalyzer()
        self.guanzi = GuanziOptimizer()
        self.huozhi = HuoZhiAnalyzer()
        
        self.strategy_history: List[Dict[str, Any]] = []
        self.last_assessment: Optional[datetime] = None
    
    async def strategic_assessment(
        self,
        five_factors: Dict[str, float],
        market_indicators: Optional[Dict[str, float]] = None,
        available_resources: Optional[Dict[str, float]] = None,
        demands: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """综合战略评估
        
        Args:
            five_factors: 五事评分 {道, 天, 地, 将, 法}
            market_indicators: 市场/系统指标
            available_resources: 可用资源
            demands: 资源需求列表
        """
        self.last_assessment = datetime.now()
        
        # 孙子兵法战略分析
        situation = self.sunzi.analyze_situation(five_factors)
        
        # 管子资源配置
        resource_plan = None
        if available_resources and demands:
            resource_plan = self.guanzi.allocate_resources(
                available_resources, demands, situation.strategy
            )
        
        # 货殖列传时机判断
        timing = None
        if market_indicators:
            timing = self.huozhi.evaluate_timing(market_indicators)
        
        result = {
            'situation': {
                'name': situation.situation_name,
                'strategy': situation.strategy.value,
                'confidence': situation.confidence,
                'rationale': situation.rationale,
                'risks': situation.risks,
                'opportunities': situation.opportunities,
                'time_sensitivity': situation.time_sensitivity,
            },
            'resource_allocation': {
                'allocations': resource_plan.allocations if resource_plan else {},
                'efficiency': resource_plan.efficiency_score if resource_plan else None,
                'rationale': resource_plan.rationale if resource_plan else "未配置资源",
            } if resource_plan else None,
            'timing': timing,
            'overall_recommendation': self._overall_recommendation(situation, timing),
            'timestamp': self.last_assessment.isoformat(),
        }
        
        self.strategy_history.append(result)
        if len(self.strategy_history) > 20:
            self.strategy_history = self.strategy_history[-20:]
        
        return result
    
    async def risk_assessment(
        self,
        five_factors: Dict[str, float],
        scenario: Optional[str] = None
    ) -> RiskAssessment:
        """专项风险评估"""
        situation = self.sunzi.analyze_situation(five_factors)
        
        risk_score = 1.0 - situation.confidence
        if risk_score > 0.7:
            level = RiskLevel.CRITICAL
        elif risk_score > 0.5:
            level = RiskLevel.HIGH
        elif risk_score > 0.3:
            level = RiskLevel.MODERATE
        else:
            level = RiskLevel.LOW
        
        return RiskAssessment(
            risk_level=level,
            risk_score=risk_score,
            risk_factors=[
                {'factor': r.split('：')[0], 'detail': r}
                for r in situation.risks
            ],
            mitigations=[
                f"针对{r.split('：')[0]}：{self._suggest_mitigation(r)}"
                for r in situation.risks
            ],
            worst_case=f"若{situation.situation_name}恶化为全面劣势，可能导致系统资源枯竭",
            best_case=f"若{situation.situation_name}持续改善，{situation.opportunities[0] if situation.opportunities else '整体态势转好'}",
        )
    
    async def recommend_strategy(
        self,
        current_state: Dict[str, Any],
        goal: Optional[str] = None
    ) -> Dict[str, Any]:
        """推荐战略方案"""
        five_factors = current_state.get('five_factors', {
            '道': current_state.get('alignment', 0.5),
            '天': current_state.get('timing', 0.5),
            '地': current_state.get('resources', 0.5),
            '将': current_state.get('capability', 0.5),
            '法': current_state.get('management', 0.5),
        })
        
        situation = self.sunzi.analyze_situation(five_factors)
        
        return {
            'recommended_strategy': situation.strategy.value,
            'situation': situation.situation_name,
            'rationale': situation.rationale,
            'key_actions': self._suggest_key_actions(situation),
            'avoid_actions': self._suggest_avoid_actions(situation),
            'resource_focus': situation.resource_needs,
        }
    
    def _overall_recommendation(
        self,
        situation: StrategicSituation,
        timing: Optional[Dict]
    ) -> str:
        """综合建议"""
        parts = [f"战略态势：{situation.situation_name}，宜{situation.strategy.value}"]
        if timing:
            parts.append(f"市场判断：{timing['recommended_action']}，{timing['advice']}")
        parts.append(situation.rationale)
        return " | ".join(parts)
    
    def _suggest_mitigation(self, risk: str) -> str:
        """建议缓解措施"""
        if '道义' in risk:
            return "明确目标，统一共识，加强团队对齐"
        elif '天时' in risk:
            return "等待更好时机，或主动创造有利条件"
        elif '地利' in risk:
            return "补充资源储备，寻找替代方案"
        elif '将领' in risk:
            return "提升执行能力，引入外部支持"
        elif '法制' in risk:
            return "完善流程规范，加强管理"
        else:
            return "全面审视，逐项改善"
    
    def _suggest_key_actions(self, situation: StrategicSituation) -> List[str]:
        """建议关键行动"""
        actions_map = {
            StrategyType.ATTACK: ["快速部署核心资源", "扩大优势领域", "抢占先机"],
            StrategyType.DEFEND: ["加固核心壁垒", "减少非必要支出", "稳固基础"],
            StrategyType.ALLIANCE: ["寻求合作伙伴", "共享资源", "互利共赢"],
            StrategyType.RETREAT: ["收缩战线", "保存核心实力", "等待时机"],
            StrategyType.OBSERVE: ["收集情报", "分析趋势", "不做重大投入"],
            StrategyType.ADAPT: ["灵活调整策略", "小步快跑试错", "保持机动性"],
        }
        return actions_map.get(situation.strategy, ["审慎行事"])
    
    def _suggest_avoid_actions(self, situation: StrategicSituation) -> List[str]:
        """建议避免的行动"""
        avoid_map = {
            StrategyType.ATTACK: ["过度扩张", "忽视风险", "孤军深入"],
            StrategyType.DEFEND: ["盲目反击", "分散资源", "消极等待"],
            StrategyType.ALLIANCE: ["过度依赖伙伴", "丧失自主性", "利益分配不均"],
            StrategyType.RETREAT: ["完全放弃", "士气崩溃", "一蹶不振"],
            StrategyType.OBSERVE: ["错失窗口", "过度分析导致瘫痪"],
            StrategyType.ADAPT: ["频繁转向", "缺乏定力", "朝令夕改"],
        }
        return avoid_map.get(situation.strategy, ["贸然行动"])
