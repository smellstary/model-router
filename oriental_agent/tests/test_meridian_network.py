"""
Unit tests for Meridian Energy Network System
经络能量网络系统单元测试
"""

import unittest
import sys
import os
import importlib.util

_test_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_test_dir, '..', '..'))

_meridian_network_path = os.path.join(_project_root, "oriental_agent", "body", "meridian_network.py")
_spec = importlib.util.spec_from_file_location("meridian_network", _meridian_network_path)
meridian_network_module = importlib.util.module_from_spec(_spec)
sys.modules["meridian_network"] = meridian_network_module
_spec.loader.exec_module(meridian_network_module)

MeridianType = meridian_network_module.MeridianType
MeridianCategory = meridian_network_module.MeridianCategory
MeridianChannel = meridian_network_module.MeridianChannel
MeridianNetwork = meridian_network_module.MeridianNetwork
EnergyFlowResult = meridian_network_module.EnergyFlowResult
BlockageInfo = meridian_network_module.BlockageInfo
create_meridian_network = meridian_network_module.create_meridian_network


class TestMeridianType(unittest.TestCase):
    """测试经络类型枚举"""

    def test_all_meridian_types_exist(self):
        types = list(MeridianType)
        self.assertEqual(len(types), 20)

    def test_twelve_regular_meridians(self):
        regular = MeridianType.get_twelve_regular()
        self.assertEqual(len(regular), 12)

    def test_eight_extraordinary_meridians(self):
        extraordinary = MeridianType.get_eight_extraordinary()
        self.assertEqual(len(extraordinary), 8)

    def test_hand_three_yin(self):
        hand_yin = MeridianType.get_hand_three_yin()
        self.assertEqual(len(hand_yin), 3)
        self.assertIn(MeridianType.HAND_TAIYIN_LUNG, hand_yin)
        self.assertIn(MeridianType.HAND_JUEYIN_PERICARDIUM, hand_yin)
        self.assertIn(MeridianType.HAND_SHAOYIN_HEART, hand_yin)

    def test_hand_three_yang(self):
        hand_yang = MeridianType.get_hand_three_yang()
        self.assertEqual(len(hand_yang), 3)
        self.assertIn(MeridianType.HAND_YANGMING_LARGE_INTESTINE, hand_yang)
        self.assertIn(MeridianType.HAND_SHAOYANG_TRIPLE_BURNER, hand_yang)
        self.assertIn(MeridianType.HAND_TAIYANG_SMALL_INTESTINE, hand_yang)

    def test_foot_three_yin(self):
        foot_yin = MeridianType.get_foot_three_yin()
        self.assertEqual(len(foot_yin), 3)
        self.assertIn(MeridianType.FOOT_TAIYIN_SPLEEN, foot_yin)
        self.assertIn(MeridianType.FOOT_JUEYIN_LIVER, foot_yin)
        self.assertIn(MeridianType.FOOT_SHAOYIN_KIDNEY, foot_yin)

    def test_foot_three_yang(self):
        foot_yang = MeridianType.get_foot_three_yang()
        self.assertEqual(len(foot_yang), 3)
        self.assertIn(MeridianType.FOOT_YANGMING_STOMACH, foot_yang)
        self.assertIn(MeridianType.FOOT_SHAOYANG_GALLBLADDER, foot_yang)
        self.assertIn(MeridianType.FOOT_TAIYANG_BLADDER, foot_yang)

    def test_yin_yang_classification(self):
        yin_meridians = [
            MeridianType.HAND_TAIYIN_LUNG,
            MeridianType.HAND_JUEYIN_PERICARDIUM,
            MeridianType.HAND_SHAOYIN_HEART,
            MeridianType.FOOT_TAIYIN_SPLEEN,
            MeridianType.FOOT_JUEYIN_LIVER,
            MeridianType.FOOT_SHAOYIN_KIDNEY,
            MeridianType.REN_MAI,
            MeridianType.YIN_QIAO_MAI,
            MeridianType.YIN_WEI_MAI,
        ]

        for m in yin_meridians:
            self.assertTrue(m.is_yin())
            self.assertFalse(m.is_yang())

        yang_meridians = [
            MeridianType.HAND_YANGMING_LARGE_INTESTINE,
            MeridianType.HAND_SHAOYANG_TRIPLE_BURNER,
            MeridianType.HAND_TAIYANG_SMALL_INTESTINE,
            MeridianType.FOOT_YANGMING_STOMACH,
            MeridianType.FOOT_SHAOYANG_GALLBLADDER,
            MeridianType.FOOT_TAIYANG_BLADDER,
            MeridianType.DU_MAI,
            MeridianType.YANG_QIAO_MAI,
            MeridianType.YANG_WEI_MAI,
        ]

        for m in yang_meridians:
            self.assertTrue(m.is_yang())
            self.assertFalse(m.is_yin())

    def test_regular_extraordinary_classification(self):
        for m in MeridianType.get_twelve_regular():
            self.assertTrue(m.is_regular())
            self.assertFalse(m.is_extraordinary())

        for m in MeridianType.get_eight_extraordinary():
            self.assertTrue(m.is_extraordinary())
            self.assertFalse(m.is_regular())

    def test_meridian_values(self):
        self.assertEqual(MeridianType.HAND_TAIYIN_LUNG.value, "手太阴肺经")
        self.assertEqual(MeridianType.REN_MAI.value, "任脉")
        self.assertEqual(MeridianType.DU_MAI.value, "督脉")


