"""
Tuibeitu Sequence Prediction Module
推背图序列预测模块 - 基于易理的序列演化预测算法

推背图是中国古代预言奇书，共六十象，每象由卦象、谶语、颂曰组成。
本模块实现基于易理的序列演化预测算法。

核心组件：
- TuibeituImage: 推背图象数据结构
- SequenceEvolver: 序列演化器
- TuibeituPredictor: 推背图预测器
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import os
import importlib.util


_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_types_path = os.path.join(_project_root, "core", "types.py")
_types_spec = importlib.util.spec_from_file_location("types_module", _types_path)
_types_module = importlib.util.module_from_spec(_types_spec)
_types_spec.loader.exec_module(_types_module)

WuxingType = _types_module.WuxingType
WuxingRelation = _types_module.WuxingRelation
HexagramType = _types_module.HexagramType
TianganType = _types_module.TianganType
DizhiType = _types_module.DizhiType


class GuaSymbol(Enum):
    """六十四卦符号 - Sixty-Four Hexagrams"""
    QIAN_QIAN = "乾为天"
    KUN_KUN = "坤为地"
    SHUI_LEI_TUN = "水雷屯"
    SHAN_SHUI_MENG = "山水蒙"
    SHUI_TIAN_XU = "水天需"
    TIAN_SHUI_SONG = "天水讼"
    DI_SHUI_SHI = "地水师"
    SHUI_DI_BI = "水地比"
    FENG_TIAN_XIAO_CHU = "风天小畜"
    TIAN_ZE_LV = "天泽履"
    DI_TIAN_TAI = "地天泰"
    TIAN_DI_PI = "天地否"
    TIAN_HUO_TONG_REN = "天火同人"
    HUO_TIAN_DA_YOU = "火天大有"
    DI_SHAN_QIAN = "地山谦"
    LEI_DI_YU = "雷地豫"
    ZE_LEI_SUI = "泽雷随"
    SHAN_FENG_GU = "山风蛊"
    DI_ZE_LIN = "地泽临"
    FENG_DI_GUAN = "风地观"
    HUO_LEI_SHI_KE = "火雷噬嗑"
    SHAN_HUO_BEN = "山火贲"
    SHAN_DI_BO = "山地剥"
    DI_LEI_FU = "地雷复"
    TIAN_LEI_WU_WANG = "天雷无妄"
    SHAN_TIAN_DA_CHU = "山天大畜"
    SHAN_LEI_YI = "山雷颐"
    ZE_FENG_DA_GUO = "泽风大过"
    KAN_KAN = "坎为水"
    LI_LI = "离为火"
    ZE_SHAN_XIAN = "泽山咸"
    LEI_FENG_HENG = "雷风恒"
    TIAN_SHAN_DUN = "天山遁"
    LEI_TIAN_DA_ZHUANG = "雷天大壮"
    HUO_DI_JIN = "火地晋"
    DI_HUO_MING_YI = "地火明夷"
    FENG_HUO_JIA_REN = "风火家人"
    HUO_ZE_KUI = "火泽睽"
    SHUI_SHAN_JIAN = "水山蹇"
    LEI_SHUI_JIE = "雷水解"
    SHAN_ZE_SUN = "山泽损"
    FENG_LEI_YI = "风雷益"
    ZE_TIAN_GUAI = "泽天夬"
    TIAN_FENG_GOU = "天风姤"
    ZE_DI_CUI = "泽地萃"
    DI_FENG_SHENG = "地风升"
    ZE_SHUI_KUN = "泽水困"
    SHUI_FENG_JING = "水风井"
    ZE_HUO_GE = "泽火革"
    HUO_FENG_DING = "火风鼎"
    ZHEN_ZHEN = "震为雷"
    GEN_GEN = "艮为山"
    FENG_SHAN_JIAN = "风山渐"
    LEI_ZE_GUI_MEI = "雷泽归妹"
    LEI_HUO_FENG = "雷火丰"
    HUO_SHAN_LV = "火山旅"
    XUN_XUN = "巽为风"
    DUI_DUI = "兑为泽"
    FENG_SHUI_HUAN = "风水涣"
    SHUI_ZE_JIE = "水泽节"
    FENG_ZE_ZHONG_FU = "风泽中孚"
    LEI_SHAN_XIAO_GUO = "雷山小过"
    SHUI_HUO_JI_JI = "水火既济"
    HUO_SHUI_WEI_JI = "火水未济"


class EvolutionDirection(Enum):
    """演化方向 - Evolution directions based on Wu Xing"""
    SHENG = "相生演化"
    KE = "相克演化"
    CHENG = "承演化"
    HUA = "化演化"
    NI = "逆演化"
    SHUN = "顺演化"


@dataclass
class TimeHint:
    """时间暗示 - Time hint in Tuibeitu image"""
    ganzhi_cycle: Optional[str] = None
    dynasty_hint: Optional[str] = None
    year_hint: Optional[str] = None
    season_hint: Optional[str] = None
    relative_time: Optional[str] = None
    confidence: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        return {
            'ganzhi_cycle': self.ganzhi_cycle,
            'dynasty_hint': self.dynasty_hint,
            'year_hint': self.year_hint,
            'season_hint': self.season_hint,
            'relative_time': self.relative_time,
            'confidence': self.confidence,
        }


@dataclass
class TuibeituImage:
    """
    推背图象数据结构 - Tuibeitu Image Data Structure
    
    推背图共六十象，每象由卦象、谶语、颂曰组成
    """
    image_number: int
    gua_symbol: GuaSymbol
    chen_yu: str
    song_yue: str
    wuxing_attribution: WuxingType
    time_hint: TimeHint = field(default_factory=TimeHint)
    upper_trigram: HexagramType = field(default=HexagramType.QIAN)
    lower_trigram: HexagramType = field(default=HexagramType.QIAN)
    yao_positions: List[int] = field(default_factory=list)
    interpretation: str = ""
    historical_events: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not 1 <= self.image_number <= 60:
            raise ValueError(f"象序必须在1-60之间，当前: {self.image_number}")
        if not self.yao_positions:
            self.yao_positions = self._calculate_default_yao()
        self._sync_trigrams()

    def _sync_trigrams(self):
        upper, lower = self._get_trigrams_from_gua()
        self.upper_trigram = upper
        self.lower_trigram = lower

    def _get_trigrams_from_gua(self) -> Tuple[HexagramType, HexagramType]:
        gua_trigram_map = {
            GuaSymbol.QIAN_QIAN: (HexagramType.QIAN, HexagramType.QIAN),
            GuaSymbol.KUN_KUN: (HexagramType.KUN, HexagramType.KUN),
            GuaSymbol.SHUI_LEI_TUN: (HexagramType.KAN, HexagramType.ZHEN),
            GuaSymbol.SHAN_SHUI_MENG: (HexagramType.GEN, HexagramType.KAN),
            GuaSymbol.SHUI_TIAN_XU: (HexagramType.KAN, HexagramType.QIAN),
            GuaSymbol.TIAN_SHUI_SONG: (HexagramType.QIAN, HexagramType.KAN),
            GuaSymbol.DI_SHUI_SHI: (HexagramType.KUN, HexagramType.KAN),
            GuaSymbol.SHUI_DI_BI: (HexagramType.KAN, HexagramType.KUN),
            GuaSymbol.FENG_TIAN_XIAO_CHU: (HexagramType.XUN, HexagramType.QIAN),
            GuaSymbol.TIAN_ZE_LV: (HexagramType.QIAN, HexagramType.DUI),
            GuaSymbol.DI_TIAN_TAI: (HexagramType.KUN, HexagramType.QIAN),
            GuaSymbol.TIAN_DI_PI: (HexagramType.QIAN, HexagramType.KUN),
            GuaSymbol.TIAN_HUO_TONG_REN: (HexagramType.QIAN, HexagramType.LI),
            GuaSymbol.HUO_TIAN_DA_YOU: (HexagramType.LI, HexagramType.QIAN),
            GuaSymbol.DI_SHAN_QIAN: (HexagramType.KUN, HexagramType.GEN),
            GuaSymbol.LEI_DI_YU: (HexagramType.ZHEN, HexagramType.KUN),
            GuaSymbol.ZE_LEI_SUI: (HexagramType.DUI, HexagramType.ZHEN),
            GuaSymbol.SHAN_FENG_GU: (HexagramType.GEN, HexagramType.XUN),
            GuaSymbol.DI_ZE_LIN: (HexagramType.KUN, HexagramType.DUI),
            GuaSymbol.FENG_DI_GUAN: (HexagramType.XUN, HexagramType.KUN),
            GuaSymbol.HUO_LEI_SHI_KE: (HexagramType.LI, HexagramType.ZHEN),
            GuaSymbol.SHAN_HUO_BEN: (HexagramType.GEN, HexagramType.LI),
            GuaSymbol.SHAN_DI_BO: (HexagramType.GEN, HexagramType.KUN),
            GuaSymbol.DI_LEI_FU: (HexagramType.KUN, HexagramType.ZHEN),
            GuaSymbol.TIAN_LEI_WU_WANG: (HexagramType.QIAN, HexagramType.ZHEN),
            GuaSymbol.SHAN_TIAN_DA_CHU: (HexagramType.GEN, HexagramType.QIAN),
            GuaSymbol.SHAN_LEI_YI: (HexagramType.GEN, HexagramType.ZHEN),
            GuaSymbol.ZE_FENG_DA_GUO: (HexagramType.DUI, HexagramType.XUN),
            GuaSymbol.KAN_KAN: (HexagramType.KAN, HexagramType.KAN),
            GuaSymbol.LI_LI: (HexagramType.LI, HexagramType.LI),
            GuaSymbol.ZE_SHAN_XIAN: (HexagramType.DUI, HexagramType.GEN),
            GuaSymbol.LEI_FENG_HENG: (HexagramType.ZHEN, HexagramType.XUN),
            GuaSymbol.TIAN_SHAN_DUN: (HexagramType.QIAN, HexagramType.GEN),
            GuaSymbol.LEI_TIAN_DA_ZHUANG: (HexagramType.ZHEN, HexagramType.QIAN),
            GuaSymbol.HUO_DI_JIN: (HexagramType.LI, HexagramType.KUN),
            GuaSymbol.DI_HUO_MING_YI: (HexagramType.KUN, HexagramType.LI),
            GuaSymbol.FENG_HUO_JIA_REN: (HexagramType.XUN, HexagramType.LI),
            GuaSymbol.HUO_ZE_KUI: (HexagramType.LI, HexagramType.DUI),
            GuaSymbol.SHUI_SHAN_JIAN: (HexagramType.KAN, HexagramType.GEN),
            GuaSymbol.LEI_SHUI_JIE: (HexagramType.ZHEN, HexagramType.KAN),
            GuaSymbol.SHAN_ZE_SUN: (HexagramType.GEN, HexagramType.DUI),
            GuaSymbol.FENG_LEI_YI: (HexagramType.XUN, HexagramType.ZHEN),
            GuaSymbol.ZE_TIAN_GUAI: (HexagramType.DUI, HexagramType.QIAN),
            GuaSymbol.TIAN_FENG_GOU: (HexagramType.QIAN, HexagramType.XUN),
            GuaSymbol.ZE_DI_CUI: (HexagramType.DUI, HexagramType.KUN),
            GuaSymbol.DI_FENG_SHENG: (HexagramType.KUN, HexagramType.XUN),
            GuaSymbol.ZE_SHUI_KUN: (HexagramType.DUI, HexagramType.KAN),
            GuaSymbol.SHUI_FENG_JING: (HexagramType.KAN, HexagramType.XUN),
            GuaSymbol.ZE_HUO_GE: (HexagramType.DUI, HexagramType.LI),
            GuaSymbol.HUO_FENG_DING: (HexagramType.LI, HexagramType.XUN),
            GuaSymbol.ZHEN_ZHEN: (HexagramType.ZHEN, HexagramType.ZHEN),
            GuaSymbol.GEN_GEN: (HexagramType.GEN, HexagramType.GEN),
            GuaSymbol.FENG_SHAN_JIAN: (HexagramType.XUN, HexagramType.GEN),
            GuaSymbol.LEI_ZE_GUI_MEI: (HexagramType.ZHEN, HexagramType.DUI),
            GuaSymbol.LEI_HUO_FENG: (HexagramType.ZHEN, HexagramType.LI),
            GuaSymbol.HUO_SHAN_LV: (HexagramType.LI, HexagramType.GEN),
            GuaSymbol.XUN_XUN: (HexagramType.XUN, HexagramType.XUN),
            GuaSymbol.DUI_DUI: (HexagramType.DUI, HexagramType.DUI),
            GuaSymbol.FENG_SHUI_HUAN: (HexagramType.XUN, HexagramType.KAN),
            GuaSymbol.SHUI_ZE_JIE: (HexagramType.KAN, HexagramType.DUI),
            GuaSymbol.FENG_ZE_ZHONG_FU: (HexagramType.XUN, HexagramType.DUI),
            GuaSymbol.LEI_SHAN_XIAO_GUO: (HexagramType.ZHEN, HexagramType.GEN),
            GuaSymbol.SHUI_HUO_JI_JI: (HexagramType.KAN, HexagramType.LI),
            GuaSymbol.HUO_SHUI_WEI_JI: (HexagramType.LI, HexagramType.KAN),
        }
        return gua_trigram_map.get(self.gua_symbol, (HexagramType.QIAN, HexagramType.QIAN))

    def _calculate_default_yao(self) -> List[int]:
        return [0, 0, 0, 0, 0, 0]

    def get_ganzhi_mapping(self) -> Tuple[TianganType, DizhiType]:
        tiangan_list = list(TianganType)
        dizhi_list = list(DizhiType)
        cycle_pos = (self.image_number - 1) % 60
        tiangan_idx = cycle_pos % 10
        dizhi_idx = cycle_pos % 12
        return tiangan_list[tiangan_idx], dizhi_list[dizhi_idx]

    def get_wuxing_energy(self) -> Dict[WuxingType, float]:
        energy = {w: 0.5 for w in WuxingType}
        energy[self.wuxing_attribution] = 1.0
        tiangan, dizhi = self.get_ganzhi_mapping()
        tiangan_wuxing = self._get_tiangan_wuxing(tiangan)
        dizhi_wuxing = self._get_dizhi_wuxing(dizhi)
        energy[tiangan_wuxing] += 0.3
        energy[dizhi_wuxing] += 0.3
        return energy

    def _get_tiangan_wuxing(self, tiangan: TianganType) -> WuxingType:
        mapping = {
            TianganType.JIA: WuxingType.WOOD,
            TianganType.YI: WuxingType.WOOD,
            TianganType.BING: WuxingType.FIRE,
            TianganType.DING: WuxingType.FIRE,
            TianganType.WU: WuxingType.EARTH,
            TianganType.JI: WuxingType.EARTH,
            TianganType.GENG: WuxingType.METAL,
            TianganType.XIN: WuxingType.METAL,
            TianganType.REN: WuxingType.WATER,
            TianganType.GUI: WuxingType.WATER,
        }
        return mapping.get(tiangan, WuxingType.EARTH)

    def _get_dizhi_wuxing(self, dizhi: DizhiType) -> WuxingType:
        mapping = {
            DizhiType.YIN: WuxingType.WOOD,
            DizhiType.MAO: WuxingType.WOOD,
            DizhiType.SI: WuxingType.FIRE,
            DizhiType.WU: WuxingType.FIRE,
            DizhiType.CHEN: WuxingType.EARTH,
            DizhiType.XU: WuxingType.EARTH,
            DizhiType.CHOU: WuxingType.EARTH,
            DizhiType.WEI: WuxingType.EARTH,
            DizhiType.SHEN: WuxingType.METAL,
            DizhiType.YOU: WuxingType.METAL,
            DizhiType.HAI: WuxingType.WATER,
            DizhiType.ZI: WuxingType.WATER,
        }
        return mapping.get(dizhi, WuxingType.EARTH)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'image_number': self.image_number,
            'gua_symbol': self.gua_symbol.value,
            'chen_yu': self.chen_yu,
            'song_yue': self.song_yue,
            'wuxing_attribution': self.wuxing_attribution.value,
            'time_hint': self.time_hint.to_dict(),
            'upper_trigram': self.upper_trigram.value,
            'lower_trigram': self.lower_trigram.value,
            'yao_positions': self.yao_positions,
            'interpretation': self.interpretation,
            'historical_events': self.historical_events,
            'metadata': self.metadata,
        }


@dataclass
class PredictionResult:
    """预测结果 - Prediction result"""
    predicted_image: TuibeituImage
    confidence: float
    evolution_direction: EvolutionDirection
    wuxing_factors: Dict[WuxingType, float]
    time_projection: Optional[str] = None
    alternative_predictions: List[Tuple['TuibeituImage', float]] = field(default_factory=list)
    reasoning: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'predicted_image': self.predicted_image.to_dict(),
            'confidence': self.confidence,
            'evolution_direction': self.evolution_direction.value,
            'wuxing_factors': {k.value: v for k, v in self.wuxing_factors.items()},
            'time_projection': self.time_projection,
            'alternative_predictions': [
                {'image': img.to_dict(), 'probability': prob}
                for img, prob in self.alternative_predictions
            ],
            'reasoning': self.reasoning,
            'metadata': self.metadata,
        }


@dataclass
class SequenceAnalysis:
    """序列分析结果 - Sequence analysis result"""
    sequence: List[TuibeituImage]
    trend_direction: str
    dominant_wuxing: WuxingType
    wuxing_distribution: Dict[WuxingType, float]
    cycle_position: int
    evolution_pattern: str
    stability_score: float
    predictions: List[PredictionResult] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'sequence': [img.to_dict() for img in self.sequence],
            'trend_direction': self.trend_direction,
            'dominant_wuxing': self.dominant_wuxing.value,
            'wuxing_distribution': {k.value: v for k, v in self.wuxing_distribution.items()},
            'cycle_position': self.cycle_position,
            'evolution_pattern': self.evolution_pattern,
            'stability_score': self.stability_score,
            'predictions': [p.to_dict() for p in self.predictions],
            'insights': self.insights,
            'metadata': self.metadata,
        }


class SequenceEvolver:
    """
    序列演化器 - Sequence Evolver
    
    基于五行生克的演化算法，实现推背图序列的演化预测
    """

    WUXING_GENERATION = {
        WuxingType.WOOD: WuxingType.FIRE,
        WuxingType.FIRE: WuxingType.EARTH,
        WuxingType.EARTH: WuxingType.METAL,
        WuxingType.METAL: WuxingType.WATER,
        WuxingType.WATER: WuxingType.WOOD,
    }

    WUXING_RESTRICTION = {
        WuxingType.WOOD: WuxingType.EARTH,
        WuxingType.EARTH: WuxingType.WATER,
        WuxingType.WATER: WuxingType.FIRE,
        WuxingType.FIRE: WuxingType.METAL,
        WuxingType.METAL: WuxingType.WOOD,
    }

    HEXAGRAM_WUXING = {
        HexagramType.QIAN: WuxingType.METAL,
        HexagramType.KUN: WuxingType.EARTH,
        HexagramType.ZHEN: WuxingType.WOOD,
        HexagramType.XUN: WuxingType.WOOD,
        HexagramType.KAN: WuxingType.WATER,
        HexagramType.LI: WuxingType.FIRE,
        HexagramType.GEN: WuxingType.EARTH,
        HexagramType.DUI: WuxingType.METAL,
    }

    TRADITIONAL_EVOLUTION = {
        HexagramType.QIAN: HexagramType.DUI,
        HexagramType.DUI: HexagramType.LI,
        HexagramType.LI: HexagramType.ZHEN,
        HexagramType.ZHEN: HexagramType.XUN,
        HexagramType.XUN: HexagramType.KAN,
        HexagramType.KAN: HexagramType.GEN,
        HexagramType.GEN: HexagramType.KUN,
        HexagramType.KUN: HexagramType.QIAN,
    }

    def __init__(self):
        self.evolution_history: List[Dict[str, Any]] = []
        self.transition_matrix: Dict[GuaSymbol, Dict[GuaSymbol, float]] = {}
        self._initialize_transition_matrix()

    def _initialize_transition_matrix(self):
        for gua in GuaSymbol:
            self.transition_matrix[gua] = {}
            for target_gua in GuaSymbol:
                self.transition_matrix[gua][target_gua] = 1.0 / 64

    def evolve_by_wuxing(
        self,
        current_image: TuibeituImage,
        direction: EvolutionDirection = EvolutionDirection.SHUN
    ) -> List[Tuple[GuaSymbol, float]]:
        """
        基于五行生克演化
        
        Args:
            current_image: 当前象
            direction: 演化方向
            
        Returns:
            可能的下一象列表及其概率
        """
        current_wuxing = current_image.wuxing_attribution
        candidates = []

        if direction == EvolutionDirection.SHENG:
            target_wuxing = self.WUXING_GENERATION[current_wuxing]
            candidates = self._find_gua_by_wuxing(target_wuxing)
        elif direction == EvolutionDirection.KE:
            target_wuxing = self.WUXING_RESTRICTION[current_wuxing]
            candidates = self._find_gua_by_wuxing(target_wuxing)
        elif direction == EvolutionDirection.SHUN:
            next_wuxing = self.WUXING_GENERATION[current_wuxing]
            candidates = self._find_gua_by_wuxing(next_wuxing)
        elif direction == EvolutionDirection.NI:
            prev_wuxing = self._get_generator(current_wuxing)
            candidates = self._find_gua_by_wuxing(prev_wuxing)
        else:
            candidates = [(gua, 1.0 / 64) for gua in GuaSymbol]

        return sorted(candidates, key=lambda x: x[1], reverse=True)[:5]

    def _find_gua_by_wuxing(self, wuxing: WuxingType) -> List[Tuple[GuaSymbol, float]]:
        gua_wuxing_map = {
            GuaSymbol.QIAN_QIAN: WuxingType.METAL,
            GuaSymbol.KUN_KUN: WuxingType.EARTH,
            GuaSymbol.KAN_KAN: WuxingType.WATER,
            GuaSymbol.LI_LI: WuxingType.FIRE,
            GuaSymbol.ZHEN_ZHEN: WuxingType.WOOD,
            GuaSymbol.XUN_XUN: WuxingType.WOOD,
            GuaSymbol.GEN_GEN: WuxingType.EARTH,
            GuaSymbol.DUI_DUI: WuxingType.METAL,
        }
        candidates = []
        for gua, gua_wuxing in gua_wuxing_map.items():
            if gua_wuxing == wuxing:
                candidates.append((gua, 0.8))
            else:
                relation = self._get_wuxing_relation(gua_wuxing, wuxing)
                if relation == WuxingRelation.GENERATE:
                    candidates.append((gua, 0.5))
                elif relation == WuxingRelation.SAME_NATURE:
                    candidates.append((gua, 0.3))
        return candidates

    def _get_wuxing_relation(self, source: WuxingType, target: WuxingType) -> WuxingRelation:
        if self.WUXING_GENERATION.get(source) == target:
            return WuxingRelation.GENERATE
        if self.WUXING_RESTRICTION.get(source) == target:
            return WuxingRelation.RESTRICT
        return WuxingRelation.SAME_NATURE

    def _get_generator(self, wuxing: WuxingType) -> WuxingType:
        for source, target in self.WUXING_GENERATION.items():
            if target == wuxing:
                return source
        return WuxingType.EARTH

    def evolve_by_gua_transform(
        self,
        current_image: TuibeituImage,
        yao_change: Optional[int] = None
    ) -> List[Tuple[GuaSymbol, float]]:
        """
        基于卦象变换规则演化
        
        易经变卦规则：爻变则卦变
        
        Args:
            current_image: 当前象
            yao_change: 变爻位置（0-5），None则自动选择
            
        Returns:
            可能的下一象列表及其概率
        """
        upper = current_image.upper_trigram
        lower = current_image.lower_trigram

        candidates = []

        new_upper = self.TRADITIONAL_EVOLUTION.get(upper, upper)
        new_lower = self.TRADITIONAL_EVOLUTION.get(lower, lower)

        target_gua = self._find_gua_by_trigrams(new_upper, new_lower)
        if target_gua:
            candidates.append((target_gua, 0.6))

        for gua in GuaSymbol:
            if gua != target_gua:
                candidates.append((gua, 0.4 / 63))

        return sorted(candidates, key=lambda x: x[1], reverse=True)[:5]

    def _find_gua_by_trigrams(
        self,
        upper: HexagramType,
        lower: HexagramType
    ) -> Optional[GuaSymbol]:
        trigram_gua_map = {
            (HexagramType.QIAN, HexagramType.QIAN): GuaSymbol.QIAN_QIAN,
            (HexagramType.KUN, HexagramType.KUN): GuaSymbol.KUN_KUN,
            (HexagramType.KAN, HexagramType.KAN): GuaSymbol.KAN_KAN,
            (HexagramType.LI, HexagramType.LI): GuaSymbol.LI_LI,
            (HexagramType.ZHEN, HexagramType.ZHEN): GuaSymbol.ZHEN_ZHEN,
            (HexagramType.XUN, HexagramType.XUN): GuaSymbol.XUN_XUN,
            (HexagramType.GEN, HexagramType.GEN): GuaSymbol.GEN_GEN,
            (HexagramType.DUI, HexagramType.DUI): GuaSymbol.DUI_DUI,
        }
        return trigram_gua_map.get((upper, lower))

    def evolve_by_ganzhi_cycle(
        self,
        current_image: TuibeituImage,
        steps: int = 1
    ) -> List[Tuple[int, float]]:
        """
        基于干支周期推演
        
        六十象对应六十甲子周期
        
        Args:
            current_image: 当前象
            steps: 推演步数
            
        Returns:
            可能的下一象序号列表及其概率
        """
        current_pos = current_image.image_number
        candidates = []

        next_pos = ((current_pos - 1 + steps) % 60) + 1
        candidates.append((next_pos, 0.7))

        for offset in [2, 3, 5, 10]:
            alt_pos = ((current_pos - 1 + offset) % 60) + 1
            candidates.append((alt_pos, 0.3 / offset))

        return sorted(candidates, key=lambda x: x[1], reverse=True)[:5]

    def calculate_evolution_probability(
        self,
        from_image: TuibeituImage,
        to_image: TuibeituImage
    ) -> float:
        """
        计算两象之间的演化概率
        
        Args:
            from_image: 起始象
            to_image: 目标象
            
        Returns:
            演化概率（0.0-1.0）
        """
        probability = 0.0

        wuxing_from = from_image.wuxing_attribution
        wuxing_to = to_image.wuxing_attribution

        if self.WUXING_GENERATION.get(wuxing_from) == wuxing_to:
            probability += 0.4
        elif self.WUXING_RESTRICTION.get(wuxing_from) == wuxing_to:
            probability += 0.2
        elif wuxing_from == wuxing_to:
            probability += 0.3

        upper_from = from_image.upper_trigram
        upper_to = to_image.upper_trigram
        if self.TRADITIONAL_EVOLUTION.get(upper_from) == upper_to:
            probability += 0.3

        pos_diff = abs(to_image.image_number - from_image.image_number)
        if pos_diff <= 5:
            probability += 0.2 * (1 - pos_diff / 5)

        return min(1.0, probability)

    def record_evolution(self, evolution_record: Dict[str, Any]):
        """记录演化历史"""
        self.evolution_history.append(evolution_record)
        if len(self.evolution_history) > 1000:
            self.evolution_history = self.evolution_history[-1000:]

    def get_evolution_patterns(self) -> List[Dict[str, Any]]:
        """获取演化模式统计"""
        patterns = {}
        for record in self.evolution_history:
            key = f"{record.get('from_wuxing', '')}->{record.get('to_wuxing', '')}"
            patterns[key] = patterns.get(key, 0) + 1

        return [
            {'pattern': k, 'count': v}
            for k, v in sorted(patterns.items(), key=lambda x: x[1], reverse=True)
        ]


class TuibeituPredictor:
    """
    推背图预测器 - Tuibeitu Predictor
    
    整合五行生克、卦象变换、干支周期的综合预测系统
    """

    TUIBEITU_DATA: Dict[int, Dict[str, Any]] = {}

    def __init__(self):
        self.evolver = SequenceEvolver()
        self.prediction_history: List[PredictionResult] = []
        self._initialize_tuibeitu_data()

    def _initialize_tuibeitu_data(self):
        """初始化推背图基础数据"""
        tiangan_list = list(TianganType)
        dizhi_list = list(DizhiType)
        gua_list = list(GuaSymbol)
        wuxing_cycle = [
            WuxingType.WOOD, WuxingType.WOOD,
            WuxingType.FIRE, WuxingType.FIRE,
            WuxingType.EARTH, WuxingType.EARTH,
            WuxingType.METAL, WuxingType.METAL,
            WuxingType.WATER, WuxingType.WATER,
        ]

        for i in range(1, 61):
            cycle_pos = (i - 1) % 60
            tiangan_idx = cycle_pos % 10
            dizhi_idx = cycle_pos % 12
            gua_idx = (i - 1) % 64

            self.TUIBEITU_DATA[i] = {
                'image_number': i,
                'tiangan': tiangan_list[tiangan_idx],
                'dizhi': dizhi_list[dizhi_idx],
                'gua_symbol': gua_list[gua_idx],
                'wuxing': wuxing_cycle[tiangan_idx],
            }

    def predict_next(
        self,
        current_state: TuibeituImage,
        context: Optional[Dict[str, Any]] = None
    ) -> PredictionResult:
        """
        预测下一状态
        
        Args:
            current_state: 当前象状态
            context: 额外上下文信息
            
        Returns:
            预测结果
        """
        wuxing_candidates = self.evolver.evolve_by_wuxing(current_state)
        gua_candidates = self.evolver.evolve_by_gua_transform(current_state)
        ganzhi_candidates = self.evolver.evolve_by_ganzhi_cycle(current_state)

        combined_scores: Dict[int, float] = {}

        for gua, prob in wuxing_candidates:
            img_num = self._get_image_number_from_gua(gua)
            combined_scores[img_num] = combined_scores.get(img_num, 0) + prob * 0.4

        for gua, prob in gua_candidates:
            img_num = self._get_image_number_from_gua(gua)
            combined_scores[img_num] = combined_scores.get(img_num, 0) + prob * 0.35

        for img_num, prob in ganzhi_candidates:
            combined_scores[img_num] = combined_scores.get(img_num, 0) + prob * 0.25

        if context:
            combined_scores = self._apply_context(combined_scores, context)

        sorted_predictions = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

        if not sorted_predictions:
            next_num = (current_state.image_number % 60) + 1
            sorted_predictions = [(next_num, 0.5)]

        predicted_num = sorted_predictions[0][0]
        predicted_image = self._create_image_from_number(predicted_num)

        confidence = min(1.0, sorted_predictions[0][1])
        evolution_direction = self._determine_evolution_direction(
            current_state, predicted_image
        )

        result = PredictionResult(
            predicted_image=predicted_image,
            confidence=confidence,
            evolution_direction=evolution_direction,
            wuxing_factors=predicted_image.get_wuxing_energy(),
            time_projection=self._project_time(predicted_num),
            alternative_predictions=[
                (self._create_image_from_number(num), prob)
                for num, prob in sorted_predictions[1:4]
            ],
            reasoning=self._generate_reasoning(current_state, predicted_image, confidence),
        )

        self.prediction_history.append(result)
        return result

    def _get_image_number_from_gua(self, gua: GuaSymbol) -> int:
        gua_list = list(GuaSymbol)
        idx = gua_list.index(gua)
        return (idx % 60) + 1

    def _apply_context(
        self,
        scores: Dict[int, float],
        context: Dict[str, Any]
    ) -> Dict[int, float]:
        if 'preferred_wuxing' in context:
            preferred = context['preferred_wuxing']
            for img_num in scores:
                img_data = self.TUIBEITU_DATA.get(img_num, {})
                if img_data.get('wuxing') == preferred:
                    scores[img_num] *= 1.3

        if 'time_hint' in context:
            pass

        return scores

    def _create_image_from_number(self, image_number: int) -> TuibeituImage:
        data = self.TUIBEITU_DATA.get(image_number, self.TUIBEITU_DATA[1])

        return TuibeituImage(
            image_number=image_number,
            gua_symbol=data['gua_symbol'],
            chen_yu=f"第{image_number}象谶语",
            song_yue=f"第{image_number}象颂曰",
            wuxing_attribution=data['wuxing'],
            time_hint=TimeHint(ganzhi_cycle=f"{data['tiangan'].value}{data['dizhi'].value}"),
        )

    def _determine_evolution_direction(
        self,
        from_image: TuibeituImage,
        to_image: TuibeituImage
    ) -> EvolutionDirection:
        from_wuxing = from_image.wuxing_attribution
        to_wuxing = to_image.wuxing_attribution

        if SequenceEvolver.WUXING_GENERATION.get(from_wuxing) == to_wuxing:
            return EvolutionDirection.SHENG
        elif SequenceEvolver.WUXING_RESTRICTION.get(from_wuxing) == to_wuxing:
            return EvolutionDirection.KE
        elif from_wuxing == to_wuxing:
            return EvolutionDirection.CHENG
        else:
            return EvolutionDirection.HUA

    def _project_time(self, image_number: int) -> str:
        data = self.TUIBEITU_DATA.get(image_number, {})
        tiangan = data.get('tiangan', TianganType.JIA)
        dizhi = data.get('dizhi', DizhiType.ZI)
        return f"干支周期: {tiangan.value}{dizhi.value}年"

    def _generate_reasoning(
        self,
        from_image: TuibeituImage,
        to_image: TuibeituImage,
        confidence: float
    ) -> str:
        direction = self._determine_evolution_direction(from_image, to_image)
        from_wuxing = from_image.wuxing_attribution.value
        to_wuxing = to_image.wuxing_attribution.value

        reasoning = f"从第{from_image.image_number}象演化至第{to_image.image_number}象，"
        reasoning += f"五行由{from_wuxing}{direction.value}至{to_wuxing}，"
        reasoning += f"置信度{confidence:.1%}。"

        return reasoning

    def analyze_sequence(
        self,
        sequence: List[TuibeituImage]
    ) -> SequenceAnalysis:
        """
        分析序列趋势
        
        Args:
            sequence: 象序列列表
            
        Returns:
            序列分析结果
        """
        if not sequence:
            raise ValueError("序列不能为空")

        wuxing_distribution = self._calculate_wuxing_distribution(sequence)
        dominant_wuxing = max(wuxing_distribution.items(), key=lambda x: x[1])[0]

        trend_direction = self._analyze_trend(sequence)
        evolution_pattern = self._identify_evolution_pattern(sequence)
        stability_score = self._calculate_stability(sequence)

        predictions = []
        if len(sequence) >= 1:
            last_image = sequence[-1]
            for _ in range(3):
                pred = self.predict_next(last_image)
                predictions.append(pred)
                last_image = pred.predicted_image

        insights = self._generate_insights(
            sequence, dominant_wuxing, trend_direction, stability_score
        )

        return SequenceAnalysis(
            sequence=sequence,
            trend_direction=trend_direction,
            dominant_wuxing=dominant_wuxing,
            wuxing_distribution=wuxing_distribution,
            cycle_position=sequence[-1].image_number,
            evolution_pattern=evolution_pattern,
            stability_score=stability_score,
            predictions=predictions,
            insights=insights,
        )

    def _calculate_wuxing_distribution(
        self,
        sequence: List[TuibeituImage]
    ) -> Dict[WuxingType, float]:
        distribution = {w: 0.0 for w in WuxingType}
        for image in sequence:
            distribution[image.wuxing_attribution] += 1.0

        total = len(sequence)
        if total > 0:
            for wuxing in distribution:
                distribution[wuxing] /= total

        return distribution

    def _analyze_trend(self, sequence: List[TuibeituImage]) -> str:
        if len(sequence) < 2:
            return "稳定"

        trends = []
        for i in range(1, len(sequence)):
            prev_wuxing = sequence[i-1].wuxing_attribution
            curr_wuxing = sequence[i].wuxing_attribution

            if SequenceEvolver.WUXING_GENERATION.get(prev_wuxing) == curr_wuxing:
                trends.append("相生")
            elif SequenceEvolver.WUXING_RESTRICTION.get(prev_wuxing) == curr_wuxing:
                trends.append("相克")
            else:
                trends.append("平稳")

        sheng_count = trends.count("相生")
        ke_count = trends.count("相克")

        if sheng_count > ke_count * 2:
            return "上升"
        elif ke_count > sheng_count * 2:
            return "下降"
        else:
            return "波动"

    def _identify_evolution_pattern(self, sequence: List[TuibeituImage]) -> str:
        if len(sequence) < 3:
            return "数据不足"

        wuxing_sequence = [img.wuxing_attribution for img in sequence]

        is_generation_chain = True
        for i in range(1, len(wuxing_sequence)):
            if SequenceEvolver.WUXING_GENERATION.get(wuxing_sequence[i-1]) != wuxing_sequence[i]:
                is_generation_chain = False
                break

        if is_generation_chain:
            return "五行相生链"

        is_restriction_chain = True
        for i in range(1, len(wuxing_sequence)):
            if SequenceEvolver.WUXING_RESTRICTION.get(wuxing_sequence[i-1]) != wuxing_sequence[i]:
                is_restriction_chain = False
                break

        if is_restriction_chain:
            return "五行相克链"

        unique_wuxing = set(wuxing_sequence)
        if len(unique_wuxing) == 1:
            return "五行专一"

        if len(unique_wuxing) >= 4:
            return "五行流转"

        return "混合演化"

    def _calculate_stability(self, sequence: List[TuibeituImage]) -> float:
        if len(sequence) < 2:
            return 1.0

        changes = 0
        for i in range(1, len(sequence)):
            if sequence[i].wuxing_attribution != sequence[i-1].wuxing_attribution:
                changes += 1

        stability = 1.0 - (changes / (len(sequence) - 1))
        return stability

    def _generate_insights(
        self,
        sequence: List[TuibeituImage],
        dominant_wuxing: WuxingType,
        trend: str,
        stability: float
    ) -> List[str]:
        insights = []

        wuxing_meanings = {
            WuxingType.WOOD: "生发之气，主创新与成长",
            WuxingType.FIRE: "光明之气，主热情与变革",
            WuxingType.EARTH: "承载之气，主稳定与积累",
            WuxingType.METAL: "收敛之气，主决断与变革",
            WuxingType.WATER: "流动之气，主智慧与变通",
        }

        insights.append(f"序列以{dominant_wuxing.value}为主，{wuxing_meanings[dominant_wuxing]}")

        if trend == "上升":
            insights.append("趋势向上发展，宜积极进取")
        elif trend == "下降":
            insights.append("趋势向下调整，宜守成待时")
        else:
            insights.append("趋势波动不定，宜审时度势")

        if stability > 0.8:
            insights.append("序列稳定，变化平缓")
        elif stability < 0.3:
            insights.append("序列动荡，变化剧烈")

        return insights

    def interpret_image(self, image_number: int) -> Dict[str, Any]:
        """
        解读特定象
        
        Args:
            image_number: 象序（1-60）
            
        Returns:
            解读结果
        """
        if not 1 <= image_number <= 60:
            raise ValueError(f"象序必须在1-60之间，当前: {image_number}")

        data = self.TUIBEITU_DATA.get(image_number)
        if not data:
            return {'error': f'未找到第{image_number}象数据'}

        image = self._create_image_from_number(image_number)
        wuxing_energy = image.get_wuxing_energy()
        tiangan, dizhi = image.get_ganzhi_mapping()

        interpretation = {
            'image_number': image_number,
            'gua_symbol': data['gua_symbol'].value,
            'ganzhi': f"{tiangan.value}{dizhi.value}",
            'wuxing': data['wuxing'].value,
            'wuxing_energy': {k.value: v for k, v in wuxing_energy.items()},
            'upper_trigram': image.upper_trigram.value,
            'lower_trigram': image.lower_trigram.value,
            'interpretation': self._interpret_gua(data['gua_symbol']),
            'time_meaning': self._interpret_ganzhi(tiangan, dizhi),
            'wuxing_meaning': self._interpret_wuxing(data['wuxing']),
        }

        return interpretation

    def _interpret_gua(self, gua: GuaSymbol) -> str:
        gua_interpretations = {
            GuaSymbol.QIAN_QIAN: "乾为天，刚健中正，自强不息",
            GuaSymbol.KUN_KUN: "坤为地，厚德载物，柔顺包容",
            GuaSymbol.KAN_KAN: "坎为水，险阻重重，需谨慎前行",
            GuaSymbol.LI_LI: "离为火，光明照耀，依附正道",
            GuaSymbol.ZHEN_ZHEN: "震为雷，震动变革，惊醒世人",
            GuaSymbol.XUN_XUN: "巽为风，柔顺渗透，顺势而为",
            GuaSymbol.GEN_GEN: "艮为山，静止安稳，知止而后定",
            GuaSymbol.DUI_DUI: "兑为泽，喜悦和谐，沟通顺畅",
        }
        return gua_interpretations.get(gua, f"{gua.value}，需结合具体情境解读")

    def _interpret_ganzhi(self, tiangan: TianganType, dizhi: DizhiType) -> str:
        tiangan_meanings = {
            TianganType.JIA: "甲为阳木，主生发",
            TianganType.YI: "乙为阴木，主柔顺",
            TianganType.BING: "丙为阳火，主光明",
            TianganType.DING: "丁为阴火，主温暖",
            TianganType.WU: "戊为阳土，主厚重",
            TianganType.JI: "己为阴土，主承载",
            TianganType.GENG: "庚为阳金，主刚决",
            TianganType.XIN: "辛为阴金，主精细",
            TianganType.REN: "壬为阳水，主智慧",
            TianganType.GUI: "癸为阴水，主润泽",
        }

        dizhi_meanings = {
            DizhiType.ZI: "子水，万物始生",
            DizhiType.CHOU: "丑土，蓄势待发",
            DizhiType.YIN: "寅木，生机勃发",
            DizhiType.MAO: "卯木，万物生长",
            DizhiType.CHEN: "辰土，承上启下",
            DizhiType.SI: "巳火，阳气渐盛",
            DizhiType.WU: "午火，阳气极盛",
            DizhiType.WEI: "未土，收敛蓄积",
            DizhiType.SHEN: "申金，肃杀之气",
            DizhiType.YOU: "酉金，收敛成熟",
            DizhiType.XU: "戌土，归藏之意",
            DizhiType.HAI: "亥水，万物归藏",
        }

        return f"{tiangan_meanings.get(tiangan, '')}，{dizhi_meanings.get(dizhi, '')}"

    def _interpret_wuxing(self, wuxing: WuxingType) -> str:
        interpretations = {
            WuxingType.WOOD: "木主仁，代表生发、创新、成长，宜开拓进取",
            WuxingType.FIRE: "火主礼，代表光明、热情、变革，宜积极行动",
            WuxingType.EARTH: "土主信，代表稳定、承载、积累，宜守成待时",
            WuxingType.METAL: "金主义，代表决断、收敛、变革，宜果断决策",
            WuxingType.WATER: "水主智，代表智慧、流动、变通，宜审时度势",
        }
        return interpretations.get(wuxing, "五行属性待解读")

    def get_prediction_statistics(self) -> Dict[str, Any]:
        """获取预测统计信息"""
        if not self.prediction_history:
            return {'total_predictions': 0}

        wuxing_distribution = {w: 0 for w in WuxingType}
        direction_distribution = {d: 0 for d in EvolutionDirection}
        total_confidence = 0.0

        for pred in self.prediction_history:
            wuxing_distribution[pred.predicted_image.wuxing_attribution] += 1
            direction_distribution[pred.evolution_direction] += 1
            total_confidence += pred.confidence

        return {
            'total_predictions': len(self.prediction_history),
            'average_confidence': total_confidence / len(self.prediction_history),
            'wuxing_distribution': {k.value: v for k, v in wuxing_distribution.items()},
            'direction_distribution': {k.value: v for k, v in direction_distribution.items()},
        }

    def clear_history(self):
        """清除预测历史"""
        self.prediction_history = []
        self.evolver.evolution_history = []
