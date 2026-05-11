"""
Unit tests for Eight Consciousness Progressive Architecture
八识递进架构单元测试
"""

import pytest
from datetime import datetime, timedelta
from typing import Dict, Any
import importlib.util
import os

spec = importlib.util.spec_from_file_location(
    "eight_consciousness",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                 "perception", "eight_consciousness.py")
)
eight_consciousness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eight_consciousness)

ConsciousnessLevel = eight_consciousness.ConsciousnessLevel
ConsciousnessData = eight_consciousness.ConsciousnessData
ConsciousnessLayer = eight_consciousness.ConsciousnessLayer
AbstractionResult = eight_consciousness.AbstractionResult
SensoryConsciousnessLayer = eight_consciousness.SensoryConsciousnessLayer
MindConsciousnessLayer = eight_consciousness.MindConsciousnessLayer
SixSensesPipeline = eight_consciousness.SixSensesPipeline
ManasConsciousness = eight_consciousness.ManasConsciousness
AlayaConsciousness = eight_consciousness.AlayaConsciousness
AlayaSeed = eight_consciousness.AlayaSeed
SelfCognitionReport = eight_consciousness.SelfCognitionReport
EightConsciousnessSystem = eight_consciousness.EightConsciousnessSystem


class TestConsciousnessLevel:
    """测试ConsciousnessLevel枚举"""
    
    def test_level_values(self):
        """测试识层级别值"""
        assert ConsciousnessLevel.EYE.level == 1
        assert ConsciousnessLevel.EAR.level == 2
        assert ConsciousnessLevel.NOSE.level == 3
        assert ConsciousnessLevel.TONGUE.level == 4
        assert ConsciousnessLevel.BODY.level == 5
        assert ConsciousnessLevel.MIND.level == 6
        assert ConsciousnessLevel.MANAS.level == 7
        assert ConsciousnessLevel.ALAYA.level == 8
    
    def test_is_sensory(self):
        """测试是否为感官识"""
        assert ConsciousnessLevel.EYE.is_sensory is True
        assert ConsciousnessLevel.EAR.is_sensory is True
        assert ConsciousnessLevel.NOSE.is_sensory is True
        assert ConsciousnessLevel.TONGUE.is_sensory is True
        assert ConsciousnessLevel.BODY.is_sensory is True
        assert ConsciousnessLevel.MIND.is_sensory is False
        assert ConsciousnessLevel.MANAS.is_sensory is False
        assert ConsciousnessLevel.ALAYA.is_sensory is False
    
    def test_is_sixth(self):
        """测试是否为第六识"""
        assert ConsciousnessLevel.MIND.is_sixth is True
        assert ConsciousnessLevel.EYE.is_sixth is False
    
    def test_is_manas(self):
        """测试是否为末那识"""
        assert ConsciousnessLevel.MANAS.is_manas is True
        assert ConsciousnessLevel.MIND.is_manas is False
    
    def test_is_alaya(self):
        """测试是否为阿赖耶识"""
        assert ConsciousnessLevel.ALAYA.is_alaya is True
        assert ConsciousnessLevel.MANAS.is_alaya is False


class TestConsciousnessData:
    """测试ConsciousnessData数据类"""
    
    def test_default_values(self):
        """测试默认值"""
        data = ConsciousnessData()
        assert data.data_id is not None
        assert data.level == ConsciousnessLevel.EYE
        assert data.raw_input is None
        assert data.processed_content == {}
        assert data.abstract_result == {}
        assert data.confidence == 0.0
        assert data.clarity == 1.0
    
    def test_custom_values(self):
        """测试自定义值"""
        data = ConsciousnessData(
            level=ConsciousnessLevel.MIND,
            raw_input="test input",
            processed_content={'key': 'value'},
            confidence=0.8
        )
        assert data.level == ConsciousnessLevel.MIND
        assert data.raw_input == "test input"
        assert data.processed_content == {'key': 'value'}
        assert data.confidence == 0.8


