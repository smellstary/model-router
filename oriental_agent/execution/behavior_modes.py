"""
Behavior Modes System based on Wu Qin Xi (Five Animals Qigong)
基于五禽戏的行为模式系统
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class BehaviorMode(Enum):
    """行为模式"""
    TIGER = "虎形"       # 刚猛迅捷
    DEER = "鹿形"        # 轻盈敏捷
    BEAR = "熊形"        # 沉稳有力
    APE = "猿形"         # 灵巧多变
    BIRD = "鸟形"        # 高瞻远瞩


@dataclass
class BehaviorState:
    """行为状态"""
    current_mode: BehaviorMode
    energy_expenditure: float
    speed_rating: float
    stability_rating: float
    adaptability_rating: float
    adaptability_score: float = 0.0


@dataclass
class BehaviorContext:
    """行为上下文"""
    environment_type: str
    threat_level: float
    resource_availability: float
    time_constraint: Optional[float] = None
    precision_requirement: float = 0.5


class WuQinXiBehaviorSystem:
    """五禽戏行为模式系统"""
    
    def __init__(self):
        self.current_mode = BehaviorMode.BEAR
        self.mode_history: List[BehaviorMode] = []
        self.transition_log: List[Dict] = []
        
        self.mode_characteristics = {
            BehaviorMode.TIGER: {
                'energy_cost': 0.8,
                'speed': 0.9,
                'stability': 0.7,
                'adaptability': 0.5,
                'strength': 0.9,
                'description': '刚猛迅捷，适合紧急响应'
            },
            BehaviorMode.DEER: {
                'energy_cost': 0.4,
                'speed': 0.8,
                'stability': 0.6,
                'adaptability': 0.8,
                'strength': 0.5,
                'description': '轻盈敏捷，适合隐蔽行动'
            },
            BehaviorMode.BEAR: {
                'energy_cost': 0.5,
                'speed': 0.5,
                'stability': 0.9,
                'adaptability': 0.6,
                'strength': 0.8,
                'description': '沉稳有力，适合持久稳定'
            },
            BehaviorMode.APE: {
                'energy_cost': 0.6,
                'speed': 0.7,
                'stability': 0.5,
                'adaptability': 0.9,
                'strength': 0.6,
                'description': '灵巧多变，适合精细操作'
            },
            BehaviorMode.BIRD: {
                'energy_cost': 0.3,
                'speed': 0.6,
                'stability': 0.4,
                'adaptability': 0.7,
                'strength': 0.4,
                'description': '高瞻远瞩，适合战略规划'
            }
        }
    
    def select_mode(
        self,
        context: BehaviorContext
    ) -> BehaviorMode:
        """选择行为模式"""
        mode_scores = {}
        
        for mode in BehaviorMode:
            score = self._evaluate_mode(mode, context)
            mode_scores[mode] = score
        
        best_mode = max(mode_scores.items(), key=lambda x: x[1])[0]
        
        if best_mode != self.current_mode:
            self._record_transition(best_mode)
            self.current_mode = best_mode
        
        return best_mode
    
    def _evaluate_mode(
        self,
        mode: BehaviorMode,
        context: BehaviorContext
    ) -> float:
        """评估模式适用性"""
        char = self.mode_characteristics[mode]
        
        threat_score = self._evaluate_threat_response(mode, context.threat_level)
        resource_score = self._evaluate_resource_usage(mode, context.resource_availability)
        time_score = self._evaluate_time_fit(mode, context.time_constraint)
        precision_score = self._evaluate_precision_fit(mode, context.precision_requirement)
        
        weights = {
            'threat': 0.3,
            'resource': 0.2,
            'time': 0.2,
            'precision': 0.3
        }
        
        total_score = (
            threat_score * weights['threat'] +
            resource_score * weights['resource'] +
            time_score * weights['time'] +
            precision_score * weights['precision']
        )
        
        return total_score
    
    def _evaluate_threat_response(
        self,
        mode: BehaviorMode,
        threat_level: float
    ) -> float:
        """评估威胁响应"""
        if threat_level < 0.3:
            return 0.8
        elif threat_level < 0.6:
            if mode == BehaviorMode.TIGER:
                return 0.9
            elif mode == BehaviorMode.BEAR:
                return 0.8
            else:
                return 0.6
        else:
            if mode == BehaviorMode.TIGER:
                return 1.0
            elif mode == BehaviorMode.BEAR:
                return 0.9
            else:
                return 0.5
    
    def _evaluate_resource_usage(
        self,
        mode: BehaviorMode,
        resource_availability: float
    ) -> float:
        """评估资源使用"""
        char = self.mode_characteristics[mode]
        energy_cost = char['energy_cost']
        
        if resource_availability < 0.3:
            if energy_cost < 0.5:
                return 1.0
            else:
                return 0.5
        else:
            return 1.0 - energy_cost * 0.3
    
    def _evaluate_time_fit(
        self,
        mode: BehaviorMode,
        time_constraint: Optional[float]
    ) -> float:
        """评估时间契合度"""
        if time_constraint is None:
            return 0.7
        
        char = self.mode_characteristics[mode]
        speed = char['speed']
        
        if time_constraint < 0.3:
            return speed * 0.5
        elif time_constraint < 0.6:
            return speed * 0.8
        else:
            return speed
    
    def _evaluate_precision_fit(
        self,
        mode: BehaviorMode,
        precision_requirement: float
    ) -> float:
        """评估精度契合度"""
        if precision_requirement < 0.3:
            return 0.5
        elif precision_requirement < 0.6:
            if mode == BehaviorMode.APE:
                return 1.0
            elif mode == BehaviorMode.DEER:
                return 0.8
            else:
                return 0.6
        else:
            if mode == BehaviorMode.APE:
                return 1.0
            elif mode == BehaviorMode.DEER:
                return 0.9
            else:
                return 0.4
    
    def _record_transition(self, new_mode: BehaviorMode) -> None:
        """记录模式转换"""
        self.transition_log.append({
            'from': self.current_mode.value,
            'to': new_mode.value,
            'timestamp': None
        })
        self.mode_history.append(new_mode)
    
    def get_current_behavior_state(self) -> BehaviorState:
        """获取当前行为状态"""
        char = self.mode_characteristics[self.current_mode]
        
        return BehaviorState(
            current_mode=self.current_mode,
            energy_expenditure=char['energy_cost'],
            speed_rating=char['speed'],
            stability_rating=char['stability'],
            adaptability_rating=char['adaptability']
        )
    
    def execute_in_mode(
        self,
        action: Any,
        context: BehaviorContext
    ) -> Dict[str, Any]:
        """在当前模式下执行动作"""
        state = self.get_current_behavior_state()
        char = self.mode_characteristics[self.current_mode]
        
        result = {
            'action': action,
            'mode': self.current_mode.value,
            'execution_parameters': self._generate_parameters(char, action),
            'expected_outcome': self._predict_outcome(char, action),
            'energy_consumption': char['energy_cost']
        }
        
        return result
    
    def _generate_parameters(
        self,
        characteristics: Dict,
        action: Any
    ) -> Dict[str, Any]:
        """生成执行参数"""
        return {
            'speed': characteristics['speed'],
            'force': characteristics['strength'],
            'precision': characteristics['adaptability'],
            'stability': characteristics['stability'],
            'duration': 1.0 / characteristics['speed'] if characteristics['speed'] > 0 else 1.0
        }
    
    def _predict_outcome(
        self,
        characteristics: Dict,
        action: Any
    ) -> Dict[str, Any]:
        """预测动作结果"""
        return {
            'success_probability': characteristics['adaptability'] * 0.8 + 0.2,
            'impact_level': characteristics['strength'] * 0.7 + 0.3,
            'risk_level': 1.0 - characteristics['stability']
        }
    
    def transition_to(
        self,
        target_mode: BehaviorMode,
        reason: str = ""
    ) -> bool:
        """切换到指定模式"""
        if target_mode == self.current_mode:
            return False
        
        self._record_transition(target_mode)
        self.current_mode = target_mode
        
        return True
    
    def get_mode_compatibility(
        self,
        mode: BehaviorMode,
        environment: str
    ) -> float:
        """获取模式与环境的兼容性"""
        environment_mappings = {
            'hostile': BehaviorMode.TIGER,
            'stealth': BehaviorMode.DEER,
            'stable': BehaviorMode.BEAR,
            'complex': BehaviorMode.APE,
            'strategic': BehaviorMode.BIRD
        }
        
        compatible_mode = environment_mappings.get(environment, BehaviorMode.BEAR)
        
        if mode == compatible_mode:
            return 1.0
        elif mode == BehaviorMode.BEAR:
            return 0.7
        else:
            return 0.5
    
    def get_behavior_advice(self) -> str:
        """获取行为建议"""
        advice_templates = {
            BehaviorMode.TIGER: "当前状态适合采取主动进攻策略。保持警觉，快速响应。",
            BehaviorMode.DEER: "当前状态适合采取灵活应变策略。保持敏捷，随机而动。",
            BehaviorMode.BEAR: "当前状态适合采取稳健防守策略。稳如磐石，以逸待劳。",
            BehaviorMode.APE: "当前状态适合采取精巧操作策略。细致入微，灵活应对。",
            BehaviorMode.BIRD: "当前状态适合采取战略观察策略。高屋建瓴，审时度势。"
        }
        
        return advice_templates.get(self.current_mode, "保持当前状态")
    
    def get_system_state(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            'current_mode': self.current_mode.value,
            'mode_history_length': len(self.mode_history),
            'recent_transitions': len(self.transition_log),
            'mode_characteristics': self.mode_characteristics[self.current_mode],
            'advice': self.get_behavior_advice()
        }
