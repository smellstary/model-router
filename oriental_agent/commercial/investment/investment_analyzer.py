"""
投资决策分析器
运筹帷幄，决胜千里
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import math
import re

from commercial.types import InvestmentAnalysis, RiskLevel

# 自然语言金额：阿拉伯数字 + 单位，或中文数字
_INVEST_KEYWORD = (
    r'(?:投资|投入|本金|出资|初始投资|initial[_\s-]*investment|invest(?:ing|ed)?)'
)
_ARABIC_AMOUNT = re.compile(
    _INVEST_KEYWORD + r'\s*[:：为]?\s*(\d+(?:\.\d+)?)\s*(亿|万|千|百|k|K|w|W|元|块)?',
    re.IGNORECASE,
)
_CHINESE_AMOUNT = re.compile(
    r'(?:投资|投入|本金|出资|初始投资)\s*[:：为]?\s*'
    r'([零〇一二两三四五六七八九十百千万亿]+)'
)
_FALLBACK_AMOUNT = re.compile(
    r'(\d+(?:\.\d+)?)\s*(亿|万|千|k|K|w|W)',
    re.IGNORECASE,
)
_CASHFLOW_AMOUNT = re.compile(
    r'(?:每年|年(?:度)?(?:现金流|收益|回报|利润)|annual[_\s-]*cash[_\s-]*flows?)'
    r'\s*[:：]?\s*(\d+(?:\.\d+)?)\s*(亿|万|千|k|K|w|W)?',
    re.IGNORECASE,
)
_CASHFLOW_YEARS = re.compile(r'(?:连续|共)\s*(\d+)\s*年')
_DISCOUNT_RATE = re.compile(
    r'(?:折现率|贴现率|discount(?:\s*rate)?)\s*[:：]?\s*(\d+(?:\.\d+)?)\s*(%)?',
    re.IGNORECASE,
)
_CN_DIGITS = {
    '零': 0, '〇': 0, '一': 1, '二': 2, '两': 2, '三': 3,
    '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
}
_CN_SECTION = {'十': 10, '百': 100, '千': 1000}
_CN_BIG = {'万': 10_000, '亿': 100_000_000}
_TEXT_KEYS = ('query', 'text', 'message', 'description', 'input', 'question')
_DEFAULT_DISCOUNT_RATE = 0.10


def _apply_unit(number: float, unit: Optional[str]) -> float:
    """把 10万 / 100k / 1.5亿 换算成元。"""
    if not unit or unit in ('元', '块'):
        return float(number)
    key = unit.lower() if unit.isascii() else unit
    multiplier = {
        'k': 1_000,
        'w': 10_000,
        '百': 100,
        '千': 1_000,
        '万': 10_000,
        '亿': 100_000_000,
    }.get(key, 1)
    return float(number) * multiplier


def _chinese_to_number(text: str) -> Optional[float]:
    """解析「十万」「一百二十万」「两亿」这类中文金额。"""
    if not text:
        return None
    total = 0
    section = 0
    number = 0
    for char in text:
        if char in _CN_DIGITS:
            number = _CN_DIGITS[char]
        elif char in _CN_SECTION:
            if number == 0:
                number = 1
            section += number * _CN_SECTION[char]
            number = 0
        elif char in _CN_BIG:
            section += number
            if section == 0:
                section = 1
            total += section * _CN_BIG[char]
            section = 0
            number = 0
        else:
            return None
    return float(total + section + number)


def _collect_text(data: Dict[str, Any]) -> str:
    parts: List[str] = []
    for key in _TEXT_KEYS:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())
    return '\n'.join(parts)


def _coerce_number(value: Any) -> Optional[float]:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip().replace(',', '').replace('，', '')
        if not text:
            return None
        matched = re.fullmatch(
            r'(\d+(?:\.\d+)?)\s*(亿|万|千|百|k|K|w|W|元|块)?',
            text,
            re.IGNORECASE,
        )
        if matched:
            return _apply_unit(float(matched.group(1)), matched.group(2))
        chinese = _chinese_to_number(text)
        if chinese is not None:
            return chinese
    return None


def parse_initial_investment(text: str) -> Optional[float]:
    """从「我想投资10万」「investing 100k」中提取初始投资额（元）。"""
    if not text:
        return None
    matched = _ARABIC_AMOUNT.search(text)
    if matched:
        return _apply_unit(float(matched.group(1)), matched.group(2))
    matched = _CHINESE_AMOUNT.search(text)
    if matched:
        chinese = _chinese_to_number(matched.group(1))
        if chinese is not None:
            return chinese
    lowered = text.lower()
    if any(token in lowered for token in ('投资', '投入', 'invest')):
        matched = _FALLBACK_AMOUNT.search(text)
        if matched:
            return _apply_unit(float(matched.group(1)), matched.group(2))
    return None


def parse_annual_cash_flows(text: str) -> List[float]:
    """从「每年回报3万，连续5年」提取年度现金流。识别不到则返回空列表。"""
    if not text:
        return []
    matched = _CASHFLOW_AMOUNT.search(text)
    if not matched:
        return []
    amount = _apply_unit(float(matched.group(1)), matched.group(2))
    years_match = _CASHFLOW_YEARS.search(text)
    years = int(years_match.group(1)) if years_match else 1
    years = max(1, min(years, 50))
    return [amount] * years


def parse_discount_rate(text: str) -> Optional[float]:
    if not text:
        return None
    matched = _DISCOUNT_RATE.search(text)
    if not matched:
        return None
    value = float(matched.group(1))
    if matched.group(2) or value > 1:
        value /= 100.0
    return value


def _coerce_risk(value: Any) -> RiskLevel:
    if isinstance(value, RiskLevel):
        return value
    if isinstance(value, str):
        mapping = {
            'LOW': RiskLevel.LOW,
            '低': RiskLevel.LOW,
            '低风险': RiskLevel.LOW,
            'MEDIUM': RiskLevel.MEDIUM,
            '中': RiskLevel.MEDIUM,
            '中风险': RiskLevel.MEDIUM,
            'HIGH': RiskLevel.HIGH,
            '高': RiskLevel.HIGH,
            '高风险': RiskLevel.HIGH,
            'EXTREME': RiskLevel.EXTREME,
            '极高风险': RiskLevel.EXTREME,
        }
        return mapping.get(value.upper(), mapping.get(value, RiskLevel.MEDIUM))
    return RiskLevel.MEDIUM


def _coerce_flows(value: Any) -> List[float]:
    if value is None:
        return []
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return [float(value)]
    if isinstance(value, str):
        number = _coerce_number(value)
        return [number] if number is not None else []
    if isinstance(value, (list, tuple)):
        flows: List[float] = []
        for item in value:
            number = _coerce_number(item)
            if number is None:
                return []
            flows.append(number)
        return flows
    return []


def investment_defaults() -> Dict[str, Any]:
    """缺字段时返回给调用方的默认值说明。initial_investment 无法猜测，保持 None。"""
    return {
        'initial_investment': None,
        'annual_cash_flows': [],
        'discount_rate': _DEFAULT_DISCOUNT_RATE,
        'name': '未知项目',
        'risk_level': RiskLevel.MEDIUM.value,
    }


def normalize_project_data(raw: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    把结构化字段或中文/英文自然语言整理成投资分析输入。

    缺少 initial_investment 时不抛 KeyError：写入 error，并给出 defaults。
    已整理过的字典（带 _normalized）会原样返回，避免把「缺失」误当成 0。
    """
    raw = dict(raw or {})
    if raw.get('_normalized'):
        return raw

    text = _collect_text(raw)
    name = raw.get('name') or raw.get('project_name') or raw.get('项目') or ''
    if not isinstance(name, str) or not name.strip():
        name = (text[:40] if text else '') or '未知项目'

    initial = None
    for key in ('initial_investment', 'investment', '初始投资', '本金'):
        if key in raw:
            initial = _coerce_number(raw.get(key))
            if initial is not None:
                break

    flows = _coerce_flows(
        raw.get('annual_cash_flows', raw.get('cash_flows', raw.get('annual_cash_flow', raw.get('年度现金流'))))
    )
    discount = _coerce_number(raw.get('discount_rate', raw.get('rate', raw.get('折现率'))))

    warnings: List[str] = []
    parsed_from_text = False
    if initial is None and text:
        parsed = parse_initial_investment(text)
        if parsed is not None:
            initial = parsed
            parsed_from_text = True
    if not flows and text:
        parsed_flows = parse_annual_cash_flows(text)
        if parsed_flows:
            flows = parsed_flows
            parsed_from_text = True
    if discount is None and text:
        parsed_rate = parse_discount_rate(text)
        if parsed_rate is not None:
            discount = parsed_rate
    if discount is None:
        discount = _DEFAULT_DISCOUNT_RATE

    error = None
    if initial is None:
        error = (
            '缺少 initial_investment。请在请求中提供初始投资额，'
            '或用自然语言说明，例如「投资10万」「investing 100k」。'
        )

    if initial is not None and not flows and not error:
        warnings.append('未提供年度现金流，NPV/IRR/回收期按空现金流计算，结果不完整。')

    normalized: Dict[str, Any] = {
        'name': name,
        'initial_investment': 0.0 if initial is None else float(initial),
        'annual_cash_flows': flows,
        'discount_rate': float(discount),
        'risk_level': _coerce_risk(raw.get('risk_level', RiskLevel.MEDIUM)),
        'warnings': warnings,
        'error': error,
        'parsed_from_text': parsed_from_text,
        'data_status': '数据不足' if error else 'ok',
        '_normalized': True,
    }
    for key in ('market_volatility', 'technology_risk', 'regulatory_risk', 'execution_risk', 'query'):
        if key in raw:
            normalized[key] = raw[key]
    if text and 'query' not in normalized:
        normalized['query'] = text
    return normalized


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
        project_data = normalize_project_data(project_data)
        if project_data.get("error"):
            return InvestmentAnalysis(
                project_name=project_data.get("name", "未知项目"),
                initial_investment=0.0,
                recommendation=project_data["error"],
                factors={
                    "error": project_data["error"],
                    "defaults": investment_defaults(),
                    "data_status": "数据不足",
                },
            )

        initial = float(project_data.get("initial_investment") or 0.0)
        cash_flows = list(project_data.get("annual_cash_flows") or [])
        discount_rate = project_data.get("discount_rate", self.discount_rate)
        risk_level = project_data.get("risk_level", RiskLevel.MEDIUM)
        if not isinstance(risk_level, RiskLevel):
            risk_level = _coerce_risk(risk_level)
        
        roi = self._calculate_roi(initial, cash_flows)
        payback = self._calculate_payback(initial, cash_flows)
        npv = self._calculate_npv(initial, cash_flows, discount_rate)
        irr = self._calculate_irr(initial, cash_flows)
        if cash_flows:
            recommendation = self._generate_recommendation(roi, npv, irr, risk_level)
        else:
            # 没有回流时 NPV/IRR 没有业务含义，不把空序列当成「亏损项目」
            recommendation = "数据不足：已识别初始投资，但缺少年度现金流，暂不给出投资建议。"
            irr = 0.0
        
        analysis = InvestmentAnalysis(
            project_name=project_data.get("name", "未知项目"),
            initial_investment=initial,
            expected_return=sum(cash_flows) - initial,
            roi=roi,
            payback_period=payback,
            npv=npv,
            irr=irr,
            risk_assessment=risk_level,
            recommendation=recommendation,
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
        project_data = normalize_project_data(project_data)
        if project_data.get("error"):
            return InvestmentDecision(
                project_name=project_data.get("name", "未知项目"),
                recommendation=project_data["error"],
                investment_rating="N/A",
                key_factors=["数据不足", project_data["error"]],
                risk_mitigation=["补充 initial_investment 与 annual_cash_flows 后再评估"],
                alternative_scenarios={},
            )

        analysis = self.analyze_investment(project_data)
        if not project_data.get("annual_cash_flows"):
            return InvestmentDecision(
                project_name=project_data.get("name", "未知项目"),
                recommendation=analysis.recommendation,
                investment_rating="N/A",
                key_factors=["已识别初始投资", "缺少 annual_cash_flows"],
                risk_mitigation=["补充年度现金流后再评估 NPV、IRR 与回收期"],
                alternative_scenarios=self._generate_scenarios(project_data),
            )
        
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

        if total_investment <= 0:
            return {
                "error": "数据不足：投资组合的初始投资为 0，无法计算权重。",
                "data_status": "数据不足",
                "total_investment": total_investment,
                "expected_return": total_expected,
            }
        
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
        if initial == 0 or not cash_flows:
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
            "average_annual_return": (
                sum(cash_flows) / len(cash_flows) / initial
                if cash_flows and initial > 0 else 0
            ),
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
        """生成情景分析。缺 initial_investment 时按 0 处理，不抛 KeyError。"""
        project_data = normalize_project_data(project_data)
        initial = float(project_data.get("initial_investment") or 0.0)
        base_flows = list(project_data.get("annual_cash_flows") or [])
        discount = project_data.get("discount_rate", self.discount_rate)
        
        optimistic = [cf * 1.3 for cf in base_flows]
        pessimistic = [cf * 0.7 for cf in base_flows]

        if base_flows:
            average = sum(base_flows) / len(base_flows)
            break_even = self._calculate_payback(initial, [average] * len(base_flows))
        else:
            break_even = None
        
        return {
            "optimistic": {
                "npv": self._calculate_npv(initial, optimistic, discount),
                "payback": self._calculate_payback(initial, optimistic),
            },
            "pessimistic": {
                "npv": self._calculate_npv(initial, pessimistic, discount),
                "payback": self._calculate_payback(initial, pessimistic),
            },
            "break_even": break_even,
            "data_status": project_data.get("data_status", "ok"),
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
