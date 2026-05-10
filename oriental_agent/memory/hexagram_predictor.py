"""
Hexagram Prediction Model (Tui Bei Tu inspired)
推背图序列预测模型
"""

from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from core.types import HexagramType, MemoryNode, WuxingType


class HexagramTransitionModel:
    """八卦转换模型 - 基于易经卦变原理"""
    
    HEXAGRAM_SYMBOLS = {
        '☰': HexagramType.QIAN,    # 乾
        '☷': HexagramType.KUN,    # 坤
        '☳': HexagramType.ZHEN,   # 震
        '☴': HexagramType.XUN,    # 巽
        '☵': HexagramType.KAN,    # 坎
        '☲': HexagramType.LI,     # 离
        '☶': HexagramType.GEN,    # 艮
        '☱': HexagramType.DUI     # 兑
    }
    
    TRIGRAMS_TRIGRAM_MAP = {
        HexagramType.QIAN: [1, 1, 1],
        HexagramType.KUN: [0, 0, 0],
        HexagramType.ZHEN: [0, 0, 1],
        HexagramType.XUN: [1, 0, 0],
        HexagramType.KAN: [0, 1, 0],
        HexagramType.LI: [1, 0, 1],
        HexagramType.GEN: [0, 1, 1],
        HexagramType.DUI: [1, 1, 0]
    }
    
    TRADITIONAL_TRANSITIONS = {
        HexagramType.QIAN: HexagramType.DUI,
        HexagramType.DUI: HexagramType.LI,
        HexagramType.LI: HexagramType.ZHEN,
        HexagramType.ZHEN: HexagramType.XUN,
        HexagramType.XUN: HexagramType.KAN,
        HexagramType.KAN: HexagramType.GEN,
        HexagramType.GEN: HexagramType.KUN,
        HexagramType.KUN: HexagramType.QIAN
    }
    
    def __init__(self):
        self.transition_matrix: Dict[HexagramType, Dict[HexagramType, float]] = {}
        self.memory_sequences: List[List[str]] = []
        self.sequence_patterns: Dict[str, int] = {}
        self._initialize_transition_matrix()
    
    def _initialize_transition_matrix(self) -> None:
        """初始化转换矩阵"""
        for source in HexagramType:
            self.transition_matrix[source] = {}
            for target in HexagramType:
                if source == self.TRADITIONAL_TRANSITIONS.get(source):
                    if target == source:
                        self.transition_matrix[source][target] = 0.6
                    else:
                        self.transition_matrix[source][target] = 0.05
                else:
                    self.transition_matrix[source][target] = 1.0 / 8
    
    def update_transition(self, from_hex: HexagramType, to_hex: HexagramType) -> None:
        """更新转换概率"""
        if to_hex not in self.transition_matrix[from_hex]:
            self.transition_matrix[from_hex][to_hex] = 0.0
        
        old_prob = self.transition_matrix[from_hex][to_hex]
        self.transition_matrix[from_hex][to_hex] = old_prob * 0.9 + 0.1
    
        total = sum(self.transition_matrix[from_hex].values())
        if total > 0:
            for hexagram in self.transition_matrix[from_hex]:
                self.transition_matrix[from_hex][hexagram] /= total
    
    def predict_next(
        self,
        current: HexagramType,
        context: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[HexagramType, float]]:
        """预测下一个最可能的卦象"""
        if current not in self.transition_matrix:
            return []
        
        predictions = []
        base_probs = self.transition_matrix[current].copy()
        
        if context:
            context_wuxing = context.get('wuxing')
            if context_wuxing:
                base_probs = self._apply_context_adjustment(base_probs, context_wuxing)
        
        for hexagram, prob in sorted(base_probs.items(), key=lambda x: x[1], reverse=True):
            predictions.append((hexagram, prob))
        
        return predictions[:3]
    
    def _apply_context_adjustment(
        self,
        probs: Dict[HexagramType, float],
        context_wuxing: str
    ) -> Dict[HexagramType, float]:
        """根据上下文调整概率"""
        wuxing_hexagram_map = {
            '木': [HexagramType.ZHEN, HexagramType.XUN],
            '火': [HexagramType.LI],
            '土': [HexagramType.KUN, HexagramType.GEN],
            '金': [HexagramType.QIAN, HexagramType.DUI],
            '水': [HexagramType.KAN]
        }
        
        relevant_hexagrams = wuxing_hexagram_map.get(context_wuxing, [])
        
        for hexagram in relevant_hexagrams:
            if hexagram in probs:
                probs[hexagram] *= 1.2
        
        return probs
    
    def record_sequence(self, sequence: List[str]) -> None:
        """记录卦象序列"""
        if len(sequence) >= 2:
            for i in range(len(sequence) - 1):
                try:
                    from_hex = HexagramType(sequence[i])
                    to_hex = HexagramType(sequence[i + 1])
                    self.update_transition(from_hex, to_hex)
                except ValueError:
                    pass
            
            pattern_key = ''.join(sequence[-3:]) if len(sequence) >= 3 else ''
            if pattern_key:
                self.sequence_patterns[pattern_key] = \
                    self.sequence_patterns.get(pattern_key, 0) + 1
    
    def detect_sequence_pattern(self, current: HexagramType) -> Optional[str]:
        """检测序列模式并预测"""
        predictions = self.predict_next(current)
        if predictions:
            return predictions[0][0].value
        return None


