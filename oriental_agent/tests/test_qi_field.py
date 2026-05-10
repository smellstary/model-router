"""
Unit tests for Qi Field Radiation System
气场辐射系统单元测试
"""

import unittest
import sys
import os
import importlib.util

_test_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_test_dir, '..', '..'))

_qi_field_path = os.path.join(_project_root, "oriental_agent", "interaction", "qi_field.py")
_spec = importlib.util.spec_from_file_location("qi_field", _qi_field_path)
qi_field_module = importlib.util.module_from_spec(_spec)
sys.modules["qi_field"] = qi_field_module
_spec.loader.exec_module(qi_field_module)

QiFieldType = qi_field_module.QiFieldType
QiFieldColor = qi_field_module.QiFieldColor
ResonanceType = qi_field_module.ResonanceType
IntentionType = qi_field_module.IntentionType
QiFieldState = qi_field_module.QiFieldState
QiFieldBoundary = qi_field_module.QiFieldBoundary
ResonanceResult = qi_field_module.ResonanceResult
QiFieldEmitter = qi_field_module.QiFieldEmitter
QiFieldVisualizer = qi_field_module.QiFieldVisualizer
QiFieldInteraction = qi_field_module.QiFieldInteraction
QiFieldSystem = qi_field_module.QiFieldSystem
create_qi_field_system = qi_field_module.create_qi_field_system


class TestQiFieldType(unittest.TestCase):
    """测试气场类型枚举"""
    
    def test_all_field_types_exist(self):
        types = list(QiFieldType)
        self.assertEqual(len(types), 8)
    
    def test_field_type_values(self):
        self.assertEqual(QiFieldType.NEUTRAL.value, "中和")
        self.assertEqual(QiFieldType.YANG_DOMINANT.value, "阳盛")
        self.assertEqual(QiFieldType.YIN_DOMINANT.value, "阴盛")
        self.assertEqual(QiFieldType.HARMONIOUS.value, "和谐")
        self.assertEqual(QiFieldType.AGGRESSIVE.value, "刚猛")
        self.assertEqual(QiFieldType.GENTLE.value, "柔和")
        self.assertEqual(QiFieldType.WISDOM.value, "智慧")
        self.assertEqual(QiFieldType.VITALITY.value, "生机")


class TestQiFieldColor(unittest.TestCase):
    """测试气场颜色枚举"""
    
    def test_all_colors_exist(self):
        colors = list(QiFieldColor)
        self.assertEqual(len(colors), 10)
    
    def test_color_values(self):
        self.assertEqual(QiFieldColor.WHITE.value, "白色")
        self.assertEqual(QiFieldColor.GOLD.value, "金色")
        self.assertEqual(QiFieldColor.RED.value, "红色")
        self.assertEqual(QiFieldColor.BLUE.value, "蓝色")
        self.assertEqual(QiFieldColor.GREEN.value, "绿色")


class TestResonanceType(unittest.TestCase):
    """测试共振类型枚举"""
    
    def test_all_resonance_types_exist(self):
        types = list(ResonanceType)
        self.assertEqual(len(types), 5)
    
    def test_resonance_type_values(self):
        self.assertEqual(ResonanceType.HARMONIC.value, "和谐共振")
        self.assertEqual(ResonanceType.DISCORDANT.value, "不和谐共振")
        self.assertEqual(ResonanceType.NEUTRAL.value, "中性共振")


class TestIntentionType(unittest.TestCase):
    """测试意图类型枚举"""
    
    def test_all_intention_types_exist(self):
        types = list(IntentionType)
        self.assertEqual(len(types), 6)
    
    def test_intention_type_values(self):
        self.assertEqual(IntentionType.HEALING.value, "治愈")
        self.assertEqual(IntentionType.PROTECTION.value, "防护")
        self.assertEqual(IntentionType.GUIDANCE.value, "引导")