class TestMeridianChannel(unittest.TestCase):
    """测试经络通道数据结构"""

    def test_channel_creation(self):
        channel = MeridianChannel(
            channel_id="test_channel",
            name="测试经络",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
        )

        self.assertEqual(channel.channel_id, "test_channel")
        self.assertEqual(channel.name, "测试经络")
        self.assertEqual(channel.meridian_type, MeridianType.HAND_TAIYIN_LUNG)
        self.assertEqual(channel.flow_rate, 1.0)
        self.assertEqual(channel.blockage_level, 0.0)
        self.assertEqual(channel.energy_level, 1.0)

    def test_channel_custom_values(self):
        channel = MeridianChannel(
            channel_id="test_channel",
            name="测试经络",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
            flow_rate=0.8,
            blockage_level=0.3,
            energy_level=0.9,
        )

        self.assertEqual(channel.flow_rate, 0.8)
        self.assertEqual(channel.blockage_level, 0.3)
        self.assertEqual(channel.energy_level, 0.9)

    def test_channel_invalid_flow_rate(self):
        with self.assertRaises(ValueError):
            MeridianChannel(
                channel_id="test",
                name="测试",
                meridian_type=MeridianType.HAND_TAIYIN_LUNG,
                flow_rate=3.0,
            )

    def test_channel_invalid_blockage_level(self):
        with self.assertRaises(ValueError):
            MeridianChannel(
                channel_id="test",
                name="测试",
                meridian_type=MeridianType.HAND_TAIYIN_LUNG,
                blockage_level=1.5,
            )

    def test_patency_calculation(self):
        channel = MeridianChannel(
            channel_id="test",
            name="测试",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
            blockage_level=0.3,
        )

        self.assertEqual(channel.patency, 0.7)

    def test_effective_flow_rate(self):
        channel = MeridianChannel(
            channel_id="test",
            name="测试",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
            flow_rate=1.0,
            blockage_level=0.2,
        )

        self.assertEqual(channel.effective_flow_rate, 0.8)

    def test_update_flow_rate(self):
        channel = MeridianChannel(
            channel_id="test",
            name="测试",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
            flow_rate=0.5,
        )

        new_rate = channel.update_flow_rate(0.3)
        self.assertEqual(new_rate, 0.8)

    def test_update_flow_rate_clamp_upper(self):
        channel = MeridianChannel(
            channel_id="test",
            name="测试",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
            flow_rate=1.8,
        )

        new_rate = channel.update_flow_rate(0.5)
        self.assertEqual(new_rate, 2.0)

    def test_update_flow_rate_clamp_lower(self):
        channel = MeridianChannel(
            channel_id="test",
            name="测试",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
            flow_rate=0.1,
        )

        new_rate = channel.update_flow_rate(-0.5)
        self.assertEqual(new_rate, 0.0)

    def test_update_blockage(self):
        channel = MeridianChannel(
            channel_id="test",
            name="测试",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
            blockage_level=0.3,
        )

        new_blockage = channel.update_blockage(0.2)
        self.assertEqual(new_blockage, 0.5)

    def test_is_blocked(self):
        blocked_channel = MeridianChannel(
            channel_id="test",
            name="测试",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
            blockage_level=0.6,
        )

        clear_channel = MeridianChannel(
            channel_id="test2",
            name="测试2",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
            blockage_level=0.3,
        )

        self.assertTrue(blocked_channel.is_blocked())
        self.assertFalse(clear_channel.is_blocked())

    def test_is_optimal(self):
        optimal_channel = MeridianChannel(
            channel_id="test",
            name="测试",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
            flow_rate=1.0,
            blockage_level=0.05,
        )

        suboptimal_channel = MeridianChannel(
            channel_id="test2",
            name="测试2",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
            flow_rate=0.7,
            blockage_level=0.2,
        )

        self.assertTrue(optimal_channel.is_optimal())
        self.assertFalse(suboptimal_channel.is_optimal())

    def test_connected_modules(self):
        channel = MeridianChannel(
            channel_id="test",
            name="测试",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
        )

        channel.add_connected_module("呼吸系统")
        channel.add_connected_module("皮肤系统")

        self.assertEqual(len(channel.connected_modules), 2)
        self.assertIn("呼吸系统", channel.connected_modules)

        channel.remove_connected_module("呼吸系统")
        self.assertNotIn("呼吸系统", channel.connected_modules)

    def test_energy_transfer(self):
        channel = MeridianChannel(
            channel_id="test",
            name="测试",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
            current_energy=50.0,
            max_capacity=100.0,
        )

        received = channel.receive_energy(30.0)
        self.assertEqual(received, 30.0)
        self.assertEqual(channel.current_energy, 80.0)

        transmitted = channel.transmit_energy(40.0)
        self.assertEqual(transmitted, 40.0)
        self.assertEqual(channel.current_energy, 40.0)

    def test_to_dict(self):
        channel = MeridianChannel(
            channel_id="test",
            name="测试经络",
            meridian_type=MeridianType.HAND_TAIYIN_LUNG,
            flow_rate=0.8,
            blockage_level=0.2,
        )

        result = channel.to_dict()

        self.assertEqual(result["channel_id"], "test")
        self.assertEqual(result["name"], "测试经络")
        self.assertEqual(result["meridian_type"], "手太阴肺经")
        self.assertEqual(result["flow_rate"], 0.8)
        self.assertEqual(result["blockage_level"], 0.2)
        self.assertEqual(result["patency"], 0.8)


