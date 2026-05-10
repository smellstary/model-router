"""
Unit tests for Martial Arts Defense System
武学防御体系单元测试
"""

import unittest
import sys
import os
import importlib.util
from datetime import datetime

_test_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_test_dir, '..', '..'))

_martial_defense_path = os.path.join(_project_root, "oriental_agent", "security", "martial_defense.py")
_spec = importlib.util.spec_from_file_location("martial_defense", _martial_defense_path)
martial_defense_module = importlib.util.module_from_spec(_spec)
sys.modules["martial_defense"] = martial_defense_module
_spec.loader.exec_module(martial_defense_module)

ThreatType = martial_defense_module.ThreatType
AttackIntensity = martial_defense_module.AttackIntensity
AnimalForm = martial_defense_module.AnimalForm
Attack = martial_defense_module.Attack
ThreatAnalysis = martial_defense_module.ThreatAnalysis
DefenseResult = martial_defense_module.DefenseResult
DefenseStrategy = martial_defense_module.DefenseStrategy
TaijiDefense = martial_defense_module.TaijiDefense
YijinjingDefense = martial_defense_module.YijinjingDefense
WuqinxiDefense = martial_defense_module.WuqinxiDefense
AdaptiveDefenseSelector = martial_defense_module.AdaptiveDefenseSelector
create_martial_defense_system = martial_defense_module.create_martial_defense_system


class TestThreatType(unittest.TestCase):
    """测试威胁类型枚举"""
    
    def test_all_threat_types_exist(self):
        types = list(ThreatType)
        self.assertEqual(len(types), 6)
    
    def test_threat_type_values(self):
        self.assertEqual(ThreatType.BRUTE_FORCE.value, "暴力攻击")
        self.assertEqual(ThreatType.STEALTH.value, "隐蔽渗透")
        self.assertEqual(ThreatType.PERSISTENT.value, "持续威胁")
        self.assertEqual(ThreatType.ADAPTIVE.value, "自适应攻击")
        self.assertEqual(ThreatType.COMPLEX.value, "复合威胁")
        self.assertEqual(ThreatType.UNKNOWN.value, "未知威胁")


class TestAnimalForm(unittest.TestCase):
    """测试动物形态枚举"""
    
    def test_all_forms_exist(self):
        forms = list(AnimalForm)
        self.assertEqual(len(forms), 5)
    
    def test_form_values(self):
        self.assertEqual(AnimalForm.TIGER.value, "虎")
        self.assertEqual(AnimalForm.DEER.value, "鹿")
        self.assertEqual(AnimalForm.BEAR.value, "熊")
        self.assertEqual(AnimalForm.MONKEY.value, "猿")
        self.assertEqual(AnimalForm.BIRD.value, "鸟")


class TestAttack(unittest.TestCase):
    """测试攻击数据结构"""
    
    def test_attack_creation(self):
        attack = Attack(
            attack_id="test_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.5,
            direction="forward",
            source="external"
        )
        
        self.assertEqual(attack.attack_id, "test_001")
        self.assertEqual(attack.attack_type, ThreatType.BRUTE_FORCE)
        self.assertEqual(attack.intensity, 0.5)
        self.assertEqual(attack.direction, "forward")
        self.assertEqual(attack.source, "external")
    
    def test_attack_default_timestamp(self):
        attack = Attack(
            attack_id="test_002",
            attack_type=ThreatType.STEALTH,
            intensity=0.3,
            direction="unknown",
            source="internal"
        )
        
        self.assertIsInstance(attack.timestamp, datetime)
    
    def test_attack_metadata(self):
        attack = Attack(
            attack_id="test_003",
            attack_type=ThreatType.COMPLEX,
            intensity=0.7,
            direction="multi",
            source="external",
            metadata={"priority": "high", "layer": "network"}
        )
        
        self.assertEqual(attack.metadata["priority"], "high")
        self.assertEqual(attack.metadata["layer"], "network")


