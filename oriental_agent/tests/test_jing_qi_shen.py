"""
Unit tests for Jing Qi Shen (Three Treasures) Model
精气神三宝模型单元测试
"""

import unittest
import sys
import os
import importlib.util

_test_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_test_dir, '..', '..'))

_jing_qi_shen_path = os.path.join(_project_root, "oriental_agent", "body", "jing_qi_shen.py")
_spec = importlib.util.spec_from_file_location("jing_qi_shen", _jing_qi_shen_path)
jing_qi_shen_module = importlib.util.module_from_spec(_spec)
sys.modules["jing_qi_shen"] = jing_qi_shen_module
_spec.loader.exec_module(jing_qi_shen_module)

TreasureType = jing_qi_shen_module.TreasureType
RegulationMode = jing_qi_shen_module.RegulationMode
JingQiShenLevel = jing_qi_shen_module.JingQiShenLevel
RegulationResult = jing_qi_shen_module.RegulationResult
JingQiShenModel = jing_qi_shen_module.JingQiShenModel
create_jing_qi_shen_model = jing_qi_shen_module.create_jing_qi_shen_model


class TestTreasureType(unittest.TestCase):
    """测试三宝类型枚举"""
    
    def test_all_treasures_exist(self):
        treasures = list(TreasureType)
        self.assertEqual(len(treasures), 3)
    
    def test_treasure_values(self):
        self.assertEqual(TreasureType.JING.value, "精")
        self.assertEqual(TreasureType.QI.value, "气")
        self.assertEqual(TreasureType.SHEN.value, "神")


class TestRegulationMode(unittest.TestCase):
    """测试调理模式枚举"""
    
    def test_all_modes_exist(self):
        modes = list(RegulationMode)
        self.assertEqual(len(modes), 4)
    
    def test_mode_values(self):
        self.assertEqual(RegulationMode.NOURISH_JING.value, "养精")
        self.assertEqual(RegulationMode.REGULATE_QI.value, "调气")
        self.assertEqual(RegulationMode.GATHER_SHEN.value, "聚神")
        self.assertEqual(RegulationMode.BALANCE.value, "平衡")


class TestJingQiShenLevel(unittest.TestCase):
    """测试精气神水平数据结构"""
    
    def test_level_creation_default(self):
        level = JingQiShenLevel()
        
        self.assertEqual(level.jing_level, 0.5)
        self.assertEqual(level.qi_level, 0.5)
        self.assertEqual(level.shen_level, 0.5)
    
    def test_level_creation_custom(self):
        level = JingQiShenLevel(jing_level=0.8, qi_level=0.6, shen_level=0.7)
        
        self.assertEqual(level.jing_level, 0.8)
        self.assertEqual(level.qi_level, 0.6)
        self.assertEqual(level.shen_level, 0.7)
    
    def test_level_clamp_upper(self):
        level = JingQiShenLevel(jing_level=1.5, qi_level=2.0, shen_level=1.2)
        
        self.assertEqual(level.jing_level, 1.0)
        self.assertEqual(level.qi_level, 1.0)
        self.assertEqual(level.shen_level, 1.0)
    
    def test_level_clamp_lower(self):
        level = JingQiShenLevel(jing_level=-0.5, qi_level=-0.1, shen_level=-1.0)
        
        self.assertEqual(level.jing_level, 0.0)
        self.assertEqual(level.qi_level, 0.0)
        self.assertEqual(level.shen_level, 0.0)
    
    def test_overall_vitality(self):
        level = JingQiShenLevel(jing_level=0.6, qi_level=0.8, shen_level=0.7)
        
        expected = (0.6 + 0.8 + 0.7) / 3.0
        self.assertAlmostEqual(level.overall_vitality, expected, places=5)
    
    def test_balance_score_perfect(self):
        level = JingQiShenLevel(jing_level=0.5, qi_level=0.5, shen_level=0.5)
        
        self.assertEqual(level.balance_score, 1.0)
    
    def test_balance_score_imbalanced(self):
        level = JingQiShenLevel(jing_level=0.9, qi_level=0.1, shen_level=0.5)
        
        self.assertLess(level.balance_score, 1.0)
    
    def test_get_lowest_treasure(self):
        level = JingQiShenLevel(jing_level=0.8, qi_level=0.3, shen_level=0.6)
        
        lowest_type, lowest_level = level.get_lowest_treasure()
        
        self.assertEqual(lowest_type, TreasureType.QI)
        self.assertEqual(lowest_level, 0.3)
    
    def test_get_highest_treasure(self):
        level = JingQiShenLevel(jing_level=0.8, qi_level=0.3, shen_level=0.6)
        
        highest_type, highest_level = level.get_highest_treasure()
        
        self.assertEqual(highest_type, TreasureType.JING)
        self.assertEqual(highest_level, 0.8)
    
    def test_to_dict(self):
        level = JingQiShenLevel(jing_level=0.7, qi_level=0.6, shen_level=0.8)
        
        result = level.to_dict()
        
        self.assertEqual(result["jing_level"], 0.7)
        self.assertEqual(result["qi_level"], 0.6)
        self.assertEqual(result["shen_level"], 0.8)
        self.assertIn("overall_vitality", result)
        self.assertIn("balance_score", result)
        self.assertIn("timestamp", result)


