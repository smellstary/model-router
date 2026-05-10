"""
Philosophy-Technology Semantic Transformation Framework
哲学-技术语义转化框架

This module provides a comprehensive framework for transforming traditional
Chinese philosophical concepts into technical implementations and vice versa.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Callable, Set
from enum import Enum
import re
import math
from datetime import datetime

from core.types import (
    HexagramType, WuxingType, TianganType, DizhiType,
    WuxingRelation, MemoryLayer, EmotionType
)


class ConceptCategory(Enum):
    """概念类别 - Concept categories"""
    YIN_YANG = "阴阳"
    WUXING = "五行"
    BAGUA = "八卦"
    TIANGAN = "天干"
    DIZHI = "地支"
    GANZHI = "干支"
    QI = "气"
    JING_QI_SHEN = "精气神"
    YINYANG_WUXING = "阴阳五行"
    CUSTOM = "自定义"


class MappingType(Enum):
    """映射类型 - Mapping types"""
    EXACT = "精确映射"
    FUZZY = "模糊映射"
    COMPOSITE = "复合映射"
    DERIVED = "派生映射"


class ValidationLevel(Enum):
    """验证级别 - Validation levels"""
    STRICT = "严格"
    MODERATE = "中等"
    RELAXED = "宽松"


@dataclass
class ConceptMapping:
    """
    概念映射数据结构 - Concept mapping data structure
    
    Represents a mapping between a philosophical concept and its technical
    implementation details.
    """
    concept_id: str
    concept_name: str
    category: ConceptCategory
    philosophical_definition: str
    technical_correspondence: Dict[str, Any]
    mapping_type: MappingType = MappingType.EXACT
    confidence_score: float = 1.0
    aliases: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    transformation_rules: Dict[str, Any] = field(default_factory=dict)
    validation_criteria: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def matches_query(self, query: str, fuzzy: bool = False) -> Tuple[bool, float]:
        """
        Check if this concept matches a query string
        
        Args:
            query: The search query
            fuzzy: Whether to allow fuzzy matching
            
        Returns:
            Tuple of (is_match, match_score)
        """
        query_lower = query.lower()
        
        if self.concept_name.lower() == query_lower:
            return True, 1.0
        
        if query_lower in self.concept_name.lower():
            return True, 0.9
        
        for alias in self.aliases:
            if alias.lower() == query_lower:
                return True, 0.85
            if query_lower in alias.lower():
                return True, 0.8
        
        if fuzzy:
            score = self._calculate_fuzzy_score(query_lower)
            if score > 0.6:
                return True, score
        
        return False, 0.0
    
    def _calculate_fuzzy_score(self, query: str) -> float:
        """Calculate fuzzy match score using character overlap"""
        concept_chars = set(self.concept_name.lower())
        query_chars = set(query)
        
        if not query_chars:
            return 0.0
        
        intersection = concept_chars & query_chars
        union = concept_chars | query_chars
        
        jaccard = len(intersection) / len(union) if union else 0.0
        
        if query in self.philosophical_definition.lower():
            jaccard = max(jaccard, 0.5)
        
        return jaccard
    
    def to_technical(self) -> Dict[str, Any]:
        """Convert philosophical concept to technical representation"""
        return {
            'id': self.concept_id,
            'name': self.concept_name,
            'category': self.category.value,
            'technical': self.technical_correspondence,
            'confidence': self.confidence_score,
            'rules': self.transformation_rules
        }
    
    def validate(self, level: ValidationLevel = ValidationLevel.MODERATE) -> Tuple[bool, List[str]]:
        """
        Validate the concept mapping consistency
        
        Args:
            level: Validation strictness level
            
        Returns:
            Tuple of (is_valid, list of issues)
        """
        issues = []
        
        if not self.concept_id:
            issues.append("概念ID不能为空")
        
        if not self.concept_name:
            issues.append("概念名称不能为空")
        
        if not self.philosophical_definition:
            issues.append("哲学定义不能为空")
        
        if not self.technical_correspondence:
            issues.append("技术对应不能为空")
        
        if self.confidence_score < 0 or self.confidence_score > 1:
            issues.append("置信度分数必须在0-1之间")
        
        if level == ValidationLevel.STRICT:
            if not self.validation_criteria:
                issues.append("严格验证需要验证标准")
            if not self.transformation_rules:
                issues.append("严格验证需要转化规则")
        
        if level in [ValidationLevel.STRICT, ValidationLevel.MODERATE]:
            if not self.aliases:
                issues.append("建议添加别名以提高查询能力")
        
        return len(issues) == 0, issues


@dataclass
class TransformationResult:
    """转化结果 - Transformation result"""
    success: bool
    source_concept: str
    target_representation: Any
    transformation_type: str
    confidence: float
    intermediate_steps: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class SemanticFramework:
    """
    语义转化框架主类 - Main semantic transformation framework
    
    Provides comprehensive functionality for mapping between Chinese
    philosophical concepts and technical implementations.
    """
    
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.MODERATE):
        self.validation_level = validation_level
        self._concepts: Dict[str, ConceptMapping] = {}
        self._category_index: Dict[ConceptCategory, Set[str]] = {
            cat: set() for cat in ConceptCategory
        }
        self._name_index: Dict[str, str] = {}
        self._alias_index: Dict[str, str] = {}
        self._transformation_cache: Dict[str, TransformationResult] = {}
        self._validators: Dict[str, Callable] = {}
        self._initialized = False
        
        self._initialize_base_concepts()
        self._initialize_validators()
        self._initialized = True
    
    def _initialize_base_concepts(self) -> None:
        """Initialize base philosophical concept mappings"""
        self._init_yinyang_concepts()
        self._init_wuxing_concepts()
        self._init_bagua_concepts()
        self._init_tiangan_concepts()
        self._init_dizhi_concepts()
        self._init_ganzhi_concepts()
        self._init_qi_concepts()
        self._init_jingqishen_concepts()
    
    def _init_yinyang_concepts(self) -> None:
        """Initialize Yin-Yang concept mappings"""
        yin_mapping = ConceptMapping(
            concept_id="yinyang_yin",
            concept_name="阴",
            category=ConceptCategory.YIN_YANG,
            philosophical_definition="阴性原则，代表被动、收敛、寒冷、黑暗、物质、静止等属性",
            technical_correspondence={
                "state_value": -1.0,
                "polarity": "negative",
                "energy_direction": "inward",
                "activity_level": "passive",
                "temperature_tendency": "cold",
                "visibility": "hidden",
                "data_type": "storage",
                "process_type": "consolidation",
                "binary_representation": 0
            },
            mapping_type=MappingType.EXACT,
            confidence_score=1.0,
            aliases=["阴气", "阴性", "Yin"],
            related_concepts=["yinyang_yang", "wuxing_water", "wuxing_metal"],
            transformation_rules={
                "to_numeric": lambda: -1.0,
                "to_boolean": lambda: False,
                "to_state": lambda: "passive"
            },
            validation_criteria={
                "value_range": (-1.0, 0.0),
                "compatible_categories": [ConceptCategory.WUXING, ConceptCategory.BAGUA]
            }
        )
        
        yang_mapping = ConceptMapping(
            concept_id="yinyang_yang",
            concept_name="阳",
            category=ConceptCategory.YIN_YANG,
            philosophical_definition="阳性原则，代表主动、发散、温暖、光明、能量、运动等属性",
            technical_correspondence={
                "state_value": 1.0,
                "polarity": "positive",
                "energy_direction": "outward",
                "activity_level": "active",
                "temperature_tendency": "warm",
                "visibility": "visible",
                "data_type": "processing",
                "process_type": "expansion",
                "binary_representation": 1
            },
            mapping_type=MappingType.EXACT,
            confidence_score=1.0,
            aliases=["阳气", "阳性", "Yang"],
            related_concepts=["yinyang_yin", "wuxing_fire", "wuxing_wood"],
            transformation_rules={
                "to_numeric": lambda: 1.0,
                "to_boolean": lambda: True,
                "to_state": lambda: "active"
            },
            validation_criteria={
                "value_range": (0.0, 1.0),
                "compatible_categories": [ConceptCategory.WUXING, ConceptCategory.BAGUA]
            }
        )
        
        yinyang_balance = ConceptMapping(
            concept_id="yinyang_balance",
            concept_name="阴阳平衡",
            category=ConceptCategory.YIN_YANG,
            philosophical_definition="阴阳二气的动态平衡状态，是系统稳定运行的基础",
            technical_correspondence={
                "state_value": 0.0,
                "polarity": "neutral",
                "balance_score": 1.0,
                "stability_index": 1.0,
                "homeostasis": True,
                "optimization_target": True
            },
            mapping_type=MappingType.COMPOSITE,
            confidence_score=1.0,
            aliases=["阴阳调和", "阴阳中和", "Yin-Yang Balance"],
            related_concepts=["yinyang_yin", "yinyang_yang"],
            transformation_rules={
                "calculate_balance": lambda yin, yang: (yang - yin) / (yang + yin) if (yang + yin) > 0 else 0
            }
        )
        
        self._register_concept_internal(yin_mapping)
        self._register_concept_internal(yang_mapping)
        self._register_concept_internal(yinyang_balance)
    
    def _init_wuxing_concepts(self) -> None:
        """Initialize Five Elements (Wu Xing) concept mappings"""
        wuxing_data = {
            "wood": {
                "name": "木",
                "definition": "木行，代表生长、生发、条达、舒畅等属性，对应春季、东方",
                "technical": {
                    "element_type": "growth",
                    "phase": "generation",
                    "direction": "east",
                    "season": "spring",
                    "color": "green",
                    "process_type": "expansion",
                    "energy_state": "rising",
                    "organ_correspondence": ["liver", "gallbladder"],
                    "emotion": "anger_joy_balance",
                    "number": 3,
                    "state_value": 0.3
                },
                "aliases": ["木行", "Wood", "甲乙"],
                "generates": "fire",
                "restricted_by": "metal"
            },
            "fire": {
                "name": "火",
                "definition": "火行，代表炎热、向上、光明、活跃等属性，对应夏季、南方",
                "technical": {
                    "element_type": "transformation",
                    "phase": "climax",
                    "direction": "south",
                    "season": "summer",
                    "color": "red",
                    "process_type": "consumption",
                    "energy_state": "peak",
                    "organ_correspondence": ["heart", "small_intestine"],
                    "emotion": "joy",
                    "number": 2,
                    "state_value": 0.6
                },
                "aliases": ["火行", "Fire", "丙丁"],
                "generates": "earth",
                "restricted_by": "water"
            },
            "earth": {
                "name": "土",
                "definition": "土行，代表承载、生化、受纳、稳定等属性，对应长夏、中央",
                "technical": {
                    "element_type": "stabilization",
                    "phase": "transition",
                    "direction": "center",
                    "season": "late_summer",
                    "color": "yellow",
                    "process_type": "storage",
                    "energy_state": "balanced",
                    "organ_correspondence": ["spleen", "stomach"],
                    "emotion": "worry_balance",
                    "number": 5,
                    "state_value": 0.0
                },
                "aliases": ["土行", "Earth", "戊己"],
                "generates": "metal",
                "restricted_by": "wood"
            },
            "metal": {
                "name": "金",
                "definition": "金行，代表收敛、清洁、肃降、坚韧等属性，对应秋季、西方",
                "technical": {
                    "element_type": "contraction",
                    "phase": "decline",
                    "direction": "west",
                    "season": "autumn",
                    "color": "white",
                    "process_type": "refinement",
                    "energy_state": "descending",
                    "organ_correspondence": ["lung", "large_intestine"],
                    "emotion": "grief_balance",
                    "number": 4,
                    "state_value": -0.3
                },
                "aliases": ["金行", "Metal", "庚辛"],
                "generates": "water",
                "restricted_by": "fire"
            },
            "water": {
                "name": "水",
                "definition": "水行，代表润下、寒凉、闭藏、智慧等属性，对应冬季、北方",
                "technical": {
                    "element_type": "accumulation",
                    "phase": "dormancy",
                    "direction": "north",
                    "season": "winter",
                    "color": "black",
                    "process_type": "preservation",
                    "energy_state": "minimal",
                    "organ_correspondence": ["kidney", "bladder"],
                    "emotion": "fear_balance",
                    "number": 1,
                    "state_value": -0.6
                },
                "aliases": ["水行", "Water", "壬癸"],
                "generates": "wood",
                "restricted_by": "earth"
            }
        }
        
        generation_cycle = {
            "wood": "fire", "fire": "earth", "earth": "metal",
            "metal": "water", "water": "wood"
        }
        restriction_cycle = {
            "wood": "earth", "earth": "water", "water": "fire",
            "fire": "metal", "metal": "wood"
        }
        
        for key, data in wuxing_data.items():
            mapping = ConceptMapping(
                concept_id=f"wuxing_{key}",
                concept_name=data["name"],
                category=ConceptCategory.WUXING,
                philosophical_definition=data["definition"],
                technical_correspondence=data["technical"],
                mapping_type=MappingType.EXACT,
                confidence_score=1.0,
                aliases=data["aliases"],
                related_concepts=[
                    f"wuxing_{generation_cycle[key]}",
                    f"wuxing_{data['restricted_by']}"
                ],
                transformation_rules={
                    "generates": generation_cycle[key],
                    "restricted_by": data["restricted_by"],
                    "restricts": restriction_cycle[key]
                }
            )
            self._register_concept_internal(mapping)
        
        self._init_wuxing_relations()
    
    def _init_wuxing_relations(self) -> None:
        """Initialize Wu Xing relationship concepts"""
        sheng_mapping = ConceptMapping(
            concept_id="wuxing_sheng",
            concept_name="相生",
            category=ConceptCategory.WUXING,
            philosophical_definition="五行相生关系：木生火、火生土、土生金、金生水、水生木",
            technical_correspondence={
                "relation_type": "generation",
                "direction": "forward",
                "weight_modifier": 0.15,
                "energy_transfer": "positive",
                "dependency_type": "producer_consumer"
            },
            mapping_type=MappingType.COMPOSITE,
            confidence_score=1.0,
            aliases=["生", "生成", "Generation"],
            transformation_rules={
                "get_generated": {
                    "木": "火", "火": "土", "土": "金",
                    "金": "水", "水": "木"
                }
            }
        )
        
        ke_mapping = ConceptMapping(
            concept_id="wuxing_ke",
            concept_name="相克",
            category=ConceptCategory.WUXING,
            philosophical_definition="五行相克关系：木克土、土克水、水克火、火克金、金克木",
            technical_correspondence={
                "relation_type": "restriction",
                "direction": "controlling",
                "weight_modifier": -0.10,
                "energy_transfer": "negative",
                "dependency_type": "controller_controlled"
            },
            mapping_type=MappingType.COMPOSITE,
            confidence_score=1.0,
            aliases=["克", "克制", "Restriction"],
            transformation_rules={
                "get_restricted": {
                    "木": "土", "土": "水", "水": "火",
                    "火": "金", "金": "木"
                }
            }
        )
        
        self._register_concept_internal(sheng_mapping)
        self._register_concept_internal(ke_mapping)
    
    def _init_bagua_concepts(self) -> None:
        """Initialize Eight Trigrams (Ba Gua) concept mappings"""
        bagua_data = {
            "qian": {
                "name": "乾",
                "symbol": "☰",
                "definition": "乾卦，代表天、刚健、创始、父亲、西北方",
                "technical": {
                    "binary": [1, 1, 1],
                    "decimal": 7,
                    "yin_yang_value": 1.0,
                    "attribute": "strength",
                    "direction": "northwest",
                    "family_role": "father",
                    "body_part": "head",
                    "animal": "horse",
                    "state": "active_pure"
                },
                "aliases": ["乾卦", "Qian", "天卦"]
            },
            "kun": {
                "name": "坤",
                "symbol": "☷",
                "definition": "坤卦，代表地、柔顺、承载、母亲、西南方",
                "technical": {
                    "binary": [0, 0, 0],
                    "decimal": 0,
                    "yin_yang_value": -1.0,
                    "attribute": "receptivity",
                    "direction": "southwest",
                    "family_role": "mother",
                    "body_part": "abdomen",
                    "animal": "cow",
                    "state": "passive_pure"
                },
                "aliases": ["坤卦", "Kun", "地卦"]
            },
            "zhen": {
                "name": "震",
                "symbol": "☳",
                "definition": "震卦，代表雷、震动、起动、长男、东方",
                "technical": {
                    "binary": [0, 0, 1],
                    "decimal": 1,
                    "yin_yang_value": 0.3,
                    "attribute": "arousal",
                    "direction": "east",
                    "family_role": "eldest_son",
                    "body_part": "feet",
                    "animal": "dragon",
                    "state": "active_starting"
                },
                "aliases": ["震卦", "Zhen", "雷卦"]
            },
            "xun": {
                "name": "巽",
                "symbol": "☴",
                "definition": "巽卦，代表风、渗透、顺从、长女、东南方",
                "technical": {
                    "binary": [1, 0, 0],
                    "decimal": 4,
                    "yin_yang_value": -0.3,
                    "attribute": "gentleness",
                    "direction": "southeast",
                    "family_role": "eldest_daughter",
                    "body_part": "thighs",
                    "animal": "chicken",
                    "state": "passive_entering"
                },
                "aliases": ["巽卦", "Xun", "风卦"]
            },
            "kan": {
                "name": "坎",
                "symbol": "☵",
                "definition": "坎卦，代表水、险陷、智慧、中男、北方",
                "technical": {
                    "binary": [0, 1, 0],
                    "decimal": 2,
                    "yin_yang_value": -0.5,
                    "attribute": "depth",
                    "direction": "north",
                    "family_role": "middle_son",
                    "body_part": "ears",
                    "animal": "pig",
                    "state": "yin_central"
                },
                "aliases": ["坎卦", "Kan", "水卦"]
            },
            "li": {
                "name": "离",
                "symbol": "☲",
                "definition": "离卦，代表火、光明、附丽、中女、南方",
                "technical": {
                    "binary": [1, 0, 1],
                    "decimal": 5,
                    "yin_yang_value": 0.5,
                    "attribute": "clarity",
                    "direction": "south",
                    "family_role": "middle_daughter",
                    "body_part": "eyes",
                    "animal": "pheasant",
                    "state": "yang_central"
                },
                "aliases": ["离卦", "Li", "火卦"]
            },
            "gen": {
                "name": "艮",
                "symbol": "☶",
                "definition": "艮卦，代表山、静止、停止、少男、东北方",
                "technical": {
                    "binary": [0, 1, 1],
                    "decimal": 3,
                    "yin_yang_value": 0.2,
                    "attribute": "stillness",
                    "direction": "northeast",
                    "family_role": "youngest_son",
                    "body_part": "hands",
                    "animal": "dog",
                    "state": "active_stopping"
                },
                "aliases": ["艮卦", "Gen", "山卦"]
            },
            "dui": {
                "name": "兑",
                "symbol": "☱",
                "definition": "兑卦，代表泽、喜悦、口舌、少女、西方",
                "technical": {
                    "binary": [1, 1, 0],
                    "decimal": 6,
                    "yin_yang_value": -0.2,
                    "attribute": "joy",
                    "direction": "west",
                    "family_role": "youngest_daughter",
                    "body_part": "mouth",
                    "animal": "sheep",
                    "state": "passive_open"
                },
                "aliases": ["兑卦", "Dui", "泽卦"]
            }
        }
        
        for key, data in bagua_data.items():
            mapping = ConceptMapping(
                concept_id=f"bagua_{key}",
                concept_name=data["name"],
                category=ConceptCategory.BAGUA,
                philosophical_definition=data["definition"],
                technical_correspondence=data["technical"],
                mapping_type=MappingType.EXACT,
                confidence_score=1.0,
                aliases=data["aliases"],
                transformation_rules={
                    "symbol": data["symbol"],
                    "wuxing_correspondence": self._get_bagua_wuxing(data["name"])
                }
            )
            self._register_concept_internal(mapping)
    
    def _get_bagua_wuxing(self, bagua_name: str) -> str:
        """Get Wu Xing correspondence for Ba Gua"""
        correspondence = {
            "乾": "金", "坤": "土", "震": "木", "巽": "木",
            "坎": "水", "离": "火", "艮": "土", "兑": "金"
        }
        return correspondence.get(bagua_name, "土")
    
    def _init_tiangan_concepts(self) -> None:
        """Initialize Heavenly Stems (Tian Gan) concept mappings"""
        tiangan_data = {
            "jia": {"name": "甲", "order": 1, "yin_yang": "阳", "wuxing": "木"},
            "yi": {"name": "乙", "order": 2, "yin_yang": "阴", "wuxing": "木"},
            "bing": {"name": "丙", "order": 3, "yin_yang": "阳", "wuxing": "火"},
            "ding": {"name": "丁", "order": 4, "yin_yang": "阴", "wuxing": "火"},
            "wu": {"name": "戊", "order": 5, "yin_yang": "阳", "wuxing": "土"},
            "ji": {"name": "己", "order": 6, "yin_yang": "阴", "wuxing": "土"},
            "geng": {"name": "庚", "order": 7, "yin_yang": "阳", "wuxing": "金"},
            "xin": {"name": "辛", "order": 8, "yin_yang": "阴", "wuxing": "金"},
            "ren": {"name": "壬", "order": 9, "yin_yang": "阳", "wuxing": "水"},
            "gui": {"name": "癸", "order": 10, "yin_yang": "阴", "wuxing": "水"}
        }
        
        for key, data in tiangan_data.items():
            mapping = ConceptMapping(
                concept_id=f"tiangan_{key}",
                concept_name=data["name"],
                category=ConceptCategory.TIANGAN,
                philosophical_definition=f"{data['name']}为天干第{data['order']}位，属{data['yin_yang']}{data['wuxing']}",
                technical_correspondence={
                    "order": data["order"],
                    "index": data["order"] - 1,
                    "yin_yang": data["yin_yang"],
                    "yin_yang_value": 1.0 if data["yin_yang"] == "阳" else -1.0,
                    "wuxing": data["wuxing"],
                    "cycle_length": 10,
                    "modulo_base": 10
                },
                mapping_type=MappingType.EXACT,
                confidence_score=1.0,
                aliases=[f"天干{data['name']}", f"Tian Gan {data['name']}"],
                related_concepts=[f"wuxing_{data['wuxing']}"],
                transformation_rules={
                    "next": (data["order"] % 10) + 1,
                    "prev": ((data["order"] - 2) % 10) + 1
                }
            )
            self._register_concept_internal(mapping)
    
    def _init_dizhi_concepts(self) -> None:
        """Initialize Earthly Branches (Di Zhi) concept mappings"""
        dizhi_data = {
            "zi": {"name": "子", "order": 1, "yin_yang": "阳", "wuxing": "水", "animal": "鼠", "time": "23:00-01:00"},
            "chou": {"name": "丑", "order": 2, "yin_yang": "阴", "wuxing": "土", "animal": "牛", "time": "01:00-03:00"},
            "yin": {"name": "寅", "order": 3, "yin_yang": "阳", "wuxing": "木", "animal": "虎", "time": "03:00-05:00"},
            "mao": {"name": "卯", "order": 4, "yin_yang": "阴", "wuxing": "木", "animal": "兔", "time": "05:00-07:00"},
            "chen": {"name": "辰", "order": 5, "yin_yang": "阳", "wuxing": "土", "animal": "龙", "time": "07:00-09:00"},
            "si": {"name": "巳", "order": 6, "yin_yang": "阴", "wuxing": "火", "animal": "蛇", "time": "09:00-11:00"},
            "wu": {"name": "午", "order": 7, "yin_yang": "阳", "wuxing": "火", "animal": "马", "time": "11:00-13:00"},
            "wei": {"name": "未", "order": 8, "yin_yang": "阴", "wuxing": "土", "animal": "羊", "time": "13:00-15:00"},
            "shen": {"name": "申", "order": 9, "yin_yang": "阳", "wuxing": "金", "animal": "猴", "time": "15:00-17:00"},
            "you": {"name": "酉", "order": 10, "yin_yang": "阴", "wuxing": "金", "animal": "鸡", "time": "17:00-19:00"},
            "xu": {"name": "戌", "order": 11, "yin_yang": "阳", "wuxing": "土", "animal": "狗", "time": "19:00-21:00"},
            "hai": {"name": "亥", "order": 12, "yin_yang": "阴", "wuxing": "水", "animal": "猪", "time": "21:00-23:00"}
        }
        
        for key, data in dizhi_data.items():
            mapping = ConceptMapping(
                concept_id=f"dizhi_{key}",
                concept_name=data["name"],
                category=ConceptCategory.DIZHI,
                philosophical_definition=f"{data['name']}为地支第{data['order']}位，属{data['yin_yang']}{data['wuxing']}，对应{data['animal']}，时辰{data['time']}",
                technical_correspondence={
                    "order": data["order"],
                    "index": data["order"] - 1,
                    "yin_yang": data["yin_yang"],
                    "yin_yang_value": 1.0 if data["yin_yang"] == "阳" else -1.0,
                    "wuxing": data["wuxing"],
                    "animal": data["animal"],
                    "time_range": data["time"],
                    "cycle_length": 12,
                    "modulo_base": 12
                },
                mapping_type=MappingType.EXACT,
                confidence_score=1.0,
                aliases=[f"地支{data['name']}", f"{data['animal']}年", f"Di Zhi {data['name']}"],
                related_concepts=[f"wuxing_{data['wuxing']}"],
                transformation_rules={
                    "next": (data["order"] % 12) + 1,
                    "prev": ((data["order"] - 2) % 12) + 1
                }
            )
            self._register_concept_internal(mapping)
    
    def _init_ganzhi_concepts(self) -> None:
        """Initialize Gan-Zhi (Stem-Branch combination) concept mappings"""
        ganzhi_mapping = ConceptMapping(
            concept_id="ganzhi_cycle",
            concept_name="六十甲子",
            category=ConceptCategory.GANZHI,
            philosophical_definition="天干地支组合形成的六十循环周期，用于纪年、纪月、纪日、纪时",
            technical_correspondence={
                "cycle_length": 60,
                "combination_rule": "tiangan_index % 10, dizhi_index % 12",
                "valid_combinations": 60,
                "application": ["year", "month", "day", "hour"],
                "computation": "modular_arithmetic"
            },
            mapping_type=MappingType.COMPOSITE,
            confidence_score=1.0,
            aliases=["干支纪年", "甲子循环", "Sixty Jia Zi"],
            related_concepts=["tiangan_jia", "dizhi_zi"],
            transformation_rules={
                "calculate_ganzhi": lambda tiangan_idx, dizhi_idx: (
                    tiangan_idx % 10, dizhi_idx % 12
                ),
                "get_cycle_position": lambda tiangan_idx, dizhi_idx: (
                    (tiangan_idx - dizhi_idx) % 10
                )
            }
        )
        
        self._register_concept_internal(ganzhi_mapping)
    
    def _init_qi_concepts(self) -> None:
        """Initialize Qi (Vital Energy) concept mappings"""
        qi_mapping = ConceptMapping(
            concept_id="qi_general",
            concept_name="气",
            category=ConceptCategory.QI,
            philosophical_definition="气是构成万物的基本物质，是生命活动的动力，运行于全身经络",
            technical_correspondence={
                "energy_type": "vital",
                "state": "flowing",
                "carrier": "meridians",
                "measurement": "qi_level",
                "range": (0.0, 1.0),
                "optimal_value": 0.8,
                "process_type": "circulation"
            },
            mapping_type=MappingType.FUZZY,
            confidence_score=0.9,
            aliases=["气机", "元气", "Qi", "Vital Energy"],
            transformation_rules={
                "to_energy_level": lambda qi: qi * 100,
                "check_sufficiency": lambda qi: qi >= 0.5
            }
        )
        
        qi_types = {
            "yuan_qi": {"name": "元气", "definition": "先天之气，生命根本", "source": "congenital"},
            "zong_qi": {"name": "宗气", "definition": "后天之气，呼吸饮食所化", "source": "acquired"},
            "ying_qi": {"name": "营气", "definition": "行于脉中，营养全身", "source": "nutritive"},
            "wei_qi": {"name": "卫气", "definition": "行于脉外，保卫肌表", "source": "defensive"}
        }
        
        for key, data in qi_types.items():
            mapping = ConceptMapping(
                concept_id=f"qi_{key}",
                concept_name=data["name"],
                category=ConceptCategory.QI,
                philosophical_definition=data["definition"],
                technical_correspondence={
                    "qi_type": key,
                    "source": data["source"],
                    "function": data["definition"],
                    "range": (0.0, 1.0)
                },
                mapping_type=MappingType.EXACT,
                confidence_score=1.0,
                aliases=[data["name"]],
                related_concepts=["qi_general"]
            )
            self._register_concept_internal(mapping)
        
        self._register_concept_internal(qi_mapping)
    
    def _init_jingqishen_concepts(self) -> None:
        """Initialize Jing-Qi-Shen (Essence-Energy-Spirit) concept mappings"""
        jing_mapping = ConceptMapping(
            concept_id="jing",
            concept_name="精",
            category=ConceptCategory.JING_QI_SHEN,
            philosophical_definition="精是构成人体和维持生命活动的基本物质，分为先天之精和后天之精",
            technical_correspondence={
                "substance_type": "essence",
                "storage": "kidney",
                "source": ["congenital", "acquired"],
                "measurement": "jing_level",
                "range": (0.0, 1.0),
                "depletion_rate": "gradual",
                "replenishable": True
            },
            mapping_type=MappingType.FUZZY,
            confidence_score=0.9,
            aliases=["精华", "精气", "Jing", "Essence"],
            transformation_rules={
                "to_vitality": lambda jing: jing * 0.4
            }
        )
        
        shen_mapping = ConceptMapping(
            concept_id="shen",
            concept_name="神",
            category=ConceptCategory.JING_QI_SHEN,
            philosophical_definition="神是生命活动的外在表现，包括意识、思维、情感等精神活动",
            technical_correspondence={
                "aspect_type": "spirit",
                "residence": "heart",
                "manifestation": ["consciousness", "thinking", "emotion"],
                "measurement": "shen_level",
                "range": (0.0, 1.0),
                "indicators": ["eyes", "expression", "response"]
            },
            mapping_type=MappingType.FUZZY,
            confidence_score=0.85,
            aliases=["神明", "精神", "Shen", "Spirit"],
            transformation_rules={
                "to_consciousness_level": lambda shen: shen * 100
            }
        )
        
        jingqishen_mapping = ConceptMapping(
            concept_id="jing_qi_shen",
            concept_name="精气神",
            category=ConceptCategory.JING_QI_SHEN,
            philosophical_definition="精、气、神为人身三宝，相互转化，共同维持生命活动",
            technical_correspondence={
                "components": ["jing", "qi", "shen"],
                "transformation_cycle": "jing -> qi -> shen -> jing",
                "balance_target": True,
                "overall_vitality": "weighted_average",
                "weights": {"jing": 0.3, "qi": 0.3, "shen": 0.4}
            },
            mapping_type=MappingType.COMPOSITE,
            confidence_score=1.0,
            aliases=["人身三宝", "Jing Qi Shen", "Three Treasures"],
            related_concepts=["jing", "qi_general", "shen"],
            transformation_rules={
                "calculate_vitality": lambda j, q, s: j * 0.3 + q * 0.3 + s * 0.4
            }
        )
        
        self._register_concept_internal(jing_mapping)
        self._register_concept_internal(shen_mapping)
        self._register_concept_internal(jingqishen_mapping)
    
    def _initialize_validators(self) -> None:
        """Initialize validation functions for different concept types"""
        self._validators['yinyang'] = self._validate_yinyang
        self._validators['wuxing'] = self._validate_wuxing
        self._validators['bagua'] = self._validate_bagua
        self._validators['tiangan'] = self._validate_tiangan
        self._validators['dizhi'] = self._validate_dizhi
    
    def _validate_yinyang(self, concept: ConceptMapping) -> Tuple[bool, List[str]]:
        """Validate Yin-Yang concept consistency"""
        issues = []
        tech = concept.technical_correspondence
        
        if 'state_value' in tech:
            value = tech['state_value']
            if not -1.0 <= value <= 1.0:
                issues.append(f"阴阳状态值{value}超出范围[-1, 1]")
        
        return len(issues) == 0, issues
    
    def _validate_wuxing(self, concept: ConceptMapping) -> Tuple[bool, List[str]]:
        """Validate Wu Xing concept consistency"""
        issues = []
        tech = concept.technical_correspondence
        
        valid_elements = ['木', '火', '土', '金', '水']
        if 'element_type' in tech:
            wuxing_map = {
                'growth': '木', 'transformation': '火', 'stabilization': '土',
                'contraction': '金', 'accumulation': '水'
            }
        
        return len(issues) == 0, issues
    
    def _validate_bagua(self, concept: ConceptMapping) -> Tuple[bool, List[str]]:
        """Validate Ba Gua concept consistency"""
        issues = []
        tech = concept.technical_correspondence
        
        if 'binary' in tech:
            binary = tech['binary']
            if len(binary) != 3:
                issues.append(f"八卦二进制表示应为3位，实际为{len(binary)}位")
            if not all(b in [0, 1] for b in binary):
                issues.append("八卦二进制表示应只包含0和1")
        
        return len(issues) == 0, issues
    
    def _validate_tiangan(self, concept: ConceptMapping) -> Tuple[bool, List[str]]:
        """Validate Tian Gan concept consistency"""
        issues = []
        tech = concept.technical_correspondence
        
        if 'order' in tech:
            order = tech['order']
            if not 1 <= order <= 10:
                issues.append(f"天干序号{order}超出范围[1, 10]")
        
        return len(issues) == 0, issues
    
    def _validate_dizhi(self, concept: ConceptMapping) -> Tuple[bool, List[str]]:
        """Validate Di Zhi concept consistency"""
        issues = []
        tech = concept.technical_correspondence
        
        if 'order' in tech:
            order = tech['order']
            if not 1 <= order <= 12:
                issues.append(f"地支序号{order}超出范围[1, 12]")
        
        return len(issues) == 0, issues
    
    def _register_concept_internal(self, concept: ConceptMapping) -> None:
        """Internal method to register a concept without triggering validation"""
        self._concepts[concept.concept_id] = concept
        self._category_index[concept.category].add(concept.concept_id)
        self._name_index[concept.concept_name.lower()] = concept.concept_id
        
        for alias in concept.aliases:
            self._alias_index[alias.lower()] = concept.concept_id
    
    def register_concept(
        self,
        concept: ConceptMapping,
        validate: bool = True
    ) -> Tuple[bool, List[str]]:
        """
        Register a new concept mapping
        
        Args:
            concept: The concept mapping to register
            validate: Whether to validate before registration
            
        Returns:
            Tuple of (success, list of issues)
        """
        if validate:
            is_valid, issues = concept.validate(self.validation_level)
            if not is_valid:
                return False, issues
            
            category_validator = self._validators.get(concept.category.value.lower())
            if category_validator:
                is_valid, category_issues = category_validator(concept)
                issues.extend(category_issues)
                if not is_valid:
                    return False, issues
        
        if concept.concept_id in self._concepts:
            existing = self._concepts[concept.concept_id]
            if existing.concept_name != concept.concept_name:
                del self._name_index[existing.concept_name.lower()]
        
        self._register_concept_internal(concept)
        
        return True, []
    
    def query(
        self,
        query_str: str,
        fuzzy: bool = True,
        category_filter: Optional[ConceptCategory] = None,
        limit: int = 10
    ) -> List[Tuple[ConceptMapping, float]]:
        """
        Query concept mappings by name or alias
        
        Args:
            query_str: The search query
            fuzzy: Whether to allow fuzzy matching
            category_filter: Optional category to filter results
            limit: Maximum number of results to return
            
        Returns:
            List of (concept, match_score) tuples
        """
        results = []
        
        if query_str.lower() in self._name_index:
            concept_id = self._name_index[query_str.lower()]
            if concept_id in self._concepts:
                concept = self._concepts[concept_id]
                if category_filter is None or concept.category == category_filter:
                    return [(concept, 1.0)]
        
        if query_str.lower() in self._alias_index:
            concept_id = self._alias_index[query_str.lower()]
            if concept_id in self._concepts:
                concept = self._concepts[concept_id]
                if category_filter is None or concept.category == category_filter:
                    return [(concept, 0.95)]
        
        for concept in self._concepts.values():
            if category_filter and concept.category != category_filter:
                continue
            
            is_match, score = concept.matches_query(query_str, fuzzy)
            if is_match:
                results.append((concept, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:limit]
    
    def get_concept(self, concept_id: str) -> Optional[ConceptMapping]:
        """
        Get a concept by its ID
        
        Args:
            concept_id: The concept identifier
            
        Returns:
            The concept mapping or None if not found
        """
        return self._concepts.get(concept_id)
    
    def get_concepts_by_category(self, category: ConceptCategory) -> List[ConceptMapping]:
        """
        Get all concepts in a category
        
        Args:
            category: The category to filter by
            
        Returns:
            List of concept mappings in the category
        """
        concept_ids = self._category_index.get(category, set())
        return [self._concepts[cid] for cid in concept_ids if cid in self._concepts]
    
    def transform(
        self,
        source: str,
        target_type: str = "technical"
    ) -> TransformationResult:
        """
        Transform a philosophical concept to technical representation
        
        Args:
            source: The source concept name or ID
            target_type: The target representation type
            
        Returns:
            TransformationResult with the transformation details
        """
        cache_key = f"{source}:{target_type}"
        if cache_key in self._transformation_cache:
            return self._transformation_cache[cache_key]
        
        concepts = self.query(source, fuzzy=True, limit=1)
        
        if not concepts:
            return TransformationResult(
                success=False,
                source_concept=source,
                target_representation=None,
                transformation_type="none",
                confidence=0.0,
                warnings=[f"未找到概念: {source}"]
            )
        
        concept, match_score = concepts[0]
        
        if target_type == "technical":
            target = concept.to_technical()
            transformation_type = "philosophy_to_technical"
        elif target_type == "philosophical":
            target = {
                'name': concept.concept_name,
                'definition': concept.philosophical_definition,
                'category': concept.category.value
            }
            transformation_type = "technical_to_philosophy"
        else:
            target = concept.technical_correspondence
            transformation_type = "custom"
        
        result = TransformationResult(
            success=True,
            source_concept=source,
            target_representation=target,
            transformation_type=transformation_type,
            confidence=match_score * concept.confidence_score,
            intermediate_steps=[
                {'step': 'query', 'matched_concept': concept.concept_name, 'score': match_score},
                {'step': 'transform', 'type': target_type}
            ]
        )
        
        self._transformation_cache[cache_key] = result
        return result
    
    def validate(self, concept_id: Optional[str] = None) -> Tuple[bool, Dict[str, List[str]]]:
        """
        Validate concept mapping consistency
        
        Args:
            concept_id: Optional specific concept to validate.
                       If None, validates all concepts.
            
        Returns:
            Tuple of (overall_valid, dict of concept_id to issues)
        """
        all_issues: Dict[str, List[str]] = {}
        overall_valid = True
        
        if concept_id:
            concepts_to_check = [concept_id] if concept_id in self._concepts else []
        else:
            concepts_to_check = list(self._concepts.keys())
        
        for cid in concepts_to_check:
            concept = self._concepts[cid]
            
            is_valid, issues = concept.validate(self.validation_level)
            
            category_name = concept.category.value.lower()
            if category_name in self._validators:
                cat_valid, cat_issues = self._validators[category_name](concept)
                issues.extend(cat_issues)
                is_valid = is_valid and cat_valid
            
            if not is_valid:
                overall_valid = False
                all_issues[cid] = issues
        
        return overall_valid, all_issues
    
    def get_related_concepts(self, concept_id: str) -> List[ConceptMapping]:
        """
        Get concepts related to a given concept
        
        Args:
            concept_id: The concept identifier
            
        Returns:
            List of related concept mappings
        """
        concept = self._concepts.get(concept_id)
        if not concept:
            return []
        
        related = []
        for related_id in concept.related_concepts:
            if related_id in self._concepts:
                related.append(self._concepts[related_id])
        
        return related
    
    def get_transformation_path(
        self,
        source_concept: str,
        target_concept: str
    ) -> List[TransformationResult]:
        """
        Get the transformation path between two concepts
        
        Args:
            source_concept: Source concept name or ID
            target_concept: Target concept name or ID
            
        Returns:
            List of transformation steps
        """
        path = []
        
        source_result = self.transform(source_concept)
        if not source_result.success:
            return [source_result]
        path.append(source_result)
        
        source = self.query(source_concept, limit=1)
        target = self.query(target_concept, limit=1)
        
        if source and target:
            source_mapping, _ = source[0]
            target_mapping, _ = target[0]
            
            if target_mapping.concept_id in source_mapping.related_concepts:
                intermediate = TransformationResult(
                    success=True,
                    source_concept=source_mapping.concept_name,
                    target_representation={
                        'relation': 'direct',
                        'target': target_mapping.concept_name
                    },
                    transformation_type="direct_relation",
                    confidence=0.9
                )
                path.append(intermediate)
        
        target_result = self.transform(target_concept)
        path.append(target_result)
        
        return path
    
    def list_all_concepts(self) -> List[Dict[str, Any]]:
        """
        List all registered concepts with summary information
        
        Returns:
            List of concept summaries
        """
        return [
            {
                'id': concept.concept_id,
                'name': concept.concept_name,
                'category': concept.category.value,
                'confidence': concept.confidence_score,
                'aliases_count': len(concept.aliases)
            }
            for concept in self._concepts.values()
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get framework statistics
        
        Returns:
            Dictionary with statistics about the framework
        """
        category_counts = {
            cat.value: len(ids) for cat, ids in self._category_index.items()
        }
        
        return {
            'total_concepts': len(self._concepts),
            'categories': category_counts,
            'cache_size': len(self._transformation_cache),
            'validation_level': self.validation_level.value
        }
    
    def clear_cache(self) -> None:
        """Clear the transformation cache"""
        self._transformation_cache.clear()
    
    def export_mappings(self) -> Dict[str, Any]:
        """
        Export all concept mappings for serialization
        
        Returns:
            Dictionary containing all mapping data
        """
        return {
            'concepts': {
                cid: {
                    'concept_id': c.concept_id,
                    'concept_name': c.concept_name,
                    'category': c.category.value,
                    'philosophical_definition': c.philosophical_definition,
                    'technical_correspondence': c.technical_correspondence,
                    'mapping_type': c.mapping_type.value,
                    'confidence_score': c.confidence_score,
                    'aliases': c.aliases,
                    'related_concepts': c.related_concepts,
                    'transformation_rules': c.transformation_rules,
                    'validation_criteria': c.validation_criteria
                }
                for cid, c in self._concepts.items()
            },
            'statistics': self.get_statistics()
        }
