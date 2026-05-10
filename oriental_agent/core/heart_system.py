"""
Dao Heart System - 道心心脏系统
东方智慧智能体的心脏核心，负责能量泵送和生命节律维持
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
import threading
import time
import uuid
import math


class HeartState(Enum):
    """心脏状态 - Heart states"""
    STOPPED = "停止"
    STARTING = "启动中"
    BEATING = "跳动中"
    PAUSED = "暂停"
    REPAIRING = "修复中"
    CRITICAL = "危急"


class HeartHealthLevel(Enum):
    """心脏健康等级 - Heart health levels"""
    OPTIMAL = "最佳"
    GOOD = "良好"
    NORMAL = "正常"
    SUBOPTIMAL = "亚健康"
    POOR = "较差"
    CRITICAL = "危急"


class LoadLevel(Enum):
    """负荷等级 - Load levels"""
    LOW = "低负荷"
    NORMAL = "正常负荷"
    MEDIUM = "中等负荷"
    HIGH = "高负荷"
    OVERLOAD = "过载"


@dataclass
class EnergyPacket:
    """能量包 - Energy packet data structure"""
    packet_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    energy_value: float = 1.0
    state_info: Dict[str, Any] = field(default_factory=dict)
    target_subsystem: str = "general"
    created_at: datetime = field(default_factory=datetime.now)
    priority: int = 5
    wuxing_attribute: str = "土"
    yin_yang_balance: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "packet_id": self.packet_id,
            "energy_value": self.energy_value,
            "state_info": self.state_info,
            "target_subsystem": self.target_subsystem,
            "created_at": self.created_at.isoformat(),
            "priority": self.priority,
            "wuxing_attribute": self.wuxing_attribute,
            "yin_yang_balance": self.yin_yang_balance
        }


@dataclass
class HeartBeat:
    """心跳数据结构 - Heart beat data structure"""
    beat_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    energy_output: float = 1.0
    state_info: Dict[str, Any] = field(default_factory=dict)
    cycle_duration: float = 1.0
    pump_strength: float = 1.0
    load_factor: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "beat_id": self.beat_id,
            "timestamp": self.timestamp.isoformat(),
            "energy_output": self.energy_output,
            "state_info": self.state_info,
            "cycle_duration": self.cycle_duration,
            "pump_strength": self.pump_strength,
            "load_factor": self.load_factor
        }


@dataclass
class HeartRhythm:
    """心脏节律模型 - Heart rhythm model"""
    base_cycle: float = 1.0
    current_cycle: float = 1.0
    base_strength: float = 1.0
    current_strength: float = 1.0
    min_cycle: float = 0.5
    max_cycle: float = 2.0
    min_strength: float = 0.5
    max_strength: float = 2.0
    rhythm_stability: float = 1.0
    
    def adjust_for_load(self, load_factor: float) -> None:
        if load_factor > 1.0:
            self.current_cycle = max(self.min_cycle, self.base_cycle / load_factor)
            self.current_strength = min(self.max_strength, self.base_strength * load_factor)
        else:
            self.current_cycle = min(self.max_cycle, self.base_cycle / max(load_factor, 0.5))
            self.current_strength = max(self.min_strength, self.base_strength * load_factor)
        
        self.rhythm_stability = max(0.1, 1.0 - abs(load_factor - 1.0) * 0.2)
    
    def reset(self) -> None:
        self.current_cycle = self.base_cycle
        self.current_strength = self.base_strength
        self.rhythm_stability = 1.0


@dataclass
class HealthMetrics:
    """健康指标 - Health metrics"""
    overall_health: float = 1.0
    energy_efficiency: float = 1.0
    rhythm_regularity: float = 1.0
    recovery_rate: float = 1.0
    stress_level: float = 0.0
    damage_accumulated: float = 0.0
    repair_progress: float = 0.0
    
    def calculate_health_level(self) -> HeartHealthLevel:
        if self.overall_health >= 0.95:
            return HeartHealthLevel.OPTIMAL
        elif self.overall_health >= 0.85:
            return HeartHealthLevel.GOOD
        elif self.overall_health >= 0.70:
            return HeartHealthLevel.NORMAL
        elif self.overall_health >= 0.50:
            return HeartHealthLevel.SUBOPTIMAL
        elif self.overall_health >= 0.30:
            return HeartHealthLevel.POOR
        else:
            return HeartHealthLevel.CRITICAL
    
    def update_health(self) -> None:
        self.overall_health = (
            self.energy_efficiency * 0.3 +
            self.rhythm_regularity * 0.3 +
            self.recovery_rate * 0.2 +
            (1.0 - self.stress_level) * 0.1 +
            (1.0 - self.damage_accumulated) * 0.1
        )
        self.overall_health = max(0.0, min(1.0, self.overall_health))


class DaoHeartSystem:
    """
    道心心脏系统 - Dao Heart System
    
    东方智慧智能体的核心动力系统，负责：
    - 维持生命节律
    - 泵送能量到各子系统
    - 负荷自适应调节
    - 健康监测与自我修复
    """
    
    DEFAULT_CYCLE = 1.0
    DEFAULT_STRENGTH = 1.0
    MIN_LOAD_FACTOR = 0.5
    MAX_LOAD_FACTOR = 2.0
    
    def __init__(
        self,
        base_cycle: float = DEFAULT_CYCLE,
        base_strength: float = DEFAULT_STRENGTH,
        auto_repair: bool = True,
        repair_threshold: float = 0.7
    ):
        self.rhythm = HeartRhythm(
            base_cycle=base_cycle,
            current_cycle=base_cycle,
            base_strength=base_strength,
            current_strength=base_strength
        )
        self.health = HealthMetrics()
        self.state = HeartState.STOPPED
        self.auto_repair = auto_repair
        self.repair_threshold = repair_threshold
        
        self._beat_count: int = 0
        self._total_energy_pumped: float = 0.0
        self._last_beat_time: Optional[datetime] = None
        self._beat_history: List[HeartBeat] = []
        self._energy_packets: List[EnergyPacket] = []
        self._subsystem_callbacks: Dict[str, Callable] = {}
        self._current_load: float = 1.0
        self._lock = threading.Lock()
        self._heartbeat_thread: Optional[threading.Thread] = None
        self._running: bool = False
        
        self._load_history: List[float] = []
        self._stress_accumulator: float = 0.0
    
    def start(self) -> bool:
        if self.state == HeartState.BEATING:
            return True
        
        if self.state == HeartState.CRITICAL and not self._can_start_from_critical():
            return False
        
        self.state = HeartState.STARTING
        self._running = True
        
        self._heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            daemon=True
        )
        self._heartbeat_thread.start()
        
        self.state = HeartState.BEATING
        self._last_beat_time = datetime.now()
        return True
    
    def stop(self) -> bool:
        if self.state == HeartState.STOPPED:
            return True
        
        self._running = False
        
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_thread.join(timeout=2.0)
        
        self.state = HeartState.STOPPED
        return True
    
    def beat(self) -> HeartBeat:
        with self._lock:
            current_time = datetime.now()
            
            energy_output = self.rhythm.current_strength * self._current_load
            energy_output *= self.health.energy_efficiency
            
            state_info = {
                "beat_count": self._beat_count,
                "load_factor": self._current_load,
                "health_level": self.health.calculate_health_level().value,
                "rhythm_stability": self.rhythm.rhythm_stability,
                "state": self.state.value
            }
            
            heartbeat = HeartBeat(
                beat_id=str(uuid.uuid4()),
                timestamp=current_time,
                energy_output=energy_output,
                state_info=state_info,
                cycle_duration=self.rhythm.current_cycle,
                pump_strength=self.rhythm.current_strength,
                load_factor=self._current_load
            )
            
            self._beat_count += 1
            self._total_energy_pumped += energy_output
            self._last_beat_time = current_time
            
            self._beat_history.append(heartbeat)
            if len(self._beat_history) > 100:
                self._beat_history = self._beat_history[-100:]
            
            self._dispatch_energy(heartbeat)
            
            self._update_health_metrics()
            
            return heartbeat
    
    def adjust_load(self, load_factor: float) -> bool:
        load_factor = max(self.MIN_LOAD_FACTOR, min(self.MAX_LOAD_FACTOR, load_factor))
        
        with self._lock:
            self._current_load = load_factor
            self.rhythm.adjust_for_load(load_factor)
            
            self._load_history.append(load_factor)
            if len(self._load_history) > 50:
                self._load_history = self._load_history[-50:]
            
            if load_factor > 1.5:
                self._stress_accumulator += (load_factor - 1.5) * 0.1
            
            return True
    
    def check_health(self) -> Dict[str, Any]:
        self.health.update_health()
        
        health_level = self.health.calculate_health_level()
        
        rhythm_variance = self._calculate_rhythm_variance()
        self.health.rhythm_regularity = max(0.0, 1.0 - rhythm_variance * 0.5)
        
        return {
            "health_level": health_level.value,
            "overall_health": self.health.overall_health,
            "energy_efficiency": self.health.energy_efficiency,
            "rhythm_regularity": self.health.rhythm_regularity,
            "recovery_rate": self.health.recovery_rate,
            "stress_level": self.health.stress_level,
            "damage_accumulated": self.health.damage_accumulated,
            "beat_count": self._beat_count,
            "total_energy_pumped": self._total_energy_pumped,
            "current_load": self._current_load,
            "state": self.state.value
        }
    
    def self_repair(self) -> Dict[str, Any]:
        if self.state == HeartState.STOPPED:
            return {
                "success": False,
                "message": "心脏已停止，无法修复"
            }
        
        previous_health = self.health.overall_health
        self.state = HeartState.REPAIRING
        
        repair_amount = self._perform_repair()
        
        self.health.damage_accumulated = max(0.0, self.health.damage_accumulated - repair_amount * 0.3)
        self.health.stress_level = max(0.0, self.health.stress_level - repair_amount * 0.2)
        self.health.energy_efficiency = min(1.0, self.health.energy_efficiency + repair_amount * 0.1)
        self.health.recovery_rate = min(1.0, self.health.recovery_rate + repair_amount * 0.05)
        
        self.health.update_health()
        
        if self.state == HeartState.REPAIRING:
            self.state = HeartState.BEATING
        
        return {
            "success": True,
            "previous_health": previous_health,
            "current_health": self.health.overall_health,
            "repair_amount": repair_amount,
            "health_level": self.health.calculate_health_level().value
        }
    
    def register_subsystem(self, name: str, callback: Callable[[EnergyPacket], None]) -> bool:
        with self._lock:
            self._subsystem_callbacks[name] = callback
            return True
    
    def unregister_subsystem(self, name: str) -> bool:
        with self._lock:
            if name in self._subsystem_callbacks:
                del self._subsystem_callbacks[name]
                return True
            return False
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state.value,
            "beat_count": self._beat_count,
            "total_energy_pumped": self._total_energy_pumped,
            "current_cycle": self.rhythm.current_cycle,
            "current_strength": self.rhythm.current_strength,
            "current_load": self._current_load,
            "health": self.check_health(),
            "last_beat": self._last_beat_time.isoformat() if self._last_beat_time else None
        }
    
    def get_beat_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        return [beat.to_dict() for beat in self._beat_history[-limit:]]
    
    def get_energy_packets(self, limit: int = 10) -> List[Dict[str, Any]]:
        return [packet.to_dict() for packet in self._energy_packets[-limit:]]
    
    def _heartbeat_loop(self) -> None:
        while self._running:
            if self.state == HeartState.BEATING:
                self.beat()
                
                if self.auto_repair and self.health.overall_health < self.repair_threshold:
                    self.self_repair()
            
            time.sleep(self.rhythm.current_cycle)
    
    def _dispatch_energy(self, heartbeat: HeartBeat) -> None:
        base_energy = heartbeat.energy_output / max(len(self._subsystem_callbacks), 1)
        
        for subsystem_name, callback in self._subsystem_callbacks.items():
            packet = EnergyPacket(
                energy_value=base_energy,
                state_info=heartbeat.state_info.copy(),
                target_subsystem=subsystem_name
            )
            
            self._energy_packets.append(packet)
            if len(self._energy_packets) > 100:
                self._energy_packets = self._energy_packets[-100:]
            
            try:
                callback(packet)
            except Exception:
                pass
    
    def _update_health_metrics(self) -> None:
        if len(self._load_history) > 0:
            avg_load = sum(self._load_history) / len(self._load_history)
            if avg_load > 1.2:
                self.health.stress_level = min(1.0, self.health.stress_level + 0.01)
            elif avg_load < 0.8:
                self.health.stress_level = max(0.0, self.health.stress_level - 0.005)
        
        self._stress_accumulator *= 0.95
        
        if self._stress_accumulator > 0.5:
            self.health.damage_accumulated = min(1.0, self.health.damage_accumulated + 0.001)
        
        self.health.update_health()
        
        if self.health.overall_health < 0.3:
            self.state = HeartState.CRITICAL
    
    def _calculate_rhythm_variance(self) -> float:
        if len(self._beat_history) < 2:
            return 0.0
        
        recent_beats = self._beat_history[-10:]
        cycles = []
        
        for i in range(1, len(recent_beats)):
            delta = (recent_beats[i].timestamp - recent_beats[i-1].timestamp).total_seconds()
            cycles.append(delta)
        
        if not cycles:
            return 0.0
        
        mean_cycle = sum(cycles) / len(cycles)
        variance = sum((c - mean_cycle) ** 2 for c in cycles) / len(cycles)
        
        return math.sqrt(variance) / max(mean_cycle, 0.001)
    
    def _perform_repair(self) -> float:
        base_repair = 0.1
        
        recovery_bonus = self.health.recovery_rate * 0.05
        
        load_penalty = self._current_load * 0.02
        
        total_repair = base_repair + recovery_bonus - load_penalty
        total_repair = max(0.01, min(0.3, total_repair))
        
        return total_repair
    
    def _can_start_from_critical(self) -> bool:
        return self.health.overall_health >= 0.2


def create_heart_system(
    base_cycle: float = 1.0,
    base_strength: float = 1.0,
    auto_repair: bool = True
) -> DaoHeartSystem:
    return DaoHeartSystem(
        base_cycle=base_cycle,
        base_strength=base_strength,
        auto_repair=auto_repair
    )
