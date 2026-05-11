"""
商道智能系统测试
"""

import pytest
from datetime import datetime

from commercial import (
    CommercialAgent,
    MarketInsightEngine,
    BusinessModelAnalyzer,
    CompetitionAnalyzer,
    InvestmentAnalyzer,
    StrategyPlanner,
    ShangDaoAdvisor,
    Opportunity,
    OpportunityType,
    RiskLevel,
    MarketPosition,
)


class TestMarketInsightEngine:
    """商机洞察引擎测试"""

    def test_engine_init(self):
        """测试引擎初始化"""
        engine = MarketInsightEngine()
        assert engine is not None
        assert len(engine.get_wisdom_insights()) > 0

    def test_analyze_market_with_gaps(self):
        """测试市场空白识别"""
        engine = MarketInsightEngine()
        market_data = {
            "unmet_needs": ["高端定制服务", "智能解决方案"],
            "underserved_segments": ["三四线城市"]
        }
        
        opportunities = engine.analyze_market(market_data)
        assert len(opportunities) > 0
        
        gap_opps = engine.get_opportunities_by_type(OpportunityType.GAP)
        assert len(gap_opps) > 0

    def test_analyze_market_with_emerging(self):
        """测试新兴机遇识别"""
        engine = MarketInsightEngine()
        market_data = {
            "technology_trends": ["AI应用", "区块链"],
            "policy_drivers": ["新能源补贴"]
        }
        
        opportunities = engine.analyze_market(market_data)
        assert len(opportunities) > 0
        
        emerging_opps = engine.get_opportunities_by_type(OpportunityType.EMERGING)
        assert len(emerging_opps) > 0

    def test_top_opportunities(self):
        """测试获取最优商机"""
        engine = MarketInsightEngine()
        market_data = {
            "unmet_needs": ["服务A", "服务B", "服务C"],
            "technology_trends": ["技术1", "技术2"]
        }
        
        engine.analyze_market(market_data)
        top = engine.get_top_opportunities(limit=3)
        
        assert len(top) <= 3
        assert all(isinstance(o, Opportunity) for o in top)

    def test_wisdom_insights(self):
        """测试东方智慧洞察"""
        engine = MarketInsightEngine()
        insights = engine.get_wisdom_insights()
        
        assert len(insights) > 0
        assert all(hasattr(i, 'title') for i in insights)
        assert all(hasattr(i, 'content') for i in insights)

    def test_assess_opportunity(self):
        """测试商机评估"""
        engine = MarketInsightEngine()
        market_data = {"unmet_needs": ["测试需求"]}
        opportunities = engine.analyze_market(market_data)
        
        if opportunities:
            assessment = engine.assess_opportunity(opportunities[0].opportunity_id)
            assert "opportunity" in assessment or assessment == {}


class TestBusinessModelAnalyzer:
    """商业模式分析器测试"""

    def test_analyzer_init(self):
        """测试分析器初始化"""
        analyzer = BusinessModelAnalyzer()
        assert analyzer is not None

    def test_analyze_subscription_model(self):
        """测试订阅模式分析"""
        analyzer = BusinessModelAnalyzer()
        model_data = {
            "type": "subscription",
            "customer_segments": ["企业客户", "个人用户"],
            "value_propositions": ["随时访问", "专业支持"],
            "revenue_streams": ["月费", "年费"],
            "key_resources": ["技术平台", "内容"],
            "key_activities": ["服务提供", "客户支持"]
        }
        
        analysis = analyzer.analyze_model(model_data)
        
        assert analysis.model_type == "subscription"
        assert 0 <= analysis.overall_score <= 1
        assert len(analysis.recommendations) > 0

    def test_analyze_marketplace_model(self):
        """测试平台模式分析"""
        analyzer = BusinessModelAnalyzer()
        model_data = {
            "type": "marketplace",
            "customer_segments": ["买家", "卖家"],
            "value_propositions": ["交易撮合", "信用保障"],
            "revenue_streams": ["交易佣金"],
            "key_resources": ["平台技术", "品牌"]
        }
        
        analysis = analyzer.analyze_model(model_data)
        
        assert analysis.model_type == "marketplace"
        assert analysis.scalability_score > 0.4

    def test_compare_models(self):
        """测试模式比较"""
        analyzer = BusinessModelAnalyzer()
        
        analyzer.analyze_model({"type": "subscription", "revenue_streams": ["月费"]})
        analyzer.analyze_model({"type": "marketplace", "revenue_streams": ["佣金"]})
        
        comparisons = analyzer.compare_models(["subscription", "marketplace"])
        assert len(comparisons) == 2

    def test_model_types_available(self):
        """测试可用模式类型"""
        analyzer = BusinessModelAnalyzer()
        types = analyzer.get_model_types()
        
        assert len(types) > 0
        assert all("type" in t and "name" in t for t in types)


