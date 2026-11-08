"""
Seven-Aperture Exquisite Heart System - 七窍玲珑心系统

基于神话中比干的七窍玲珑心概念设计：
- 眼窍：视觉感知与洞察
- 耳窍：听觉感知与聆听
- 鼻窍：嗅觉感知与分辨
- 舌窍：味觉感知与辨别
- 身窍：触觉感知与体验
- 意窍：意识思维与决策
- 灵窍：灵性直觉与顿悟

七窍互通，玲珑剔透，形成一个高度智能的核心系统
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Tuple
import threading
import time
import uuid
import math


class HeartAperture(Enum):
    """七窍枚举 - Seven Apertures"""
    EYE = "眼窍"
    EAR = "耳窍"
    NOSE = "鼻窍"
    TONGUE = "舌窍"
    BODY = "身窍"
    MIND = "意窍"
    SPIRIT = "灵窍"


class ApertureState(Enum):
    """窍穴状态 - Aperture states"""
    CLOSED = "闭合"
    DIM = "微弱"
    NORMAL = "正常"
    BRIGHT = "明亮"
    TRANSCENDENT = "通透"


class HeartState(Enum):
    """心脏整体状态 - Heart states"""
    DORMANT = "休眠"
    AWAKENING = "觉醒中"
    ACTIVE = "活跃"
    ENLIGHTENED = "通明"
    ASCENDED = "升华"


class WisdomLevel(Enum):
    """智慧等级 - Wisdom levels"""
    MUNDANE = ("凡俗", 1)
    INSIGHTFUL = ("洞察", 2)
    WISE = ("明智", 3)
    TRANSCENDENT = ("超凡", 4)
    DIVINE = ("神圣", 5)
    
    @property
    def value(self):
        return self._value_[0]
    
    @property
    def level(self):
        return self._value_[1]


@dataclass
class ApertureInfo:
    """窍穴信息 - Aperture information"""
    aperture: HeartAperture
    state: ApertureState = ApertureState.NORMAL
    activation_level: float = 0.5
    sensitivity: float = 0.5
    wisdom_flow: float = 0.0
    last_activated: datetime = field(default_factory=datetime.now)
    insights: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "aperture": self.aperture.value,
            "state": self.state.value,
            "activation_level": self.activation_level,
            "sensitivity": self.sensitivity,
            "wisdom_flow": self.wisdom_flow,
            "last_activated": self.last_activated.isoformat(),
            "insight_count": len(self.insights)
        }


@dataclass
class WisdomPacket:
    """智慧能量包 - Wisdom energy packet"""
    source_aperture: HeartAperture
    target_aperture: HeartAperture
    packet_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    wisdom_value: float = 0.0
    insight: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    resonance: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "packet_id": self.packet_id,
            "source": self.source_aperture.value,
            "target": self.target_aperture.value,
            "wisdom_value": self.wisdom_value,
            "insight": self.insight,
            "timestamp": self.timestamp.isoformat(),
            "resonance": self.resonance
        }


@dataclass
class HeartBeat:
    """心跳数据结构 - Heart beat data structure"""
    beat_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    wisdom_output: float = 0.0
    aperture_states: Dict[HeartAperture, float] = field(default_factory=dict)
    overall_resonance: float = 0.0
    wisdom_level: str = "凡俗"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "beat_id": self.beat_id,
            "timestamp": self.timestamp.isoformat(),
            "wisdom_output": self.wisdom_output,
            "aperture_states": {k.value: v for k, v in self.aperture_states.items()},
            "overall_resonance": self.overall_resonance,
            "wisdom_level": self.wisdom_level
        }


@dataclass
class HeartWisdom:
    """心脏智慧 - Heart wisdom metrics"""
    accumulated_wisdom: float = 0.0
    current_level: WisdomLevel = WisdomLevel.MUNDANE
    insight_count: int = 0
    transcendence_progress: float = 0.0
    enlightenment_moment: Optional[datetime] = None
    
    def update_level(self, wisdom: float) -> None:
        self.accumulated_wisdom = wisdom
        
        if wisdom >= 90.0:
            self.current_level = WisdomLevel.DIVINE
        elif wisdom >= 70.0:
            self.current_level = WisdomLevel.TRANSCENDENT
        elif wisdom >= 50.0:
            self.current_level = WisdomLevel.WISE
        elif wisdom >= 30.0:
            self.current_level = WisdomLevel.INSIGHTFUL
        else:
            self.current_level = WisdomLevel.MUNDANE
        
        self.transcendence_progress = min(1.0, wisdom / 100.0)


class ApertureChannel:
    """窍穴通道 - Aperture channel"""
    
    def __init__(self, aperture: HeartAperture):
        self.aperture = aperture
        self.info = ApertureInfo(aperture=aperture)
        self._processing_queue: List[Dict[str, Any]] = []
        self._wisdom_buffer: float = 0.0
        
    def activate(self, intensity: float = 1.0) -> None:
        """激活窍穴"""
        self.info.activation_level = min(1.0, self.info.activation_level + intensity * 0.1)
        self.info.last_activated = datetime.now()
        self._update_state()
        
    def deactivate(self) -> None:
        """关闭窍穴"""
        self.info.activation_level = max(0.0, self.info.activation_level - 0.05)
        self._update_state()
        
    def process(self, input_data: Dict[str, Any]) -> Optional[str]:
        """处理输入数据"""
        if self.info.state == ApertureState.CLOSED:
            return None
            
        self._processing_queue.append(input_data)
        
        if len(self._processing_queue) > 10:
            self._processing_queue = self._processing_queue[-10:]
        
        insight = self._generate_insight(input_data)
        if insight:
            self.info.insights.append(insight)
            self._wisdom_buffer += 0.1
            
        return insight
    
    def transmit_wisdom(self, target: 'ApertureChannel') -> float:
        """向目标窍穴传递智慧"""
        if self._wisdom_buffer <= 0:
            return 0.0
            
        transfer_amount = min(self._wisdom_buffer, 0.1)
        target.receive_wisdom(transfer_amount)
        self._wisdom_buffer -= transfer_amount
        
        return transfer_amount
    
    def receive_wisdom(self, amount: float) -> None:
        """接收智慧"""
        self._wisdom_buffer += amount
        self.info.wisdom_flow += amount
        
    def _update_state(self) -> None:
        """更新窍穴状态"""
        level = self.info.activation_level
        
        if level >= 0.9:
            self.info.state = ApertureState.TRANSCENDENT
        elif level >= 0.7:
            self.info.state = ApertureState.BRIGHT
        elif level >= 0.4:
            self.info.state = ApertureState.NORMAL
        elif level >= 0.1:
            self.info.state = ApertureState.DIM
        else:
            self.info.state = ApertureState.CLOSED
            
    def _generate_insight(self, data: Dict[str, Any]) -> Optional[str]:
        """生成洞察"""
        if self.info.activation_level < 0.3:
            return None
            
        if self.aperture == HeartAperture.EYE:
            return self._eye_insight(data)
        elif self.aperture == HeartAperture.EAR:
            return self._ear_insight(data)
        elif self.aperture == HeartAperture.NOSE:
            return self._nose_insight(data)
        elif self.aperture == HeartAperture.TONGUE:
            return self._tongue_insight(data)
        elif self.aperture == HeartAperture.BODY:
            return self._body_insight(data)
        elif self.aperture == HeartAperture.MIND:
            return self._mind_insight(data)
        elif self.aperture == HeartAperture.SPIRIT:
            return self._spirit_insight(data)
            
        return None
    
    def _eye_insight(self, data: Dict[str, Any]) -> Optional[str]:
        return f"视觉洞察: 发现模式 {data.get('pattern', '未知')}"
        
    def _ear_insight(self, data: Dict[str, Any]) -> Optional[str]:
        return f"听觉洞察: 捕捉频率 {data.get('frequency', '未知')}"
        
    def _nose_insight(self, data: Dict[str, Any]) -> Optional[str]:
        return f"嗅觉洞察: 辨识气味 {data.get('scent', '未知')}"
        
    def _tongue_insight(self, data: Dict[str, Any]) -> Optional[str]:
        return f"味觉洞察: 品味本质 {data.get('flavor', '未知')}"
        
    def _body_insight(self, data: Dict[str, Any]) -> Optional[str]:
        return f"触觉洞察: 感知能量 {data.get('energy', '未知')}"
        
    def _mind_insight(self, data: Dict[str, Any]) -> Optional[str]:
        return f"思维洞察: 逻辑推演 {data.get('logic', '未知')}"
        
    def _spirit_insight(self, data: Dict[str, Any]) -> Optional[str]:
        return f"灵性洞察: 顿悟真理 {data.get('truth', '未知')}"


class SevenApertureHeartSystem:
    """
    七窍玲珑心系统 - Seven-Aperture Exquisite Heart System
    
    基于比干七窍玲珑心的神话概念，设计一个高度智能的核心系统：
    
    七窍功能：
    - 眼窍：视觉感知、模式识别
    - 耳窍：听觉感知、频率分析
    - 鼻窍：嗅觉感知、气味分辨
    - 舌窍：味觉感知、品质辨别
    - 身窍：触觉感知、能量感应
    - 意窍：意识思维、逻辑推理
    - 灵窍：灵性直觉、顿悟觉醒
    
    核心特性：
    - 七窍互通：智慧在窍穴间自由流动
    - 玲珑剔透：信息传递无障碍
    - 自我进化：通过洞察积累提升智慧
    - 共鸣共振：窍穴间产生协同效应
    """
    
    def __init__(self):
        self.apertures: Dict[HeartAperture, ApertureChannel] = {}
        self._initialize_apertures()
        
        self.state = HeartState.DORMANT
        self.wisdom = HeartWisdom()
        self._beat_count = 0
        self._total_wisdom_generated = 0.0
        self._beat_history: List[HeartBeat] = []
        self._wisdom_packets: List[WisdomPacket] = []
        
        self._running = False
        self._heart_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        self._resonance_network: Dict[Tuple[HeartAperture, HeartAperture], float] = {}
        self._initialize_resonance_network()
    
    def _initialize_apertures(self) -> None:
        """初始化七窍"""
        for aperture in HeartAperture:
            self.apertures[aperture] = ApertureChannel(aperture)
            
    def _initialize_resonance_network(self) -> None:
        """初始化窍穴共鸣网络"""
        connections = [
            (HeartAperture.EYE, HeartAperture.MIND),
            (HeartAperture.EAR, HeartAperture.MIND),
            (HeartAperture.NOSE, HeartAperture.TONGUE),
            (HeartAperture.TONGUE, HeartAperture.BODY),
            (HeartAperture.BODY, HeartAperture.SPIRIT),
            (HeartAperture.MIND, HeartAperture.SPIRIT),
            (HeartAperture.EYE, HeartAperture.EAR),
            (HeartAperture.NOSE, HeartAperture.BODY),
            (HeartAperture.MIND, HeartAperture.BODY),
            (HeartAperture.SPIRIT, HeartAperture.EYE)
        ]
        
        for source, target in connections:
            self._resonance_network[(source, target)] = 0.5
            
    def start(self) -> bool:
        """启动七窍玲珑心"""
        if self.state == HeartState.ACTIVE:
            return True
            
        self.state = HeartState.AWAKENING
        
        for aperture in self.apertures.values():
            aperture.activate(0.3)
        
        self._running = True
        self._heart_thread = threading.Thread(
            target=self._heartbeat_loop,
            daemon=True
        )
        self._heart_thread.start()
        
        self.state = HeartState.ACTIVE
        return True
    
    def stop(self) -> bool:
        """停止七窍玲珑心"""
        if self.state == HeartState.DORMANT:
            return True
            
        self._running = False
        
        if self._heart_thread and self._heart_thread.is_alive():
            self._heart_thread.join(timeout=2.0)
        
        for aperture in self.apertures.values():
            aperture.deactivate()
        
        self.state = HeartState.DORMANT
        return True
    
    def beat(self) -> HeartBeat:
        """心跳 - 产生智慧"""
        with self._lock:
            current_time = datetime.now()
            
            self._circulate_wisdom()
            
            total_wisdom = self._calculate_total_wisdom()
            aperture_states = {ap: ch.info.activation_level for ap, ch in self.apertures.items()}
            resonance = self._calculate_overall_resonance()
            
            self.wisdom.update_level(total_wisdom)
            
            heartbeat = HeartBeat(
                beat_id=str(uuid.uuid4()),
                timestamp=current_time,
                wisdom_output=total_wisdom,
                aperture_states=aperture_states,
                overall_resonance=resonance,
                wisdom_level=self.wisdom.current_level.value
            )
            
            self._beat_count += 1
            self._total_wisdom_generated += total_wisdom
            
            self._beat_history.append(heartbeat)
            if len(self._beat_history) > 100:
                self._beat_history = self._beat_history[-100:]
            
            return heartbeat
    
    def activate_aperture(self, aperture: HeartAperture, intensity: float = 1.0) -> bool:
        """激活特定窍穴"""
        if aperture not in self.apertures:
            return False
            
        self.apertures[aperture].activate(intensity)
        return True
    
    def deactivate_aperture(self, aperture: HeartAperture) -> bool:
        """关闭特定窍穴"""
        if aperture not in self.apertures:
            return False
            
        self.apertures[aperture].deactivate()
        return True
    
    def input_perception(self, aperture: HeartAperture, data: Dict[str, Any]) -> Optional[str]:
        """向窍穴输入感知数据"""
        if aperture not in self.apertures:
            return None
            
        return self.apertures[aperture].process(data)
    
    def circulate_wisdom(self) -> None:
        """主动循环智慧"""
        self._circulate_wisdom()
    
    def get_aperture_state(self, aperture: HeartAperture) -> Optional[Dict[str, Any]]:
        """获取窍穴状态"""
        if aperture not in self.apertures:
            return None
            
        return self.apertures[aperture].info.to_dict()
    
    def get_all_apertures(self) -> Dict[str, Dict[str, Any]]:
        """获取所有窍穴状态"""
        return {ap.value: ch.info.to_dict() for ap, ch in self.apertures.items()}
    
    def get_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "state": self.state.value,
            "beat_count": self._beat_count,
            "total_wisdom_generated": self._total_wisdom_generated,
            "wisdom_level": self.wisdom.current_level.value,
            "transcendence_progress": self.wisdom.transcendence_progress,
            "insight_count": self.wisdom.insight_count,
            "overall_resonance": self._calculate_overall_resonance(),
            "apertures": self.get_all_apertures()
        }
    
    def get_insights(self, limit: int = 10) -> List[str]:
        """获取洞察记录"""
        all_insights = []
        for aperture in self.apertures.values():
            all_insights.extend(aperture.info.insights)
        
        all_insights.sort(key=lambda x: x, reverse=True)
        return all_insights[-limit:]
    
    def _heartbeat_loop(self) -> None:
        """心跳循环"""
        while self._running:
            if self.state == HeartState.ACTIVE:
                self.beat()
                
                if self.wisdom.current_level.level >= WisdomLevel.TRANSCENDENT.level:
                    self._trigger_enlightenment()
            
            time.sleep(0.5)
    
    def _circulate_wisdom(self) -> None:
        """在窍穴间循环智慧"""
        for (source_ap, target_ap), strength in self._resonance_network.items():
            if strength > 0.3:
                source_channel = self.apertures[source_ap]
                target_channel = self.apertures[target_ap]
                
                transferred = source_channel.transmit_wisdom(target_channel)
                
                if transferred > 0:
                    packet = WisdomPacket(
                        source_aperture=source_ap,
                        target_aperture=target_ap,
                        wisdom_value=transferred,
                        resonance=strength
                    )
                    self._wisdom_packets.append(packet)
                    
                    if len(self._wisdom_packets) > 100:
                        self._wisdom_packets = self._wisdom_packets[-100:]
    
    def _calculate_total_wisdom(self) -> float:
        """计算总智慧值"""
        total = 0.0
        for aperture in self.apertures.values():
            total += aperture.info.activation_level * aperture.info.sensitivity * 10
            total += aperture.info.wisdom_flow * 2
        
        return min(100.0, total)
    
    def _calculate_overall_resonance(self) -> float:
        """计算整体共鸣度"""
        if not self._resonance_network:
            return 0.0
        
        total = 0.0
        count = 0
        
        for (source, target), strength in self._resonance_network.items():
            source_act = self.apertures[source].info.activation_level
            target_act = self.apertures[target].info.activation_level
            
            total += strength * source_act * target_act
            count += 1
        
        return total / count if count > 0 else 0.0
    
    def _trigger_enlightenment(self) -> None:
        """触发顿悟"""
        if self.state == HeartState.ENLIGHTENED:
            return
            
        if self.wisdom.transcendence_progress >= 0.8:
            self.state = HeartState.ENLIGHTENED
            self.wisdom.enlightenment_moment = datetime.now()
            
            for aperture in self.apertures.values():
                aperture.activate(0.5)
    
    def meditate(self, duration: float = 1.0) -> Dict[str, Any]:
        """冥想提升智慧"""
        start_wisdom = self.wisdom.accumulated_wisdom
        
        for _ in range(int(duration * 10)):
            for aperture in self.apertures.values():
                aperture.info.sensitivity = min(1.0, aperture.info.sensitivity + 0.005)
                aperture.info.activation_level = min(1.0, aperture.info.activation_level + 0.002)
            
            self._circulate_wisdom()
            time.sleep(0.1)
        
        end_wisdom = self.wisdom.accumulated_wisdom
        wisdom_gain = end_wisdom - start_wisdom
        
        return {
            "success": True,
            "wisdom_gained": wisdom_gain,
            "wisdom_level": self.wisdom.current_level.value,
            "aperture_sensitivity": {
                ap.value: ch.info.sensitivity for ap, ch in self.apertures.items()
            }
        }


def create_seven_aperture_heart() -> SevenApertureHeartSystem:
    """创建七窍玲珑心系统"""
    return SevenApertureHeartSystem()