class TestQiFieldState(unittest.TestCase):
    """测试气场状态数据结构"""
    
    def test_state_creation_default(self):
        state = QiFieldState()
        
        self.assertEqual(state.intensity, 50.0)
        self.assertEqual(state.radius, 1.0)
        self.assertEqual(state.frequency, 1.0)
        self.assertEqual(state.harmony, 0.5)
        self.assertEqual(state.color, QiFieldColor.WHITE)
    
    def test_state_creation_custom(self):
        state = QiFieldState(
            intensity=75.0,
            radius=2.0,
            frequency=1.5,
            harmony=0.8,
            color=QiFieldColor.GOLD
        )
        
        self.assertEqual(state.intensity, 75.0)
        self.assertEqual(state.radius, 2.0)
        self.assertEqual(state.frequency, 1.5)
        self.assertEqual(state.harmony, 0.8)
        self.assertEqual(state.color, QiFieldColor.GOLD)
    
    def test_state_clamp_upper(self):
        state = QiFieldState(intensity=150.0, harmony=1.5)
        
        self.assertEqual(state.intensity, 100.0)
        self.assertEqual(state.harmony, 1.0)
    
    def test_state_clamp_lower(self):
        state = QiFieldState(intensity=-10.0, harmony=-0.5)
        
        self.assertEqual(state.intensity, 0.0)
        self.assertEqual(state.harmony, 0.0)
    
    def test_power_calculation(self):
        state = QiFieldState(intensity=50.0, radius=2.0, harmony=0.5)
        
        expected_power = 50.0 * 2.0 * 0.5
        self.assertEqual(state.power, expected_power)
    
    def test_density_calculation(self):
        state = QiFieldState(intensity=100.0, radius=2.0)
        
        expected_density = 100.0 / 4.0
        self.assertEqual(state.density, expected_density)
    
    def test_wave_length_calculation(self):
        state = QiFieldState(frequency=2.0)
        
        self.assertEqual(state.wave_length, 0.5)
    
    def test_field_strength_at_distance(self):
        state = QiFieldState(intensity=100.0, radius=2.0, harmony=1.0)
        
        strength_at_origin = state.get_field_strength_at_distance(0)
        self.assertEqual(strength_at_origin, 100.0)
        
        strength_at_far = state.get_field_strength_at_distance(10)
        self.assertEqual(strength_at_far, 0.0)
    
    def test_to_dict(self):
        state = QiFieldState(intensity=60.0, radius=1.5)
        
        result = state.to_dict()
        
        self.assertEqual(result["intensity"], 60.0)
        self.assertEqual(result["radius"], 1.5)
        self.assertIn("power", result)
        self.assertIn("density", result)


class TestQiFieldBoundary(unittest.TestCase):
    """测试气场边界"""
    
    def test_boundary_creation(self):
        boundary = QiFieldBoundary(
            inner_radius=0.5,
            outer_radius=1.5,
            permeability=0.7
        )
        
        self.assertEqual(boundary.inner_radius, 0.5)
        self.assertEqual(boundary.outer_radius, 1.5)
        self.assertEqual(boundary.permeability, 0.7)
    
    def test_is_within_boundary(self):
        boundary = QiFieldBoundary(inner_radius=0.5, outer_radius=1.5)
        
        self.assertTrue(boundary.is_within_boundary(1.0))
        self.assertFalse(boundary.is_within_boundary(0.3))
        self.assertFalse(boundary.is_within_boundary(2.0))
    
    def test_boundary_strength(self):
        boundary = QiFieldBoundary(
            inner_radius=0.5,
            outer_radius=1.5,
            permeability=0.5,
            strength=1.0
        )
        
        strength_at_mid = boundary.get_boundary_strength(1.0)
        self.assertGreater(strength_at_mid, 0)
        
        strength_outside = boundary.get_boundary_strength(2.0)
        self.assertEqual(strength_outside, 0.0)