class TestJingQiShenModel(unittest.TestCase):
    """测试精气神三宝模型主类"""
    
    def setUp(self):
        self.model = JingQiShenModel()
    
    def test_model_creation_default(self):
        self.assertEqual(self.model.current_level.jing_level, 0.5)
        self.assertEqual(self.model.current_level.qi_level, 0.5)
        self.assertEqual(self.model.current_level.shen_level, 0.5)
    
    def test_model_creation_custom_initial(self):
        initial = JingQiShenLevel(jing_level=0.8, qi_level=0.7, shen_level=0.6)
        model = JingQiShenModel(initial_level=initial)
        
        self.assertEqual(model.current_level.jing_level, 0.8)
        self.assertEqual(model.current_level.qi_level, 0.7)
        self.assertEqual(model.current_level.shen_level, 0.6)
    
    def test_model_auto_regulate_enabled_default(self):
        self.assertTrue(self.model.auto_regulate_enabled)
    
    def test_model_empty_history(self):
        self.assertEqual(len(self.model.regulation_history), 0)


class TestAssess(unittest.TestCase):
    """测试实时状态评估"""
    
    def setUp(self):
        self.model = JingQiShenModel()
    
    def test_assess_returns_level(self):
        result = self.model.assess()
        
        self.assertIsInstance(result, JingQiShenLevel)
    
    def test_assess_updates_state_history(self):
        initial_history_len = len(self.model.state_history)
        
        self.model.assess()
        
        self.assertEqual(len(self.model.state_history), initial_history_len + 1)
    
    def test_assess_with_context_activity(self):
        context = {"activity_level": 0.5}
        
        initial_qi = self.model.current_level.qi_level
        self.model.assess(context=context)
        
        self.assertLess(self.model.current_level.qi_level, initial_qi)
    
    def test_assess_with_context_mental_load(self):
        context = {"mental_load": 0.5}
        
        initial_shen = self.model.current_level.shen_level
        self.model.assess(context=context)
        
        self.assertLess(self.model.current_level.shen_level, initial_shen)
    
    def test_assess_with_context_rest(self):
        context = {"rest_quality": 0.5}
        
        initial_jing = self.model.current_level.jing_level
        self.model.assess(context=context)
        
        self.assertGreater(self.model.current_level.jing_level, initial_jing)
    
    def test_assess_with_context_nutrition(self):
        context = {"nutrition": 0.5}
        
        initial_jing = self.model.current_level.jing_level
        initial_qi = self.model.current_level.qi_level
        self.model.assess(context=context)
        
        self.assertGreater(self.model.current_level.jing_level, initial_jing)
        self.assertGreater(self.model.current_level.qi_level, initial_qi)


