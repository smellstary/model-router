"""
Jing Qi Shen (Three Treasures) Model - 精气神三宝模型

Implements the Three Treasures (三宝) concept from Traditional Chinese Medicine:
- Jing (精): Essence, the material foundation of life
- Qi (气): Vital energy, the dynamic force of life
- Shen (神): Spirit, the consciousness and mental activities

Relationships:
- 精亏则气虚，气虚则神散 (Jing deficiency leads to Qi deficiency, Qi deficiency leads to Shen scattering)
- 神旺则气足，气足则精充 (Shen flourishing leads to sufficient Qi, sufficient Qi leads to abundant Jing)
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math


class TreasureType(Enum):
    """三宝类型枚举 - Three Treasures Enumeration"""
    JING = "精"
    QI = "气"
    SHEN = "神"


class RegulationMode(Enum):
    """调理模式枚举 - Regulation Mode Enumeration"""
    NOURISH_JING = "养精"
    REGULATE_QI = "调气"
    GATHER_SHEN = "聚神"
    BALANCE = "平衡"


@dataclass
class JingQiShenLevel:
    """
    精气神水平数据结构 - Jing Qi Shen Level Data Structure
    
    Attributes:
        jing_level: 精水平 (0.0-1.0) - 物质基础
        qi_level: 气水平 (0.0-1.0) - 能量流动
        shen_level: 神水平 (0.0-1.0) - 意识主导
    """
    jing_level: float = 0.5
    qi_level: float = 0.5
    shen_level: float = 0.5
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        self.jing_level = max(0.0, min(1.0, self.jing_level))
        self.qi_level = max(0.0, min(1.0, self.qi_level))
        self.shen_level = max(0.0, min(1.0, self.shen_level))
    
    @property
    def overall_vitality(self) -> float:
        """计算整体活力水平"""
        return (self.jing_level + self.qi_level + self.shen_level) / 3.0
    
    @property
    def balance_score(self) -> float:
        """计算精气神平衡分数"""
        levels = [self.jing_level, self.qi_level, self.shen_level]
        avg = sum(levels) / len(levels)
        variance = sum((l - avg) ** 2 for l in levels) / len(levels)
        max_variance = 0.25
        return 1.0 - min(1.0, variance / max_variance)
    
    def get_lowest_treasure(self) -> Tuple[TreasureType, float]:
        """获取最低水平的三宝"""
        levels = [
            (TreasureType.JING, self.jing_level),
            (TreasureType.QI, self.qi_level),
            (TreasureType.SHEN, self.shen_level)
        ]
        return min(levels, key=lambda x: x[1])
    
    def get_highest_treasure(self) -> Tuple[TreasureType, float]:
        """获取最高水平的三宝"""
        levels = [
            (TreasureType.JING, self.jing_level),
            (TreasureType.QI, self.qi_level),
            (TreasureType.SHEN, self.shen_level)
        ]
        return max(levels, key=lambda x: x[1])
    
    def to_dict(self) -> Dict:
        return {
            "jing_level": self.jing_level,
            "qi_level": self.qi_level,
            "shen_level": self.shen_level,
            "overall_vitality": self.overall_vitality,
            "balance_score": self.balance_score,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class RegulationResult:
    """调理结果数据结构"""
    mode: RegulationMode
    success: bool
    initial_state: JingQiShenLevel
    final_state: JingQiShenLevel
    changes: Dict[str, float]
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "mode": self.mode.value,
            "success": self.success,
            "initial_state": self.initial_state.to_dict(),
            "final_state": self.final_state.to_dict(),
            "changes": self.changes,
            "message": self.message,
            "timestamp": self.timestamp.isoformat()
        }


class JingQiShenModel:
    """
    精气神三宝模型主类 - Jing Qi Shen Three Treasures Model Main Class
    
    实现精气神的相互影响关系和动态平衡调节
    """
    
    ALERT_THRESHOLD = 0.3
    OPTIMAL_THRESHOLD = 0.7
    
    JING_QI_INFLUENCE = 0.15
    QI_SHEN_INFLUENCE = 0.15
    
    NOURISH_JING_RATE = 0.1
    REGULATE_QI_RATE = 0.12
    GATHER_SHEN_RATE = 0.08
    
    NATURAL_DECAY_RATE = 0.02
    REGENERATION_RATE = 0.01
    
    UPWARD_AMPLIFICATION = 1.2
    DOWNWARD_ATTENUATION = 0.8
    
    def __init__(self, initial_level: Optional[JingQiShenLevel] = None):
        self.current_level = initial_level or JingQiShenLevel()
        self.regulation_history: List[RegulationResult] = []
        self.state_history: List[JingQiShenLevel] = [self.current_level]
        self.auto_regulate_enabled = True
    
    def assess(self, context: Optional[Dict] = None) -> JingQiShenLevel:
        """
        实时状态评估 - Real-time State Assessment
        
        根据当前状态和上下文评估精气神水平
        
        Args:
            context: 可选的上下文信息，可能包含影响精气神的因素
            
        Returns:
            当前精气神水平状态
        """
        self._apply_natural_changes()
        
        if context:
            self._apply_context_influences(context)
        
        self._apply_inter_influences()
        
        self.current_level.timestamp = datetime.now()
        self.state_history.append(self.current_level)
        
        if len(self.state_history) > 100:
            self.state_history = self.state_history[-100:]
        
        return self.current_level
    
    def _apply_natural_changes(self) -> None:
        """应用自然变化（衰减和再生）"""
        self.current_level.jing_level = max(
            0.0, 
            min(1.0, 
                self.current_level.jing_level - self.NATURAL_DECAY_RATE * 0.5 + self.REGENERATION_RATE
            )
        )
        self.current_level.qi_level = max(
            0.0, 
            min(1.0, 
                self.current_level.qi_level - self.NATURAL_DECAY_RATE + self.REGENERATION_RATE * 1.5
            )
        )
        self.current_level.shen_level = max(
            0.0, 
            min(1.0, 
                self.current_level.shen_level - self.NATURAL_DECAY_RATE * 0.8 + self.REGENERATION_RATE
            )
        )
    
    def _apply_context_influences(self, context: Dict) -> None:
        """应用上下文影响因素"""
        if "activity_level" in context:
            activity = context["activity_level"]
            qi_consumption = activity * 0.05
            self.current_level.qi_level = max(0.0, self.current_level.qi_level - qi_consumption)
        
        if "mental_load" in context:
            mental_load = context["mental_load"]
            shen_consumption = mental_load * 0.04
            self.current_level.shen_level = max(0.0, self.current_level.shen_level - shen_consumption)
        
        if "rest_quality" in context:
            rest = context["rest_quality"]
            jing_recovery = rest * 0.03
            self.current_level.jing_level = min(1.0, self.current_level.jing_level + jing_recovery)
        
        if "nutrition" in context:
            nutrition = context["nutrition"]
            jing_boost = nutrition * 0.02
            qi_boost = nutrition * 0.025
            self.current_level.jing_level = min(1.0, self.current_level.jing_level + jing_boost)
            self.current_level.qi_level = min(1.0, self.current_level.qi_level + qi_boost)
    
    def _apply_inter_influences(self) -> None:
        """
        应用精气神相互影响 - Apply Inter-Influences among Jing, Qi, Shen
        
        相互影响关系：
        - 精亏则气虚，气虚则神散（下行影响）
        - 神旺则气足，气足则精充（上行影响）
        """
        jing = self.current_level.jing_level
        qi = self.current_level.qi_level
        shen = self.current_level.shen_level
        
        if jing < 0.5:
            qi_reduction = (0.5 - jing) * self.JING_QI_INFLUENCE * self.DOWNWARD_ATTENUATION
            self.current_level.qi_level = max(0.0, qi - qi_reduction)
        
        if qi < 0.5:
            shen_reduction = (0.5 - qi) * self.QI_SHEN_INFLUENCE * self.DOWNWARD_ATTENUATION
            self.current_level.shen_level = max(0.0, shen - shen_reduction)
        
        if shen > 0.5:
            qi_boost = (shen - 0.5) * self.QI_SHEN_INFLUENCE * self.UPWARD_AMPLIFICATION
            self.current_level.qi_level = min(1.0, self.current_level.qi_level + qi_boost)
        
        if qi > 0.5:
            jing_boost = (qi - 0.5) * self.JING_QI_INFLUENCE * self.UPWARD_AMPLIFICATION
            self.current_level.jing_level = min(1.0, self.current_level.jing_level + jing_boost)
    
    def nourish_jing(self, intensity: float = 0.5) -> RegulationResult:
        """
        养精机制 - Nourish Jing Mechanism
        
        通过调养来增强精的水平
        
        Args:
            intensity: 调养强度 (0.0-1.0)
            
        Returns:
            调理结果
        """
        initial_state = JingQiShenLevel(
            jing_level=self.current_level.jing_level,
            qi_level=self.current_level.qi_level,
            shen_level=self.current_level.shen_level
        )
        
        intensity = max(0.0, min(1.0, intensity))
        
        jing_increase = self.NOURISH_JING_RATE * intensity * (1.0 + 0.5 * self.current_level.qi_level)
        
        qi_cost = jing_increase * 0.3
        
        new_jing = min(1.0, self.current_level.jing_level + jing_increase)
        new_qi = max(0.0, self.current_level.qi_level - qi_cost)
        
        self.current_level.jing_level = new_jing
        self.current_level.qi_level = new_qi
        
        final_state = JingQiShenLevel(
            jing_level=self.current_level.jing_level,
            qi_level=self.current_level.qi_level,
            shen_level=self.current_level.shen_level
        )
        
        changes = {
            "jing_change": new_jing - initial_state.jing_level,
            "qi_change": new_qi - initial_state.qi_level,
            "shen_change": 0.0
        }
        
        result = RegulationResult(
            mode=RegulationMode.NOURISH_JING,
            success=True,
            initial_state=initial_state,
            final_state=final_state,
            changes=changes,
            message=f"养精调理完成，精水平提升 {changes['jing_change']:.3f}"
        )
        
        self._record_regulation(result)
        return result
    
    def regulate_qi(self, intensity: float = 0.5) -> RegulationResult:
        """
        调气机制 - Regulate Qi Mechanism
        
        通过调节来平衡气的流动
        
        Args:
            intensity: 调节强度 (0.0-1.0)
            
        Returns:
            调理结果
        """
        initial_state = JingQiShenLevel(
            jing_level=self.current_level.jing_level,
            qi_level=self.current_level.qi_level,
            shen_level=self.current_level.shen_level
        )
        
        intensity = max(0.0, min(1.0, intensity))
        
        target_qi = 0.7
        current_qi = self.current_level.qi_level
        
        if current_qi < target_qi:
            qi_change = self.REGULATE_QI_RATE * intensity * (1.0 + 0.3 * self.current_level.jing_level)
        else:
            qi_change = -self.REGULATE_QI_RATE * intensity * 0.5
        
        new_qi = max(0.0, min(1.0, current_qi + qi_change))
        
        shen_influence = qi_change * 0.2 if qi_change > 0 else qi_change * 0.1
        new_shen = max(0.0, min(1.0, self.current_level.shen_level + shen_influence))
        
        self.current_level.qi_level = new_qi
        self.current_level.shen_level = new_shen
        
        final_state = JingQiShenLevel(
            jing_level=self.current_level.jing_level,
            qi_level=self.current_level.qi_level,
            shen_level=self.current_level.shen_level
        )
        
        changes = {
            "jing_change": 0.0,
            "qi_change": new_qi - initial_state.qi_level,
            "shen_change": new_shen - initial_state.shen_level
        }
        
        result = RegulationResult(
            mode=RegulationMode.REGULATE_QI,
            success=True,
            initial_state=initial_state,
            final_state=final_state,
            changes=changes,
            message=f"调气调理完成，气水平变化 {changes['qi_change']:.3f}"
        )
        
        self._record_regulation(result)
        return result
    
    def gather_shen(self, intensity: float = 0.5) -> RegulationResult:
        """
        聚神机制 - Gather Shen Mechanism
        
        通过聚神来增强神（意识）的水平
        
        Args:
            intensity: 聚神强度 (0.0-1.0)
            
        Returns:
            调理结果
        """
        initial_state = JingQiShenLevel(
            jing_level=self.current_level.jing_level,
            qi_level=self.current_level.qi_level,
            shen_level=self.current_level.shen_level
        )
        
        intensity = max(0.0, min(1.0, intensity))
        
        shen_increase = self.GATHER_SHEN_RATE * intensity * (1.0 + 0.4 * self.current_level.qi_level)
        
        qi_cost = shen_increase * 0.25
        
        new_shen = min(1.0, self.current_level.shen_level + shen_increase)
        new_qi = max(0.0, self.current_level.qi_level - qi_cost)
        
        self.current_level.shen_level = new_shen
        self.current_level.qi_level = new_qi
        
        final_state = JingQiShenLevel(
            jing_level=self.current_level.jing_level,
            qi_level=self.current_level.qi_level,
            shen_level=self.current_level.shen_level
        )
        
        changes = {
            "jing_change": 0.0,
            "qi_change": new_qi - initial_state.qi_level,
            "shen_change": new_shen - initial_state.shen_level
        }
        
        result = RegulationResult(
            mode=RegulationMode.GATHER_SHEN,
            success=True,
            initial_state=initial_state,
            final_state=final_state,
            changes=changes,
            message=f"聚神调理完成，神水平提升 {changes['shen_change']:.3f}"
        )
        
        self._record_regulation(result)
        return result
    
    def balance(self, target_balance: float = 0.7) -> RegulationResult:
        """
        动态平衡调节 - Dynamic Balance Regulation
        
        自动检测并调节精气神的平衡状态
        
        Args:
            target_balance: 目标平衡水平 (0.0-1.0)
            
        Returns:
            调理结果
        """
        initial_state = JingQiShenLevel(
            jing_level=self.current_level.jing_level,
            qi_level=self.current_level.qi_level,
            shen_level=self.current_level.shen_level
        )
        
        adjustments = []
        total_changes = {"jing_change": 0.0, "qi_change": 0.0, "shen_change": 0.0}
        
        if self.current_level.jing_level < self.ALERT_THRESHOLD:
            result = self.nourish_jing(intensity=0.7)
            adjustments.append("养精")
            total_changes["jing_change"] += result.changes["jing_change"]
            total_changes["qi_change"] += result.changes["qi_change"]
        
        if self.current_level.qi_level < self.ALERT_THRESHOLD:
            result = self.regulate_qi(intensity=0.7)
            adjustments.append("调气")
            total_changes["qi_change"] += result.changes["qi_change"]
            total_changes["shen_change"] += result.changes["shen_change"]
        
        if self.current_level.shen_level < self.ALERT_THRESHOLD:
            result = self.gather_shen(intensity=0.7)
            adjustments.append("聚神")
            total_changes["shen_change"] += result.changes["shen_change"]
            total_changes["qi_change"] += result.changes["qi_change"]
        
        self._apply_balance_adjustment(target_balance)
        
        final_state = JingQiShenLevel(
            jing_level=self.current_level.jing_level,
            qi_level=self.current_level.qi_level,
            shen_level=self.current_level.shen_level
        )
        
        actual_changes = {
            "jing_change": final_state.jing_level - initial_state.jing_level,
            "qi_change": final_state.qi_level - initial_state.qi_level,
            "shen_change": final_state.shen_level - initial_state.shen_level
        }
        
        message = f"平衡调节完成，执行: {', '.join(adjustments) if adjustments else '维持现状'}"
        
        result = RegulationResult(
            mode=RegulationMode.BALANCE,
            success=True,
            initial_state=initial_state,
            final_state=final_state,
            changes=actual_changes,
            message=message
        )
        
        self._record_regulation(result)
        return result
    
    def _apply_balance_adjustment(self, target: float) -> None:
        """应用平衡调整"""
        avg_level = self.current_level.overall_vitality
        
        if avg_level < target:
            deficit = target - avg_level
            boost = deficit * 0.3
            
            lowest_type, lowest_level = self.current_level.get_lowest_treasure()
            
            if lowest_type == TreasureType.JING:
                self.current_level.jing_level = min(1.0, self.current_level.jing_level + boost)
            elif lowest_type == TreasureType.QI:
                self.current_level.qi_level = min(1.0, self.current_level.qi_level + boost)
            else:
                self.current_level.shen_level = min(1.0, self.current_level.shen_level + boost)
        
        balance_score = self.current_level.balance_score
        if balance_score < 0.7:
            self._harmonize_levels()
    
    def _harmonize_levels(self) -> None:
        """调和精气神水平，使其更加均衡"""
        levels = {
            TreasureType.JING: self.current_level.jing_level,
            TreasureType.QI: self.current_level.qi_level,
            TreasureType.SHEN: self.current_level.shen_level
        }
        
        avg = sum(levels.values()) / len(levels)
        
        harmonization_rate = 0.1
        
        for treasure_type in TreasureType:
            current = levels[treasure_type]
            if current < avg:
                boost = (avg - current) * harmonization_rate
                if treasure_type == TreasureType.JING:
                    self.current_level.jing_level = min(1.0, current + boost)
                elif treasure_type == TreasureType.QI:
                    self.current_level.qi_level = min(1.0, current + boost)
                else:
                    self.current_level.shen_level = min(1.0, current + boost)
    
    def _record_regulation(self, result: RegulationResult) -> None:
        """记录调理历史"""
        self.regulation_history.append(result)
        
        if len(self.regulation_history) > 100:
            self.regulation_history = self.regulation_history[-100:]
    
    def get_status_report(self) -> Dict:
        """获取状态报告"""
        lowest_type, lowest_level = self.current_level.get_lowest_treasure()
        highest_type, highest_level = self.current_level.get_highest_treasure()
        
        alerts = []
        if self.current_level.jing_level < self.ALERT_THRESHOLD:
            alerts.append({
                "treasure": "精",
                "level": self.current_level.jing_level,
                "recommendation": "建议进行养精调理"
            })
        if self.current_level.qi_level < self.ALERT_THRESHOLD:
            alerts.append({
                "treasure": "气",
                "level": self.current_level.qi_level,
                "recommendation": "建议进行调气调理"
            })
        if self.current_level.shen_level < self.ALERT_THRESHOLD:
            alerts.append({
                "treasure": "神",
                "level": self.current_level.shen_level,
                "recommendation": "建议进行聚神调理"
            })
        
        return {
            "current_level": self.current_level.to_dict(),
            "overall_vitality": self.current_level.overall_vitality,
            "balance_score": self.current_level.balance_score,
            "lowest_treasure": {
                "type": lowest_type.value,
                "level": lowest_level
            },
            "highest_treasure": {
                "type": highest_type.value,
                "level": highest_level
            },
            "alerts": alerts,
            "regulation_count": len(self.regulation_history)
        }
    
    def get_regulation_history(self, limit: int = 10) -> List[Dict]:
        """获取调理历史"""
        history = self.regulation_history[-limit:] if limit else self.regulation_history
        return [r.to_dict() for r in reversed(history)]
    
    def get_state_trend(self, periods: int = 5) -> Dict:
        """获取状态趋势"""
        if len(self.state_history) < 2:
            return {"trend": "insufficient_data"}
        
        recent_states = self.state_history[-periods:] if periods else self.state_history
        
        if len(recent_states) < 2:
            return {"trend": "insufficient_data"}
        
        jing_trend = recent_states[-1].jing_level - recent_states[0].jing_level
        qi_trend = recent_states[-1].qi_level - recent_states[0].qi_level
        shen_trend = recent_states[-1].shen_level - recent_states[0].shen_level
        
        def get_trend_direction(change: float) -> str:
            if change > 0.05:
                return "上升"
            elif change < -0.05:
                return "下降"
            else:
                return "稳定"
        
        return {
            "jing_trend": {
                "direction": get_trend_direction(jing_trend),
                "change": jing_trend
            },
            "qi_trend": {
                "direction": get_trend_direction(qi_trend),
                "change": qi_trend
            },
            "shen_trend": {
                "direction": get_trend_direction(shen_trend),
                "change": shen_trend
            },
            "overall_trend": get_trend_direction((jing_trend + qi_trend + shen_trend) / 3)
        }
    
    def reset(self, initial_level: Optional[JingQiShenLevel] = None) -> None:
        """重置模型状态"""
        self.current_level = initial_level or JingQiShenLevel()
        self.regulation_history.clear()
        self.state_history = [self.current_level]


def create_jing_qi_shen_model(
    jing_level: float = 0.5,
    qi_level: float = 0.5,
    shen_level: float = 0.5
) -> JingQiShenModel:
    """工厂函数：创建精气神模型"""
    initial_level = JingQiShenLevel(
        jing_level=jing_level,
        qi_level=qi_level,
        shen_level=shen_level
    )
    return JingQiShenModel(initial_level=initial_level)
