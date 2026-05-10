"""
Unit tests for Dao Heart System
道心心脏系统单元测试
"""

import unittest
import sys
import os
import time
import threading
import importlib.util
from datetime import datetime
from typing import Any, Dict, List

_test_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_test_dir, '..', '..'))

_heart_system_path = os.path.join(_project_root, "oriental_agent", "core", "heart_system.py")
_spec = importlib.util.spec_from_file_location("heart_system", _heart_system_path)
heart_system_module = importlib.util.module_from_spec(_spec)
sys.modules["heart_system"] = heart_system_module
_spec.loader.exec_module(heart_system_module)

DaoHeartSystem = heart_system_module.DaoHeartSystem
HeartBeat = heart_system_module.HeartBeat
EnergyPacket = heart_system_module.EnergyPacket
HeartRhythm = heart_system_module.HeartRhythm
HealthMetrics = heart_system_module.HealthMetrics
HeartState = heart_system_module.HeartState
HeartHealthLevel = heart_system_module.HeartHealthLevel
LoadLevel = heart_system_module.LoadLevel
create_heart_system = heart_system_module.create_heart_system


class TestHeartBeat(unittest.TestCase):
    """测试 HeartBeat 数据结构"""
    
    def test_heartbeat_creation(self):
        heartbeat = HeartBeat(
            beat_id="test_beat_001",
            timestamp=datetime.now(),
            energy_output=1.5,
            state_info={"test": "value"}
        )
        
        self.assertEqual(heartbeat.beat_id, "test_beat_001")
        self.assertEqual(heartbeat.energy_output, 1.5)
        self.assertIn("test", heartbeat.state_info)
    
    def test_heartbeat_auto_id(self):
        heartbeat1 = HeartBeat()
        heartbeat2 = HeartBeat()
        
        self.assertNotEqual(heartbeat1.beat_id, heartbeat2.beat_id)
        self.assertIsNotNone(heartbeat1.beat_id)
    
    def test_heartbeat_to_dict(self):
        heartbeat = HeartBeat(
            beat_id="test_001",
            energy_output=2.0,
            state_info={"key": "value"},
            cycle_duration=1.0,
            pump_strength=1.5,
            load_factor=1.2
        )
        
        result = heartbeat.to_dict()
        
        self.assertEqual(result["beat_id"], "test_001")
        self.assertEqual(result["energy_output"], 2.0)
        self.assertEqual(result["cycle_duration"], 1.0)
        self.assertEqual(result["pump_strength"], 1.5)
        self.assertEqual(result["load_factor"], 1.2)
        self.assertIn("timestamp", result)


class TestEnergyPacket(unittest.TestCase):
    """测试 EnergyPacket 数据结构"""
    
    def test_energy_packet_creation(self):
        packet = EnergyPacket(
            energy_value=1.5,
            state_info={"status": "active"},
            target_subsystem="memory"
        )
        
        self.assertEqual(packet.energy_value, 1.5)
        self.assertEqual(packet.target_subsystem, "memory")
        self.assertIn("status", packet.state_info)
    
    def test_energy_packet_defaults(self):
        packet = EnergyPacket()
        
        self.assertEqual(packet.energy_value, 1.0)
        self.assertEqual(packet.target_subsystem, "general")
        self.assertEqual(packet.priority, 5)
        self.assertEqual(packet.wuxing_attribute, "土")
        self.assertEqual(packet.yin_yang_balance, 0.0)
    
    def test_energy_packet_to_dict(self):
        packet = EnergyPacket(
            energy_value=2.5,
            state_info={"test": True},
            target_subsystem="thinking",
            priority=3
        )
        
        result = packet.to_dict()
        
        self.assertEqual(result["energy_value"], 2.5)
        self.assertEqual(result["target_subsystem"], "thinking")
        self.assertEqual(result["priority"], 3)
        self.assertIn("packet_id", result)