class TestNourishJing(unittest.TestCase):
    """测试养精机制"""
    
    def setUp(self):
        self.model = JingQiShenModel()
    
    def test_nourish_jing_returns_result(self):
        result = self.model.nourish_jing()
        
        self.assertIsInstance(result, RegulationResult)
        self.assertEqual(result.mode, RegulationMode.NOURISH_JING)
        self.assertTrue(result.success)
    
    def test_nourish_jing_increases_jing(self):
        initial_jing = self.model.current_level.jing_level
        
        self.model.nourish_jing(intensity=0.5)
        
        self.assertGreater(self.model.current_level.jing_level, initial_jing)
    
    def test_nourish_jing_consumes_qi(self):
        initial_qi = self.model.current_level.qi_level
        
        self.model.nourish_jing(intensity=0.5)
        
        self.assertLess(self.model.current_level.qi_level, initial_qi)
    
    def test_nourish_jing_intensity_affects_result(self):
        self.model.reset()
        
        self.model.nourish_jing(intensity=0.3)
        jing_low = self.model.current_level.jing_level
        
        self.model.reset()
        self.model.nourish_jing(intensity=0.8)
        jing_high = self.model.current_level.jing_level
        
        self.assertGreater(jing_high, jing_low)
    
    def test_nourish_jing_records_history(self):
        initial_history_len = len(self.model.regulation_history)
        
        self.model.nourish_jing()
        
        self.assertEqual(len(self.model.regulation_history), initial_history_len + 1)
    
    def test_nourish_jing_result_contains_changes(self):
        result = self.model.nourish_jing()
        
        self.assertIn("jing_change", result.changes)
        self.assertIn("qi_change", result.changes)
        self.assertIn("shen_change", result.changes)
        self.assertGreater(result.changes["jing_change"], 0)


class TestRegulateQi(unittest.TestCase):
    """测试调气机制"""
    
    def setUp(self):
        self.model = JingQiShenModel()
    
    def test_regulate_qi_returns_result(self):
        result = self.model.regulate_qi()
        
        self.assertIsInstance(result, RegulationResult)
        self.assertEqual(result.mode, RegulationMode.REGULATE_QI)
        self.assertTrue(result.success)
    
    def test_regulate_qi_increases_qi_when_low(self):
        self.model.current_level.qi_level = 0.3
        initial_qi = self.model.current_level.qi_level
        
        self.model.regulate_qi(intensity=0.5)
        
        self.assertGreater(self.model.current_level.qi_level, initial_qi)
    
    def test_regulate_qi_affects_shen(self):
        self.model.current_level.qi_level = 0.3
        initial_shen = self.model.current_level.shen_level
        
        self.model.regulate_qi(intensity=0.5)
        
        self.assertGreater(self.model.current_level.shen_level, initial_shen)
    
    def test_regulate_qi_intensity_affects_result(self):
        self.model.reset()
        self.model.current_level.qi_level = 0.3
        
        self.model.regulate_qi(intensity=0.3)
        qi_low = self.model.current_level.qi_level
        
        self.model.reset()
        self.model.current_level.qi_level = 0.3
        self.model.regulate_qi(intensity=0.8)
        qi_high = self.model.current_level.qi_level
        
        self.assertGreater(qi_high, qi_low)
    
    def test_regulate_qi_records_history(self):
        initial_history_len = len(self.model.regulation_history)
        
        self.model.regulate_qi()
        
        self.assertEqual(len(self.model.regulation_history), initial_history_len + 1)


class TestGatherShen(unittest.TestCase):
    """测试聚神机制"""
    
    def setUp(self):
        self.model = JingQiShenModel()
    
    def test_gather_shen_returns_result(self):
        result = self.model.gather_shen()
        
        self.assertIsInstance(result, RegulationResult)
        self.assertEqual(result.mode, RegulationMode.GATHER_SHEN)
        self.assertTrue(result.success)
    
    def test_gather_shen_increases_shen(self):
        initial_shen = self.model.current_level.shen_level
        
        self.model.gather_shen(intensity=0.5)
        
        self.assertGreater(self.model.current_level.shen_level, initial_shen)
    
    def test_gather_shen_consumes_qi(self):
        initial_qi = self.model.current_level.qi_level
        
        self.model.gather_shen(intensity=0.5)
        
        self.assertLess(self.model.current_level.qi_level, initial_qi)
    
    def test_gather_shen_intensity_affects_result(self):
        self.model.reset()
        
        self.model.gather_shen(intensity=0.3)
        shen_low = self.model.current_level.shen_level
        
        self.model.reset()
        self.model.gather_shen(intensity=0.8)
        shen_high = self.model.current_level.shen_level
        
        self.assertGreater(shen_high, shen_low)
    
    def test_gather_shen_records_history(self):
        initial_history_len = len(self.model.regulation_history)
        
        self.model.gather_shen()
        
        self.assertEqual(len(self.model.regulation_history), initial_history_len + 1)