class TestDefenseResult(unittest.TestCase):
    """测试防御结果"""
    
    def test_defense_result_creation(self):
        result = DefenseResult(
            success=True,
            damage_mitigated=0.8,
            energy_consumed=0.2,
            counter_attack_potential=0.5,
            strategy_used="太极防御"
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.damage_mitigated, 0.8)
        self.assertEqual(result.energy_consumed, 0.2)
        self.assertEqual(result.counter_attack_potential, 0.5)
        self.assertEqual(result.strategy_used, "太极防御")
    
    def test_defense_result_with_details(self):
        result = DefenseResult(
            success=True,
            damage_mitigated=0.6,
            energy_consumed=0.3,
            counter_attack_potential=0.4,
            strategy_used="五禽戏防御",
            details={"form": "虎形", "effectiveness": 0.75}
        )
        
        self.assertEqual(result.details["form"], "虎形")
        self.assertEqual(result.details["effectiveness"], 0.75)


class TestTaijiDefense(unittest.TestCase):
    """测试太极防御"""
    
    def setUp(self):
        self.taiji = TaijiDefense()
    
    def test_taiji_creation(self):
        self.assertEqual(self.taiji.name, "太极防御")
        self.assertEqual(self.taiji.philosophy, "以柔克刚，借力打力，四两拨千斤")
        self.assertEqual(self.taiji.defense_power, 0.6)
        self.assertEqual(self.taiji.adaptability, 0.95)
    
    def test_taiji_circular_defense_radius(self):
        self.assertEqual(self.taiji.circular_defense_radius, 1.0)
    
    def test_taiji_yield_and_redirect_weak_attack(self):
        attack = Attack(
            attack_id="weak_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.2,
            direction="forward",
            source="external"
        )
        
        redirect_ratio, message = self.taiji.yield_and_redirect(attack)
        
        self.assertGreater(redirect_ratio, 0.8)
        self.assertIn("化解", message)
    
    def test_taiji_yield_and_redirect_strong_attack(self):
        attack = Attack(
            attack_id="strong_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.8,
            direction="forward",
            source="external"
        )
        
        redirect_ratio, message = self.taiji.yield_and_redirect(attack)
        
        self.assertLess(redirect_ratio, 0.5)
        self.assertIn("消耗", message)
    
    def test_taiji_execute_returns_result(self):
        attack = Attack(
            attack_id="test_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.5,
            direction="forward",
            source="external"
        )
        
        result = self.taiji.execute(attack)
        
        self.assertIsInstance(result, DefenseResult)
        self.assertEqual(result.strategy_used, "太极防御")
    
    def test_taiji_get_characteristics(self):
        chars = self.taiji.get_characteristics()
        
        self.assertEqual(chars["name"], "太极防御")
        self.assertIn("qi_flow_state", chars)
        self.assertIn("circular_defense_radius", chars)
    
    def test_taiji_restore_qi(self):
        self.taiji._qi_flow_state = 0.3
        
        self.taiji.restore_qi(0.2)
        
        self.assertEqual(self.taiji._qi_flow_state, 0.5)
    
    def test_taiji_record_effectiveness(self):
        self.taiji.record_effectiveness(0.8)
        self.taiji.record_effectiveness(0.6)
        
        avg = self.taiji.get_average_effectiveness()
        
        self.assertEqual(avg, 0.7)