class TestHeartRhythm(unittest.TestCase):
    """测试心脏节律模型"""
    
    def test_rhythm_defaults(self):
        rhythm = HeartRhythm()
        
        self.assertEqual(rhythm.base_cycle, 1.0)
        self.assertEqual(rhythm.current_cycle, 1.0)
        self.assertEqual(rhythm.base_strength, 1.0)
        self.assertEqual(rhythm.current_strength, 1.0)
        self.assertEqual(rhythm.rhythm_stability, 1.0)
    
    def test_rhythm_adjust_high_load(self):
        rhythm = HeartRhythm()
        rhythm.adjust_for_load(1.5)
        
        self.assertLess(rhythm.current_cycle, rhythm.base_cycle)
        self.assertGreater(rhythm.current_strength, rhythm.base_strength)
        self.assertLess(rhythm.rhythm_stability, 1.0)
    
    def test_rhythm_adjust_low_load(self):
        rhythm = HeartRhythm()
        rhythm.adjust_for_load(0.7)
        
        self.assertGreater(rhythm.current_cycle, rhythm.base_cycle)
        self.assertLess(rhythm.current_strength, rhythm.base_strength)
    
    def test_rhythm_cycle_limits(self):
        rhythm = HeartRhythm()
        
        rhythm.adjust_for_load(2.0)
        self.assertGreaterEqual(rhythm.current_cycle, rhythm.min_cycle)
        self.assertLessEqual(rhythm.current_strength, rhythm.max_strength)
        
        rhythm.adjust_for_load(0.5)
        self.assertLessEqual(rhythm.current_cycle, rhythm.max_cycle)
        self.assertGreaterEqual(rhythm.current_strength, rhythm.min_strength)
    
    def test_rhythm_reset(self):
        rhythm = HeartRhythm()
        rhythm.adjust_for_load(1.8)
        rhythm.reset()
        
        self.assertEqual(rhythm.current_cycle, rhythm.base_cycle)
        self.assertEqual(rhythm.current_strength, rhythm.base_strength)
        self.assertEqual(rhythm.rhythm_stability, 1.0)


class TestHealthMetrics(unittest.TestCase):
    """测试健康指标"""
    
    def test_health_metrics_defaults(self):
        metrics = HealthMetrics()
        
        self.assertEqual(metrics.overall_health, 1.0)
        self.assertEqual(metrics.energy_efficiency, 1.0)
        self.assertEqual(metrics.stress_level, 0.0)
        self.assertEqual(metrics.damage_accumulated, 0.0)
    
    def test_calculate_health_level_optimal(self):
        metrics = HealthMetrics(overall_health=0.96)
        self.assertEqual(metrics.calculate_health_level(), HeartHealthLevel.OPTIMAL)
    
    def test_calculate_health_level_good(self):
        metrics = HealthMetrics(overall_health=0.87)
        self.assertEqual(metrics.calculate_health_level(), HeartHealthLevel.GOOD)
    
    def test_calculate_health_level_normal(self):
        metrics = HealthMetrics(overall_health=0.75)
        self.assertEqual(metrics.calculate_health_level(), HeartHealthLevel.NORMAL)
    
    def test_calculate_health_level_suboptimal(self):
        metrics = HealthMetrics(overall_health=0.55)
        self.assertEqual(metrics.calculate_health_level(), HeartHealthLevel.SUBOPTIMAL)
    
    def test_calculate_health_level_poor(self):
        metrics = HealthMetrics(overall_health=0.35)
        self.assertEqual(metrics.calculate_health_level(), HeartHealthLevel.POOR)
    
    def test_calculate_health_level_critical(self):
        metrics = HealthMetrics(overall_health=0.20)
        self.assertEqual(metrics.calculate_health_level(), HeartHealthLevel.CRITICAL)
    
    def test_update_health(self):
        metrics = HealthMetrics(
            energy_efficiency=0.9,
            rhythm_regularity=0.8,
            recovery_rate=0.7,
            stress_level=0.2,
            damage_accumulated=0.1
        )
        metrics.update_health()
        
        expected = (
            0.9 * 0.3 +
            0.8 * 0.3 +
            0.7 * 0.2 +
            (1.0 - 0.2) * 0.1 +
            (1.0 - 0.1) * 0.1
        )
        self.assertAlmostEqual(metrics.overall_health, expected, places=5)


