"""
Dialectical Thinking System based on Taoist principles
基于道家思想的辩证思维系统
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class DialecticalAspect(Enum):
    """辩证方面"""
    YIN = "阴"
    YANG = "阳"
    NEUTRAL = "中"


class TransformationType(Enum):
    """转化类型"""
    YIN_TO_YANG = "阴极阳生"
    YANG_TO_YIN = "阳极阴生"
    BALANCED = "阴阳平衡"
    CONFLICTING = "阴阳对立"


@dataclass
class DialecticalAnalysis:
    """辩证分析结果"""
    subject: Any
    yin_aspects: List[str] = field(default_factory=list)
    yang_aspects: List[str] = field(default_factory=list)
    neutral_aspects: List[str] = field(default_factory=list)
    transformation_type: TransformationType = TransformationType.BALANCED
    transformation_likelihood: float = 0.0
    dialectical_tension: float = 0.0
    harmony_score: float = 0.5


@dataclass
class WuweiDecision:
    """无为决策"""
    decision: Any
    action_level: str
    intervention_needed: bool
    natural_flow_followed: bool
    harmony_with_tao: float


class DialecticalThinkingSystem:
    """辩证思维系统 - 道家辩证智慧"""
    
    def __init__(self):
        self.transformation_thresholds = {
            'yin_emerging': 0.3,
            'yang_emerging': 0.7,
            'extreme_yin': 0.1,
            'extreme_yang': 0.9
        }
        self.transformation_history: List[Dict] = []
        self.negation_history: List[Dict] = []
    
    def analyze_dialectically(
        self,
        subject: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> DialecticalAnalysis:
        """辩证分析"""
        yin_aspects = self._identify_yin_aspects(subject, context)
        yang_aspects = self._identify_yang_aspects(subject, context)
        neutral_aspects = self._identify_neutral_aspects(subject, context)
        
        dialectical_tension = self._calculate_tension(yin_aspects, yang_aspects)
        
        transformation_type, likelihood = self._predict_transformation(
            yin_aspects, yang_aspects, dialectical_tension
        )
        
        harmony_score = self._calculate_harmony(
            yin_aspects, yang_aspects, neutral_aspects
        )
        
        return DialecticalAnalysis(
            subject=subject,
            yin_aspects=yin_aspects,
            yang_aspects=yang_aspects,
            neutral_aspects=neutral_aspects,
            transformation_type=transformation_type,
            transformation_likelihood=likelihood,
            dialectical_tension=dialectical_tension,
            harmony_score=harmony_score
        )
    
    def _identify_yin_aspects(
        self,
        subject: Any,
        context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """识别阴的属性"""
        yin_characteristics = []
        
        subject_str = str(subject).lower()
        
        yin_keywords = {
            'internal': ['内部', '内在', '本质', '根', '本'],
            'passive': ['被动', '静', '柔', '退', '守'],
            'receptive': ['接受', '包容', '承载', '沉'],
            'cold': ['暗', '暗', '寒', '阴'],
            'feminine': ['柔', '静', '敛', '收']
        }
        
        for category, keywords in yin_keywords.items():
            if any(kw in subject_str for kw in keywords):
                yin_characteristics.append(category)
        
        if context:
            if context.get('state') in ['passive', 'resting', 'waiting']:
                yin_characteristics.append('state_passive')
            if context.get('energy_level', 1.0) < 0.5:
                yin_characteristics.append('low_energy')
        
        return yin_characteristics
    
    def _identify_yang_aspects(
        self,
        subject: Any,
        context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """识别阳的属笥"""
        yang_characteristics = []
        
        subject_str = str(subject).lower()
        
        yang_keywords = {
            'external': ['外部', '外在', '表象', '末', '标'],
            'active': ['主动', '动', '刚', '进', '攻'],
            'expansive': ['扩张', '发扬', '显明', '上升'],
            'hot': ['热', '明', '阳', '旺'],
            'masculine': ['刚', '动', '散', '发']
        }
        
        for category, keywords in yang_keywords.items():
            if any(kw in subject_str for kw in keywords):
                yang_characteristics.append(category)
        
        if context:
            if context.get('state') in ['active', 'moving', 'pushing']:
                yang_characteristics.append('state_active')
            if context.get('energy_level', 1.0) > 0.5:
                yang_characteristics.append('high_energy')
        
        return yang_characteristics
    
    def _identify_neutral_aspects(
        self,
        subject: Any,
        context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """识别中性的属性"""
        neutral = []
        
        if context:
            if 'balance' in context:
                neutral.append('balance_oriented')
            if 'transition' in context:
                neutral.append('in_transition')
        
        return neutral
    
    def _calculate_tension(
        self,
        yin_aspects: List[str],
        yang_aspects: List[str]
    ) -> float:
        """计算辩证张力"""
        if not yin_aspects and not yang_aspects:
            return 0.0
        
        tension = abs(len(yin_aspects) - len(yang_aspects)) / max(
            len(yin_aspects) + len(yang_aspects), 1
        )
        
        return min(1.0, tension)
    
    def _predict_transformation(
        self,
        yin_aspects: List[str],
        yang_aspects: List[str],
        tension: float
    ) -> Tuple[TransformationType, float]:
        """预测阴阳转化"""
        balance = (len(yang_aspects) - len(yin_aspects)) / max(
            len(yang_aspects) + len(yin_aspects), 1
        )
        
        if balance > 0.5:
            return TransformationType.YANG_TO_YIN, min(1.0, tension * 1.5)
        elif balance < -0.5:
            return TransformationType.YIN_TO_YANG, min(1.0, tension * 1.5)
        elif abs(balance) < 0.2:
            return TransformationType.BALANCED, 0.3
        else:
            return TransformationType.CONFLICTING, tension
    
    def _calculate_harmony(
        self,
        yin_aspects: List[str],
        yang_aspects: List[str],
        neutral_aspects: List[str]
    ) -> float:
        """计算和谐度"""
        total_aspects = len(yin_aspects) + len(yang_aspects) + len(neutral_aspects)
        
        if total_aspects == 0:
            return 0.5
        
        tension = self._calculate_tension(yin_aspects, yang_aspects)
        harmony = 1.0 - tension * 0.5
        
        if neutral_aspects:
            harmony += len(neutral_aspects) * 0.05
        
        return min(1.0, max(0.0, harmony))
    
    def apply_negation(
        self,
        proposition: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """应用否定之否定律"""
        first_negation = self._negate(proposition)
        second_negation = self._negate(first_negation['negated'])
        
        self.negation_history.append({
            'original': proposition,
            'first_negation': first_negation,
            'second_negation': second_negation,
            'timestamp': context.get('timestamp') if context else None
        })
        
        return {
            'original': proposition,
            'thesis': proposition,
            'antithesis': first_negation['negated'],
            'synthesis': second_negation['negated'],
            'dialectical_progress': self._evaluate_dialectical_progress(
                proposition, first_negation, second_negation
            )
        }
    
    def _negate(self, proposition: Any) -> Dict[str, Any]:
        """执行否定"""
        prop_str = str(proposition)
        
        opposite_pairs = {
            '是': '非',
            '有': '无',
            '动': '静',
            '阳': '阴',
            '进': '退',
            '刚': '柔',
            '正': '反',
            '显': '隐'
        }
        
        negated = prop_str
        for original, opposite in opposite_pairs.items():
            if original in negated:
                negated = negated.replace(original, opposite)
                break
        
        return {
            'negated': negated,
            'negation_type': 'partial' if negated != prop_str else 'complete'
        }
    
    def _evaluate_dialectical_progress(
        self,
        original: Any,
        first: Dict,
        second: Dict
    ) -> float:
        """评估辩证进展"""
        progress = 0.0
        
        if first['negated'] != str(original):
            progress += 0.3
        
        if second['negated'] != first['negated']:
            progress += 0.3
        
        if second['negated'] != str(original):
            progress += 0.4
        
        return min(1.0, progress)
    
    def make_wuwei_decision(
        self,
        situation: Any,
        options: List[Any],
        context: Optional[Dict[str, Any]] = None
    ) -> WuweiDecision:
        """无为而治的决策"""
        if not options:
            return WuweiDecision(
                decision=None,
                action_level="wuwei",
                intervention_needed=False,
                natural_flow_followed=True,
                harmony_with_tao=1.0
            )
        
        natural_flow_options = []
        for option in options:
            dialectical = self.analyze_dialectically(option, context)
            if dialectical.harmony_score > 0.6:
                natural_flow_options.append((option, dialectical.harmony_score))
        
        if natural_flow_options:
            best_option = max(natural_flow_options, key=lambda x: x[1])
            intervention_needed = False
            action_level = "wuwei"
        else:
            best_option = (options[0], 0.5)
            intervention_needed = True
            action_level = "weiwei"
        
        harmony = best_option[1]
        
        return WuweiDecision(
            decision=best_option[0],
            action_level=action_level,
            intervention_needed=intervention_needed,
            natural_flow_followed=not intervention_needed,
            harmony_with_tao=harmony
        )
    
    def follow_natural_flow(
        self,
        current_state: Any,
        target_state: Optional[Any] = None
    ) -> Dict[str, Any]:
        """顺应自然流向"""
        dialectical = self.analyze_dialectically(current_state)
        
        recommended_approach = self._determine_natural_approach(dialectical)
        
        return {
            'current_state': current_state,
            'dialectical_analysis': dialectical,
            'recommended_approach': recommended_approach,
            'effort_level': 'minimal' if dialectical.harmony_score > 0.7 else 'moderate',
            'expected_outcome': self._predict_natural_outcome(dialectical)
        }
    
    def _determine_natural_approach(
        self,
        analysis: DialecticalAnalysis
    ) -> str:
        """确定自然的行动方式"""
        if analysis.transformation_type == TransformationType.YANG_TO_YIN:
            return "顺应收敛趋势，减少干预"
        elif analysis.transformation_type == TransformationType.YIN_TO_YANG:
            return "顺应生发趋势，适时引导"
        elif analysis.transformation_type == TransformationType.BALANCED:
            return "保持平衡，顺其自然"
        else:
            return "寻求调和，化解张力"
    
    def _predict_natural_outcome(
        self,
        analysis: DialecticalAnalysis
    ) -> str:
        """预测自然的结局"""
        if analysis.transformation_likelihood > 0.7:
            return f"预计{analysis.transformation_type.value}"
        elif analysis.harmony_score > 0.8:
            return "和谐稳定"
        else:
            return "持续演变"
    
    def detect_bujishengji(
        self,
        current_state: Any,
        threshold: float = 0.8
    ) -> Optional[Dict[str, Any]]:
        """检测否极泰来时刻"""
        dialectical = self.analyze_dialectically(current_state)
        
        extreme_yin = dialectical.yin_aspects and len(dialectical.yang_aspects) == 0
        extreme_yang = dialectical.yang_aspects and len(dialectical.yin_aspects) == 0
        
        if extreme_yin and dialectical.transformation_likelihood > threshold:
            return {
                'type': 'turning_point',
                'direction': 'yin_to_yang',
                'message': '阴极阳生，转变在即',
                'readiness': dialectical.transformation_likelihood
            }
        elif extreme_yang and dialectical.transformation_likelihood > threshold:
            return {
                'type': 'turning_point',
                'direction': 'yang_to_yin',
                'message': '阳极阴生，收敛将至',
                'readiness': dialectical.transformation_likelihood
            }
        
        return None
    
    def apply_contradiction_resolution(
        self,
        contradiction: Tuple[Any, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """解决矛盾"""
        side_a, side_b = contradiction
        
        dialectical_a = self.analyze_dialectically(side_a, context)
        dialectical_b = self.analyze_dialectically(side_b, context)
        
        resolution_types = {
            'synthesis': self._synthesize(dialectical_a, dialectical_b),
            'sublation': self._sublate(dialectical_a, dialectical_b),
            'transcendence': self._transcend(dialectical_a, dialectical_b)
        }
        
        return {
            'original_contradiction': contradiction,
            'side_a_analysis': dialectical_a,
            'side_b_analysis': dialectical_b,
            'possible_resolutions': resolution_types,
            'recommended_resolution': resolution_types['synthesis']
        }
    
    def _synthesize(
        self,
        analysis_a: DialecticalAnalysis,
        analysis_b: DialecticalAnalysis
    ) -> str:
        """综合"""
        yin = set(analysis_a.yin_aspects) | set(analysis_b.yin_aspects)
        yang = set(analysis_a.yang_aspects) | set(analysis_b.yang_aspects)
        return f"综合阴阳：阴-{len(yin)}项，阳-{len(yang)}项"
    
    def _sublate(
        self,
        analysis_a: DialecticalAnalysis,
        analysis_b: DialecticalAnalysis
    ) -> str:
        """扬弃"""
        return "保留有益部分，舍弃消极因素"
    
    def _transcend(
        self,
        analysis_a: DialecticalAnalysis,
        analysis_b: DialecticalAnalysis
    ) -> str:
        """超越"""
        return "站在更高视角看待矛盾"
