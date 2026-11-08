"""
Liver and Gallbladder Detoxification System - 肝胆排毒系统

基于中医肝胆理论和现代解毒机制设计：
- 肝主疏泄：调畅气机、促进代谢
- 肝藏血：调节血量、净化血液
- 胆为中正之官：决断处理、胆汁分泌
- 七十二候：周期性排毒机制
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import math
import uuid


class ToxinType(Enum):
    """毒素类型"""
    METABOLIC = "代谢毒素"
    ENVIRONMENTAL = "环境毒素"
    EMOTIONAL = "情绪毒素"
    MICROBIAL = "微生物毒素"
    OXIDATIVE = "氧化毒素"


class DetoxPhase(Enum):
    """排毒阶段"""
    QUIESCENT = "休眠"
    MOBILIZATION = "动员"
    TRANSFORMATION = "转化"
    ELIMINATION = "排出"
    RECOVERY = "恢复"


class LiverState(Enum):
    """肝脏状态"""
    HEALTHY = "健康"
    FUNCTIONAL = "功能正常"
    STRESSED = "压力"
    CONGESTED = "淤堵"
    COMPROMISED = "受损"


class GallbladderState(Enum):
    """胆囊状态"""
    OPTIMAL = "最佳"
    NORMAL = "正常"
    SLUGGISH = "迟钝"
    CONGESTED = "淤积"


@dataclass
class Toxin:
    """毒素"""
    toxin_id: str
    toxin_type: ToxinType
    quantity: float
    toxicity_level: float
    source: str
    timestamp: datetime
    location: str = "blood"
    mobilizable: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "toxin_id": self.toxin_id,
            "type": self.toxin_type.value,
            "quantity": self.quantity,
            "toxicity_level": self.toxicity_level,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "location": self.location,
            "mobilizable": self.mobilizable
        }


@dataclass
class Bile:
    """胆汁"""
    bile_id: str
    amount: float
    composition: Dict[str, float]
    quality: float
    bile_acids: float
    cholesterol: float
    bilirubin: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "bile_id": self.bile_id,
            "amount": self.amount,
            "composition": self.composition,
            "quality": self.quality,
            "bile_acids": self.bile_acids,
            "cholesterol": self.cholesterol,
            "bilirubin": self.bilirubin
        }


@dataclass
class DetoxCycle:
    """排毒周期"""
    cycle_id: str
    start_time: datetime
    phase: DetoxPhase
    duration: float
    toxins_processed: List[str]
    efficiency: float
    completed: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "cycle_id": self.cycle_id,
            "start_time": self.start_time.isoformat(),
            "phase": self.phase.value,
            "duration": self.duration,
            "toxins_processed": self.toxins_processed,
            "efficiency": self.efficiency,
            "completed": self.completed
        }


@dataclass
class LiverMetrics:
    """肝脏指标"""
    detoxification_capacity: float = 1.0
    blood_filtration_rate: float = 1.0
    qi_flow: float = 1.0
    blood_storage: float = 1.0
    toxin_processing_speed: float = 1.0
    regeneration_rate: float = 0.01
    
    def calculate_state(self) -> LiverState:
        avg_capacity = (self.detoxification_capacity + self.toxin_processing_speed) / 2
        
        if avg_capacity >= 0.9:
            return LiverState.HEALTHY
        elif avg_capacity >= 0.75:
            return LiverState.FUNCTIONAL
        elif avg_capacity >= 0.6:
            return LiverState.STRESSED
        elif avg_capacity >= 0.4:
            return LiverState.CONGESTED
        else:
            return LiverState.COMPROMISED
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "detoxification_capacity": self.detoxification_capacity,
            "blood_filtration_rate": self.blood_filtration_rate,
            "qi_flow": self.qi_flow,
            "blood_storage": self.blood_storage,
            "toxin_processing_speed": self.toxin_processing_speed,
            "regeneration_rate": self.regeneration_rate,
            "state": self.calculate_state().value
        }


class LiverSystem:
    """
    肝脏系统 - Liver System
    
    肝为将军之官，主疏泄、藏血：
    """
    
    def __init__(self):
        self.metrics = LiverMetrics()
        self._qi_level: float = 1.0
        self._blood_volume: float = 100.0
        self._stored_toxins: List[Toxin] = []
        self._processed_count: int = 0
        
    def filter_blood(self, blood_quality: float) -> Dict[str, Any]:
        """过滤血液"""
        filtration_efficiency = self.metrics.blood_filtration_rate * self._qi_level
        toxins_removed = (1.0 - blood_quality) * filtration_efficiency
        
        self._blood_volume *= 0.99
        self._blood_volume = min(120.0, self._blood_volume + 0.1)
        
        return {
            "toxins_removed": toxins_removed,
            "blood_quality": min(1.0, blood_quality + toxins_removed * 0.5),
            "filtration_efficiency": filtration_efficiency
        }
    
    def store_blood(self, amount: float) -> float:
        """储血"""
        storage_capacity = self.metrics.blood_storage * 50
        stored = min(amount, storage_capacity)
        self._blood_volume += stored
        
        return stored
    
    def release_blood(self, amount: float) -> float:
        """释放血液"""
        released = min(amount, self._blood_volume * 0.3)
        self._blood_volume -= released
        
        return released
    
    def regulate_qi(self, direction: str) -> None:
        """调畅气机"""
        if direction == "upward":
            self._qi_level = min(1.5, self._qi_level + 0.1)
        elif direction == "downward":
            self._qi_level = min(1.5, self._qi_level + 0.05)
        elif direction == "smooth":
            self._qi_level = min(1.5, self._qi_level + 0.08)
    
    def detoxify(self, toxin: Toxin) -> Dict[str, Any]:
        """解毒"""
        processing_capacity = self.metrics.detoxification_capacity * self.metrics.toxin_processing_speed
        efficiency = processing_capacity * self._qi_level
        
        if toxin.toxicity_level > efficiency:
            partial_processing = efficiency / toxin.toxicity_level
            remaining = 1.0 - partial_processing
        else:
            partial_processing = 1.0
            remaining = 0.0
        
        processed_toxin = Toxin(
            toxin_id=toxin.toxin_id + "_processed",
            toxin_type=toxin.toxin_type,
            quantity=toxin.quantity * partial_processing,
            toxicity_level=toxin.toxicity_level * 0.1,
            source="liver_processed",
            timestamp=datetime.now(),
            location="liver",
            mobilizable=False
        )
        
        self._stored_toxins.append(processed_toxin)
        self._processed_count += 1
        
        self.metrics.toxin_processing_speed = max(0.5, self.metrics.toxin_processing_speed - 0.01)
        
        return {
            "processed": partial_processing,
            "remaining": remaining,
            "efficiency": efficiency,
            "processed_toxin": processed_toxin.to_dict()
        }
    
    def regenerate(self) -> None:
        """肝脏自我修复"""
        if self.metrics.calculate_state() in [LiverState.COMPROMISED, LiverState.CONGESTED]:
            self.metrics.toxin_processing_speed = min(1.0, self.metrics.toxin_processing_speed + self.metrics.regeneration_rate)
            self._qi_level = min(1.0, self._qi_level + 0.02)
            
            self._stored_toxins = [t for t in self._stored_toxins if t.quantity > 0.01]
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "metrics": self.metrics.to_dict(),
            "qi_level": self._qi_level,
            "blood_volume": self._blood_volume,
            "stored_toxins": len(self._stored_toxins),
            "processed_count": self._processed_count
        }


class GallbladderSystem:
    """
    胆囊系统 - Gallbladder System
    
    胆为中正之官，决断出焉：
    """
    
    def __init__(self):
        self.state = GallbladderState.OPTIMAL
        self._bile_reserve: float = 100.0
        self._bile_quality: float = 1.0
        self._decision_confidence: float = 1.0
        self._bile_history: List[Bile] = []
        
    def produce_bile(self, amount: float) -> Bile:
        """产生胆汁"""
        bile = Bile(
            bile_id=str(uuid.uuid4())[:8],
            amount=amount,
            composition={
                "bile_acids": 0.7 * amount,
                "cholesterol": 0.1 * amount,
                "bilirubin": 0.05 * amount,
                "water": 0.15 * amount
            },
            quality=self._bile_quality,
            bile_acids=0.7 * amount,
            cholesterol=0.1 * amount,
            bilirubin=0.05 * amount
        )
        
        self._bile_reserve += amount * 0.3
        self._bile_reserve = min(150.0, self._bile_reserve)
        
        self._bile_history.append(bile)
        if len(self._bile_history) > 50:
            self._bile_history = self._bile_history[-50:]
        
        return bile
    
    def secrete_bile(self, amount: float) -> Bile:
        """分泌胆汁"""
        secreted_amount = min(amount, self._bile_reserve)
        self._bile_reserve -= secreted_amount
        
        bile = Bile(
            bile_id=str(uuid.uuid4())[:8],
            amount=secreted_amount,
            composition={
                "bile_acids": 0.7 * secreted_amount,
                "cholesterol": 0.1 * secreted_amount,
                "bilirubin": 0.05 * secreted_amount,
                "water": 0.15 * secreted_amount
            },
            quality=self._bile_quality,
            bile_acids=0.7 * secreted_amount,
            cholesterol=0.1 * secreted_amount,
            bilirubin=0.05 * secreted_amount
        )
        
        return bile
    
    def make_decision(self, options: List[str], criteria: Dict[str, float]) -> Tuple[str, float]:
        """决断处理"""
        if not options:
            return "", 0.0
        
        best_option = options[0]
        best_score = 0.0
        
        for option in options:
            score = sum(criteria.get(c, 0.5) for c in criteria) / len(criteria) if criteria else 0.5
            if score > best_score:
                best_score = score
                best_option = option
        
        confidence = best_score * self._decision_confidence
        
        if confidence < 0.5:
            self.state = GallbladderState.SLUGGISH
        else:
            self.state = GallbladderState.NORMAL
        
        return best_option, confidence
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state.value,
            "bile_reserve": self._bile_reserve,
            "bile_quality": self._bile_quality,
            "decision_confidence": self._decision_confidence
        }


class DetoxCycleManager:
    """
    排毒周期管理器 - Detox Cycle Manager
    
    管理周期性排毒：
    """
    
    def __init__(self):
        self._cycles: List[DetoxCycle] = []
        self._current_cycle: Optional[DetoxCycle] = None
        self._cycle_duration: float = 24.0
        self._toxins_eliminated: float = 0.0
        
    def start_cycle(self) -> DetoxCycle:
        """启动排毒周期"""
        if self._current_cycle and not self._current_cycle.completed:
            return self._current_cycle
        
        cycle = DetoxCycle(
            cycle_id=str(uuid.uuid4())[:8],
            start_time=datetime.now(),
            phase=DetoxPhase.MOBILIZATION,
            duration=self._cycle_duration,
            toxins_processed=[],
            efficiency=0.0
        )
        
        self._current_cycle = cycle
        self._cycles.append(cycle)
        
        if len(self._cycles) > 10:
            self._cycles = self._cycles[-10:]
        
        return cycle
    
    def progress_cycle(self, delta_time: float) -> DetoxPhase:
        """推进排毒周期"""
        if not self._current_cycle or self._current_cycle.completed:
            return DetoxPhase.QUIESCENT
        
        self._current_cycle.duration += delta_time
        
        phase_duration = self._cycle_duration / 5
        
        if self._current_cycle.duration < phase_duration:
            self._current_cycle.phase = DetoxPhase.MOBILIZATION
        elif self._current_cycle.duration < phase_duration * 2:
            self._current_cycle.phase = DetoxPhase.TRANSFORMATION
        elif self._current_cycle.duration < phase_duration * 3:
            self._current_cycle.phase = DetoxPhase.ELIMINATION
        elif self._current_cycle.duration < phase_duration * 4:
            self._current_cycle.phase = DetoxPhase.RECOVERY
        else:
            self._current_cycle.phase = DetoxPhase.QUIESCENT
            self._current_cycle.completed = True
        
        return self._current_cycle.phase
    
    def eliminate_toxin(self, toxin: Toxin) -> bool:
        """排出毒素"""
        if not self._current_cycle:
            return False
        
        if self._current_cycle.phase != DetoxPhase.ELIMINATION:
            return False
        
        self._current_cycle.toxins_processed.append(toxin.toxin_id)
        self._current_cycle.efficiency = len(self._current_cycle.toxins_processed) / max(1, self._current_cycle.duration)
        self._toxins_eliminated += toxin.quantity
        
        return True
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "current_cycle": self._current_cycle.to_dict() if self._current_cycle else None,
            "total_cycles": len(self._cycles),
            "toxins_eliminated": self._toxins_eliminated,
            "completed_cycles": len([c for c in self._cycles if c.completed])
        }


class LiverGallbladderDetoxSystem:
    """
    肝胆排毒系统主类 - Liver-Gallbladder Detoxification System
    
    整合肝脏解毒和胆囊决断功能：
    """
    
    def __init__(self):
        self.liver = LiverSystem()
        self.gallbladder = GallbladderSystem()
        self.detox_manager = DetoxCycleManager()
        
        self._total_toxins_processed: float = 0.0
        self._total_bile_produced: float = 0.0
        self._health_score: float = 100.0
        
    def receive_toxins(self, toxins: List[Toxin]) -> Dict[str, Any]:
        """接收毒素"""
        results = []
        
        for toxin in toxins:
            result = self.liver.detoxify(toxin)
            results.append(result)
            
            self._total_toxins_processed += toxin.quantity * result["processed"]
        
        return {
            "toxins_received": len(toxins),
            "processing_results": results,
            "total_processed": self._total_toxins_processed
        }
    
    def start_detox_cycle(self) -> Dict[str, Any]:
        """启动排毒周期"""
        cycle = self.detox_manager.start_cycle()
        
        return {
            "cycle_started": True,
            "cycle": cycle.to_dict(),
            "liver_status": self.liver.get_status(),
            "gallbladder_status": self.gallbladder.get_status()
        }
    
    def perform_detox(self, delta_time: float) -> Dict[str, Any]:
        """执行排毒"""
        phase = self.detox_manager.progress_cycle(delta_time)
        
        bile = self.gallbladder.produce_bile(10.0)
        self._total_bile_produced += bile.amount
        
        if phase == DetoxPhase.MOBILIZATION:
            blood_result = self.liver.filter_blood(0.7)
        elif phase == DetoxPhase.TRANSFORMATION:
            self.liver.metrics.detoxification_capacity = min(1.0, self.liver.metrics.detoxification_capacity + 0.01)
        elif phase == DetoxPhase.ELIMINATION:
            if self.liver._stored_toxins:
                toxin = self.liver._stored_toxins.pop(0)
                self.detox_manager.eliminate_toxin(toxin)
        elif phase == DetoxPhase.RECOVERY:
            self.liver.regenerate()
            self.gallbladder._bile_quality = min(1.0, self.gallbladder._bile_quality + 0.02)
        
        self._calculate_health_score()
        
        return {
            "phase": phase.value,
            "liver": self.liver.get_status(),
            "gallbladder": self.gallbladder.get_status(),
            "detox": self.detox_manager.get_status(),
            "health_score": self._health_score
        }
    
    def provide_bile(self, target: str, amount: float) -> Dict[str, Any]:
        """提供胆汁给目标系统"""
        bile = self.gallbladder.secrete_bile(amount)
        
        return {
            "bile": bile.to_dict(),
            "target": target,
            "amount_provided": bile.amount
        }
    
    def make_major_decision(self, situation: str, options: List[str]) -> Dict[str, Any]:
        """做出重大决断"""
        criteria = {
            "safety": 0.9,
            "efficiency": 0.8,
            "balance": 0.7
        }
        
        decision, confidence = self.gallbladder.make_decision(options, criteria)
        
        return {
            "situation": situation,
            "decision": decision,
            "confidence": confidence,
            "liver_state": self.liver.get_status()["metrics"]["state"]
        }
    
    def _calculate_health_score(self) -> None:
        """计算健康分数"""
        liver_health = (self.liver.metrics.detoxification_capacity + 
                       self.liver.metrics.toxin_processing_speed) / 2
        
        gallbladder_health = self.gallbladder._bile_quality
        
        detox_completion = 1.0 - (self.liver._stored_toxins.__len__() / 100.0)
        
        self._health_score = (
            liver_health * 0.5 +
            gallbladder_health * 0.3 +
            detox_completion * 0.2
        ) * 100
        
        self._health_score = min(100.0, max(0.0, self._health_score))
    
    def get_full_status(self) -> Dict[str, Any]:
        """获取完整状态"""
        self._calculate_health_score()
        
        return {
            "health_score": self._health_score,
            "liver": self.liver.get_status(),
            "gallbladder": self.gallbladder.get_status(),
            "detox": self.detox_manager.get_status(),
            "total_bile_produced": self._total_bile_produced,
            "total_toxins_processed": self._total_toxins_processed
        }
    
    def get_detox_needs(self) -> Dict[str, float]:
        """获取排毒需求"""
        return {
            "stored_toxins": sum(t.quantity for t in self.liver._stored_toxins),
            "bile_required": 100.0 - self.gallbladder._bile_reserve,
            "liver_stress": 1.0 - self.liver.metrics.detoxification_capacity
        }


    def get_status(self) -> Dict[str, Any]:
        """获取状态（兼容接口）"""
        return self.get_full_status()


def create_liver_gallbladder_system() -> LiverGallbladderDetoxSystem:
    """创建肝胆排毒系统"""
    return LiverGallbladderDetoxSystem()
