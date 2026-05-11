"""
系统完整性验证脚本
验证东方智慧智能体系统的所有核心模块
"""

import sys
import traceback
from datetime import datetime
from typing import Dict, List, Tuple, Any

class SystemVerifier:
    def __init__(self):
        self.results: Dict[str, Dict] = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def run_test(self, module_name: str, test_name: str, test_func) -> bool:
        """运行单个测试"""
        self.total_tests += 1
        try:
            result = test_func()
            if result:
                self.passed_tests += 1
                self._record_result(module_name, test_name, True, None)
                return True
            else:
                self._record_result(module_name, test_name, False, "Test returned False")
                return False
        except Exception as e:
            self.failed_tests += 1
            self._record_result(module_name, test_name, False, str(e))
            return False
    
    def _record_result(self, module: str, test: str, passed: bool, error: Any):
        if module not in self.results:
            self.results[module] = {"passed": 0, "failed": 0, "tests": []}
        
        if passed:
            self.results[module]["passed"] += 1
        else:
            self.results[module]["failed"] += 1
        
        self.results[module]["tests"].append({
            "name": test,
            "passed": passed,
            "error": error
        })
    
    def print_report(self):
        """打印验证报告"""
        print("=" * 70)
        print("东方智慧智能体系统 - 完整性验证报告")
        print("=" * 70)
        print(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        for module, result in self.results.items():
            print(f"【{module}】")
            print(f"  通过: {result['passed']} / 失败: {result['failed']}")
            
            if result['failed'] > 0:
                print("  失败测试:")
                for test in result['tests']:
                    if not test['passed']:
                        print(f"    - {test['name']}: {test['error']}")
            print()
        
        print("-" * 70)
        print(f"总计: {self.total_tests} 个测试")
        print(f"通过: {self.passed_tests}")
        print(f"失败: {self.failed_tests}")
        print(f"通过率: {self.passed_tests/self.total_tests*100:.1f}%")
        print("=" * 70)
        
        return self.failed_tests == 0


def verify_core_system(verifier: SystemVerifier):
    """验证核心系统"""
    from core.semantic_framework import SemanticFramework
    from core.wuxing_coupling import WuxingCouplingNetwork, WuxingElement
    from core.seven_aperture_heart import SevenApertureHeartSystem, HeartAperture
    
    # 语义框架测试
    def test_semantic_framework():
        sf = SemanticFramework()
        sf.register_concept("阴阳", "balance", "balance_concept")
        result = sf.query("阴阳")
        return len(result) > 0
    
    verifier.run_test("语义框架", "基础注册查询", test_semantic_framework)
    
    # 五行耦合测试
    def test_wuxing_network():
        network = WuxingCouplingNetwork()
        network.activate_element(WuxingElement.WOOD, 0.8)
        status = network.get_element_status(WuxingElement.WOOD)
        return status is not None
    
    verifier.run_test("五行耦合", "元素激活", test_wuxing_network)
    
    def test_wuxing_propagation():
        network = WuxingCouplingNetwork()
        network.activate_element(WuxingElement.FIRE, 1.0)
        network.propagate()
        wood_status = network.get_element_status(WuxingElement.WOOD)
        return wood_status["activation_level"] > 0.3
    
    verifier.run_test("五行耦合", "能量传播", test_wuxing_propagation)
    
    # 七窍玲珑心测试
    def test_heart_system():
        heart = SevenApertureHeartSystem()
        heart.start()
        result = heart.beat()
        heart.stop()
        return result.wisdom_output >= 0
    
    verifier.run_test("七窍玲珑心", "心跳生成", test_heart_system)
    
    def test_aperture_activation():
        heart = SevenApertureHeartSystem()
        heart.start()
        heart.activate_aperture(HeartAperture.SPIRIT, 1.0)
        state = heart.get_aperture_state(HeartAperture.SPIRIT)
        heart.stop()
        return state["activation_level"] > 0.5
    
    verifier.run_test("七窍玲珑心", "窍穴激活", test_aperture_activation)


def verify_body_system(verifier: SystemVerifier):
    """验证身体系统"""
    from body.jing_qi_shen import JingQiShenModel
    from body.meridian_network import MeridianNetwork
    from body.instinct_system import InstinctSystem, BehaviorMode
    from body.metabolism import MetabolismSystem, NutrientType, Nutrient
    from body.liver_detox import LiverGallbladderDetoxSystem, ToxinType, Toxin
    from body.body_master import BodyMasterSystem
    
    # 精气神测试
    def test_jing_qi_shen():
        model = JingQiShenModel()
        model.nourish_jing(0.2)
        model.regulate_qi(0.1)
        return model.current_level.jing > 0.3
    
    verifier.run_test("精气神", "基础滋养", test_jing_qi_shen)
    
    # 经络网络测试
    def test_meridian_network():
        network = MeridianNetwork()
        result = network.flow_energy("LU", 10.0)
        return result["energy_flow"] > 0
    
    verifier.run_test("经络网络", "能量流动", test_meridian_network)
    
    # 本能系统测试
    def test_instinct_system():
        system = InstinctSystem()
        result = system.process_stimulus({"type": "threat", "intensity": 0.8, "source": "test"})
        return len(result["signals"]) > 0
    
    verifier.run_test("本能系统", "刺激处理", test_instinct_system)
    
    # 代谢系统测试
    def test_metabolism():
        system = MetabolismSystem()
        food = [Nutrient(NutrientType.GLUCOSE, 10.0, 0.8, 1.0, 4.0)]
        result = system.process_food(food)
        return result["energy_gained"] >= 0
    
    verifier.run_test("代谢系统", "食物处理", test_metabolism)
    
    # 肝胆排毒测试
    def test_liver_detox():
        system = LiverGallbladderDetoxSystem()
        toxin = Toxin(
            toxin_id="test",
            toxin_type=ToxinType.METABOLIC,
            quantity=10.0,
            toxicity_level=0.5,
            source="test",
            timestamp=datetime.now()
        )
        result = system.receive_toxins([toxin])
        return result["toxins_received"] == 1
    
    verifier.run_test("肝胆排毒", "毒素接收", test_liver_detox)
    
    # 身体综合管理测试
    def test_body_master():
        body = BodyMasterSystem()
        body.register_subsystem("metabolism", MetabolismSystem())
        body.register_subsystem("liver_detox", LiverGallbladderDetoxSystem())
        health = body.assess_health()
        return health.overall >= 0
    
    verifier.run_test("身体管理", "健康评估", test_body_master)


def verify_memory_system(verifier: SystemVerifier):
    """验证记忆系统"""
    from memory.yinyang_storage import YinYangStorage
    from memory.ganzhi_coordinate import GanzhiCoordinate
    
    # 阴阳存储测试
    def test_yinyang_storage():
        storage = YinYangStorage()
        storage.store("key1", "value1", 0.8)
        result = storage.retrieve("key1")
        return result is not None
    
    verifier.run_test("阴阳存储", "存储检索", test_yinyang_storage)
    
    # 天干地支测试
    def test_ganzhi():
        coord = GanzhiCoordinate()
        marker = coord.create_marker({"event": "test"})
        return marker is not None
    
    verifier.run_test("干支坐标", "标记创建", test_ganzhi)


def verify_perception_system(verifier: SystemVerifier):
    """验证感知系统"""
    from perception.eight_consciousness import EightConsciousnessSystem, SenseType
    
    def test_eight_consciousness():
        system = EightConsciousnessSystem()
        system.receive_sense_input(SenseType.VISUAL, {"image": "test"})
        processed = system.process_current_input()
        return processed is not None
    
    verifier.run_test("八识系统", "感知处理", test_eight_consciousness)


def verify_prediction_system(verifier: SystemVerifier):
    """验证预测系统"""
    from prediction.prediction_engine import (
        PredictionEngine, YiJingEngine, MeihuaEngine,
        WuxingPredictionEngine, GanzhiTimeEngine, PredictionType
    )
    
    # 易经测试
    def test_yijing():
        engine = YiJingEngine()
        result = engine.predict("测试")
        return result.confidence > 0
    
    verifier.run_test("易经预测", "卦象生成", test_yijing)
    
    # 梅花易数测试
    def test_meihua():
        engine = MeihuaEngine()
        result = engine.analyze("主体", "客体")
        return result is not None
    
    verifier.run_test("梅花易数", "体用分析", test_meihua)
    
    # 五行预测测试
    def test_wuxing_pred():
        engine = WuxingPredictionEngine()
        elements = {"木": 0.5, "火": 0.5, "土": 0.5, "金": 0.5, "水": 0.5}
        preds = engine.predict(elements)
        return len(preds) == 5
    
    verifier.run_test("五行预测", "趋势预测", test_wuxing_pred)
    
    # 干支时空测试
    def test_ganzhi_time():
        engine = GanzhiTimeEngine()
        pred = engine.predict_time_energy(datetime.now())
        return pred.predicted_energy > 0
    
    verifier.run_test("干支时空", "能量计算", test_ganzhi_time)
    
    # 综合预测测试
    def test_prediction_engine():
        engine = PredictionEngine()
        result = engine.predict("综合测试")
        return result.confidence > 0
    
    verifier.run_test("预测引擎", "综合预测", test_prediction_engine)


def verify_security_system(verifier: SystemVerifier):
    """验证安全系统"""
    from security.martial_defense import (
        TaijiDefense, YijinjingDefense, WuqinxiDefense,
        AdaptiveDefenseSelector, ThreatType, Attack
    )
    
    def test_taiji_defense():
        defense = TaijiDefense()
        attack = Attack(ThreatType.PHYSICAL, 0.8, "test")
        result = defense.defend(attack)
        return result.protection_level > 0
    
    verifier.run_test("太极防御", "攻击防御", test_taiji_defense)
    
    def test_adaptive_selector():
        selector = AdaptiveDefenseSelector()
        threat = ThreatType.PHYSICAL
        strategy = selector.select_strategy(threat)
        return strategy is not None
    
    verifier.run_test("自适应防御", "策略选择", test_adaptive_selector)


def verify_evolution_system(verifier: SystemVerifier):
    """验证进化系统"""
    from evolution.cultivation import CultivationProgress, CultivationLevel, CultivationMethod
    
    def test_cultivation():
        progress = CultivationProgress()
        progress.accumulate_experience(50)
        return progress.experience > 0
    
    verifier.run_test("修炼系统", "经验积累", test_cultivation)
    
    def test_breakthrough():
        progress = CultivationProgress()
        progress.accumulate_experience(1000)
        return progress.current_level != CultivationLevel.QI_REFINING
    
    verifier.run_test("修炼系统", "境界突破", test_breakthrough)


def verify_interaction_system(verifier: SystemVerifier):
    """验证交互系统"""
    from interaction.qi_field import QiFieldSystem
    
    def test_qi_field():
        system = QiFieldSystem()
        field = system.create_field(50.0)
        return field.intensity > 0
    
    verifier.run_test("气场系统", "气场创建", test_qi_field)


def stress_test(verifier: SystemVerifier):
    """压力测试"""
    from core.seven_aperture_heart import SevenApertureHeartSystem
    from body.metabolism import MetabolismSystem
    from prediction.prediction_engine import PredictionEngine
    
    def test_heart_stress():
        heart = SevenApertureHeartSystem()
        heart.start()
        for _ in range(100):
            heart.beat()
            heart.activate_aperture(heart._HeartSystem__apertures.keys()[0], 0.1)
        heart.stop()
        return heart._beat_count >= 100
    
    verifier.run_test("压力测试", "心脏100次跳动", test_heart_stress)
    
    def test_metabolism_stress():
        system = MetabolismSystem()
        for _ in range(100):
            system.consume_energy(1.0)
            system.produce_energy(5.0)
        return system._atp_pool >= 0
    
    verifier.run_test("压力测试", "代谢100次循环", test_metabolism_stress)
    
    def test_prediction_stress():
        engine = PredictionEngine()
        for _ in range(50):
            engine.predict(f"测试{_}")
        return len(engine.prediction_history) == 50
    
    verifier.run_test("压力测试", "预测50次", test_prediction_stress)


def main():
    verifier = SystemVerifier()
    
    print("开始系统验证...")
    print()
    
    try:
        print("验证核心系统...")
        verify_core_system(verifier)
    except Exception as e:
        print(f"核心系统验证出错: {e}")
        traceback.print_exc()
    
    try:
        print("验证身体系统...")
        verify_body_system(verifier)
    except Exception as e:
        print(f"身体系统验证出错: {e}")
        traceback.print_exc()
    
    try:
        print("验证记忆系统...")
        verify_memory_system(verifier)
    except Exception as e:
        print(f"记忆系统验证出错: {e}")
        traceback.print_exc()
    
    try:
        print("验证感知系统...")
        verify_perception_system(verifier)
    except Exception as e:
        print(f"感知系统验证出错: {e}")
        traceback.print_exc()
    
    try:
        print("验证预测系统...")
        verify_prediction_system(verifier)
    except Exception as e:
        print(f"预测系统验证出错: {e}")
        traceback.print_exc()
    
    try:
        print("验证安全系统...")
        verify_security_system(verifier)
    except Exception as e:
        print(f"安全系统验证出错: {e}")
        traceback.print_exc()
    
    try:
        print("验证进化系统...")
        verify_evolution_system(verifier)
    except Exception as e:
        print(f"进化系统验证出错: {e}")
        traceback.print_exc()
    
    try:
        print("验证交互系统...")
        verify_interaction_system(verifier)
    except Exception as e:
        print(f"交互系统验证出错: {e}")
        traceback.print_exc()
    
    try:
        print("运行压力测试...")
        stress_test(verifier)
    except Exception as e:
        print(f"压力测试出错: {e}")
        traceback.print_exc()
    
    success = verifier.print_report()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