class TestAbstractionResult:
    """测试AbstractionResult"""
    
    def test_default_values(self):
        """测试默认值"""
        result = AbstractionResult(
            source_level=ConsciousnessLevel.EYE,
            target_level=ConsciousnessLevel.MIND,
            abstracted_content={},
            essence="test"
        )
        assert result.source_level == ConsciousnessLevel.EYE
        assert result.target_level == ConsciousnessLevel.MIND
        assert result.essence == "test"
        assert result.associations == []
        assert result.importance == 0.5


class TestSensoryConsciousnessLayer:
    """测试感官识层"""
    
    def test_init_eye_consciousness(self):
        """测试眼识初始化"""
        layer = SensoryConsciousnessLayer(ConsciousnessLevel.EYE)
        assert layer.level == ConsciousnessLevel.EYE
    
    def test_init_non_sensory_raises(self):
        """测试非感官识初始化应抛出异常"""
        with pytest.raises(ValueError):
            SensoryConsciousnessLayer(ConsciousnessLevel.MIND)
    
    def test_process_visual_data(self):
        """测试处理视觉数据"""
        layer = SensoryConsciousnessLayer(ConsciousnessLevel.EYE)
        data = ConsciousnessData(
            level=ConsciousnessLevel.EYE,
            raw_input={'objects': ['tree', 'house'], 'colors': ['green']}
        )
        
        result = layer.process(data)
        
        assert result.level == ConsciousnessLevel.EYE
        assert 'objects' in result.processed_content
        assert result.processed_content['objects'] == ['tree', 'house']
        assert result.confidence > 0
    
    def test_process_auditory_data(self):
        """测试处理听觉数据"""
        layer = SensoryConsciousnessLayer(ConsciousnessLevel.EAR)
        data = ConsciousnessData(
            level=ConsciousnessLevel.EAR,
            raw_input={'speech': 'hello world', 'volume': 0.8}
        )
        
        result = layer.process(data)
        
        assert result.level == ConsciousnessLevel.EAR
        assert 'speech' in result.processed_content
        assert result.processed_content['speech'] == 'hello world'
    
    def test_abstract_result(self):
        """测试抽象结果"""
        layer = SensoryConsciousnessLayer(ConsciousnessLevel.EYE)
        data = ConsciousnessData(
            level=ConsciousnessLevel.EYE,
            raw_input={'objects': ['tree']},
            processed_content={'objects': ['tree'], 'intensity': 0.7}
        )
        
        abstraction = layer.abstract(data)
        
        assert abstraction.source_level == ConsciousnessLevel.EYE
        assert abstraction.target_level == ConsciousnessLevel.MIND
        assert '视觉感知' in abstraction.essence
        assert abstraction.importance >= 0
    
    def test_get_recent_data(self):
        """测试获取最近数据"""
        layer = SensoryConsciousnessLayer(ConsciousnessLevel.EYE)
        
        for i in range(5):
            data = ConsciousnessData(
                level=ConsciousnessLevel.EYE,
                raw_input={'objects': [f'obj_{i}']}
            )
            layer.process(data)
        
        recent = layer.get_recent_data(limit=3)
        assert len(recent) == 3
    
    def test_get_stats(self):
        """测试获取统计"""
        layer = SensoryConsciousnessLayer(ConsciousnessLevel.EYE)
        
        for i in range(3):
            data = ConsciousnessData(
                level=ConsciousnessLevel.EYE,
                raw_input={'objects': [f'obj_{i}']}
            )
            layer.process(data)
        
        stats = layer.get_stats()
        assert stats['total_processed'] == 3
        assert stats['avg_confidence'] > 0


