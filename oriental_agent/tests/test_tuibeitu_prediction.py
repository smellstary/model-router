"""
Unit tests for Tuibeitu Prediction Module
推背图序列预测模块单元测试
"""

import unittest
import sys
import os
import importlib.util

_test_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_test_dir, '..'))

_prediction_path = os.path.join(_project_root, "prediction", "tuibeitu_prediction.py")
_spec = importlib.util.spec_from_file_location("tuibeitu_prediction", _prediction_path)
tuibeitu_module = importlib.util.module_from_spec(_spec)
sys.modules["tuibeitu_prediction"] = tuibeitu_module
_spec.loader.exec_module(tuibeitu_module)

TuibeituImage = tuibeitu_module.TuibeituImage
SequenceEvolver = tuibeitu_module.SequenceEvolver
TuibeituPredictor = tuibeitu_module.TuibeituPredictor
GuaSymbol = tuibeitu_module.GuaSymbol
EvolutionDirection = tuibeitu_module.EvolutionDirection
TimeHint = tuibeitu_module.TimeHint
PredictionResult = tuibeitu_module.PredictionResult
SequenceAnalysis = tuibeitu_module.SequenceAnalysis

WuxingType = tuibeitu_module.WuxingType
HexagramType = tuibeitu_module.HexagramType
TianganType = tuibeitu_module.TianganType
DizhiType = tuibeitu_module.DizhiType


class TestGuaSymbol(unittest.TestCase):
    """测试六十四卦符号枚举"""

    def test_gua_symbol_count(self):
        self.assertEqual(len(list(GuaSymbol)), 64)

    def test_gua_symbol_values(self):
        self.assertEqual(GuaSymbol.QIAN_QIAN.value, "乾为天")
        self.assertEqual(GuaSymbol.KUN_KUN.value, "坤为地")
        self.assertEqual(GuaSymbol.KAN_KAN.value, "坎为水")
        self.assertEqual(GuaSymbol.LI_LI.value, "离为火")

    def test_gua_symbol_uniqueness(self):
        values = [gua.value for gua in GuaSymbol]
        self.assertEqual(len(values), len(set(values)))


class TestEvolutionDirection(unittest.TestCase):
    """测试演化方向枚举"""

    def test_evolution_directions_count(self):
        self.assertEqual(len(list(EvolutionDirection)), 6)

    def test_evolution_direction_values(self):
        self.assertEqual(EvolutionDirection.SHENG.value, "相生演化")
        self.assertEqual(EvolutionDirection.KE.value, "相克演化")
        self.assertEqual(EvolutionDirection.SHUN.value, "顺演化")
        self.assertEqual(EvolutionDirection.NI.value, "逆演化")


class TestTimeHint(unittest.TestCase):
    """测试时间暗示数据结构"""

    def test_time_hint_creation(self):
        hint = TimeHint(
            ganzhi_cycle="甲子",
            dynasty_hint="唐朝",
            year_hint="贞观年间",
            confidence=0.8
        )
        self.assertEqual(hint.ganzhi_cycle, "甲子")
        self.assertEqual(hint.dynasty_hint, "唐朝")
        self.assertEqual(hint.confidence, 0.8)

    def test_time_hint_default_values(self):
        hint = TimeHint()
        self.assertIsNone(hint.ganzhi_cycle)
        self.assertEqual(hint.confidence, 0.5)

    def test_time_hint_to_dict(self):
        hint = TimeHint(ganzhi_cycle="乙丑", confidence=0.7)
        result = hint.to_dict()
        self.assertIn('ganzhi_cycle', result)
        self.assertEqual(result['ganzhi_cycle'], "乙丑")


