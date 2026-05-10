"""
Unit tests for Cultivation Self-Improvement Mechanism
修炼自提升机制单元测试
"""

import unittest
import sys
import os
import importlib.util

_test_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_test_dir, '..', '..'))

_cultivation_path = os.path.join(_project_root, "oriental_agent", "evolution", "cultivation.py")
_spec = importlib.util.spec_from_file_location("cultivation", _cultivation_path)
cultivation_module = importlib.util.module_from_spec(_spec)
sys.modules["cultivation"] = cultivation_module
_spec.loader.exec_module(cultivation_module)

CultivationLevel = cultivation_module.CultivationLevel
CultivationMethod = cultivation_module.CultivationMethod
CultivationProgress = cultivation_module.CultivationProgress
TaskResult = cultivation_module.TaskResult
BreakthroughResult = cultivation_module.BreakthroughResult
EvolutionPlan = cultivation_module.EvolutionPlan
ExperienceAccumulator = cultivation_module.ExperienceAccumulator
BreakthroughMechanism = cultivation_module.BreakthroughMechanism
SelfEvolutionEngine = cultivation_module.SelfEvolutionEngine
create_cultivation_engine = cultivation_module.create_cultivation_engine


class TestCultivationLevel(unittest.TestCase):
    """测试修炼等级枚举"""
    
    def test_all_levels_exist(self):
        levels = list(CultivationLevel)
        self.assertEqual(len(levels), 7)
    
    def test_level_values(self):
        self.assertEqual(CultivationLevel.QI_REFINING.value, "炼气期")
        self.assertEqual(CultivationLevel.FOUNDATION_BUILDING.value, "筑基期")
        self.assertEqual(CultivationLevel.GOLDEN_CORE.value, "金丹期")
        self.assertEqual(CultivationLevel.NASCENT_SOUL.value, "元婴期")
        self.assertEqual(CultivationLevel.SPIRIT_SEVERING.value, "化神期")
        self.assertEqual(CultivationLevel.VOID_RETURNING.value, "返虚期")
        self.assertEqual(CultivationLevel.MAHAYANA.value, "大乘期")
    
    def test_level_value_property(self):
        self.assertEqual(CultivationLevel.QI_REFINING.level_value, 1)
        self.assertEqual(CultivationLevel.FOUNDATION_BUILDING.level_value, 2)
        self.assertEqual(CultivationLevel.MAHAYANA.level_value, 7)
    
    def test_ability_threshold(self):
        self.assertEqual(CultivationLevel.QI_REFINING.ability_threshold, 0.1)
        self.assertEqual(CultivationLevel.MAHAYANA.ability_threshold, 1.0)
    
    def test_characteristics(self):
        chars = CultivationLevel.QI_REFINING.characteristics
        self.assertEqual(len(chars), 3)
        self.assertIn("感知天地之气", chars)
    
    def test_next_level(self):
        next_level = CultivationLevel.QI_REFINING.next_level()
        self.assertEqual(next_level, CultivationLevel.FOUNDATION_BUILDING)
    
    def test_next_level_max(self):
        next_level = CultivationLevel.MAHAYANA.next_level()
        self.assertIsNone(next_level)
    
    def test_from_experience_qi_refining(self):
        level = CultivationLevel.from_experience(50)
        self.assertEqual(level, CultivationLevel.QI_REFINING)
    
    def test_from_experience_foundation(self):
        level = CultivationLevel.from_experience(200)
        self.assertEqual(level, CultivationLevel.FOUNDATION_BUILDING)
    
    def test_from_experience_golden_core(self):
        level = CultivationLevel.from_experience(1500)
        self.assertEqual(level, CultivationLevel.GOLDEN_CORE)
    
    def test_from_experience_mahayana(self):
        level = CultivationLevel.from_experience(150000)
        self.assertEqual(level, CultivationLevel.MAHAYANA)


