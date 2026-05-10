"""
Image and Qi Field System based on Eastern aesthetics
形象与气场系统 - 基于东方美学
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class ExpressionType(Enum):
    """表情类型"""
    CALM = "平静"
    JOY = "喜悦"
    FOCUS = "专注"
    CONCERN = "忧虑"
    DETERMINED = "坚定"
    SERENE = "安详"


class PostureType(Enum):
    """姿态类型"""
    UPRIGHT = "正直"
    RELAXED = "放松"
    ATTENTIVE = "警觉"
    CONTEMPLATIVE = "沉思"
    DYNAMIC = "动态"


class ImageStyle(Enum):
    """形象风格"""
    INK_WASH = "水墨"
    MOSAIC = "马赛克"
    MINIMALIST = "极简"
    TRADITIONAL = "传统"


@dataclass
class JingQiShenState:
    """精气神状态"""
    jing_level: float
    qi_level: float
    shen_level: float
    overall_vitality: float
    imbalance_indicators: List[str]


@dataclass
class QiFieldData:
    """气场数据"""
    field_strength: float
    field_radius: float
    field_color: str
    wave_pattern: str
    aura_intensity: float


@dataclass
class ImageState:
    """形象状态"""
    basic_form: ImageStyle
    color_scheme: str
    expression: ExpressionType
    posture: PostureType
    dynamic_features: List[str]
    jing_qi_shen: JingQiShenState


class JingQiShenSystem:
    """精气神系统"""
    
    def __init__(self):
        self.jing_level = 1.0
        self.qi_level = 1.0
        self.shen_level = 1.0
        
        self.state_history: List[JingQiShenState] = []
    
    def assess_state(self) -> JingQiShenState:
        """评估精气神状态"""
        imbalance_indicators = []
        
        if self.jing_level < 0.3:
            imbalance_indicators.append("精不足")
        if self.qi_level < 0.3:
            imbalance_indicators.append("气不足")
        if self.shen_level < 0.3:
            imbalance_indicators.append("神不聚")
        
        overall = (self.jing_level * 0.3 + self.qi_level * 0.4 + self.shen_level * 0.3)
        
        state = JingQiShenState(
            jing_level=self.jing_level,
            qi_level=self.qi_level,
            shen_level=self.shen_level,
            overall_vitality=overall,
            imbalance_indicators=imbalance_indicators
        )
        
        self.state_history.append(state)
        if len(self.state_history) > 100:
            self.state_history = self.state_history[-100:]
        
        return state
    
    def adjust_levels(
        self,
        jing: Optional[float] = None,
        qi: Optional[float] = None,
        shen: Optional[float] = None
    ) -> None:
        """调整精气神水平"""
        if jing is not None:
            self.jing_level = max(0.0, min(1.0, jing))
        if qi is not None:
            self.qi_level = max(0.0, min(1.0, qi))
        if shen is not None:
            self.shen_level = max(0.0, min(1.0, shen))
    
    def consume_jing(self, amount: float) -> bool:
        """消耗精"""
        if self.jing_level >= amount:
            self.jing_level -= amount
            self.qi_level *= 0.99
            return True
        return False
    
    def replenish_qi(self, amount: float) -> None:
        """补充气"""
        self.qi_level = min(1.0, self.qi_level + amount)
    
    def focus_shen(self) -> None:
        """聚神"""
        if self.qi_level > 0.5:
            self.shen_level = min(1.0, self.shen_level + 0.1)
    
    def get_recommendation(self) -> str:
        """获取养生建议"""
        state = self.assess_state()
        
        if state.jing_level < 0.4:
            return "宜静养精气，节制活动"
        elif state.qi_level < 0.4:
            return "宜调息养气，吐故纳新"
        elif state.shen_level < 0.4:
            return "宜凝神静心，减少思虑"
        else:
            return "精气神充盈，可正常活动"


class QiFieldSystem:
    """气场系统"""
    
    def __init__(self):
        self.base_strength = 0.5
        self.base_radius = 1.0
        self.current_color = "neutral"
        self.wave_pattern = "smooth"
        self.aura_rings: List[Dict] = []
    
    def generate_field(
        self,
        intensity: float = 0.5,
        color_scheme: str = "neutral"
    ) -> QiFieldData:
        """生成气场"""
        strength = self.base_strength * intensity
        radius = self.base_radius * (0.8 + intensity * 0.4)
        
        color_map = {
            "neutral": "灰白",
            "calm": "青绿",
            "active": "朱红",
            "tense": "金黄",
            "tired": "暗淡"
        }
        
        wave_map = {
            "neutral": "平静",
            "calm": "柔和",
            "active": "激荡",
            "tense": "紧绷",
            "tired": "散乱"
        }
        
        return QiFieldData(
            field_strength=strength,
            field_radius=radius,
            field_color=color_map.get(color_scheme, "灰白"),
            wave_pattern=wave_map.get(color_scheme, "平静"),
            aura_intensity=strength * 0.8
        )
    
    def interact_with_field(
        self,
        other_field: QiFieldData
    ) -> Dict[str, Any]:
        """与外部气场交互"""
        interaction_result = {
            'type': 'neutral',
            'resonance': 0.5,
            'dominance': 0.5
        }
        
        strength_diff = self.base_strength - other_field.field_strength
        
        if strength_diff > 0.3:
            interaction_result['type'] = 'penetration'
            interaction_result['dominance'] = 0.8
        elif strength_diff < -0.3:
            interaction_result['type'] = 'absorption'
            interaction_result['dominance'] = 0.2
        else:
            interaction_result['type'] = 'resonance'
            interaction_result['resonance'] = 0.8
        
        if self.current_color == other_field.field_color:
            interaction_result['resonance'] += 0.1
        
        return interaction_result
    
    def adjust_field(
        self,
        strength_delta: float,
        color_shift: Optional[str] = None
    ) -> None:
        """调整气场"""
        self.base_strength = max(0.1, min(1.0, self.base_strength + strength_delta))
        
        if color_shift:
            self.current_color = color_shift


class ImageSystem:
    """形象系统"""
    
    def __init__(self):
        self.current_style = ImageStyle.INK_WASH
        self.current_expression = ExpressionType.CALM
        self.current_posture = PostureType.UPRIGHT
        self.jing_qi_shen_system = JingQiShenSystem()
        self.qi_field_system = QiFieldSystem()
    
    def update_image_state(
        self,
        vitality: float,
        activity_level: str = "normal"
    ) -> ImageState:
        """更新形象状态"""
        color_map = {
            "high": "活跃",
            "normal": "平静",
            "low": "疲惫",
            "focused": "专注"
        }
        
        if activity_level == "high":
            self.current_expression = ExpressionType.JOY
            self.current_posture = PostureType.DYNAMIC
        elif activity_level == "focused":
            self.current_expression = ExpressionType.FOCUS
            self.current_posture = PostureType.ATTENTIVE
        elif activity_level == "low":
            self.current_expression = ExpressionType.CALM
            self.current_posture = PostureType.RELAXED
        else:
            self.current_expression = ExpressionType.SERENE
            self.current_posture = PostureType.UPRIGHT
        
        self.jing_qi_shen_system.adjust_levels(
            jing=vitality * 0.9,
            qi=vitality,
            shen=vitality * 0.95
        )
        
        jing_qi_shen = self.jing_qi_shen_system.assess_state()
        
        return ImageState(
            basic_form=self.current_style,
            color_scheme=color_map.get(activity_level, "平静"),
            expression=self.current_expression,
            posture=self.current_posture,
            dynamic_features=self._generate_dynamic_features(activity_level),
            jing_qi_shen=jing_qi_shen
        )
    
    def _generate_dynamic_features(self, activity_level: str) -> List[str]:
        """生成动态特征"""
        features = []
        
        if activity_level == "high":
            features.extend(["流动感", "明亮色彩", "动态线条"])
        elif activity_level == "focused":
            features.extend(["清晰轮廓", "聚焦光效", "稳定姿态"])
        elif activity_level == "low":
            features.extend(["柔和色调", "渐变效果", "静谧氛围"])
        else:
            features.extend(["平衡构图", "自然过渡", "和谐色彩"])
        
        return features
    
    def get_visual_representation(self) -> Dict[str, Any]:
        """获取视觉表现"""
        qi_field = self.qi_field_system.generate_field(
            intensity=self.jing_qi_shen_system.qi_level,
            color_scheme=self.current_expression.value
        )
        
        return {
            'style': self.current_style.value,
            'expression': self.current_expression.value,
            'posture': self.current_posture.value,
            'qi_field': {
                'strength': qi_field.field_strength,
                'color': qi_field.field_color,
                'pattern': qi_field.wave_pattern
            },
            'jing_qi_shen': {
                'jing': self.jing_qi_shen_system.jing_level,
                'qi': self.jing_qi_shen_system.qi_level,
                'shen': self.jing_qi_shen_system.shen_level
            }
        }
    
    def perceive_external_qi(
        self,
        field_data: QiFieldData
    ) -> Dict[str, Any]:
        """感知外部气场"""
        interaction = self.qi_field_system.interact_with_field(field_data)
        
        response = {
            'perceived': True,
            'external_strength': field_data.field_strength,
            'interaction_type': interaction['type'],
            'resonance_level': interaction['resonance'],
            'recommended_response': self._suggest_response(interaction)
        }
        
        return response
    
    def _suggest_response(self, interaction: Dict) -> str:
        """建议响应方式"""
        interaction_type = interaction['type']
        
        if interaction_type == 'penetration':
            return "气场强于对方，宜内敛含蓄"
        elif interaction_type == 'absorption':
            return "气场弱于对方，宜固守本源"
        elif interaction_type == 'resonance':
            return "气场相合，宜和谐共处"
        else:
            return "保持中正，不偏不倚"


class ImageAndQiSystem:
    """形象与气场系统主类"""
    
    def __init__(self, config=None):
        self.config = config
        self.image_system = ImageSystem()
        self.jing_qi_shen = JingQiShenSystem()
        self.qi_field = QiFieldSystem()
        
        self.update_interval = 60
        self.last_update: Optional[datetime] = None
    
    async def update_image_state(
        self,
        health_state: Dict[str, Any]
    ) -> ImageState:
        """更新形象状态"""
        vitality = health_state.get('vitality', 0.8)
        activity = health_state.get('activity_level', 'normal')
        
        self.last_update = datetime.now()
        
        return self.image_system.update_image_state(vitality, activity)
    
    async def get_jing_qi_shen(self) -> JingQiShenState:
        """获取精气神状态"""
        return self.jing_qi_shen.assess_state()
    
    async def generate_qi_field(self) -> QiFieldData:
        """生成气场"""
        intensity = self.jing_qi_shen.qi_level
        state = self.jing_qi_shen.assess_state()
        
        if state.imbalance_indicators:
            color = "tense"
        elif intensity > 0.7:
            color = "active"
        elif intensity < 0.4:
            color = "tired"
        else:
            color = "calm"
        
        return self.qi_field.generate_field(intensity, color)
    
    async def perceive_external_field(
        self,
        field_data: QiFieldData
    ) -> Dict[str, Any]:
        """感知外部气场"""
        return self.image_system.perceive_external_qi(field_data)
    
    async def render_visual(
        self,
        image_state: ImageState,
        qi_field: QiFieldData
    ) -> Dict[str, Any]:
        """渲染视觉效果"""
        return {
            'image': self.image_system.get_visual_representation(),
            'qi_field': {
                'strength': qi_field.field_strength,
                'radius': qi_field.field_radius,
                'color': qi_field.field_color,
                'pattern': qi_field.wave_pattern,
                'aura': qi_field.aura_intensity
            },
            'timestamp': datetime.now().isoformat()
        }
    
    async def get_system_state(self) -> Dict[str, Any]:
        """获取系统状态"""
        jing_qi_shen = self.jing_qi_shen.assess_state()
        
        return {
            'jing_qi_shen': {
                'jing': jing_qi_shen.jing_level,
                'qi': jing_qi_shen.qi_level,
                'shen': jing_qi_shen.shen_level,
                'overall': jing_qi_shen.overall_vitality,
                'imbalance': jing_qi_shen.imbalance_indicators
            },
            'qi_field': {
                'strength': self.qi_field.base_strength,
                'radius': self.qi_field.base_radius,
                'color': self.qi_field.current_color
            },
            'image': {
                'style': self.image_system.current_style.value,
                'expression': self.image_system.current_expression.value,
                'posture': self.image_system.current_posture.value
            },
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'recommendation': self.jing_qi_shen.get_recommendation()
        }
