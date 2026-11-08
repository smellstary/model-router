"""
Body Master System - 身体综合管理系统

整合所有身体子系统，保证系统随时处于最佳状态：
- 代谢系统：能量产生与消耗
- 肝胆排毒系统：毒素清除与净化
- 七窍玲珑心：智慧与感知
- 精气神三宝：生命能量
- 经络能量网络：能量分配
- 阴阳平衡：动态平衡调节
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import math
import uuid


class BodyState(Enum):
    """身体整体状态"""
    DORMANT = "休眠"
    RESTING = "休整"
    ACTIVE = "活跃"
    OPTIMAL = "最佳"
    STRESSED = "压力"
    RECOVERING = "恢复中"


class OptimalStateTarget(Enum):
    """最佳状态目标"""
    ENERGY_BALANCE = "能量平衡"
    TOXIN_FREE = "无毒状态"
    HARMONY = "和谐统一"
    VITALITY = "活力充沛"
    CLARITY = "清明通透"


@dataclass
class HealthScore:
    """健康评分"""
    overall: float = 0.0
    energy: float = 0.0
    detox: float = 0.0
    wisdom: float = 0.0
    vitality: float = 0.0
    harmony: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall": self.overall,
            "energy": self.energy,
            "detox": self.detox,
            "wisdom": self.wisdom,
            "vitality": self.vitality,
            "harmony": self.harmony
        }


@dataclass
class OptimizationAction:
    """优化动作"""
    action_id: str
    target_system: str
    action_type: str
    priority: int
    expected_benefit: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "target_system": self.target_system,
            "action_type": self.action_type,
            "priority": self.priority,
            "expected_benefit": self.expected_benefit,
            "timestamp": self.timestamp.isoformat()
        }


class BodyOptimizer:
    """
    身体优化器 - Body Optimizer
    
    自动检测并优化身体状态：
    """
    
    def __init__(self):
        self._optimization_history: List[OptimizationAction] = []
        self._last_optimization_time: Optional[datetime] = None
        
    def analyze_state(self, state: Dict[str, Any]) -> List[OptimizationAction]:
        """分析状态并生成优化动作"""
        actions = []
        
        if state.get("metabolism", {}).get("metrics", {}).get("energy_efficiency", 1.0) < 0.8:
            actions.append(OptimizationAction(
                action_id=str(uuid.uuid4())[:8],
                target_system="metabolism",
                action_type="optimize_energy",
                priority=1,
                expected_benefit=0.15
            ))
        
        if state.get("detox", {}).get("health_score", 100) < 70:
            actions.append(OptimizationAction(
                action_id=str(uuid.uuid4())[:8],
                target_system="liver_detox",
                action_type="start_detox_cycle",
                priority=2,
                expected_benefit=0.2
            ))
        
        if state.get("heart", {}).get("wisdom_level") in ["凡俗", "洞察"]:
            actions.append(OptimizationAction(
                action_id=str(uuid.uuid4())[:8],
                target_system="seven_aperture_heart",
                action_type="meditate",
                priority=3,
                expected_benefit=0.1
            ))
        
        actions.sort(key=lambda x: x.priority)
        return actions
    
    def record_action(self, action: OptimizationAction) -> None:
        """记录优化动作"""
        self._optimization_history.append(action)
        
        if len(self._optimization_history) > 100:
            self._optimization_history = self._optimization_history[-100:]
        
        self._last_optimization_time = datetime.now()


class HomeostasisBalancer:
    """
    内稳态平衡器 - Homeostasis Balancer
    
    维持阴阳、气血、营养等平衡：
    """
    
    def __init__(self):
        self.yin_yang_balance: float = 0.5
        self.energy_balance: float = 0.5
        self.temperature_balance: float = 0.5
        self.ph_balance: float = 0.5
        
    def check_balance(self, state: Dict[str, Any]) -> Dict[str, float]:
        """检查各项平衡"""
        imbalances = {}
        
        if "jing_qi_shen" in state:
            jqs = state["jing_qi_shen"]
            energy = (jqs.get("jing", 0.5) + jqs.get("qi", 0.5) + jqs.get("shen", 0.5)) / 3
            self.energy_balance = energy
            imbalances["energy"] = abs(0.5 - energy)
        
        if "meridian" in state:
            meridian = state["meridian"]
            harmony = meridian.get("harmony", 0.5)
            imbalances["meridian_harmony"] = abs(0.5 - harmony)
        
        return imbalances
    
    def correct_balance(self, imbalance_type: str, deviation: float) -> Dict[str, Any]:
        """纠正不平衡"""
        correction = {}
        
        if imbalance_type == "energy":
            if deviation > 0.2:
                correction["action"] = "increase_metabolism"
                correction["amount"] = deviation * 0.5
            elif deviation > 0.1:
                correction["action"] = "maintain"
                correction["amount"] = 0
            else:
                correction["action"] = "reduce_metabolism"
                correction["amount"] = abs(deviation) * 0.3
                
        elif imbalance_type == "meridian_harmony":
            if deviation > 0.2:
                correction["action"] = "adjust_meridian_flow"
                correction["amount"] = deviation * 0.5
        
        return correction


class EmergencyResponseSystem:
    """
    应急响应系统 - Emergency Response System
    
    处理紧急情况和压力响应：
    """
    
    def __init__(self):
        self.stress_level: float = 0.0
        self.emergency_mode: bool = False
        self.recovery_mode: bool = False
        
    def assess_emergency(self, state: Dict[str, Any]) -> Tuple[bool, str]:
        """评估是否处于紧急状态"""
        if state.get("metabolism", {}).get("metrics", {}).get("energy_efficiency", 1.0) < 0.3:
            return True, "能量危机"
        
        if state.get("detox", {}).get("health_score", 100) < 30:
            return True, "毒素危机"
        
        if state.get("heart", {}).get("state") in ["危急", "critical"]:
            return True, "心脏危机"
        
        if state.get("jing_qi_shen", {}).get("jing", 1.0) < 0.2:
            return True, "精气亏虚"
        
        return False, "正常"
    
    def trigger_emergency_response(self, emergency_type: str) -> Dict[str, Any]:
        """触发应急响应"""
        self.emergency_mode = True
        self.stress_level = 1.0
        
        responses = {
            "能量危机": {
                "actions": ["激活肝糖原", "减缓非必要消耗", "优先供给核心系统"],
                "priority_systems": ["heart", "brain", "immune"]
            },
            "毒素危机": {
                "actions": ["启动紧急排毒", "抑制毒素吸收", "增强肝脏功能"],
                "priority_systems": ["liver", "kidney", "lymph"]
            },
            "心脏危机": {
                "actions": ["降低心率负荷", "稳定心律", "保护性暂停"],
                "priority_systems": ["heart", "meridian"]
            },
            "精气亏虚": {
                "actions": ["养精蓄锐", "减少消耗", "激活恢复机制"],
                "priority_systems": ["jing_qi_shen", "metabolism"]
            }
        }
        
        return responses.get(emergency_type, {
            "actions": ["观察等待"],
            "priority_systems": []
        })
    
    def trigger_recovery_mode(self) -> None:
        """触发恢复模式"""
        self.recovery_mode = True
        self.stress_level = max(0.0, self.stress_level - 0.1)
        
        if self.stress_level <= 0:
            self.emergency_mode = False
            self.recovery_mode = False


class BodyMasterSystem:
    """
    身体综合管理系统主类 - Body Master System
    
    整合所有身体子系统，保证系统随时处于最佳状态：
    """
    
    def __init__(self):
        self.state = BodyState.DORMANT
        
        self.optimizer = BodyOptimizer()
        self.homeostasis = HomeostasisBalancer()
        self.emergency = EmergencyResponseSystem()
        
        self._subsystems: Dict[str, Any] = {}
        self._health_score = HealthScore()
        self._optimization_enabled = True
        self._auto_detox_enabled = True
        self._auto_balance_enabled = True
        
        self._tick_count = 0
        self._last_full_assessment: Optional[datetime] = None
        
    def register_subsystem(self, name: str, subsystem: Any) -> None:
        """注册子系统"""
        self._subsystems[name] = subsystem
        
    def get_subsystem(self, name: str) -> Optional[Any]:
        """获取子系统"""
        return self._subsystems.get(name)
    
    def assess_health(self) -> HealthScore:
        """评估健康状况"""
        scores = {
            "energy": 0.0,
            "detox": 0.0,
            "wisdom": 0.0,
            "vitality": 0.0,
            "harmony": 0.0
        }
        
        for name, subsystem in self._subsystems.items():
            if name == "metabolism":
                metrics = subsystem.get_status().get("metrics", {})
                scores["energy"] = metrics.get("energy_efficiency", 0.5) * 100
            elif name == "liver_detox":
                health = subsystem.get_full_status().get("health_score", 50)
                scores["detox"] = health
            elif name == "seven_aperture_heart":
                status = subsystem.get_status()
                wisdom = status.get("wisdom_level", "凡俗")
                wisdom_map = {"凡俗": 40, "洞察": 60, "明智": 80, "超凡": 95, "神圣": 100}
                scores["wisdom"] = wisdom_map.get(wisdom, 50)
            elif name == "jing_qi_shen":
                jqs = subsystem.current_level.to_dict()
                scores["vitality"] = jqs.get("overall_vitality", 0.5) * 100
        
        imbalances = self.homeostasis.check_balance({k: v.get_status() for k, v in self._subsystems.items()})
        scores["harmony"] = max(0, 100 - sum(imbalances.values()) * 100)
        
        self._health_score = HealthScore(
            overall=sum(scores.values()) / len(scores),
            energy=scores["energy"],
            detox=scores["detox"],
            wisdom=scores["wisdom"],
            vitality=scores["vitality"],
            harmony=scores["harmony"]
        )
        
        self._update_body_state()
        self._last_full_assessment = datetime.now()
        
        return self._health_score
    
    def _update_body_state(self) -> None:
        """更新身体状态"""
        overall = self._health_score.overall
        
        if overall >= 90:
            self.state = BodyState.OPTIMAL
        elif overall >= 70:
            self.state = BodyState.ACTIVE
        elif overall >= 50:
            self.state = BodyState.RESTING
        elif overall >= 30:
            self.state = BodyState.STRESSED
        else:
            self.state = BodyState.RECOVERING
    
    def optimize(self) -> Dict[str, Any]:
        """执行优化"""
        if not self._optimization_enabled:
            return {"enabled": False}
        
        current_state = {k: v.get_status() for k, v in self._subsystems.items()}
        
        is_emergency, emergency_type = self.emergency.assess_emergency(current_state)
        
        if is_emergency:
            response = self.emergency.trigger_emergency_response(emergency_type)
            return {
                "emergency_mode": True,
                "emergency_type": emergency_type,
                "response": response
            }
        
        actions = self.optimizer.analyze_state(current_state)
        executed = []
        
        for action in actions[:3]:
            result = self._execute_optimization_action(action)
            if result:
                executed.append(result)
                self.optimizer.record_action(action)
        
        self._perform_auto_detox()
        self._perform_auto_balance()
        
        self._tick_count += 1
        
        return {
            "emergency_mode": False,
            "optimizations_executed": executed,
            "current_state": self.state.value,
            "health_score": self._health_score.to_dict()
        }
    
    def _execute_optimization_action(self, action: OptimizationAction) -> Optional[Dict[str, Any]]:
        """执行优化动作"""
        subsystem = self._subsystems.get(action.target_system)
        if not subsystem:
            return None
        
        result = {"action": action.action_type, "target": action.target_system}
        
        if action.target_system == "metabolism" and hasattr(subsystem, "optimize_metabolism"):
            opt_result = subsystem.optimize_metabolism()
            result["details"] = opt_result
        
        elif action.target_system == "liver_detox" and hasattr(subsystem, "start_detox_cycle"):
            cycle = subsystem.start_detox_cycle()
            result["details"] = {"cycle_started": True}
        
        elif action.target_system == "seven_aperture_heart" and hasattr(subsystem, "meditate"):
            meditation = subsystem.meditate(0.5)
            result["details"] = meditation
        
        return result
    
    def _perform_auto_detox(self) -> None:
        """自动排毒"""
        if not self._auto_detox_enabled:
            return
        
        liver_detox = self._subsystems.get("liver_detox")
        metabolism = self._subsystems.get("metabolism")
        
        if not liver_detox or not metabolism:
            return
        
        metabolism_toxin = metabolism.get_detox_needs()
        if isinstance(metabolism_toxin, float):
            metabolism_toxin = {"stored_toxins": metabolism_toxin}
        
        liver_needs = liver_detox.get_detox_needs()
        
        total_toxin_load = metabolism_toxin.get("stored_toxins", 0) + liver_needs.get("stored_toxins", 0)
        
        if total_toxin_load > 20:
            liver_detox.start_detox_cycle()
            liver_detox.perform_detox(1.0)
    
    def _perform_auto_balance(self) -> None:
        """自动平衡"""
        if not self._auto_balance_enabled:
            return
        
        current_state = {k: v.get_status() for k, v in self._subsystems.items()}
        imbalances = self.homeostasis.check_balance(current_state)
        
        for imbalance_type, deviation in imbalances.items():
            if deviation > 0.15:
                correction = self.homeostasis.correct_balance(imbalance_type, deviation)
                if correction.get("action"):
                    pass
    
    def tick(self, delta_time: float = 1.0) -> Dict[str, Any]:
        """系统Tick"""
        if self.state == BodyState.DORMANT:
            return {"status": "dormant"}
        
        for subsystem in self._subsystems.values():
            if hasattr(subsystem, "tick"):
                subsystem.tick(delta_time)
        
        return self.optimize()
    
    def get_full_status(self) -> Dict[str, Any]:
        """获取完整状态"""
        health = self.assess_health()
        
        subsystems_status = {}
        for name, subsystem in self._subsystems.items():
            if hasattr(subsystem, "get_status"):
                subsystems_status[name] = subsystem.get_status()
        
        return {
            "state": self.state.value,
            "health_score": health.to_dict(),
            "subsystems": subsystems_status,
            "emergency_mode": self.emergency.emergency_mode,
            "stress_level": self.emergency.stress_level,
            "optimization_enabled": self._optimization_enabled,
            "auto_detox_enabled": self._auto_detox_enabled,
            "tick_count": self._tick_count
        }
    
    def enable_optimization(self, enabled: bool = True) -> None:
        """启用/禁用优化"""
        self._optimization_enabled = enabled
    
    def enable_auto_detox(self, enabled: bool = True) -> None:
        """启用/禁用自动排毒"""
        self._auto_detox_enabled = enabled
    
    def enable_auto_balance(self, enabled: bool = True) -> None:
        """启用/禁用自动平衡"""
        self._auto_balance_enabled = enabled


def create_body_master_system() -> BodyMasterSystem:
    """创建身体综合管理系统"""
    return BodyMasterSystem()
