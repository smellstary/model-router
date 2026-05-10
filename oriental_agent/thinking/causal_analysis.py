"""
Causal Analysis System based on Buddhist principles
基于佛家思想的因果分析系统
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class CausalityType(Enum):
    """因果类型"""
    DIRECT = "直接因果"
    INDIRECT = "间接因果"
    CONDITIONAL = "条件因果"
    MUTUAL = "相互因果"
    CYCLIC = "循环因果"


class TimeHorizon(Enum):
    """时间视野"""
    PAST = "过去"
    PRESENT = "现在"
    FUTURE = "未来"


@dataclass
class CausalNode:
    """因果节点"""
    node_id: str
    event: Any
    causes: List[str] = field(default_factory=list)
    effects: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)
    karma_weight: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CausalChain:
    """因果链"""
    chain_id: str
    nodes: List[CausalNode] = field(default_factory=list)
    strength: float = 1.0
    time_horizon: TimeHorizon = TimeHorizon.PRESENT
    root_causes: List[str] = field(default_factory=list)
    ultimate_effects: List[str] = field(default_factory=list)


@dataclass
class KarmaAnalysis:
    """业力分析结果"""
    action_type: str
    intention: str
    consequence_score: float
    long_term_impact: float
    short_term_impact: float
    recommended_adjustment: str


class CausalAnalysisSystem:
    """因果分析系统 - 佛家因果智慧"""
    
    def __init__(self):
        self.causal_graph: Dict[str, CausalNode] = {}
        self.karma_history: List[KarmaAnalysis] = []
        self.condition_templates: Dict[str, List[str]] = {}
        self._initialize_condition_templates()
    
    def _initialize_condition_templates(self) -> None:
        """初始化条件模板"""
        self.condition_templates = {
            'success': ['effort', 'skill', 'timing', 'resources', 'circumstances'],
            'failure': ['obstacle', 'lack', 'mistake', 'external_factor'],
            'growth': ['learning', 'experience', 'adaptation', 'opportunity'],
            'conflict': ['misunderstanding', 'interest_clash', 'competition', 'ego']
        }
    
    def analyze_causality(
        self,
        event: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> CausalChain:
        """分析事件的因果关系"""
        chain_id = f"chain_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        direct_causes = self._identify_direct_causes(event, context)
        direct_effects = self._identify_direct_effects(event, context)
        conditions = self._evaluate_conditions(event, context)
        
        node = CausalNode(
            node_id=f"node_{len(self.causal_graph)}",
            event=event,
            causes=[c.node_id for c in direct_causes],
            effects=[e.node_id for e in direct_effects],
            conditions=conditions
        )
        
        self.causal_graph[node.node_id] = node
        
        chain = CausalChain(
            chain_id=chain_id,
            nodes=[node] + direct_causes + direct_effects,
            strength=self._calculate_chain_strength(node),
            root_causes=self._trace_root_causes(node),
            ultimate_effects=self._trace_ultimate_effects(node)
        )
        
        return chain
    
    def _identify_direct_causes(
        self,
        event: Any,
        context: Optional[Dict[str, Any]]
    ) -> List[CausalNode]:
        """识别直接原因"""
        causes = []
        
        if context:
            for key in ['previous_event', 'trigger', 'antecedent']:
                if key in context:
                    cause_event = context[key]
                    cause_node = CausalNode(
                        node_id=f"cause_{len(self.causal_graph)}_{key}",
                        event=cause_event
                    )
                    causes.append(cause_node)
                    self.causal_graph[cause_node.node_id] = cause_node
        
        return causes
    
    def _identify_direct_effects(
        self,
        event: Any,
        context: Optional[Dict[str, Any]]
    ) -> List[CausalNode]:
        """识别直接结果"""
        effects = []
        
        if context:
            for key in ['consequence', 'result', 'outcome']:
                if key in context:
                    effect_event = context[key]
                    effect_node = CausalNode(
                        node_id=f"effect_{len(self.causal_graph)}_{key}",
                        event=effect_event
                    )
                    effects.append(effect_node)
                    self.causal_graph[effect_node.node_id] = effect_node
        
        return effects
    
    def _evaluate_conditions(
        self,
        event: Any,
        context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """评估必要条件和充分条件"""
        conditions = []
        
        if context and 'conditions' in context:
            conditions.extend(context['conditions'])
        
        event_type = self._classify_event_type(event)
        if event_type in self.condition_templates:
            conditions.extend(self.condition_templates[event_type])
        
        return list(set(conditions))
    
    def _classify_event_type(self, event: Any) -> Optional[str]:
        """分类事件类型"""
        event_str = str(event).lower()
        
        type_keywords = {
            'success': ['成功', '完成', '达到', '实现', '成就'],
            'failure': ['失败', '错误', '挫折', '失误', '损失'],
            'growth': ['成长', '发展', '进步', '学习', '提升'],
            'conflict': ['冲突', '矛盾', '争执', '对立', '竞争']
        }
        
        for event_type, keywords in type_keywords.items():
            if any(kw in event_str for kw in keywords):
                return event_type
        
        return None
    
    def _calculate_chain_strength(self, node: CausalNode) -> float:
        """计算因果链强度"""
        if not node.causes:
            return 0.5
        
        cause_strengths = []
        for cause_id in node.causes:
            if cause_id in self.causal_graph:
                cause = self.causal_graph[cause_id]
                cause_strengths.append(cause.karma_weight)
        
        if not cause_strengths:
            return 0.5
        
        return sum(cause_strengths) / len(cause_strengths)
    
    def _trace_root_causes(self, node: CausalNode) -> List[str]:
        """追溯根本原因"""
        root_causes = []
        visited = set()
        
        def traverse(current_id: str):
            if current_id in visited:
                return
            visited.add(current_id)
            
            if current_id in self.causal_graph:
                current = self.causal_graph[current_id]
                if not current.causes:
                    root_causes.append(current_id)
                else:
                    for cause_id in current.causes:
                        traverse(cause_id)
        
        for node_id in node.causes:
            traverse(node_id)
        
        return root_causes
    
    def _trace_ultimate_effects(self, node: CausalNode) -> List[str]:
        """追溯最终结果"""
        ultimate_effects = []
        visited = set()
        
        def traverse(current_id: str):
            if current_id in visited:
                return
            visited.add(current_id)
            
            if current_id in self.causal_graph:
                current = self.causal_graph[current_id]
                if not current.effects:
                    ultimate_effects.append(current_id)
                else:
                    for effect_id in current.effects:
                        traverse(effect_id)
        
        for node_id in node.effects:
            traverse(node_id)
        
        return ultimate_effects
    
    def analyze_three_lives(
        self,
        current_event: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """分析三世因果"""
        analysis = {
            'short_term': self._analyze_timeframe(current_event, context, 'short'),
            'medium_term': self._analyze_timeframe(current_event, context, 'medium'),
            'long_term': self._analyze_timeframe(current_event, context, 'long')
        }
        
        return analysis
    
    def _analyze_timeframe(
        self,
        event: Any,
        context: Optional[Dict[str, Any]],
        timeframe: str
    ) -> Dict[str, Any]:
        """分析特定时间范围内的因果"""
        depth_map = {
            'short': 1,
            'medium': 3,
            'long': 5
        }
        
        chain = self.analyze_causality(event, context)
        
        return {
            'immediate_causes': chain.root_causes[:depth_map[timeframe]],
            'immediate_effects': chain.ultimate_effects[:depth_map[timeframe]],
            'chain_strength': chain.strength,
            'timeframe': timeframe
        }
    
    def analyze_karma(
        self,
        action: Any,
        intention: str,
        outcome: Any
    ) -> KarmaAnalysis:
        """分析行为业力"""
        intention_weight = self._evaluate_intention(intention)
        outcome_score = self._evaluate_outcome(outcome)
        
        karma_analysis = KarmaAnalysis(
            action_type=str(type(action).__name__),
            intention=intention,
            consequence_score=intention_weight * outcome_score,
            long_term_impact=self._estimate_long_term_impact(action, intention),
            short_term_impact=self._estimate_short_term_impact(action, outcome),
            recommended_adjustment=self._suggest_karma_adjustment(
                intention_weight, outcome_score
            )
        )
        
        self.karma_history.append(karma_analysis)
        return karma_analysis
    
    def _evaluate_intention(self, intention: str) -> float:
        """评估意图的善恶程度"""
        good_keywords = ['善', '帮助', '利他', '慈悲', '智慧']
        bad_keywords = ['恶', '伤害', '自私', '贪欲', '嗔恨']
        
        score = 0.5
        
        for kw in good_keywords:
            if kw in intention:
                score += 0.1
        for kw in bad_keywords:
            if kw in intention:
                score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_outcome(self, outcome: Any) -> float:
        """评估结果的好坏"""
        outcome_str = str(outcome).lower()
        
        if any(kw in outcome_str for kw in ['成功', '正面', '良好']):
            return 0.8
        elif any(kw in outcome_str for kw in ['失败', '负面', '不良']):
            return 0.3
        
        return 0.5
    
    def _estimate_long_term_impact(self, action: Any, intention: str) -> float:
        """估算长期影响"""
        intention_score = self._evaluate_intention(intention)
        return intention_score * 0.7 + 0.3
    
    def _estimate_short_term_impact(self, action: Any, outcome: Any) -> float:
        """估算短期影响"""
        outcome_score = self._evaluate_outcome(outcome)
        return outcome_score
    
    def _suggest_karma_adjustment(
        self,
        intention: float,
        outcome: float
    ) -> str:
        """建议业力调整"""
        if intention < 0.3 and outcome < 0.3:
            return "需要反思动机和结果，避免负面业力积累"
        elif intention > 0.7 and outcome < 0.3:
            return "善念但结果不佳，需要调整方法"
        elif intention < 0.3 and outcome > 0.7:
            return "结果虽好但动机需审视，保持正念"
        else:
            return "保持当前平衡状态"
    
    def analyze_conditions(
        self,
        target_outcome: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """分析达成目标所需条件"""
        necessary = self._find_necessary_conditions(target_outcome, context)
        sufficient = self._find_sufficient_conditions(target_outcome, context)
        obstacles = self._identify_obstacles(target_outcome, context)
        
        return {
            'necessary_conditions': necessary,
            'sufficient_conditions': sufficient,
            'potential_obstacles': obstacles,
            'readiness_score': self._calculate_readiness(necessary, obstacles)
        }
    
    def _find_necessary_conditions(
        self,
        outcome: Any,
        context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """找出必要条件"""
        event_type = self._classify_event_type(outcome)
        if event_type and event_type in self.condition_templates:
            return self.condition_templates[event_type].copy()
        return []
    
    def _find_sufficient_conditions(
        self,
        outcome: Any,
        context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """找出充分条件"""
        necessary = self._find_necessary_conditions(outcome, context)
        return necessary + ['timing', 'persistence', 'adaptability']
    
    def _identify_obstacles(
        self,
        outcome: Any,
        context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """识别潜在障碍"""
        obstacles = []
        
        if context and 'obstacles' in context:
            obstacles.extend(context['obstacles'])
        
        return list(set(obstacles))
    
    def _calculate_readiness(
        self,
        conditions: List[str],
        obstacles: List[str]
    ) -> float:
        """计算准备就绪度"""
        if not conditions:
            return 0.5
        
        readiness = len(conditions) / (len(conditions) + len(obstacles))
        return max(0.0, min(1.0, readiness))
