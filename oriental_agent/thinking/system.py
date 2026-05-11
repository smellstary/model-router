"""
Main Thinking System - Integration of Buddhist, Taoist, and Confucian philosophy
多哲学融合思考系统主模块 - 整合佛道儒三教思想
"""

import asyncio
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from core.types import ThinkingContext, ReasoningType, TimeHorizon, MemoryNode
from thinking.causal_analysis import CausalAnalysisSystem, CausalChain, KarmaAnalysis
from thinking.dialectical_thinking import (
    DialecticalThinkingSystem, 
    DialecticalAnalysis,
    WuweiDecision
)
from thinking.ethical_judgment import (
    EthicalJudgmentSystem,
    EthicalEvaluation,
    ZhongyongDecision
)
from config.settings import get_config


@dataclass
class ReasoningStep:
    """推理步骤"""
    step_id: str
    step_type: ReasoningType
    premise: Any
    inference: str
    conclusion: Any
    basis_memories: List[str] = field(default_factory=list)


@dataclass
class ThinkingResult:
    """思考结果"""
    conclusion: Any
    reasoning_trace: List[ReasoningStep] = field(default_factory=list)
    causal_analysis: Optional[CausalChain] = None
    dialectical_analysis: Optional[DialecticalAnalysis] = None
    ethical_evaluation: Optional[EthicalEvaluation] = None
    confidence: float = 0.0
    alternatives_considered: List[Any] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    philosophy_contributions: Dict[str, float] = field(default_factory=dict)


