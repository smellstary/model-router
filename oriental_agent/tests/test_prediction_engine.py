"""
Unit tests for Prediction Engine - 预测推理系统单元测试
"""

import pytest
from datetime import datetime
from prediction.prediction_engine import (
    PredictionEngine,
    YiJingEngine,
    MeihuaEngine,
    WuxingPredictionEngine,
    GanzhiTimeEngine,
    PredictionType,
    HexagramType,
    create_prediction_engine
)


class TestYiJingEngine:
    """测试易经卦象推演引擎"""
    
    def test_initialize(self):
        engine = YiJingEngine()
        
        assert engine.trigrams is not None
        assert len(engine.trigrams) == 8
    
    def test_generate_hexagram(self):
        engine = YiJingEngine()
        
        hexagram = engine.generate_hexagram(123)
        
        assert hexagram is not None
        assert hexagram.hexagram_type is not None
        assert hexagram.lower_trigram is not None
        assert hexagram.upper_trigram is not None
    
    def test_generate_multiple_hexagrams(self):
        engine = YiJingEngine()
        
        hexagrams = [engine.generate_hexagram(i) for i in range(10)]
        
        assert len(hexagrams) == 10
    
    def test_interpret_hexagram(self):
        engine = YiJingEngine()
        hexagram = engine.generate_hexagram(123)
        
        interpretation = engine.interpret_hexagram(hexagram)
        
        assert "name" in interpretation
        assert "element" in interpretation
        assert "interpretation" in interpretation
    
    def test_predict(self):
        engine = YiJingEngine()
        
        result = engine.predict("测试预测")
        
        assert result is not None
        assert result.prediction_type == PredictionType.YI_JING
        assert result.confidence > 0
        assert result.probability > 0


class TestMeihuaEngine:
    """测试梅花易数引擎"""
    
    def test_initialize(self):
        engine = MeihuaEngine()
        
        assert len(engine.prediction_history) == 0
    
    def test_analyze(self):
        engine = MeihuaEngine()
        
        result = engine.analyze("主体", "客体")
        
        assert result is not None
        assert result.prediction_type == PredictionType.MEIHUA
        assert "tiangan" in result.result
        assert "dizhi" in result.result
    
    def test_analyze_with_time(self):
        engine = MeihuaEngine()
        
        result = engine.analyze("A", "B", datetime.now())
        
        assert result is not None
        assert result.timestamp is not None
    
    def test_prediction_history(self):
        engine = MeihuaEngine()
        
        engine.analyze("主体", "客体")
        engine.analyze("测试", "环境")
        
        assert len(engine.prediction_history) == 2


class TestWuxingPredictionEngine:
    """测试五行预测引擎"""
    
    def test_initialize(self):
        engine = WuxingPredictionEngine()
        
        assert engine.WUXING_ELEMENTS == ["木", "火", "土", "金", "水"]
    
    def test_predict(self):
        engine = WuxingPredictionEngine()
        elements = {"木": 0.5, "火": 0.6, "土": 0.4, "金": 0.7, "水": 0.3}
        
        predictions = engine.predict(elements)
        
        assert len(predictions) == 5
        for pred in predictions:
            assert pred.element in engine.WUXING_ELEMENTS
    
    def test_predict_with_target(self):
        engine = WuxingPredictionEngine()
        elements = {"木": 0.5, "火": 0.6, "土": 0.4, "金": 0.7, "水": 0.3}
        
        predictions = engine.predict(elements, target="火")
        
        assert len(predictions) > 0
    
    def test_suggest_balance(self):
        engine = WuxingPredictionEngine()
        elements = {"木": 0.8, "火": 0.3, "土": 0.5, "金": 0.5, "水": 0.5}
        
        suggestion = engine.suggest_balance(elements)
        
        assert "suggestions" in suggestion
        assert "actions" in suggestion
        assert "木过旺" in suggestion["suggestions"][0]
    
    def test_predict_trend(self):
        engine = WuxingPredictionEngine()
        historical = [
            {"木": 0.5, "火": 0.5, "土": 0.5, "金": 0.5, "水": 0.5},
            {"木": 0.6, "火": 0.4, "土": 0.5, "金": 0.5, "水": 0.5}
        ]
        
        trends = engine.predict_trend(historical, steps=3)
        
        assert len(trends) == 3