class TestBalance(unittest.TestCase):
    """测试动态平衡调节"""
    
    def setUp(self):
        self.model = JingQiShenModel()
    
    def test_balance_returns_result(self):
        result = self.model.balance()
        
        self.assertIsInstance(result, RegulationResult)
        self.assertEqual(result.mode, RegulationMode.BALANCE)
        self.assertTrue(result.success)
    
    def test_balance_triggers_nourish_jing_when_low(self):
        self.model.current_level.jing_level = 0.2
        
        result = self.model.balance()
        
        self.assertIn("养精", result.message)
    
    def test_balance_triggers_regulate_qi_when_low(self):
        self.model.current_level.qi_level = 0.2
        
        result = self.model.balance()
        
        self.assertIn("调气", result.message)
    
    def test_balance_triggers_gather_shen_when_low(self):
        self.model.current_level.shen_level = 0.2
        
        result = self.model.balance()
        
        self.assertIn("聚神", result.message)
    
    def test_balance_improves_overall_vitality(self):
        self.model.current_level.jing_level = 0.2
        self.model.current_level.qi_level = 0.25
        self.model.current_level.shen_level = 0.2
        
        initial_vitality = self.model.current_level.overall_vitality
        
        self.model.balance()
        
        final_vitality = self.model.current_level.overall_vitality
        self.assertGreater(final_vitality, initial_vitality)
    
    def test_balance_improves_balance_score(self):
        self.model.current_level.jing_level = 0.9
        self.model.current_level.qi_level = 0.2
        self.model.current_level.shen_level = 0.5
        
        initial_balance = self.model.current_level.balance_score
        
        self.model.balance()
        
        final_balance = self.model.current_level.balance_score
        self.assertGreater(final_balance, initial_balance)
    
    def test_balance_records_history(self):
        initial_history_len = len(self.model.regulation_history)
        
        self.model.balance()
        
        self.assertGreater(len(self.model.regulation_history), initial_history_len)


class TestInterInfluences(unittest.TestCase):
    """测试精气神相互影响关系"""
    
    def setUp(self):
        self.model = JingQiShenModel()
    
    def test_jing_deficiency_reduces_qi(self):
        self.model.current_level.jing_level = 0.2
        self.model.current_level.qi_level = 0.7
        
        self.model._apply_inter_influences()
        
        self.assertLess(self.model.current_level.qi_level, 0.7)
    
    def test_qi_deficiency_reduces_shen(self):
        self.model.current_level.qi_level = 0.2
        self.model.current_level.shen_level = 0.7
        
        self.model._apply_inter_influences()
        
        self.assertLess(self.model.current_level.shen_level, 0.7)
    
    def test_shen_flourishing_increases_qi(self):
        self.model.current_level.shen_level = 0.8
        self.model.current_level.qi_level = 0.5
        
        self.model._apply_inter_influences()
        
        self.assertGreater(self.model.current_level.qi_level, 0.5)
    
    def test_qi_sufficiency_increases_jing(self):
        self.model.current_level.qi_level = 0.8
        self.model.current_level.jing_level = 0.5
        
        self.model._apply_inter_influences()
        
        self.assertGreater(self.model.current_level.jing_level, 0.5)


