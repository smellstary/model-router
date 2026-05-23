"""
形象与气场系统 - ASCII / SVG / 文字描述
Image and Aura System
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import random
import hashlib


class AuraColor(Enum):
    """气场颜色枚举"""
    RED = "赤"
    ORANGE = "橙"
    YELLOW = "黄"
    GREEN = "绿"
    BLUE = "蓝"
    INDIGO = "靛"
    PURPLE = "紫"
    WHITE = "白"
    BLACK = "黑"
    GOLD = "金"
    SILVER = "银"


class AnimalForm(Enum):
    """兽形枚举"""
    DRAGON = "龙"
    PHOENIX = "凤凰"
    TIGER = "虎"
    TURTLE = "龟"
    QILIN = "麒麟"
    FENGHUANG = "凤凰"
    WHITE_TIGER = "白虎"
    BLACK_TORTOISE = "玄武"
    GREEN_DRAGON = "青龙"
    VERMILION_BIRD = "朱雀"


@dataclass
class AuraState:
    """气场状态"""
    primary_color: AuraColor
    secondary_colors: List[AuraColor]
    intensity: float
    radius: float
    stability: float
    description: str = ""


@dataclass
class AnimalSpirit:
    """兽灵状态"""
    form: AnimalForm
    strength: float
    health: float
    active: bool
    description: str = ""


@dataclass
class ImageState:
    """形象状态"""
    aura: AuraState
    animal_spirit: Optional[AnimalSpirit]
    vitality: float
    reputation: float
    influence: float
    description: str = ""


AURA_COLOR_WUXING_MAP = {
    "龙": AuraColor.GREEN,
    "凤凰": AuraColor.ORANGE,
    "麒麟": AuraColor.PURPLE,
    "虎": AuraColor.ORANGE,
    "龟": AuraColor.BLUE,
    "白虎": AuraColor.WHITE,
    "玄武": AuraColor.BLACK,
    "青龙": AuraColor.GREEN,
    "朱雀": AuraColor.RED,
}


@dataclass
class PromptContext:
    """提示词上下文"""
    wuxing_type: str
    aura_color: str
    animal_form: str
    mood: str
    scene: str
    color_palette: List[str] = field(default_factory=list)
    style_keywords: List[str] = field(default_factory=list)


class ImageSystem:
    """形象与气场生成系统"""

    def __init__(self):
        self.current_aura: Optional[AuraState] = None
        self.current_animal: Optional[AnimalSpirit] = None
        self.prompt_history: List[Dict] = []
        self._aura_cache: Dict[str, AuraState] = {}

    def _generate_hash(self, content: str) -> str:
        return hashlib.md5(content.encode()).hexdigest()[:8]

    def create_aura(
        self,
        wuxing_type: str,
        intensity: float = 0.8,
        stability: float = 0.8
    ) -> AuraState:
        """创建气场"""
        wuxing_to_colors: Dict[str, Tuple[AuraColor, List[AuraColor]]] = {
            "木": (AuraColor.GREEN, [AuraColor.BLUE, AuraColor.YELLOW]),
            "火": (AuraColor.ORANGE, [AuraColor.RED, AuraColor.YELLOW]),
            "土": (AuraColor.GOLD, [AuraColor.YELLOW, AuraColor.ORANGE]),
            "金": (AuraColor.WHITE, [AuraColor.SILVER, AuraColor.GOLD]),
            "水": (AuraColor.BLUE, [AuraColor.INDIGO, AuraColor.PURPLE]),
        }

        primary, secondaries = wuxing_to_colors.get(
            wuxing_type, (AuraColor.WHITE, [AuraColor.SILVER])
        )

        aura = AuraState(
            primary_color=primary,
            secondary_colors=secondaries,
            intensity=intensity,
            radius=1.0 + intensity * 0.5,
            stability=stability,
        )

        self.current_aura = aura
        return aura

    def summon_animal_spirit(
        self,
        animal_type: str,
        strength: float = 0.8
    ) -> AnimalSpirit:
        """召唤兽灵"""
        animal_map = {
            "龙": AnimalForm.DRAGON,
            "凤凰": AnimalForm.PHOENIX,
            "虎": AnimalForm.TIGER,
            "龟": AnimalForm.TURTLE,
            "麒麟": AnimalForm.QILIN,
        }

        form = animal_map.get(animal_type, AnimalForm.QILIN)

        spirit = AnimalSpirit(
            form=form,
            strength=strength,
            health=1.0,
            active=True,
        )

        self.current_animal = spirit
        return spirit

    def get_image_state(
        self,
        wuxing_type: str,
        mood: str = "平静",
        scene: str = "自然"
    ) -> ImageState:
        """获取当前形象状态"""
        aura = self.current_aura or self.create_aura(wuxing_type)
        animal = self.current_animal

        vitality = aura.intensity * aura.stability
        reputation = random.uniform(0.6, 1.0) * aura.intensity
        influence = random.uniform(0.5, 1.0) * aura.stability

        return ImageState(
            aura=aura,
            animal_spirit=animal,
            vitality=vitality,
            reputation=reputation,
            influence=influence,
        )

    def generate_prompt(
        self,
        wuxing_type: str,
        mood: str = "平静",
        scene: str = "自然",
        style: str = "中国风",
        include_animal: bool = True
    ) -> str:
        """生成形象提示词"""
        context = PromptContext(
            wuxing_type=wuxing_type,
            aura_color=self._get_aura_color_name(wuxing_type),
            animal_form=self._get_animal_name(wuxing_type) if include_animal else "无",
            mood=mood,
            scene=scene,
            color_palette=self._get_color_palette(wuxing_type),
            style_keywords=self._get_style_keywords(style),
        )

        prompt = self._build_prompt(context)

        self.prompt_history.append({
            "timestamp": datetime.now().isoformat(),
            "wuxing": wuxing_type,
            "mood": mood,
            "prompt": prompt,
        })

        return prompt

    def _get_aura_color_name(self, wuxing_type: str) -> str:
        color_map = {
            "木": "青色/翠绿色",
            "火": "赤红色/橙红色",
            "土": "黄色/金黄色",
            "金": "白色/银白色",
            "水": "蓝紫色/深蓝色",
        }
        return color_map.get(wuxing_type, "白色")

    def _get_animal_name(self, wuxing_type: str) -> str:
        animal_map = {
            "木": "青龙",
            "火": "朱雀",
            "土": "麒麟",
            "金": "白虎",
            "水": "玄武",
        }
        return animal_map.get(wuxing_type, "麒麟")

    def _get_color_palette(self, wuxing_type: str) -> List[str]:
        palettes = {
            "木": ["#00A86B", "#228B22", "#ADFF2F", "#98FB98"],
            "火": ["#FF4500", "#FF6347", "#FFD700", "#FFA500"],
            "土": ["#DAA520", "#B8860B", "#CD853F", "#DEB887"],
            "金": ["#E8E8E8", "#C0C0C0", "#FFD700", "#F5F5F5"],
            "水": ["#4169E1", "#6A5ACD", "#9370DB", "#87CEEB"],
        }
        return palettes.get(wuxing_type, ["#FFFFFF", "#E8E8E8"])

    def _get_style_keywords(self, style: str) -> List[str]:
        style_map = {
            "中国风": ["水墨", "工笔", "写意", "祥云", "龙纹", "仙鹤"],
            "古典": ["古风", "绢本", "宣纸", "毛笔", "印章"],
            "现代": ["极简", "几何", "渐变", "扁平"],
        }
        return style_map.get(style, ["水墨", "古风"])

    def _build_prompt(self, context: PromptContext) -> str:
        parts = []

        parts.append(f"{context.wuxing_type}行修士")
        parts.append(f"气场颜色：{context.aura_color}")
        parts.append(f"心境：{context.mood}")
        parts.append(f"场景：{context.scene}")

        if context.animal_form != "无":
            parts.append(f"守护灵：{context.animal_form}")

        parts.append(f"配色：{', '.join(context.color_palette[:3])}")
        parts.append(f"风格：{', '.join(context.style_keywords[:3])}")

        return "，".join(parts)

    def get_aura_visualization(self) -> str:
        """获取气场 ASCII 可视化"""
        if not self.current_aura:
            return "无气场"

        aura = self.current_aura
        color_char = self._aura_color_to_char(aura.primary_color)

        size = int(aura.radius * 5)
        lines = []
        center = size // 2

        for y in range(size):
            row = []
            for x in range(size):
                dist = ((x - center) ** 2 + (y - center) ** 2) ** 0.5
                if dist <= center * 0.3:
                    row.append(color_char * 2)
                elif dist <= center * 0.6:
                    row.append(color_char)
                elif dist <= center:
                    opacity = (1 - (dist - center * 0.6) / (center * 0.4))
                    if random.random() < opacity:
                        row.append(color_char)
                    else:
                        row.append(" ")
                else:
                    row.append(" ")
            lines.append("".join(row))

        return "\n".join(lines)

    def _aura_color_to_char(self, color: AuraColor) -> str:
        char_map = {
            AuraColor.RED: "█",
            AuraColor.ORANGE: "▓",
            AuraColor.YELLOW: "▒",
            AuraColor.GREEN: "░",
            AuraColor.BLUE: "▄",
            AuraColor.INDIGO: "▀",
            AuraColor.PURPLE: "█",
            AuraColor.WHITE: "□",
            AuraColor.BLACK: "■",
            AuraColor.GOLD: "★",
            AuraColor.SILVER: "○",
        }
        return char_map.get(color, "░")

    def describe_image(self, wuxing_type: str, mood: str = "平静") -> str:
        """生成形象文字描述"""
        aura_color = self._get_aura_color_name(wuxing_type)
        animal_name = self._get_animal_name(wuxing_type)

        descriptions = {
            "平静": f"周身环绕着{aura_color}的气场，{animal_name}盘踞其侧，神态安详。",
            "威严": f"散发着耀眼的{aura_color}光芒，{animal_name}昂首挺立，气势如虹。",
            "神秘": f"周身{aura_color}雾气缭绕，{animal_name}若隐若现，神秘莫测。",
            "祥和": f"温和的{aura_color}光芒笼罩全身，{animal_name}静卧守护，一片祥和。",
            "激昂": f"{aura_color}光芒冲天而起，{animal_name}展翅欲飞，战意昂扬。",
        }

        return descriptions.get(mood, descriptions["平静"])
