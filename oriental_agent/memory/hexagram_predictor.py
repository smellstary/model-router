"""
六爻预测系统
Hexagram Divination System

基于《易经》六爻方法论，支持：
- 摇卦（Three Coins Method）生成六爻
- 梅花易数简化版
- 老阴少阳转换
- 六亲六神装配
- 卦象解读与建议
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import random
import hashlib
import logging

logger = logging.getLogger(__name__)


class TrigramType(Enum):
    """八卦"""
    QIAN = ("乾", "天", "☰")
    KUN = ("坤", "地", "☷")
    ZHEN = ("震", "雷", "☳")
    XUN = ("巽", "风", "☴")
    KAN = ("坎", "水", "☵")
    LI = ("离", "火", "☲")
    GEN = ("艮", "山", "☶")
    DUI = ("兑", "泽", "☱")


class LineType(Enum):
    """爻位"""
    YANG = "阳"
    YIN = "阴"


@dataclass
class HexagramLine:
    """单爻"""
    position: int
    line_type: LineType
    is_change: bool

    def __str__(self):
        base = "━━━" if self.line_type == LineType.YANG else "━ ━"
        marker = "×" if self.is_change else " "
        return f"{marker}{base}{marker}"

    @property
    def is_yang(self) -> bool:
        return self.line_type == LineType.YANG


@dataclass
class Hexagram:
    """完整卦象"""
    upper_trigram: TrigramType
    lower_trigram: TrigramType
    lines: List[HexagramLine]
    changing_lines: List[int]
    name: str
    meaning: str
    judgment: str
    image: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class SixRelatives:
    """六亲"""
    parents: List[int] = field(default_factory=list)
    siblings: List[int] = field(default_factory=list)
    finances: List[int] = field(default_factory=list)
    official: List[int] = field(default_factory=list)
    children: List[int] = field(default_factory=list)
    self_relation: List[int] = field(default_factory=list)


@dataclass
class SixShen:
    """六神"""
    shen: List[Tuple[str, str]] = field(default_factory=list)


class HexagramPredictor:
    """六爻预测主类"""

    TRIGRAM_MEMBERS = {
        TrigramType.QIAN: ["父", "父", "官", "兄", "财", "子"],
        TrigramType.KUN: ["母", "财", "子", "官", "官", "父"],
        TrigramType.ZHEN: ["财", "官", "子", "父", "父", "官"],
        TrigramType.XUN: ["官", "父", "兄", "财", "财", "子"],
        TrigramType.KAN: ["兄", "子", "父", "财", "官", "父"],
        TrigramType.LI: ["子", "父", "财", "父", "父", "官"],
        TrigramType.GEN: ["兄", "父", "官", "父", "财", "官"],
        TrigramType.DUI: ["父", "官", "财", "父", "子", "兄"],
    }

    SIX_SHEN_SEQUENCE = ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"]

    HEXAGRAM_DATA = {
        ("乾", "乾"): {
            "name": "乾为天",
            "meaning": "刚健中正，纯粹的阳",
            "judgment": "元亨利贞。",
            "image": "天行健，君子以自强不息。",
        },
        ("坤", "坤"): {
            "name": "坤为地",
            "meaning": "柔顺厚重，纯粹阴",
            "judgment": "元亨利牝马之贞。",
            "image": "地势坤，君子以厚德载物。",
        },
        ("乾", "坤"): {
            "name": "天地否",
            "meaning": "阴阳不交，阻塞不通",
            "judgment": "否之匪人，不利君子贞。",
            "image": "天地不交，否。",
        },
        ("坤", "乾"): {
            "name": "地天泰",
            "meaning": "阴阳相交，通泰和谐",
            "judgment": "泰，小往大来。",
            "image": "天地交，泰。",
        },
    }

    def __init__(self):
        self.current_hexagram: Optional[Hexagram] = None
        self.divination_history: List[Dict] = []

    def cast_three_coins(self) -> Tuple[int, int]:
        """摇卦：抛三枚硬币
        返回 (正面数, 背面数)
        3正 = 老阳(变爻)
        2正1背 = 少阳(静爻)
        1正2背 = 少阴(静爻)
        0正 = 老阴(变爻)
        """
        heads = sum(random.randint(0, 1) for _ in range(3))
        return heads, 3 - heads

    def coins_to_line(self, heads: int) -> Tuple[LineType, bool]:
        """硬币结果转换为爻"""
        if heads == 3:
            return LineType.YANG, True
        elif heads == 0:
            return LineType.YIN, True
        elif heads == 2:
            return LineType.YANG, False
        else:
            return LineType.YIN, False

    def cast_hexagram(self, question: str, cast_type: str = "three_coins") -> Hexagram:
        """摇六爻成卦"""
        lines: List[HexagramLine] = []
        changing_indices: List[int] = []

        for i in range(6):
            if cast_type == "three_coins":
                heads, _ = self.cast_three_coins()
                line_type, is_change = self.coins_to_line(heads)
            else:
                line_type = random.choice([LineType.YANG, LineType.YIN])
                is_change = random.random() < 0.15

            lines.append(HexagramLine(
                position=6 - i,
                line_type=line_type,
                is_change=is_change
            ))

            if is_change:
                changing_indices.append(6 - i)

        upper_lines = lines[0:3]
        lower_lines = lines[3:6]

        upper_trigram = self._lines_to_trigram(upper_lines)
        lower_trigram = self._lines_to_trigram(lower_lines)

        hexagram_key = (upper_trigram.value[0], lower_trigram.value[0])
        hex_data = self.HEXAGRAM_DATA.get(hexagram_key, {
            "name": f"{upper_trigram.value[0]}{lower_trigram.value[0]}卦",
            "meaning": "变化之卦",
            "judgment": "时机待定。",
            "image": "观察形势，灵活应对。",
        })

        hexagram = Hexagram(
            upper_trigram=upper_trigram,
            lower_trigram=lower_trigram,
            lines=lines,
            changing_lines=changing_indices,
            name=hex_data["name"],
            meaning=hex_data["meaning"],
            judgment=hex_data["judgment"],
            image=hex_data["image"],
        )

        self.current_hexagram = hexagram

        self.divination_history.append({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "hexagram": hex_data["name"],
            "changing_lines": changing_indices,
        })

        return hexagram

    def _lines_to_trigram(self, lines: List[HexagramLine]) -> TrigramType:
        """三爻转换为八卦"""
        pattern = "".join("1" if line.is_yang else "0" for line in lines)

        trigram_map = {
            "111": TrigramType.QIAN,
            "000": TrigramType.KUN,
            "001": TrigramType.GEN,
            "010": TrigramType.KAN,
            "011": TrigramType.XUN,
            "100": TrigramType.LI,
            "101": TrigramType.DUI,
            "110": TrigramType.ZHEN,
        }

        return trigram_map.get(pattern, TrigramType.QIAN)

    def get_six_relatives(self, hexagram: Hexagram) -> SixRelatives:
        """装配六亲"""
        upper = hexagram.upper_trigram
        lower = hexagram.lower_trigram

        members_upper = self.TRIGRAM_MEMBERS[upper]
        members_lower = self.TRIGRAM_MEMBERS[lower]

        all_members = members_lower + members_upper

        relatives = SixRelatives()
        for i, member in enumerate(all_members):
            if member == "父":
                relatives.parents.append(i + 1)
            elif member == "官":
                relatives.official.append(i + 1)
            elif member == "兄":
                relatives.siblings.append(i + 1)
            elif member == "财":
                relatives.finances.append(i + 1)
            elif member == "子":
                relatives.children.append(i + 1)

        return relatives

    def get_six_shen(self, hexagram: Hexagram) -> SixShen:
        """装配六神（每日换神起始）"""
        today_offset = datetime.now().weekday()
        start_idx = today_offset % 6

        shen_list = []
        for i in range(6):
            shen_name = self.SIX_SHEN_SEQUENCE[(start_idx + i) % 6]
            position = 6 - i
            shen_list.append((shen_name, position))

        return SixShen(shen=shen_list)

    def interpret_hexagram(
        self,
        question: str,
        focus_area: Optional[str] = None
    ) -> Dict[str, Any]:
        """解读卦象"""
        if not self.current_hexagram:
            return {"error": "请先摇卦"}

        hexagram = self.current_hexagram
        six_relatives = self.get_six_relatives(hexagram)
        six_shen = self.get_six_shen(hexagram)

        changing_line_desc = ""
        if hexagram.changing_lines:
            line_nums = ", ".join(f"第{i}爻" for i in hexagram.changing_lines)
            changing_line_desc = f"变爻在{line_nums}，事物正在转化中。"
        else:
            changing_line_desc = "六爻安静，局势稳定。"

        interpretation = {
            "question": question,
            "hexagram_name": hexagram.name,
            "upper_trigram": hexagram.upper_trigram.value[1],
            "lower_trigram": hexagram.lower_trigram.value[1],
            "meaning": hexagram.meaning,
            "judgment": hexagram.judgment,
            "image_text": hexagram.image,
            "changing_lines": hexagram.changing_lines,
            "changing_description": changing_line_desc,
            "six_relatives": {
                "父母": six_relatives.parents,
                "兄弟": six_relatives.siblings,
                "妻财": six_relatives.finances,
                "官鬼": six_relatives.official,
                "子孙": six_relatives.children,
            },
            "six_shen": [{"shen": s, "position": p} for s, p in six_shen.shen],
            "line_display": self._format_hexagram_lines(hexagram),
            "advice": self._generate_advice(hexagram, question, focus_area),
        }

        return interpretation

    def _format_hexagram_lines(self, hexagram: Hexagram) -> List[str]:
        """格式化六爻显示"""
        lines_str = []
        for line in hexagram.lines:
            lines_str.append(str(line))
        return lines_str

    def _generate_advice(
        self,
        hexagram: Hexagram,
        question: str,
        focus_area: Optional[str]
    ) -> List[str]:
        """生成建议"""
        advice = []

        if len(hexagram.changing_lines) >= 3:
            advice.append("变爻较多，局势正处于重要转变期，宜静观其变。")
        elif len(hexagram.changing_lines) == 0:
            advice.append("六爻安静，当前形势稳定，适合按部就班行动。")
        else:
            advice.append("有所变化但尚在可控范围内，宜顺势而为。")

        if hexagram.name in ["天地否", "天雷无妄"]:
            advice.append("注意小人是非，低调行事。")
        elif hexagram.name in ["地天泰", "风天小畜"]:
            advice.append("形势向好，宜把握时机，积极进取。")

        if "婚" in question or "感情" in question:
            advice.append("感情事宜需耐心沟通，避免冲动决策。")
        elif "事业" in question or "工作" in question:
            advice.append("事业上宜稳扎稳打，不宜冒进。")
        elif "财运" in question or "投资" in question:
            advice.append("财务决策需谨慎，避免高风险投资。")

        return advice

    def get_divination_history(self, limit: int = 10) -> List[Dict]:
        """获取历史占卜记录"""
        return self.divination_history[-limit:]

    def clear_history(self) -> None:
        """清空历史"""
        self.divination_history.clear()
        self.current_hexagram = None