class TestCompetitionAnalyzer:
    """竞争分析器测试"""

    def test_analyzer_init(self):
        """测试分析器初始化"""
        analyzer = CompetitionAnalyzer()
        assert analyzer is not None

    def test_add_competitor(self):
        """测试添加竞争对手"""
        analyzer = CompetitionAnalyzer()
        competitor_data = {
            "name": "竞争者A",
            "market_share": 0.25,
            "revenue": 10000000,
            "growth_rate": 0.3,
            "strengths": ["品牌优势", "渠道广"],
            "weaknesses": ["价格高", "服务慢"]
        }
        
        competitor = analyzer.add_competitor(competitor_data)
        
        assert competitor.name == "竞争者A"
        assert competitor.market_share == 0.25
        assert competitor.threat_level > 0

    def test_swot_analysis(self):
        """测试SWOT分析"""
        analyzer = CompetitionAnalyzer()
        competitor_data = {
            "name": "竞争者B",
            "market_share": 0.15,
            "strengths": ["技术创新"],
            "weaknesses": ["经验不足"]
        }
        
        competitor = analyzer.add_competitor(competitor_data)
        swot = analyzer.get_swot_analysis(competitor.competitor_id)
        
        assert "swot" in swot
        assert "strengths" in swot["swot"]
        assert "weaknesses" in swot["swot"]

    def test_compare_competitors(self):
        """测试竞争对手对比"""
        analyzer = CompetitionAnalyzer()
        analyzer.add_competitor({
            "name": "竞品1",
            "market_share": 0.2,
            "strengths": ["品牌"],
            "weaknesses": ["创新"]
        })
        
        comparison = analyzer.compare_with_competitors(
            my_strengths=["技术", "价格"],
            my_weaknesses=["渠道", "品牌"]
        )
        
        assert "competitive_advantages" in comparison
        assert "competitive_disadvantages" in comparison

    def test_response_strategy(self):
        """测试应对策略"""
        analyzer = CompetitionAnalyzer()
        competitor = analyzer.add_competitor({
            "name": "威胁者",
            "market_share": 0.35,
            "growth_rate": 0.4,
            "weaknesses": ["服务差"]
        })
        
        strategy = analyzer.generate_response_strategy(competitor.competitor_id)
        
        assert "recommended_strategies" in strategy
        assert len(strategy["recommended_strategies"]) > 0

    def test_top_competitors(self):
        """测试获取主要竞争对手"""
        analyzer = CompetitionAnalyzer()
        analyzer.add_competitor({"name": "大公司", "market_share": 0.4})
        analyzer.add_competitor({"name": "小公司", "market_share": 0.1})
        
        top = analyzer.get_top_competitors(limit=1)
        
        assert len(top) == 1
        assert top[0].name == "大公司"


