"""投资计算与自然语言回归。"""

import pytest

from commercial.agent import CommercialAgent
from commercial.investment.investment_analyzer import (
    InvestmentAnalyzer,
    normalize_project_data,
    parse_initial_investment,
)
from commercial.types import RiskLevel


def test_roi_npv_irr_known_cashflows():
    analyzer = InvestmentAnalyzer(discount_rate=0.10)
    result = analyzer.analyze_investment({
        "name": "样例项目",
        "initial_investment": 100000,
        "annual_cash_flows": [40000, 40000, 40000],
        "discount_rate": 0.10,
        "risk_level": RiskLevel.MEDIUM,
    })

    assert result.roi == pytest.approx(0.2)
    # NPV = -100000 + 40000/1.1 + 40000/1.1^2 + 40000/1.1^3
    expected_npv = (
        -100000
        + 40000 / 1.1
        + 40000 / (1.1 ** 2)
        + 40000 / (1.1 ** 3)
    )
    assert result.npv == pytest.approx(expected_npv, rel=1e-6)
    assert result.payback_period == pytest.approx(2.5)
    # 9% 时 NPV 为正，10% 时为负，IRR 落在两者之间
    assert 0.09 < result.irr < 0.10
    assert result.initial_investment == 100000


def test_chinese_10_wan_does_not_keyerror():
    text = "我想投资10万"
    assert parse_initial_investment(text) == pytest.approx(100000)

    analyzer = InvestmentAnalyzer()
    # 旧路径在 _generate_scenarios 里直接取 project_data["initial_investment"]
    scenarios = analyzer._generate_scenarios({"query": text})
    assert "optimistic" in scenarios

    decision = analyzer.make_decision({"query": text})
    assert decision.investment_rating == "N/A"
    assert "数据不足" in decision.recommendation

    agent = CommercialAgent()
    result = agent.analyze_investment({"query": text})
    assert "error" not in result
    assert result["initial_investment"] == pytest.approx(100000)
    assert result["parsed_from_text"] is True
    assert result["irr"] == pytest.approx(0.0)
    assert any("现金流" in item for item in result["warnings"])


def test_investing_100k_and_chinese_numerals():
    assert parse_initial_investment("I am investing 100k") == pytest.approx(100000)
    assert parse_initial_investment("投资一百万") == pytest.approx(1_000_000)
    assert parse_initial_investment("投入十万") == pytest.approx(100_000)

    result = CommercialAgent().analyze_investment({"query": "investing 100k into this project"})
    assert result["initial_investment"] == pytest.approx(100000)
    assert "error" not in result


def test_missing_investment_returns_clear_error():
    analyzer = InvestmentAnalyzer()
    decision = analyzer.make_decision({"query": "帮我看看这个想法"})
    assert "initial_investment" in decision.recommendation

    result = CommercialAgent().analyze_investment({})
    assert "initial_investment" in result["error"]
    assert result["data_status"] == "数据不足"
    defaults = result["defaults"]
    assert defaults["initial_investment"] is None
    assert defaults["annual_cash_flows"] == []
    assert defaults["discount_rate"] == pytest.approx(0.10)
    assert defaults["name"] == "未知项目"


def test_cashflow_sentence_is_parsed():
    prepared = normalize_project_data({
        "query": "投资10万，每年回报3万，连续4年，折现率10%",
    })
    assert prepared["error"] is None
    assert prepared["initial_investment"] == pytest.approx(100000)
    assert prepared["annual_cash_flows"] == [30000, 30000, 30000, 30000]
    assert prepared["discount_rate"] == pytest.approx(0.10)

    analysis = InvestmentAnalyzer().analyze_investment(prepared)
    flows = [30000, 30000, 30000, 30000]
    assert analysis.roi == pytest.approx((sum(flows) - 100000) / 100000)
    expected_npv = -100000 + sum(cf / (1.1 ** (index + 1)) for index, cf in enumerate(flows))
    assert analysis.npv == pytest.approx(expected_npv, rel=1e-6)
    assert analysis.irr > 0
