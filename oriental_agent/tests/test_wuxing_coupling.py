"""
Unit tests for Wu Xing Coupling System
五行生克耦合系统单元测试
"""

import unittest
import sys
import os
import importlib.util

_test_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_test_dir, '..', '..'))

_wuxing_coupling_path = os.path.join(_project_root, "oriental_agent", "core", "wuxing_coupling.py")
_spec = importlib.util.spec_from_file_location("wuxing_coupling", _wuxing_coupling_path)
wuxing_coupling_module = importlib.util.module_from_spec(_spec)
sys.modules["wuxing_coupling"] = wuxing_coupling_module
_spec.loader.exec_module(wuxing_coupling_module)

WuxingElement = wuxing_coupling_module.WuxingElement
WuxingModule = wuxing_coupling_module.WuxingModule
WuxingCouplingNetwork = wuxing_coupling_module.WuxingCouplingNetwork
WuxingBalancer = wuxing_coupling_module.WuxingBalancer
create_wuxing_network = wuxing_coupling_module.create_wuxing_network
create_wuxing_balancer = wuxing_coupling_module.create_wuxing_balancer


class TestWuxingElement(unittest.TestCase):
    """测试五行元素枚举"""
    
    def test_all_elements_exist(self):
        elements = list(WuxingElement)
        self.assertEqual(len(elements), 5)
        
    def test_element_values(self):
        self.assertEqual(WuxingElement.WOOD.value, "木")
        self.assertEqual(WuxingElement.FIRE.value, "火")
        self.assertEqual(WuxingElement.EARTH.value, "土")
        self.assertEqual(WuxingElement.METAL.value, "金")
        self.assertEqual(WuxingElement.WATER.value, "水")


class TestWuxingModule(unittest.TestCase):
    """测试五行模块数据结构"""
    
    def test_module_creation(self):
        module = WuxingModule(element=WuxingElement.WOOD)
        
        self.assertEqual(module.element, WuxingElement.WOOD)
        self.assertEqual(module.activation_level, 0.5)
        self.assertEqual(module.energy_reserve, 1.0)
        self.assertEqual(module.stability, 1.0)
    
    def test_module_custom_activation(self):
        module = WuxingModule(element=WuxingElement.FIRE, activation_level=0.8)
        
        self.assertEqual(module.activation_level, 0.8)
    
    def test_module_invalid_activation(self):
        with self.assertRaises(ValueError):
            WuxingModule(element=WuxingElement.WOOD, activation_level=1.5)
        
        with self.assertRaises(ValueError):
            WuxingModule(element=WuxingElement.WOOD, activation_level=-0.1)
    
    def test_update_activation(self):
        module = WuxingModule(element=WuxingElement.WOOD, activation_level=0.5)
        
        new_level = module.update_activation(0.2)
        
        self.assertEqual(new_level, 0.7)
        self.assertEqual(module.activation_level, 0.7)
    
    def test_update_activation_clamp_upper(self):
        module = WuxingModule(element=WuxingElement.WOOD, activation_level=0.9)
        
        new_level = module.update_activation(0.5)
        
        self.assertEqual(new_level, 1.0)
    
    def test_update_activation_clamp_lower(self):
        module = WuxingModule(element=WuxingElement.WOOD, activation_level=0.2)
        
        new_level = module.update_activation(-0.5)
        
        self.assertEqual(new_level, 0.0)
    
    def test_add_connection(self):
        module = WuxingModule(element=WuxingElement.WOOD)
        
        module.add_connection(WuxingElement.FIRE, 1.0)
        
        self.assertIn(WuxingElement.FIRE, module.connected_modules)
        self.assertEqual(module.get_connection_weight(WuxingElement.FIRE), 1.0)
    
    def test_remove_connection(self):
        module = WuxingModule(element=WuxingElement.WOOD)
        module.add_connection(WuxingElement.FIRE, 1.0)
        
        result = module.remove_connection(WuxingElement.FIRE)
        
        self.assertTrue(result)
        self.assertNotIn(WuxingElement.FIRE, module.connected_modules)
    
    def test_remove_nonexistent_connection(self):
        module = WuxingModule(element=WuxingElement.WOOD)
        
        result = module.remove_connection(WuxingElement.FIRE)
        
        self.assertFalse(result)
    
    def test_to_dict(self):
        module = WuxingModule(
            element=WuxingElement.WOOD,
            activation_level=0.7,
            energy_reserve=0.9,
            stability=0.8
        )
        module.add_connection(WuxingElement.FIRE, 1.0)
        
        result = module.to_dict()
        
        self.assertEqual(result["element"], "木")
        self.assertEqual(result["activation_level"], 0.7)
        self.assertEqual(result["energy_reserve"], 0.9)
        self.assertEqual(result["stability"], 0.8)
        self.assertIn("火", result["connected_modules"])