class TestMindConsciousnessLayer:
    """测试意识层"""
    
    def test_init(self):
        """测试初始化"""
        layer = MindConsciousnessLayer()
        assert layer.level == ConsciousnessLevel.MIND
    
    def test_process_single_abstraction(self):
        """测试处理单个抽象结果"""
        layer = MindConsciousnessLayer()
        abstraction = AbstractionResult(
            source_level=ConsciousnessLevel.EYE,
            target_level=ConsciousnessLevel.MIND,
            abstracted_content={'key': 'value'},
            essence="视觉感知: tree",
            associations=['tree', 'green']
        )
        
        data = ConsciousnessData(
            level=ConsciousnessLevel.MIND,
            raw_input=abstraction
        )
        
        result = layer.process(data)
        
        assert result.level == ConsciousnessLevel.MIND
        assert 'integrated_meaning' in result.processed_content
        assert result.confidence > 0
    
    def test_process_multiple_abstractions(self):
        """测试处理多个抽象结果"""
        layer = MindConsciousnessLayer()
        
        abstractions = [
            AbstractionResult(
                source_level=ConsciousnessLevel.EYE,
                target_level=ConsciousnessLevel.MIND,
                abstracted_content={},
                essence="视觉感知",
                associations=['visual']
            ),
            AbstractionResult(
                source_level=ConsciousnessLevel.EAR,
                target_level=ConsciousnessLevel.MIND,
                abstracted_content={},
                essence="听觉感知",
                associations=['auditory']
            )
        ]
        
        data = ConsciousnessData(
            level=ConsciousnessLevel.MIND,
            raw_input=abstractions
        )
        
        result = layer.process(data)
        
        assert result.level == ConsciousnessLevel.MIND
        assert 'source_senses' in result.processed_content
        assert result.processed_content['thought_type'] == 'integrated'
    
    def test_abstract_to_manas(self):
        """测试抽象到末那识"""
        layer = MindConsciousnessLayer()
        data = ConsciousnessData(
            level=ConsciousnessLevel.MIND,
            processed_content={
                'integrated_meaning': 'test meaning',
                'key_concepts': ['concept1'],
                'thought_type': 'reflective'
            },
            confidence=0.8,
            clarity=0.9
        )
        
        abstraction = layer.abstract(data)
        
        assert abstraction.source_level == ConsciousnessLevel.MIND
        assert abstraction.target_level == ConsciousnessLevel.MANAS
        assert '思维' in abstraction.essence


class TestSixSensesPipeline:
    """测试六识流水线"""
    
    def test_init(self):
        """测试初始化"""
        pipeline = SixSensesPipeline()
        assert pipeline.get_layer(ConsciousnessLevel.EYE) is not None
        assert pipeline.get_layer(ConsciousnessLevel.MIND) is not None
    
    def test_process_sensory(self):
        """测试处理单个感官"""
        pipeline = SixSensesPipeline()
        
        processed, abstraction = pipeline.process_sensory(
            ConsciousnessLevel.EYE,
            {'objects': ['tree']}
        )
        
        assert processed.level == ConsciousnessLevel.EYE
        assert abstraction.source_level == ConsciousnessLevel.EYE
        assert abstraction.target_level == ConsciousnessLevel.MIND
    
    def test_process_sensory_invalid_level(self):
        """测试无效感官级别"""
        pipeline = SixSensesPipeline()
        
        with pytest.raises(ValueError):
            pipeline.process_sensory(
                ConsciousnessLevel.MIND,
                {'data': 'test'}
            )
    
    def test_process_pipeline_full(self):
        """测试完整流水线处理"""
        pipeline = SixSensesPipeline()
        
        sensory_inputs = {
            ConsciousnessLevel.EYE: {'objects': ['tree', 'sky']},
            ConsciousnessLevel.EAR: {'speech': 'hello'},
            ConsciousnessLevel.BODY: {'temperature': 0.6}
        }
        
        mind_result, abstractions = pipeline.process_pipeline(sensory_inputs)
        
        assert mind_result.level == ConsciousnessLevel.MIND
        assert len(abstractions) == 4
        assert abstractions[-1].source_level == ConsciousnessLevel.MIND
    
    def test_process_single_stream(self):
        """测试单一流水线"""
        pipeline = SixSensesPipeline()
        
        result = pipeline.process_single_stream(
            ConsciousnessLevel.EYE,
            {'objects': ['flower']}
        )
        
        assert result.level == ConsciousnessLevel.MIND
        assert result.confidence > 0
    
    def test_get_pipeline_stats(self):
        """测试获取流水线统计"""
        pipeline = SixSensesPipeline()
        
        pipeline.process_pipeline({
            ConsciousnessLevel.EYE: {'objects': ['test']}
        })
        
        stats = pipeline.get_pipeline_stats()
        assert stats['total_processed'] == 1


