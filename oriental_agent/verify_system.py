"""
系统完整性核对脚本。

用正常 import 调用当前公开 API，不再假设旧方法名。
这是手工核对，不是验收套件。通过数不能写成生产结论。
权威测试是 pytest tests/。
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
            result = test_func()
            if result:
                self.passed_tests += 1
                self._record_result(module_name, test_name, True, None)
                return True
            self.failed_tests += 1
            self._record_result(module_name, test_name, False, "Test returned False")
            return False
        except Exception as exc:
            self.failed_tests += 1
            self._record_result(module_name, test_name, False, str(exc))
            return False

    def _record_result(self, module: str, test: str, passed: bool, error: Any):
        bucket = self.results.setdefault(module, {"passed": 0, "failed": 0, "tests": []})
        if passed:
            bucket["passed"] += 1
        else:
            bucket["failed"] += 1
        bucket["tests"].append({"name": test, "passed": passed, "error": error})

    def print_report(self) -> bool:
        print("=" * 70)
        print("东方智慧智能体系统 - 完整性核对")
        print("=" * 70)
        print(f"核对时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("说明: 手工 import 核对，权威结果以 pytest 为准。")
        print()

        for module, result in self.results.items():
            print(f"【{module}】通过 {result['passed']} / 失败 {result['failed']}")
            for test in result["tests"]:
                if not test["passed"]:
                    print(f"  - {test['name']}: {test['error']}")
        print()
        print("-" * 70)
        rate = (self.passed_tests / self.total_tests * 100) if self.total_tests else 0
        print(f"总计: {self.total_tests}  通过: {self.passed_tests}  失败: {self.failed_tests}  通过率: {rate:.1f}%")
        print("=" * 70)
        return self.failed_tests == 0


def verify_core_system(verifier: SystemVerifier):
    from core.semantic_framework import ConceptCategory, ConceptMapping, SemanticFramework
    from core.seven_aperture_heart import HeartAperture, SevenApertureHeartSystem
    from core.wuxing_coupling import WuxingCouplingNetwork, WuxingElement

    def test_semantic_framework():
        framework = SemanticFramework()
        concept = ConceptMapping(
            concept_id="yinyang",
            concept_name="阴阳",
            category=ConceptCategory.YIN_YANG,
            philosophical_definition="阴阳平衡",
            technical_correspondence={"module": "memory"},
        )
        ok, _issues = framework.register_concept(concept, validate=False)
        found = framework.query("阴阳")
        return ok and len(found) > 0

    def test_wuxing_activate():
        network = WuxingCouplingNetwork()
        result = network.activate(WuxingElement.WOOD, 0.8)
        module = network.get_module(WuxingElement.WOOD)
        return module is not None and result.get("new_level", 0) > 0.3

    def test_heart_beat():
        heart = SevenApertureHeartSystem()
        heart.start()
        beat = heart.beat()
        state = heart.get_aperture_state(HeartAperture.SPIRIT)
        heart.stop()
        return beat.wisdom_output >= 0 and state is not None

    verifier.run_test("语义框架", "注册并查询", test_semantic_framework)
    verifier.run_test("五行耦合", "激活木行", test_wuxing_activate)
    verifier.run_test("七窍玲珑心", "心跳", test_heart_beat)


def verify_body_system(verifier: SystemVerifier):
    from body.body_master import BodyMasterSystem
    from body.instinct_system import InstinctSystem
    from body.jing_qi_shen import JingQiShenModel
    from body.liver_detox import LiverGallbladderDetoxSystem, Toxin, ToxinType
    from body.meridian_network import MeridianNetwork, MeridianType
    from body.metabolism import MetabolismSystem, Nutrient, NutrientType

    def test_jing():
        model = JingQiShenModel()
        before = model.current_level.jing_level
        model.nourish_jing(0.2)
        return model.current_level.jing_level >= before

    def test_meridian():
        network = MeridianNetwork()
        network.initialize()
        source = network.type_to_channel[MeridianType.HAND_TAIYIN_LUNG]
        target = network.type_to_channel[MeridianType.HAND_YANGMING_LARGE_INTESTINE]
        flow = network.flow_energy(source, target, 10.0)
        return flow.actual_transferred >= 0

    def test_instinct():
        system = InstinctSystem()
        result = system.process_stimulus({"type": "threat", "intensity": 0.8, "source": "test"})
        return "signals" in result and "candidate_behaviors" in result

    def test_metabolism():
        system = MetabolismSystem()
        food = [Nutrient(NutrientType.GLUCOSE, 10.0, 0.8, 1.0, 4.0)]
        result = system.process_food(food)
        return result.get("energy_gained", -1) >= 0

    def test_liver():
        system = LiverGallbladderDetoxSystem()
        toxin = Toxin("test", ToxinType.METABOLIC, 10.0, 0.5, "test", datetime.now())
        result = system.receive_toxins([toxin])
        return result["toxins_received"] == 1

    def test_body_master():
        body = BodyMasterSystem()
        body.register_subsystem("metabolism", MetabolismSystem())
        health = body.assess_health()
        status = body.get_full_status()
        return health.overall >= 0 and "state" in status

    verifier.run_test("精气神", "滋养", test_jing)
    verifier.run_test("经络网络", "能量流动", test_meridian)
    verifier.run_test("本能系统", "刺激处理", test_instinct)
    verifier.run_test("代谢系统", "食物处理", test_metabolism)
    verifier.run_test("肝胆排毒", "接收毒素", test_liver)
    verifier.run_test("身体管理", "健康评估", test_body_master)


def verify_memory_system(verifier: SystemVerifier):
    from memory.ganzhi_coordinate import GanzhiMarker
    from memory.yinyang_storage import YinYangStorage

    def test_storage():
        storage = YinYangStorage()
        memory = storage.store("value1")
        return storage.get(memory.memory_id) is not None

    def test_ganzhi():
        marker = GanzhiMarker()
        record = marker.mark({"event": "test"}, "rec-1")
        return record is not None and marker.get_marked_record("rec-1") is not None

    verifier.run_test("阴阳存储", "存储检索", test_storage)
    verifier.run_test("干支坐标", "打标", test_ganzhi)


def verify_perception_system(verifier: SystemVerifier):
    from perception.eight_consciousness import ConsciousnessLevel, EightConsciousnessSystem

    def test_eight():
        system = EightConsciousnessSystem()
        processed = system.process({ConsciousnessLevel.EYE: {"image": "test"}})
        return processed is not None

    verifier.run_test("八识系统", "感知处理", test_eight)


def verify_prediction_system(verifier: SystemVerifier):
    from prediction.prediction_engine import (
        GanzhiTimeEngine,
        HEURISTIC_DISCLAIMER,
        MeihuaEngine,
        PredictionEngine,
        WuxingPredictionEngine,
        YiJingEngine,
    )

    def test_yijing():
        result = YiJingEngine().predict("测试")
        return result.confidence > 0

    def test_meihua():
        result = MeihuaEngine().analyze("主体", "客体")
        return result is not None and result.result.get("tiangan")

    def test_wuxing():
        preds = WuxingPredictionEngine().predict({"木": 0.5, "火": 0.5, "土": 0.5, "金": 0.5, "水": 0.5})
        return len(preds) == 5

    def test_ganzhi():
        pred = GanzhiTimeEngine().predict_time_energy(datetime.now())
        return pred.predicted_energy > 0

    def test_engine():
        result = PredictionEngine().predict("综合测试")
        return result.confidence > 0 and HEURISTIC_DISCLAIMER in result.interpretation

    verifier.run_test("易经预测", "卦象", test_yijing)
    verifier.run_test("梅花易数", "体用", test_meihua)
    verifier.run_test("五行预测", "趋势", test_wuxing)
    verifier.run_test("干支时空", "能量", test_ganzhi)
    verifier.run_test("预测引擎", "综合预测与免责声明", test_engine)


def verify_martial_narrative(verifier: SystemVerifier):
    """核对武学叙事状态机。真实访问控制在 integration/，不在这里。"""
    from narrative.martial_state_machine import AdaptiveDefenseSelector, Attack, TaijiDefense, ThreatType

    def test_taiji():
        attack = Attack("a1", ThreatType.BRUTE_FORCE, 0.8, "front", "test")
        result = TaijiDefense().execute(attack)
        return result.damage_mitigated >= 0

    def test_selector():
        attack = Attack("a2", ThreatType.BRUTE_FORCE, 0.8, "front", "test")
        selector = AdaptiveDefenseSelector()
        strategy = selector.select_strategy(selector.analyze_threat(attack))
        return strategy is not None

    verifier.run_test("武学叙事", "太极回合", test_taiji)
    verifier.run_test("武学叙事", "策略切换", test_selector)


def verify_evolution_system(verifier: SystemVerifier):
    from evolution.cultivation import (
        BreakthroughMechanism,
        CultivationProgress,
        ExperienceAccumulator,
        TaskResult,
    )

    def test_experience():
        progress = CultivationProgress()
        gained = ExperienceAccumulator(progress).accumulate(TaskResult(
            task_id="t1",
            task_type="meditate",
            success=True,
            difficulty=1.0,
            execution_time=1.0,
            quality_score=0.8,
        ))
        return gained > 0 and progress.experience > 0

    def test_readiness():
        progress = CultivationProgress(experience=1000, insight_points=50, stability=0.8)
        report = BreakthroughMechanism(progress).check_breakthrough_readiness()
        return isinstance(report, dict)

    verifier.run_test("修炼系统", "经验积累", test_experience)
    verifier.run_test("修炼系统", "突破就绪检查", test_readiness)


def verify_interaction_system(verifier: SystemVerifier):
    from interaction.qi_field import QiFieldSystem

    def test_qi():
        system = QiFieldSystem()
        emitted = system.emit_field()
        return emitted.get("success") is True and system.emitter.get_state().intensity > 0

    verifier.run_test("气场系统", "发射气场", test_qi)


def verify_investment_regression(verifier: SystemVerifier):
    from commercial.agent import CommercialAgent

    def test_chinese_amount():
        result = CommercialAgent().analyze_investment({"query": "我想投资10万"})
        return result.get("initial_investment") == 100000 and "error" not in result

    def test_missing_amount():
        result = CommercialAgent().analyze_investment({"query": "帮我看看"})
        return "initial_investment" in result.get("error", "") and result.get("data_status") == "数据不足"

    verifier.run_test("投资分析", "中文金额不崩溃", test_chinese_amount)
    verifier.run_test("投资分析", "缺金额返回明确错误", test_missing_amount)


def main():
    verifier = SystemVerifier()
    steps = [
        ("核心系统", verify_core_system),
        ("身体系统", verify_body_system),
        ("记忆系统", verify_memory_system),
        ("感知系统", verify_perception_system),
        ("预测系统", verify_prediction_system),
        ("武学叙事", verify_martial_narrative),
        ("修炼系统", verify_evolution_system),
        ("交互系统", verify_interaction_system),
        ("投资回归", verify_investment_regression),
    ]
    for title, func in steps:
        print(f"核对{title}...")
        try:
            func(verifier)
        except Exception as exc:
            print(f"{title}核对出错: {exc}")
            traceback.print_exc()
    success = verifier.print_report()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