class TestWuxingCouplingNetwork(unittest.TestCase):
    """测试五行耦合网络"""
    
    def setUp(self):
        self.network = WuxingCouplingNetwork()
    
    def test_network_initialization(self):
        self.assertEqual(len(self.network.modules), 5)
        
        for element in WuxingElement:
            self.assertIn(element, self.network.modules)
    
    def test_generation_cycle_definition(self):
        self.assertEqual(
            WuxingCouplingNetwork.GENERATION_CYCLE[WuxingElement.WOOD],
            WuxingElement.FIRE
        )
        self.assertEqual(
            WuxingCouplingNetwork.GENERATION_CYCLE[WuxingElement.FIRE],
            WuxingElement.EARTH
        )
        self.assertEqual(
            WuxingCouplingNetwork.GENERATION_CYCLE[WuxingElement.EARTH],
            WuxingElement.METAL
        )
        self.assertEqual(
            WuxingCouplingNetwork.GENERATION_CYCLE[WuxingElement.METAL],
            WuxingElement.WATER
        )
        self.assertEqual(
            WuxingCouplingNetwork.GENERATION_CYCLE[WuxingElement.WATER],
            WuxingElement.WOOD
        )
    
    def test_restriction_cycle_definition(self):
        self.assertEqual(
            WuxingCouplingNetwork.RESTRICTION_CYCLE[WuxingElement.WOOD],
            WuxingElement.EARTH
        )
        self.assertEqual(
            WuxingCouplingNetwork.RESTRICTION_CYCLE[WuxingElement.EARTH],
            WuxingElement.WATER
        )
        self.assertEqual(
            WuxingCouplingNetwork.RESTRICTION_CYCLE[WuxingElement.WATER],
            WuxingElement.FIRE
        )
        self.assertEqual(
            WuxingCouplingNetwork.RESTRICTION_CYCLE[WuxingElement.FIRE],
            WuxingElement.METAL
        )
        self.assertEqual(
            WuxingCouplingNetwork.RESTRICTION_CYCLE[WuxingElement.METAL],
            WuxingElement.WOOD
        )
    
    def test_get_module(self):
        module = self.network.get_module(WuxingElement.WOOD)
        
        self.assertIsNotNone(module)
        self.assertEqual(module.element, WuxingElement.WOOD)
    
    def test_get_nonexistent_module(self):
        module = self.network.get_module("invalid")
        
        self.assertIsNone(module)
    
    def test_add_module_rejects_duplicate(self):
        new_module = WuxingModule(element=WuxingElement.WOOD)
        
        result = self.network.add_module(new_module)
        
        self.assertFalse(result)
    
    def test_network_state(self):
        state = self.network.get_network_state()
        
        self.assertEqual(len(state), 5)
        for element in WuxingElement:
            self.assertIn(element.value, state)
    
    def test_reset(self):
        self.network.modules[WuxingElement.WOOD].activation_level = 0.9
        
        self.network.reset()
        
        for module in self.network.modules.values():
            self.assertEqual(module.activation_level, 0.5)