class TestManasConsciousness:
    """测试末那识"""
    
    def test_init(self):
        """测试初始化"""
        manas = ManasConsciousness()
        assert manas._self_references is not None
    
    def test_monitor_self_low_involvement(self):
        """测试监控低自我参与"""
        manas = ManasConsciousness()
        
        data = ConsciousnessData(
            level=ConsciousnessLevel.MIND,
            processed_content={
                'integrated_meaning': '客观观察自然现象',
                'key_concepts': ['自然', '现象']
            },
            confidence=0.7
        )
        
        report = manas.monitor_self(data)
        
        assert isinstance(report, SelfCognitionReport)
        assert report.self_involvement_score >= 0
        assert report.self_involvement_score < 0.5
    
    def test_monitor_self_high_involvement(self):
        """测试监控高自我参与"""
        manas = ManasConsciousness()
        
        data = ConsciousnessData(
            level=ConsciousnessLevel.MIND,
            processed_content={
                'integrated_meaning': '我认为这是我的重要发现',
                'key_concepts': ['我', '我的', '发现']
            },
            confidence=0.9
        )
        
        report = manas.monitor_self(data)
        
        assert report.self_involvement_score > 0
        assert '自我参照' in report.identified_self_patterns
    
    def test_generate_report(self):
        """测试生成报告"""
        manas = ManasConsciousness()
        
        for i in range(5):
            data = ConsciousnessData(
                level=ConsciousnessLevel.MIND,
                processed_content={
                    'integrated_meaning': f'测试内容 {i}',
                    'key_concepts': ['test']
                },
                confidence=0.7
            )
            manas.monitor_self(data)
        
        report = manas.generate_report()
        
        assert 'metrics' in report
        assert 'average_self_involvement' in report['metrics']
        assert report['period']['sample_count'] == 5
    
    def test_generate_report_with_time_range(self):
        """测试带时间范围的报告"""
        manas = ManasConsciousness()
        
        for i in range(3):
            data = ConsciousnessData(
                level=ConsciousnessLevel.MIND,
                processed_content={'integrated_meaning': f'test {i}'},
                confidence=0.7
            )
            manas.monitor_self(data)
        
        start = datetime.now() - timedelta(hours=1)
        end = datetime.now() + timedelta(hours=1)
        
        report = manas.generate_report(time_range=(start, end))
        
        assert report['period']['sample_count'] == 3
    
    def test_get_recent_reports(self):
        """测试获取最近报告"""
        manas = ManasConsciousness()
        
        for i in range(15):
            data = ConsciousnessData(
                level=ConsciousnessLevel.MIND,
                processed_content={'integrated_meaning': f'test {i}'},
                confidence=0.7
            )
            manas.monitor_self(data)
        
        recent = manas.get_recent_reports(limit=5)
        assert len(recent) == 5


