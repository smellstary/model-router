"""
系统完整性验证脚本 v2 - 使用直接执行方式避免导入链问题
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
            self._record_result(module_name, test_name, False, str(e)[:100])
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
        print("=" * 70)
        print("东方智慧智能体系统 - 完整性验证报告 v2")
        print("=" * 70)
        print(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        for module, result in self.results.items():
            status = "✅" if result['failed'] == 0 else "❌"
            print(f"{status}【{module}】 通过: {result['passed']} / 失败: {result['failed']}")
            
            if result['failed'] > 0:
                for test in result['tests']:
                    if not test['passed']:
                        print(f"   - {test['name']}: {test['error']}")
        print()
        print("-" * 70)
        print(f"总计: {self.total_tests} 个测试")
        print(f"通过: {self.passed_tests}  失败: {self.failed_tests}")
        print(f"通过率: {self.passed_tests/self.total_tests*100:.1f}%")
        print("=" * 70)
        
        return self.failed_tests == 0


def verify_seven_aperture_heart(verifier: SystemVerifier):
    """验证七窍玲珑心系统"""
    sys.path.insert(0, '/workspace/oriental_agent')
    exec(open('/workspace/oriental_agent/core/seven_aperture_heart.py').read())
    
    def test_create():
        heart = SevenApertureHeartSystem()
        return heart is not None
    
    def test_start():
        heart = SevenApertureHeartSystem()
        result = heart.start()
        heart.stop()
        return result is True
    
    def test_beat():
        heart = SevenApertureHeartSystem()
        heart.start()
        beat = heart.beat()
        heart.stop()
        return beat is not None and beat.wisdom_output >= 0
    
    def test_aperture():
        heart = SevenApertureHeartSystem()
        heart.start()
        heart.activate_aperture(HeartAperture.SPIRIT, 0.8)
        state = heart.get_aperture_state(HeartAperture.SPIRIT)
        heart.stop()
        return state is not None and state["activation_level"] > 0.5
    
    def test_meditate():
        heart = SevenApertureHeartSystem()
        heart.start()
        result = heart.meditate(0.3)
        heart.stop()
        return result is not None and result["success"] is True
    
    verifier.run_test("七窍玲珑心", "创建系统", test_create)
    verifier.run_test("七窍玲珑心", "启动系统", test_start)
    verifier.run_test("七窍玲珑心", "心跳生成", test_beat)
    verifier.run_test("七窍玲珑心", "窍穴激活", test_aperture)
    verifier.run_test("七窍玲珑心", "冥想提升", test_meditate)


def verify_metabolism(verifier: SystemVerifier):
    """验证代谢系统"""
    sys.path.insert(0, '/workspace/oriental_agent')
    exec(open('/workspace/oriental_agent/body/metabolism.py').read())
    
    def test_create():
        system = MetabolismSystem()
        return system is not None
    
    def test_process_food():
        system = MetabolismSystem()
        food = [
            Nutrient(NutrientType.GLUCOSE, 10.0, 0.8, 1.0, 4.0),
            Nutrient(NutrientType.FAT, 5.0, 0.9, 1.0, 9.0)
        ]
        result = system.process_food(food)
        return result is not None and "energy_gained" in result
    
    def test_produce_energy():
        system = MetabolismSystem()
        system._energy_reserve = 100.0
        result = system.produce_energy(10.0)
        return result is not None and result["success"] is True
    
    def test_consume_energy():
        system = MetabolismSystem()
        system._atp_pool = 50.0
        result = system.consume_energy(10.0)
        return result is True
    
    def test_metabolize_carb():
        system = MetabolismSystem()
        result = system.metabolize_carbohydrate(10.0)
        return result is not None and "atp_produced" in result
    
    verifier.run_test("代谢系统", "创建系统", test_create)
    verifier.run_test("代谢系统", "处理食物", test_process_food)
    verifier.run_test("代谢系统", "产生能量", test_produce_energy)
    verifier.run_test("代谢系统", "消耗能量", test_consume_energy)
    verifier.run_test("代谢系统", "糖代谢", test_metabolize_carb)


def verify_liver_detox(verifier: SystemVerifier):
    """验证肝胆排毒系统"""
    sys.path.insert(0, '/workspace/oriental_agent')
    exec(open('/workspace/oriental_agent/body/liver_detox.py').read())
    
    def test_create():
        system = LiverGallbladderDetoxSystem()
        return system is not None
    
    def test_receive_toxins():
        system = LiverGallbladderDetoxSystem()
        toxins = [
            Toxin(
                toxin_id='test',
                toxin_type=ToxinType.METABOLIC,
                quantity=10.0,
                toxicity_level=0.5,
                source='test',
                timestamp=datetime.now()
            )
        ]
        result = system.receive_toxins(toxins)
        return result is not None and result["toxins_received"] == 1
    
    def test_start_detox():
        system = LiverGallbladderDetoxSystem()
        result = system.start_detox_cycle()
        return result is not None and result["cycle_started"] is True
    
    def test_perform_detox():
        system = LiverGallbladderDetoxSystem()
        system.start_detox_cycle()
        result = system.perform_detox(1.0)
        return result is not None and "phase" in result
    
    def test_bile_production():
        gb = GallbladderSystem()
        bile = gb.produce_bile(10.0)
        return bile is not None and bile.amount == 10.0
    
    verifier.run_test("肝胆排毒", "创建系统", test_create)
    verifier.run_test("肝胆排毒", "接收毒素", test_receive_toxins)
    verifier.run_test("肝胆排毒", "启动排毒", test_start_detox)
    verifier.run_test("肝胆排毒", "执行排毒", test_perform_detox)
    verifier.run_test("肝胆排毒", "胆汁分泌", test_bile_production)


def verify_body_master(verifier: SystemVerifier):
    """验证身体综合管理系统"""
    sys.path.insert(0, '/workspace/oriental_agent')
    exec(open('/workspace/oriental_agent/body/metabolism.py').read())
    exec(open('/workspace/oriental_agent/body/liver_detox.py').read())
    exec(open('/workspace/oriental_agent/body/body_master.py').read())
    
    def test_create():
        body = BodyMasterSystem()
        return body is not None
    
    def test_register():
        body = BodyMasterSystem()
        body.register_subsystem("metabolism", MetabolismSystem())
        return body.get_subsystem("metabolism") is not None
    
    def test_assess_health():
        body = BodyMasterSystem()
        body.register_subsystem("metabolism", MetabolismSystem())
        health = body.assess_health()
        return health is not None and health.overall >= 0
    
    def test_optimize():
        body = BodyMasterSystem()
        body.register_subsystem("metabolism", MetabolismSystem())
        result = body.optimize()
        return result is not None
    
    def test_get_status():
        body = BodyMasterSystem()
        status = body.get_full_status()
        return status is not None and "state" in status
    
    verifier.run_test("身体管理", "创建系统", test_create)
    verifier.run_test("身体管理", "注册子系统", test_register)
    verifier.run_test("身体管理", "健康评估", test_assess_health)
    verifier.run_test("身体管理", "执行优化", test_optimize)
    verifier.run_test("身体管理", "获取状态", test_get_status)


def verify_prediction_engine(verifier: SystemVerifier):
    """验证预测引擎"""
    sys.path.insert(0, '/workspace/oriental_agent')
    exec(open('/workspace/oriental_agent/prediction/prediction_engine.py').read())
    
    def test_yijing():
        engine = YiJingEngine()
        hexagram = engine.generate_hexagram(123)
        return hexagram is not None
    
    def test_yijing_interpret():
        engine = YiJingEngine()
        hexagram = engine.generate_hexagram(123)
        interp = engine.interpret_hexagram(hexagram)
        return interp is not None and "interpretation" in interp
    
    def test_meihua():
        engine = MeihuaEngine()
        result = engine.analyze("主体", "客体")
        return result is not None and result.tiangan is not None
    
    def test_wuxing_pred():
        engine = WuxingPredictionEngine()
        elements = {"木": 0.5, "火": 0.5, "土": 0.5, "金": 0.5, "水": 0.5}
        preds = engine.predict(elements)
        return len(preds) == 5
    
    def test_ganzhi_time():
        engine = GanzhiTimeEngine()
        year, month, day = engine.calculate_ganzhi(2024, 5, 15, 10)
        return len(year) == 2 and len(month) == 2 and len(day) == 2
    
    def test_prediction_engine():
        engine = PredictionEngine()
        result = engine.predict("测试")
        return result is not None and result.confidence > 0
    
    verifier.run_test("预测引擎", "易经卦象", test_yijing)
    verifier.run_test("预测引擎", "卦象解读", test_yijing_interpret)
    verifier.run_test("预测引擎", "梅花易数", test_meihua)
    verifier.run_test("预测引擎", "五行预测", test_wuxing_pred)
    verifier.run_test("预测引擎", "干支推算", test_ganzhi_time)
    verifier.run_test("预测引擎", "综合预测", test_prediction_engine)


def verify_instinct_system(verifier: SystemVerifier):
    """验证本能系统"""
    sys.path.insert(0, '/workspace/oriental_agent')
    exec(open('/workspace/oriental_agent/body/instinct_system.py').read())
    
    def test_create():
        system = InstinctSystem()
        return system is not None
    
    def test_process_stimulus():
        system = InstinctSystem()
        result = system.process_stimulus({"type": "threat", "intensity": 0.8, "source": "test"})
        return result is not None and len(result["signals"]) > 0
    
    def test_behavior_mapping():
        system = InstinctSystem()
        result = system.process_stimulus({"type": "novelty", "intensity": 0.7, "source": "test"})
        return result is not None and "candidate_behaviors" in result
    
    def test_wuxing_map():
        system = InstinctSystem()
        result = system.map_wuxing_influence("水", 0.5)
        return result is not None and "affected_levels" in result
    
    def test_yinyang_map():
        system = InstinctSystem()
        result = system.map_yinyang_balance(0.6)
        return result is not None and "yin_levels_activated" in result
    
    verifier.run_test("本能系统", "创建系统", test_create)
    verifier.run_test("本能系统", "刺激处理", test_process_stimulus)
    verifier.run_test("本能系统", "行为映射", test_behavior_mapping)
    verifier.run_test("本能系统", "五行映射", test_wuxing_map)
    verifier.run_test("本能系统", "阴阳映射", test_yinyang_map)


def stress_test(verifier: SystemVerifier):
    """压力测试"""
    sys.path.insert(0, '/workspace/oriental_agent')
    exec(open('/workspace/oriental_agent/core/seven_aperture_heart.py').read())
    exec(open('/workspace/oriental_agent/body/metabolism.py').read())
    exec(open('/workspace/oriental_agent/prediction/prediction_engine.py').read())
    
    def test_heart_100():
        heart = SevenApertureHeartSystem()
        heart.start()
        for i in range(100):
            heart.beat()
        heart.stop()
        return heart._beat_count >= 100
    
    def test_metabolism_100():
        system = MetabolismSystem()
        for i in range(100):
            system.consume_energy(1.0)
            system.produce_energy(5.0)
        return system._atp_pool >= 0
    
    def test_prediction_100():
        engine = PredictionEngine()
        for i in range(100):
            engine.predict(f"压力测试{i}")
        return len(engine.prediction_history) >= 100
    
    def test_parallel():
        heart = SevenApertureHeartSystem()
        metabolism = MetabolismSystem()
        engine = PredictionEngine()
        
        heart.start()
        for i in range(50):
            heart.beat()
            metabolism.consume_energy(1.0)
            engine.predict(f"并行测试{i}")
        heart.stop()
        
        return heart._beat_count >= 50 and len(engine.prediction_history) >= 50
    
    verifier.run_test("压力测试", "心脏100次", test_heart_100)
    verifier.run_test("压力测试", "代谢100次", test_metabolism_100)
    verifier.run_test("压力测试", "预测100次", test_prediction_100)
    verifier.run_test("压力测试", "并行测试", test_parallel)


def main():
    verifier = SystemVerifier()
    
    print("=" * 70)
    print("开始系统验证...")
    print("=" * 70)
    print()
    
    try:
        print("【1】验证七窍玲珑心系统...")
        verify_seven_aperture_heart(verifier)
    except Exception as e:
        print(f"   错误: {e}")
    
    try:
        print("【2】验证代谢系统...")
        verify_metabolism(verifier)
    except Exception as e:
        print(f"   错误: {e}")
    
    try:
        print("【3】验证肝胆排毒系统...")
        verify_liver_detox(verifier)
    except Exception as e:
        print(f"   错误: {e}")
    
    try:
        print("【4】验证身体综合管理系统...")
        verify_body_master(verifier)
    except Exception as e:
        print(f"   错误: {e}")
    
    try:
        print("【5】验证预测引擎...")
        verify_prediction_engine(verifier)
    except Exception as e:
        print(f"   错误: {e}")
    
    try:
        print("【6】验证本能系统...")
        verify_instinct_system(verifier)
    except Exception as e:
        print(f"   错误: {e}")
    
    try:
        print("【7】运行压力测试...")
        stress_test(verifier)
    except Exception as e:
        print(f"   错误: {e}")
    
    success = verifier.print_report()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