class TestTuibeituImage(unittest.TestCase):
    """测试推背图象数据结构"""

    def test_image_creation(self):
        image = TuibeituImage(
            image_number=1,
            gua_symbol=GuaSymbol.QIAN_QIAN,
            chen_yu="谶语测试",
            song_yue="颂曰测试",
            wuxing_attribution=WuxingType.WOOD
        )
        self.assertEqual(image.image_number, 1)
        self.assertEqual(image.gua_symbol, GuaSymbol.QIAN_QIAN)
        self.assertEqual(image.wuxing_attribution, WuxingType.WOOD)

    def test_image_number_validation_lower(self):
        with self.assertRaises(ValueError):
            TuibeituImage(
                image_number=0,
                gua_symbol=GuaSymbol.QIAN_QIAN,
                chen_yu="test",
                song_yue="test",
                wuxing_attribution=WuxingType.WOOD
            )

    def test_image_number_validation_upper(self):
        with self.assertRaises(ValueError):
            TuibeituImage(
                image_number=61,
                gua_symbol=GuaSymbol.QIAN_QIAN,
                chen_yu="test",
                song_yue="test",
                wuxing_attribution=WuxingType.WOOD
            )

    def test_image_valid_boundaries(self):
        image_1 = TuibeituImage(
            image_number=1,
            gua_symbol=GuaSymbol.QIAN_QIAN,
            chen_yu="test",
            song_yue="test",
            wuxing_attribution=WuxingType.WOOD
        )
        self.assertEqual(image_1.image_number, 1)

        image_60 = TuibeituImage(
            image_number=60,
            gua_symbol=GuaSymbol.HUO_SHUI_WEI_JI,
            chen_yu="test",
            song_yue="test",
            wuxing_attribution=WuxingType.WATER
        )
        self.assertEqual(image_60.image_number, 60)

    def test_get_ganzhi_mapping(self):
        image_1 = TuibeituImage(
            image_number=1,
            gua_symbol=GuaSymbol.QIAN_QIAN,
            chen_yu="test",
            song_yue="test",
            wuxing_attribution=WuxingType.WOOD
        )
        tiangan, dizhi = image_1.get_ganzhi_mapping()
        self.assertEqual(tiangan, TianganType.JIA)
        self.assertEqual(dizhi, DizhiType.ZI)

    def test_get_ganzhi_mapping_cycle(self):
        image_11 = TuibeituImage(
            image_number=11,
            gua_symbol=GuaSymbol.DI_TIAN_TAI,
            chen_yu="test",
            song_yue="test",
            wuxing_attribution=WuxingType.EARTH
        )
        tiangan, dizhi = image_11.get_ganzhi_mapping()
        self.assertEqual(tiangan, TianganType.JIA)
        self.assertEqual(dizhi, DizhiType.XU)

    def test_get_wuxing_energy(self):
        image = TuibeituImage(
            image_number=1,
            gua_symbol=GuaSymbol.QIAN_QIAN,
            chen_yu="test",
            song_yue="test",
            wuxing_attribution=WuxingType.FIRE
        )
        energy = image.get_wuxing_energy()
        self.assertIn(WuxingType.FIRE, energy)
        self.assertGreater(energy[WuxingType.FIRE], 0.5)

    def test_to_dict(self):
        image = TuibeituImage(
            image_number=1,
            gua_symbol=GuaSymbol.QIAN_QIAN,
            chen_yu="谶语",
            song_yue="颂曰",
            wuxing_attribution=WuxingType.WOOD
        )
        result = image.to_dict()
        self.assertIn('image_number', result)
        self.assertIn('gua_symbol', result)
        self.assertIn('chen_yu', result)
        self.assertIn('song_yue', result)
        self.assertIn('wuxing_attribution', result)


