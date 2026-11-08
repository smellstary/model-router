"""五行衰减与八识路由的不变量。"""

import pytest

from core.agent import _detect_intent
from core.metaphor_invariants import (
    BASE_DECAY,
    EIGHT_CONSCIOUSNESS_ROUTING,
    GENERATE_DECAY_FACTOR,
    RESTRICT_DECAY_FACTOR,
    apply_consciousness_routing,
    apply_wuxing_decay,
    consciousness_intent_bonus,
    infer_consciousness_activations,
    wuxing_decay_factor,
)
from core.types import WuxingType
from memory.wuxing import WuxingSystem
from perception.eight_consciousness import ConsciousnessLevel


def test_generation_and_restriction_directions_match_wuxing_table():
    system = WuxingSystem()
    assert system.GENERATION_CYCLE[WuxingType.WOOD] == WuxingType.FIRE
    assert system.RESTRICTION_CYCLE[WuxingType.WOOD] == WuxingType.EARTH
    assert wuxing_decay_factor(WuxingType.WOOD, WuxingType.FIRE) == GENERATE_DECAY_FACTOR
    assert wuxing_decay_factor(WuxingType.WOOD, WuxingType.EARTH) == RESTRICT_DECAY_FACTOR
    assert wuxing_decay_factor(WuxingType.WOOD, WuxingType.WOOD) == 1.0
    assert wuxing_decay_factor(None, WuxingType.FIRE) == 1.0


def test_decay_orders_generate_slower_than_restrict():
    start = 1.0
    generated = apply_wuxing_decay(start, WuxingType.WOOD, WuxingType.FIRE)
    neutral = apply_wuxing_decay(start, WuxingType.WOOD, WuxingType.WOOD)
    restricted = apply_wuxing_decay(start, WuxingType.WOOD, WuxingType.EARTH)

    assert generated == pytest.approx(start * (1 - BASE_DECAY * GENERATE_DECAY_FACTOR))
    assert restricted == pytest.approx(start * (1 - BASE_DECAY * RESTRICT_DECAY_FACTOR))
    assert generated > neutral > restricted
    assert restricted >= 0.0


def test_decay_is_monotone_and_deterministic():
    once = apply_wuxing_decay(0.8, WuxingType.WATER, WuxingType.WOOD)
    twice = apply_wuxing_decay(once, WuxingType.WATER, WuxingType.WOOD)
    again = apply_wuxing_decay(0.8, WuxingType.WATER, WuxingType.WOOD)
    assert 0.0 <= twice < once < 0.8
    assert once == again
    assert apply_wuxing_decay(0.0, WuxingType.METAL, WuxingType.WOOD) == 0.0


def test_zero_consciousness_activation_does_not_change_routing():
    intents = [("investment", 0.85), ("hello", 0.6)]
    zeros = {level: 0.0 for level in ConsciousnessLevel}
    assert apply_consciousness_routing(intents, zeros) == intents
    assert apply_consciousness_routing(intents, None) == intents


def test_body_activation_raises_only_its_route_and_stays_in_range():
    intents = [("body_health", 0.7), ("investment", 0.85)]
    low = apply_consciousness_routing(intents, {ConsciousnessLevel.BODY: 0.0})
    high = apply_consciousness_routing(intents, {ConsciousnessLevel.BODY: 1.0})
    low_map = dict(low)
    high_map = dict(high)
    assert high_map["body_health"] == pytest.approx(0.82)
    assert high_map["body_health"] > low_map["body_health"]
    assert high_map["investment"] == low_map["investment"] == 0.85
    assert all(0.0 <= confidence <= 1.0 for _, confidence in high)


def test_consciousness_bonus_never_targets_investment():
    sensory = [
        ConsciousnessLevel.EYE,
        ConsciousnessLevel.EAR,
        ConsciousnessLevel.NOSE,
        ConsciousnessLevel.TONGUE,
        ConsciousnessLevel.BODY,
        ConsciousnessLevel.MANAS,
        ConsciousnessLevel.ALAYA,
        ConsciousnessLevel.MIND,
    ]
    for level in sensory:
        assert "investment" not in EIGHT_CONSCIOUSNESS_ROUTING.get(level, {})
    full = {level: 1.0 for level in ConsciousnessLevel}
    assert "investment" not in consciousness_intent_bonus(full)


def test_confidence_caps_at_one():
    routed = apply_consciousness_routing(
        [("body_health", 0.95)],
        {ConsciousnessLevel.BODY: 1.0},
    )
    assert dict(routed)["body_health"] == 1.0


def test_existing_intent_phrases_keep_their_primary_route():
    investment = "我想投资10万"
    routed_investment = apply_consciousness_routing(
        _detect_intent(investment),
        infer_consciousness_activations(investment),
    )
    assert routed_investment[0][0] == "investment"

    health = "我最近身体不舒服"
    raw = dict(_detect_intent(health))
    routed = dict(apply_consciousness_routing(
        _detect_intent(health),
        infer_consciousness_activations(health),
    ))
    assert routed["body_health"] > raw["body_health"]
    assert infer_consciousness_activations(health)[ConsciousnessLevel.BODY] > 0
