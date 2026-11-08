"""
系统核对脚本 v2。

旧版用 exec() 把源码注入全局命名空间，并且路径指向不存在的
/workspace/oriental_agent/...。这里改为与包结构一致的正常 import。
权威测试仍是 pytest tests/。
"""

import sys
import traceback
from datetime import datetime
from typing import Any, Callable, Dict


class SystemVerifier:
    def __init__(self):
        self.results: Dict[str, Dict] = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

    def run_test(self, module_name: str, test_name: str, test_func: Callable[[], bool]) -> bool:
        self.total_tests += 1
        try:
            if test_func():
                self.passed_tests += 1
                self._record_result(module_name, test_name, True, None)
                return True
            self.failed_tests += 1
            self._record_result(module_name, test_name, False, "Test returned False")
            return False
        except Exception as exc:
            self.failed_tests += 1
            self._record_result(module_name, test_name, False, str(exc)[:200])
            return False

    def _record_result(self, module: str, test: str, passed: bool, error: Any):
        bucket = self.results.setdefault(module, {"passed": 0, "failed": 0, "tests": []})
        bucket["passed" if passed else "failed"] += 1
        bucket["tests"].append({"name": test, "passed": passed, "error": error})

    def print_report(self) -> bool:
        print("=" * 70)
        print("东方智慧智能体系统 - 完整性核对 v2")
        print("=" * 70)
        print(f"核对时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("说明: 正常 import，不再 exec 注入源码。")
        print()
        for module, result in self.results.items():
            mark = "OK" if result["failed"] == 0 else "FAIL"
            print(f"[{mark}] {module}  通过 {result['passed']} / 失败 {result['failed']}")
            for test in result["tests"]:
                if not test["passed"]:
                    print(f"   - {test['name']}: {test['error']}")
        print("-" * 70)
        rate = (self.passed_tests / self.total_tests * 100) if self.total_tests else 0
        print(f"总计 {self.total_tests}  通过 {self.passed_tests}  失败 {self.failed_tests}  通过率 {rate:.1f}%")
        print("=" * 70)
        return self.failed_tests == 0


def verify_seven_aperture_heart(verifier: SystemVerifier):
    from core.seven_aperture_heart import HeartAperture, SevenApertureHeartSystem

    def test_create():
        return SevenApertureHeartSystem() is not None

    def test_start():
        heart = SevenApertureHeartSystem()
        started = heart.start()
        heart.stop()
        return started is True

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
        # duration=0 不睡眠，只确认接口返回成功
        result = heart.meditate(0)
        heart.stop()
        return result is not None and result["success"] is True

    verifier.run_test("七窍玲珑心", "创建系统", test_create)
    verifier.run_test("七窍玲珑心", "启动系统", test_start)
    verifier.run_test("七窍玲珑心", "心跳生成", test_beat)
    verifier.run_test("七窍玲珑心", "窍穴激活", test_aperture)
    verifier.run_test("七窍玲珑心", "冥想接口", test_meditate)


def verify_metabolism(verifier: SystemVerifier):
    from body.metabolism import MetabolismSystem, Nutrient, NutrientType

    def test_create():
        return MetabolismSystem() is not None

    def test_process_food():
        system = MetabolismSystem()
        food = [
            Nutrient(NutrientType.GLUCOSE, 10.0, 0.8, 1.0, 4.0),
            Nutrient(NutrientType.FAT, 5.0, 0.9, 1.0, 9.0),
        ]
        result = system.process_food(food)
        return result is not None and "energy_gained" in result

    def test_produce_energy():
        system = MetabolismSystem()
        system._energy_reserve = 100.0
        result = system.produce_energy(10.0)
        return result is not None and result.get("success") is True

    def test_consume_energy():
        system = MetabolismSystem()
        system._atp_pool = 50.0
        return system.consume_energy(10.0) is True

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
    from body.liver_detox import GallbladderSystem, LiverGallbladderDetoxSystem, Toxin, ToxinType

    def test_create():
        return LiverGallbladderDetoxSystem() is not None

    def test_receive_toxins():
        system = LiverGallbladderDetoxSystem()
        toxins = [Toxin("test", ToxinType.METABOLIC, 10.0, 0.5, "test", datetime.now())]
        result = system.receive_toxins(toxins)
        return result is not None and result["toxins_received"] == 1

    def test_start_detox():
        result = LiverGallbladderDetoxSystem().start_detox_cycle()
        return result is not None and result["cycle_started"] is True

    def test_perform_detox():
        system = LiverGallbladderDetoxSystem()
        system.start_detox_cycle()
        result = system.perform_detox(1.0)
        return result is not None and "phase" in result

    def test_bile():
        bile = GallbladderSystem().produce_bile(10.0)
        return bile is not None and bile.amount == 10.0

    verifier.run_test("肝胆排毒", "创建系统", test_create)
    verifier.run_test("肝胆排毒", "接收毒素", test_receive_toxins)
    verifier.run_test("肝胆排毒", "启动排毒", test_start_detox)
    verifier.run_test("肝胆排毒", "执行排毒", test_perform_detox)
    verifier.run_test("肝胆排毒", "胆汁分泌", test_bile)


def verify_body_master(verifier: SystemVerifier):
    from body.body_master import BodyMasterSystem
    from body.metabolism import MetabolismSystem

    def test_create():
        return BodyMasterSystem() is not None

    def test_register():
        body = BodyMasterSystem()
        body.register_subsystem("metabolism", MetabolismSystem())
        return body.get_subsystem("metabolism") is not None

    def test_assess_health():
        body = BodyMasterSystem()
        body.register_subsystem("metabolism", MetabolismSystem())
        health = body.assess_health()
        return health is not None and health.overall >= 0

    def test_status():
        status = BodyMasterSystem().get_full_status()
        return status is not None and "state" in status

    verifier.run_test("身体管理", "创建系统", test_create)
    verifier.run_test("身体管理", "注册子系统", test_register)
    verifier.run_test("身体管理", "健康评估", test_assess_health)
    verifier.run_test("身体管理", "获取状态", test_status)


def verify_prediction_engine(verifier: SystemVerifier):
    from prediction.prediction_engine import (
        GanzhiTimeEngine,
        MeihuaEngine,
        PredictionEngine,
        WuxingPredictionEngine,
        YiJingEngine,
    )

    def test_yijing():
        engine = YiJingEngine()
        return engine.generate_hexagram(123) is not None

    def test_interpret():
        engine = YiJingEngine()
        interp = engine.interpret_hexagram(engine.generate_hexagram(123))
        return interp is not None and "interpretation" in interp

    def test_meihua():
        result = MeihuaEngine().analyze("主体", "客体")
        return result is not None and result.result.get("tiangan") is not None

    def test_wuxing():
        preds = WuxingPredictionEngine().predict({"木": 0.5, "火": 0.5, "土": 0.5, "金": 0.5, "水": 0.5})
        return len(preds) == 5

    def test_ganzhi():
        year, month, day = GanzhiTimeEngine().calculate_ganzhi(2024, 5, 15, 10)
        return len(year) == 2 and len(month) == 2 and len(day) == 2

    def test_engine():
        result = PredictionEngine().predict("测试")
        return result is not None and result.confidence > 0 and result.heuristic_disclaimer

    verifier.run_test("预测引擎", "易经卦象", test_yijing)
    verifier.run_test("预测引擎", "卦象解读", test_interpret)
    verifier.run_test("预测引擎", "梅花易数", test_meihua)
    verifier.run_test("预测引擎", "五行预测", test_wuxing)
    verifier.run_test("预测引擎", "干支推算", test_ganzhi)
    verifier.run_test("预测引擎", "综合预测", test_engine)


def verify_instinct_system(verifier: SystemVerifier):
    from body.instinct_system import InstinctSystem

    def test_create():
        return InstinctSystem() is not None

    def test_process():
        result = InstinctSystem().process_stimulus({"type": "threat", "intensity": 0.8, "source": "test"})
        return result is not None and len(result["signals"]) >= 0 and "candidate_behaviors" in result

    def test_wuxing():
        result = InstinctSystem().map_wuxing_influence("水", 0.5)
        return result is not None and "affected_levels" in result

    def test_yinyang():
        result = InstinctSystem().map_yinyang_balance(0.6)
        return result is not None and "yin_levels_activated" in result

    verifier.run_test("本能系统", "创建系统", test_create)
    verifier.run_test("本能系统", "刺激处理", test_process)
    verifier.run_test("本能系统", "五行映射", test_wuxing)
    verifier.run_test("本能系统", "阴阳映射", test_yinyang)


def verify_short_stress(verifier: SystemVerifier):
    from body.metabolism import MetabolismSystem
    from core.seven_aperture_heart import SevenApertureHeartSystem
    from prediction.prediction_engine import PredictionEngine

    def test_heart():
        heart = SevenApertureHeartSystem()
        heart.start()
        for _ in range(20):
            heart.beat()
        heart.stop()
        return heart._beat_count >= 20

    def test_metabolism():
        system = MetabolismSystem()
        for _ in range(20):
            system.consume_energy(1.0)
            system.produce_energy(5.0)
        return system._atp_pool >= 0

    def test_prediction():
        engine = PredictionEngine()
        for index in range(10):
            engine.predict(f"核对{index}")
        return len(engine.prediction_history) >= 10

    verifier.run_test("短压测", "心脏 20 次", test_heart)
    verifier.run_test("短压测", "代谢 20 次", test_metabolism)
    verifier.run_test("短压测", "预测 10 次", test_prediction)


def main():
    verifier = SystemVerifier()
    steps = [
        ("七窍玲珑心", verify_seven_aperture_heart),
        ("代谢系统", verify_metabolism),
        ("肝胆排毒", verify_liver_detox),
        ("身体管理", verify_body_master),
        ("预测引擎", verify_prediction_engine),
        ("本能系统", verify_instinct_system),
        ("短压测", verify_short_stress),
    ]
    print("开始系统核对 v2（正常 import）")
    for title, func in steps:
        print(f"【{title}】")
        try:
            func(verifier)
        except Exception as exc:
            print(f"   错误: {exc}")
            traceback.print_exc()
    return 0 if verifier.print_report() else 1


if __name__ == "__main__":
    sys.exit(main())