class TestQiFieldEmitter(unittest.TestCase):
    """测试气场发射器"""
    
    def setUp(self):
        self.emitter = QiFieldEmitter()
    
    def test_emitter_creation_default(self):
        self.assertEqual(self.emitter.state.intensity, 50.0)
        self.assertEqual(self.emitter._energy_reserve, 100.0)
        self.assertFalse(self.emitter.is_emitting)
    
    def test_emit_success(self):
        result = self.emitter.emit()
        
        self.assertTrue(result["success"])
        self.assertTrue(self.emitter.is_emitting)
    
    def test_emit_with_intensity(self):
        result = self.emitter.emit(intensity=80.0)
        
        self.assertTrue(result["success"])
        self.assertEqual(self.emitter.state.intensity, 80.0)
    
    def test_emit_insufficient_energy(self):
        self.emitter._energy_reserve = 0.5
        
        result = self.emitter.emit(intensity=100.0)
        
        self.assertFalse(result["success"])
    
    def test_adjust_intensity(self):
        result = self.emitter.adjust_intensity(75.0)
        
        self.assertEqual(result["old_intensity"], 50.0)
        self.assertEqual(result["new_intensity"], 75.0)
    
    def test_adjust_intensity_clamp(self):
        result = self.emitter.adjust_intensity(150.0)
        
        self.assertEqual(self.emitter.state.intensity, 100.0)
    
    def test_create_boundary(self):
        boundary = self.emitter.create_boundary(
            inner_radius=0.5,
            outer_radius=1.5,
            permeability=0.6
        )
        
        self.assertIsNotNone(self.emitter.boundary)
        self.assertEqual(boundary.inner_radius, 0.5)
    
    def test_remove_boundary(self):
        self.emitter.create_boundary()
        
        result = self.emitter.remove_boundary()
        
        self.assertTrue(result)
        self.assertIsNone(self.emitter.boundary)
    
    def test_resonate_with_harmonic(self):
        target = QiFieldState(
            intensity=50.0,
            frequency=1.0,
            harmony=0.8
        )
        
        result = self.emitter.resonate_with(target)
        
        self.assertIsInstance(result, ResonanceResult)
        self.assertIn(result.resonance_type, list(ResonanceType))
    
    def test_resonate_with_dissonant(self):
        self.emitter.state.frequency = 1.0
        self.emitter.state.harmony = 0.1
        self.emitter.state.intensity = 10.0
        
        target = QiFieldState(
            intensity=100.0,
            frequency=10.0,
            harmony=0.1
        )
        
        result = self.emitter.resonate_with(target)
        
        self.assertIn(result.resonance_type, [ResonanceType.DISCORDANT, ResonanceType.DAMPENING])
    
    def test_update_from_jing_qi_shen(self):
        result = self.emitter.update_from_jing_qi_shen(
            jing_level=0.8,
            qi_level=0.7,
            shen_level=0.9
        )
        
        self.assertIn("new_state", result)
        self.assertGreater(self.emitter.state.intensity, 50.0)
    
    def test_update_from_yinyang_balance_yang(self):
        result = self.emitter.update_from_yinyang_balance(0.5)
        
        self.assertEqual(self.emitter.state.field_type, QiFieldType.YANG_DOMINANT)
    
    def test_update_from_yinyang_balance_yin(self):
        result = self.emitter.update_from_yinyang_balance(-0.5)
        
        self.assertEqual(self.emitter.state.field_type, QiFieldType.YIN_DOMINANT)
    
    def test_update_from_wuxing(self):
        result = self.emitter.update_from_wuxing("火")
        
        self.assertEqual(self.emitter.state.color, QiFieldColor.RED)
    
    def test_recover_energy(self):
        self.emitter._energy_reserve = 50.0
        
        new_energy = self.emitter.recover_energy(20.0)
        
        self.assertEqual(new_energy, 70.0)
    
    def test_reset(self):
        self.emitter.emit()
        self.emitter.create_boundary()
        
        self.emitter.reset()
        
        self.assertEqual(self.emitter.state.intensity, 50.0)
        self.assertIsNone(self.emitter.boundary)
        self.assertFalse(self.emitter.is_emitting)


class TestQiFieldVisualizer(unittest.TestCase):
    """测试气场可视化器"""
    
    def setUp(self):
        self.visualizer = QiFieldVisualizer()
        self.state = QiFieldState(
            intensity=60.0,
            radius=2.0,
            frequency=1.5,
            harmony=0.7,
            color=QiFieldColor.BLUE
        )
    
    def test_visualize_state(self):
        result = self.visualizer.visualize_state(self.state)
        
        self.assertIn("color", result)
        self.assertIn("sound", result)
        self.assertIn("text", result)
    
    def test_to_color(self):
        result = self.visualizer.to_color(self.state)
        
        self.assertEqual(result["name"], "蓝色")
        self.assertIn("rgb", result)
        self.assertIn("hex", result)
    
    def test_to_sound(self):
        result = self.visualizer.to_sound(self.state)
        
        self.assertIn("frequency_hz", result)
        self.assertIn("volume", result)
        self.assertIn("musical_note", result)
    
    def test_to_text(self):
        result = self.visualizer.to_text(self.state)
        
        self.assertIn("气场", result)
        self.assertIn("强度", result)
        self.assertIn("和谐度", result)
    
    def test_to_ascii_art(self):
        result = self.visualizer.to_ascii_art(self.state)
        
        self.assertIsInstance(result, str)
        self.assertIn("◉", result)
    
    def test_shape_description(self):
        result = self.visualizer.visualize_state(self.state)
        
        self.assertIn("shape", result)
        self.assertIsInstance(result["shape"], str)
    
    def test_aura_layers(self):
        result = self.visualizer.visualize_state(self.state)
        
        self.assertIn("aura_layers", result)
        self.assertIsInstance(result["aura_layers"], list)