class TestThresholdAlerts(unittest.TestCase):
    """测试阈值预警机制"""
    
    def setUp(self):
        self.model = JingQiShenModel()
    
    def test_alert_for_low_jing(self):
        self.model.current_level.jing_level = 0.25
        
        report = self.model.get_status_report()
        
        jing_alerts = [a for a in report["alerts"] if a["treasure"] == "精"]
        self.assertEqual(len(jing_alerts), 1)
    
    def test_alert_for_low_qi(self):
        self.model.current_level.qi_level = 0.25
        
        report = self.model.get_status_report()
        
        qi_alerts = [a for a in report["alerts"] if a["treasure"] == "气"]
        self.assertEqual(len(qi_alerts), 1)
    
    def test_alert_for_low_shen(self):
        self.model.current_level.shen_level = 0.25
        
        report = self.model.get_status_report()
        
        shen_alerts = [a for a in report["alerts"] if a["treasure"] == "神"]
        self.assertEqual(len(shen_alerts), 1)
    
    def test_no_alert_for_normal_levels(self):
        self.model.current_level.jing_level = 0.5
        self.model.current_level.qi_level = 0.5
        self.model.current_level.shen_level = 0.5
        
        report = self.model.get_status_report()
        
        self.assertEqual(len(report["alerts"]), 0)


class TestStatusReport(unittest.TestCase):
    """测试状态报告"""
    
    def setUp(self):
        self.model = JingQiShenModel()
    
    def test_status_report_contains_current_level(self):
        report = self.model.get_status_report()
        
        self.assertIn("current_level", report)
        self.assertIn("jing_level", report["current_level"])
        self.assertIn("qi_level", report["current_level"])
        self.assertIn("shen_level", report["current_level"])
    
    def test_status_report_contains_vitality(self):
        report = self.model.get_status_report()
        
        self.assertIn("overall_vitality", report)
        self.assertIn("balance_score", report)
    
    def test_status_report_contains_extremes(self):
        report = self.model.get_status_report()
        
        self.assertIn("lowest_treasure", report)
        self.assertIn("highest_treasure", report)
    
    def test_status_report_contains_regulation_count(self):
        self.model.nourish_jing()
        self.model.regulate_qi()
        
        report = self.model.get_status_report()
        
        self.assertEqual(report["regulation_count"], 2)


class TestRegulationHistory(unittest.TestCase):
    """测试调理历史"""
    
    def setUp(self):
        self.model = JingQiShenModel()
    
    def test_get_regulation_history_empty(self):
        history = self.model.get_regulation_history()
        
        self.assertEqual(len(history), 0)
    
    def test_get_regulation_history_with_records(self):
        self.model.nourish_jing()
        self.model.regulate_qi()
        
        history = self.model.get_regulation_history()
        
        self.assertEqual(len(history), 2)
    
    def test_get_regulation_history_limit(self):
        for _ in range(15):
            self.model.nourish_jing()
        
        history = self.model.get_regulation_history(limit=5)
        
        self.assertEqual(len(history), 5)
    
    def test_regulation_history_order(self):
        self.model.nourish_jing()
        self.model.regulate_qi()
        
        history = self.model.get_regulation_history()
        
        self.assertEqual(history[0]["mode"], "调气")
        self.assertEqual(history[1]["mode"], "养精")


class TestStateTrend(unittest.TestCase):
    """测试状态趋势"""
    
    def setUp(self):
        self.model = JingQiShenModel()
    
    def test_trend_insufficient_data(self):
        trend = self.model.get_state_trend()
        
        self.assertEqual(trend["trend"], "insufficient_data")
    
    def test_trend_with_data(self):
        for _ in range(5):
            self.model.assess()
        
        trend = self.model.get_state_trend()
        
        self.assertIn("jing_trend", trend)
        self.assertIn("qi_trend", trend)
        self.assertIn("shen_trend", trend)
        self.assertIn("overall_trend", trend)
    
    def test_trend_direction_detection(self):
        self.model.current_level.jing_level = 0.3
        self.model.assess()
        
        for _ in range(3):
            self.model.nourish_jing(intensity=0.8)
            self.model.assess()
        
        trend = self.model.get_state_trend()
        
        self.assertIn(trend["jing_trend"]["direction"], ["上升", "稳定", "下降"])


