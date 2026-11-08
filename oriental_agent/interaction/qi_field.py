"""
Qi Field Radiation System - 气场辐射系统

气场是系统对外辐射的能量场，反映系统当前状态并影响外部交互。
The Qi Field is an energy field radiated by the system, reflecting current state
and influencing external interactions.

Core Components:
- QiFieldState: 气场状态数据结构
- QiFieldEmitter: 气场发射器
- QiFieldVisualizer: 气场可视化器
- QiFieldInteraction: 气场交互处理器
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math


class QiFieldType(Enum):
    """气场类型枚举 - Qi Field Type Enumeration"""
    NEUTRAL = "中和"
    YANG_DOMINANT = "阳盛"
    YIN_DOMINANT = "阴盛"
    HARMONIOUS = "和谐"
    AGGRESSIVE = "刚猛"
    GENTLE = "柔和"
    WISDOM = "智慧"
    VITALITY = "生机"


class QiFieldColor(Enum):
    """气场颜色枚举 - Qi Field Color Enumeration"""
    WHITE = "白色"
    GOLD = "金色"
    PURPLE = "紫色"
    BLUE = "蓝色"
    GREEN = "绿色"
    RED = "红色"
    YELLOW = "黄色"
    BLACK = "黑色"
    CYAN = "青色"
    MIXED = "混色"


class ResonanceType(Enum):
    """共振类型枚举 - Resonance Type Enumeration"""
    HARMONIC = "和谐共振"
    DISCORDANT = "不和谐共振"
    NEUTRAL = "中性共振"
    AMPLIFYING = "增强共振"
    DAMPENING = "减弱共振"


class IntentionType(Enum):
    """意图类型枚举 - Intention Type Enumeration"""
    HEALING = "治愈"
    PROTECTION = "防护"
    GUIDANCE = "引导"
    COMMUNICATION = "沟通"
    INFLUENCE = "影响"
    DETECTION = "探测"


@dataclass
class QiFieldState:
    """
    气场状态数据结构 - Qi Field State Data Structure
    
    Attributes:
        intensity: 气场强度 (0-100)
        radius: 辐射半径
        frequency: 振动频率
        harmony: 和谐度 (0-1)
        color: 气场颜色表示
    """
    intensity: float = 50.0
    radius: float = 1.0
    frequency: float = 1.0
    harmony: float = 0.5
    color: QiFieldColor = QiFieldColor.WHITE
    field_type: QiFieldType = QiFieldType.NEUTRAL
    stability: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        self.intensity = max(0.0, min(100.0, self.intensity))
        self.radius = max(0.0, self.radius)
        self.frequency = max(0.0, self.frequency)
        self.harmony = max(0.0, min(1.0, self.harmony))
        self.stability = max(0.0, min(1.0, self.stability))
    
    @property
    def power(self) -> float:
        """计算气场总能量"""
        return self.intensity * self.radius * self.harmony
    
    @property
    def density(self) -> float:
        """计算气场密度"""
        if self.radius == 0:
            return 0.0
        return self.intensity / (self.radius ** 2)
    
    @property
    def wave_length(self) -> float:
        """计算波长"""
        if self.frequency == 0:
            return float('inf')
        return 1.0 / self.frequency
    
    def get_field_strength_at_distance(self, distance: float) -> float:
        """计算指定距离处的气场强度"""
        if distance <= 0:
            return self.intensity
        if distance > self.radius * 3:
            return 0.0
        
        decay_factor = 1.0 / (1.0 + distance ** 2)
        return self.intensity * decay_factor * self.harmony
    
    def to_dict(self) -> Dict:
        return {
            "intensity": self.intensity,
            "radius": self.radius,
            "frequency": self.frequency,
            "harmony": self.harmony,
            "color": self.color.value,
            "field_type": self.field_type.value,
            "stability": self.stability,
            "power": self.power,
            "density": self.density,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class QiFieldBoundary:
    """气场边界数据结构 - Qi Field Boundary Data Structure"""
    inner_radius: float = 0.5
    outer_radius: float = 1.5
    permeability: float = 0.5
    strength: float = 1.0
    active: bool = True
    
    def is_within_boundary(self, distance: float) -> bool:
        """判断是否在边界范围内"""
        return self.inner_radius <= distance <= self.outer_radius
    
    def get_boundary_strength(self, distance: float) -> float:
        """获取边界强度"""
        if not self.is_within_boundary(distance):
            return 0.0
        
        mid = (self.inner_radius + self.outer_radius) / 2
        distance_from_mid = abs(distance - mid)
        range_half = (self.outer_radius - self.inner_radius) / 2
        
        if range_half == 0:
            return self.strength
        
        return self.strength * (1.0 - distance_from_mid / range_half) * self.permeability
    
    def to_dict(self) -> Dict:
        return {
            "inner_radius": self.inner_radius,
            "outer_radius": self.outer_radius,
            "permeability": self.permeability,
            "strength": self.strength,
            "active": self.active
        }


@dataclass
class ResonanceResult:
    """共振结果数据结构 - Resonance Result Data Structure"""
    resonance_type: ResonanceType
    strength: float
    frequency_match: float
    harmony_change: float
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "resonance_type": self.resonance_type.value,
            "strength": self.strength,
            "frequency_match": self.frequency_match,
            "harmony_change": self.harmony_change,
            "message": self.message,
            "timestamp": self.timestamp.isoformat()
        }


class QiFieldEmitter:
    """
    气场发射器 - Qi Field Emitter
    
    负责发射、调节和管理气场辐射
    """
    
    INTENSITY_STEP = 5.0
    MAX_INTENSITY = 100.0
    MIN_INTENSITY = 0.0
    NATURAL_DECAY_RATE = 0.02
    RECOVERY_RATE = 0.01
    
    def __init__(self, initial_state: Optional[QiFieldState] = None):
        self.state = initial_state or QiFieldState()
        self.boundary: Optional[QiFieldBoundary] = None
        self.emission_history: List[Dict] = []
        self.is_emitting = False
        self._energy_reserve = 100.0
    
    def emit(self, intensity: Optional[float] = None) -> Dict:
        """
        发射气场 - Emit Qi Field
        
        Args:
            intensity: 可选的发射强度，不指定则使用当前状态强度
            
        Returns:
            发射结果字典
        """
        if intensity is not None:
            self.adjust_intensity(intensity)
        
        if self._energy_reserve < self.state.intensity * 0.1:
            return {
                "success": False,
                "message": "能量储备不足，无法发射气场",
                "current_energy": self._energy_reserve
            }
        
        self.is_emitting = True
        
        energy_cost = self.state.intensity * 0.05
        self._energy_reserve = max(0.0, self._energy_reserve - energy_cost)
        
        emission_result = {
            "success": True,
            "emitted_intensity": self.state.intensity,
            "radius": self.state.radius,
            "field_type": self.state.field_type.value,
            "energy_cost": energy_cost,
            "remaining_energy": self._energy_reserve,
            "timestamp": datetime.now().isoformat()
        }
        
        self._record_emission(emission_result)
        
        return emission_result
    
    def adjust_intensity(self, level: float) -> Dict:
        """
        调整气场强度 - Adjust Qi Field Intensity
        
        Args:
            level: 目标强度 (0-100)
            
        Returns:
            调整结果
        """
        old_intensity = self.state.intensity
        self.state.intensity = max(self.MIN_INTENSITY, 
                                   min(self.MAX_INTENSITY, level))
        
        intensity_change = self.state.intensity - old_intensity
        
        if intensity_change > 0:
            self.state.field_type = self._determine_field_type()
        
        return {
            "old_intensity": old_intensity,
            "new_intensity": self.state.intensity,
            "change": intensity_change,
            "field_type": self.state.field_type.value
        }
    
    def resonate_with(self, target_field: 'QiFieldState') -> ResonanceResult:
        """
        与目标气场共振 - Resonate with Target Field
        
        Args:
            target_field: 目标气场状态
            
        Returns:
            共振结果
        """
        frequency_diff = abs(self.state.frequency - target_field.frequency)
        frequency_match = 1.0 - min(1.0, frequency_diff / max(self.state.frequency, target_field.frequency, 0.1))
        
        harmony_avg = (self.state.harmony + target_field.harmony) / 2
        
        intensity_diff = abs(self.state.intensity - target_field.intensity)
        intensity_match = 1.0 - min(1.0, intensity_diff / 100.0)
        
        resonance_strength = (frequency_match * 0.4 + harmony_avg * 0.3 + intensity_match * 0.3)
        
        if resonance_strength > 0.8:
            resonance_type = ResonanceType.HARMONIC
            harmony_change = 0.1
            message = "气场和谐共振，能量增强"
        elif resonance_strength > 0.6:
            resonance_type = ResonanceType.AMPLIFYING
            harmony_change = 0.05
            message = "气场增强共振，相互促进"
        elif resonance_strength > 0.4:
            resonance_type = ResonanceType.NEUTRAL
            harmony_change = 0.0
            message = "气场中性共振，互不影响"
        elif resonance_strength > 0.2:
            resonance_type = ResonanceType.DAMPENING
            harmony_change = -0.05
            message = "气场减弱共振，能量消耗"
        else:
            resonance_type = ResonanceType.DISCORDANT
            harmony_change = -0.1
            message = "气场不和谐，产生冲突"
        
        self.state.harmony = max(0.0, min(1.0, self.state.harmony + harmony_change))
        
        result = ResonanceResult(
            resonance_type=resonance_type,
            strength=resonance_strength,
            frequency_match=frequency_match,
            harmony_change=harmony_change,
            message=message
        )
        
        return result
    
    def create_boundary(
        self, 
        inner_radius: float = 0.5, 
        outer_radius: float = 1.5,
        permeability: float = 0.5
    ) -> QiFieldBoundary:
        """
        创建气场边界 - Create Qi Field Boundary
        
        Args:
            inner_radius: 内半径
            outer_radius: 外半径
            permeability: 渗透性
            
        Returns:
            创建的气场边界
        """
        self.boundary = QiFieldBoundary(
            inner_radius=inner_radius,
            outer_radius=outer_radius,
            permeability=permeability,
            strength=self.state.intensity / 100.0
        )
        
        return self.boundary
    
    def remove_boundary(self) -> bool:
        """移除气场边界"""
        if self.boundary:
            self.boundary = None
            return True
        return False
    
    def update_from_jing_qi_shen(
        self, 
        jing_level: float, 
        qi_level: float, 
        shen_level: float
    ) -> Dict:
        """
        根据精气神水平更新气场状态
        
        Args:
            jing_level: 精水平 (0-1)
            qi_level: 气水平 (0-1)
            shen_level: 神水平 (0-1)
            
        Returns:
            更新结果
        """
        old_intensity = self.state.intensity
        
        new_intensity = (jing_level * 30 + qi_level * 40 + shen_level * 30)
        self.state.intensity = new_intensity
        
        self.state.radius = 0.5 + qi_level * 2.0
        
        self.state.frequency = 0.5 + shen_level * 2.0
        
        self.state.harmony = (jing_level + qi_level + shen_level) / 3.0
        
        self._energy_reserve = 50.0 + jing_level * 50.0
        
        self.state.field_type = self._determine_field_type()
        
        return {
            "intensity_change": self.state.intensity - old_intensity,
            "new_state": self.state.to_dict()
        }
    
    def update_from_yinyang_balance(self, yinyang_balance: float) -> Dict:
        """
        根据阴阳平衡更新气场和谐度
        
        Args:
            yinyang_balance: 阴阳平衡值 (-1 到 1)
            
        Returns:
            更新结果
        """
        old_harmony = self.state.harmony
        
        self.state.harmony = 1.0 - abs(yinyang_balance) * 0.5
        
        if yinyang_balance > 0.3:
            self.state.field_type = QiFieldType.YANG_DOMINANT
        elif yinyang_balance < -0.3:
            self.state.field_type = QiFieldType.YIN_DOMINANT
        else:
            self.state.field_type = QiFieldType.HARMONIOUS
        
        return {
            "harmony_change": self.state.harmony - old_harmony,
            "new_field_type": self.state.field_type.value
        }
    
    def update_from_wuxing(self, wuxing_element: str) -> Dict:
        """
        根据五行属性更新气场颜色
        
        Args:
            wuxing_element: 五行元素 ("木", "火", "土", "金", "水")
            
        Returns:
            更新结果
        """
        wuxing_color_map = {
            "木": QiFieldColor.GREEN,
            "火": QiFieldColor.RED,
            "土": QiFieldColor.YELLOW,
            "金": QiFieldColor.WHITE,
            "水": QiFieldColor.BLUE
        }
        
        wuxing_frequency_map = {
            "木": 1.2,
            "火": 1.8,
            "土": 1.0,
            "金": 1.5,
            "水": 0.8
        }
        
        old_color = self.state.color
        
        self.state.color = wuxing_color_map.get(wuxing_element, QiFieldColor.WHITE)
        self.state.frequency = wuxing_frequency_map.get(wuxing_element, 1.0)
        
        return {
            "old_color": old_color.value,
            "new_color": self.state.color.value,
            "new_frequency": self.state.frequency
        }
    
    def recover_energy(self, amount: float = 1.0) -> float:
        """恢复能量储备"""
        self._energy_reserve = min(100.0, self._energy_reserve + amount)
        return self._energy_reserve
    
    def get_state(self) -> QiFieldState:
        """获取当前气场状态"""
        return self.state
    
    def get_energy_reserve(self) -> float:
        """获取能量储备"""
        return self._energy_reserve
    
    def _determine_field_type(self) -> QiFieldType:
        """根据强度确定气场类型"""
        if self.state.intensity >= 80:
            return QiFieldType.AGGRESSIVE
        elif self.state.intensity >= 60:
            return QiFieldType.VITALITY
        elif self.state.intensity >= 40:
            return QiFieldType.HARMONIOUS
        elif self.state.intensity >= 20:
            return QiFieldType.GENTLE
        else:
            return QiFieldType.NEUTRAL
    
    def _record_emission(self, result: Dict) -> None:
        """记录发射历史"""
        self.emission_history.append(result)
        if len(self.emission_history) > 100:
            self.emission_history = self.emission_history[-100:]
    
    def reset(self) -> None:
        """重置发射器状态"""
        self.state = QiFieldState()
        self.boundary = None
        self.emission_history.clear()
        self.is_emitting = False
        self._energy_reserve = 100.0


class QiFieldVisualizer:
    """
    气场可视化器 - Qi Field Visualizer
    
    将气场状态转换为各种可视化表示
    """
    
    COLOR_RGB_MAP = {
        QiFieldColor.WHITE: (255, 255, 255),
        QiFieldColor.GOLD: (255, 215, 0),
        QiFieldColor.PURPLE: (128, 0, 128),
        QiFieldColor.BLUE: (0, 0, 255),
        QiFieldColor.GREEN: (0, 128, 0),
        QiFieldColor.RED: (255, 0, 0),
        QiFieldColor.YELLOW: (255, 255, 0),
        QiFieldColor.BLACK: (0, 0, 0),
        QiFieldColor.CYAN: (0, 255, 255),
        QiFieldColor.MIXED: (128, 128, 128)
    }
    
    SOUND_FREQUENCY_MAP = {
        QiFieldColor.WHITE: 528.0,
        QiFieldColor.GOLD: 432.0,
        QiFieldColor.PURPLE: 396.0,
        QiFieldColor.BLUE: 741.0,
        QiFieldColor.GREEN: 639.0,
        QiFieldColor.RED: 852.0,
        QiFieldColor.YELLOW: 417.0,
        QiFieldColor.BLACK: 174.0,
        QiFieldColor.CYAN: 963.0,
        QiFieldColor.MIXED: 528.0
    }
    
    FIELD_TYPE_DESCRIPTIONS = {
        QiFieldType.NEUTRAL: "平和稳定的中性气场",
        QiFieldType.YANG_DOMINANT: "阳刚充沛的活跃气场",
        QiFieldType.YIN_DOMINANT: "阴柔内敛的沉静气场",
        QiFieldType.HARMONIOUS: "阴阳调和的和谐气场",
        QiFieldType.AGGRESSIVE: "刚猛强劲的威压气场",
        QiFieldType.GENTLE: "柔和温润的治愈气场",
        QiFieldType.WISDOM: "深邃睿智的灵性气场",
        QiFieldType.VITALITY: "生机勃勃的活力气场"
    }
    
    def __init__(self):
        self.visualization_history: List[Dict] = []
    
    def visualize_state(self, state: QiFieldState) -> Dict:
        """
        可视化当前状态 - Visualize Current State
        
        Args:
            state: 气场状态
            
        Returns:
            可视化结果字典
        """
        visualization = {
            "color": self.to_color(state),
            "sound": self.to_sound(state),
            "text": self.to_text(state),
            "shape": self._get_shape_description(state),
            "movement": self._get_movement_description(state),
            "aura_layers": self._calculate_aura_layers(state)
        }
        
        self._record_visualization(visualization)
        
        return visualization
    
    def to_color(self, state: QiFieldState) -> Dict:
        """
        转换为颜色表示 - Convert to Color Representation
        
        Args:
            state: 气场状态
            
        Returns:
            颜色信息字典
        """
        base_rgb = self.COLOR_RGB_MAP.get(state.color, (255, 255, 255))
        
        intensity_factor = state.intensity / 100.0
        harmony_factor = state.harmony
        
        adjusted_rgb = tuple(
            int(min(255, c * (0.5 + 0.5 * intensity_factor) * (0.7 + 0.3 * harmony_factor)))
            for c in base_rgb
        )
        
        hex_color = '#{:02x}{:02x}{:02x}'.format(*adjusted_rgb)
        
        return {
            "name": state.color.value,
            "rgb": adjusted_rgb,
            "hex": hex_color,
            "brightness": intensity_factor,
            "saturation": harmony_factor
        }
    
    def to_sound(self, state: QiFieldState) -> Dict:
        """
        转换为声音表示 - Convert to Sound Representation
        
        Args:
            state: 气场状态
            
        Returns:
            声音信息字典
        """
        base_frequency = self.SOUND_FREQUENCY_MAP.get(state.color, 528.0)
        
        adjusted_frequency = base_frequency * state.frequency
        
        volume = state.intensity / 100.0
        
        timbre = self._determine_timbre(state)
        
        note = self._frequency_to_note(adjusted_frequency)
        
        return {
            "frequency_hz": round(adjusted_frequency, 2),
            "volume": round(volume, 2),
            "timbre": timbre,
            "musical_note": note,
            "duration_suggestion": self._get_duration_suggestion(state)
        }
    
    def to_text(self, state: QiFieldState) -> str:
        """
        转换为文本描述 - Convert to Text Description
        
        Args:
            state: 气场状态
            
        Returns:
            文本描述
        """
        field_desc = self.FIELD_TYPE_DESCRIPTIONS.get(
            state.field_type, "未知气场类型"
        )
        
        intensity_desc = self._get_intensity_description(state.intensity)
        harmony_desc = self._get_harmony_description(state.harmony)
        
        description = (
            f"【{state.field_type.value}气场】{field_desc}。"
            f"强度{state.intensity:.1f}，{intensity_desc}；"
            f"和谐度{state.harmony * 100:.1f}%，{harmony_desc}。"
            f"辐射半径{state.radius:.1f}，振动频率{state.frequency:.2f}Hz。"
            f"气场呈现{state.color.value}光芒。"
        )
        
        return description
    
    def to_ascii_art(self, state: QiFieldState) -> str:
        """生成ASCII艺术表示"""
        center = "◉"
        layers = int(min(5, state.radius))
        
        chars = ["·", "∘", "○", "◯", "◌"]
        
        art_lines = []
        size = layers * 2 + 3
        
        for y in range(size):
            line = ""
            for x in range(size):
                dist = math.sqrt((x - size // 2) ** 2 + (y - size // 2) ** 2)
                
                if dist < 0.5:
                    line += center
                elif dist <= layers + 1:
                    layer = int(dist)
                    if layer < len(chars):
                        char_index = min(layer, len(chars) - 1)
                        intensity_char = chars[char_index]
                        if state.intensity > 50:
                            intensity_char = intensity_char.upper() if intensity_char.isalpha() else intensity_char
                        line += intensity_char
                    else:
                        line += " "
                else:
                    line += " "
            art_lines.append(line)
        
        return "\n".join(art_lines)
    
    def _get_shape_description(self, state: QiFieldState) -> str:
        """获取形状描述"""
        if state.harmony > 0.8:
            return "完美的圆形，边缘光滑"
        elif state.harmony > 0.5:
            return "近似圆形，略有波动"
        else:
            return "不规则形状，边缘模糊"
    
    def _get_movement_description(self, state: QiFieldState) -> str:
        """获取运动描述"""
        if state.frequency > 1.5:
            return "快速脉动，如心跳般活跃"
        elif state.frequency > 1.0:
            return "平稳流动，如水波扩散"
        else:
            return "缓慢起伏，如云烟缭绕"
    
    def _calculate_aura_layers(self, state: QiFieldState) -> List[Dict]:
        """计算气场层级"""
        layers = []
        num_layers = max(1, int(state.radius))
        
        for i in range(num_layers):
            layer_intensity = state.get_field_strength_at_distance(i + 0.5)
            layers.append({
                "layer": i + 1,
                "distance": i + 0.5,
                "intensity": round(layer_intensity, 2),
                "color_blend": self._blend_color_with_intensity(state, layer_intensity)
            })
        
        return layers
    
    def _determine_timbre(self, state: QiFieldState) -> str:
        """确定音色"""
        if state.field_type == QiFieldType.AGGRESSIVE:
            return "金属质感，锐利清晰"
        elif state.field_type == QiFieldType.GENTLE:
            return "丝滑柔和，如水如风"
        elif state.field_type == QiFieldType.WISDOM:
            return "空灵悠远，如钟如磬"
        else:
            return "圆润饱满，和谐统一"
    
    def _frequency_to_note(self, frequency: float) -> str:
        """将频率转换为音符"""
        if frequency <= 0:
            return "静音"
        
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        A4 = 440.0
        half_steps = 12 * math.log2(frequency / A4)
        note_index = int(round(half_steps)) % 12
        octave = 4 + int(round(half_steps + 9) // 12)
        
        return f"{notes[note_index]}{octave}"
    
    def _get_duration_suggestion(self, state: QiFieldState) -> float:
        """获取持续时间建议"""
        base_duration = 3.0
        return base_duration * (1.0 + state.harmony)
    
    def _get_intensity_description(self, intensity: float) -> str:
        """获取强度描述"""
        if intensity >= 80:
            return "气势磅礴"
        elif intensity >= 60:
            return "充沛有力"
        elif intensity >= 40:
            return "平稳适中"
        elif intensity >= 20:
            return "微弱轻柔"
        else:
            return "几不可察"
    
    def _get_harmony_description(self, harmony: float) -> str:
        """获取和谐度描述"""
        if harmony >= 0.8:
            return "完美和谐"
        elif harmony >= 0.6:
            return "较为协调"
        elif harmony >= 0.4:
            return "略有波动"
        else:
            return "紊乱不稳"
    
    def _blend_color_with_intensity(self, state: QiFieldState, intensity: float) -> str:
        """根据强度混合颜色"""
        base_rgb = self.COLOR_RGB_MAP.get(state.color, (255, 255, 255))
        blend_factor = intensity / state.intensity if state.intensity > 0 else 0
        
        blended = tuple(int(c * blend_factor) for c in base_rgb)
        return '#{:02x}{:02x}{:02x}'.format(*blended)
    
    def _record_visualization(self, visualization: Dict) -> None:
        """记录可视化历史"""
        self.visualization_history.append({
            "timestamp": datetime.now().isoformat(),
            "visualization": visualization
        })
        if len(self.visualization_history) > 50:
            self.visualization_history = self.visualization_history[-50:]


class QiFieldInteraction:
    """
    气场交互处理器 - Qi Field Interaction Handler
    
    处理气场与外部环境的交互
    """
    
    PROTECTION_ENERGY_COST = 10.0
    INTENTION_ENERGY_COST = 5.0
    HARMONIZE_ENERGY_COST = 8.0
    
    def __init__(self, emitter: QiFieldEmitter):
        self.emitter = emitter
        self.interaction_history: List[Dict] = []
        self.active_protection = False
        self.protection_strength = 0.0
        self.detected_fields: List[QiFieldState] = []
    
    def sense_external(self, external_field: QiFieldState) -> Dict:
        """
        感知外部气场 - Sense External Qi Field
        
        Args:
            external_field: 外部气场状态
            
        Returns:
            感知结果
        """
        self.detected_fields.append(external_field)
        if len(self.detected_fields) > 20:
            self.detected_fields = self.detected_fields[-20:]
        
        my_state = self.emitter.get_state()
        
        intensity_ratio = external_field.intensity / my_state.intensity if my_state.intensity > 0 else 0
        
        frequency_diff = abs(external_field.frequency - my_state.frequency)
        
        harmony_diff = abs(external_field.harmony - my_state.harmony)
        
        threat_level = self._assess_threat_level(external_field, intensity_ratio)
        
        compatibility = self._calculate_compatibility(my_state, external_field)
        
        result = {
            "detected": True,
            "external_intensity": external_field.intensity,
            "intensity_ratio": round(intensity_ratio, 2),
            "frequency_difference": round(frequency_diff, 2),
            "harmony_difference": round(harmony_diff, 2),
            "threat_level": threat_level,
            "compatibility": round(compatibility, 2),
            "recommended_action": self._recommend_action(threat_level, compatibility)
        }
        
        self._record_interaction("sense", result)
        
        return result
    
    def harmonize(self, target_field: QiFieldState) -> Dict:
        """
        与目标气场和谐 - Harmonize with Target Field
        
        Args:
            target_field: 目标气场状态
            
        Returns:
            和谐结果
        """
        if self.emitter._energy_reserve < self.HARMONIZE_ENERGY_COST:
            return {
                "success": False,
                "message": "能量不足，无法进行和谐调整"
            }
        
        my_state = self.emitter.get_state()
        
        target_frequency = target_field.frequency
        my_frequency = my_state.frequency
        
        adjustment = (target_frequency - my_frequency) * 0.3
        new_frequency = my_frequency + adjustment
        my_state.frequency = max(0.1, new_frequency)
        
        target_harmony = target_field.harmony
        harmony_boost = (target_harmony - my_state.harmony) * 0.2
        my_state.harmony = max(0.0, min(1.0, my_state.harmony + harmony_boost))
        
        self.emitter._energy_reserve -= self.HARMONIZE_ENERGY_COST
        
        resonance_result = self.emitter.resonate_with(target_field)
        
        result = {
            "success": True,
            "frequency_adjustment": round(adjustment, 3),
            "new_frequency": round(my_state.frequency, 3),
            "harmony_change": round(harmony_boost, 3),
            "new_harmony": round(my_state.harmony, 3),
            "resonance": resonance_result.to_dict(),
            "energy_cost": self.HARMONIZE_ENERGY_COST
        }
        
        self._record_interaction("harmonize", result)
        
        return result
    
    def protect(self, strength: float = 0.5) -> Dict:
        """
        气场护盾 - Qi Field Protection Shield
        
        Args:
            strength: 护盾强度 (0-1)
            
        Returns:
            护盾结果
        """
        if self.emitter._energy_reserve < self.PROTECTION_ENERGY_COST:
            return {
                "success": False,
                "message": "能量不足，无法启动护盾"
            }
        
        strength = max(0.0, min(1.0, strength))
        
        my_state = self.emitter.get_state()
        
        if not self.emitter.boundary:
            self.emitter.create_boundary(
                inner_radius=my_state.radius * 0.3,
                outer_radius=my_state.radius * 0.8,
                permeability=1.0 - strength
            )
        else:
            self.emitter.boundary.permeability = 1.0 - strength
            self.emitter.boundary.strength = strength * my_state.intensity / 100.0
        
        self.active_protection = True
        self.protection_strength = strength
        
        energy_cost = self.PROTECTION_ENERGY_COST * strength
        self.emitter._energy_reserve -= energy_cost
        
        result = {
            "success": True,
            "protection_active": True,
            "protection_strength": round(strength, 2),
            "boundary": self.emitter.boundary.to_dict() if self.emitter.boundary else None,
            "energy_cost": round(energy_cost, 2),
            "remaining_energy": round(self.emitter._energy_reserve, 2)
        }
        
        self._record_interaction("protect", result)
        
        return result
    
    def deactivate_protection(self) -> Dict:
        """关闭护盾"""
        self.active_protection = False
        self.protection_strength = 0.0
        
        if self.emitter.boundary:
            self.emitter.boundary.active = False
        
        return {
            "success": True,
            "protection_active": False,
            "message": "护盾已关闭"
        }
    
    def project_intention(
        self, 
        intention: IntentionType, 
        target_distance: float = 1.0,
        intensity: float = 0.5
    ) -> Dict:
        """
        投射意图 - Project Intention
        
        Args:
            intention: 意图类型
            target_distance: 目标距离
            intensity: 投射强度
            
        Returns:
            投射结果
        """
        if self.emitter._energy_reserve < self.INTENTION_ENERGY_COST:
            return {
                "success": False,
                "message": "能量不足，无法投射意图"
            }
        
        my_state = self.emitter.get_state()
        
        effective_intensity = my_state.get_field_strength_at_distance(target_distance)
        projected_intensity = effective_intensity * intensity
        
        intention_frequency = self._get_intention_frequency(intention)
        my_state.frequency = (my_state.frequency + intention_frequency) / 2
        
        intention_color = self._get_intention_color(intention)
        
        energy_cost = self.INTENTION_ENERGY_COST * intensity
        self.emitter._energy_reserve -= energy_cost
        
        result = {
            "success": True,
            "intention": intention.value,
            "projected_intensity": round(projected_intensity, 2),
            "target_distance": target_distance,
            "intention_frequency": round(intention_frequency, 2),
            "intention_color": intention_color,
            "energy_cost": round(energy_cost, 2),
            "remaining_energy": round(self.emitter._energy_reserve, 2)
        }
        
        self._record_interaction("project_intention", result)
        
        return result
    
    def absorb_external_energy(
        self, 
        external_field: QiFieldState, 
        amount: float = 0.1
    ) -> Dict:
        """
        吸收外部气场能量
        
        Args:
            external_field: 外部气场
            amount: 吸收比例
            
        Returns:
            吸收结果
        """
        my_state = self.emitter.get_state()
        
        compatibility = self._calculate_compatibility(my_state, external_field)
        
        if compatibility < 0.3:
            return {
                "success": False,
                "message": "气场不兼容，无法吸收"
            }
        
        absorbed_energy = external_field.intensity * amount * compatibility
        self.emitter._energy_reserve = min(100.0, self.emitter._energy_reserve + absorbed_energy)
        
        self.emitter.state.intensity = min(100.0, my_state.intensity + absorbed_energy * 0.5)
        
        result = {
            "success": True,
            "absorbed_energy": round(absorbed_energy, 2),
            "new_energy_reserve": round(self.emitter._energy_reserve, 2),
            "new_intensity": round(self.emitter.state.intensity, 2)
        }
        
        self._record_interaction("absorb", result)
        
        return result
    
    def get_interaction_summary(self) -> Dict:
        """获取交互摘要"""
        return {
            "total_interactions": len(self.interaction_history),
            "detected_fields_count": len(self.detected_fields),
            "protection_active": self.active_protection,
            "protection_strength": self.protection_strength,
            "recent_interactions": self.interaction_history[-5:] if self.interaction_history else []
        }
    
    def _assess_threat_level(self, external_field: QiFieldState, intensity_ratio: float) -> str:
        """评估威胁等级"""
        if intensity_ratio > 2.0 and external_field.harmony < 0.3:
            return "危险"
        elif intensity_ratio > 1.5:
            return "警戒"
        elif intensity_ratio > 1.0:
            return "注意"
        else:
            return "安全"
    
    def _calculate_compatibility(
        self, 
        my_state: QiFieldState, 
        external_field: QiFieldState
    ) -> float:
        """计算兼容性"""
        frequency_match = 1.0 - min(1.0, abs(my_state.frequency - external_field.frequency) / max(my_state.frequency, 1.0))
        harmony_match = 1.0 - abs(my_state.harmony - external_field.harmony)
        color_match = 1.0 if my_state.color == external_field.color else 0.5
        
        return frequency_match * 0.4 + harmony_match * 0.4 + color_match * 0.2
    
    def _recommend_action(self, threat_level: str, compatibility: float) -> str:
        """推荐行动"""
        if threat_level == "危险":
            return "立即启动护盾并撤离"
        elif threat_level == "警戒":
            return "保持警惕，准备防御"
        elif compatibility > 0.7:
            return "可以尝试和谐共振"
        else:
            return "保持观察"
    
    def _get_intention_frequency(self, intention: IntentionType) -> float:
        """获取意图对应频率"""
        frequency_map = {
            IntentionType.HEALING: 0.8,
            IntentionType.PROTECTION: 1.5,
            IntentionType.GUIDANCE: 1.2,
            IntentionType.COMMUNICATION: 1.0,
            IntentionType.INFLUENCE: 1.8,
            IntentionType.DETECTION: 2.0
        }
        return frequency_map.get(intention, 1.0)
    
    def _get_intention_color(self, intention: IntentionType) -> str:
        """获取意图对应颜色"""
        color_map = {
            IntentionType.HEALING: "绿色",
            IntentionType.PROTECTION: "金色",
            IntentionType.GUIDANCE: "紫色",
            IntentionType.COMMUNICATION: "蓝色",
            IntentionType.INFLUENCE: "红色",
            IntentionType.DETECTION: "白色"
        }
        return color_map.get(intention, "白色")
    
    def _record_interaction(self, interaction_type: str, result: Dict) -> None:
        """记录交互历史"""
        self.interaction_history.append({
            "type": interaction_type,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })
        if len(self.interaction_history) > 100:
            self.interaction_history = self.interaction_history[-100:]


class QiFieldSystem:
    """
    气场系统主类 - Qi Field System Main Class
    
    整合气场发射、可视化和交互功能
    """
    
    def __init__(self, initial_state: Optional[QiFieldState] = None):
        self.emitter = QiFieldEmitter(initial_state)
        self.visualizer = QiFieldVisualizer()
        self.interaction = QiFieldInteraction(self.emitter)
        self.system_history: List[Dict] = []
    
    def initialize(
        self,
        jing_level: float = 0.5,
        qi_level: float = 0.5,
        shen_level: float = 0.5,
        yinyang_balance: float = 0.0,
        wuxing_element: str = "土"
    ) -> Dict:
        """
        初始化气场系统
        
        Args:
            jing_level: 精水平
            qi_level: 气水平
            shen_level: 神水平
            yinyang_balance: 阴阳平衡
            wuxing_element: 五行属性
            
        Returns:
            初始化结果
        """
        jing_qi_shen_result = self.emitter.update_from_jing_qi_shen(
            jing_level, qi_level, shen_level
        )
        
        yinyang_result = self.emitter.update_from_yinyang_balance(yinyang_balance)
        
        wuxing_result = self.emitter.update_from_wuxing(wuxing_element)
        
        init_result = {
            "success": True,
            "jing_qi_shen_update": jing_qi_shen_result,
            "yinyang_update": yinyang_result,
            "wuxing_update": wuxing_result,
            "final_state": self.emitter.get_state().to_dict()
        }
        
        self._record_system_event("initialize", init_result)
        
        return init_result
    
    def emit_field(self, intensity: Optional[float] = None) -> Dict:
        """发射气场"""
        result = self.emitter.emit(intensity)
        self._record_system_event("emit", result)
        return result
    
    def visualize(self) -> Dict:
        """可视化气场"""
        state = self.emitter.get_state()
        return self.visualizer.visualize_state(state)
    
    def sense(self, external_field: QiFieldState) -> Dict:
        """感知外部气场"""
        return self.interaction.sense_external(external_field)
    
    def harmonize_with(self, target_field: QiFieldState) -> Dict:
        """与目标和谐"""
        return self.interaction.harmonize(target_field)
    
    def activate_protection(self, strength: float = 0.5) -> Dict:
        """激活护盾"""
        return self.interaction.protect(strength)
    
    def project(self, intention: IntentionType, distance: float = 1.0) -> Dict:
        """投射意图"""
        return self.interaction.project_intention(intention, distance)
    
    def get_full_status(self) -> Dict:
        """获取完整状态"""
        state = self.emitter.get_state()
        visualization = self.visualizer.visualize_state(state)
        interaction_summary = self.interaction.get_interaction_summary()
        
        return {
            "field_state": state.to_dict(),
            "visualization": visualization,
            "interaction": interaction_summary,
            "energy_reserve": self.emitter.get_energy_reserve(),
            "is_emitting": self.emitter.is_emitting,
            "has_boundary": self.emitter.boundary is not None
        }
    
    def _record_system_event(self, event_type: str, data: Dict) -> None:
        """记录系统事件"""
        self.system_history.append({
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        })
        if len(self.system_history) > 100:
            self.system_history = self.system_history[-100:]
    
    def reset(self) -> None:
        """重置系统"""
        self.emitter.reset()
        self.interaction = QiFieldInteraction(self.emitter)
        self.system_history.clear()


def create_qi_field_system(
    intensity: float = 50.0,
    radius: float = 1.0,
    harmony: float = 0.5
) -> QiFieldSystem:
    """工厂函数：创建气场系统"""
    initial_state = QiFieldState(
        intensity=intensity,
        radius=radius,
        harmony=harmony
    )
    return QiFieldSystem(initial_state=initial_state)