class TestDaoHeartSystemRhythmicPumping(unittest.TestCase):
    """测试节律泵送功能"""
    
    def setUp(self):
        self.heart = DaoHeartSystem(base_cycle=0.1, base_strength=1.0)
    
    def tearDown(self):
        self.heart.stop()
    
    def test_heart_start(self):
        self.assertEqual(self.heart.state, HeartState.STOPPED)
        
        result = self.heart.start()
        
        self.assertTrue(result)
        self.assertEqual(self.heart.state, HeartState.BEATING)
    
    def test_heart_stop(self):
        self.heart.start()
        time.sleep(0.05)
        
        result = self.heart.stop()
        
        self.assertTrue(result)
        self.assertEqual(self.heart.state, HeartState.STOPPED)
    
    def test_single_beat(self):
        heartbeat = self.heart.beat()
        
        self.assertIsInstance(heartbeat, HeartBeat)
        self.assertIsNotNone(heartbeat.beat_id)
        self.assertIsNotNone(heartbeat.timestamp)
        self.assertGreater(heartbeat.energy_output, 0)
    
    def test_beat_count_increment(self):
        initial_count = self.heart._beat_count
        
        self.heart.beat()
        self.heart.beat()
        self.heart.beat()
        
        self.assertEqual(self.heart._beat_count, initial_count + 3)
    
    def test_energy_pumped_accumulation(self):
        initial_energy = self.heart._total_energy_pumped
        
        self.heart.beat()
        
        self.assertGreater(self.heart._total_energy_pumped, initial_energy)
    
    def test_beat_history_recording(self):
        for _ in range(5):
            self.heart.beat()
        
        history = self.heart.get_beat_history(limit=10)
        
        self.assertEqual(len(history), 5)
    
    def test_beat_history_limit(self):
        for _ in range(150):
            self.heart.beat()
        
        self.assertLessEqual(len(self.heart._beat_history), 100)
    
    def test_continuous_beating(self):
        received_packets: List[EnergyPacket] = []
        
        def callback(packet: EnergyPacket):
            received_packets.append(packet)
        
        self.heart.register_subsystem("test", callback)
        self.heart.start()
        time.sleep(0.35)
        self.heart.stop()
        
        self.assertGreater(len(received_packets), 1)
    
    def test_state_info_in_beat(self):
        self.heart.beat()
        self.heart.beat()
        
        heartbeat = self.heart.beat()
        
        self.assertIn("beat_count", heartbeat.state_info)
        self.assertIn("load_factor", heartbeat.state_info)
        self.assertIn("health_level", heartbeat.state_info)
        self.assertEqual(heartbeat.state_info["beat_count"], 2)


