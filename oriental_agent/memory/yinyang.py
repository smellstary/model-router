"""
Yin Yang balance system for dynamic state management
阴阳平衡系统
"""

from typing import Dict, Tuple
from core.types import HexagramType


class YinYangSystem:
    """Manages Yin Yang balance for memories and system states"""
    
    YIN_THRESHOLD = -0.5
    YANG_THRESHOLD = 0.5
    
    HEXAGRAM_YIN_YANG = {
        HexagramType.QIAN: 1.0,
        HexagramType.KUN: -1.0,
        HexagramType.ZHEN: 0.3,
        HexagramType.XUN: -0.3,
        HexagramType.KAN: -0.5,
        HexagramType.LI: 0.5,
        HexagramType.GEN: 0.2,
        HexagramType.DUI: -0.2
    }
    
    def __init__(self, initial_balance: float = 0.0):
        self.balance = initial_balance
        self.balance_history: list[float] = []
        self.transformation_log: list[Dict] = []
    
    def get_yin_yang_value(self, hexagram: HexagramType) -> float:
        """Get Yin Yang value for a hexagram"""
        return self.HEXAGRAM_YIN_YANG.get(hexagram, 0.0)
    
    def calculate_balance(
        self,
        positive_factors: float = 0.0,
        negative_factors: float = 0.0
    ) -> float:
        """Calculate current Yin Yang balance"""
        if positive_factors + negative_factors == 0:
            return 0.0
        
        total = positive_factors + negative_factors
        raw_balance = (positive_factors - negative_factors) / total
        
        self.balance = max(-1.0, min(1.0, raw_balance))
        
        self.balance_history.append(self.balance)
        if len(self.balance_history) > 100:
            self.balance_history = self.balance_history[-100:]
        
        return self.balance
    
    def apply_yin_yang_adjustment(
        self,
        memory_yin_yang: float,
        weight: float = 1.0
    ) -> None:
        """Apply Yin Yang influence from a memory"""
        adjustment = memory_yin_yang * weight * 0.1
        self.balance = max(-1.0, min(1.0, self.balance + adjustment))
        
        self.transformation_log.append({
            'type': 'adjustment',
            'memory_yin_yang': memory_yin_yang,
            'weight': weight,
            'new_balance': self.balance
        })
    
    def check_transformation(self) -> Tuple[bool, str]:
        """Check if Yin Yang transformation is occurring"""
        if self.balance >= self.YANG_THRESHOLD:
            return True, "yang_transforming"
        elif self.balance <= self.YIN_THRESHOLD:
            return True, "yin_transforming"
        return False, "balanced"
    
    def get_polarity(self) -> str:
        """Get current polarity state"""
        if self.balance > 0.3:
            return "yang_dominant"
        elif self.balance < -0.3:
            return "yin_dominant"
        elif self.balance > 0:
            return "yang_leading"
        elif self.balance < 0:
            return "yin_leading"
        return "balanced"
    
    def suggest_adjustment(self) -> Dict[str, float]:
        """Suggest adjustments to achieve better balance"""
        suggestions = {}
        
        if self.balance > 0.7:
            suggestions['yin_boost'] = 0.2
            suggestions['yang_reduce'] = 0.1
        elif self.balance < -0.7:
            suggestions['yang_boost'] = 0.2
            suggestions['yin_reduce'] = 0.1
        elif self.balance > 0.5:
            suggestions['yin_boost'] = 0.1
        elif self.balance < -0.5:
            suggestions['yang_boost'] = 0.1
        
        return suggestions
    
    def get_wuxing_yin_yang(self, wuxing_type: str) -> float:
        """Get Yin Yang tendency for Wu Xing element"""
        yin_yang_map = {
            '木': 0.3,
            '火': 0.6,
            '土': 0.0,
            '金': -0.3,
            '水': -0.6
        }
        return yin_yang_map.get(wuxing_type, 0.0)
    
    def calculate_composite_yin_yang(
        self,
        hexagram: HexagramType,
        wuxing: str,
        context_weight: float = 1.0
    ) -> float:
        """Calculate composite Yin Yang from multiple factors"""
        hex_value = self.get_yin_yang_value(hexagram)
        wuxing_value = self.get_wuxing_yin_yang(wuxing)
        
        return (hex_value * 0.6 + wuxing_value * 0.4) * context_weight
    
    def get_dynamic_state(self) -> Dict[str, any]:
        """Get comprehensive dynamic state information"""
        return {
            'balance': self.balance,
            'polarity': self.get_polarity(),
            'is_transforming': self.check_transformation()[0],
            'transformation_type': self.check_transformation()[1],
            'history_length': len(self.balance_history),
            'recent_trend': self._calculate_trend()
        }
    
    def _calculate_trend(self) -> str:
        """Calculate recent balance trend"""
        if len(self.balance_history) < 10:
            return "insufficient_data"
        
        recent = self.balance_history[-10:]
        first_half = sum(recent[:5]) / 5
        second_half = sum(recent[5:]) / 5
        
        if abs(second_half - first_half) < 0.1:
            return "stable"
        elif second_half > first_half:
            return "yang_trending"
        else:
            return "yin_trending"
    
    def apply_extreme_intervention(self) -> None:
        """Apply intervention when reaching extreme states"""
        if self.balance > 0.9:
            self.balance = 0.7
            self.transformation_log.append({
                'type': 'extreme_intervention',
                'from': 0.9,
                'to': 0.7,
                'reason': 'yang_extreme'
            })
        elif self.balance < -0.9:
            self.balance = -0.7
            self.transformation_log.append({
                'type': 'extreme_intervention',
                'from': -0.9,
                'to': -0.7,
                'reason': 'yin_extreme'
            })