class TestGenerationPropagation(unittest.TestCase):
    """测试相生传播"""
    
    def setUp(self):
        self.network = WuxingCouplingNetwork()
    
    def test_propagate_generation_increases_target(self):
        wood_module = self.network.modules[WuxingElement.WOOD]
        fire_module = self.network.modules[WuxingElement.FIRE]
        
        initial_fire = fire_module.activation_level
        
        self.network.propagate_generation(WuxingElement.WOOD, 0.3)
        
        self.assertGreater(fire_module.activation_level, initial_fire)
    
    def test_generation_chain_propagation(self):
        self.network.reset()
        
        results = self.network.propagate_generation(WuxingElement.WOOD, 0.4)
        
        self.assertIn("木→火", results)
        self.assertIn("火→土", results)
        self.assertIn("土→金", results)
        self.assertIn("金→水", results)
    
    def test_generation_gain_values(self):
        self.network.reset()
        
        results = self.network.propagate_generation(WuxingElement.WOOD, 0.3)
        
        first_gain = results["木→火"]["gain"]
        self.assertGreater(first_gain, 0)
        
        for key, value in results.items():
            self.assertIn("gain", value)
            self.assertIn("old_level", value)
            self.assertIn("new_level", value)
    
    def test_generation_nonlinear_decay(self):
        self.network.reset()
        
        results = self.network.propagate_generation(WuxingElement.WOOD, 0.5)
        
        gains = [v["gain"] for v in results.values()]
        
        for i in range(1, len(gains)):
            self.assertLess(gains[i], gains[i-1])
    
    def test_generation_cycle_completeness(self):
        chain = self.network.get_generation_chain(WuxingElement.WOOD)
        
        self.assertEqual(len(chain), 5)
        self.assertEqual(chain[0], WuxingElement.WOOD)
        self.assertEqual(chain[1], WuxingElement.FIRE)
        self.assertEqual(chain[2], WuxingElement.EARTH)
        self.assertEqual(chain[3], WuxingElement.METAL)
        self.assertEqual(chain[4], WuxingElement.WATER)
    
    def test_activate_triggers_generation(self):
        self.network.reset()
        
        initial_fire = self.network.modules[WuxingElement.FIRE].activation_level
        
        result = self.network.activate(WuxingElement.WOOD, 0.3)
        
        self.assertIn("propagated", result)
        self.assertIn("generation", result["propagated"])
        
        final_fire = self.network.modules[WuxingElement.FIRE].activation_level
        self.assertGreater(final_fire, initial_fire)


class TestRestrictionPropagation(unittest.TestCase):
    """测试相克传播"""
    
    def setUp(self):
        self.network = WuxingCouplingNetwork()
    
    def test_propagate_restriction_decreases_target(self):
        earth_module = self.network.modules[WuxingElement.EARTH]
        
        initial_earth = earth_module.activation_level
        
        self.network.propagate_restriction(WuxingElement.WOOD, 0.3)
        
        self.assertLess(earth_module.activation_level, initial_earth)
    
    def test_restriction_chain_propagation(self):
        self.network.reset()
        
        results = self.network.propagate_restriction(WuxingElement.WOOD, 0.4)
        
        self.assertIn("木⊃土", results)
        self.assertIn("土⊃水", results)
        self.assertIn("水⊃火", results)
        self.assertIn("火⊃金", results)
    
    def test_restriction_suppression_values(self):
        self.network.reset()
        
        results = self.network.propagate_restriction(WuxingElement.WOOD, 0.3)
        
        first_suppression = results["木⊃土"]["suppression"]
        self.assertGreater(first_suppression, 0)
        
        for key, value in results.items():
            self.assertIn("suppression", value)
            self.assertIn("old_level", value)
            self.assertIn("new_level", value)
    
    def test_restriction_nonlinear_decay(self):
        self.network.reset()
        
        results = self.network.propagate_restriction(WuxingElement.WOOD, 0.5)
        
        suppressions = [v["suppression"] for v in results.values()]
        
        for i in range(1, len(suppressions)):
            self.assertLess(suppressions[i], suppressions[i-1])
    
    def test_restriction_cycle_completeness(self):
        chain = self.network.get_restriction_chain(WuxingElement.WOOD)
        
        self.assertEqual(len(chain), 5)
        self.assertEqual(chain[0], WuxingElement.WOOD)
        self.assertEqual(chain[1], WuxingElement.EARTH)
        self.assertEqual(chain[2], WuxingElement.WATER)
        self.assertEqual(chain[3], WuxingElement.FIRE)
        self.assertEqual(chain[4], WuxingElement.METAL)
    
    def test_activate_triggers_restriction(self):
        self.network.reset()
        
        initial_earth = self.network.modules[WuxingElement.EARTH].activation_level
        
        result = self.network.activate(WuxingElement.WOOD, 0.3)
        
        self.assertIn("propagated", result)
        self.assertIn("restriction", result["propagated"])
        
        final_earth = self.network.modules[WuxingElement.EARTH].activation_level
        self.assertLess(final_earth, initial_earth)


