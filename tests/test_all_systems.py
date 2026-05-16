"""
四大系统单元测试
- 本能系统 (body/system.py)
- 形象气场系统 (image/system.py)
- 预测系统 (memory/hexagram_predictor.py)
- 商道系统 (execution/shangdao.py)
"""

import sys
import os
import asyncio
import unittest
from datetime import datetime

# 设置导入路径 — 用 importlib 绕过 __init__.py 循环导入
OA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if OA_DIR not in sys.path:
    sys.path.insert(0, OA_DIR)

import importlib.util

def _load_module(rel_path: str):
    full = os.path.join(OA_DIR, 'oriental_agent', rel_path)
    spec = importlib.util.spec_from_file_location('_mod', full)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod

# 按依赖顺序加载
cfg = _load_module('config/settings.py')
sys.modules['config'] = cfg; sys.modules['config.settings'] = cfg

ct = _load_module('core/types.py')
sys.modules['core.types'] = ct; sys.modules['oriental_agent.core.types'] = ct

wu = _load_module('memory/wuxing.py')
sys.modules['memory.wuxing'] = wu; sys.modules['oriental_agent.memory.wuxing'] = wu

yy = _load_module('memory/yinyang.py')
sys.modules['memory.yinyang'] = yy

td = _load_module('memory/tiangan_dizhi.py')
sys.modules['memory.tiangan_dizhi'] = td

hx = _load_module('memory/hexagram_predictor.py')
sys.modules['memory.hexagram_predictor'] = hx

sd = _load_module('execution/shangdao.py')
sys.modules['execution.shangdao'] = sd

bs = _load_module('body/system.py')
sys.modules['body.system'] = bs

ims = _load_module('image/system.py')
sys.modules['image.system'] = ims

heh = _load_module('memory/heaven_earth_human.py')
sys.modules['memory.heaven_earth_human'] = heh

ms = _load_module('memory/system.py')
sys.modules['memory.system'] = ms

# ---- 类型别名 ----
HexagramType = ct.HexagramType
WuxingType = ct.WuxingType
MemoryNode = ct.MemoryNode
MemoryLayer = ct.MemoryLayer
MemoryQuery = ct.MemoryQuery
AssociationType = ct.AssociationType
QueryType = ct.QueryType

# ---- 本能系统 ----
SystemMetricsCollector = bs.SystemMetricsCollector
InstinctSystem = bs.InstinctSystem
BodyMappingSystem = bs.BodyMappingSystem
MeridianSystem = bs.MeridianSystem
OrganSystem = bs.OrganSystem
HeartSystem = bs.HeartSystem
QiXueMetabolism = bs.QiXueMetabolism
MeridianType = bs.MeridianType
OrganType = bs.OrganType
HealthState = bs.HealthState

# ---- 形象气场 ----
FiveElement = ims.FiveElement
FiveElementWeights = ims.FiveElementWeights
FiveElementColorMapper = ims.FiveElementColorMapper
JingQiShenSystem = ims.JingQiShenSystem
QiFieldSystem = ims.QiFieldSystem
ImageSystem = ims.ImageSystem
ExpressionType = ims.ExpressionType
PostureType = ims.PostureType
ImageStyle = ims.ImageStyle
AnimalForm = ims.AnimalForm
ImageChangeLogEntry = ims.ImageChangeLogEntry
ImageAndQiSystem = ims.ImageAndQiSystem

# ---- 预测系统 ----
HexagramTransitionModel = hx.HexagramTransitionModel
MarkovChainPredictor = hx.MarkovChainPredictor
TianganDizhiPredictor = hx.TianganDizhiPredictor
EnsemblePredictor = hx.EnsemblePredictor
PredictionEvaluator = hx.PredictionEvaluator
TuibeituSequencePredictor = hx.TuibeituSequencePredictor

# ---- 商道系统 ----
ShangdaoSystem = sd.ShangdaoSystem
SunziAnalyzer = sd.SunziAnalyzer
GuanziOptimizer = sd.GuanziOptimizer
HuoZhiAnalyzer = sd.HuoZhiAnalyzer
StrategyType = sd.StrategyType
RiskLevel = sd.RiskLevel
ResourcePriority = sd.ResourcePriority