class TestMeridianNetwork(unittest.TestCase):
    """测试经络网络主类"""

    def setUp(self):
        self.network = MeridianNetwork()
        self.network.initialize()

    def test_network_initialization(self):
        self.assertEqual(len(self.network.channels), 20)

    def test_initialize_returns_status(self):
        network = MeridianNetwork()
        result = network.initialize()

        self.assertEqual(result["status"], "initialized")
        self.assertEqual(result["total_channels"], 20)
        self.assertEqual(result["regular_channels"], 12)
        self.assertEqual(result["extraordinary_channels"], 8)

    def test_get_channel(self):
        channel = self.network.get_channel("meridian_hand_taiyin_lung")

        self.assertIsNotNone(channel)
        self.assertEqual(channel.name, "手太阴肺经")

    def test_get_channel_by_type(self):
        channel = self.network.get_channel_by_type(MeridianType.REN_MAI)

        self.assertIsNotNone(channel)
        self.assertEqual(channel.name, "任脉")

    def test_get_nonexistent_channel(self):
        channel = self.network.get_channel("nonexistent")

        self.assertIsNone(channel)

    def test_network_state(self):
        state = self.network.get_network_state()

        self.assertEqual(state["total_channels"], 20)
        self.assertIn("average_flow_rate", state)
        self.assertIn("average_blockage", state)
        self.assertIn("network_balance", state)