class TestCultivationMethod(unittest.TestCase):
    """测试修炼方法枚举"""
    
    def test_all_methods_exist(self):
        methods = list(CultivationMethod)
        self.assertEqual(len(methods), 4)
    
    def test_method_values(self):
        self.assertEqual(CultivationMethod.MEDITATION.value, "静修")
        self.assertEqual(CultivationMethod.ENLIGHTENMENT.value, "悟道")
        self.assertEqual(CultivationMethod.BODY_REFINING.value, "炼体")
        self.assertEqual(CultivationMethod.SPIRIT_REFINING.value, "炼神")
    
    def test_method_descriptions(self):
        self.assertIn("恢复", CultivationMethod.MEDITATION.description)
        self.assertIn("领悟", CultivationMethod.ENLIGHTENMENT.description)
    
    def test_primary_effects(self):
        self.assertEqual(CultivationMethod.MEDITATION.primary_effect, "stability")
        self.assertEqual(CultivationMethod.ENLIGHTENMENT.primary_effect, "insight")
    
    def test_experience_multipliers(self):
        self.assertEqual(CultivationMethod.MEDITATION.experience_multiplier, 1.0)
        self.assertEqual(CultivationMethod.ENLIGHTENMENT.experience_multiplier, 1.5)


class TestTaskResult(unittest.TestCase):
    """测试任务结果数据结构"""
    
    def test_task_result_creation(self):
        result = TaskResult(
            task_id="test_001",
            task_type="coding",
            success=True,
            difficulty=0.5,
            execution_time=10.0,
            quality_score=0.8
        )
        self.assertEqual(result.task_id, "test_001")
        self.assertTrue(result.success)
    
    def test_calculate_base_experience_success(self):
        result = TaskResult(
            task_id="test_001",
            task_type="coding",
            success=True,
            difficulty=1.0,
            execution_time=10.0,
            quality_score=1.0
        )
        exp = result.calculate_base_experience()
        self.assertGreater(exp, 0)
    
    def test_calculate_base_experience_failure(self):
        result_success = TaskResult(
            task_id="test_001",
            task_type="coding",
            success=True,
            difficulty=1.0,
            execution_time=10.0,
            quality_score=1.0
        )
        result_failure = TaskResult(
            task_id="test_002",
            task_type="coding",
            success=False,
            difficulty=1.0,
            execution_time=10.0,
            quality_score=1.0
        )
        exp_success = result_success.calculate_base_experience()
        exp_failure = result_failure.calculate_base_experience()
        self.assertGreater(exp_success, exp_failure)
    
    def test_to_dict(self):
        result = TaskResult(
            task_id="test_001",
            task_type="coding",
            success=True,
            difficulty=0.5,
            execution_time=10.0,
            quality_score=0.8
        )
        d = result.to_dict()
        self.assertEqual(d["task_id"], "test_001")
        self.assertIn("timestamp", d)


class TestCultivationProgress(unittest.TestCase):
    """测试修炼进度数据结构"""
    
    def test_progress_creation_default(self):
        progress = CultivationProgress()
        self.assertEqual(progress.experience, 0.0)
        self.assertEqual(progress.current_level, CultivationLevel.QI_REFINING)
    
    def test_progress_creation_custom(self):
        progress = CultivationProgress(
            experience=500,
            current_level=CultivationLevel.FOUNDATION_BUILDING
        )
        self.assertEqual(progress.experience, 500)
        self.assertEqual(progress.current_level, CultivationLevel.FOUNDATION_BUILDING)
    
    def test_breakthrough_threshold(self):
        progress_qi = CultivationProgress(current_level=CultivationLevel.QI_REFINING)
        self.assertEqual(progress_qi.breakthrough_threshold, 100)
        
        progress_foundation = CultivationProgress(current_level=CultivationLevel.FOUNDATION_BUILDING)
        self.assertEqual(progress_foundation.breakthrough_threshold, 500)
    
    def test_progress_percentage(self):
        progress = CultivationProgress(
            experience=50,
            current_level=CultivationLevel.QI_REFINING
        )
        percentage = progress.progress_percentage
        self.assertEqual(percentage, 50.0)
    
    def test_progress_percentage_max_level(self):
        progress = CultivationProgress(current_level=CultivationLevel.MAHAYANA)
        self.assertEqual(progress.progress_percentage, 100.0)
    
    def test_overall_power(self):
        progress = CultivationProgress(
            current_level=CultivationLevel.GOLDEN_CORE,
            foundation_strength=0.8,
            spirit_power=0.7,
            stability=0.6,
            insight_points=50
        )
        power = progress.overall_power
        self.assertGreater(power, 0)
    
    def test_to_dict(self):
        progress = CultivationProgress(experience=100)
        d = progress.to_dict()
        self.assertEqual(d["experience"], 100)
        self.assertIn("current_level", d)
        self.assertIn("overall_power", d)