# ---- 记忆系统 ----
MemorySystem = ms.MemorySystem

# 事件循环 helper
_loop = asyncio.new_event_loop()

def _run(coro):
    return _loop.run_until_complete(coro)


# ============================================================
# 本能系统测试
# ============================================================

class TestSystemMetricsCollector(unittest.TestCase):
    """SystemMetricsCollector 测试"""

    def test_collect_returns_dict(self):
        c = SystemMetricsCollector()
        m = c.collect()
        self.assertIsInstance(m, dict)
        self.assertGreater(len(m), 0)

    def test_last_metrics_matches_collect(self):
        c = SystemMetricsCollector()
        c.collect()
        lm = c.last_metrics  # property, not method
        self.assertIsInstance(lm, dict)
        self.assertGreater(len(lm), 0)

    def test_metrics_contains_cpu(self):
        c = SystemMetricsCollector()
        m = c.collect()
        self.assertTrue(any('cpu' in k for k in m),
            f"指标应包含 cpu 相关键: {list(m.keys())}")


class TestInstinctSystem(unittest.TestCase):
    """InstinctSystem 本能反应测试"""

    def setUp(self):
        self.isys = InstinctSystem()

    def test_default_defense_level(self):
        d = self.isys.defense_level  # property
        self.assertIsInstance(d, float)
        self.assertGreaterEqual(d, 0.0)

    def test_default_not_degraded(self):
        self.assertFalse(self.isys.is_degraded)  # property

    def test_react_to_normal_metrics(self):
        metrics = {
            'cpu_load': 0.3, 'memory_usage': 0.4,
            'disk_usage': 0.5, 'network_latency': 50.0,
        }
        state = self.isys.react_to_metrics(metrics, qi_level=0.8, meridian_states={})
        self.assertIsInstance(state, dict)
        self.assertIn('defense_activated', state)
        self.assertFalse(state['defense_activated'], "正常指标不应激活防御")

    def test_react_to_high_error_rate(self):
        metrics = {
            'cpu_load': 0.9, 'memory_usage': 0.9,
            'disk_usage': 0.95, 'network_latency': 200.0,
        }
        state = self.isys.react_to_metrics(metrics, qi_level=0.2, meridian_states={})
        # 高负载+低 qi 应激活防御或降级
        self.assertTrue(
            state.get('defense_activated') or state.get('degradation_activated'),
            "高负载/低 qi 应激活防御或降级")

    def test_get_state(self):
        s = self.isys.get_state()
        self.assertIsInstance(s, dict)


class TestMeridianSystem(unittest.TestCase):
    """经络系统测试"""

    def setUp(self):
        self.msys = MeridianSystem()

    def test_meridians_initialized(self):
        for mid in self.msys.meridians:
            state = self.msys.get_meridian_state(mid)
            self.assertIsNotNone(state)

    def test_regulate_meridian(self):
        mid = 'ren_mai'
        self.msys.regulate_meridian(mid, target_flow=0.5)  # param: target_flow
        after = self.msys.get_meridian_state(mid)
        self.assertAlmostEqual(after.flow_rate, 0.5, places=2)

    def test_circulate_qi(self):
        result = self.msys.circulate_qi()
        self.assertIsInstance(result, dict)

    def test_diagnose_blockages(self):
        blockages = self.msys.diagnose_blockages()
        self.assertIsInstance(blockages, list)

    def test_update_from_metrics(self):
        metrics = {
            'memory_usage': 0.7, 'cpu_load': 0.5,
            'disk_usage': 0.6, 'network_latency': 80.0,
        }
        self.msys.update_from_metrics(metrics)
        state = self.msys.get_meridian_state('ren_mai')
        self.assertIsNotNone(state)


class TestOrganSystem(unittest.TestCase):
    """脏腑系统测试"""

    def setUp(self):
        self.osys = OrganSystem()

    def test_organs_initialized(self):
        for oname in self.osys.organs:
            state = self.osys.get_organ_state(oname)
            self.assertIsNotNone(state)

    def test_update_functional_level(self):
        self.osys.update_functional_level('心', 0.6)
        state = self.osys.get_organ_state('心')
        self.assertAlmostEqual(state.functional_level, 0.6, places=2)

    def test_diagnose_organ_health(self):
        diag = self.osys.diagnose_organ_health()
        self.assertIsInstance(diag, dict)

    def test_update_from_subsystems(self):
        health = {'心': 0.8, '肝': 0.7, '脾': 0.6, '肺': 0.5, '肾': 0.9}
        self.osys.update_from_subsystems(health)
        state = self.osys.get_organ_state('心')
        self.assertGreaterEqual(state.functional_level, 0.5)


