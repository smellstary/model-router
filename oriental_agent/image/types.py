"""
智能体形象系统 - 类型定义
基于SVG矢量图形的可自定义虚拟形象
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid


class FaceShape(Enum):
    """脸型枚举"""
    OVAL = "oval"           # 鹅蛋脸
    ROUND = "round"         # 圆脸
    HEART = "heart"         # 心形脸
    SQUARE = "square"       # 方脸
    LONG = "long"           # 长脸
    DIAMOND = "diamond"     # 菱形脸


class EyeShape(Enum):
    """眼型枚举"""
    ALMOND = "almond"       # 杏仁眼
    ROUND = "round"         # 圆眼
    MONOLID = "monolid"     # 单眼皮
    HOODDED = "hooded"      # 内双
    DEEPSET = "deepset"     # 深眼窝


class HairStyle(Enum):
    """发型枚举"""
    STRAIGHT_LONG = "straight_long"     # 长直发
    STRAIGHT_SHORT = "straight_short"   # 短直发
    WAVY_LONG = "wavy_long"             # 长卷发
    WAVY_SHORT = "wavy_short"           # 短卷发
    BOB = "bob"                         # 波波头
    PONYTAIL = "ponytail"               # 马尾
    BUN = "bun"                         # 丸子头
    SHAVED = "shaved"                   # 剃短发


class SkinTone(Enum):
    """肤色枚举"""
    FAIR = "fair"             # 白皙
    LIGHT = "light"           # 浅肤色
    MEDIUM = "medium"         # 中等肤色
    OLIVE = "olive"           # 橄榄色
    TAN = "tan"               # 古铜色


class MakeupStyle(Enum):
    """妆容风格"""
    NATURAL = "natural"       # 自然妆
    GLAM = "glam"             # 华丽妆
    MINIMAL = "minimal"       # 极简妆
    SMOKEY = "smokey"         # 烟熏妆
    BRIGHT = "bright"         # 亮色妆


@dataclass
class FacialFeatures:
    """面部特征"""
    face_shape: FaceShape = FaceShape.OVAL
    face_width: float = 0.5           # 0-1 脸宽
    face_length: float = 0.5          # 0-1 脸长
    
    eye_shape: EyeShape = EyeShape.ALMOND
    eye_size: float = 0.5             # 0-1 眼睛大小
    eye_spacing: float = 0.5          # 0-1 眼间距
    eye_height: float = 0.5           # 0-1 眼高
    
    nose_width: float = 0.5           # 0-1 鼻梁宽度
    nose_length: float = 0.5          # 0-1 鼻子长度
    nose_tip: float = 0.5             # 0-1 鼻尖圆润度
    
    lip_thickness: float = 0.5        # 0-1 嘴唇厚度
    lip_width: float = 0.5            # 0-1 嘴唇宽度
    lip_curve: float = 0.5            # 0-1 唇形弧度
    
    cheekbones: float = 0.5           # 0-1 颧骨突出度
    jawline: float = 0.5              # 0-1 下颌线清晰度
    forehead: float = 0.5             # 0-1 额头高度


@dataclass
class HairFeatures:
    """发型特征"""
    style: HairStyle = HairStyle.STRAIGHT_LONG
    length: float = 0.7               # 0-1 头发长度
    volume: float = 0.5               # 0-1 头发蓬松度
    wave_intensity: float = 0.3       # 0-1 卷曲程度
    
    color: str = "#2c2c2c"            # 头发颜色
    highlights: Optional[str] = None   # 挑染颜色
    
    bangs: bool = False               # 是否有刘海
    bangs_length: float = 0.3         # 刘海长度


@dataclass
class MakeupFeatures:
    """妆容特征"""
    style: MakeupStyle = MakeupStyle.NATURAL
    
    foundation_shade: str = "#f5e6d3" # 粉底颜色
    foundation_coverage: float = 0.5  # 0-1 粉底覆盖度
    
    eyeshadow_color: str = "#d4c4b0"  # 眼影颜色
    eyeshadow_intensity: float = 0.3  # 0-1 眼影浓度
    
    eyeliner: bool = True             # 是否画眼线
    eyeliner_thickness: float = 0.3   # 0-1 眼线粗细
    
    mascara: bool = True              # 是否涂睫毛膏
    mascara_intensity: float = 0.5    # 0-1 睫毛膏浓度
    
    blush_color: str = "#ffb7c5"      # 腮红颜色
    blush_intensity: float = 0.3      # 0-1 腮红浓度
    
    lipstick_color: str = "#e87a8a"   # 口红颜色
    lipstick_gloss: float = 0.5       # 0-1 口红光泽度
    
    eyebrow_color: str = "#5a4a42"    # 眉毛颜色
    eyebrow_thickness: float = 0.5    # 0-1 眉毛粗细
    eyebrow_arch: float = 0.5         # 0-1 眉峰高度


@dataclass
class Accessories:
    """配饰"""
    earrings: bool = False
    earring_style: str = "stud"        # stud, hoop, drop
    
    necklace: bool = False
    necklace_style: str = "simple"     # simple, layered, pendant
    
    bracelet: bool = False
    bracelet_style: str = "bangle"     # bangle, chain, charm
    
    glasses: bool = False
    glasses_style: str = "cat_eye"     # cat_eye, round, square, aviator


@dataclass
class Outfit:
    """服装"""
    type: str = "casual"               # casual, formal, sporty, elegant
    color: str = "#ffffff"             # 服装颜色
    pattern: str = "solid"             # solid, striped, floral, plaid
    neckline: str = "round"            # round, v-neck, scoop, off-shoulder
    sleeves: str = "long"              # long, short, sleeveless


@dataclass
class AvatarPreset:
    """形象预设"""
    preset_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    category: str = "default"          # default, celebrity, custom
    
    facial_features: FacialFeatures = field(default_factory=FacialFeatures)
    hair_features: HairFeatures = field(default_factory=HairFeatures)
    makeup_features: MakeupFeatures = field(default_factory=MakeupFeatures)
    accessories: Accessories = field(default_factory=Accessories)
    outfit: Outfit = field(default_factory=Outfit)
    
    created_at: datetime = field(default_factory=datetime.now)
    popularity: int = 0


@dataclass
class Avatar:
    """智能体形象"""
    avatar_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    name: str = "东方智慧"
    display_name: str = ""
    
    facial_features: FacialFeatures = field(default_factory=FacialFeatures)
    hair_features: HairFeatures = field(default_factory=HairFeatures)
    makeup_features: MakeupFeatures = field(default_factory=MakeupFeatures)
    accessories: Accessories = field(default_factory=Accessories)
    outfit: Outfit = field(default_factory=Outfit)
    
    skin_tone: SkinTone = SkinTone.LIGHT
    
    emotion: str = "neutral"           # neutral, happy, sad, surprised, angry
    pose: str = "standing"             # standing, sitting, walking, thinking
    
    last_modified: datetime = field(default_factory=datetime.now)
    preset_source: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "avatar_id": self.avatar_id,
            "name": self.name,
            "display_name": self.display_name,
            "facial_features": {
                "face_shape": self.facial_features.face_shape.value,
                "face_width": self.facial_features.face_width,
                "face_length": self.facial_features.face_length,
                "eye_shape": self.facial_features.eye_shape.value,
                "eye_size": self.facial_features.eye_size,
                "eye_spacing": self.facial_features.eye_spacing,
                "eye_height": self.facial_features.eye_height,
                "nose_width": self.facial_features.nose_width,
                "nose_length": self.facial_features.nose_length,
                "nose_tip": self.facial_features.nose_tip,
                "lip_thickness": self.facial_features.lip_thickness,
                "lip_width": self.facial_features.lip_width,
                "lip_curve": self.facial_features.lip_curve,
                "cheekbones": self.facial_features.cheekbones,
                "jawline": self.facial_features.jawline,
                "forehead": self.facial_features.forehead
            },
            "hair_features": {
                "style": self.hair_features.style.value,
                "length": self.hair_features.length,
                "volume": self.hair_features.volume,
                "wave_intensity": self.hair_features.wave_intensity,
                "color": self.hair_features.color,
                "highlights": self.hair_features.highlights,
                "bangs": self.hair_features.bangs,
                "bangs_length": self.hair_features.bangs_length
            },
            "makeup_features": {
                "style": self.makeup_features.style.value,
                "foundation_shade": self.makeup_features.foundation_shade,
                "foundation_coverage": self.makeup_features.foundation_coverage,
                "eyeshadow_color": self.makeup_features.eyeshadow_color,
                "eyeshadow_intensity": self.makeup_features.eyeshadow_intensity,
                "eyeliner": self.makeup_features.eyeliner,
                "eyeliner_thickness": self.makeup_features.eyeliner_thickness,
                "mascara": self.makeup_features.mascara,
                "mascara_intensity": self.makeup_features.mascara_intensity,
                "blush_color": self.makeup_features.blush_color,
                "blush_intensity": self.makeup_features.blush_intensity,
                "lipstick_color": self.makeup_features.lipstick_color,
                "lipstick_gloss": self.makeup_features.lipstick_gloss,
                "eyebrow_color": self.makeup_features.eyebrow_color,
                "eyebrow_thickness": self.makeup_features.eyebrow_thickness,
                "eyebrow_arch": self.makeup_features.eyebrow_arch
            },
            "accessories": {
                "earrings": self.accessories.earrings,
                "earring_style": self.accessories.earring_style,
                "necklace": self.accessories.necklace,
                "necklace_style": self.accessories.necklace_style,
                "bracelet": self.accessories.bracelet,
                "bracelet_style": self.accessories.bracelet_style,
                "glasses": self.accessories.glasses,
                "glasses_style": self.accessories.glasses_style
            },
            "outfit": {
                "type": self.outfit.type,
                "color": self.outfit.color,
                "pattern": self.outfit.pattern,
                "neckline": self.outfit.neckline,
                "sleeves": self.outfit.sleeves
            },
            "skin_tone": self.skin_tone.value,
            "emotion": self.emotion,
            "pose": self.pose,
            "last_modified": self.last_modified.isoformat(),
            "preset_source": self.preset_source
        }