class TestEnergyFlow(unittest.TestCase):
    """测试能量流动"""

    def setUp(self):
        self.network = MeridianNetwork()
        self.network.initialize()

    def test_flow_energy_basic(self):
        source_id = "meridian_hand_taiyin_lung"
        target_id = "meridian_hand_yangming_large_intestine"

        result = self.network.flow_energy(source_id, target_id, 10.0)

        self.assertEqual(result.source_channel, source_id)
        self.assertEqual(result.target_channel, target_id)
        self.assertGreater(result.actual_transferred, 0)

    def test_flow_energy_with_blockage(self):
        source_id = "meridian_hand_taiyin_lung"
        target_id = "meridian_hand_yangming_large_intestine"

        self.network.channels[source_id].blockage_level = 0.7

        result = self.network.flow_energy(source_id, target_id, 10.0)

        self.assertTrue(result.blockage_encountered)
        self.assertLess(result.flow_rate, 1.0)

    def test_flow_energy_invalid_channels(self):
        result = self.network.flow_energy("invalid1", "invalid2", 10.0)

        self.assertEqual(result.actual_transferred, 0.0)
        self.assertTrue(result.blockage_encountered)

    def test_circulate_energy(self):
        result = self.network.circulate_energy(cycles=1)

        self.assertEqual(result["cycles"], 1)
        self.assertGreater(result["total_transferred"], 0)
        self.assertEqual(len(result["flows"]), 12)

    def test_flow_history_recording(self):
        source_id = "meridian_hand_taiyin_lung"
        target_id = "meridian_hand_yangming_large_intestine"

        self.network.flow_energy(source_id, target_id, 10.0)

        self.assertEqual(len(self.network.flow_history), 1)


class TestBlockageDetection(unittest.TestCase):
    """测试堵塞检测"""

    def setUp(self):
        self.network = MeridianNetwork()
        self.network.initialize()

    def test_detect_no_blockages(self):
        blockages = self.network.detect_blockage()

        self.assertEqual(len(blockages), 0)

    def test_detect_blockages(self):
        channel_id = "meridian_hand_taiyin_lung"
        self.network.channels[channel_id].blockage_level = 0.5

        blockages = self.network.detect_blockage()

        self.assertEqual(len(blockages), 1)
        self.assertEqual(blockages[0].channel_id, channel_id)

    def test_blockage_severity_classification(self):
        channel_id = "meridian_hand_taiyin_lung"
        self.network.channels[channel_id].blockage_level = 0.85

        blockages = self.network.detect_blockage()

        self.assertEqual(blockages[0].severity, "严重")

    def test_blockage_suggested_actions(self):
        channel_id = "meridian_hand_taiyin_lung"
        self.network.channels[channel_id].blockage_level = 0.7

        blockages = self.network.detect_blockage()

        self.assertGreater(len(blockages[0].suggested_actions), 0)

    def test_blockage_threshold(self):
        channel_id = "meridian_hand_taiyin_lung"
        self.network.channels[channel_id].blockage_level = 0.2

        blockages = self.network.detect_blockage(threshold=0.3)

        self.assertEqual(len(blockages), 0)

        blockages = self.network.detect_blockage(threshold=0.1)

        self.assertEqual(len(blockages), 1)


class TestBlockageClearing(unittest.TestCase):
    """测试疏通机制"""

    def setUp(self):
        self.network = MeridianNetwork()
        self.network.initialize()

    def test_clear_blockage_basic(self):
        channel_id = "meridian_hand_taiyin_lung"
        self.network.channels[channel_id].blockage_level = 0.5

        result = self.network.clear_blockage(channel_id, intensity=0.5)

        self.assertTrue(result["success"])
        self.assertLess(result["new_blockage_level"], result["old_blockage_level"])

    def test_clear_blockage_already_clear(self):
        channel_id = "meridian_hand_taiyin_lung"
        self.network.channels[channel_id].blockage_level = 0.0

        result = self.network.clear_blockage(channel_id)

        self.assertTrue(result["success"])
        self.assertEqual(result["blockage_level"], 0.0)

    def test_clear_blockage_invalid_channel(self):
        result = self.network.clear_blockage("invalid_channel")

        self.assertFalse(result["success"])

    def test_clear_all_blockages(self):
        self.network.channels["meridian_hand_taiyin_lung"].blockage_level = 0.4
        self.network.channels["meridian_hand_jueyin_pericardium"].blockage_level = 0.3

        result = self.network.clear_all_blockages(intensity=0.5)

        self.assertEqual(result["channels_cleared"], 2)
        self.assertGreater(result["total_clearing"], 0)

    def test_clearing_intensity_effect(self):
        channel_id = "meridian_hand_taiyin_lung"
        self.network.channels[channel_id].blockage_level = 0.6

        result_low = self.network.clear_blockage(channel_id, intensity=0.2)

        self.network.channels[channel_id].blockage_level = 0.6
        result_high = self.network.clear_blockage(channel_id, intensity=0.8)

        self.assertGreater(
            result_low["old_blockage_level"] - result_low["new_blockage_level"],
            0
        )