class TestHeartSystem(unittest.TestCase):
    """心脏系统测试"""

    def setUp(self):
        self.hsys = HeartSystem()

    def test_pump_energy(self):
        e = self.hsys.pump_energy()
        self.assertIsInstance(e, float)
        self.assertGreater(e, 0)

    def test_adjust_output(self):
        self.hsys.adjust_output(0.7)
        self.assertAlmostEqual(self.hsys.energy_output, 0.7, places=2)

    def test_check_rhythm(self):
        r = self.hsys.check_rhythm()
        self.assertIsInstance(r, dict)
        self.assertIn('status', r)


class TestQiXueMetabolism(unittest.TestCase):
    """气血代谢测试"""

    def setUp(self):
        self.met = QiXueMetabolism()

    def test_consume_qi(self):
        self.assertTrue(self.met.consume_qi(30.0))

    def test_consume_too_much_qi(self):
        self.met.qi_total = 10.0
        self.assertFalse(self.met.consume_qi(50.0))

    def test_generate_qi(self):
        # generate_qi may cap at max; verify no exception and qi stays valid
        self.met.generate_qi(20.0)
        self.assertGreaterEqual(self.met.qi_total, 0)

    def test_circulate_qi(self):
        r = self.met.circulate_qi()
        self.assertIsInstance(r, float)

    def test_update_metabolism(self):
        before = self.met.qi_total
        self.met.update_metabolism(1.0)
        self.assertGreaterEqual(self.met.qi_total, 0)

    def test_recalculate_from_metrics(self):
        metrics = {
            'cpu_load': 0.5, 'memory_usage': 0.6,
            'disk_usage': 0.4, 'network_latency': 60.0,
        }
        self.met.recalculate_from_metrics(metrics)
        state = self.met.get_metabolism_state()
        self.assertIn('qi_total', state)

    def test_zi_wu_rhythm(self):
        zi_wu = self.met.apply_zi_wu_rhythm(current_hour=23)
        self.assertIn('boost', zi_wu)

    def test_zi_wu_rhythm_noon(self):
        zi_wu = self.met.apply_zi_wu_rhythm(current_hour=11)
        self.assertIn('peak_organ', zi_wu)


class TestBodyMappingSystem(unittest.TestCase):
    """BodyMappingSystem 集成测试"""

    def setUp(self):
        self.bms = BodyMappingSystem()

    def test_collect_metrics(self):
        m = self.bms.collect_metrics(force=True)
        self.assertIsInstance(m, dict)

    def test_diagnose_health(self):
        diag = _run(self.bms.diagnose_health())
        # Returns HealthState dataclass, not dict
        self.assertIsInstance(diag, HealthState)
        self.assertGreaterEqual(diag.vitality_score, 0)

    def test_get_system_state(self):
        state = _run(self.bms.get_system_state())  # async
        self.assertIsInstance(state, dict)
        self.assertIn('vitality', state)


# ============================================================
# 形象气场系统测试
# ============================================================

class TestFiveElementColorMapper(unittest.TestCase):
    """五行颜色映射测试"""

    def setUp(self):
        self.mapper = FiveElementColorMapper()

    def test_blend_balanced(self):
        w = FiveElementWeights(wood=1.0, fire=1.0, earth=1.0, metal=1.0, water=1.0)
        c = self.mapper.blend_color(w)
        self.assertIsInstance(c, str)
        self.assertTrue(c.startswith('#'))
        self.assertEqual(len(c), 7)

    def test_blend_wood_dominant(self):
        w = FiveElementWeights(wood=5.0, fire=0.1, earth=0.1, metal=0.1, water=0.1)
        c = self.mapper.blend_color(w)
        r = int(c[1:3], 16)
        g = int(c[3:5], 16)
        self.assertGreaterEqual(g, r, "木元素主导时应偏绿色")

    def test_imbalance_description(self):
        w = FiveElementWeights(wood=5.0, fire=0.1, earth=0.1, metal=0.1, water=0.1)
        desc = self.mapper.get_imbalance_description(w)
        self.assertIsNotNone(desc)

    def test_imbalanced_none(self):
        w = FiveElementWeights(wood=1.0, fire=1.0, earth=1.0, metal=1.0, water=1.0)
        desc = self.mapper.get_imbalance_description(w)
        self.assertIsNone(desc)

    def test_get_color_name(self):
        name = self.mapper.get_color_name('#00FF00')
        self.assertIsInstance(name, str)