class TestSequenceEvolver(unittest.TestCase):
    """测试序列演化器"""

    def setUp(self):
        self.evolver = SequenceEvolver()
        self.test_image = TuibeituImage(
            image_number=1,
            gua_symbol=GuaSymbol.QIAN_QIAN,
            chen_yu="test",
            song_yue="test",
            wuxing_attribution=WuxingType.WOOD
        )

    def test_evolver_initialization(self):
        self.assertIsNotNone(self.evolver.transition_matrix)
        self.assertEqual(len(self.evolver.transition_matrix), 64)

    def test_wuxing_generation_cycle(self):
        self.assertEqual(
            SequenceEvolver.WUXING_GENERATION[WuxingType.WOOD],
            WuxingType.FIRE
        )
        self.assertEqual(
            SequenceEvolver.WUXING_GENERATION[WuxingType.FIRE],
            WuxingType.EARTH
        )
        self.assertEqual(
            SequenceEvolver.WUXING_GENERATION[WuxingType.EARTH],
            WuxingType.METAL
        )
        self.assertEqual(
            SequenceEvolver.WUXING_GENERATION[WuxingType.METAL],
            WuxingType.WATER
        )
        self.assertEqual(
            SequenceEvolver.WUXING_GENERATION[WuxingType.WATER],
            WuxingType.WOOD
        )

    def test_wuxing_restriction_cycle(self):
        self.assertEqual(
            SequenceEvolver.WUXING_RESTRICTION[WuxingType.WOOD],
            WuxingType.EARTH
        )
        self.assertEqual(
            SequenceEvolver.WUXING_RESTRICTION[WuxingType.EARTH],
            WuxingType.WATER
        )
        self.assertEqual(
            SequenceEvolver.WUXING_RESTRICTION[WuxingType.WATER],
            WuxingType.FIRE
        )
        self.assertEqual(
            SequenceEvolver.WUXING_RESTRICTION[WuxingType.FIRE],
            WuxingType.METAL
        )
        self.assertEqual(
            SequenceEvolver.WUXING_RESTRICTION[WuxingType.METAL],
            WuxingType.WOOD
        )

    def test_evolve_by_wuxing_sheng(self):
        candidates = self.evolver.evolve_by_wuxing(
            self.test_image,
            EvolutionDirection.SHENG
        )
        self.assertGreater(len(candidates), 0)
        self.assertIsInstance(candidates[0], tuple)
        self.assertIsInstance(candidates[0][0], GuaSymbol)

    def test_evolve_by_wuxing_ke(self):
        candidates = self.evolver.evolve_by_wuxing(
            self.test_image,
            EvolutionDirection.KE
        )
        self.assertGreater(len(candidates), 0)

    def test_evolve_by_gua_transform(self):
        candidates = self.evolver.evolve_by_gua_transform(self.test_image)
        self.assertGreater(len(candidates), 0)
        self.assertLessEqual(len(candidates), 5)

    def test_evolve_by_ganzhi_cycle(self):
        candidates = self.evolver.evolve_by_ganzhi_cycle(self.test_image, steps=1)
        self.assertGreater(len(candidates), 0)
        for img_num, prob in candidates:
            self.assertGreaterEqual(img_num, 1)
            self.assertLessEqual(img_num, 60)

    def test_calculate_evolution_probability(self):
        image1 = TuibeituImage(
            image_number=1,
            gua_symbol=GuaSymbol.QIAN_QIAN,
            chen_yu="test",
            song_yue="test",
            wuxing_attribution=WuxingType.WOOD
        )
        image2 = TuibeituImage(
            image_number=2,
            gua_symbol=GuaSymbol.KUN_KUN,
            chen_yu="test",
            song_yue="test",
            wuxing_attribution=WuxingType.FIRE
        )
        prob = self.evolver.calculate_evolution_probability(image1, image2)
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)

    def test_record_evolution(self):
        record = {
            'from_image': 1,
            'to_image': 2,
            'from_wuxing': '木',
            'to_wuxing': '火'
        }
        initial_len = len(self.evolver.evolution_history)
        self.evolver.record_evolution(record)
        self.assertEqual(len(self.evolver.evolution_history), initial_len + 1)

    def test_get_evolution_patterns(self):
        for i in range(5):
            self.evolver.record_evolution({
                'from_wuxing': '木',
                'to_wuxing': '火'
            })
        patterns = self.evolver.get_evolution_patterns()
        self.assertIsInstance(patterns, list)