class TestQiFieldInteraction(unittest.TestCase):
    """测试气场交互"""
    
    def setUp(self):
        self.emitter = QiFieldEmitter()
        self.interaction = QiFieldInteraction(self.emitter)
    
    def test_sense_external(self):
        external = QiFieldState(intensity=40.0, frequency=1.2, harmony=0.6)
        
        result = self.interaction.sense_external(external)
        
        self.assertTrue(result["detected"])
        self.assertIn("threat_level", result)
        self.assertIn("compatibility", result)
    
    def test_sense_threat_assessment(self):
        weak_external = QiFieldState(intensity=20.0)
        
        result = self.interaction.sense_external(weak_external)
        
        self.assertEqual(result["threat_level"], "安全")
    
    def test_harmonize_success(self):
        target = QiFieldState(frequency=1.5, harmony=0.8)
        
        result = self.interaction.harmonize(target)
        
        self.assertTrue(result["success"])
        self.assertIn("resonance", result)
    
    def test_harmonize_insufficient_energy(self):
        self.emitter._energy_reserve = 1.0
        target = QiFieldState(frequency=1.5, harmony=0.8)
        
        result = self.interaction.harmonize(target)
        
        self.assertFalse(result["success"])
    
    def test_protect_success(self):
        result = self.interaction.protect(strength=0.7)
        
        self.assertTrue(result["success"])
        self.assertTrue(self.interaction.active_protection)
        self.assertEqual(self.interaction.protection_strength, 0.7)
    
    def test_protect_creates_boundary(self):
        self.interaction.protect(strength=0.5)
        
        self.assertIsNotNone(self.emitter.boundary)
    
    def test_protect_insufficient_energy(self):
        self.emitter._energy_reserve = 1.0
        
        result = self.interaction.protect()
        
        self.assertFalse(result["success"])
    
    def test_deactivate_protection(self):
        self.interaction.protect(strength=0.5)
        
        result = self.interaction.deactivate_protection()
        
        self.assertTrue(result["success"])
        self.assertFalse(self.interaction.active_protection)
    
    def test_project_intention(self):
        result = self.interaction.project_intention(
            intention=IntentionType.HEALING,
            target_distance=1.0,
            intensity=0.5
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["intention"], "治愈")
    
    def test_project_intention_insufficient_energy(self):
        self.emitter._energy_reserve = 1.0
        
        result = self.interaction.project_intention(IntentionType.HEALING)
        
        self.assertFalse(result["success"])
    
    def test_absorb_external_energy(self):
        external = QiFieldState(
            intensity=80.0,
            frequency=1.0,
            harmony=0.5,
            color=QiFieldColor.WHITE
        )
        
        result = self.interaction.absorb_external_energy(external, amount=0.2)
        
        self.assertTrue(result["success"])
        self.assertIn("absorbed_energy", result)
    
    def test_absorb_incompatible_field(self):
        self.emitter.state.frequency = 5.0
        self.emitter.state.harmony = 0.1
        self.emitter.state.color = QiFieldColor.RED
        
        external = QiFieldState(
            intensity=80.0,
            frequency=0.1,
            harmony=0.9,
            color=QiFieldColor.BLUE
        )
        
        result = self.interaction.absorb_external_energy(external)
        
        self.assertFalse(result["success"])
    
    def test_get_interaction_summary(self):
        external = QiFieldState(intensity=40.0)
        self.interaction.sense_external(external)
        
        summary = self.interaction.get_interaction_summary()
        
        self.assertEqual(summary["total_interactions"], 1)
        self.assertEqual(summary["detected_fields_count"], 1)