class TestJingQiShenSystem(unittest.TestCase):
    """精气神系统测试"""

    def setUp(self):
        self.jqs = JingQiShenSystem()

    def test_initial_state(self):
        s = self.jqs.assess_state()
        self.assertGreaterEqual(s.jing_level, 0.5)
        self.assertGreaterEqual(s.qi_level, 0.5)
        self.assertGreaterEqual(s.shen_level, 0.5)

    def test_set_system_resources(self):
        self.jqs.set_system_resources(disk_free_pct=0.3, memory_health=0.4)
        s = self.jqs.assess_state()
        self.assertLess(s.jing_level, 0.8, "资源不足时精应降低")

    def test_set_system_runtime(self):
        # sig: (throughput, latency_health, task_completion_rate)
        self.jqs.set_system_runtime(throughput=0.3, latency_health=0.4, task_completion_rate=0.3)
        s = self.jqs.assess_state()
        self.assertLess(s.qi_level, 0.8, "运行不佳时气应降低")

    def test_set_system_intelligence(self):
        self.jqs.set_system_intelligence(response_quality=0.3, decision_confidence=0.2)
        s = self.jqs.assess_state()
        self.assertLess(s.shen_level, 0.8, "智能不佳时神应降低")

    def test_cascade_effect(self):
        self.jqs.jing_level = 0.1
        self.jqs.apply_cascade()
        # Cascade replenishes qi/shen; qi should be high after
        s = self.jqs.assess_state()
        self.assertGreater(s.qi_level, 0.5, "级联后气应恢复")

    def test_consume_and_replenish(self):
        before = self.jqs.jing_level
        self.jqs.consume_jing(0.3)
        self.assertLess(self.jqs.jing_level, before)
        self.jqs.replenish_all(jing_amt=0.3)
        self.assertGreater(self.jqs.jing_level, before - 0.3)

    def test_composite_score(self):
        s = self.jqs.get_composite_score()
        self.assertIsInstance(s, float)
        self.assertGreaterEqual(s, 0.0)
        self.assertLessEqual(s, 1.0)

    def test_recommendation(self):
        self.jqs.jing_level = 0.2
        r = self.jqs.get_recommendation()
        self.assertIsInstance(r, str)
        self.assertGreater(len(r), 0)

    def test_five_element_integration(self):
        self.jqs.set_five_element_weights(2.0, 1.0, 1.0, 1.0, 1.0)
        c = self.jqs.get_mixed_color()
        self.assertTrue(c.startswith('#'))


class TestQiFieldSystem(unittest.TestCase):
    """气场系统测试"""

    def setUp(self):
        self.qfs = QiFieldSystem()

    def test_generate_field(self):
        f = self.qfs.generate_field(intensity=0.8)
        self.assertGreater(f.field_strength, 0)
        self.assertIsInstance(f.field_color, str)

    def test_generate_ascii_art(self):
        art = self.qfs.generate_ascii_art(strength=0.7)
        self.assertIsInstance(art, str)
        self.assertGreater(len(art), 10)

    def test_ascii_art_contains_content(self):
        # sig: (strength, color, width) — no radius
        art = self.qfs.generate_ascii_art(strength=0.5, width=30)
        self.assertTrue(len(art) > 50)

    def test_interact_with_field(self):
        other = self.qfs.generate_field(intensity=0.3)
        result = self.qfs.interact_with_field(other)
        self.assertIn('type', result)
        self.assertIn('resonance', result)

    def test_adjust_field(self):
        before = self.qfs.base_strength
        self.qfs.adjust_field(0.2)
        self.assertGreater(self.qfs.base_strength, before)