class TestTuibeituPredictor(unittest.TestCase):
    """测试推背图预测器"""

    def setUp(self):
        self.predictor = TuibeituPredictor()
        self.test_image = TuibeituImage(
            image_number=1,
            gua_symbol=GuaSymbol.QIAN_QIAN,
            chen_yu="test",
            song_yue="test",
            wuxing_attribution=WuxingType.WOOD
        )

    def test_predictor_initialization(self):
        self.assertIsNotNone(self.predictor.evolver)
        self.assertEqual(len(self.predictor.TUIBEITU_DATA), 60)

    def test_tuibeitu_data_structure(self):
        for i in range(1, 61):
            self.assertIn(i, self.predictor.TUIBEITU_DATA)
            data = self.predictor.TUIBEITU_DATA[i]
            self.assertIn('image_number', data)
            self.assertIn('tiangan', data)
            self.assertIn('dizhi', data)
            self.assertIn('gua_symbol', data)
            self.assertIn('wuxing', data)

    def test_predict_next(self):
        result = self.predictor.predict_next(self.test_image)
        self.assertIsInstance(result, PredictionResult)
        self.assertIsNotNone(result.predicted_image)
        self.assertGreater(result.confidence, 0)
        self.assertLessEqual(result.confidence, 1.0)

    def test_predict_next_with_context(self):
        context = {'preferred_wuxing': WuxingType.FIRE}
        result = self.predictor.predict_next(self.test_image, context)
        self.assertIsInstance(result, PredictionResult)

    def test_prediction_result_structure(self):
        result = self.predictor.predict_next(self.test_image)
        self.assertIsNotNone(result.predicted_image)
        self.assertIsNotNone(result.evolution_direction)
        self.assertIsNotNone(result.wuxing_factors)
        self.assertIsNotNone(result.reasoning)

    def test_analyze_sequence(self):
        sequence = [
            TuibeituImage(
                image_number=i,
                gua_symbol=GuaSymbol.QIAN_QIAN,
                chen_yu=f"test{i}",
                song_yue=f"test{i}",
                wuxing_attribution=WuxingType.WOOD
            )
            for i in range(1, 6)
        ]
        analysis = self.predictor.analyze_sequence(sequence)
        self.assertIsInstance(analysis, SequenceAnalysis)
        self.assertEqual(len(analysis.sequence), 5)

    def test_analyze_sequence_empty(self):
        with self.assertRaises(ValueError):
            self.predictor.analyze_sequence([])

    def test_analyze_sequence_wuxing_distribution(self):
        sequence = [
            TuibeituImage(
                image_number=1,
                gua_symbol=GuaSymbol.QIAN_QIAN,
                chen_yu="test",
                song_yue="test",
                wuxing_attribution=WuxingType.WOOD
            ),
            TuibeituImage(
                image_number=2,
                gua_symbol=GuaSymbol.KUN_KUN,
                chen_yu="test",
                song_yue="test",
                wuxing_attribution=WuxingType.WOOD
            ),
        ]
        analysis = self.predictor.analyze_sequence(sequence)
        self.assertEqual(analysis.dominant_wuxing, WuxingType.WOOD)

    def test_interpret_image(self):
        interpretation = self.predictor.interpret_image(1)
        self.assertIn('image_number', interpretation)
        self.assertIn('gua_symbol', interpretation)
        self.assertIn('ganzhi', interpretation)
        self.assertIn('wuxing', interpretation)

    def test_interpret_image_invalid_number(self):
        with self.assertRaises(ValueError):
            self.predictor.interpret_image(0)

    def test_interpret_image_invalid_upper(self):
        with self.assertRaises(ValueError):
            self.predictor.interpret_image(61)

    def test_get_prediction_statistics(self):
        for _ in range(3):
            self.predictor.predict_next(self.test_image)
        stats = self.predictor.get_prediction_statistics()
        self.assertEqual(stats['total_predictions'], 3)
        self.assertIn('average_confidence', stats)

    def test_clear_history(self):
        self.predictor.predict_next(self.test_image)
        self.predictor.clear_history()
        self.assertEqual(len(self.predictor.prediction_history), 0)


class TestPredictionResult(unittest.TestCase):
    """测试预测结果数据结构"""

    def test_prediction_result_creation(self):
        image = TuibeituImage(
            image_number=1,
            gua_symbol=GuaSymbol.QIAN_QIAN,
            chen_yu="test",
            song_yue="test",
            wuxing_attribution=WuxingType.WOOD
        )
        result = PredictionResult(
            predicted_image=image,
            confidence=0.8,
            evolution_direction=EvolutionDirection.SHENG,
            wuxing_factors={WuxingType.WOOD: 0.5},
            reasoning="test reasoning"
        )
        self.assertEqual(result.confidence, 0.8)
        self.assertEqual(result.evolution_direction, EvolutionDirection.SHENG)

    def test_prediction_result_to_dict(self):
        image = TuibeituImage(
            image_number=1,
            gua_symbol=GuaSymbol.QIAN_QIAN,
            chen_yu="test",
            song_yue="test",
            wuxing_attribution=WuxingType.WOOD
        )
        result = PredictionResult(
            predicted_image=image,
            confidence=0.8,
            evolution_direction=EvolutionDirection.SHENG,
            wuxing_factors={WuxingType.WOOD: 0.5},
            reasoning="test"
        )
        data = result.to_dict()
        self.assertIn('predicted_image', data)
        self.assertIn('confidence', data)
        self.assertIn('evolution_direction', data)