class TestGanzhiTimeEngine:
    """测试干支时空引擎"""
    
    def test_initialize(self):
        engine = GanzhiTimeEngine()
        
        assert len(engine.TIANGAN) == 10
        assert len(engine.DIZHI) == 12
    
    def test_calculate_ganzhi(self):
        engine = GanzhiTimeEngine()
        
        year, month, day = engine.calculate_ganzhi(2024, 5, 15, 10)
        
        assert len(year) == 2
        assert len(month) == 2
        assert len(day) == 2
    
    def test_get_hour_ganzhi(self):
        engine = GanzhiTimeEngine()
        
        hour_ganzhi = engine.get_hour_ganzhi(10, "甲子")
        
        assert len(hour_ganzhi) == 2
    
    def test_calculate_energy(self):
        engine = GanzhiTimeEngine()
        
        energy = engine.calculate_energy("甲", "子")
        
        assert "tiangan_wuxing" in energy
        assert "dizhi_wuxing" in energy
        assert energy["tiangan_wuxing"] == "木"
        assert energy["dizhi_wuxing"] == "水"
    
    def test_predict_time_energy(self):
        engine = GanzhiTimeEngine()
        
        pred = engine.predict_time_energy(datetime.now())
        
        assert pred is not None
        assert pred.tiangan is not None
        assert pred.dizhi is not None
        assert pred.predicted_energy > 0


class TestPredictionEngine:
    """测试综合预测引擎"""
    
    def test_initialize(self):
        engine = PredictionEngine()
        
        assert engine.yijing is not None
        assert engine.meihua is not None
        assert engine.wuxing is not None
        assert engine.ganzhi is not None
    
    def test_predict_default(self):
        engine = PredictionEngine()
        
        result = engine.predict("测试查询")
        
        assert result is not None
        assert result.prediction_type == PredictionType.COMPREHENSIVE
        assert result.confidence > 0
    
    def test_predict_single_method(self):
        engine = PredictionEngine()
        
        result = engine.predict("测试", methods=[PredictionType.YI_JING])
        
        assert result is not None
    
    def test_predict_multiple_methods(self):
        engine = PredictionEngine()
        
        result = engine.predict("综合预测", methods=[
            PredictionType.YI_JING,
            PredictionType.MEIHUA,
            PredictionType.WUXING
        ])
        
        assert result is not None
        assert result.result.get("method_count", 0) >= 1
    
    def test_predict_with_context(self):
        engine = PredictionEngine()
        
        result = engine.predict(
            "测试预测",
            context={
                "subject": "主体",
                "object": "客体",
                "elements": {"木": 0.5, "火": 0.5, "土": 0.5, "金": 0.5, "水": 0.5}
            }
        )
        
        assert result is not None
    
    def test_prediction_history(self):
        engine = PredictionEngine()
        
        engine.predict("预测1")
        engine.predict("预测2")
        
        history = engine.get_prediction_history(limit=5)
        
        assert len(history) == 2
    
    def test_get_statistics(self):
        engine = PredictionEngine()
        
        engine.predict("预测1")
        engine.predict("预测2")
        
        stats = engine.get_statistics()
        
        assert "total_predictions" in stats
        assert stats["total_predictions"] == 2


class TestIntegration:
    """集成测试"""
    
    def test_full_prediction_workflow(self):
        engine = PredictionEngine()
        
        result = engine.predict(
            "项目发展方向预测",
            context={
                "subject": "项目",
                "object": "市场",
                "elements": {"木": 0.6, "火": 0.4, "土": 0.5, "金": 0.7, "水": 0.3}
            }
        )
        
        assert result is not None
        assert result.confidence > 0
        assert len(result.result.get("predictions", [])) > 0
    
    def test_multiple_predictions(self):
        engine = PredictionEngine()
        
        queries = ["事业发展", "投资决策", "人际关系", "健康状况"]
        
        for query in queries:
            result = engine.predict(query)
            assert result is not None
            assert result.confidence > 0
        
        stats = engine.get_statistics()
        assert stats["total_predictions"] == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