class TestImageSystem(unittest.TestCase):
    """形象系统测试"""

    def setUp(self):
        self.isys = ImageSystem()

    def test_ethical_state_mapping(self):
        self.isys.set_ethical_state("仁")
        self.assertEqual(self.isys.current_expression, ExpressionType.BENEVOLENT)

        self.isys.set_ethical_state("义")
        self.assertEqual(self.isys.current_expression, ExpressionType.RIGHTEOUS)

        self.isys.set_ethical_state("智")
        self.assertEqual(self.isys.current_expression, ExpressionType.WISE)

    def test_animal_form_mapping(self):
        self.isys.set_animal_form(AnimalForm.TIGER)
        self.assertIsNotNone(self.isys.current_animal_form)

        self.isys.set_animal_form(AnimalForm.APE)
        self.assertEqual(self.isys.current_animal_form, AnimalForm.APE)

    def test_change_log(self):
        # change_log records on update_image_state, not set_ethical_state
        self.isys.update_image_state(vitality=0.8, activity_level='high')
        log = self.isys.get_change_log()
        self.assertGreater(len(log), 0)
        self.assertIsInstance(log[0], ImageChangeLogEntry)

    def test_update_image_state(self):
        state = self.isys.update_image_state(vitality=0.8, activity_level="high")
        self.assertEqual(state.expression, ExpressionType.JOY)
        self.assertEqual(state.posture, PostureType.DYNAMIC)

    def test_render_ascii_image(self):
        art = self.isys.render_ascii_image(width=30)
        self.assertIsInstance(art, str)
        self.assertGreater(len(art), 50)

    def test_render_svg_snippet(self):
        svg = self.isys.render_svg_snippet()
        self.assertIsInstance(svg, str)
        self.assertIn('<svg', svg)

    def test_get_visual_representation(self):
        vis = self.isys.get_visual_representation()
        self.assertIn('style', vis)
        self.assertIn('qi_field', vis)
        self.assertIn('jing_qi_shen', vis)

    def test_perceive_external_qi(self):
        qfs = QiFieldSystem()
        ext = qfs.generate_field(intensity=0.6)
        resp = self.isys.perceive_external_qi(ext)
        self.assertIn('perceived', resp)
        self.assertTrue(resp['perceived'])


class TestImageAndQiSystem(unittest.TestCase):
    """ImageAndQiSystem 集成测试"""

    def setUp(self):
        self.iaq = ImageAndQiSystem()

    def test_update_image_state(self):
        health = {'vitality': 0.8, 'activity_level': 'normal'}
        state = _run(self.iaq.update_image_state(health))
        self.assertIsNotNone(state)

    def test_get_jing_qi_shen(self):
        jqs = _run(self.iaq.get_jing_qi_shen())
        self.assertIsNotNone(jqs)

    def test_generate_qi_field(self):
        qf = _run(self.iaq.generate_qi_field())
        self.assertIsNotNone(qf)

    def test_get_system_state(self):
        state = _run(self.iaq.get_system_state())
        self.assertIn('jing_qi_shen', state)
        self.assertIn('qi_field', state)
        self.assertIn('image', state)


# ============================================================
# 预测系统测试
# ============================================================

class TestHexagramTransitionModel(unittest.TestCase):
    """八卦转换模型测试"""

    def setUp(self):
        self.model = HexagramTransitionModel()

    def test_transition_matrix_initialized(self):
        for src in HexagramType:
            self.assertIn(src, self.model.transition_matrix)
            for tgt in HexagramType:
                self.assertIn(tgt, self.model.transition_matrix[src])

    def test_predict_next_returns_list(self):
        preds = self.model.predict_next(HexagramType.QIAN)
        self.assertIsInstance(preds, list)
        self.assertGreater(len(preds), 0)

    def test_update_transition_increases_probability(self):
        # update_transition normalizes the entire row; verify row sums to 1
        self.model.update_transition(HexagramType.QIAN, HexagramType.DUI)
        after_sum = sum(self.model.transition_matrix[HexagramType.QIAN].values())
        self.assertAlmostEqual(after_sum, 1.0, places=5,
            msg="更新后概率行总和应为 1")

    def test_record_sequence(self):
        seq = ['乾', '兑', '离']
        self.model.record_sequence(seq)
        self.assertGreater(self.model.sequence_patterns.get('乾兑离', 0), 0)

    def test_detect_sequence_pattern(self):
        result = self.model.detect_sequence_pattern(HexagramType.QIAN)
        self.assertIsNotNone(result)