class TestSequenceAnalysis(unittest.TestCase):
    """测试序列分析结果"""

    def test_sequence_analysis_creation(self):
        sequence = [
            TuibeituImage(
                image_number=1,
                gua_symbol=GuaSymbol.QIAN_QIAN,
                chen_yu="test",
                song_yue="test",
                wuxing_attribution=WuxingType.WOOD
            )
        ]
        analysis = SequenceAnalysis(
            sequence=sequence,
            trend_direction="上升",
            dominant_wuxing=WuxingType.WOOD,
            wuxing_distribution={WuxingType.WOOD: 1.0},
            cycle_position=1,
            evolution_pattern="五行专一",
            stability_score=1.0
        )
        self.assertEqual(analysis.trend_direction, "上升")
        self.assertEqual(analysis.dominant_wuxing, WuxingType.WOOD)

    def test_sequence_analysis_to_dict(self):
        sequence = [
            TuibeituImage(
                image_number=1,
                gua_symbol=GuaSymbol.QIAN_QIAN,
                chen_yu="test",
                song_yue="test",
                wuxing_attribution=WuxingType.WOOD
            )
        ]
        analysis = SequenceAnalysis(
            sequence=sequence,
            trend_direction="稳定",
            dominant_wuxing=WuxingType.WOOD,
            wuxing_distribution={WuxingType.WOOD: 1.0},
            cycle_position=1,
            evolution_pattern="五行专一",
            stability_score=1.0
        )
        data = analysis.to_dict()
        self.assertIn('sequence', data)
        self.assertIn('trend_direction', data)
        self.assertIn('dominant_wuxing', data)


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_full_prediction_workflow(self):
        predictor = TuibeituPredictor()
        image = TuibeituImage(
            image_number=1,
            gua_symbol=GuaSymbol.QIAN_QIAN,
            chen_yu="第一象",
            song_yue="第一象颂曰",
            wuxing_attribution=WuxingType.WOOD
        )
        result = predictor.predict_next(image)
        self.assertIsNotNone(result.predicted_image)
        self.assertGreater(result.confidence, 0)

    def test_sequence_evolution_chain(self):
        evolver = SequenceEvolver()
        image = TuibeituImage(
            image_number=1,
            gua_symbol=GuaSymbol.QIAN_QIAN,
            chen_yu="test",
            song_yue="test",
            wuxing_attribution=WuxingType.WOOD
        )
        wuxing_results = evolver.evolve_by_wuxing(image)
        gua_results = evolver.evolve_by_gua_transform(image)
        ganzhi_results = evolver.evolve_by_ganzhi_cycle(image)
        self.assertGreater(len(wuxing_results), 0)
        self.assertGreater(len(gua_results), 0)
        self.assertGreater(len(ganzhi_results), 0)

    def test_sixty_cycle_completeness(self):
        predictor = TuibeituPredictor()
        for i in range(1, 61):
            data = predictor.TUIBEITU_DATA[i]
            self.assertIsNotNone(data['tiangan'])
            self.assertIsNotNone(data['dizhi'])
            self.assertIsNotNone(data['wuxing'])

    def test_prediction_history_tracking(self):
        predictor = TuibeituPredictor()
        image = TuibeituImage(
            image_number=1,
            gua_symbol=GuaSymbol.QIAN_QIAN,
            chen_yu="test",
            song_yue="test",
            wuxing_attribution=WuxingType.WOOD
        )
        for i in range(5):
            predictor.predict_next(image)
        self.assertEqual(len(predictor.prediction_history), 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