class TuibeituSequencePredictor:
    """推背图序列预测器"""
    
    def __init__(self):
        self.hexagram_model = HexagramTransitionModel()
        self.historical_predictions: List[Dict] = []
        self.sequence_templates: Dict[str, List[str]] = {}
        self.cycle_stages = {
            0: "天地初开",
            1: "万物生发",
            2: "繁荣鼎盛",
            3: "阴阳交替",
            4: "变化孕育",
            5: "转化过渡",
            6: "新秩序立",
            7: "循环往复"
        }
    
    def analyze_current_state(
        self,
        current_hexagram: HexagramType,
        memory_states: List[MemoryNode]
    ) -> Dict[str, Any]:
        """分析当前状态"""
        predictions = self.hexagram_model.predict_next(current_hexagram)
        
        active_wuxing = self._extract_active_wuxing(memory_states)
        
        return {
            'current_hexagram': current_hexagram.value,
            'predictions': [
                {'hexagram': h.value, 'probability': p}
                for h, p in predictions
            ],
            'active_wuxing': active_wuxing,
            'recommended_direction': self._suggest_direction(predictions, active_wuxing)
        }
    
    def _extract_active_wuxing(self, memories: List[MemoryNode]) -> List[str]:
        """提取活跃的五行"""
        wuxing_counts = {}
        for memory in memories:
            wuxing = memory.wuxing_attribute.value
            wuxing_counts[wuxing] = wuxing_counts.get(wuxing, 0) + memory.weight
        
        sorted_wuxing = sorted(wuxing_counts.items(), key=lambda x: x[1], reverse=True)
        return [w for w, _ in sorted_wuxing[:3]]
    
    def _suggest_direction(
        self,
        predictions: List[Tuple[HexagramType, float]],
        active_wuxing: List[str]
    ) -> str:
        """建议发展方向"""
        if not predictions:
            return "维持现状"
        
        top_hexagram = predictions[0][0]
        
        hexagram_meanings = {
            HexagramType.QIAN: "刚健进取",
            HexagramType.KUN: "柔顺包容",
            HexagramType.ZHEN: "震动变革",
            HexagramType.XUN: "柔顺渗透",
            HexagramType.KAN: "陷溺危险",
            HexagramType.LI: "光明依附",
            HexagramType.GEN: "静止安稳",
            HexagramType.DUI: "喜悦和谐"
        }
        
        return hexagram_meanings.get(top_hexagram, "观察等待")
    
    def predict_sequence(
        self,
        current: HexagramType,
        steps: int = 3,
        context: Optional[Dict] = None
    ) -> List[Dict]:
        """预测序列演化"""
        sequence = []
        current_hex = current
        
        for _ in range(steps):
            predictions = self.hexagram_model.predict_next(current_hex, context)
            if predictions:
                next_hex = predictions[0][0]
                sequence.append({
                    'hexagram': next_hex.value,
                    'probability': predictions[0][1],
                    'stage': self._get_stage_description(len(sequence))
                })
                current_hex = next_hex
            else:
                break
        
        return sequence
    
    def _get_stage_description(self, step: int) -> str:
        """获取阶段描述"""
        stage_key = step % len(self.cycle_stages)
        return self.cycle_stages[stage_key]
    
    def evaluate_sequence_quality(self, sequence: List[str]) -> float:
        """评估序列质量"""
        if len(sequence) < 2:
            return 0.0
        
        quality = 0.5
        
        pattern_key = ''.join(sequence[-3:]) if len(sequence) >= 3 else ''
        if pattern_key in self.sequence_patterns:
            frequency = self.sequence_patterns[pattern_key]
            quality += min(0.3, frequency * 0.05)
        
        try:
            for i in range(len(sequence) - 1):
                from_hex = HexagramType(sequence[i])
                to_hex = HexagramType(sequence[i + 1])
                prob = self.hexagram_model.transition_matrix.get(from_hex, {}).get(to_hex, 0)
                quality += prob * 0.1
        except ValueError:
            pass
        
        return min(1.0, max(0.0, quality))
    
    def suggest_intervention(
        self,
        current: HexagramType,
        target: HexagramType,
        memories: List[MemoryNode]
    ) -> Dict[str, Any]:
        """建议干预措施"""
        predictions = self.hexagram_model.predict_next(current)
        
        if not predictions:
            return {'action': '等待观察', 'reason': '预测不确定'}
        
        current_pred = predictions[0][0]
        
        if current_pred == target:
            return {
                'action': '顺其自然',
                'reason': '当前发展趋势与目标一致',
                'confidence': predictions[0][1]
            }
        
        alternative_path = self._find_alternative_path(current, target)
        
        return {
            'action': '引导调整',
            'reason': f'当前趋势为{current_pred.value}，需要引导至{target.value}',
            'suggested_path': alternative_path,
            'confidence': predictions[0][1]
        }
    
    def _find_alternative_path(
        self,
        start: HexagramType,
        end: HexagramType
    ) -> List[str]:
        """寻找替代路径"""
        path = [start.value]
        current = start
        max_steps = 5
        
        for _ in range(max_steps):
            predictions = self.hexagram_model.predict_next(current)
            
            for hexagram, prob in predictions:
                if hexagram == end:
                    path.append(end.value)
                    return path
            
            if predictions:
                current = predictions[0][0]
                path.append(current.value)
            else:
                break
        
        return path