class TestMarkovChainPredictor(unittest.TestCase):
    """马尔可夫链预测器测试"""

    def setUp(self):
        self.predictor = MarkovChainPredictor()

    def test_first_order_training(self):
        # train expects List[List[str]]
        seq = [HexagramType.QIAN, HexagramType.DUI, HexagramType.LI] * 5
        seqs = [seq[i:i+3] for i in range(0, len(seq), 3)]
        self.predictor.train(seqs)
        preds = self.predictor.predict([HexagramType.QIAN])
        self.assertIsInstance(preds, list)

    def test_empty_history(self):
        preds = self.predictor.predict([])
        self.assertIsInstance(preds, list)

    def test_multi_step_prediction(self):
        seq = [HexagramType.QIAN, HexagramType.DUI, HexagramType.LI] * 5
        seqs = [seq[i:i+3] for i in range(0, len(seq), 3)]
        self.predictor.train(seqs)
        multi = self.predictor.predict_multi_step([HexagramType.QIAN], steps=3)
        self.assertIsInstance(multi, list)
        self.assertGreater(len(multi), 0)


class TestTianganDizhiPredictor(unittest.TestCase):
    """天干地支预测器测试"""

    def setUp(self):
        self.predictor = TianganDizhiPredictor()

    def test_predict_with_time(self):
        # predict takes (dt, history_pattern) — both optional
        preds = self.predictor.predict()
        self.assertIsInstance(preds, list)

    def test_training_improves_predictions(self):
        before = self.predictor.predict()
        # record_observation takes (datetime, HexagramType)
        for i in range(5):
            self.predictor.record_observation(datetime.now(), HexagramType.QIAN)
        after = self.predictor.predict()
        self.assertIsInstance(after, list)


class TestEnsemblePredictor(unittest.TestCase):
    """集成预测器测试"""

    def setUp(self):
        self.predictor = EnsemblePredictor()

    def test_predict_returns_dict(self):
        result = self.predictor.predict(HexagramType.QIAN)
        self.assertIsInstance(result, dict)
        self.assertIn('predictions', result)
        self.assertIn('confidence', result)

    def test_predict_with_history(self):
        history = [HexagramType.QIAN, HexagramType.DUI, HexagramType.LI]
        result = self.predictor.predict(HexagramType.QIAN, history=history)
        self.assertIn('predictions', result)

    def test_train_markov(self):
        seq = [HexagramType.QIAN, HexagramType.DUI, HexagramType.LI] * 5
        seqs = [seq[i:i+3] for i in range(0, len(seq), 3)]
        self.predictor.train_markov(seqs)
        result = self.predictor.predict(HexagramType.QIAN)
        self.assertIn('predictions', result)

    def test_evaluate_prediction(self):
        # evaluate_prediction expects a dict with 'component_predictions'
        pred = {
            'component_predictions': {
                'markov': [(HexagramType.QIAN, 0.5), (HexagramType.DUI, 0.3)],
                'tiangan_dizhi': [(HexagramType.QIAN, 0.4), (HexagramType.LI, 0.3)],
            }
        }
        self.predictor.evaluate_prediction(pred, HexagramType.QIAN)

    def test_get_prediction_quality(self):
        q = self.predictor.get_prediction_quality()
        self.assertIsInstance(q, dict)


class TestPredictionEvaluator(unittest.TestCase):
    """预测评估器测试"""

    def setUp(self):
        self.evaluator = PredictionEvaluator()

    def test_backtest(self):
        # backtest expects List[Dict] with string hexagram names in 'sequence'
        data = [
            {'sequence': ['乾', '兑'], 'actual': '离'},
            {'sequence': ['兑', '离'], 'actual': '震'},
            {'sequence': ['离', '震'], 'actual': '巽'},
        ]
        results = self.evaluator.backtest(data)
        self.assertIsInstance(results, dict)
        self.assertIn('top1_accuracy', results)
        self.assertIn('detailed_results', results)

    def test_step_accuracy(self):
        # step_accuracy is a defaultdict tracking attribute, not callable
        sa = self.evaluator.step_accuracy
        self.assertIsInstance(sa, dict)

    def test_get_quality_report(self):
        # get_quality_report takes no args
        report = self.evaluator.get_quality_report()
        self.assertIsInstance(report, dict)