class TestDaoHeartSystemLoadAdjustment(unittest.TestCase):
    """测试负荷调节功能"""
    
    def setUp(self):
        self.heart = DaoHeartSystem(base_cycle=1.0, base_strength=1.0)
    
    def tearDown(self):
        self.heart.stop()
    
    def test_adjust_load_normal(self):
        result = self.heart.adjust_load(1.5)
        
        self.assertTrue(result)
        self.assertEqual(self.heart._current_load, 1.5)
    
    def test_adjust_load_high(self):
        self.heart.adjust_load(2.0)
        
        self.assertEqual(self.heart._current_load, 2.0)
        self.assertLess(self.heart.rhythm.current_cycle, self.heart.rhythm.base_cycle)
        self.assertGreater(self.heart.rhythm.current_strength, self.heart.rhythm.base_strength)
    
    def test_adjust_load_low(self):
        self.heart.adjust_load(0.5)
        
        self.assertEqual(self.heart._current_load, 0.5)
        self.assertGreater(self.heart.rhythm.current_cycle, self.heart.rhythm.base_cycle)
        self.assertLess(self.heart.rhythm.current_strength, self.heart.rhythm.base_strength)
    
    def test_load_factor_clamping_max(self):
        self.heart.adjust_load(3.0)
        
        self.assertEqual(self.heart._current_load, 2.0)
    
    def test_load_factor_clamping_min(self):
        self.heart.adjust_load(0.2)
        
        self.assertEqual(self.heart._current_load, 0.5)
    
    def test_load_affects_energy_output(self):
        self.heart.adjust_load(1.0)
        beat1 = self.heart.beat()
        
        self.heart.adjust_load(2.0)
        beat2 = self.heart.beat()
        
        self.assertGreater(beat2.energy_output, beat1.energy_output)
    
    def test_load_history_tracking(self):
        self.heart.adjust_load(1.0)
        self.heart.adjust_load(1.5)
        self.heart.adjust_load(2.0)
        
        self.assertEqual(len(self.heart._load_history), 3)
        self.assertEqual(self.heart._load_history[-1], 2.0)
    
    def test_high_load_stress_accumulation(self):
        initial_stress = self.heart._stress_accumulator
        
        self.heart.adjust_load(1.8)
        
        self.assertGreater(self.heart._stress_accumulator, initial_stress)


class TestDaoHeartSystemHealthMonitoring(unittest.TestCase):
    """测试健康监测功能"""
    
    def setUp(self):
        self.heart = DaoHeartSystem(base_cycle=1.0, base_strength=1.0)
    
    def tearDown(self):
        self.heart.stop()
    
    def test_check_health_returns_dict(self):
        health = self.heart.check_health()
        
        self.assertIsInstance(health, dict)
        self.assertIn("health_level", health)
        self.assertIn("overall_health", health)
        self.assertIn("energy_efficiency", health)
    
    def test_initial_health_optimal(self):
        health = self.heart.check_health()
        
        self.assertEqual(health["health_level"], HeartHealthLevel.OPTIMAL.value)
        self.assertGreaterEqual(health["overall_health"], 0.95)
    
    def test_health_degradation_under_stress(self):
        self.heart.health.stress_level = 0.5
        self.heart.health.damage_accumulated = 0.2
        self.heart.health.energy_efficiency = 0.8
        
        health = self.heart.check_health()
        
        self.assertLess(health["overall_health"], 1.0)
    
    def test_rhythm_regularity_calculation(self):
        for _ in range(10):
            self.heart.beat()
            time.sleep(0.01)
        
        health = self.heart.check_health()
        
        self.assertIn("rhythm_regularity", health)
        self.assertGreater(health["rhythm_regularity"], 0.0)
    
    def test_get_status(self):
        status = self.heart.get_status()
        
        self.assertIn("state", status)
        self.assertIn("beat_count", status)
        self.assertIn("total_energy_pumped", status)
        self.assertIn("current_cycle", status)
        self.assertIn("current_strength", status)
        self.assertIn("health", status)