class TestEnergyRouting(unittest.TestCase):
    """测试能量路由"""

    def setUp(self):
        self.network = MeridianNetwork()
        self.network.initialize()

    def test_route_energy_direct(self):
        source_id = "meridian_hand_taiyin_lung"
        target_id = "meridian_hand_yangming_large_intestine"

        result = self.network.route_energy(source_id, target_id, 10.0)

        self.assertTrue(result["success"])
        self.assertEqual(result["route_type"], "direct")

    def test_route_energy_alternative_path(self):
        source_id = "meridian_hand_taiyin_lung"
        target_id = "meridian_foot_jueyin_liver"

        result = self.network.route_energy(source_id, target_id, 10.0, avoid_blocked=False)

        self.assertTrue(result["success"])

    def test_route_energy_avoid_blocked(self):
        source_id = "meridian_hand_taiyin_lung"
        target_id = "meridian_hand_yangming_large_intestine"

        self.network.channels[target_id].blockage_level = 0.8

        result = self.network.route_energy(source_id, target_id, 10.0, avoid_blocked=True)

        self.assertTrue(result["success"])
        self.assertIn("route_type", result)

    def test_route_energy_invalid_channels(self):
        result = self.network.route_energy("invalid1", "invalid2", 10.0)

        self.assertFalse(result["success"])


class TestNetworkOperations(unittest.TestCase):
    """测试网络操作"""

    def setUp(self):
        self.network = MeridianNetwork()
        self.network.initialize()

    def test_inject_energy(self):
        channel_id = "meridian_hand_taiyin_lung"

        result = self.network.inject_energy(channel_id, 30.0)

        self.assertTrue(result["success"])
        self.assertEqual(result["injected"], 30.0)

    def test_balance_energy(self):
        for i, channel in enumerate(self.network.channels.values()):
            channel.current_energy = 20.0 + i * 10

        result = self.network.balance_energy()

        self.assertIn("average_energy", result)
        self.assertIn("adjustments", result)

    def test_get_module_connections(self):
        connections = self.network.get_module_connections("呼吸系统")

        self.assertGreater(len(connections), 0)

    def test_get_meridian_flow_sequence(self):
        sequence = self.network.get_meridian_flow_sequence()

        self.assertEqual(len(sequence), 12)
        self.assertEqual(sequence[0]["name"], "手太阴肺经")

    def test_diagnose(self):
        diagnosis = self.network.diagnose()

        self.assertIn("overall_health", diagnosis)
        self.assertIn("average_flow_rate", diagnosis)
        self.assertIn("recommendations", diagnosis)

    def test_diagnose_with_blockages(self):
        self.network.channels["meridian_hand_taiyin_lung"].blockage_level = 0.85
        self.network.channels["meridian_hand_jueyin_pericardium"].blockage_level = 0.4

        diagnosis = self.network.diagnose()

        self.assertIn("手太阴肺经", diagnosis["critical_channels"])
        self.assertIn("手厥阴心包经", diagnosis["warning_channels"])

    def test_reset(self):
        channel = self.network.channels["meridian_hand_taiyin_lung"]
        channel.flow_rate = 0.5
        channel.blockage_level = 0.5
        channel.current_energy = 20.0

        self.network.reset()

        self.assertEqual(channel.flow_rate, 1.0)
        self.assertEqual(channel.blockage_level, 0.0)
        self.assertEqual(channel.current_energy, 50.0)