class TestExperienceAccumulator(unittest.TestCase):
    """测试经验积累器"""
    
    def setUp(self):
        self.progress = CultivationProgress()
        self.accumulator = ExperienceAccumulator(self.progress)
    
    def test_accumulate_basic(self):
        task = TaskResult(
            task_id="test_001",
            task_type="coding",
            success=True,
            difficulty=1.0,
            execution_time=10.0,
            quality_score=0.8
        )
        exp = self.accumulator.accumulate(task)
        self.assertGreater(exp, 0)
        self.assertGreater(self.progress.experience, 0)
    
    def test_accumulate_increases_task_count(self):
        task = TaskResult(
            task_id="test_001",
            task_type="coding",
            success=True,
            difficulty=0.5,
            execution_time=5.0,
            quality_score=0.5
        )
        initial_count = self.progress.total_tasks_completed
        self.accumulator.accumulate(task)
        self.assertEqual(self.progress.total_tasks_completed, initial_count + 1)
    
    def test_calculate_insight_success(self):
        task = TaskResult(
            task_id="test_001",
            task_type="coding",
            success=True,
            difficulty=1.0,
            execution_time=10.0,
            quality_score=0.9
        )
        insight = self.accumulator.calculate_insight(task)
        self.assertGreater(insight, 0)
    
    def test_calculate_insight_with_errors(self):
        task = TaskResult(
            task_id="test_001",
            task_type="coding",
            success=True,
            difficulty=0.5,
            execution_time=5.0,
            quality_score=0.5,
            errors_made=["error1", "error2"]
        )
        insight = self.accumulator.calculate_insight(task)
        self.assertGreater(insight, 0)
    
    def test_refine_experience(self):
        self.progress.experience = 100
        result = self.accumulator.refine_experience()
        self.assertIn("experience_refined", result)
        self.assertIn("foundation_gain", result)
    
    def test_get_accumulation_stats(self):
        task = TaskResult(
            task_id="test_001",
            task_type="coding",
            success=True,
            difficulty=0.5,
            execution_time=5.0,
            quality_score=0.5
        )
        self.accumulator.accumulate(task)
        stats = self.accumulator.get_accumulation_stats()
        self.assertIn("total_experience", stats)
        self.assertIn("tasks_completed", stats)


