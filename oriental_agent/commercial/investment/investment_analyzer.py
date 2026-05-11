"""
投资决策分析器
运筹帷幄，决胜千里
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import math

from commercial.types import InvestmentAnalysis, RiskLevel


@dataclass
class FinancialProjection:
    """财务预测"""
    year: int
    revenue: float
    costs: float
    profit: float
    cash_flow: float
    cumulative: float = 0.0


@dataclass
class InvestmentDecision:
    """投资决策"""
    decision_id: str = field(default_factory=lambda: str(datetime.now().timestamp()))
    project_name: str = ""
    recommendation: str = ""
    investment_rating: str = ""
    key_factors: List[str] = field(default_factory=list)
    risk_mitigation: List[str] = field(default_factory=list)
    alternative_scenarios: Dict[str, Any] = field(default_factory=dict)


class InvestmentAnalyzer:
    """投资决策分析器"""

    def __init__(self, discount_rate: float = 0.10):
        self.discount_rate = discount_rate
        self._projects: Dict[str, InvestmentAnalysis] = {}
        self._decisions: Dict[str, InvestmentDecision] = {}

    def analyze_investment(
        self,
        project_data: Dict[str, Any]
    ) -> InvestmentAnalysis:
        """
        分析投资项目
        
        Args:
            project_data: 项目数据
            
        Returns:
            投资分析结果
        """
        initial = project_data.get("initial_investment", 0.0)
        cash_flows = project_data.get("annual_cash_flows", [])
        discount_rate = project_data.get("discount_rate", self.discount_rate)
        risk_level = project_data.get("risk_level", RiskLevel.MEDIUM)
        
        roi = self._calculate_roi(initial, cash_flows)
        payback = self._calculate_payback(initial, cash_flows)
        npv = self._calculate_npv(initial, cash_flows, discount_rate)
        irr = self._calculate_irr(initial, cash_flows)
        
        analysis = InvestmentAnalysis(
            project_name=project_data.get("name", "未知项目"),
            initial_investment=initial,
            expected_return=sum(cash_flows) - initial,
            roi=roi,
            payback_period=payback,
            npv=npv,
            irr=irr,
            risk_assessment=risk_level,
            recommendation=self._generate_recommendation(roi, npv, irr, risk_level),
            factors={
                "roi_analysis": self._detailed_roi_analysis(initial, cash_flows),
                "risk_factors": self._identify_investment_risks(project_data),
                "sensitivity": self._sensitivity_analysis(initial, cash_flows, discount_rate)
            }
        )
        
        self._projects[analysis.project_name] = analysis
        return analysis

    def make_decision(
        self,
        project_data: Dict[str, Any]
    ) -> InvestmentDecision:
        """做出投资决策"""
        analysis = self.analyze_investment(project_data)
        
        rating = "B"
        if analysis.npv > 0 and analysis.irr > self.discount_rate:
            rating = "A"
            recommendation = "强烈推荐：项目具有良好的投资价值"
        elif analysis.npv > 0 or analysis.irr > self.discount_rate:
            rating = "B"
            recommendation = "建议投资：项目基本可行，需关注风险"
        elif analysis.payback_period < 3:
            rating = "C"
            recommendation = "谨慎投资：短期回报可期，长期不确定性大"
        else:
            rating = "D"
            recommendation = "不建议投资：项目风险大于收益"
        
        decision = InvestmentDecision(
            project_name=project_data.get("name", "未知项目"),
            recommendation=recommendation,
            investment_rating=rating,
            key_factors=self._extract_key_factors(analysis),
            risk_mitigation=self._propose_risk_mitigation(project_data),
            alternative_scenarios=self._generate_scenarios(project_data)
        )
        
        self._decisions[decision.project_name] = decision
        return decision

    def compare_investments(
        self,
        projects: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """比较多个投资项目"""
        analyses = [self.analyze_investment(p) for p in projects]
        
        if not analyses:
            return {}
        
        best_roi = max(analyses, key=lambda x: x.roi)
        best_npv = max(analyses, key=lambda x: x.npv)
        lowest_risk = min(analyses, key=lambda x: x.risk_assessment.value)
        
        risk_map = {"低风险": 0.1, "中风险": 0.5, "高风险": 0.8, "极高风险": 1.0}
        
        def risk_score(x):
            return risk_map.get(x.risk_assessment.value, 0.5)
        
        def composite_score(x):
            return x.npv * 0.4 + x.roi * 0.3 - risk_score(x) * 0.3
        
        rankings = sorted(analyses, key=composite_score, reverse=True)
        
        return {
            "analyses": analyses,
            "rankings": [
                {"name": a.project_name, "composite_score": composite_score(a)}
                for a in rankings
            ],
            "best_roi": best_roi.project_name,
            "best_npv": best_npv.project_name,
            "lowest_risk": lowest_risk.project_name,
            "recommendation": rankings[0].project_name if rankings else None
        }

    def portfolio_analysis(
        self,
        investments: List[Dict[str, Any]],
        correlation: float = 0.3
    ) -> Dict[str, Any]:
        """投资组合分析"""
        analyses = [self.analyze_investment(inv) for inv in investments]
        
        total_investment = sum(a.initial_investment for a in analyses)
        total_expected = sum(a.expected_return for a in analyses)
        
        weights = [a.initial_investment / total_investment for a in analyses]
        
        portfolio_return = sum(w * a.roi for w, a in zip(weights, analyses))
        
        risk_variance = 0.0
        for i, a1 in enumerate(analyses):
            for j, a2 in enumerate(analyses):
                if i != j:
                    risk_variance += weights[i] * weights[j] * correlation
        
        portfolio_risk = math.sqrt(risk_variance)
        
        sharpe = (portfolio_return - self.discount_rate) / portfolio_risk if portfolio_risk > 0 else 0
        
        return {
            "total_investment": total_investment,
            "expected_return": total_expected,
            "portfolio_return": portfolio_return,
            "portfolio_risk": portfolio_risk,
            "sharpe_ratio": sharpe,
            "diversification_benefit": self._calculate_diversification(analyses, weights),
            "recommendation": self._portfolio_recommendation(sharpe, portfolio_risk)
        }

    def _calculate_roi(self, initial: float, cash_flows: List[float]) -> float:
        """计算投资回报率"""
        if initial == 0:
            return 0.0
        total_return = sum(cash_flows) - initial
        return total_return / initial

    def _calculate_payback(self, initial: float, cash_flows: List[float]) -> float:
        """计算回收期"""
        cumulative = 0.0
        for i, cf in enumerate(cash_flows):
            cumulative += cf
            if cumulative >= initial:
                remaining = initial - (cumulative - cf)
                return i + (remaining / cf if cf != 0 else 0)
        return len(cash_flows) + 1

    def _calculate_npv(
        self,
        initial: float,
        cash_flows: List[float],
        rate: float
    ) -> float:
        """计算净现值"""
        npv = -initial
        for i, cf in enumerate(cash_flows):
            npv += cf / math.pow(1 + rate, i + 1)
        return npv

    def _calculate_irr(self, initial: float, cash_flows: List[float]) -> float:
        """计算内部收益率"""
        if initial == 0:
            return 0.0
        
        flows = [-initial] + cash_flows
        min_rate, max_rate = -0.9, 10.0
        
        for _ in range(100):
            mid_rate = (min_rate + max_rate) / 2
            npv = sum(cf / math.pow(1 + mid_rate, i) for i, cf in enumerate(flows))
            
            if abs(npv) < 0.01:
                return mid_rate
            
            if npv > 0:
                min_rate = mid_rate
            else:
                max_rate = mid_rate
        
        return (min_rate + max_rate) / 2

    def _generate_recommendation(
        self,
        roi: float,
        npv: float,
        irr: float,
        risk: RiskLevel
    ) -> str:
        """生成投资建议"""
        score = 0
        
        if roi > 0.2:
            score += 3
        elif roi > 0.1:
            score += 2
        elif roi > 0:
            score += 1
            
        if npv > 0:
            score += 2
            
        if irr > self.discount_rate:
            score += 2
            
        if risk == RiskLevel.LOW:
            score += 2
        elif risk == RiskLevel.MEDIUM:
            score += 1
            
        if score >= 7:
            return "★★★★★ 强烈推荐：优质投资项目"
        elif score >= 5:
            return "★★★★ 推荐投资：项目可行"
        elif score >= 3:
            return "★★★ 谨慎投资：需要更多论证"
        else:
            return "★★ 不建议投资：风险较高"

    def _detailed_roi_analysis(
        self,
        initial: float,
        cash_flows: List[float]
    ) -> Dict[str, Any]:
        """详细ROI分析"""
        projections = []
        cumulative = 0.0
        
        for i, cf in enumerate(cash_flows):
            cumulative += cf
            projections.append(FinancialProjection(
                year=i + 1,
                revenue=cf * 1.5,
                costs=cf * 0.5,
                profit=cf,
                cash_flow=cf,
                cumulative=cumulative
            ))
        
        return {
            "projections": projections,
            "total_roi": self._calculate_roi(initial, cash_flows),
            "average_annual_return": sum(cash_flows) / len(cash_flows) / initial if initial > 0 else 0
        }

    def _identify_investment_risks(self, project_data: Dict[str, Any]) -> List[str]:
        """识别投资风险"""
        risks = []
        
        if project_data.get("market_volatility", 0) > 0.5:
            risks.append("市场波动风险")
        if project_data.get("technology_risk", False):
            risks.append("技术风险")
        if project_data.get("regulatory_risk", False):
            risks.append("政策监管风险")
        if project_data.get("execution_risk", False):
            risks.append("执行风险")
            
        return risks

    def _sensitivity_analysis(
        self,
        initial: float,
        cash_flows: List[float],
        base_rate: float
    ) -> Dict[str, Any]:
        """敏感性分析"""
        variations = [-0.2, -0.1, 0.1, 0.2]
        
        sensitivity = {}
        for var in variations:
            adjusted_flows = [cf * (1 + var) for cf in cash_flows]
            npv = self._calculate_npv(initial, adjusted_flows, base_rate)
            sensitivity[f"revenue_{int(var*100)}%"] = npv
        
        for var in variations:
            adjusted_rate = base_rate * (1 + var)
            npv = self._calculate_npv(initial, cash_flows, adjusted_rate)
            sensitivity[f"rate_{int(var*100)}%"] = npv
            
        return sensitivity

    def _extract_key_factors(self, analysis: InvestmentAnalysis) -> List[str]:
        """提取关键因素"""
        factors = []
        
        if analysis.roi > 0.2:
            factors.append(f"高ROI：{analysis.roi:.1%}")
        if analysis.npv > 0:
            factors.append(f"正NPV：{analysis.npv:,.0f}")
        factors.append(f"回收期：{analysis.payback_period:.1f}年")
        factors.append(f"IRR：{analysis.irr:.1%}")
        
        return factors

    def _propose_risk_mitigation(self, project_data: Dict[str, Any]) -> List[str]:
        """建议风险缓解措施"""
        measures = [
            "分阶段投资，降低单次投入风险",
            "建立项目监控机制",
            "预留应急资金",
            "制定退出策略"
        ]
        
        if project_data.get("technology_risk", False):
            measures.append("引入技术专家评审")
        if project_data.get("market_volatility", 0) > 0.5:
            measures.append("增加市场调研频次")
            
        return measures

    def _generate_scenarios(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成情景分析"""
        base_flows = project_data.get("annual_cash_flows", [])
        
        optimistic = [cf * 1.3 for cf in base_flows]
        pessimistic = [cf * 0.7 for cf in base_flows]
        
        return {
            "optimistic": {
                "npv": self._calculate_npv(
                    project_data["initial_investment"],
                    optimistic,
                    project_data.get("discount_rate", self.discount_rate)
                ),
                "payback": self._calculate_payback(
                    project_data["initial_investment"],
                    optimistic
                )
            },
            "pessimistic": {
                "npv": self._calculate_npv(
                    project_data["initial_investment"],
                    pessimistic,
                    project_data.get("discount_rate", self.discount_rate)
                ),
                "payback": self._calculate_payback(
                    project_data["initial_investment"],
                    pessimistic
                )
            },
            "break_even": self._calculate_payback(
                project_data["initial_investment"],
                [sum(base_flows) / len(base_flows)] * len(base_flows)
            )
        }

    def _calculate_diversification(
        self,
        analyses: List[InvestmentAnalysis],
        weights: List[float]
    ) -> str:
        """计算分散化收益"""
        weighted_return = sum(w * a.roi for w, a in zip(weights, analyses))
        
        if len(analyses) > 1:
            return f"组合回报 {weighted_return:.1%}，优于单一投资"
        return "分散化效果有限"

    def _portfolio_recommendation(self, sharpe: float, risk: float) -> str:
        """组合投资建议"""
        if sharpe > 1:
            return "投资组合优秀，风险调整后收益高"
        elif sharpe > 0.5:
            return "投资组合良好，具备投资价值"
        elif risk < 0.3:
            return "低风险投资组合，适合稳健型投资者"
        else:
            return "建议调整组合结构，提高风险调整后收益"