class TestDaoHeartSystemSelfRepair(unittest.TestCase):
    """测试自我修复功能"""
    
    def setUp(self):
        self.heart = DaoHeartSystem(base_cycle=1.0, base_strength=1.0, auto_repair=False)
    
    def tearDown(self):
        self.heart.stop()
    
    def test_self_repair_improves_health(self):
        self.heart.health.damage_accumulated = 0.3
        self.heart.health.stress_level = 0.4
        self.heart.health.energy_efficiency = 0.7
        self.heart.health.update_health()
        self.heart.start()
        
        result = self.heart.self_repair()
        
        self.assertTrue(result["success"])
        self.assertGreater(result["current_health"], result["previous_health"])
    
    def test_self_repair_reduces_damage(self):
        self.heart.start()
        self.heart.health.damage_accumulated = 0.3
        initial_damage = self.heart.health.damage_accumulated
        
        self.heart.self_repair()
        
        self.assertLess(self.heart.health.damage_accumulated, initial_damage)
    
    def test_self_repair_reduces_stress(self):
        self.heart.start()
        self.heart.health.stress_level = 0.5
        initial_stress = self.heart.health.stress_level
        
        self.heart.self_repair()
        
        self.assertLess(self.heart.health.stress_level, initial_stress)
    
    def test_self_repair_stopped_heart(self):
        self.heart.stop()
        
        result = self.heart.self_repair()
        
        self.assertFalse(result["success"])
        self.assertIn("message", result)
    
    def test_auto_repair_triggers(self):
        heart = DaoHeartSystem(
            base_cycle=0.1,
            base_strength=1.0,
            auto_repair=True,
            repair_threshold=0.8
        )
        heart.health.overall_health = 0.6
        heart.start()
        time.sleep(0.25)
        heart.stop()
        
        self.assertGreater(heart.health.overall_health, 0.6)
    
    def test_repair_returns_health_level(self):
        self.heart.start()
        
        result = self.heart.self_repair()
        
        self.assertIn("health_level", result)
    
    def test_repair_state_transition(self):
        self.heart.start()
        self.heart.state = HeartState.BEATING
        
        self.heart.self_repair()
        
        self.assertEqual(self.heart.state, HeartState.BEATING)


class TestDaoHeartSystemEnergyDispatch(unittest.TestCase):
    """测试能量分发功能"""
    
    def setUp(self):
        self.heart = DaoHeartSystem(base_cycle=1.0, base_strength=1.0)
    
    def tearDown(self):
        self.heart.stop()
    
    def test_register_subsystem(self):
        def callback(packet):
            pass
        
        result = self.heart.register_subsystem("memory", callback)
        
        self.assertTrue(result)
        self.assertIn("memory", self.heart._subsystem_callbacks)
    
    def test_unregister_subsystem(self):
        def callback(packet):
            pass
        
        self.heart.register_subsystem("memory", callback)
        result = self.heart.unregister_subsystem("memory")
        
        self.assertTrue(result)
        self.assertNotIn("memory", self.heart._subsystem_callbacks)
    
    def test_unregister_nonexistent_subsystem(self):
        result = self.heart.unregister_subsystem("nonexistent")
        
        self.assertFalse(result)
    
    def test_energy_dispatch_to_subsystem(self):
        received_packets: List[EnergyPacket] = []
        
        def callback(packet: EnergyPacket):
            received_packets.append(packet)
        
        self.heart.register_subsystem("test_subsystem", callback)
        self.heart.beat()
        
        self.assertEqual(len(received_packets), 1)
        self.assertEqual(received_packets[0].target_subsystem, "test_subsystem")
    
    def test_energy_dispatch_multiple_subsystems(self):
        received: Dict[str, List[EnergyPacket]] = {
            "memory": [],
            "thinking": [],
            "perception": []
        }
        
        def make_callback(name):
            def callback(packet: EnergyPacket):
                received[name].append(packet)
            return callback
        
        for name in received.keys():
            self.heart.register_subsystem(name, make_callback(name))
        
        self.heart.beat()
        
        for name in received.keys():
            self.assertEqual(len(received[name]), 1)
    
    def test_energy_division_among_subsystems(self):
        received_packets: List[EnergyPacket] = []
        
        def callback(packet: EnergyPacket):
            received_packets.append(packet)
        
        self.heart.register_subsystem("sub1", callback)
        self.heart.register_subsystem("sub2", callback)
        
        heartbeat = self.heart.beat()
        total_received = sum(p.energy_value for p in received_packets)
        
        self.assertAlmostEqual(total_received, heartbeat.energy_output, places=5)
    
    def test_callback_exception_handling(self):
        def bad_callback(packet):
            raise Exception("Test exception")
        
        received_packets: List[EnergyPacket] = []
        
        def good_callback(packet):
            received_packets.append(packet)
        
        self.heart.register_subsystem("bad", bad_callback)
        self.heart.register_subsystem("good", good_callback)
        
        heartbeat = self.heart.beat()
        
        self.assertEqual(len(received_packets), 1)