class TestInvestmentAnalyzer:
    """投资分析器测试"""

    def test_analyzer_init(self):
        """测试分析器初始化"""
        analyzer = InvestmentAnalyzer(discount_rate=0.1)
        assert analyzer.discount_rate == 0.1

    def test_basic_investment_analysis(self):
        """测试基本投资分析"""
        analyzer = InvestmentAnalyzer()
        project_data = {
            "name": "新项目",
            "initial_investment": 1000000,
            "annual_cash_flows": [300000, 400000, 500000, 400000],
            "risk_level": RiskLevel.MEDIUM
        }
        
        analysis = analyzer.analyze_investment(project_data)
        
        assert analysis.project_name == "新项目"
        assert analysis.initial_investment == 1000000
        assert isinstance(analysis.roi, float)
        assert isinstance(analysis.payback_period, float)

    def test_roi_calculation(self):
        """测试ROI计算"""
        analyzer = InvestmentAnalyzer()
        project_data = {
            "initial_investment": 1000000,
            "annual_cash_flows": [600000, 500000, 400000]
        }
        
        analysis = analyzer.analyze_investment(project_data)
        
        assert analysis.roi > 0

    def test_npv_calculation(self):
        """测试NPV计算"""
        analyzer = InvestmentAnalyzer(discount_rate=0.1)
        project_data = {
            "initial_investment": 1000000,
            "annual_cash_flows": [400000, 400000, 400000, 400000],
            "discount_rate": 0.1
        }
        
        analysis = analyzer.analyze_investment(project_data)
        
        assert isinstance(analysis.npv, float)

    def test_make_decision(self):
        """测试投资决策"""
        analyzer = InvestmentAnalyzer()
        project_data = {
            "name": "高回报项目",
            "initial_investment": 500000,
            "annual_cash_flows": [300000, 300000, 300000],
            "risk_level": RiskLevel.LOW
        }
        
        decision = analyzer.make_decision(project_data)
        
        assert decision.project_name == "高回报项目"
        assert decision.investment_rating in ["A", "B", "C", "D"]

    def test_compare_investments(self):
        """测试投资项目比较"""
        analyzer = InvestmentAnalyzer()
        projects = [
            {
                "name": "项目A",
                "initial_investment": 1000000,
                "annual_cash_flows": [400000, 400000, 400000]
            },
            {
                "name": "项目B",
                "initial_investment": 500000,
                "annual_cash_flows": [300000, 300000, 300000]
            }
        ]
        
        comparison = analyzer.compare_investments(projects)
        
        assert "analyses" in comparison
        assert "rankings" in comparison
        assert "recommendation" in comparison

    def test_portfolio_analysis(self):
        """测试投资组合分析"""
        analyzer = InvestmentAnalyzer()
        investments = [
            {
                "initial_investment": 600000,
                "annual_cash_flows": [200000, 250000, 300000]
            },
            {
                "initial_investment": 400000,
                "annual_cash_flows": [150000, 180000, 200000]
            }
        ]
        
        portfolio = analyzer.portfolio_analysis(investments)
        
        assert "total_investment" in portfolio
        assert "portfolio_return" in portfolio
        assert "sharpe_ratio" in portfolio


class TestStrategyPlanner:
    """战略规划器测试"""

    def test_planner_init(self):
        """测试规划器初始化"""
        planner = StrategyPlanner()
        assert planner is not None

    def test_create_strategic_plan(self):
        """测试创建战略规划"""
        planner = StrategyPlanner()
        business_data = {
            "industry": "科技",
            "core_value": "创新",
            "strategy_type": "differentiation"
        }
        
        plan = planner.create_strategic_plan(business_data)
        
        assert plan.name != ""
        assert plan.vision != ""
        assert len(plan.objectives) > 0
        assert len(plan.key_strategies) > 0

    def test_swot_analysis(self):
        """测试SWOT分析"""
        planner = StrategyPlanner()
        swot = planner.analyze_swot(
            strengths=["技术领先", "品牌好"],
            weaknesses=["渠道弱"],
            opportunities=["市场扩大"],
            threats=["竞争加剧"]
        )
        
        assert "strengths" in swot
        assert "so_strategies" in swot
        assert "wt_strategies" in swot

    def test_get_strategic_frames(self):
        """测试获取战略框架"""
        planner = StrategyPlanner()
        frames = planner.get_strategic_frames()
        
        assert len(frames) > 0
        assert all("name" in f for f in frames)

    def test_get_initiatives(self):
        """测试获取战略举措"""
        planner = StrategyPlanner()
        planner.create_strategic_plan({"industry": "测试"})
        
        initiatives = planner.get_initiatives()
        assert len(initiatives) > 0


