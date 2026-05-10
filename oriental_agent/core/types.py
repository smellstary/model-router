"""
Core type definitions for Oriental Wisdom Agent System
东方智慧智能体系统核心类型定义
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


class HexagramType(Enum):
    """八卦类型 - Eight Trigrams (伏羲八卦)"""
    QIAN = "乾"   # 天 - Heaven/Sky
    KUN = "坤"   # 地 - Earth
    ZHEN = "震"   # 雷 - Thunder
    XUN = "巽"   # 风 - Wind
    KAN = "坎"   # 水 - Water
    LI = "离"    # 火 - Fire
    GEN = "艮"   # 山 - Mountain
    DUI = "兑"   # 泽 - Lake/Marsh


class MemoryLayer(Enum):
    """记忆层次 - Three-layer memory architecture"""
    HEAVEN = "天道"   # 天道层 - Macro principles and universal laws
    EARTH = "地道"   # 地道层 - Environment interaction and external stimuli
    HUMAN = "人道"   # 人道层 - Subjective experience and decision history


class WuxingType(Enum):
    """五行类型 - Five Elements"""
    WOOD = "木"   # Wood - Growth, creation
    FIRE = "火"   # Fire - Passion, motivation
    EARTH = "土"  # Earth - Stability, bearing
    METAL = "金"  # Metal - Decision, contraction
    WATER = "水"  # Water - Flow, wisdom


class TianganType(Enum):
    """天干类型 - Ten Heavenly Stems"""
    JIA = "甲"
    YI = "乙"
    BING = "丙"
    DING = "丁"
    WU = "戊"
    JI = "己"
    GENG = "庚"
    XIN = "辛"
    REN = "壬"
    GUI = "癸"


class DizhiType(Enum):
    """地支类型 - Twelve Earthly Branches"""
    ZI = "子"
    CHOU = "丑"
    YIN = "寅"
    MAO = "卯"
    CHEN = "辰"
    SI = "巳"
    WU = "午"
    WEI = "未"
    SHEN = "申"
    YOU = "酉"
    XU = "戌"
    HAI = "亥"


class AssociationType(Enum):
    """记忆关联类型 - Memory association types"""
    CAUSAL = "因果"      # 因果关系
    SIMILAR = "相似"     # 相似关系
    TEMPORAL = "时序"    # 时间顺序
    CONTRAST = "对比"    # 对比关系
    COMPLEMENT = "互补"  # 互补关系


class WuxingRelation(Enum):
    """五行关系 - Five elements relationship"""
    GENERATE = "相生"    # 相生 - Generation
    RESTRICT = "相克"    # 相克 - Restriction
    SAME_NATURE = "同性"  # 同性 - Same nature


class QueryType(Enum):
    """记忆查询类型 - Memory query types"""
    KEYWORD = "关键词"
    CONTEXT = "上下文"
    TIME_RANGE = "时间范围"
    ASSOCIATION = "关联查询"
    PREDICTION = "预测查询"


class SenseType(Enum):
    """感知类型 - Six consciousness types (六识)"""
    VISUAL = "眼识"      # 视觉 - Eye consciousness
    AUDITORY = "耳识"   # 听觉 - Ear consciousness
    OLFACTORY = "鼻识"  # 嗅觉 - Nose consciousness
    GUSTATORY = "舌识"  # 味觉 - Tongue consciousness
    TACTILE = "身识"    # 触觉 - Body consciousness
    MENTAL = "意识"     # 意识 - Mind consciousness


class EmotionType(Enum):
    """情感类型 - Emotion types based on Chinese philosophy"""
    JOY = "喜"          # 喜 - Joy
    ANGER = "怒"        # 怒 - Anger
    WORRY = "忧"        # 忧 - Worry
    SADNESS = "悲"      # 悲 - Sadness
    FEAR = "恐"         # 恐 - Fear
    SHOCK = "惊"        # 惊 - Shock
    CALM = "静"          # 静 - Calm
    HARMONY = "和"      # 和 - Harmony


class OrganType(Enum):
    """脏腑类型 - Organ types"""
    HEART = "心"         # Heart - 君主之官
    LIVER = "肝"         # Liver - 将军之官
    SPLEEN = "脾"        # Spleen - 仓廪之官
    LUNG = "肺"          # Lung - 相傅之官
    KIDNEY = "肾"        # Kidney - 作强之官
    SMALL_INTESTINE = "小肠"  # Small intestine
    GALLBLADDER = "胆"   # Gallbladder
    STOMACH = "胃"       # Stomach
    LARGE_INTESTINE = "大肠"  # Large intestine
    BLADDER = "膀胱"     # Bladder
    TRIPLE_BURNER = "三焦"  # Triple burner
    PERICARDIUM = "心包"  # Pericardium


class ThreatLevel(Enum):
    """威胁等级 - Threat levels"""
    NORMAL = "正常"      # Normal fluctuation
    POTENTIAL = "潜在"   # Potential risk
    DEFINITE = "明确"    # Clear threat
    CRITICAL = "紧急"    # Critical emergency


class BehaviorMode(Enum):
    """行为模式 - Behavior modes based on Five Animals (五禽戏)"""
    TIGER = "虎形"       # 刚猛迅捷
    DEER = "鹿形"        # 轻盈敏捷
    BEAR = "熊形"        # 沉稳有力
    APE = "猿形"         # 灵巧多变
    BIRD = "鸟形"        # 高瞻远瞩


class ReasoningType(Enum):
    """推理类型 - Reasoning types"""
    CAUSAL = "因果推理"
    DEDUCTIVE = "演绎推理"
    ABDUCTIVE = "溯因推理"
    ANALOGICAL = "类比推理"
    DIALECTICAL = "辩证推理"


class TimeHorizon(Enum):
    """时间视野 - Time horizons"""
    SHORT_TERM = "短期"
    MEDIUM_TERM = "中期"
    LONG_TERM = "长期"


@dataclass
class MemoryNode:
    """记忆节点 - Memory node"""
    memory_id: str
    content: Any
    memory_type: HexagramType
    layer: MemoryLayer
    yin_yang_balance: float = 0.0
    wuxing_attribute: WuxingType = WuxingType.EARTH
    tiangan_tag: Optional[TianganType] = None
    dizhi_tag: Optional[DizhiType] = None
    weight: float = 1.0
    strength: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    associations: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryAssociation:
    """记忆关联 - Memory association"""
    source_id: str
    target_id: str
    association_type: AssociationType
    wuxing_relationship: WuxingRelation
    strength: float = 1.0
    bidirectional: bool = True


@dataclass
class MemoryQuery:
    """记忆查询 - Memory query"""
    query_type: QueryType
    keywords: List[str] = field(default_factory=list)
    hexagram_filter: Optional[List[HexagramType]] = None
    layer_filter: Optional[MemoryLayer] = None
    time_range: Optional[Tuple[datetime, datetime]] = None
    wuxing_filter: Optional[WuxingType] = None
    limit: int = 10


@dataclass
class ThinkingContext:
    """思考上下文 - Thinking context"""
    question: str
    situation: Any
    available_options: List[Any] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    time_horizon: TimeHorizon = TimeHorizon.SHORT_TERM
    relevant_memories: List[MemoryNode] = field(default_factory=list)


@dataclass
class Stakeholder:
    """利益相关方 - Stakeholder"""
    name: str
    role: str
    interests: List[str] = field(default_factory=list)
    relationship: str = "neutral"


@dataclass
class ExecutionTask:
    """执行任务 - Execution task"""
    task_id: str
    task_type: str
    action_sequence: List[Any] = field(default_factory=list)
    priority: int = 5
    resource_requirement: Dict[str, float] = field(default_factory=dict)
    deadline: Optional[datetime] = None
    constraints: List[str] = field(default_factory=list)


@dataclass
class DefenseState:
    """防御状态 - Defense state"""
    threat_level: ThreatLevel
    active_defenses: List[str] = field(default_factory=list)
    resource_allocation: Dict[str, float] = field(default_factory=dict)
    energy_level: float = 1.0
    stability_score: float = 1.0


@dataclass
class PerceptionData:
    """感知数据 - Perception data"""
    perception_id: str
    sense_type: SenseType
    raw_data: Any
    processed_features: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    confidence: float = 0.0
    attention_weight: float = 1.0


@dataclass
class MeridianState:
    """经络状态 - Meridian state"""
    meridian_id: str
    meridian_name: str
    flow_rate: float = 1.0
    blockage_level: float = 0.0
    energy_level: float = 1.0


@dataclass
class OrganState:
    """脏腑状态 - Organ state"""
    organ_id: str
    organ_name: str
    organ_type: OrganType
    wuxing_attribute: WuxingType
    functional_level: float = 1.0
    energy_consumption: float = 0.0


@dataclass
class HealthState:
    """健康状态 - Health state"""
    vitality_score: float = 1.0
    meridian_network: List[MeridianState] = field(default_factory=list)
    organ_states: List[OrganState] = field(default_factory=list)
    qi_total: float = 1.0
    blood_total: float = 1.0


@dataclass
class JingQiShenState:
    """精气神状态 - Jing Qi Shen state"""
    jing_level: float = 1.0
    qi_level: float = 1.0
    shen_level: float = 1.0
    overall_vitality: float = 1.0


@dataclass
class ImageState:
    """形象状态 - Image state"""
    basic_form: str = "neutral"
    color_scheme: str = "balanced"
    dynamic_features: List[str] = field(default_factory=list)
    expression: str = "calm"
    posture: str = "upright"


@dataclass
class QiFieldData:
    """气场数据 - Qi field data"""
    field_strength: float = 0.5
    field_radius: float = 1.0
    field_color: str = "neutral"
    wave_pattern: str = "smooth"