class TestDynamicBalance(unittest.TestCase):
    """测试动态平衡调节"""
    
    def setUp(self):
        self.network = WuxingCouplingNetwork()
        self.balancer = WuxingBalancer(self.network)
    
    def test_monitor_balanced_state(self):
        self.network.reset()
        
        status = self.balancer.monitor()
        
        for element, state in status.items():
            self.assertEqual(state, "balanced")
    
    def test_monitor_overstrong_detection(self):
        self.network.modules[WuxingElement.WOOD].activation_level = 0.85
        
        status = self.balancer.monitor()
        
        self.assertEqual(status[WuxingElement.WOOD], "overstrong")
    
    def test_monitor_overweak_detection(self):
        self.network.modules[WuxingElement.WOOD].activation_level = 0.25
        
        status = self.balancer.monitor()
        
        self.assertEqual(status[WuxingElement.WOOD], "overweak")
    
    def test_find_restrictor(self):
        restrictor = self.balancer._find_restrictor(WuxingElement.EARTH)
        
        self.assertEqual(restrictor, WuxingElement.WOOD)
        
        restrictor = self.balancer._find_restrictor(WuxingElement.WOOD)
        self.assertEqual(restrictor, WuxingElement.METAL)
    
    def test_find_generator(self):
        generator = self.balancer._find_generator(WuxingElement.FIRE)
        
        self.assertEqual(generator, WuxingElement.WOOD)
        
        generator = self.balancer._find_generator(WuxingElement.WOOD)
        self.assertEqual(generator, WuxingElement.WATER)
    
    def test_trigger_restriction_reduces_overstrong(self):
        self.network.modules[WuxingElement.EARTH].activation_level = 0.85
        
        initial_level = self.network.modules[WuxingElement.EARTH].activation_level
        
        result = self.balancer.trigger_restriction(WuxingElement.EARTH)
        
        self.assertEqual(result["action"], "trigger_restriction")
        self.assertEqual(result["element"], "土")
        self.assertEqual(result["restrictor"], "木")
        
        final_level = self.network.modules[WuxingElement.EARTH].activation_level
        self.assertLess(final_level, initial_level)
    
    def test_trigger_generation_increases_overweak(self):
        self.network.modules[WuxingElement.FIRE].activation_level = 0.25
        
        initial_level = self.network.modules[WuxingElement.FIRE].activation_level
        
        result = self.balancer.trigger_generation(WuxingElement.FIRE)
        
        self.assertEqual(result["action"], "trigger_generation")
        self.assertEqual(result["element"], "火")
        self.assertEqual(result["generator"], "木")
        
        final_level = self.network.modules[WuxingElement.FIRE].activation_level
        self.assertGreater(final_level, initial_level)
    
    def test_balance_overall(self):
        self.network.modules[WuxingElement.WOOD].activation_level = 0.85
        self.network.modules[WuxingElement.FIRE].activation_level = 0.25
        
        result = self.balancer.balance()
        
        self.assertIn("initial_state", result)
        self.assertIn("final_state", result)
        self.assertIn("balance_score", result)
        self.assertIn("adjustments", result)
    
    def test_balance_improves_score(self):
        self.network.modules[WuxingElement.WOOD].activation_level = 0.9
        self.network.modules[WuxingElement.FIRE].activation_level = 0.2
        self.network.modules[WuxingElement.EARTH].activation_level = 0.8
        
        initial_score = self.network.get_balance_score()
        
        self.balancer.balance()
        
        final_score = self.network.get_balance_score()
        self.assertGreater(final_score, initial_score)
    
    def test_suggest_adjustments(self):
        self.network.modules[WuxingElement.WOOD].activation_level = 0.85
        self.network.modules[WuxingElement.FIRE].activation_level = 0.25
        
        suggestions = self.balancer.suggest_adjustments()
        
        self.assertGreater(len(suggestions), 0)
        
        for suggestion in suggestions:
            self.assertIn("element", suggestion)
            self.assertIn("action", suggestion)
            self.assertIn("source", suggestion)
            self.assertIn("reason", suggestion)
    
    def test_balance_history_recording(self):
        self.network.modules[WuxingElement.WOOD].activation_level = 0.85
        
        self.balancer.balance()
        
        self.assertEqual(len(self.balancer.balance_history), 1)
    
    def test_adjustment_log_recording(self):
        self.network.modules[WuxingElement.WOOD].activation_level = 0.85
        
        self.balancer.trigger_restriction(WuxingElement.WOOD)
        
        self.assertEqual(len(self.balancer.adjustment_log), 1)


