"""
五行、八识进入路由和记忆衰减的可测约定。

五行：当前旺的一行对记忆所属一行做生克，改变这一步的衰减倍率。
    相生（旺行生记忆行）衰减更慢，相克（旺行克记忆行）衰减更快，其余为中性。
    方向以 memory.wuxing.WuxingSystem 的生克表为准，不另造一套。

八识：各识激活度在 0 到 1 之间，按固定权重加到意图置信度上，结果再夹到 [0, 1]。
    激活度为 0 时不改变已有意图。前五识与末那、阿赖耶不给「投资」加分。
"""

from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from core.types import WuxingRelation, WuxingType
from memory.wuxing import WuxingSystem
from perception.eight_consciousness import ConsciousnessLevel

# 中性一步去掉的强度比例。相生打 0.5 折，相克打 1.5 倍。
BASE_DECAY = 0.05
GENERATE_DECAY_FACTOR = 0.5
RESTRICT_DECAY_FACTOR = 1.5
NEUTRAL_DECAY_FACTOR = 1.0

# 八识激活度 1.0 时加到对应意图上的置信度。投资不在表内。
EIGHT_CONSCIOUSNESS_ROUTING: Dict[ConsciousnessLevel, Dict[str, float]] = {
    ConsciousnessLevel.EYE: {"commercial_opportunity": 0.06},
    ConsciousnessLevel.EAR: {"relationship": 0.06},
    ConsciousnessLevel.NOSE: {"body_health": 0.04},
    ConsciousnessLevel.TONGUE: {"body_health": 0.04},
    ConsciousnessLevel.BODY: {"body_health": 0.12},
    ConsciousnessLevel.MIND: {"strategy": 0.10, "wisdom_advice": 0.06},
    ConsciousnessLevel.MANAS: {"emotion_support": 0.12},
    ConsciousnessLevel.ALAYA: {"prediction": 0.10, "cultivation": 0.06},
}

_ACTIVATION_CUES: Tuple[Tuple[ConsciousnessLevel, Tuple[str, ...]], ...] = (
    (ConsciousnessLevel.BODY, ("身体", "健康", "养生", "经络", "失眠")),
    (ConsciousnessLevel.MANAS, ("焦虑", "我自己", "自我", "情绪", "心情")),
    (ConsciousnessLevel.ALAYA, ("预测", "起卦", "卦", "因果", "吉凶")),
    (ConsciousnessLevel.MIND, ("战略", "怎么想", "分析", "布局")),
    (ConsciousnessLevel.EYE, ("看到", "看见")),
    (ConsciousnessLevel.EAR, ("听到", "听说")),
    (ConsciousnessLevel.NOSE, ("闻到",)),
    (ConsciousnessLevel.TONGUE, ("尝到", "味道")),
)


def wuxing_decay_factor(active: Optional[WuxingType], memory_element: WuxingType) -> float:
    """旺行对记忆行的衰减倍率。active 为空时保持中性。"""
    if active is None:
        return NEUTRAL_DECAY_FACTOR
    relation = WuxingSystem().get_relation(active, memory_element)
    if relation == WuxingRelation.GENERATE:
        return GENERATE_DECAY_FACTOR
    if relation == WuxingRelation.RESTRICT:
        return RESTRICT_DECAY_FACTOR
    return NEUTRAL_DECAY_FACTOR


def apply_wuxing_decay(
    strength: float,
    active: Optional[WuxingType],
    memory_element: WuxingType,
    base_decay: float = BASE_DECAY,
) -> float:
    """按生克倍率衰减强度。结果不小于 0，也不大于原强度。"""
    current = max(0.0, float(strength))
    rate = max(0.0, float(base_decay)) * wuxing_decay_factor(active, memory_element)
    if rate > 1.0:
        rate = 1.0
    return current * (1.0 - rate)


def infer_consciousness_activations(text: str) -> Dict[ConsciousnessLevel, float]:
    """从话语线索读八识激活。没有线索的识为 0，不凭空抬路由。"""
    activations = {level: 0.0 for level in ConsciousnessLevel}
    if not text:
        return activations
    for level, cues in _ACTIVATION_CUES:
        hits = sum(1 for cue in cues if cue in text)
        if hits:
            activations[level] = min(1.0, 0.5 + 0.25 * (hits - 1))
    return activations


def consciousness_intent_bonus(activations: Mapping[ConsciousnessLevel, float]) -> Dict[str, float]:
    """把八识激活度换成各意图的加分。激活度夹到 [0, 1]。"""
    bonuses: Dict[str, float] = {}
    for level, weight_map in EIGHT_CONSCIOUSNESS_ROUTING.items():
        raw = activations.get(level, 0.0) if activations else 0.0
        try:
            activation = float(raw)
        except (TypeError, ValueError):
            activation = 0.0
        activation = max(0.0, min(1.0, activation))
        if activation == 0.0:
            continue
        for intent, weight in weight_map.items():
            bonuses[intent] = bonuses.get(intent, 0.0) + activation * weight
    return bonuses


def apply_consciousness_routing(
    intents: Sequence[Tuple[str, float]],
    activations: Optional[Mapping[ConsciousnessLevel, float]] = None,
) -> List[Tuple[str, float]]:
    """按八识加分调整意图置信度，并按置信度从高到低排列。"""
    bonuses = consciousness_intent_bonus(activations or {})
    adjusted: List[Tuple[str, float]] = []
    seen = set()
    for intent, confidence in intents:
        try:
            value = float(confidence)
        except (TypeError, ValueError):
            value = 0.0
        value = min(1.0, max(0.0, value + bonuses.get(intent, 0.0)))
        adjusted.append((intent, value))
        seen.add(intent)
    for intent, bonus in bonuses.items():
        if intent not in seen and bonus > 0:
            adjusted.append((intent, min(1.0, bonus)))
    adjusted.sort(key=lambda item: -item[1])
    return adjusted


def intents_receiving_bonus(levels: Iterable[ConsciousnessLevel]) -> set:
    names = set()
    for level in levels:
        names.update(EIGHT_CONSCIOUSNESS_ROUTING.get(level, {}))
    return names