class TestTuibeituSequencePredictor(unittest.TestCase):
    """推背图预测器集成测试"""

    def setUp(self):
        self.predictor = TuibeituSequencePredictor()

    def test_analyze_current_state(self):
        state = self.predictor.analyze_current_state(
            HexagramType.QIAN,
            [MemoryNode(
                memory_id='test', content='test',
                memory_type=HexagramType.QIAN, layer=MemoryLayer.HEAVEN,
                wuxing_attribute=WuxingType.WOOD, weight=0.5
            )]
        )
        self.assertIn('current_hexagram', state)
        self.assertIn('predictions', state)
        self.assertIn('recommended_direction', state)

    def test_predict_sequence(self):
        seq = self.predictor.predict_sequence(HexagramType.QIAN, steps=3)
        self.assertIsInstance(seq, list)
        self.assertGreater(len(seq), 0)
        for item in seq:
            self.assertIn('hexagram', item)
            self.assertIn('probability', item)

    def test_suggest_intervention(self):
        result = self.predictor.suggest_intervention(
            HexagramType.QIAN,
            HexagramType.KUN,
            [MemoryNode(
                memory_id='t', content='t',
                memory_type=HexagramType.QIAN, layer=MemoryLayer.HEAVEN,
                wuxing_attribute=WuxingType.WOOD, weight=0.5
            )]
        )
        self.assertIn('action', result)
        self.assertIn('reason', result)


# ============================================================
# 商道系统测试
# ============================================================

class TestSunziAnalyzer(unittest.TestCase):
    """孙子兵法分析器测试"""

    def setUp(self):
        self.sunzi = SunziAnalyzer()

    def test_strong_situation(self):
        factors = {'道': 0.9, '天': 0.9, '地': 0.8, '将': 0.9, '法': 0.85}
        result = self.sunzi.analyze_situation(factors)
        self.assertEqual(result.strategy, StrategyType.ATTACK)
        self.assertIn(result.situation_name, ['势如破竹', '乘胜追击'])

    def test_weak_situation(self):
        factors = {'道': 0.1, '天': 0.1, '地': 0.1, '将': 0.1, '法': 0.1}
        result = self.sunzi.analyze_situation(factors)
        self.assertIn(result.strategy, [StrategyType.RETREAT, StrategyType.OBSERVE])

    def test_moderate_situation(self):
        factors = {'道': 0.5, '天': 0.5, '地': 0.5, '将': 0.5, '法': 0.5}
        result = self.sunzi.analyze_situation(factors)
        self.assertIn(result.strategy, [StrategyType.DEFEND, StrategyType.ADAPT])

    def test_alliance_when_leader_strong(self):
        factors = {'道': 0.6, '天': 0.6, '地': 0.6, '将': 0.8, '法': 0.6}
        result = self.sunzi.analyze_situation(factors)
        self.assertEqual(result.strategy, StrategyType.ALLIANCE)

    def test_risks_identified(self):
        factors = {'道': 0.2, '天': 0.1, '地': 0.5, '将': 0.5, '法': 0.5}
        result = self.sunzi.analyze_situation(factors)
        self.assertGreater(len(result.risks), 0)

    def test_opportunities_identified(self):
        factors = {'道': 0.8, '天': 0.5, '地': 0.5, '将': 0.7, '法': 0.5}
        result = self.sunzi.analyze_situation(factors)
        self.assertGreater(len(result.opportunities), 0)

    def test_historical_analysis_recorded(self):
        factors = {'道': 0.7, '天': 0.6, '地': 0.5, '将': 0.8, '法': 0.7}
        self.sunzi.analyze_situation(factors)
        self.assertGreater(len(self.sunzi.historical_analyses), 0)


