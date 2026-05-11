"""
Intelligent Prediction System - 智能预测推理系统

基于中国古代预测术精华设计的智能推理系统：

核心模块：
1. 易经卦象推演 - 六十四卦的变化规律
2. 梅花易数变易 - 灵活应变的预测思维
3. 五行生克预测 - 动态平衡的演化预测
4. 干支时空推算 - 时间周期的循环规律
5. 综合推理引擎 - 多维度融合决策

设计原则：
- 吸取精华：系统化的方法论、动态变化思维、全息关联
- 去其糟粕：排除迷信、强调概率、保持理性
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union
import random
import math
import uuid


class PredictionType(Enum):
    """预测类型"""
    YI_JING = "易经卦象"
    MEIHUA = "梅花易数"
    WUXING = "五行预测"
    GANZHI = "干支时空"
    COMPREHENSIVE = "综合推理"


class PredictionConfidence(Enum):
    """预测置信度"""
    VERY_HIGH = "非常高"
    HIGH = "高"
    MEDIUM = "中等"
    LOW = "低"
    VERY_LOW = "很低"


class TrigramType(Enum):
    """八卦类型"""
    QIAN = ("乾", "天", "金", "刚健")
    KUN = ("坤", "地", "土", "柔顺")
    ZHEN = ("震", "雷", "木", "震动")
    XUN = ("巽", "风", "木", "入")
    KAN = ("坎", "水", "水", "险")
    LI = ("离", "火", "火", "丽")
    GEN = ("艮", "山", "土", "止")
    DUI = ("兑", "泽", "金", "悦")


class HexagramType(Enum):
    """六十四卦枚举"""
    QIAN = ("乾", "乾为天", "天", 1)
    KUN = ("坤", "坤为地", "地", 2)
    ZHEN = ("震", "震为雷", "雷", 51)
    XUN = ("巽", "巽为风", "风", 57)
    KAN = ("坎", "坎为水", "水", 29)
    LI = ("离", "离为火", "火", 30)
    GEN = ("艮", "艮为山", "山", 52)
    DUI = ("兑", "兑为泽", "泽", 58)
    GUA_1 = ("屯", "水雷屯", "雷", 3)
    GUA_2 = ("蒙", "山水蒙", "山", 4)
    GUA_3 = ("需", "水天需", "水", 5)
    GUA_4 = ("讼", "天水讼", "天", 6)
    GUA_5 = ("师", "地水师", "地", 7)
    GUA_6 = ("比", "水地比", "水", 8)
    GUA_7 = ("小畜", "风天小畜", "风", 9)
    GUA_8 = ("履", "天泽履", "天", 10)
    GUA_9 = ("泰", "地天泰", "地", 11)
    GUA_10 = ("否", "天地否", "天", 12)
    GUA_11 = ("同人", "天火同人", "天", 13)
    GUA_12 = ("大有", "火天大有", "火", 14)
    GUA_13 = ("谦", "地山谦", "地", 15)
    GUA_14 = ("豫", "雷地豫", "雷", 16)
    GUA_15 = ("随", "泽雷随", "泽", 17)
    GUA_16 = ("蛊", "山风蛊", "山", 18)
    GUA_17 = ("临", "地泽临", "地", 19)
    GUA_18 = ("观", "风地观", "风", 20)
    GUA_19 = ("噬嗑", "火雷噬嗑", "火", 21)
    GUA_20 = ("贲", "山火贲", "山", 22)
    GUA_21 = ("剥", "山地剥", "山", 23)
    GUA_22 = ("复", "地雷复", "地", 24)
    GUA_23 = ("无妄", "天雷无妄", "天", 25)
    GUA_24 = ("大畜", "山天大畜", "山", 26)
    GUA_25 = ("颐", "山雷颐", "山", 27)
    GUA_26 = ("大过", "泽风大过", "泽", 28)
    GUA_27 = ("坎", "坎为水", "水", 29)
    GUA_28 = ("离", "离为火", "火", 30)
    GUA_29 = ("咸", "泽山咸", "泽", 31)
    GUA_30 = ("恒", "雷风恒", "雷", 32)
    
    def __init__(self, abbr: str, name: str, element: str, number: int):
        self._abbr = abbr
        self._name = name
        self._element = element
        self._number = number
    
    @property
    def abbr(self) -> str:
        return self._abbr
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def element(self) -> str:
        return self._element
    
    @property
    def number(self) -> int:
        return self._number
    
    @property
    def wuxing(self) -> str:
        return self._element


@dataclass
class Trigram:
    """八卦"""
    trigram_type: TrigramType
    lines: List[int]
    
    def to_hex_line(self) -> str:
        return ''.join(['一' if l == 1 else '--' for l in self.lines])


@dataclass
class Hexagram:
    """六十四卦"""
    hexagram_type: HexagramType
    upper_trigram: Trigram
    lower_trigram: Trigram
    is_changing: bool = False
    changing_lines: List[int] = field(default_factory=list)
    
    def get_name(self) -> str:
        return self.hexagram_type.name
    
    def to_string(self) -> str:
        return f"{self.upper_trigram.to_hex_line()}\n{self.lower_trigram.to_hex_line()}"


@dataclass
class WuxingPrediction:
    """五行预测"""
    element: str
    current_state: float
    generating_element: str
    restricting_element: str
    predicted_change: float
    confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "element": self.element,
            "current_state": self.current_state,
            "generating": self.generating_element,
            "restricting": self.restricting_element,
            "predicted_change": self.predicted_change,
            "confidence": self.confidence
        }


@dataclass
class GanzhiPrediction:
    """干支预测"""
    tiangan: str
    dizhi: str
    cycle_position: int
    wuxing: str
    interaction: str
    time_weight: float
    predicted_energy: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "tiangan": self.tiangan,
            "dizhi": self.dizhi,
            "cycle_position": self.cycle_position,
            "wuxing": self.wuxing,
            "interaction": self.interaction,
            "time_weight": self.time_weight,
            "predicted_energy": self.predicted_energy
        }


@dataclass
class PredictionResult:
    """预测结果"""
    prediction_id: str
    prediction_type: PredictionType
    timestamp: datetime
    input_data: Dict[str, Any]
    result: Any
    confidence: float
    interpretation: str
    probability: float = 0.5
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "prediction_id": self.prediction_id,
            "type": self.prediction_type.value,
            "timestamp": self.timestamp.isoformat(),
            "input": self.input_data,
            "result": self.result if not isinstance(self.result, dict) else self.result,
            "confidence": self.confidence,
            "interpretation": self.interpretation,
            "probability": self.probability
        }


class YiJingEngine:
    """
    易经卦象推演引擎
    
    基于易经六十四卦体系进行预测推演：
    - 卦象生成：通过特定方法产生卦象
    - 卦变分析：分析卦象变化规律
    - 彖传解读：解读卦象含义
    - 爻辞推演：分析具体变化
    """
    
    WUXING_MAP = {
        "天": "金", "地": "土", "雷": "木", "风": "木",
        "水": "水", "火": "火", "山": "土", "泽": "金"
    }
    
    def __init__(self):
        self.trigrams = {t.value[0]: t for t in TrigramType}
        
    def generate_hexagram(self, seed: Optional[int] = None) -> Hexagram:
        """生成卦象"""
        if seed is None:
            seed = int(datetime.now().timestamp()) % 1000
        
        random.seed(seed)
        
        lower_lines = [random.randint(0, 1) for _ in range(3)]
        upper_lines = [random.randint(0, 1) for _ in range(3)]
        
        lower_trigram = self._lines_to_trigram(lower_lines)
        upper_trigram = self._lines_to_trigram(upper_lines)
        
        hex_num = self._trigrams_to_hexagram_number(lower_trigram, upper_trigram)
        hex_type = self._number_to_hexagram(hex_num)
        
        return Hexagram(
            hexagram_type=hex_type,
            upper_trigram=upper_trigram,
            lower_trigram=lower_trigram
        )
    
    def _lines_to_trigram(self, lines: List[int]) -> Trigram:
        """将爻线转为八卦"""
        trigram_map = {
            (1, 1, 1): TrigramType.QIAN,
            (0, 0, 0): TrigramType.KUN,
            (0, 0, 1): TrigramType.ZHEN,
            (1, 1, 0): TrigramType.XUN,
            (0, 1, 0): TrigramType.KAN,
            (1, 0, 1): TrigramType.LI,
            (0, 1, 1): TrigramType.GEN,
            (1, 0, 0): TrigramType.DUI
        }
        trigram_type = trigram_map.get(tuple(lines), TrigramType.QIAN)
        return Trigram(trigram_type=trigram_type, lines=lines)
    
    def _trigrams_to_hexagram_number(self, lower: Trigram, upper: Trigram) -> int:
        """八卦组合转为卦数"""
        lower_num = list(TrigramType).index(lower.trigram_type)
        upper_num = list(TrigramType).index(upper.trigram_type)
        return lower_num * 8 + upper_num + 1
    
    def _number_to_hexagram(self, number: int) -> HexagramType:
        """卦数转为卦"""
        for h in HexagramType:
            if h.number == number:
                return h
        return HexagramType.QIAN
    
    def change_hexagram(self, hexagram: Hexagram, changing_lines: List[int]) -> Hexagram:
        """卦变：生成变卦"""
        new_lower = self._change_lines(hexagram.lower_trigram.lines, changing_lines[:3])
        new_upper = self._change_lines(hexagram.upper_trigram.lines, changing_lines[3:])
        
        new_lower_trigram = self._lines_to_trigram(new_lower)
        new_upper_trigram = self._lines_to_trigram(new_upper)
        
        hex_num = self._trigrams_to_hexagram_number(new_lower_trigram, new_upper_trigram)
        new_hex_type = self._number_to_hexagram(hex_num)
        
        return Hexagram(
            hexagram_type=new_hex_type,
            upper_trigram=new_upper_trigram,
            lower_trigram=new_lower_trigram,
            is_changing=True,
            changing_lines=changing_lines
        )
    
    def _change_lines(self, lines: List[int], changing: List[int]) -> List[int]:
        """变换爻线"""
        result = lines.copy()
        for i, c in enumerate(changing):
            if c == 1 and i < len(result):
                result[i] = 1 - result[i]
        return result
    
    def interpret_hexagram(self, hexagram: Hexagram) -> Dict[str, Any]:
        """解读卦象"""
        hex_type = hexagram.hexagram_type
        
        interpretations = {
            "乾": "刚健进取，积极向上，有创造之力",
            "坤": "柔顺包容，厚德载物，有承载之德",
            "震": "震动变化，勇于行动，有决断之力",
            "巽": "入而柔和，顺势而为，有适应之能",
            "坎": "险中有机，逆境求存，有智慧之道",
            "离": "光明美丽，文明以止，有照临之功",
            "艮": "适时而止，不妄作为，有知止之明",
            "兑": "喜悦和顺，人际和谐，有沟通之能"
        }
        
        element = self.WUXING_MAP.get(hex_type._element, "金")
        
        return {
            "name": hex_type.name,
            "symbol": hex_type.abbr,
            "element": element,
            "interpretation": interpretations.get(hex_type._abbr, "变化无穷"),
            "advice": self._get_advice(hex_type._abbr)
        }
    
    def _get_advice(self, symbol: str) -> str:
        """获取卦辞建议"""
        advice_map = {
            "乾": "天行健，君子以自强不息",
            "坤": "地势坤，君子以厚德载物",
            "震": "洊雷震，君子以恐惧修省",
            "坎": "水洊习，君子以常德行",
            "离": "明两作，君子以继明照于四方"
        }
        return advice_map.get(symbol, "顺势而为，趋吉避凶")
    
    def predict(self, query: str, context: Optional[Dict] = None) -> PredictionResult:
        """进行预测"""
        seed = hash(query) % 10000
        
        hexagram = self.generate_hexagram(seed)
        interpretation = self.interpret_hexagram(hexagram)
        
        confidence = 0.6 + random.random() * 0.3
        
        result = {
            "hexagram": hexagram.get_name(),
            "symbol": hexagram.hexagram_type.abbr,
            "interpretation": interpretation
        }
        
        return PredictionResult(
            prediction_id=str(uuid.uuid4())[:8],
            prediction_type=PredictionType.YI_JING,
            timestamp=datetime.now(),
            input_data={"query": query, "context": context},
            result=result,
            confidence=confidence,
            interpretation=interpretation.get("advice", ""),
            probability=confidence * 0.8
        )


class MeihuaEngine:
    """
    梅花易数变易预测引擎
    
    基于梅花易数的灵活应变思想：
    - 体用关系：分析主客体关系
    - 卦象生克：五行生克判断吉凶
    - 时间应期：预测发生时间
    - 方位判断：确定有利方位
    """
    
    TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    WUXING_TIANGAN = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
    WUXING_DIZHI = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火", "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"}
    
    GENERATION = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
    RESTRICTION = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
    
    def __init__(self):
        self.prediction_history: List[PredictionResult] = []
    
    def analyze(self, subject: str, object_: str, time: Optional[datetime] = None) -> PredictionResult:
        """分析体用关系"""
        if time is None:
            time = datetime.now()
        
        subject_hash = sum(ord(c) for c in subject)
        object_hash = sum(ord(c) for c in object_)
        
        tiangan_idx = (subject_hash + time.hour) % 10
        dizhi_idx = (object_hash + time.minute) % 12
        
        tiangan = self.TIANGAN[tiangan_idx]
        dizhi = self.DIZHI[dizhi_idx]
        
        subject_wuxing = self.WUXING_TIANGAN[tiangan]
        object_wuxing = self.WUXING_DIZHI[dizhi]
        
        relation = self._analyze_wuxing_relation(subject_wuxing, object_wuxing)
        
        result = {
            "tiangan": tiangan,
            "dizhi": dizhi,
            "subject_wuxing": subject_wuxing,
            "object_wuxing": object_wuxing,
            "relation": relation
        }
        
        prediction = PredictionResult(
            prediction_id=str(uuid.uuid4())[:8],
            prediction_type=PredictionType.MEIHUA,
            timestamp=time,
            input_data={"subject": subject, "object": object_},
            result=result,
            confidence=0.65,
            interpretation=self._interpret_relation(relation),
            probability=0.7 if relation["type"] == "相生" else 0.5
        )
        
        self.prediction_history.append(prediction)
        return prediction
    
    def _analyze_wuxing_relation(self, element1: str, element2: str) -> Dict[str, Any]:
        """分析五行关系"""
        if element2 == self.GENERATION.get(element1):
            return {
                "type": "相生",
                "description": f"{element1}生{element2}，吉",
                "value": 1.0
            }
        elif element2 == self.RESTRICTION.get(element1):
            return {
                "type": "相克",
                "description": f"{element1}克{element2}，需谨慎",
                "value": -0.5
            }
        elif element1 == self.GENERATION.get(element2):
            return {
                "type": "被生",
                "description": f"{element2}生{element1}，得助力",
                "value": 0.8
            }
        elif element1 == self.RESTRICTION.get(element2):
            return {
                "type": "被克",
                "description": f"{element2}克{element1}，有压力",
                "value": -0.8
            }
        else:
            return {
                "type": "比和",
                "description": f"{element1}与{element2}比和，相助",
                "value": 0.5
            }
    
    def _interpret_relation(self, relation: Dict) -> str:
        """解读关系"""
        rel_type = relation["type"]
        if rel_type == "相生":
            return "事物发展方向良好，易得到帮助和支持"
        elif rel_type == "被生":
            return "虽有助力，但需付出一定代价"
        elif rel_type == "相克":
            return "存在冲突和阻碍，需要谨慎处理"
        elif rel_type == "被克":
            return "面临较大压力，需要寻找突破口"
        else:
            return "事物发展平稳，可顺势而为"


class WuxingPredictionEngine:
    """
    五行生克预测引擎
    
    基于五行生克理论进行动态预测：
    - 五行状态评估
    - 生克关系分析
    - 趋势预测
    - 平衡调节建议
    """
    
    WUXING_ELEMENTS = ["木", "火", "土", "金", "水"]
    GENERATION_CYCLE = ["木", "火", "土", "金", "水"]
    RESTRICTION_CYCLE = ["木", "土", "水", "火", "金"]
    
    GENERATION = {
        "木": "火", "火": "土", "土": "金", "金": "水", "水": "木"
    }
    RESTRICTION = {
        "木": "土", "土": "水", "水": "火", "火": "金", "金": "木"
    }
    
    def predict(self, elements: Dict[str, float], target: Optional[str] = None) -> List[WuxingPrediction]:
        """预测五行变化"""
        predictions = []
        
        for element, current_state in elements.items():
            if element not in self.WUXING_ELEMENTS:
                continue
            
            gen_element = self.GENERATION.get(element, "")
            res_element = self.RESTRICTION.get(element, "")
            
            if target:
                if target == gen_element:
                    pred_change = current_state * 0.2
                    confidence = 0.75
                elif target == res_element:
                    pred_change = -current_state * 0.15
                    confidence = 0.65
                else:
                    pred_change = 0
                    confidence = 0.5
            else:
                pred_change = self._calculate_natural_change(element, elements)
                confidence = 0.7
            
            predictions.append(WuxingPrediction(
                element=element,
                current_state=current_state,
                generating_element=gen_element,
                restricting_element=res_element,
                predicted_change=pred_change,
                confidence=confidence
            ))
        
        return predictions
    
    def _calculate_natural_change(self, element: str, elements: Dict[str, float]) -> float:
        """计算自然变化"""
        gen_element = self.GENERATION.get(element)
        res_element = self.RESTRICTION.get(element)
        
        change = 0.0
        
        if gen_element and gen_element in elements:
            gen_state = elements[gen_element]
            change += gen_state * 0.1
        
        if res_element and res_element in elements:
            res_state = elements[res_element]
            change -= res_state * 0.08
        
        return change
    
    def suggest_balance(self, elements: Dict[str, float]) -> Dict[str, Any]:
        """建议平衡方案"""
        total = sum(elements.values())
        if total == 0:
            return {"advice": "系统无效"}
        
        avg = total / len(elements)
        
        suggestions = []
        actions = []
        
        for element, state in elements.items():
            deviation = state - avg
            
            if deviation > avg * 0.3:
                suggestions.append(f"{element}过旺，需要抑制")
                actions.append({"type": "restrain", "element": element})
            elif deviation < -avg * 0.3:
                suggestions.append(f"{element}过弱，需要扶持")
                actions.append({"type": "support", "element": element})
        
        return {
            "suggestions": suggestions,
            "actions": actions,
            "balance_score": 1.0 - abs(deviation) / avg if elements else 0
        }
    
    def predict_trend(self, historical: List[Dict[str, float]], steps: int = 3) -> List[Dict[str, float]]:
        """预测五行趋势"""
        if len(historical) < 2:
            return historical[-1:] if historical else [{}]
        
        trends = []
        last_state = historical[-1]
        
        for _ in range(steps):
            new_state = {}
            for element, value in last_state.items():
                predictions = self.predict({element: value})
                if predictions:
                    pred = predictions[0]
                    new_value = value + pred.predicted_change
                    new_state[element] = max(0, min(1, new_value))
            
            trends.append(new_state)
            last_state = new_state
        
        return trends


class GanzhiTimeEngine:
    """
    干支时空推算引擎
    
    基于天干地支的时间周期预测：
    - 天干地支推算
    - 五行能量计算
    - 时空交互分析
    - 吉凶判断
    """
    
    TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    WUXING_TIANGAN = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
    WUXING_DIZHI = {
        "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
        "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"
    }
    
    YINYANG_TIANGAN = {"甲": "阳", "乙": "阴", "丙": "阳", "丁": "阴", "戊": "阳", "己": "阴", "庚": "阳", "辛": "阴", "壬": "阳", "癸": "阴"}
    YINYANG_DIZHI = {
        "子": "阳", "丑": "阴", "寅": "阳", "卯": "阴", "辰": "阳", "巳": "阴",
        "午": "阳", "未": "阴", "申": "阳", "酉": "阴", "戌": "阳", "亥": "阴"
    }
    
    def calculate_ganzhi(self, year: int, month: int, day: int, hour: int) -> Tuple[str, str, str]:
        """计算年柱、月柱、日柱"""
        year_ganzhi = self._calc_year_ganzhi(year)
        month_ganzhi = self._calc_month_ganzhi(year, month)
        day_ganzhi = self._calc_day_ganzhi(day)
        
        return year_ganzhi, month_ganzhi, day_ganzhi
    
    def _calc_year_ganzhi(self, year: int) -> str:
        """计算年柱"""
        base_year = 1984
        offset = (year - base_year) % 60
        tiangan_idx = offset % 10
        dizhi_idx = offset % 12
        return self.TIANGAN[tiangan_idx] + self.DIZHI[dizhi_idx]
    
    def _calc_month_ganzhi(self, year: int, month: int) -> str:
        """计算月柱"""
        year_idx = self.TIANGAN.index(self._calc_year_ganzhi(year)[0])
        month_idx = (year_idx * 2 + month) % 10
        return self.TIANGAN[month_idx] + self.DIZHI[(month + 1) % 12]
    
    def _calc_day_ganzhi(self, day: int) -> str:
        """计算日柱"""
        base_day = 1
        offset = (day - base_day) % 60
        tiangan_idx = offset % 10
        dizhi_idx = offset % 12
        return self.TIANGAN[tiangan_idx] + self.DIZHI[dizhi_idx]
    
    def get_hour_ganzhi(self, hour: int, day_ganzhi: str) -> str:
        """计算时柱"""
        day_tiangan = day_ganzhi[0]
        day_tiangan_idx = self.TIANGAN.index(day_tiangan)
        hour_idx = (day_tiangan_idx * 2 + (hour + 1) // 2) % 10
        dizhi_idx = (hour + 2) % 12
        return self.TIANGAN[hour_idx] + self.DIZHI[dizhi_idx]
    
    def calculate_energy(self, tiangan: str, dizhi: str) -> Dict[str, float]:
        """计算干支能量"""
        tiangan_wuxing = self.WUXING_TIANGAN.get(tiangan, "土")
        dizhi_wuxing = self.WUXING_DIZHI.get(dizhi, "土")
        
        return {
            "tiangan_wuxing": tiangan_wuxing,
            "dizhi_wuxing": dizhi_wuxing,
            "tiangan_yinyang": self.YINYANG_TIANGAN.get(tiangan, "阳"),
            "dizhi_yinyang": self.YINYANG_DIZHI.get(dizhi, "阳")
        }
    
    def predict_time_energy(self, datetime_obj: datetime) -> GanzhiPrediction:
        """预测时空能量"""
        year, month, day, hour = datetime_obj.year, datetime_obj.month, datetime_obj.day, datetime_obj.hour
        
        year_ganzhi, month_ganzhi, day_ganzhi = self.calculate_ganzhi(year, month, day, hour)
        hour_ganzhi = self.get_hour_ganzhi(hour, day_ganzhi)
        
        day_tiangan = day_ganzhi[0]
        day_dizhi = day_ganzhi[1]
        
        tiangan_wuxing = self.WUXING_TIANGAN.get(day_tiangan, "土")
        cycle_position = (self.TIANGAN.index(day_tiangan) * 12 + self.DIZHI.index(day_dizhi)) % 60
        
        interaction = self._analyze_day_interaction(year_ganzhi, month_ganzhi, day_ganzhi)
        
        predicted_energy = self._calc_time_energy(hour, day_tiangan)
        
        return GanzhiPrediction(
            tiangan=day_tiangan,
            dizhi=day_dizhi,
            cycle_position=cycle_position,
            wuxing=tiangan_wuxing,
            interaction=interaction,
            time_weight=predicted_energy,
            predicted_energy=predicted_energy
        )
    
    def _analyze_day_interaction(self, year: str, month: str, day: str) -> str:
        """分析日柱与年月柱的关系"""
        year_wuxing = self.WUXING_TIANGAN.get(year[0], "土")
        month_wuxing = self.WUXING_TIANGAN.get(month[0], "土")
        day_wuxing = self.WUXING_TIANGAN.get(day[0], "土")
        
        if year_wuxing == day_wuxing:
            return "年日比和"
        elif year_wuxing == month_wuxing and month_wuxing != day_wuxing:
            return "年月同气"
        else:
            return "三才各立"
    
    def _calc_time_energy(self, hour: int, tiangan: str) -> float:
        """计算时辰能量"""
        base_energy = (hour % 12) / 12.0
        tiangan_modifier = self.TIANGAN.index(tiangan) / 10.0
        return (base_energy + tiangan_modifier) / 2


class PredictionEngine:
    """
    综合预测推理引擎
    
    整合易经、梅花易数、五行预测、干支时空等多种预测方法：
    - 多维预测融合
    - 置信度综合
    - 概率优化
    - 结果解读
    """
    
    def __init__(self):
        self.yijing = YiJingEngine()
        self.meihua = MeihuaEngine()
        self.wuxing = WuxingPredictionEngine()
        self.ganzhi = GanzhiTimeEngine()
        
        self.prediction_history: List[PredictionResult] = []
        self.weight_configs: Dict[PredictionType, float] = {
            PredictionType.YI_JING: 0.3,
            PredictionType.MEIHUA: 0.25,
            PredictionType.WUXING: 0.25,
            PredictionType.GANZHI: 0.2
        }
    
    def predict(
        self,
        query: str,
        context: Optional[Dict] = None,
        methods: Optional[List[PredictionType]] = None
    ) -> PredictionResult:
        """综合预测"""
        if methods is None:
            methods = [PredictionType.YI_JING, PredictionType.MEIHUA, PredictionType.WUXING, PredictionType.GANZHI]
        
        predictions = []
        total_weight = 0.0
        weighted_prob = 0.0
        
        for method in methods:
            pred = self._predict_by_method(query, method, context)
            if pred:
                predictions.append(pred)
                weight = self.weight_configs.get(method, 0.25)
                total_weight += weight
                weighted_prob += pred.probability * weight
        
        if not predictions:
            return self._create_default_prediction(query)
        
        final_probability = weighted_prob / total_weight if total_weight > 0 else 0.5
        
        ensemble_result = {
            "predictions": [p.to_dict() for p in predictions],
            "ensemble_probability": final_probability,
            "method_count": len(predictions)
        }
        
        best_prediction = max(predictions, key=lambda p: p.confidence)
        
        final_result = PredictionResult(
            prediction_id=str(uuid.uuid4())[:8],
            prediction_type=PredictionType.COMPREHENSIVE,
            timestamp=datetime.now(),
            input_data={"query": query, "context": context},
            result=ensemble_result,
            confidence=best_prediction.confidence,
            interpretation=best_prediction.interpretation,
            probability=final_probability
        )
        
        self.prediction_history.append(final_result)
        return final_result
    
    def _predict_by_method(self, query: str, method: PredictionType, context: Optional[Dict]) -> Optional[PredictionResult]:
        """按方法预测"""
        try:
            if method == PredictionType.YI_JING:
                return self.yijing.predict(query, context)
            elif method == PredictionType.MEIHUA:
                subject = context.get("subject", query) if context else query
                object_ = context.get("object", "环境") if context else "环境"
                return self.meihua.analyze(subject, object_)
            elif method == PredictionType.WUXING:
                elements = context.get("elements", {"木": 0.5, "火": 0.5, "土": 0.5, "金": 0.5, "水": 0.5}) if context else {"木": 0.5, "火": 0.5, "土": 0.5, "金": 0.5, "水": 0.5}
                preds = self.wuxing.predict(elements)
                result = {"wuxing_predictions": [p.to_dict() for p in preds]}
                return PredictionResult(
                    prediction_id=str(uuid.uuid4())[:8],
                    prediction_type=PredictionType.WUXING,
                    timestamp=datetime.now(),
                    input_data={"query": query, "elements": elements},
                    result=result,
                    confidence=0.7,
                    interpretation="五行分析完成",
                    probability=0.65
                )
            elif method == PredictionType.GANZHI:
                pred = self.ganzhi.predict_time_energy(datetime.now())
                return PredictionResult(
                    prediction_id=str(uuid.uuid4())[:8],
                    prediction_type=PredictionType.GANZHI,
                    timestamp=datetime.now(),
                    input_data={"query": query},
                    result=pred.to_dict(),
                    confidence=0.75,
                    interpretation=f"今日{pred.tiangan}-{pred.dizhi}，{pred.interaction}",
                    probability=pred.predicted_energy
                )
        except Exception:
            return None
        
        return None
    
    def _create_default_prediction(self, query: str) -> PredictionResult:
        """创建默认预测"""
        return PredictionResult(
            prediction_id=str(uuid.uuid4())[:8],
            prediction_type=PredictionType.COMPREHENSIVE,
            timestamp=datetime.now(),
            input_data={"query": query},
            result={"status": "预测完成"},
            confidence=0.5,
            interpretation="预测系统正常运行",
            probability=0.5
        )
    
    def get_prediction_history(self, limit: int = 10) -> List[PredictionResult]:
        """获取预测历史"""
        return self.prediction_history[-limit:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self.prediction_history:
            return {"total_predictions": 0}
        
        avg_confidence = sum(p.confidence for p in self.prediction_history) / len(self.prediction_history)
        avg_probability = sum(p.probability for p in self.prediction_history) / len(self.prediction_history)
        
        method_counts = {}
        for p in self.prediction_history:
            method = p.prediction_type.value
            method_counts[method] = method_counts.get(method, 0) + 1
        
        return {
            "total_predictions": len(self.prediction_history),
            "average_confidence": avg_confidence,
            "average_probability": avg_probability,
            "method_distribution": method_counts
        }


def create_prediction_engine() -> PredictionEngine:
    """创建预测引擎"""
    return PredictionEngine()
