"""
Ethical Judgment System based on Confucian principles
基于儒家思想的伦理道德判断系统
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class FiveConstants(Enum):
    """五常"""
    REN = "仁"      # 仁爱
    YI = "义"       # 正义
    LI = "礼"       # 礼仪
    ZHI = "智"      # 智慧
    XIN = "信"      # 诚信


class MoralJudgment(Enum):
    """道德判断"""
    HIGHLY_MORAL = "高道德"
    MORAL = "道德"
    NEUTRAL = "中立"
    IMMORAL = "不道德"
    HIGHLY_IMMORAL = "极不道德"


@dataclass
class EthicalEvaluation:
    """伦理评估结果"""
    action: Any
    ren_score: float = 0.0
    yi_score: float = 0.0
    li_score: float = 0.0
    zhi_score: float = 0.0
    xin_score: float = 0.0
    overall_moral_judgment: MoralJudgment = MoralJudgment.NEUTRAL
    balance_evaluation: str = ""
    conflicts: List[str] = field(default_factory=list)


@dataclass
class ZhongyongDecision:
    """中庸决策"""
    decision: Any
    balance_point: float
    stakeholder_impacts: Dict[str, float]
    compromise_needed: List[str]
    harmony_score: float
    deviation_from_extremes: float


class EthicalJudgmentSystem:
    """伦理道德判断系统 - 儒家仁义礼智信"""
    
    def __init__(self):
        self.five_constants_weights = {
            FiveConstants.REN: 0.2,
            FiveConstants.YI: 0.2,
            FiveConstants.LI: 0.2,
            FiveConstants.ZHI: 0.2,
            FiveConstants.XIN: 0.2
        }
        self.moral_history: List[EthicalEvaluation] = []
        self.social_norm_database: Dict[str, List[str]] = {}
        self._initialize_social_norms()
    
    def _initialize_social_norms(self) -> None:
        """初始化社会规范数据库"""
        self.social_norm_database = {
            'family': ['孝', '悌', '慈', '和'],
            'society': ['忠', '恕', '礼', '义'],
            'personal': ['修身', '正心', '诚意', '格物'],
            'professional': ['敬', '勤', '信', '廉']
        }
    
    def evaluate_ethics(
        self,
        action: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> EthicalEvaluation:
        """评估行为的伦理道德"""
        ren_score = self._evaluate_ren(action, context)
        yi_score = self._evaluate_yi(action, context)
        li_score = self._evaluate_li(action, context)
        zhi_score = self._evaluate_zhi(action, context)
        xin_score = self._evaluate_xin(action, context)
        
        overall = self._compute_overall_moral_judgment(
            ren_score, yi_score, li_score, zhi_score, xin_score
        )
        
        balance_evaluation = self._evaluate_balance(
            ren_score, yi_score, li_score, zhi_score, xin_score
        )
        
        conflicts = self._identify_conflicts(
            ren_score, yi_score, li_score, zhi_score, xin_score
        )
        
        evaluation = EthicalEvaluation(
            action=action,
            ren_score=ren_score,
            yi_score=yi_score,
            li_score=li_score,
            zhi_score=zhi_score,
            xin_score=xin_score,
            overall_moral_judgment=overall,
            balance_evaluation=balance_evaluation,
            conflicts=conflicts
        )
        
        self.moral_history.append(evaluation)
        return evaluation
    
    def _evaluate_ren(self, action: Any, context: Optional[Dict[str, Any]]) -> float:
        """评估仁（仁爱之心）"""
        action_str = str(action).lower()
        
        ren_indicators = ['帮助', '关爱', '仁慈', '善意', '利他', '善待', '同情']
        non_ren_indicators = ['伤害', '冷漠', '残忍', '自私', '损人', '无情']
        
        ren_count = sum(1 for ind in ren_indicators if ind in action_str)
        non_ren_count = sum(1 for ind in non_ren_indicators if ind in action_str)
        
        score = 0.5
        score += ren_count * 0.1
        score -= non_ren_count * 0.1
        
        if context and 'beneficiary' in context:
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_yi(self, action: Any, context: Optional[Dict[str, Any]]) -> float:
        """评估义（正当适宜）"""
        action_str = str(action).lower()
        
        yi_indicators = ['正当', '合理', '公正', '公平', '合适', '应该', '正当']
        non_yi_indicators = ['不正当', '不合理', '偏私', '过分', '不当', '越矩']
        
        yi_count = sum(1 for ind in yi_indicators if ind in action_str)
        non_yi_count = sum(1 for ind in non_yi_indicators if ind in action_str)
        
        score = 0.5
        score += yi_count * 0.15
        score -= non_yi_count * 0.15
        
        if context and 'context_appropriateness' in context:
            score += context['context_appropriateness'] * 0.1
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_li(self, action: Any, context: Optional[Dict[str, Any]]) -> float:
        """评估礼（规范秩序）"""
        action_str = str(action).lower()
        
        li_indicators = ['礼貌', '规矩', '规范', '秩序', '尊敬', '谦逊', '礼仪']
        non_li_indicators = ['失礼', '无礼', '粗暴', '傲慢', '违规', '越礼']
        
        li_count = sum(1 for ind in li_indicators if ind in action_str)
        non_li_count = sum(1 for ind in non_li_indicators if ind in action_str)
        
        score = 0.5
        score += li_count * 0.1
        score -= non_li_count * 0.1
        
        if context and 'social_setting' in context:
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_zhi(self, action: Any, context: Optional[Dict[str, Any]]) -> float:
        """评估智（明辨是非）"""
        action_str = str(action).lower()
        
        zhi_indicators = ['明智', '理性', '判断', '分析', '辨别', '理解', '智慧']
        non_zhi_indicators = ['愚昧', '盲目', '冲动', '糊涂', '无知', '偏见']
        
        zhi_count = sum(1 for ind in zhi_indicators if ind in action_str)
        non_zhi_count = sum(1 for ind in non_zhi_indicators if ind in action_str)
        
        score = 0.5
        score += zhi_count * 0.12
        score -= non_zhi_count * 0.12
        
        if context and 'rational_basis' in context:
            score += context['rational_basis'] * 0.1
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_xin(self, action: Any, context: Optional[Dict[str, Any]]) -> float:
        """评估信（诚实可靠）"""
        action_str = str(action).lower()
        
        xin_indicators = ['诚实', '守信', '可靠', '承诺', '信用', '真诚', '坦诚']
        non_xin_indicators = ['欺骗', '虚伪', '失信', '谎言', '背信', '诈伪']
        
        xin_count = sum(1 for ind in xin_indicators if ind in action_str)
        non_xin_count = sum(1 for ind in non_xin_indicators if ind in action_str)
        
        score = 0.5
        score += xin_count * 0.15
        score -= non_xin_count * 0.15
        
        if context and 'promise_made' in context:
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _compute_overall_moral_judgment(
        self,
        ren: float,
        yi: float,
        li: float,
        zhi: float,
        xin: float
    ) -> MoralJudgment:
        """计算整体道德判断"""
        weighted_score = (
            ren * self.five_constants_weights[FiveConstants.REN] +
            yi * self.five_constants_weights[FiveConstants.YI] +
            li * self.five_constants_weights[FiveConstants.LI] +
            zhi * self.five_constants_weights[FiveConstants.ZHI] +
            xin * self.five_constants_weights[FiveConstants.XIN]
        )
        
        if weighted_score >= 0.8:
            return MoralJudgment.HIGHLY_MORAL
        elif weighted_score >= 0.6:
            return MoralJudgment.MORAL
        elif weighted_score >= 0.4:
            return MoralJudgment.NEUTRAL
        elif weighted_score >= 0.2:
            return MoralJudgment.IMMORAL
        else:
            return MoralJudgment.HIGHLY_IMMORAL
    
    def _evaluate_balance(
        self,
        ren: float,
        yi: float,
        li: float,
        zhi: float,
        xin: float
    ) -> str:
        """评估五常平衡"""
        scores = [ren, yi, li, zhi, xin]
        avg = sum(scores) / len(scores)
        variance = sum((s - avg) ** 2 for s in scores) / len(scores)
        
        if variance < 0.02:
            return "五常均衡，各方面协调发展"
        elif variance < 0.05:
            return "整体平衡，某些方面略有侧重"
        else:
            max_aspect = [('仁', ren), ('义', yi), ('礼', li), ('智', zhi), ('信', xin)]
            dominant = max(max_aspect, key=lambda x: x[1])
            return f"道德重心偏向于{dominant[0]}"
    
    def _identify_conflicts(
        self,
        ren: float,
        yi: float,
        li: float,
        zhi: float,
        xin: float
    ) -> List[str]:
        """识别道德冲突"""
        conflicts = []
        scores = {'仁': ren, '义': yi, '礼': li, '智': zhi, '信': xin}
        
        for aspect1, score1 in scores.items():
            for aspect2, score2 in scores.items():
                if aspect1 < aspect2 and abs(score1 - score2) > 0.4:
                    conflicts.append(f"{aspect1}与{aspect2}存在较大张力")
        
        if ren < 0.3 and yi > 0.7:
            conflicts.append("仁义冲突：为求正当可能牺牲仁爱")
        if li < 0.3 and xin > 0.7:
            conflicts.append("礼信冲突：坚守承诺可能失礼")
        
        return conflicts
    
    def make_zhongyong_decision(
        self,
        options: List[Any],
        context: Optional[Dict[str, Any]] = None
    ) -> ZhongyongDecision:
        """中庸决策 - 在极端之间寻找平衡点"""
        if not options:
            return ZhongyongDecision(
                decision=None,
                balance_point=0.5,
                stakeholder_impacts={},
                compromise_needed=[],
                harmony_score=0.0,
                deviation_from_extremes=0.0
            )
        
        option_evaluations = []
        for option in options:
            eval_result = self.evaluate_ethics(option, context)
            overall_score = (
                eval_result.ren_score * 0.2 +
                eval_result.yi_score * 0.2 +
                eval_result.li_score * 0.2 +
                eval_result.zhi_score * 0.2 +
                eval_result.xin_score * 0.2
            )
            option_evaluations.append((option, overall_score))
        
        scores = [e[1] for e in option_evaluations]
        max_score = max(scores)
        min_score = min(scores)
        
        if max_score - min_score < 0.1:
            best_option = options[len(options) // 2]
            balance_point = 0.5
        else:
            sorted_options = sorted(option_evaluations, key=lambda x: x[1])
            middle_idx = len(sorted_options) // 2
            best_option = sorted_options[middle_idx][0]
            balance_point = sorted_options[middle_idx][1]
        
        stakeholder_impacts = self._analyze_stakeholder_impacts(
            best_option, context
        )
        
        compromise_needed = self._determine_compromises(
            best_option, options
        )
        
        harmony_score = balance_point
        deviation = (max_score - min_score) / 2
        
        return ZhongyongDecision(
            decision=best_option,
            balance_point=balance_point,
            stakeholder_impacts=stakeholder_impacts,
            compromise_needed=compromise_needed,
            harmony_score=harmony_score,
            deviation_from_extremes=deviation
        )
    
    def _analyze_stakeholder_impacts(
        self,
        decision: Any,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, float]:
        """分析利益相关方影响"""
        impacts = {}
        
        if context and 'stakeholders' in context:
            for stakeholder in context['stakeholders']:
                impacts[stakeholder] = 0.5
        else:
            impacts['self'] = 0.5
            impacts['others'] = 0.5
        
        return impacts
    
    def _determine_compromises(
        self,
        chosen: Any,
        options: List[Any]
    ) -> List[str]:
        """确定需要的妥协"""
        compromises = []
        
        if len(options) > 1:
            compromises.append("需要平衡不同价值观")
        
        if chosen != options[0] and chosen != options[-1]:
            compromises.append("避免极端选择带来的风险")
        
        return compromises
    
    def evaluate_social_relationship(
        self,
        relationship_type: str,
        action: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """评估社会关系中的伦理"""
        if relationship_type in self.social_norm_database:
            relevant_norms = self.social_norm_database[relationship_type]
        else:
            relevant_norms = []
        
        ethics_result = self.evaluate_ethics(action, context)
        
        norm_compliance = []
        for norm in relevant_norms:
            if norm in str(action):
                norm_compliance.append((norm, True))
            else:
                norm_compliance.append((norm, False))
        
        return {
            'relationship_type': relationship_type,
            'relevant_norms': relevant_norms,
            'norm_compliance': norm_compliance,
            'ethics_evaluation': ethics_result,
            'relationship_health': ethics_result.overall_moral_judgment
        }
    
    def recommend_moral_improvement(
        self,
        current_evaluation: EthicalEvaluation
    ) -> Dict[str, Any]:
        """推荐道德提升建议"""
        scores = {
            '仁': current_evaluation.ren_score,
            '义': current_evaluation.yi_score,
            '礼': current_evaluation.li_score,
            '智': current_evaluation.zhi_score,
            '信': current_evaluation.xin_score
        }
        
        lowest_aspect = min(scores.items(), key=lambda x: x[1])
        
        recommendations = {
            '仁': '培养仁爱之心，多行善举',
            '义': '坚守正当原则，不做不当之事',
            '礼': '学习礼仪规范，尊重他人',
            '智': '提升明辨能力，多做理性思考',
            '信': '坚守诚信承诺，做可靠之人'
        }
        
        return {
            'weakest_aspect': lowest_aspect[0],
            'weakest_score': lowest_aspect[1],
            'recommendation': recommendations[lowest_aspect[0]],
            'all_scores': scores,
            'overall_judgment': current_evaluation.overall_moral_judgment
        }
    
    def apply_ren_yi_unity(
        self,
        action: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """应用仁义合一原则"""
        evaluation = self.evaluate_ethics(action, context)
        
        ren_yi_harmony = 1.0 - abs(evaluation.ren_score - evaluation.yi_score)
        
        if ren_yi_harmony > 0.8:
            unity_judgment = "仁义协调"
        elif ren_yy_harmony > 0.5:
            unity_judgment = "仁义基本一致"
        else:
            unity_judgment = "仁义需要调和"
        
        return {
            'action': action,
            'ren_score': evaluation.ren_score,
            'yi_score': evaluation.yi_score,
            'unity_score': ren_yi_harmony,
            'judgment': unity_judgment,
            'suggestion': self._suggest_ren_yi_balance(evaluation)
        }
    
    def _suggest_ren_yi_balance(
        self,
        evaluation: EthicalEvaluation
    ) -> str:
        """建议仁义平衡"""
        if evaluation.ren_score > evaluation.yi_score + 0.2:
            return "仁心有余，义理不足，需加强原则判断"
        elif evaluation.yi_score > evaluation.ren_score + 0.2:
            return "义理有余，仁心不足，需增加温情关怀"
        else:
            return "仁义平衡，继续保持"
