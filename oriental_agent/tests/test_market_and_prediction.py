"""商机不编造收入；预测默认带启发式免责声明。"""

from commercial.agent import CommercialAgent
from commercial.insight.market_insight import MarketInsightEngine
from prediction.prediction_engine import HEURISTIC_DISCLAIMER, PredictionEngine


def test_no_market_data_says_insufficient():
    engine = MarketInsightEngine()
    opportunities = engine.analyze_market({})
    assert opportunities == []
    assert engine.last_data_status == "数据不足"

    result = CommercialAgent().analyze_opportunity({"query": "现在有什么商机"})
    assert result["data_status"] == "数据不足"
    assert "数据不足" in result["message"]
    assert result["opportunities"] == []


def test_signal_without_revenue_does_not_invent_amount():
    engine = MarketInsightEngine()
    opportunities = engine.analyze_market({"unmet_needs": ["夜间配送"]})
    assert len(opportunities) == 1
    assert opportunities[0].potential_revenue == 0
    assert opportunities[0].market_indicators["revenue_status"] == "数据不足"
    assert "数据不足" in opportunities[0].description


def test_provided_revenue_is_kept():
    engine = MarketInsightEngine()
    opportunities = engine.analyze_market({
        "unmet_needs": ["夜间配送"],
        "potential_revenue": 250000,
    })
    assert opportunities[0].potential_revenue == 250000
    assert opportunities[0].market_indicators["revenue_status"] == "已提供"


def test_prediction_disclaimer_on_by_default():
    engine = PredictionEngine()
    result = engine.predict("这个项目能成吗")
    assert engine.include_heuristic_disclaimer is True
    assert HEURISTIC_DISCLAIMER in result.interpretation
    assert result.heuristic_disclaimer == HEURISTIC_DISCLAIMER
    payload = result.to_dict()
    assert payload["disclaimer"] == HEURISTIC_DISCLAIMER
    assert payload["heuristic"] is True


def test_prediction_is_stable_for_the_same_query():
    engine_a = PredictionEngine()
    engine_b = PredictionEngine()
    first = engine_a.predict("这个项目能成吗")
    second = engine_b.predict("这个项目能成吗")
    assert first.confidence == second.confidence
    assert first.interpretation == second.interpretation


def test_prediction_disclaimer_can_be_disabled():
    engine = PredictionEngine(include_heuristic_disclaimer=False)
    result = engine.predict("这个项目能成吗")
    assert HEURISTIC_DISCLAIMER not in result.interpretation
    assert result.heuristic_disclaimer == ""
    assert "disclaimer" not in result.to_dict()