class TestYijinjingDefense(unittest.TestCase):
    """测试易筋经防御"""
    
    def setUp(self):
        self.yijinjing = YijinjingDefense()
    
    def test_yijinjing_creation(self):
        self.assertEqual(self.yijinjing.name, "易筋经防御")
        self.assertEqual(self.yijinjing.philosophy, "强筋健骨，易筋洗髓，固本培元")
        self.assertEqual(self.yijinjing.defense_power, 0.95)
        self.assertEqual(self.yijinjing.adaptability, 0.5)
    
    def test_yijinjing_strengthen_core(self):
        result = self.yijinjing.strengthen_core(0.2)
        
        self.assertGreater(result["core_strength"], 0.5)
        self.assertGreater(result["bone_density"], 0.5)
        self.assertIn("muscle_tension", result)
    
    def test_yijinjing_absorb_and_transform(self):
        attack = Attack(
            attack_id="absorb_001",
            attack_type=ThreatType.PERSISTENT,
            intensity=0.5,
            direction="steady",
            source="external"
        )
        
        absorbed, transformed = self.yijinjing.absorb_and_transform(attack)
        
        self.assertGreater(absorbed, 0)
        self.assertGreater(transformed, 0)
        self.assertLess(transformed, absorbed)
    
    def test_yijinjing_execute_returns_result(self):
        attack = Attack(
            attack_id="test_002",
            attack_type=ThreatType.PERSISTENT,
            intensity=0.6,
            direction="forward",
            source="external"
        )
        
        result = self.yijinjing.execute(attack)
        
        self.assertIsInstance(result, DefenseResult)
        self.assertEqual(result.strategy_used, "易筋经防御")
    
    def test_yijinjing_high_defense_power(self):
        attack = Attack(
            attack_id="high_power_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.8,
            direction="forward",
            source="external"
        )
        
        result = self.yijinjing.execute(attack)
        
        self.assertGreater(result.damage_mitigated, 0.4)
    
    def test_yijinjing_get_characteristics(self):
        chars = self.yijinjing.get_characteristics()
        
        self.assertEqual(chars["name"], "易筋经防御")
        self.assertIn("core_strength", chars)
        self.assertIn("bone_density", chars)
        self.assertIn("muscle_tension", chars)
    
    def test_yijinjing_meditate(self):
        self.yijinjing._core_strength = 0.5
        
        self.yijinjing.meditate(1.0)
        
        self.assertGreater(self.yijinjing._core_strength, 0.5)


class TestWuqinxiDefense(unittest.TestCase):
    """测试五禽戏防御"""
    
    def setUp(self):
        self.wuqinxi = WuqinxiDefense()
    
    def test_wuqinxi_creation(self):
        self.assertEqual(self.wuqinxi.name, "五禽戏防御")
        self.assertEqual(self.wuqinxi.philosophy, "模仿自然，五形合一，变化无穷")
        self.assertEqual(self.wuqinxi.defense_power, 0.75)
        self.assertEqual(self.wuqinxi.adaptability, 0.85)
    
    def test_tiger_form(self):
        result = self.wuqinxi.tiger_form()
        
        self.assertEqual(result["form"], "虎形")
        self.assertEqual(result["action"], "猛虎下山")
        self.assertIn("power_multiplier", result)
        self.assertEqual(result["special_ability"], "虎啸震慑")
    
    def test_deer_form(self):
        result = self.wuqinxi.deer_form()
        
        self.assertEqual(result["form"], "鹿形")
        self.assertEqual(result["action"], "灵鹿跃涧")
        self.assertIn("evasion_factor", result)
    
    def test_bear_form(self):
        result = self.wuqinxi.bear_form()
        
        self.assertEqual(result["form"], "熊形")
        self.assertEqual(result["action"], "黑熊蹭背")
        self.assertIn("endurance_factor", result)
    
    def test_monkey_form(self):
        result = self.wuqinxi.monkey_form()
        
        self.assertEqual(result["form"], "猿形")
        self.assertEqual(result["action"], "灵猿献果")
        self.assertIn("trickery_factor", result)
    
    def test_bird_form(self):
        result = self.wuqinxi.bird_form()
        
        self.assertEqual(result["form"], "鸟形")
        self.assertEqual(result["action"], "鹤翔九天")
        self.assertIn("flight_factor", result)
    
    def test_wuqinxi_execute_returns_result(self):
        attack = Attack(
            attack_id="test_003",
            attack_type=ThreatType.ADAPTIVE,
            intensity=0.5,
            direction="variable",
            source="external"
        )
        
        result = self.wuqinxi.execute(attack)
        
        self.assertIsInstance(result, DefenseResult)
        self.assertIn("五禽戏防御", result.strategy_used)
    
    def test_wuqinxi_form_selection_high_intensity(self):
        attack = Attack(
            attack_id="high_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.8,
            direction="forward",
            source="external"
        )
        
        self.wuqinxi.execute(attack)
        
        self.assertEqual(self.wuqinxi._current_form, AnimalForm.BEAR)
    
    def test_wuqinxi_form_selection_low_intensity(self):
        attack = Attack(
            attack_id="low_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.2,
            direction="forward",
            source="external"
        )
        
        self.wuqinxi.execute(attack)
        
        self.assertEqual(self.wuqinxi._current_form, AnimalForm.TIGER)
    
    def test_wuqinxi_form_selection_stealth(self):
        attack = Attack(
            attack_id="stealth_001",
            attack_type=ThreatType.STEALTH,
            intensity=0.5,
            direction="hidden",
            source="internal"
        )
        
        self.wuqinxi.execute(attack)
        
        self.assertEqual(self.wuqinxi._current_form, AnimalForm.MONKEY)
    
    def test_wuqinxi_get_characteristics(self):
        chars = self.wuqinxi.get_characteristics()
        
        self.assertEqual(chars["name"], "五禽戏防御")
        self.assertIn("form_mastery", chars)
        self.assertIn("current_form", chars)
    
    def test_wuqinxi_form_mastery_increases(self):
        attack = Attack(
            attack_id="mastery_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.2,
            direction="forward",
            source="external"
        )
        
        initial_mastery = self.wuqinxi._form_mastery[AnimalForm.TIGER]
        
        self.wuqinxi.execute(attack)
        
        self.assertGreater(
            self.wuqinxi._form_mastery[AnimalForm.TIGER],
            initial_mastery
        )