class TestAlayaConsciousness:
    """测试阿赖耶识"""
    
    def test_init(self):
        """测试初始化"""
        alaya = AlayaConsciousness()
        assert alaya._seeds == {}
    
    def test_store_important_memory(self):
        """测试存储重要记忆"""
        alaya = AlayaConsciousness()
        
        seed = alaya.store(
            content={'meaning': 'important insight'},
            seed_type='insight',
            importance=0.9
        )
        
        assert isinstance(seed, AlayaSeed)
        assert seed.seed_id is not None
        assert seed.seed_type == 'insight'
        assert seed.strength > 1.0
    
    def test_store_unimportant_memory(self):
        """测试存储不重要记忆（低于阈值）"""
        alaya = AlayaConsciousness()
        alaya._importance_threshold = 0.5
        
        seed = alaya.store(
            content={'data': 'minor'},
            seed_type='general',
            importance=0.3
        )
        
        assert seed is not None
        assert len(alaya._seeds) == 1
    
    def test_retrieve_by_type(self):
        """测试按类型检索"""
        alaya = AlayaConsciousness()
        
        alaya.store({'data': 'type1'}, seed_type='type1', importance=0.8)
        alaya.store({'data': 'type2'}, seed_type='type2', importance=0.8)
        alaya.store({'data': 'type1_2'}, seed_type='type1', importance=0.8)
        
        results = alaya.retrieve(seed_type='type1')
        
        assert len(results) == 2
        assert all(s.seed_type == 'type1' for s in results)
    
    def test_retrieve_by_query(self):
        """测试按查询检索"""
        alaya = AlayaConsciousness()
        
        alaya.store({'meaning': 'wisdom insight'}, seed_type='insight', importance=0.8)
        alaya.store({'meaning': 'random thought'}, seed_type='thought', importance=0.8)
        
        results = alaya.retrieve(query='wisdom')
        
        assert len(results) == 1
        assert 'wisdom' in str(results[0].content)
    
    def test_retrieve_by_time_range(self):
        """测试按时间范围检索"""
        alaya = AlayaConsciousness()
        
        alaya.store({'data': 'recent'}, seed_type='test', importance=0.8)
        
        start = datetime.now() - timedelta(hours=1)
        end = datetime.now() + timedelta(hours=1)
        
        results = alaya.retrieve(time_range=(start, end))
        
        assert len(results) == 1
    
    def test_retrieve_by_strength(self):
        """测试按强度检索"""
        alaya = AlayaConsciousness()
        
        alaya.store({'data': 'weak'}, seed_type='test', importance=0.5)
        alaya.store({'data': 'strong'}, seed_type='test', importance=0.9)
        
        results = alaya.retrieve(min_strength=1.3)
        
        assert len(results) == 1
        assert results[0].strength >= 1.3
    
    def test_plant_seed_from_abstraction(self):
        """测试从抽象结果种植种子"""
        alaya = AlayaConsciousness()
        
        abstraction = AbstractionResult(
            source_level=ConsciousnessLevel.MIND,
            target_level=ConsciousnessLevel.MANAS,
            abstracted_content={'thought_type': 'reflective'},
            essence="深刻洞察",
            importance=0.85
        )
        
        report = SelfCognitionReport(
            self_involvement_score=0.3,
            attachment_level=0.2
        )
        
        seed = alaya.plant_seed(abstraction, report)
        
        assert seed.seed_type == 'consciousness_意识'
        assert seed.karmic_weight > 0
    
    def test_get_karmic_state(self):
        """测试获取业力状态"""
        alaya = AlayaConsciousness()
        
        alaya.store({'data': 'a'}, seed_type='type1', importance=0.8, karmic_weight=0.3)
        alaya.store({'data': 'b'}, seed_type='type2', importance=0.8, karmic_weight=0.2)
        
        state = alaya.get_karmic_state()
        
        assert state['total_seeds'] == 2
        assert state['total_karmic_weight'] == 0.5
        assert 'type1' in state['type_distribution']
        assert 'type2' in state['type_distribution']
    
    def test_retrieve_by_association(self):
        """测试关联检索"""
        alaya = AlayaConsciousness()
        
        seed1 = alaya.store(
            {'data': 'seed1'},
            seed_type='test',
            importance=0.8,
            source_trace=['source_a']
        )
        
        seed2 = alaya.store(
            {'data': 'seed2'},
            seed_type='test',
            importance=0.8,
            source_trace=[seed1.seed_id]
        )
        
        related = alaya.retrieve_by_association(seed1.seed_id)
        
        assert len(related) > 0
    
    def test_seed_activation(self):
        """测试种子激活"""
        alaya = AlayaConsciousness()
        
        seed = alaya.store({'data': 'test'}, seed_type='test', importance=0.8)
        initial_count = seed.activation_count
        
        alaya.retrieve(seed_type='test')
        
        assert seed.activation_count == initial_count + 1