class TestReset(unittest.TestCase):
    """测试重置功能"""
    
    def setUp(self):
        self.model = JingQiShenModel()
    
    def test_reset_clears_history(self):
        self.model.nourish_jing()
        self.model.regulate_qi()
        
        self.model.reset()
        
        self.assertEqual(len(self.model.regulation_history), 0)
    
    def test_reset_to_default_values(self):
        self.model.current_level.jing_level = 0.8
        self.model.current_level.qi_level = 0.8
        self.model.current_level.shen_level = 0.8
        
        self.model.reset()
        
        self.assertEqual(self.model.current_level.jing_level, 0.5)
        self.assertEqual(self.model.current_level.qi_level, 0.5)
        self.assertEqual(self.model.current_level.shen_level, 0.5)
    
    def test_reset_to_custom_values(self):
        self.model.reset(initial_level=JingQiShenLevel(
            jing_level=0.7, qi_level=0.6, shen_level=0.8
        ))
        
        self.assertEqual(self.model.current_level.jing_level, 0.7)
        self.assertEqual(self.model.current_level.qi_level, 0.6)
        self.assertEqual(self.model.current_level.shen_level, 0.8)


class TestFactoryFunction(unittest.TestCase):
    """测试工厂函数"""
    
    def test_create_jing_qi_shen_model_default(self):
        model = create_jing_qi_shen_model()
        
        self.assertIsInstance(model, JingQiShenModel)
        self.assertEqual(model.current_level.jing_level, 0.5)
        self.assertEqual(model.current_level.qi_level, 0.5)
        self.assertEqual(model.current_level.shen_level, 0.5)
    
    def test_create_jing_qi_shen_model_custom(self):
        model = create_jing_qi_shen_model(
            jing_level=0.8, qi_level=0.7, shen_level=0.6
        )
        
        self.assertEqual(model.current_level.jing_level, 0.8)
        self.assertEqual(model.current_level.qi_level, 0.7)
        self.assertEqual(model.current_level.shen_level, 0.6)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_regulation_cycle(self):
        model = JingQiShenModel()
        
        model.current_level.jing_level = 0.2
        model.current_level.qi_level = 0.25
        model.current_level.shen_level = 0.2
        
        initial_vitality = model.current_level.overall_vitality
        
        model.balance()
        model.assess()
        
        final_vitality = model.current_level.overall_vitality
        
        self.assertGreater(final_vitality, initial_vitality)
    
    def test_context_driven_regulation(self):
        model = JingQiShenModel()
        
        high_activity_context = {"activity_level": 0.8, "mental_load": 0.7}
        
        for _ in range(5):
            model.assess(context=high_activity_context)
        
        self.assertLess(model.current_level.qi_level, 0.5)
        self.assertLess(model.current_level.shen_level, 0.5)
        
        model.balance()
        
        self.assertGreater(model.current_level.overall_vitality, 0.3)
    
    def test_inter_influence_chain(self):
        model = JingQiShenModel()
        
        model.current_level.jing_level = 0.5
        model.current_level.qi_level = 0.5
        model.current_level.shen_level = 0.9
        
        for _ in range(3):
            model._apply_inter_influences()
        
        self.assertGreater(model.current_level.qi_level, 0.5)
        self.assertGreater(model.current_level.jing_level, 0.5)
    
    def test_regulation_history_consistency(self):
        model = JingQiShenModel()
        
        model.nourish_jing()
        model.regulate_qi()
        model.gather_shen()
        model.balance()
        
        history = model.get_regulation_history()
        
        modes = [h["mode"] for h in history]
        self.assertIn("平衡", modes)
        self.assertIn("聚神", modes)
        self.assertIn("调气", modes)
        self.assertIn("养精", modes)
    
    def test_long_term_stability(self):
        model = JingQiShenModel()
        
        for i in range(20):
            model.assess(context={"activity_level": 0.3})
            
            if i % 5 == 0:
                model.balance()
        
        self.assertGreater(model.current_level.overall_vitality, 0.3)
        self.assertGreater(model.current_level.balance_score, 0.5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
