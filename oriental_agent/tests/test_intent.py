"""意图路由。只依赖启发式函数，不拉起完整对话循环。"""

from core.agent import _detect_intent


def _primary(text: str) -> str:
    intents = _detect_intent(text)
    assert intents, text
    return intents[0][0]


def test_investment_phrase_routes_to_investment():
    intents = dict(_detect_intent("我想投资10万"))
    assert "investment" in intents
    assert intents["investment"] >= 0.85
    assert _primary("我想投资10万") == "investment"


def test_investing_100k_routes_to_investment():
    assert _primary("I am investing 100k") == "investment"


def test_startup_and_investment_can_both_match():
    intents = dict(_detect_intent("我想创业投资"))
    assert "commercial_opportunity" in intents
    assert "investment" in intents


def test_prediction_and_hello():
    assert _primary("帮我起卦看看吉凶") == "prediction"
    assert _primary("你好") == "hello"