class TestQiFieldSystem(unittest.TestCase):
    """测试气场系统主类"""
    
    def setUp(self):
        self.system = QiFieldSystem()
    
    def test_system_creation(self):
        self.assertIsNotNone(self.system.emitter)
        self.assertIsNotNone(self.system.visualizer)
        self.assertIsNotNone(self.system.interaction)
    
    def test_initialize(self):
        result = self.system.initialize(
            jing_level=0.8,
            qi_level=0.7,
            shen_level=0.9,
            yinyang_balance=0.3,
            wuxing_element="火"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(self.system.emitter.state.color, QiFieldColor.RED)
    
    def test_emit_field(self):
        result = self.system.emit_field(intensity=70.0)
        
        self.assertTrue(result["success"])
    
    def test_visualize(self):
        result = self.system.visualize()
        
        self.assertIn("color", result)
        self.assertIn("sound", result)
        self.assertIn("text", result)
    
    def test_sense(self):
        external = QiFieldState(intensity=40.0)
        
        result = self.system.sense(external)
        
        self.assertTrue(result["detected"])
    
    def test_harmonize_with(self):
        target = QiFieldState(frequency=1.2, harmony=0.7)
        
        result = self.system.harmonize_with(target)
        
        self.assertTrue(result["success"])
    
    def test_activate_protection(self):
        result = self.system.activate_protection(strength=0.6)
        
        self.assertTrue(result["success"])
    
    def test_project(self):
        result = self.system.project(IntentionType.GUIDANCE, distance=2.0)
        
        self.assertTrue(result["success"])
    
    def test_get_full_status(self):
        status = self.system.get_full_status()
        
        self.assertIn("field_state", status)
        self.assertIn("visualization", status)
        self.assertIn("interaction", status)
        self.assertIn("energy_reserve", status)
    
    def test_reset(self):
        self.system.emit_field()
        self.system.activate_protection()
        
        self.system.reset()
        
        self.assertEqual(self.system.emitter.state.intensity, 50.0)
        self.assertFalse(self.system.interaction.active_protection)


class TestFactoryFunction(unittest.TestCase):
    """测试工厂函数"""
    
    def test_create_qi_field_system_default(self):
        system = create_qi_field_system()
        
        self.assertIsInstance(system, QiFieldSystem)
        self.assertEqual(system.emitter.state.intensity, 50.0)
    
    def test_create_qi_field_system_custom(self):
        system = create_qi_field_system(
            intensity=80.0,
            radius=2.0,
            harmony=0.8
        )
        
        self.assertEqual(system.emitter.state.intensity, 80.0)
        self.assertEqual(system.emitter.state.radius, 2.0)
        self.assertEqual(system.emitter.state.harmony, 0.8)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        system = QiFieldSystem()
        
        system.initialize(
            jing_level=0.7,
            qi_level=0.8,
            shen_level=0.6,
            yinyang_balance=0.2,
            wuxing_element="木"
        )
        
        emit_result = system.emit_field()
        self.assertTrue(emit_result["success"])
        
        visualization = system.visualize()
        self.assertIn("text", visualization)
        
        external = QiFieldState(intensity=30.0, frequency=1.0, harmony=0.5)
        sense_result = system.sense(external)
        self.assertTrue(sense_result["detected"])
        
        protect_result = system.activate_protection(strength=0.5)
        self.assertTrue(protect_result["success"])
        
        status = system.get_full_status()
        self.assertTrue(status["has_boundary"])
    
    def test_resonance_chain(self):
        emitter = QiFieldEmitter()
        
        fields = [
            QiFieldState(intensity=50.0, frequency=1.0, harmony=0.6),
            QiFieldState(intensity=55.0, frequency=1.1, harmony=0.65),
            QiFieldState(intensity=60.0, frequency=1.2, harmony=0.7)
        ]
        
        for field in fields:
            result = emitter.resonate_with(field)
            self.assertIsInstance(result, ResonanceResult)
    
    def test_energy_management(self):
        emitter = QiFieldEmitter()
        interaction = QiFieldInteraction(emitter)
        
        initial_energy = emitter.get_energy_reserve()
        
        for _ in range(5):
            emitter.emit()
        
        after_emit_energy = emitter.get_energy_reserve()
        self.assertLess(after_emit_energy, initial_energy)
        
        emitter.recover_energy(50.0)
        after_recovery = emitter.get_energy_reserve()
        self.assertGreater(after_recovery, after_emit_energy)
    
    def test_protection_and_interaction(self):
        system = QiFieldSystem()
        
        system.activate_protection(strength=0.8)
        
        hostile_field = QiFieldState(
            intensity=100.0,
            frequency=0.1,
            harmony=0.1
        )
        
        sense_result = system.sense(hostile_field)
        
        self.assertIn(sense_result["threat_level"], ["警戒", "危险", "注意", "安全"])
    
    def test_jing_qi_shen_influence(self):
        emitter = QiFieldEmitter()
        
        emitter.update_from_jing_qi_shen(0.9, 0.9, 0.9)
        high_vitality = emitter.state.intensity
        
        emitter.update_from_jing_qi_shen(0.2, 0.2, 0.2)
        low_vitality = emitter.state.intensity
        
        self.assertGreater(high_vitality, low_vitality)
    
    def test_wuxing_color_mapping(self):
        emitter = QiFieldEmitter()
        
        wuxing_colors = {
            "木": QiFieldColor.GREEN,
            "火": QiFieldColor.RED,
            "土": QiFieldColor.YELLOW,
            "金": QiFieldColor.WHITE,
            "水": QiFieldColor.BLUE
        }
        
        for element, expected_color in wuxing_colors.items():
            emitter.update_from_wuxing(element)
            self.assertEqual(emitter.state.color, expected_color)


if __name__ == '__main__':
    unittest.main(verbosity=2)