class TestEightConsciousnessSystem:
    """测试八识系统完整集成"""
    
    def test_init(self):
        """测试初始化"""
        system = EightConsciousnessSystem()
        assert system.pipeline is not None
        assert system.manas is not None
        assert system.alaya is not None
    
    def test_full_process(self):
        """测试完整处理流程"""
        system = EightConsciousnessSystem()
        
        result = system.process({
            ConsciousnessLevel.EYE: {'objects': ['mountain', 'river']},
            ConsciousnessLevel.EAR: {'speech': 'nature sounds'}
        })
        
        assert 'mind_result' in result
        assert 'consciousness_report' in result
        assert 'abstractions' in result
        assert 'alaya_seed' in result
        
        assert result['mind_result']['confidence'] > 0
        assert result['consciousness_report']['self_involvement'] >= 0
    
    def test_process_without_alaya_storage(self):
        """测试不存储到阿赖耶识"""
        system = EightConsciousnessSystem()
        
        result = system.process(
            {ConsciousnessLevel.EYE: {'objects': ['test']}},
            store_to_alaya=False
        )
        
        assert 'alaya_seed' not in result
    
    def test_get_system_state(self):
        """测试获取系统状态"""
        system = EightConsciousnessSystem()
        
        system.process({
            ConsciousnessLevel.EYE: {'objects': ['test']}
        })
        
        state = system.get_system_state()
        
        assert 'pipeline_stats' in state
        assert 'karmic_state' in state
        assert state['recent_processing_count'] == 1
    
    def test_generate_self_cognition_report(self):
        """测试生成自我认知报告"""
        system = EightConsciousnessSystem()
        
        for i in range(3):
            system.process({
                ConsciousnessLevel.EYE: {'objects': [f'obj_{i}']}
            })
        
        report = system.generate_self_cognition_report()
        
        assert 'metrics' in report
        assert report['period']['sample_count'] == 3


class TestIntegration:
    """集成测试"""
    
    def test_full_eight_consciousness_flow(self):
        """测试完整的八识流转"""
        pipeline = SixSensesPipeline()
        manas = ManasConsciousness()
        alaya = AlayaConsciousness()
        
        sensory_inputs = {
            ConsciousnessLevel.EYE: {
                'objects': ['flower'],
                'colors': ['red'],
                'intensity': 0.8
            },
            ConsciousnessLevel.EAR: {
                'speech': 'beautiful flower',
                'volume': 0.6
            },
            ConsciousnessLevel.NOSE: {
                'scents': ['fragrance'],
                'intensity': 0.7
            }
        }
        
        mind_result, abstractions = pipeline.process_pipeline(sensory_inputs)
        
        assert mind_result.level == ConsciousnessLevel.MIND
        assert len(abstractions) == 4
        
        manas_report = manas.monitor_self(mind_result, abstractions[-1])
        
        assert manas_report.self_involvement_score >= 0
        assert manas_report.ego_strength >= 0
        
        alaya_seed = alaya.plant_seed(abstractions[-1], manas_report)
        
        assert alaya_seed is not None
        
        stored_seeds = alaya.retrieve(seed_type=f'consciousness_{abstractions[-1].source_level.value}')
        assert len(stored_seeds) >= 1
    
    def test_multiple_processing_cycles(self):
        """测试多次处理循环"""
        system = EightConsciousnessSystem()
        
        for i in range(5):
            result = system.process({
                ConsciousnessLevel.EYE: {'objects': [f'object_{i}']},
                ConsciousnessLevel.EAR: {'speech': f'message {i}'}
            })
            
            assert result['mind_result']['confidence'] > 0
        
        state = system.get_system_state()
        assert state['pipeline_stats']['total_processed'] == 5
        
        karmic_state = state['karmic_state']
        assert karmic_state['total_seeds'] >= 5
    
    def test_self_awareness_tracking(self):
        """测试自我觉察追踪"""
        manas = ManasConsciousness()
        
        low_self_data = ConsciousnessData(
            level=ConsciousnessLevel.MIND,
            processed_content={
                'integrated_meaning': '观察自然现象的变化规律',
                'key_concepts': ['自然', '规律', '变化']
            },
            confidence=0.8
        )
        
        high_self_data = ConsciousnessData(
            level=ConsciousnessLevel.MIND,
            processed_content={
                'integrated_meaning': '我认为我的观点是正确的',
                'key_concepts': ['我', '我的', '观点']
            },
            confidence=0.9
        )
        
        low_report = manas.monitor_self(low_self_data)
        high_report = manas.monitor_self(high_self_data)
        
        assert low_report.self_involvement_score < high_report.self_involvement_score
        
        summary = manas.generate_report()
        assert summary['metrics']['average_self_involvement'] > 0