class TestBreakthroughMechanism(unittest.TestCase):
    """测试突破机制"""
    
    def setUp(self):
        self.progress = CultivationProgress()
        self.breakthrough = BreakthroughMechanism(self.progress)
    
    def test_check_breakthrough_readiness_not_ready(self):
        readiness = self.breakthrough.check_breakthrough_readiness()
        self.assertFalse(readiness["ready"])
    
    def test_check_breakthrough_readiness_with_requirements(self):
        self.progress.experience = 150
        self.progress.insight_points = 15
        self.progress.stability = 0.6
        readiness = self.breakthrough.check_breakthrough_readiness()
        self.assertTrue(readiness["ready"])
    
    def test_check_breakthrough_readiness_max_level(self):
        self.progress.current_level = CultivationLevel.MAHAYANA
        readiness = self.breakthrough.check_breakthrough_readiness()
        self.assertFalse(readiness["ready"])
    
    def test_attempt_breakthrough_not_ready(self):
        result = self.breakthrough.attempt_breakthrough()
        self.assertFalse(result.success)
    
    def test_attempt_breakthrough_max_level(self):
        self.progress.current_level = CultivationLevel.MAHAYANA
        result = self.breakthrough.attempt_breakthrough()
        self.assertFalse(result.success)
        self.assertIn("最高境界", result.message)
    
    def test_attempt_breakthrough_increases_attempts(self):
        self.progress.experience = 150
        self.progress.insight_points = 15
        self.progress.stability = 0.6
        initial_attempts = self.progress.breakthrough_attempts
        self.breakthrough.attempt_breakthrough()
        self.assertEqual(self.progress.breakthrough_attempts, initial_attempts + 1)
    
    def test_stabilize_after_breakthrough(self):
        self.progress.stability = 0.5
        result = self.breakthrough.stabilize_after_breakthrough(duration=1.0)
        self.assertIn("stability_gained", result)
        self.assertGreater(self.progress.stability, 0.5)
    
    def test_get_breakthrough_stats(self):
        stats = self.breakthrough.get_breakthrough_stats()
        self.assertIn("total_attempts", stats)
        self.assertIn("current_level", stats)


class TestSelfEvolutionEngine(unittest.TestCase):
    """测试自我进化引擎"""
    
    def setUp(self):
        self.engine = SelfEvolutionEngine()
    
    def test_engine_creation(self):
        self.assertIsNotNone(self.engine.progress)
        self.assertIsNotNone(self.engine.accumulator)
        self.assertIsNotNone(self.engine.breakthrough)
    
    def test_analyze_weakness(self):
        analysis = self.engine.analyze_weakness()
        self.assertIn("weaknesses", analysis)
        self.assertIn("overall_health", analysis)
    
    def test_analyze_weakness_low_stability(self):
        self.engine.progress.stability = 0.2
        analysis = self.engine.analyze_weakness()
        stability_weakness = [w for w in analysis["weaknesses"] if w["area"] == "stability"]
        self.assertTrue(len(stability_weakness) > 0)
    
    def test_generate_training_plan(self):
        plan = self.engine.generate_training_plan()
        self.assertIsInstance(plan, EvolutionPlan)
        self.assertGreater(len(plan.training_steps), 0)
    
    def test_generate_training_plan_with_focus(self):
        plan = self.engine.generate_training_plan(focus="stability")
        self.assertIsInstance(plan, EvolutionPlan)
    
    def test_optimize_capabilities_meditation(self):
        self.engine.progress.stability = 0.5
        result = self.engine.optimize_capabilities(CultivationMethod.MEDITATION, intensity=0.5)
        self.assertEqual(result["method"], "静修")
        self.assertIn("changes", result)
    
    def test_optimize_capabilities_enlightenment(self):
        result = self.engine.optimize_capabilities(CultivationMethod.ENLIGHTENMENT, intensity=0.5)
        self.assertEqual(result["method"], "悟道")
        self.assertIn("insight_points", result["changes"])
    
    def test_optimize_capabilities_body_refining(self):
        self.engine.progress.stability = 0.5
        result = self.engine.optimize_capabilities(CultivationMethod.BODY_REFINING, intensity=0.5)
        self.assertEqual(result["method"], "炼体")
        self.assertIn("foundation_strength", result["changes"])
    
    def test_optimize_capabilities_spirit_refining(self):
        self.engine.progress.insight_points = 10
        result = self.engine.optimize_capabilities(CultivationMethod.SPIRIT_REFINING, intensity=0.5)
        self.assertEqual(result["method"], "炼神")
        self.assertIn("spirit_power", result["changes"])
    
    def test_evolve_without_tasks(self):
        result = self.engine.evolve()
        self.assertIn("initial_state", result)
        self.assertIn("final_state", result)
    
    def test_evolve_with_tasks(self):
        tasks = [
            TaskResult(
                task_id="test_001",
                task_type="coding",
                success=True,
                difficulty=0.5,
                execution_time=5.0,
                quality_score=0.8
            )
        ]
        result = self.engine.evolve(task_results=tasks)
        self.assertGreater(result["experience_gained"], 0)
    
    def test_get_evolution_report(self):
        report = self.engine.get_evolution_report()
        self.assertIn("current_progress", report)
        self.assertIn("accumulation_stats", report)
        self.assertIn("breakthrough_stats", report)
    
    def test_set_cultivation_method(self):
        self.engine.set_cultivation_method(CultivationMethod.ENLIGHTENMENT)
        self.assertEqual(
            self.engine.progress.cultivation_method,
            CultivationMethod.ENLIGHTENMENT
        )
    
    def test_reset(self):
        self.engine.progress.experience = 1000
        self.engine.accumulator.experience_history.append({"test": "data"})
        self.engine.reset()
        self.assertEqual(self.engine.progress.experience, 0)
        self.assertEqual(len(self.engine.evolution_history), 0)