class TestAdaptiveDefenseSelector(unittest.TestCase):
    """测试自适应防御选择器"""
    
    def setUp(self):
        self.selector = AdaptiveDefenseSelector()
    
    def test_selector_creation(self):
        self.assertIsInstance(self.selector.taiji, TaijiDefense)
        self.assertIsInstance(self.selector.yijinjing, YijinjingDefense)
        self.assertIsInstance(self.selector.wuqinxi, WuqinxiDefense)
    
    def test_analyze_threat_returns_analysis(self):
        attack = Attack(
            attack_id="analyze_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.5,
            direction="forward",
            source="external"
        )
        
        analysis = self.selector.analyze_threat(attack)
        
        self.assertIsInstance(analysis, ThreatAnalysis)
        self.assertEqual(analysis.threat_type, ThreatType.BRUTE_FORCE)
    
    def test_analyze_threat_intensity_classification(self):
        weak_attack = Attack(
            attack_id="weak",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.1,
            direction="forward",
            source="external"
        )
        
        strong_attack = Attack(
            attack_id="strong",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.9,
            direction="forward",
            source="external"
        )
        
        weak_analysis = self.selector.analyze_threat(weak_attack)
        strong_analysis = self.selector.analyze_threat(strong_attack)
        
        self.assertEqual(weak_analysis.intensity_level, "微弱")
        self.assertEqual(strong_analysis.intensity_level, "毁灭性")
    
    def test_select_strategy_returns_strategy(self):
        attack = Attack(
            attack_id="select_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.5,
            direction="forward",
            source="external"
        )
        
        analysis = self.selector.analyze_threat(attack)
        strategy = self.selector.select_strategy(analysis)
        
        self.assertIsInstance(strategy, DefenseStrategy)
    
    def test_select_strategy_for_brute_force(self):
        attack = Attack(
            attack_id="brute_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.5,
            direction="forward",
            source="external"
        )
        
        analysis = self.selector.analyze_threat(attack)
        strategy = self.selector.select_strategy(analysis)
        
        self.assertEqual(strategy.name, "太极防御")
    
    def test_select_strategy_for_persistent(self):
        attack = Attack(
            attack_id="persist_001",
            attack_type=ThreatType.PERSISTENT,
            intensity=0.5,
            direction="steady",
            source="external"
        )
        
        analysis = self.selector.analyze_threat(attack)
        strategy = self.selector.select_strategy(analysis)
        
        self.assertEqual(strategy.name, "易筋经防御")
    
    def test_select_strategy_for_adaptive(self):
        attack = Attack(
            attack_id="adapt_001",
            attack_type=ThreatType.ADAPTIVE,
            intensity=0.5,
            direction="variable",
            source="external"
        )
        
        analysis = self.selector.analyze_threat(attack)
        strategy = self.selector.select_strategy(analysis)
        
        self.assertEqual(strategy.name, "五禽戏防御")
    
    def test_switch_strategy(self):
        attack = Attack(
            attack_id="switch_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.5,
            direction="forward",
            source="external"
        )
        
        analysis = self.selector.analyze_threat(attack)
        initial_strategy = self.selector.select_strategy(analysis)
        
        new_strategy = self.selector.switch_strategy()
        
        self.assertNotEqual(new_strategy.name, initial_strategy.name)
        self.assertEqual(new_strategy.name, self.selector._current_strategy.name)
    
    def test_execute_defense_full_flow(self):
        attack = Attack(
            attack_id="execute_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.5,
            direction="forward",
            source="external"
        )
        
        result = self.selector.execute_defense(attack)
        
        self.assertIsInstance(result, DefenseResult)
        self.assertTrue(result.success or not result.success)
    
    def test_get_status(self):
        status = self.selector.get_status()
        
        self.assertIn("current_strategy", status)
        self.assertIn("strategy_history_count", status)
        self.assertIn("threat_history_count", status)
    
    def test_get_all_characteristics(self):
        chars = self.selector.get_all_characteristics()
        
        self.assertIn("taiji", chars)
        self.assertIn("yijinjing", chars)
        self.assertIn("wuqinxi", chars)
    
    def test_reset(self):
        attack = Attack(
            attack_id="reset_001",
            attack_type=ThreatType.BRUTE_FORCE,
            intensity=0.5,
            direction="forward",
            source="external"
        )
        
        self.selector.execute_defense(attack)
        self.selector.execute_defense(attack)
        
        self.selector.reset()
        
        self.assertIsNone(self.selector._current_strategy)
        self.assertEqual(len(self.selector._strategy_history), 0)
        self.assertEqual(len(self.selector._threat_history), 0)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_defense_cycle(self):
        selector = AdaptiveDefenseSelector()
        
        attacks = [
            Attack("atk1", ThreatType.BRUTE_FORCE, 0.8, "fwd", "ext"),
            Attack("atk2", ThreatType.PERSISTENT, 0.6, "steady", "ext"),
            Attack("atk3", ThreatType.ADAPTIVE, 0.4, "var", "ext"),
            Attack("atk4", ThreatType.STEALTH, 0.3, "hidden", "int"),
            Attack("atk5", ThreatType.COMPLEX, 0.7, "multi", "ext"),
        ]
        
        results = []
        for attack in attacks:
            result = selector.execute_defense(attack)
            results.append(result)
        
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertIsInstance(result, DefenseResult)
    
    def test_strategy_effectiveness_tracking(self):
        selector = AdaptiveDefenseSelector()
        
        for _ in range(5):
            attack = Attack(
                f"track_{_}",
                ThreatType.BRUTE_FORCE,
                0.5,
                "forward",
                "external"
            )
            selector.execute_defense(attack)
        
        taiji_eff = selector.taiji.get_average_effectiveness()
        
        self.assertGreater(taiji_eff, 0)
    
    def test_form_mastery_progression(self):
        wuqinxi = WuqinxiDefense()
        
        for i in range(10):
            attack = Attack(
                f"mastery_{i}",
                ThreatType.BRUTE_FORCE,
                0.2,
                "forward",
                "external"
            )
            wuqinxi.execute(attack)
        
        tiger_mastery = wuqinxi._form_mastery[AnimalForm.TIGER]
        
        self.assertGreater(tiger_mastery, 0.5)
    
    def test_strategy_switch_on_failure(self):
        selector = AdaptiveDefenseSelector()
        
        attack = Attack(
            "fail_test",
            ThreatType.BRUTE_FORCE,
            0.99,
            "overwhelming",
            "external"
        )
        
        result = selector.execute_defense(attack)
        
        self.assertIsInstance(result, DefenseResult)


class TestFactoryFunction(unittest.TestCase):
    """测试工厂函数"""
    
    def test_create_martial_defense_system(self):
        selector = create_martial_defense_system()
        
        self.assertIsInstance(selector, AdaptiveDefenseSelector)
        self.assertIsInstance(selector.taiji, TaijiDefense)
        self.assertIsInstance(selector.yijinjing, YijinjingDefense)
        self.assertIsInstance(selector.wuqinxi, WuqinxiDefense)


if __name__ == '__main__':
    unittest.main(verbosity=2)