class TestCommercialAgent:
    """商道智能体测试"""

    def test_agent_init(self):
        """测试智能体初始化"""
        agent = CommercialAgent()
        assert agent.insight_engine is not None
        assert agent.model_analyzer is not None
        assert agent.competition_analyzer is not None
        assert agent.investment_analyzer is not None
        assert agent.strategy_planner is not None

    def test_analyze_opportunity(self):
        """测试商机分析"""
        agent = CommercialAgent()
        market_data = {
            "unmet_needs": ["智能家居"],
            "technology_trends": ["AI"]
        }
        
        result = agent.analyze_opportunity(market_data)
        
        assert "opportunities" in result
        assert "top_opportunities" in result
        assert result["total_count"] > 0

    def test_analyze_business_model(self):
        """测试商业模式分析"""
        agent = CommercialAgent()
        model_data = {
            "type": "saas",
            "customer_segments": ["企业"],
            "revenue_streams": ["订阅费"]
        }
        
        result = agent.analyze_business_model(model_data)
        
        assert "model_type" in result
        assert "overall_score" in result
        assert "scores" in result

    def test_analyze_competition(self):
        """测试竞争分析"""
        agent = CommercialAgent()
        competitor_data = {
            "name": "强劲对手",
            "market_share": 0.3,
            "strengths": ["资源多"]
        }
        
        result = agent.analyze_competition(competitor_data)
        
        assert "competitor" in result
        assert "threat_level" in result

    def test_analyze_investment(self):
        """测试投资分析"""
        agent = CommercialAgent()
        project_data = {
            "name": "扩张项目",
            "initial_investment": 2000000,
            "annual_cash_flows": [600000, 800000, 1000000, 800000],
            "risk_level": RiskLevel.MEDIUM
        }
        
        result = agent.analyze_investment(project_data)
        
        assert "project_name" in result
        assert "roi" in result
        assert "recommendation" in result

    def test_formulate_strategy(self):
        """测试战略规划"""
        agent = CommercialAgent()
        business_data = {
            "industry": "互联网",
            "strategy_type": "agile"
        }
        
        result = agent.formulate_strategy(business_data)
        
        assert "vision" in result
        assert "objectives" in result
        assert "action_plans" in result

    def test_generate_report(self):
        """测试生成综合报告"""
        agent = CommercialAgent()
        context = {
            "title": "年度商业分析",
            "market_data": {"unmet_needs": ["健康管理"]},
            "strategy_data": {"industry": "大健康"}
        }
        
        report = agent.generate_comprehensive_report(context)
        
        assert report.title == "年度商业分析"
        assert report.executive_summary != ""

    def test_get_state(self):
        """测试获取状态"""
        agent = CommercialAgent()
        agent.analyze_opportunity({"unmet_needs": ["测试"]})
        
        state = agent.get_state()
        
        assert "analysis_count" in state
        assert state["analysis_count"] > 0


class TestShangDaoAdvisor:
    """商道顾问测试"""

    def test_get_advice_startup(self):
        """测试创业建议"""
        advice = ShangDaoAdvisor.get_advice("startup")
        
        assert "advice" in advice
        assert "wisdom_quote" in advice
        assert len(advice["action_steps"]) > 0

    def test_get_advice_growth(self):
        """测试成长期建议"""
        advice = ShangDaoAdvisor.get_advice("growth")
        
        assert advice["situation"] == "growth"

    def test_evaluate_decision(self):
        """测试决策评估"""
        evaluation = ShangDaoAdvisor.evaluate_decision(
            "进入新市场",
            {"risk_level": 0.4, "potential_return": 0.7}
        )
        
        assert "assessment" in evaluation
        assert "wisdom_score" in evaluation
        assert 0 <= evaluation["wisdom_score"] <= 1

    def test_wisdom_principles(self):
        """测试智慧原则"""
        assert len(ShangDaoAdvisor.WISDOM_PRINCIPLES) > 0


class TestCommercialTypes:
    """商业类型测试"""

    def test_opportunity_creation(self):
        """测试商机创建"""
        opp = Opportunity(
            title="测试商机",
            opportunity_type=OpportunityType.GAP,
            potential_revenue=1000000
        )
        
        assert opp.title == "测试商机"
        assert opp.opportunity_type == OpportunityType.GAP
        assert opp.potential_revenue == 1000000

    def test_risk_level_enum(self):
        """测试风险等级枚举"""
        assert RiskLevel.LOW.value == "低风险"
        assert RiskLevel.HIGH.value == "高风险"

    def test_market_position_enum(self):
        """测试市场定位枚举"""
        assert MarketPosition.PIONEER.value == "先驱者"
        assert MarketPosition.FOLLOWER.value == "追随者"