class ThinkingSystem:
    """融合三教思想的思考系统主类"""
    
    def __init__(self, config=None, memory_system=None):
        self.config = config or get_config()
        self.memory_system = memory_system
        
        self.causal_system = CausalAnalysisSystem()
        self.dialectical_system = DialecticalThinkingSystem()
        self.ethical_system = EthicalJudgmentSystem()
        
        self.philosophy_weights = self.config.get(
            'thinking.philosophy_weights',
            {'佛家': 0.33, '道家': 0.34, '儒家': 0.33}
        )
        
        self.reasoning_depth = self.config.get('thinking.reasoning_depth', 3)
        self.confidence_threshold = self.config.get(
            'thinking.decision_confidence_threshold', 0.7
        )
        
        self._thinking_history: List[ThinkingResult] = []
        self._lock = asyncio.Lock()
    
    async def analyze(
        self,
        context: ThinkingContext
    ) -> ThinkingResult:
        """综合思考分析"""
        reasoning_trace = []
        
        causal_result = await self._analyze_causal(context)
        if causal_result:
            reasoning_trace.extend(causal_result)
        
        dialectical_result = self.dialectical_system.analyze_dialectically(
            context.question,
            {'situation': context.situation}
        )
        
        ethical_result = self._analyze_ethical(context)
        if ethical_result:
            reasoning_trace.extend(ethical_result)
        
        zhongyong_result = self.ethical_system.make_zhongyong_decision(
            context.available_options,
            {'situation': context.situation}
        )
        
        wuwei_result = self.dialectical_system.make_wuwei_decision(
            context.situation,
            context.available_options
        )
        
        conclusion = self._synthesize_conclusion(
            dialectical_result,
            zhongyong_result,
            wuwei_result,
            context
        )
        
        confidence = self._calculate_confidence(
            dialectical_result,
            None,
            zhongyong_result
        )
        
        philosophy_contributions = {
            '佛家': self._estimate_buddhist_contribution(reasoning_trace),
            '道家': self._estimate_taoist_contribution(dialectical_result),
            '儒家': self._estimate_confucian_contribution(None)
        }
        
        result = ThinkingResult(
            conclusion=conclusion,
            reasoning_trace=reasoning_trace,
            causal_analysis=None,
            dialectical_analysis=dialectical_result,
            ethical_evaluation=ethical_result,
            confidence=confidence,
            alternatives_considered=context.available_options,
            recommended_actions=self._generate_recommendations(
                dialectical_result,
                ethical_result,
                zhongyong_result
            ),
            philosophy_contributions=philosophy_contributions
        )
        
        async with self._lock:
            self._thinking_history.append(result)
        
        return result
    
    async def _analyze_causal(
        self,
        context: ThinkingContext
    ) -> List[ReasoningStep]:
        """因果分析推理步骤"""
        steps = []
        
        if self.config.get('thinking.causal_analysis_enabled', True):
            for depth in range(min(self.reasoning_depth, 3)):
                chain = self.causal_system.analyze_causality(
                    context.question if depth == 0 else f"causal_level_{depth}",
                    {
                        'situation': context.situation,
                        'constraints': context.constraints
                    }
                )
                
                step = ReasoningStep(
                    step_id=f"causal_{depth}",
                    step_type=ReasoningType.CAUSAL,
                    premise=context.question,
                    inference=f"基于因果分析：{chain.root_causes}",
                    conclusion=chain.ultimate_effects,
                    basis_memories=[m.memory_id for m in context.relevant_memories[:3]]
                )
                steps.append(step)
        
        return steps
    
    def _analyze_ethical(
        self,
        context: ThinkingContext
    ) -> Optional[List[ReasoningStep]]:
        """伦理分析推理步骤"""
        if not self.config.get('thinking.ethical_judgment_enabled', True):
            return None
        
        steps = []
        
        for option in context.available_options[:3]:
            evaluation = self.ethical_system.evaluate_ethics(
                option,
                {'situation': context.situation}
            )
            
            step = ReasoningStep(
                step_id=f"ethical_{option}",
                step_type=ReasoningType.DEDUCTIVE,
                premise=option,
                inference=f"伦理评估：{evaluation.overall_moral_judgment}",
                conclusion=evaluation,
                basis_memories=[]
            )
            steps.append(step)
        
        return steps if steps else None
    
    def _synthesize_conclusion(
        self,
        dialectical: DialecticalAnalysis,
        zhongyong: ZhongyongDecision,
        wuwei: WuweiDecision,
        context: ThinkingContext
    ) -> Any:
        """综合形成结论"""
        if not context.available_options:
            return {
                'analysis': dialectical,
                'recommendation': dialectical.transformation_type.value,
                'harmony_score': dialectical.harmony_score
            }
        
        synthesis = {
            'primary_decision': zhongyong.decision,
            'approach': wuwei.action_level,
            'dialectical_insight': dialectical.transformation_type.value,
            'harmony_with_tao': wuwei.harmony_with_tao,
            'balance_score': zhongyong.balance_point,
            'confidence': (dialectical.harmony_score + 
                         zhongyong.harmony_score + 
                         wuwei.harmony_with_tao) / 3
        }
        
        return synthesis
    
    def _calculate_confidence(
        self,
        dialectical: DialecticalAnalysis,
        ethical: Optional[EthicalEvaluation],
        zhongyong: ZhongyongDecision
    ) -> float:
        """计算置信度"""
        confidence_factors = [
            dialectical.harmony_score
        ]
        
        if ethical:
            ethical_score = (
                ethical.ren_score + ethical.yi_score +
                ethical.li_score + ethical.zhi_score +
                ethical.xin_score
            ) / 5
            confidence_factors.append(ethical_score)
        
        confidence_factors.append(zhongyong.harmony_score)
        
        return sum(confidence_factors) / len(confidence_factors)
    
    def _estimate_buddhist_contribution(
        self,
        reasoning_trace: List[ReasoningStep]
    ) -> float:
        """估算佛家思想的贡献度"""
        causal_steps = sum(
            1 for step in reasoning_trace
            if step.step_type == ReasoningType.CAUSAL
        )
        
        return min(1.0, causal_steps * 0.3)
    
    def _estimate_taoist_contribution(
        self,
        dialectical: DialecticalAnalysis
    ) -> float:
        """估算道家思想的贡献度"""
        return dialectical.harmony_score
    
    def _estimate_confucian_contribution(
        self,
        ethical: Optional[EthicalEvaluation]
    ) -> float:
        """估算儒家思想的贡献度"""
        if not ethical:
            return 0.5
        
        avg_score = (
            ethical.ren_score + ethical.yi_score +
            ethical.li_score + ethical.zhi_score +
            ethical.xin_score
        ) / 5
        
        return avg_score
    
    def _generate_recommendations(
        self,
        dialectical: DialecticalAnalysis,
        ethical: Optional[EthicalEvaluation],
        zhongyong: ZhongyongDecision
    ) -> List[str]:
        """生成行动建议"""
        recommendations = []
        
        recommendations.append(
            f"顺势而为：{self.dialectical_system._determine_natural_approach(dialectical)}"
        )
        
        if ethical:
            improvement = self.ethical_system.recommend_moral_improvement(ethical)
            recommendations.append(
                f"道德提升：{improvement['recommendation']}"
            )
        
        if zhongyong.compromise_needed:
            recommendations.extend([
                f"中庸之道：{comp}" for comp in zhongyong.compromise_needed
            ])
        
        return recommendations
    
    async def causal_analysis(
        self,
        event: Any
    ) -> CausalChain:
        """执行因果分析"""
        return self.causal_system.analyze_causality(event)
    
    async def dialectical_think(
        self,
        subject: Any
    ) -> DialecticalAnalysis:
        """执行辩证思考"""
        return self.dialectical_system.analyze_dialectically(subject)
    
    async def ethical_judge(
        self,
        action: Any,
        context: Optional[Dict] = None
    ) -> EthicalEvaluation:
        """执行伦理判断"""
        return self.ethical_system.evaluate_ethics(action, context)
    
    async def make_decision(
        self,
        options: List[Any],
        context: ThinkingContext
    ) -> Any:
        """制定决策"""
        result = await self.analyze(context)
        return result.conclusion.get('primary_decision', options[0] if options else None)
    
    async def analyze_three_lives(
        self,
        event: Any
    ) -> Dict[str, Any]:
        """分析三世因果"""
        return self.causal_system.analyze_three_lives(event)
    
    async def apply_negation(
        self,
        proposition: Any
    ) -> Dict[str, Any]:
        """应用否定之否定律"""
        return self.dialectical_system.apply_negation(proposition)
    
    async def make_wuwei_decision(
        self,
        situation: Any,
        options: List[Any]
    ) -> WuweiDecision:
        """无为而治决策"""
        return self.dialectical_system.make_wuwei_decision(situation, options)
    
    async def apply_ren_yi_unity(
        self,
        action: Any
    ) -> Dict[str, Any]:
        """应用仁义合一原则"""
        return self.ethical_system.apply_ren_yi_unity(action)
    
    async def detect_turning_point(
        self,
        current_state: Any
    ) -> Optional[Dict[str, Any]]:
        """检测转化时机（否极泰来）"""
        return self.dialectical_system.detect_bujishengji(current_state)
    
    async def resolve_contradiction(
        self,
        contradiction: Tuple[Any, Any]
    ) -> Dict[str, Any]:
        """解决矛盾"""
        return self.dialectical_system.apply_contradiction_resolution(contradiction)
    
    async def get_system_state(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            'thinking_history_length': len(self._thinking_history),
            'philosophy_weights': self.philosophy_weights,
            'reasoning_depth': self.reasoning_depth,
            'confidence_threshold': self.confidence_threshold,
            'recent_philosophy_contributions': [
                result.philosophy_contributions
                for result in self._thinking_history[-5:]
            ]
        }