class TestDaoHeartSystemCriticalState(unittest.TestCase):
    """测试危急状态处理"""
    
    def setUp(self):
        self.heart = DaoHeartSystem(base_cycle=1.0, base_strength=1.0)
    
    def tearDown(self):
        self.heart.stop()
    
    def test_critical_state_on_low_health(self):
        self.heart.health.energy_efficiency = 0.3
        self.heart.health.rhythm_regularity = 0.3
        self.heart.health.recovery_rate = 0.2
        self.heart.health.stress_level = 0.8
        self.heart.health.damage_accumulated = 0.5
        self.heart.health.update_health()
        
        self.heart.start()
        self.heart._update_health_metrics()
        
        self.assertLess(self.heart.health.overall_health, 0.3)
        self.assertEqual(self.heart.state, HeartState.CRITICAL)
    
    def test_cannot_start_from_critical_low_health(self):
        self.heart.health.overall_health = 0.15
        self.heart.state = HeartState.CRITICAL
        
        result = self.heart.start()
        
        self.assertFalse(result)
    
    def test_can_start_from_critical_sufficient_health(self):
        self.heart.health.overall_health = 0.25
        self.heart.state = HeartState.CRITICAL
        
        result = self.heart.start()
        
        self.assertTrue(result)


class TestCreateHeartSystemFactory(unittest.TestCase):
    """测试工厂函数"""
    
    def test_create_heart_system_defaults(self):
        heart = create_heart_system()
        
        self.assertEqual(heart.rhythm.base_cycle, 1.0)
        self.assertEqual(heart.rhythm.base_strength, 1.0)
        self.assertTrue(heart.auto_repair)
    
    def test_create_heart_system_custom(self):
        heart = create_heart_system(
            base_cycle=0.5,
            base_strength=1.5,
            auto_repair=False
        )
        
        self.assertEqual(heart.rhythm.base_cycle, 0.5)
        self.assertEqual(heart.rhythm.base_strength, 1.5)
        self.assertFalse(heart.auto_repair)


class TestDaoHeartSystemIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        self.heart = DaoHeartSystem(base_cycle=0.1, base_strength=1.0)
    
    def tearDown(self):
        self.heart.stop()
    
    def test_full_lifecycle(self):
        received_packets: List[EnergyPacket] = []
        
        def callback(packet: EnergyPacket):
            received_packets.append(packet)
        
        self.heart.register_subsystem("main", callback)
        
        self.heart.start()
        self.assertEqual(self.heart.state, HeartState.BEATING)
        
        time.sleep(0.25)
        
        self.heart.adjust_load(1.5)
        time.sleep(0.15)
        
        self.heart.adjust_load(0.8)
        time.sleep(0.15)
        
        self.heart.stop()
        self.assertEqual(self.heart.state, HeartState.STOPPED)
        
        self.assertGreater(len(received_packets), 0)
        self.assertGreater(self.heart._beat_count, 0)
        self.assertGreater(self.heart._total_energy_pumped, 0)
    
    def test_health_monitoring_during_operation(self):
        self.heart.start()
        
        initial_health = self.heart.check_health()["overall_health"]
        
        for _ in range(5):
            self.heart.adjust_load(1.8)
            time.sleep(0.05)
        
        final_health = self.heart.check_health()["overall_health"]
        
        self.heart.stop()
        
        self.assertGreater(initial_health, 0.9)


if __name__ == '__main__':
    unittest.main(verbosity=2)