class TestMeridianConnections(unittest.TestCase):
    """测试经络连接关系"""

    def setUp(self):
        self.network = MeridianNetwork()
        self.network.initialize()

    def test_yin_yang_pairs_connected(self):
        lung_id = "meridian_hand_taiyin_lung"
        large_intestine_id = "meridian_hand_yangming_large_intestine"

        lung = self.network.channels[lung_id]
        large_intestine = self.network.channels[large_intestine_id]

        self.assertIn(large_intestine_id, lung.connected_channels)
        self.assertIn(lung_id, large_intestine.connected_channels)

    def test_ren_mai_connects_yin_meridians(self):
        ren_mai = self.network.channels["meridian_ren_mai"]

        yin_meridians = MeridianType.get_hand_three_yin() + MeridianType.get_foot_three_yin()

        for meridian_type in yin_meridians:
            channel_id = self.network.type_to_channel[meridian_type]
            self.assertIn(channel_id, ren_mai.connected_channels)

    def test_du_mai_connects_yang_meridians(self):
        du_mai = self.network.channels["meridian_du_mai"]

        yang_meridians = MeridianType.get_hand_three_yang() + MeridianType.get_foot_three_yang()

        for meridian_type in yang_meridians:
            channel_id = self.network.type_to_channel[meridian_type]
            self.assertIn(channel_id, du_mai.connected_channels)

    def test_flow_sequence_connections(self):
        sequence = MeridianNetwork.TWELVE_REGULAR_FLOW_ORDER

        for i in range(len(sequence)):
            current_type = sequence[i]
            next_type = sequence[(i + 1) % len(sequence)]

            current_id = self.network.type_to_channel[current_type]
            next_id = self.network.type_to_channel[next_type]

            current = self.network.channels[current_id]

            self.assertIn(next_id, current.connected_channels,
                f"{current.name} should connect to {self.network.channels[next_id].name}")


class TestFactoryFunction(unittest.TestCase):
    """测试工厂函数"""

    def test_create_meridian_network(self):
        network = create_meridian_network()

        self.assertIsInstance(network, MeridianNetwork)
        self.assertEqual(len(network.channels), 20)
        self.assertTrue(network._initialized)


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def setUp(self):
        self.network = create_meridian_network()

    def test_full_flow_cycle(self):
        result = self.network.circulate_energy(cycles=1)

        self.assertEqual(len(result["flows"]), 12)

        for flow in result["flows"]:
            self.assertIn("from", flow)
            self.assertIn("to", flow)
            self.assertIn("transferred", flow)

    def test_blockage_and_clear_workflow(self):
        channel_id = "meridian_hand_taiyin_lung"
        self.network.channels[channel_id].blockage_level = 0.7

        blockages = self.network.detect_blockage()
        self.assertEqual(len(blockages), 1)

        clear_result = self.network.clear_blockage(channel_id, intensity=0.8)
        self.assertTrue(clear_result["success"])

        blockages_after = self.network.detect_blockage(threshold=0.3)
        self.assertLessEqual(len(blockages_after), len(blockages))

    def test_energy_routing_with_blockages(self):
        self.network.channels["meridian_hand_yangming_large_intestine"].blockage_level = 0.8

        source_id = "meridian_hand_taiyin_lung"
        target_id = "meridian_hand_yangming_large_intestine"

        result = self.network.route_energy(source_id, target_id, 10.0, avoid_blocked=True)

        self.assertTrue(result["success"])
        self.assertEqual(result["route_type"], "alternative")

    def test_network_balance_improvement(self):
        for i, channel in enumerate(self.network.channels.values()):
            channel.current_energy = 10.0 + i * 8

        initial_balance = self.network._calculate_network_balance()

        self.network.balance_energy()

        final_balance = self.network._calculate_network_balance()

        self.assertGreaterEqual(final_balance, initial_balance)

    def test_diagnosis_with_recommendations(self):
        self.network.channels["meridian_hand_taiyin_lung"].blockage_level = 0.7
        self.network.channels["meridian_foot_jueyin_liver"].blockage_level = 0.5

        diagnosis = self.network.diagnose()

        self.assertGreater(len(diagnosis["recommendations"]), 0)
        self.assertIn("critical_channels", diagnosis)
        self.assertIn("warning_channels", diagnosis)


if __name__ == '__main__':
    unittest.main(verbosity=2)