class TestNetworkBalanceScore(unittest.TestCase):
    """测试网络平衡分数计算"""
    
    def setUp(self):
        self.network = WuxingCouplingNetwork()
    
    def test_perfect_balance_score(self):
        self.network.reset()
        
        score = self.network.get_balance_score()
        
        self.assertEqual(score, 1.0)
    
    def test_imbalanced_score(self):
        self.network.modules[WuxingElement.WOOD].activation_level = 0.9
        self.network.modules[WuxingElement.FIRE].activation_level = 0.1
        
        score = self.network.get_balance_score()
        
        self.assertLess(score, 1.0)
    
    def test_highly_imbalanced_score(self):
        self.network.modules[WuxingElement.WOOD].activation_level = 1.0
        self.network.modules[WuxingElement.FIRE].activation_level = 0.0
        self.network.modules[WuxingElement.EARTH].activation_level = 1.0
        self.network.modules[WuxingElement.METAL].activation_level = 0.0
        self.network.modules[WuxingElement.WATER].activation_level = 1.0
        
        score = self.network.get_balance_score()
        
        self.assertLess(score, 0.5)


class TestFactoryFunctions(unittest.TestCase):
    """测试工厂函数"""
    
    def test_create_wuxing_network(self):
        network = create_wuxing_network()
        
        self.assertIsInstance(network, WuxingCouplingNetwork)
        self.assertEqual(len(network.modules), 5)
    
    def test_create_wuxing_network_custom_nonlinearity(self):
        network = create_wuxing_network(nonlinearity_factor=2.0)
        
        self.assertEqual(network.nonlinearity_factor, 2.0)
    
    def test_create_wuxing_balancer(self):
        network = create_wuxing_network()
        balancer = create_wuxing_balancer(network)
        
        self.assertIsInstance(balancer, WuxingBalancer)
        self.assertIs(balancer.network, network)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_cycle_propagation(self):
        network = WuxingCouplingNetwork()
        network.reset()
        
        network.activate(WuxingElement.WOOD, 0.4)
        
        wood_level = network.modules[WuxingElement.WOOD].activation_level
        fire_level = network.modules[WuxingElement.FIRE].activation_level
        earth_level = network.modules[WuxingElement.EARTH].activation_level
        
        self.assertGreater(wood_level, 0.5)
        self.assertGreater(fire_level, 0.5)
        self.assertLess(earth_level, 0.5)
    
    def test_multiple_activations(self):
        network = WuxingCouplingNetwork()
        network.reset()
        
        network.activate(WuxingElement.WOOD, 0.3)
        network.activate(WuxingElement.METAL, 0.3)
        
        balance_score = network.get_balance_score()
        
        self.assertGreater(balance_score, 0.5)
    
    def test_automatic_balancing(self):
        network = WuxingCouplingNetwork()
        
        network.modules[WuxingElement.WOOD].activation_level = 0.9
        network.modules[WuxingElement.FIRE].activation_level = 0.2
        network.modules[WuxingElement.EARTH].activation_level = 0.8
        network.modules[WuxingElement.METAL].activation_level = 0.3
        network.modules[WuxingElement.WATER].activation_level = 0.6
        
        initial_score = network.get_balance_score()
        
        result = network.balance()
        
        final_score = result["balance_score"]
        self.assertGreater(final_score, initial_score)
    
    def test_propagation_history(self):
        network = WuxingCouplingNetwork()
        network.reset()
        
        network.activate(WuxingElement.WOOD, 0.3)
        network.activate(WuxingElement.FIRE, 0.2)
        
        self.assertEqual(len(network.propagation_history), 2)
    
    def test_nonlinear_coupling_effect(self):
        network_low = WuxingCouplingNetwork(nonlinearity_factor=1.0)
        network_high = WuxingCouplingNetwork(nonlinearity_factor=2.0)
        
        network_low.reset()
        network_high.reset()
        
        network_low.propagate_generation(WuxingElement.WOOD, 0.5)
        network_high.propagate_generation(WuxingElement.WOOD, 0.5)
        
        fire_low = network_low.modules[WuxingElement.FIRE].activation_level
        fire_high = network_high.modules[WuxingElement.FIRE].activation_level
        
        self.assertNotEqual(fire_low, fire_high)


if __name__ == '__main__':
    unittest.main(verbosity=2)