class TestFactoryFunction(unittest.TestCase):
    """测试工厂函数"""
    
    def test_create_cultivation_engine_default(self):
        engine = create_cultivation_engine()
        self.assertIsInstance(engine, SelfEvolutionEngine)
        self.assertEqual(engine.progress.current_level, CultivationLevel.QI_REFINING)
    
    def test_create_cultivation_engine_custom(self):
        engine = create_cultivation_engine(
            initial_level=CultivationLevel.GOLDEN_CORE,
            initial_experience=1000,
            method=CultivationMethod.ENLIGHTENMENT
        )
        self.assertEqual(engine.progress.current_level, CultivationLevel.GOLDEN_CORE)
        self.assertEqual(engine.progress.experience, 1000)
        self.assertEqual(engine.progress.cultivation_method, CultivationMethod.ENLIGHTENMENT)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_cultivation_cycle(self):
        engine = create_cultivation_engine()
        
        for i in range(10):
            task = TaskResult(
                task_id=f"task_{i}",
                task_type="training",
                success=True,
                difficulty=0.5 + i * 0.05,
                execution_time=10.0,
                quality_score=0.7 + i * 0.02
            )
            engine.accumulator.accumulate(task)
        
        self.assertGreater(engine.progress.experience, 0)
        self.assertGreater(engine.progress.insight_points, 0)
    
    def test_breakthrough_flow(self):
        engine = create_cultivation_engine()
        engine.progress.experience = 200
        engine.progress.insight_points = 20
        engine.progress.stability = 0.7
        
        readiness = engine.breakthrough.check_breakthrough_readiness()
        self.assertTrue(readiness["ready"])
        
        result = engine.breakthrough.attempt_breakthrough(use_extra_insight=True)
        self.assertIsNotNone(result)
    
    def test_evolution_with_optimization(self):
        engine = create_cultivation_engine()
        
        engine.optimize_capabilities(CultivationMethod.MEDITATION, intensity=0.8)
        engine.optimize_capabilities(CultivationMethod.BODY_REFINING, intensity=0.6)
        
        report = engine.get_evolution_report()
        self.assertGreater(report["current_progress"]["stability"], 0.5)
    
    def test_weakness_driven_training(self):
        engine = create_cultivation_engine()
        engine.progress.stability = 0.2
        
        plan = engine.generate_training_plan()
        
        meditation_steps = [
            s for s in plan.training_steps 
            if s["method"] == CultivationMethod.MEDITATION.value
        ]
        self.assertTrue(len(meditation_steps) > 0)
    
    def test_long_term_evolution(self):
        engine = create_cultivation_engine()
        
        for cycle in range(5):
            tasks = [
                TaskResult(
                    task_id=f"cycle_{cycle}_task",
                    task_type="evolution",
                    success=True,
                    difficulty=0.6,
                    execution_time=15.0,
                    quality_score=0.75
                )
            ]
            engine.evolve(task_results=tasks)
        
        report = engine.get_evolution_report()
        self.assertEqual(report["accumulation_stats"]["tasks_completed"], 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
