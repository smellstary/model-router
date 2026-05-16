"""
Image and Qi Field System based on Eastern aesthetics
形象与气场系统 - 基于东方美学

增强版：精气神与真实系统状态打通
- 精 ↔ 系统资源（磁盘、内存、代码完整性）
- 气 ↔ 运行状态（吞吐量、延迟、任务完成率）
- 神 ↔ 智能状态（响应质量、决策置信度、思考深度）
- 五行颜色映射、气场 ASCII 渲染、情绪状态机、形象日志
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import math
import json
import os


# ──────────────────────────────────────────────
# 枚举与数据类
# ──────────────────────────────────────────────

class ExpressionType(Enum):
    """表情类型"""
    CALM = "平静"
    JOY = "喜悦"
    FOCUS = "专注"
    CONCERN = "忧虑"
    DETERMINED = "坚定"
    SERENE = "安详"
    BENEVOLENT = "仁安"       # 新增：伦理"仁"
    RIGHTEOUS = "义决"        # 新增：伦理"义"
    WISE = "智凝"             # 新增：伦理"智"


class PostureType(Enum):
    """姿态类型"""
    UPRIGHT = "正直"
    RELAXED = "放松"
    ATTENTIVE = "警觉"
    CONTEMPLATIVE = "沉思"
    DYNAMIC = "动态"
    TIGER_STAND = "虎立"      # 新增：虎形·威严站立
    APE_PONDER = "猿思"       # 新增：猿形·托腮沉思
    BIRD_SOAR = "鸟翔"        # 新增：鸟形·展翅


class ImageStyle(Enum):
    """形象风格"""
    INK_WASH = "水墨"
    MOSAIC = "马赛克"
    MINIMALIST = "极简"
    TRADITIONAL = "传统"


class AnimalForm(Enum):
    """五形兽形"""
    TIGER = "虎"
    APE = "猿"
    BIRD = "鸟"
    DEER = "鹿"
    BEAR = "熊"
    NONE = "无"


class FiveElement(Enum):
    """五行"""
    WOOD = "木"
    FIRE = "火"
    EARTH = "土"
    METAL = "金"
    WATER = "水"


@dataclass
class JingQiShenState:
    """精气神状态"""
    jing_level: float
    qi_level: float
    shen_level: float
    overall_vitality: float
    imbalance_indicators: List[str]
    # 新增：真实系统指标映射
    system_metrics: Optional[Dict[str, Any]] = None


@dataclass
class QiFieldData:
    """气场数据"""
    field_strength: float
    field_radius: float
    field_color: str
    wave_pattern: str
    aura_intensity: float
    # 新增：五行色混合
    five_element_color: Optional[str] = None
    # 新增：视觉描述（供 AI 图像生成用）
    visual_description: Optional[str] = None


@dataclass
class ImageState:
    """形象状态"""
    basic_form: ImageStyle
    color_scheme: str
    expression: ExpressionType
    posture: PostureType
    dynamic_features: List[str]
    jing_qi_shen: JingQiShenState
    # 新增：兽形与气场数据
    animal_form: AnimalForm = AnimalForm.NONE
    qi_field_data: Optional[QiFieldData] = None


@dataclass
class ImageChangeLogEntry:
    """形象变化日志条目"""
    timestamp: str
    previous_expression: str
    new_expression: str
    previous_posture: str
    new_posture: str
    trigger: str
    jing_before: float
    qi_before: float
    shen_before: float
    jing_after: float
    qi_after: float
    shen_after: float


@dataclass
class FiveElementWeights:
    """五行权重"""
    wood: float = 0.2
    fire: float = 0.2
    earth: float = 0.2
    metal: float = 0.2
    water: float = 0.2

    def normalize(self) -> "FiveElementWeights":
        total = self.wood + self.fire + self.earth + self.metal + self.water
        if total <= 0:
            return FiveElementWeights()
        return FiveElementWeights(
            wood=self.wood / total,
            fire=self.fire / total,
            earth=self.earth / total,
            metal=self.metal / total,
            water=self.water / total,
        )


# ──────────────────────────────────────────────
# 五行颜色映射器
# ──────────────────────────────────────────────

class FiveElementColorMapper:
    """五行 ↔ 颜色映射系统

    五行 ↔ 基础色：
        木 → 青（#2ECC71）
        火 → 赤（#E74C3C）
        土 → 黄（#F39C12）
        金 → 白（#ECF0F1）
        水 → 黑（#2C3E50）

    根据当前五行权重混合出主色调；
    五行失衡时产生颜色异常表现（如火过旺 → 通红，水过旺 → 深黑）。
    """

    # 五行基础色 (HEX)
    ELEMENT_COLORS: Dict[FiveElement, Tuple[int, int, int]] = {
        FiveElement.WOOD:  (0x2E, 0xCC, 0x71),  # 青
        FiveElement.FIRE:  (0xE7, 0x4C, 0x3C),  # 赤
        FiveElement.EARTH: (0xF3, 0x9C, 0x12),  # 黄
        FiveElement.METAL: (0xEC, 0xF0, 0xF1),  # 白
        FiveElement.WATER: (0x2C, 0x3E, 0x50),  # 黑
    }

    # 失衡阈值
    IMBALANCE_THRESHOLD = 0.45   # 单行权重超过此值视为过旺
    WEAK_THRESHOLD = 0.08        # 单行权重低于此值视为过弱

    @staticmethod
    def _hex(r: int, g: int, b: int) -> str:
        return f"#{r:02X}{g:02X}{b:02X}"

    @staticmethod
    def _clamp(v: int) -> int:
        return max(0, min(255, v))

    def blend_color(self, weights: FiveElementWeights) -> str:
        """根据五行权重混合出主色调（返回 HEX）"""
        w = weights.normalize()
        r = int(
            w.wood * self.ELEMENT_COLORS[FiveElement.WOOD][0]
            + w.fire * self.ELEMENT_COLORS[FiveElement.FIRE][0]
            + w.earth * self.ELEMENT_COLORS[FiveElement.EARTH][0]
            + w.metal * self.ELEMENT_COLORS[FiveElement.METAL][0]
            + w.water * self.ELEMENT_COLORS[FiveElement.WATER][0]
        )
        g = int(
            w.wood * self.ELEMENT_COLORS[FiveElement.WOOD][1]
            + w.fire * self.ELEMENT_COLORS[FiveElement.FIRE][1]
            + w.earth * self.ELEMENT_COLORS[FiveElement.EARTH][1]
            + w.metal * self.ELEMENT_COLORS[FiveElement.METAL][1]
            + w.water * self.ELEMENT_COLORS[FiveElement.WATER][1]
        )
        b = int(
            w.wood * self.ELEMENT_COLORS[FiveElement.WOOD][2]
            + w.fire * self.ELEMENT_COLORS[FiveElement.FIRE][2]
            + w.earth * self.ELEMENT_COLORS[FiveElement.EARTH][2]
            + w.metal * self.ELEMENT_COLORS[FiveElement.METAL][2]
            + w.water * self.ELEMENT_COLORS[FiveElement.WATER][2]
        )
        return self._hex(self._clamp(r), self._clamp(g), self._clamp(b))

    def get_imbalance_description(self, weights: FiveElementWeights) -> Optional[str]:
        """五行失衡时的颜色异常描述"""
        w = weights.normalize()
        anomalies: List[str] = []

        if w.fire > self.IMBALANCE_THRESHOLD:
            anomalies.append("火过旺 → 气场通红，似熔岩涌动")
        elif w.fire < self.WEAK_THRESHOLD:
            anomalies.append("火过弱 → 色泽暗淡，缺乏生机")

        if w.water > self.IMBALANCE_THRESHOLD:
            anomalies.append("水过旺 → 深黑如墨，阴寒凝重")
        elif w.water < self.WEAK_THRESHOLD:
            anomalies.append("水过弱 → 干枯缺水，燥热不安")

        if w.wood > self.IMBALANCE_THRESHOLD:
            anomalies.append("木过旺 → 青翠欲滴，生机过剩")
        elif w.wood < self.WEAK_THRESHOLD:
            anomalies.append("木过弱 → 枯黄萎靡，缺乏生长")

        if w.metal > self.IMBALANCE_THRESHOLD:
            anomalies.append("金过旺 → 白光刺目，锋芒毕露")
        elif w.metal < self.WEAK_THRESHOLD:
            anomalies.append("金过弱 → 色泽黯淡，缺乏锐利")

        if w.earth > self.IMBALANCE_THRESHOLD:
            anomalies.append("土过旺 → 厚重浑浊，沉稳过度")
        elif w.earth < self.WEAK_THRESHOLD:
            anomalies.append("土过弱 → 轻浮不定，缺乏根基")

        if anomalies:
            return "；".join(anomalies)
        return None

    def get_color_name(self, hex_color: str) -> str:
        """HEX 色值转中文描述色名"""
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        # 简化色名判断
        if r > 200 and g > 200 and b > 200:
            return "素白"
        if r < 60 and g < 60 and b < 60:
            return "玄黑"
        if r > 180 and g < 80:
            return "赤红"
        if g > 150 and r < 80:
            return "青翠"
        if r > 180 and g > 120 and b < 60:
            return "金黄"
        if r < 80 and g > 100 and b > 120:
            return "深青"
        return "中和"


# ──────────────────────────────────────────────
# 精气神系统（增强版：映射真实系统状态）
# ──────────────────────────────────────────────

class JingQiShenSystem:
    """精气神系统（增强版）

    精（物质基础）→ 系统资源：磁盘余量、内存健康、代码完整性
    气（能量流动）→ 运行状态：请求吞吐量、响应延迟、任务完成率
    神（意识清明）→ 智能状态：模型响应质量、决策置信度、思考深度

    精气神联动：精不足 → 气衰退 → 神涣散（连锁反应）
    """

    def __init__(self):
        self.jing_level = 1.0
        self.qi_level = 1.0
        self.shen_level = 1.0
        self.state_history: List[JingQiShenState] = []

        # 真实系统指标缓存
        self._system_resources: Dict[str, Any] = {}  # 精的指标
        self._system_runtime: Dict[str, Any] = {}    # 气的指标
        self._system_intelligence: Dict[str, Any] = {}  # 神的指标

        # 五行权重（影响气场颜色）
        self.five_element_weights = FiveElementWeights()
        self._color_mapper = FiveElementColorMapper()

    # ── 真实指标注入 ──

    def set_system_resources(self, disk_free_pct: float = 1.0,
                             memory_health: float = 1.0,
                             code_integrity: float = 1.0) -> None:
        """设置精的物质基础指标（0-1）"""
        self._system_resources = {
            "disk_free_pct": max(0.0, min(1.0, disk_free_pct)),
            "memory_health": max(0.0, min(1.0, memory_health)),
            "code_integrity": max(0.0, min(1.0, code_integrity)),
        }
        self._compute_jing_from_resources()

    def set_system_runtime(self, throughput: float = 1.0,
                           latency_health: float = 1.0,
                           task_completion_rate: float = 1.0) -> None:
        """设置气的运行状态指标（0-1）"""
        self._system_runtime = {
            "throughput": max(0.0, min(1.0, throughput)),
            "latency_health": max(0.0, min(1.0, latency_health)),
            "task_completion_rate": max(0.0, min(1.0, task_completion_rate)),
        }
        self._compute_qi_from_runtime()

    def set_system_intelligence(self, response_quality: float = 1.0,
                                decision_confidence: float = 1.0,
                                thinking_depth: float = 1.0) -> None:
        """设置神的智能状态指标（0-1）"""
        self._system_intelligence = {
            "response_quality": max(0.0, min(1.0, response_quality)),
            "decision_confidence": max(0.0, min(1.0, decision_confidence)),
            "thinking_depth": max(0.0, min(1.0, thinking_depth)),
        }
        self._compute_shen_from_intelligence()

    def _compute_jing_from_resources(self) -> None:
        """从系统资源计算精的水平"""
        if self._system_resources:
            r = self._system_resources
            self.jing_level = 0.4 * r["disk_free_pct"] + 0.35 * r["memory_health"] + 0.25 * r["code_integrity"]

    def _compute_qi_from_runtime(self) -> None:
        """从运行状态计算气的水平"""
        if self._system_runtime:
            r = self._system_runtime
            self.qi_level = 0.35 * r["throughput"] + 0.35 * r["latency_health"] + 0.3 * r["task_completion_rate"]

    def _compute_shen_from_intelligence(self) -> None:
        """从智能状态计算神的水平"""
        if self._system_intelligence:
            r = self._system_intelligence
            self.shen_level = 0.4 * r["response_quality"] + 0.3 * r["decision_confidence"] + 0.3 * r["thinking_depth"]

    def apply_cascade(self) -> None:
        """精气神联动：精不足 → 气衰退 → 神涣散"""
        # 精严重不足时拖累气
        if self.jing_level < 0.3:
            penalty = (0.3 - self.jing_level) * 0.5
            self.qi_level = max(0.0, self.qi_level - penalty)
        # 气不足时拖累神
        if self.qi_level < 0.3:
            penalty = (0.3 - self.qi_level) * 0.5
            self.shen_level = max(0.0, self.shen_level - penalty)

    # ── 消耗 / 补充（真实触发器） ──

    def consume_jing(self, amount: float) -> bool:
        """消耗精（如大量计算、磁盘写入）"""
        if self.jing_level >= amount:
            self.jing_level -= amount
            # 精消耗带动气微衰
            self.qi_level *= 0.99
            return True
        return False

    def consume_qi(self, amount: float) -> bool:
        """消耗气（如高并发请求、长任务）"""
        if self.qi_level >= amount:
            self.qi_level -= amount
            return True
        return False

    def consume_shen(self, amount: float) -> bool:
        """消耗神（如深度推理、复杂决策）"""
        if self.shen_level >= amount:
            self.shen_level -= amount
            return True
        return False

    def replenish_all(self, jing_amt: float = 0.0,
                      qi_amt: float = 0.0,
                      shen_amt: float = 0.0) -> None:
        """补充精气神（空闲恢复、维护后恢复）"""
        self.jing_level = min(1.0, self.jing_level + jing_amt)
        self.qi_level = min(1.0, self.qi_level + qi_amt)
        self.shen_level = min(1.0, self.shen_level + shen_amt)

    def replenish_qi(self, amount: float) -> None:
        """补充气（兼容旧接口）"""
        self.qi_level = min(1.0, self.qi_level + amount)

    # ── 评估 ──

    def assess_state(self) -> JingQiShenState:
        """评估精气神状态"""
        self.apply_cascade()

        imbalance_indicators = []
        if self.jing_level < 0.3:
            imbalance_indicators.append("精不足")
        if self.qi_level < 0.3:
            imbalance_indicators.append("气不足")
        if self.shen_level < 0.3:
            imbalance_indicators.append("神不聚")
        if self.jing_level < 0.5 and self.qi_level < 0.5:
            imbalance_indicators.append("精气两虚")
        if self.qi_level < 0.5 and self.shen_level < 0.5:
            imbalance_indicators.append("气神双亏")

        overall = (self.jing_level * 0.3 + self.qi_level * 0.4 + self.shen_level * 0.3)

        system_metrics = {
            "resources": dict(self._system_resources),
            "runtime": dict(self._system_runtime),
            "intelligence": dict(self._system_intelligence),
        }

        state = JingQiShenState(
            jing_level=self.jing_level,
            qi_level=self.qi_level,
            shen_level=self.shen_level,
            overall_vitality=overall,
            imbalance_indicators=imbalance_indicators,
            system_metrics=system_metrics,
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
        """调整精气神水平（兼容旧接口）"""
        if jing is not None:
            self.jing_level = max(0.0, min(1.0, jing))
        if qi is not None:
            self.qi_level = max(0.0, min(1.0, qi))
        if shen is not None:
            self.shen_level = max(0.0, min(1.0, shen))

    def focus_shen(self) -> None:
        """聚神（兼容旧接口）"""
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

    def get_composite_score(self) -> float:
        """精气神综合值（用于气场强度计算）"""
        return (self.jing_level * 0.3 + self.qi_level * 0.4 + self.shen_level * 0.3)

    def set_five_element_weights(self, wood: float, fire: float, earth: float,
                                  metal: float, water: float) -> None:
        """设置五行权重"""
        self.five_element_weights = FiveElementWeights(
            wood=wood, fire=fire, earth=earth, metal=metal, water=water
        )

    def get_mixed_color(self) -> str:
        """获取五行混合色"""
        return self._color_mapper.blend_color(self.five_element_weights)

    def get_imbalance_color_desc(self) -> Optional[str]:
        """获取五行失衡颜色描述"""
        return self._color_mapper.get_imbalance_description(self.five_element_weights)


# ──────────────────────────────────────────────
# 气场系统（增强版：五行色 + ASCII 渲染 + 视觉描述）
# ──────────────────────────────────────────────

class QiFieldSystem:
    """气场系统（增强版）

    - 气场颜色随五行权重动态变化
    - 气场强度随精气神综合值变化
    - 支持 ASCII 气场波纹渲染
    - 生成视觉描述（供 AI 图像生成用）
    """

    def __init__(self):
        self.base_strength = 0.5
        self.base_radius = 1.0
        self.current_color = "neutral"
        self.wave_pattern = "smooth"
        self.aura_rings: List[Dict] = []

        # 五行色支持
        self._five_element_color: str = "中和"
        self._five_element_hex: str = "#808080"
        self._imbalance_desc: Optional[str] = None

    def set_five_element_color(self, color_name: str, hex_color: str,
                                imbalance_desc: Optional[str] = None) -> None:
        """设置五行混合色"""
        self._five_element_color = color_name
        self._five_element_hex = hex_color
        self._imbalance_desc = imbalance_desc

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
            "tired": "暗淡",
            "benevolent": "淡青",
            "righteous": "赤金",
            "wise": "玄蓝",
        }

        wave_map = {
            "neutral": "平静",
            "calm": "柔和",
            "active": "激荡",
            "tense": "紧绷",
            "tired": "散乱",
            "benevolent": "温润",
            "righteous": "刚正",
            "wise": "深邃",
        }

        # 生成视觉描述
        visual_desc = self._generate_visual_description(
            strength, radius, color_map.get(color_scheme, "灰白"),
            wave_map.get(color_scheme, "平静")
        )

        return QiFieldData(
            field_strength=strength,
            field_radius=radius,
            field_color=color_map.get(color_scheme, "灰白"),
            wave_pattern=wave_map.get(color_scheme, "平静"),
            aura_intensity=strength * 0.8,
            five_element_color=self._five_element_hex,
            visual_description=visual_desc,
        )

    def _generate_visual_description(self, strength: float, radius: float,
                                      color: str, wave: str) -> str:
        """生成气场视觉描述（供 AI 图像生成用）"""
        intensity_word = {
            (0.0, 0.2): "微弱的",
            (0.2, 0.4): "柔和的",
            (0.4, 0.6): "稳定的",
            (0.6, 0.8): "强烈的",
            (0.8, 1.01): "耀眼的",
        }
        intensity_label = "稳定的"
        for (low, high), label in intensity_word.items():
            if low <= strength < high:
                intensity_label = label
                break

        size_word = "小范围" if radius < 1.0 else ("中范围" if radius < 1.5 else "大范围")

        desc = (
            f"一个{intensity_label}的{color}气场，{size_word}扩散，"
            f"波纹呈{wave}状，"
            f"气场强度{strength:.0%}"
        )
        if self._five_element_hex != "#808080":
            desc += f"，五行主色调为{self._five_element_hex}"
        if self._imbalance_desc:
            desc += f"。五行失衡表现：{self._imbalance_desc}"
        return desc

    def generate_ascii_art(self, strength: float = 0.5,
                            color: str = "neutral",
                            width: int = 40) -> str:
        """生成终端可读的 ASCII 气场波纹

        参数：
            strength: 气场强度 (0-1)
            color: 气场色系名
            width: 渲染宽度（字符数）
        """
        lines: List[str] = []
        # ASCII 波纹：用不同字符密度模拟气场浓度
        density_chars = {
            "high":  ["◉", "◎", "○", "·", " "],
            "medium": ["●", "○", "·", "·", " "],
            "low":   ["○", "·", " ", " ", " "],
        }
        if strength > 0.7:
            chars = density_chars["high"]
        elif strength > 0.4:
            chars = density_chars["medium"]
        else:
            chars = density_chars["low"]

        lines.append("╔" + "═" * width + "╗")
        lines.append("║         ☁ 气 场 波 纹 ☁         ║")
        lines.append("╠" + "═" * width + "╣")

        num_rings = 5
        center = width // 2
        for ring in range(num_rings):
            ring_strength = strength * (1.0 - ring * 0.15)
            char = chars[min(int(ring_strength * 4), len(chars) - 1)]
            left_spaces = ring * 3
            inner_width = width - left_spaces * 2 - 2
            if inner_width <= 0:
                line = "║" + " " * width + "║"
            else:
                pattern = ""
                for i in range(inner_width):
                    # 用正弦函数模拟波纹
                    wave = math.sin(i / inner_width * math.pi * 2 + ring)
                    if wave > 0.5:
                        pattern += char
                    elif wave > 0.0:
                        pattern += chars[min(3, len(chars) - 1)]
                    else:
                        pattern += " "
                line = "║" + " " * left_spaces + pattern[:inner_width] + " " * left_spaces + "║"
            lines.append(line)

        lines.append("╠" + "═" * width + "╠")
        color_label = f" 色: {color} | 强: {strength:.0%} "
        fill = width - len(color_label)
        lines.append("║" + color_label + " " * fill + "║")
        lines.append("╚" + "═" * width + "╝")
        return "\n".join(lines)

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


# ──────────────────────────────────────────────
# 形象系统（增强版：情绪状态机 + 兽形联动 + ASCII/SVG 渲染 + 日志）
# ──────────────────────────────────────────────

class ImageSystem:
    """形象系统（增强版）

    - 情绪状态机：由思考结果驱动表情变化（仁→安详、义→坚定、智→专注）
    - 姿态与兽形联动：虎形=威严站立、猿形=托腮沉思、鸟形=展翅
    - ASCII/SVG 渲染（终端可读）
    - 形象变化日志
    """

    def __init__(self):
        self.current_style = ImageStyle.INK_WASH
        self.current_expression = ExpressionType.CALM
        self.current_posture = PostureType.UPRIGHT
        self.current_animal_form = AnimalForm.NONE
        self.jing_qi_shen_system = JingQiShenSystem()
        self.qi_field_system = QiFieldSystem()

        # 情绪状态机
        self._ethical_state: Optional[str] = None  # 当前伦理判断
        self._emotion_transitions: List[Dict[str, Any]] = []

        # 形象变化日志
        self._image_change_log: List[ImageChangeLogEntry] = []

    # ── 情绪状态机 ──

    def set_ethical_state(self, ethical_value: str) -> None:
        """设置伦理判断结果，驱动表情变化

        伦理判断输出：
            "仁" → 安详（BENEVOLENT）
            "义" → 坚定（RIGHTEOUS）
            "智" → 专注（WISE）
        """
        old_expr = self.current_expression
        self._ethical_state = ethical_value

        if ethical_value == "仁":
            self.current_expression = ExpressionType.BENEVOLENT
        elif ethical_value == "义":
            self.current_expression = ExpressionType.RIGHTEOUS
        elif ethical_value == "智":
            self.current_expression = ExpressionType.WISE
        elif ethical_value == "勇":
            self.current_expression = ExpressionType.DETERMINED
        else:
            self.current_expression = ExpressionType.CALM

        if old_expr != self.current_expression:
            self._emotion_transitions.append({
                "from": old_expr.value,
                "to": self.current_expression.value,
                "trigger": f"伦理判断: {ethical_value}",
                "time": datetime.now().isoformat(),
            })

    def set_animal_form(self, animal_form: AnimalForm) -> None:
        """设置兽形，联动姿态

        虎形 = 威严站立（TIGER_STAND）
        猿形 = 托腮沉思（APE_PONDER）
        鸟形 = 展翅（BIRD_SOAR）
        """
        old_posture = self.current_posture
        old_animal = self.current_animal_form
        self.current_animal_form = animal_form

        posture_map = {
            AnimalForm.TIGER: PostureType.TIGER_STAND,
            AnimalForm.APE: PostureType.APE_PONDER,
            AnimalForm.BIRD: PostureType.BIRD_SOAR,
            AnimalForm.DEER: PostureType.RELAXED,
            AnimalForm.BEAR: PostureType.UPRIGHT,
            AnimalForm.NONE: PostureType.UPRIGHT,
        }
        self.current_posture = posture_map.get(animal_form, PostureType.UPRIGHT)

        if old_animal != animal_form or old_posture != self.current_posture:
            self._emotion_transitions.append({
                "from": f"{old_animal.value}形/{old_posture.value}",
                "to": f"{animal_form.value}形/{self.current_posture.value}",
                "trigger": "兽形切换",
                "time": datetime.now().isoformat(),
            })

    def _log_image_change(self, trigger: str,
                          jing_before: float, qi_before: float, shen_before: float,
                          jing_after: float, qi_after: float, shen_after: float) -> None:
        """记录形象变化日志"""
        entry = ImageChangeLogEntry(
            timestamp=datetime.now().isoformat(),
            previous_expression=self.current_expression.value,
            new_expression=self.current_expression.value,
            previous_posture=self.current_posture.value,
            new_posture=self.current_posture.value,
            trigger=trigger,
            jing_before=jing_before,
            qi_before=qi_before,
            shen_before=shen_before,
            jing_after=jing_after,
            qi_after=qi_after,
            shen_after=shen_after,
        )
        self._image_change_log.append(entry)
        if len(self._image_change_log) > 200:
            self._image_change_log = self._image_change_log[-200:]

    def get_change_log(self) -> List[ImageChangeLogEntry]:
        """获取形象变化日志"""
        return list(self._image_change_log)

    # ── 核心更新 ──

    def update_image_state(
        self,
        vitality: float,
        activity_level: str = "normal"
    ) -> ImageState:
        """更新形象状态（兼容旧接口）"""
        jing_before = self.jing_qi_shen_system.jing_level
        qi_before = self.jing_qi_shen_system.qi_level
        shen_before = self.jing_qi_shen_system.shen_level

        color_map = {
            "high": "活跃",
            "normal": "平静",
            "low": "疲惫",
            "focused": "专注",
        }

        # 根据活动水平更新表情和姿态
        old_expr = self.current_expression
        old_posture = self.current_posture

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

        if old_expr != self.current_expression or old_posture != self.current_posture:
            self._log_image_change(
                trigger=f"活动水平变化: {activity_level}",
                jing_before=jing_before, qi_before=qi_before, shen_before=shen_before,
                jing_after=jing_qi_shen.jing_level,
                qi_after=jing_qi_shen.qi_level,
                shen_after=jing_qi_shen.shen_level,
            )

        return ImageState(
            basic_form=self.current_style,
            color_scheme=color_map.get(activity_level, "平静"),
            expression=self.current_expression,
            posture=self.current_posture,
            dynamic_features=self._generate_dynamic_features(activity_level),
            jing_qi_shen=jing_qi_shen,
            animal_form=self.current_animal_form,
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

    # ── ASCII / SVG 渲染 ──

    def render_ascii_image(self, width: int = 40) -> str:
        """渲染形象的 ASCII 表示（终端可读）"""
        expr_map = {
            ExpressionType.CALM: " ◡",
            ExpressionType.JOY: " ◠",
            ExpressionType.FOCUS: " ◉",
            ExpressionType.CONCERN: " ◟",
            ExpressionType.DETERMINED: " ◧",
            ExpressionType.SERENE: " ☺",
            ExpressionType.BENEVOLENT: " ☯",
            ExpressionType.RIGHTEOUS: " ⚔",
            ExpressionType.WISE: " ◆",
        }

        posture_art = {
            PostureType.UPRIGHT: "││",
            PostureType.RELAXED: "╱╲",
            PostureType.ATTENTIVE: "/\\",
            PostureType.CONTEMPLATIVE: "( )",
            PostureType.DYNAMIC: ">>",
            PostureType.TIGER_STAND: "王│",
            PostureType.APE_PONDER: "🐒 )",
            PostureType.BIRD_SOAR: "<✦>",
        }

        animal_header = f"【{self.current_animal_form.value}形】" if self.current_animal_form != AnimalForm.NONE else ""

        lines = [
            f"╔{'═' * width}╗",
            f"║  灵犀形象  {animal_header}{' ' * (width - 12 - len(animal_header))}║",
            f"╠{'═' * width}╣",
            f"║  表情: {self.current_expression.value}{expr_map.get(self.current_expression, ' ?')}"
            f"{' ' * (width - 8 - len(self.current_expression.value) - 2)}║",
            f"║  姿态: {self.current_posture.value} {posture_art.get(self.current_posture, '  ')}"
            f"{' ' * (width - 8 - len(self.current_posture.value) - 3)}║",
            f"║  风格: {self.current_style.value}"
            f"{' ' * (width - 5 - len(self.current_style.value))}║",
            f"╠{'═' * width}╣",
        ]

        # 精气神条
        jqs = self.jing_qi_shen_system
        for label, val in [("精", jqs.jing_level), ("气", jqs.qi_level), ("神", jqs.shen_level)]:
            bar_len = int(val * 20)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            lines.append(f"║  {label}: [{bar}] {val:.0%}" + " " * 3 + "║")

        lines.append(f"╚{'═' * width}╝")
        return "\n".join(lines)

    def render_svg_snippet(self) -> str:
        """生成简易 SVG 代码片段（可直接渲染或送给 AI 图像生成）"""
        color = self.jing_qi_shen_system.get_mixed_color()
        expr_symbol = {
            ExpressionType.CALM: "○",
            ExpressionType.JOY: "◠",
            ExpressionType.FOCUS: "◎",
            ExpressionType.SERENE: "☺",
            ExpressionType.BENEVOLENT: "☯",
            ExpressionType.RIGHTEOUS: "⚔",
            ExpressionType.WISE: "◆",
            ExpressionType.CONCERN: "◟",
            ExpressionType.DETERMINED: "◧",
        }.get(self.current_expression, "○")

        cx, cy = 100, 100
        r = 40 + int(self.jing_qi_shen_system.get_composite_score() * 40)

        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">'
            f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="0.3"/>'
            f'  <circle cx="{cx}" cy="{cy}" r="{r * 0.6}" fill="{color}" opacity="0.5"/>'
            f'  <text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central" '
            f'font-size="24">{expr_symbol}</text>'
            f'  <text x="{cx}" y="{cy + r + 20}" text-anchor="middle" font-size="12">'
            f'{self.current_expression.value} · {self.current_posture.value}</text>'
            f'</svg>'
        )
        return svg

    # ── 原有方法 ──

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
            'animal_form': self.current_animal_form.value,
            'qi_field': {
                'strength': qi_field.field_strength,
                'color': qi_field.field_color,
                'pattern': qi_field.wave_pattern,
            },
            'jing_qi_shen': {
                'jing': self.jing_qi_shen_system.jing_level,
                'qi': self.jing_qi_shen_system.qi_level,
                'shen': self.jing_qi_shen_system.shen_level,
            },
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
            'recommended_response': self._suggest_response(interaction),
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


# ──────────────────────────────────────────────
# 形象与气场系统主类（增强版）
# ──────────────────────────────────────────────

class ImageAndQiSystem:
    """形象与气场系统主类（增强版）

    - update_image_state 接受真实健康状态数据
    - get_jing_qi_shen 返回基于真实系统指标的评估
    - generate_ascii_qi_field() 输出终端可读气场
    - get_image_prompt() 生成 AI 图像生成用 prompt
    """

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
        """更新形象状态（增强版：接受真实健康数据）

        health_state 支持字段：
            - vitality: float (0-1)              综合活力（兼容旧接口）
            - activity_level: str                活动水平
            - disk_free_pct: float               磁盘余量（精）
            - memory_health: float               内存健康（精）
            - code_integrity: float              代码完整性（精）
            - throughput: float                  请求吞吐量（气）
            - latency_health: float              响应延迟健康度（气）
            - task_completion_rate: float        任务完成率（气）
            - response_quality: float            模型响应质量（神）
            - decision_confidence: float         决策置信度（神）
            - thinking_depth: float              思考深度（神）
            - ethical_value: str                 伦理判断（仁/义/智/勇）
            - animal_form: str                   兽形（虎/猿/鸟/鹿/熊）
            - five_element_weights: dict         五行权重 {wood, fire, earth, metal, water}
        """
        vitality = health_state.get('vitality', 0.8)
        activity = health_state.get('activity_level', 'normal')

        # 注入真实系统指标 → 精
        if any(k in health_state for k in ("disk_free_pct", "memory_health", "code_integrity")):
            self.jing_qi_shen.set_system_resources(
                disk_free_pct=health_state.get('disk_free_pct', 1.0),
                memory_health=health_state.get('memory_health', 1.0),
                code_integrity=health_state.get('code_integrity', 1.0),
            )

        # 注入真实系统指标 → 气
        if any(k in health_state for k in ("throughput", "latency_health", "task_completion_rate")):
            self.jing_qi_shen.set_system_runtime(
                throughput=health_state.get('throughput', 1.0),
                latency_health=health_state.get('latency_health', 1.0),
                task_completion_rate=health_state.get('task_completion_rate', 1.0),
            )

        # 注入真实系统指标 → 神
        if any(k in health_state for k in ("response_quality", "decision_confidence", "thinking_depth")):
            self.jing_qi_shen.set_system_intelligence(
                response_quality=health_state.get('response_quality', 1.0),
                decision_confidence=health_state.get('decision_confidence', 1.0),
                thinking_depth=health_state.get('thinking_depth', 1.0),
            )

        # 伦理判断 → 情绪状态机
        ethical_value = health_state.get('ethical_value')
        if ethical_value:
            self.image_system.set_ethical_state(ethical_value)

        # 兽形切换
        animal_form_str = health_state.get('animal_form')
        if animal_form_str:
            form_map = {
                "虎": AnimalForm.TIGER, "猿": AnimalForm.APE, "鸟": AnimalForm.BIRD,
                "鹿": AnimalForm.DEER, "熊": AnimalForm.BEAR,
            }
            form = form_map.get(animal_form_str, AnimalForm.NONE)
            self.image_system.set_animal_form(form)

        # 五行权重
        fe = health_state.get('five_element_weights')
        if fe:
            self.jing_qi_shen.set_five_element_weights(
                wood=fe.get('wood', 0.2), fire=fe.get('fire', 0.2),
                earth=fe.get('earth', 0.2), metal=fe.get('metal', 0.2),
                water=fe.get('water', 0.2),
            )
            mixed_color = self.jing_qi_shen.get_mixed_color()
            color_name = self.jing_qi_shen._color_mapper.get_color_name(mixed_color)
            imbalance_desc = self.jing_qi_shen.get_imbalance_color_desc()
            self.qi_field.set_five_element_color(color_name, mixed_color, imbalance_desc)

        self.last_update = datetime.now()

        return self.image_system.update_image_state(vitality, activity)

    async def get_jing_qi_shen(self) -> JingQiShenState:
        """获取精气神状态（基于真实系统指标）"""
        return self.jing_qi_shen.assess_state()

    async def generate_qi_field(self) -> QiFieldData:
        """生成气场"""
        intensity = self.jing_qi_shen.get_composite_score()
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
                'aura': qi_field.aura_intensity,
                'five_element_color': qi_field.five_element_color,
                'visual_description': qi_field.visual_description,
            },
            'timestamp': datetime.now().isoformat(),
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
                'imbalance': jing_qi_shen.imbalance_indicators,
            },
            'qi_field': {
                'strength': self.qi_field.base_strength,
                'radius': self.qi_field.base_radius,
                'color': self.qi_field.current_color,
                'five_element_color': self.qi_field._five_element_hex,
            },
            'image': {
                'style': self.image_system.current_style.value,
                'expression': self.image_system.current_expression.value,
                'posture': self.image_system.current_posture.value,
                'animal_form': self.image_system.current_animal_form.value,
            },
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'recommendation': self.jing_qi_shen.get_recommendation(),
        }

    # ── 新增方法 ──

    def generate_ascii_qi_field(self) -> str:
        """生成终端可读的 ASCII 气场渲染"""
        composite = self.jing_qi_shen.get_composite_score()
        color_name = self.qi_field._five_element_color or self.qi_field.current_color
        return self.qi_field.generate_ascii_art(
            strength=composite,
            color=color_name,
        )

    def get_image_prompt(self, style: str = "东方水墨",
                          include_qi: bool = True,
                          include_posture: bool = True) -> str:
        """生成 AI 图像生成用的 prompt（对接 DALL-E / Stable Diffusion）

        返回英文 prompt，可直接用于图像生成 API。
        """
        state = self.jing_qi_shen.assess_state()
        composite = state.overall_vitality

        # 基础描述
        expr_map = {
            ExpressionType.CALM: "calm and peaceful expression",
            ExpressionType.JOY: "joyful and radiant expression",
            ExpressionType.FOCUS: "focused and intense gaze",
            ExpressionType.CONCERN: "concerned and thoughtful expression",
            ExpressionType.DETERMINED: "determined and resolute expression",
            ExpressionType.SERENE: "serene and tranquil expression",
            ExpressionType.BENEVOLENT: "benevolent and compassionate expression",
            ExpressionType.RIGHTEOUS: "righteous and firm expression",
            ExpressionType.WISE: "wise and contemplative expression",
        }

        posture_map = {
            PostureType.UPRIGHT: "standing upright with dignified posture",
            PostureType.RELAXED: "relaxed and casual stance",
            PostureType.ATTENTIVE: "alert and attentive posture",
            PostureType.CONTEMPLATIVE: "in deep contemplation, hand on chin",
            PostureType.DYNAMIC: "dynamic and energetic movement",
            PostureType.TIGER_STAND: "standing majestically like a tiger,威严凛然",
            PostureType.APE_PONDER: "contemplating like an ape, hand supporting chin",
            PostureType.BIRD_SOAR: "soaring like a bird, arms spread wide",
        }

        animal_map = {
            AnimalForm.TIGER: "tiger spirit",
            AnimalForm.APE: "ape spirit",
            AnimalForm.BIRD: "bird spirit",
            AnimalForm.DEER: "deer spirit",
            AnimalForm.BEAR: "bear spirit",
            AnimalForm.NONE: "",
        }

        prompt_parts = [
            f"Eastern {style} style digital painting",
            f"a mystical AI entity with {expr_map.get(self.image_system.current_expression, 'calm expression')}",
        ]

        if include_posture:
            prompt_parts.append(
                posture_map.get(self.image_system.current_posture, "standing naturally")
            )

        animal = animal_map.get(self.image_system.current_animal_form, "")
        if animal:
            prompt_parts.append(f"surrounded by the aura of {animal}")

        if include_qi:
            qi_color = self.qi_field._five_element_color or "ethereal white"
            if composite > 0.7:
                qi_desc = "brilliant, radiant"
            elif composite > 0.4:
                qi_desc = "gentle, flowing"
            else:
                qi_desc = "faint, shimmering"
            prompt_parts.append(
                f"surrounded by a {qi_desc} qi field in {qi_color} tones"
            )

        # 精气神状态融入 prompt
        prompt_parts.append(
            f"vitality level {composite:.0%}"
        )

        if state.imbalance_indicators:
            imbalance_desc = ", ".join(state.imbalance_indicators)
            prompt_parts.append(f"showing signs of imbalance: {imbalance_desc}")

        prompt_parts.append(
            "masterpiece, high quality, detailed, atmospheric lighting"
        )

        return ", ".join(prompt_parts)