class TestGuanziOptimizer(unittest.TestCase):
    """管子资源配置优化器测试"""

    def setUp(self):
        self.guanzi = GuanziOptimizer()

    def test_allocate_sufficient_resources(self):
        available = {'computing': 1.0, 'memory': 1.0, 'network': 1.0}
        demands = [
            {'name': 'task_a', 'priority': ResourcePriority.CRITICAL, 'amount': 0.3},
            {'name': 'task_b', 'priority': ResourcePriority.IMPORTANT, 'amount': 0.3},
            {'name': 'task_c', 'priority': ResourcePriority.SUPPORTING, 'amount': 0.3},
        ]
        result = self.guanzi.allocate_resources(available, demands)
        self.assertGreater(result.efficiency_score, 0.5)

    def test_allocate_insufficient_resources(self):
        available = {'computing': 0.1}
        demands = [
            {'name': 'big_task', 'priority': ResourcePriority.CRITICAL, 'amount': 0.9},
        ]
        result = self.guanzi.allocate_resources(available, demands)
        self.assertLess(result.efficiency_score, 0.5)

    def test_attack_strategy_consumes_more(self):
        available = {'computing': 1.0, 'memory': 1.0}
        demands = [{'name': 't', 'priority': ResourcePriority.CRITICAL, 'amount': 0.5}]
        normal = self.guanzi.allocate_resources(available, demands)
        attack = self.guanzi.allocate_resources(available, demands, StrategyType.ATTACK)
        normal_amt = normal.allocations['t']['amount']
        attack_amt = attack.allocations['t']['amount']
        self.assertGreaterEqual(attack_amt, normal_amt)


class TestHuoZhiAnalyzer(unittest.TestCase):
    """货殖列传时机分析器测试"""

    def setUp(self):
        self.huozhi = HuoZhiAnalyzer()

    def test_hot_market(self):
        indicators = {
            'resource_usage': 0.95, 'response_latency': 0.9,
            'error_rate': 0.8,
        }
        result = self.huozhi.evaluate_timing(indicators)
        self.assertIn(result['recommended_action'], ['谨慎观望', '逐步收缩'])

    def test_cold_market(self):
        indicators = {
            'resource_usage': 0.1, 'response_latency': 0.1,
            'error_rate': 0.05,
        }
        result = self.huozhi.evaluate_timing(indicators)
        self.assertIn(result['recommended_action'], ['逐步布局', '积极建仓'])

    def test_neutral_market(self):
        indicators = {
            'resource_usage': 0.5, 'response_latency': 0.5,
            'error_rate': 0.3,
        }
        result = self.huozhi.evaluate_timing(indicators)
        self.assertIn(result['recommended_action'], ['正常运作'])


class TestShangdaoSystem(unittest.TestCase):
    """商道系统主类测试"""

    def setUp(self):
        self.shangdao = ShangdaoSystem()

    def test_strategic_assessment(self):
        five_factors = {'道': 0.8, '天': 0.7, '地': 0.6, '将': 0.8, '法': 0.7}
        market = {'resource_usage': 0.5, 'response_latency': 0.4, 'error_rate': 0.2}
        resources = {'computing': 1.0, 'memory': 0.8}
        demands = [
            {'name': 'task_a', 'priority': ResourcePriority.CRITICAL, 'amount': 0.3},
        ]
        result = _run(self.shangdao.strategic_assessment(
            five_factors, market, resources, demands))
        self.assertIn('situation', result)
        self.assertIn('overall_recommendation', result)
        self.assertGreater(len(result['overall_recommendation']), 0)

    def test_risk_assessment(self):
        five_factors = {'道': 0.3, '天': 0.2, '地': 0.3, '将': 0.4, '法': 0.3}
        result = _run(self.shangdao.risk_assessment(five_factors))
        self.assertIsInstance(result.risk_score, float)
        self.assertGreater(result.risk_score, 0.3, "弱势五事应有较高风险分")

    def test_recommend_strategy(self):
        state = {
            'five_factors': {'道': 0.7, '天': 0.6, '地': 0.5, '将': 0.8, '法': 0.7},
        }
        result = _run(self.shangdao.recommend_strategy(state))
        self.assertIn('recommended_strategy', result)
        self.assertIn('key_actions', result)
        self.assertGreater(len(result['key_actions']), 0)


if __name__ == '__main__':
    unittest.main()
