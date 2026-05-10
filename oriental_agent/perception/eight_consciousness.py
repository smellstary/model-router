"""
Eight Consciousness Progressive Architecture (八识递进架构)
Based on Yogacara Buddhism consciousness theory

八识层次：
- 前五识：眼识、耳识、鼻识、舌识、身识（感官知觉）
- 第六识：意识（综合思维）
- 第七识：末那识（自我认知）
- 第八识：阿赖耶识（根本存储）
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
import uuid
import hashlib
import json


class ConsciousnessLevel(Enum):
    """八识层次枚举 - Eight Consciousness Levels"""
    EYE = "眼识"
    EAR = "耳识"
    NOSE = "鼻识"
    TONGUE = "舌识"
    BODY = "身识"
    MIND = "意识"
    MANAS = "末那识"
    ALAYA = "阿赖耶识"
    
    @property
    def level(self) -> int:
        """获取识层级别（1-8）"""
        levels = {
            ConsciousnessLevel.EYE: 1,
            ConsciousnessLevel.EAR: 2,
            ConsciousnessLevel.NOSE: 3,
            ConsciousnessLevel.TONGUE: 4,
            ConsciousnessLevel.BODY: 5,
            ConsciousnessLevel.MIND: 6,
            ConsciousnessLevel.MANAS: 7,
            ConsciousnessLevel.ALAYA: 8,
        }
        return levels[self]
    
    @property
    def is_sensory(self) -> bool:
        """是否为感官识（前五识）"""
        return self.level <= 5
    
    @property
    def is_sixth(self) -> bool:
        """是否为第六识（意识）"""
        return self == ConsciousnessLevel.MIND
    
    @property
    def is_manas(self) -> bool:
        """是否为末那识"""
        return self == ConsciousnessLevel.MANAS
    
    @property
    def is_alaya(self) -> bool:
        """是否为阿赖耶识"""
        return self == ConsciousnessLevel.ALAYA


@dataclass
class ConsciousnessData:
    """识层数据结构"""
    data_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    level: ConsciousnessLevel = ConsciousnessLevel.EYE
    raw_input: Any = None
    processed_content: Dict[str, Any] = field(default_factory=dict)
    abstract_result: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    clarity: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    source_level: Optional[ConsciousnessLevel] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AbstractionResult:
    """抽象结果 - 传递给下一层的数据"""
    source_level: ConsciousnessLevel
    target_level: ConsciousnessLevel
    abstracted_content: Dict[str, Any]
    essence: str
    associations: List[str] = field(default_factory=list)
    importance: float = 0.5
    timestamp: datetime = field(default_factory=datetime.now)


class ConsciousnessLayer(ABC):
    """识层基类 - Base class for consciousness layers"""
    
    def __init__(self, level: ConsciousnessLevel):
        self.level = level
        self._buffer: List[ConsciousnessData] = []
        self._max_buffer_size = 100
        self._processing_stats = {
            'total_processed': 0,
            'avg_confidence': 0.0,
            'last_process_time': None
        }
    
    @abstractmethod
    def process(self, data: ConsciousnessData) -> ConsciousnessData:
        """
        处理输入数据
        
        Args:
            data: 输入的识层数据
            
        Returns:
            处理后的识层数据
        """
        pass
    
    @abstractmethod
    def abstract(self, data: ConsciousnessData) -> AbstractionResult:
        """
        抽象结果传递给下一层
        
        Args:
            data: 处理后的识层数据
            
        Returns:
            抽象结果，用于传递给下一层
        """
        pass
    
    def _store_to_buffer(self, data: ConsciousnessData) -> None:
        """存储到缓冲区"""
        self._buffer.append(data)
        if len(self._buffer) > self._max_buffer_size:
            self._buffer = self._buffer[-self._max_buffer_size:]
    
    def _update_stats(self, confidence: float) -> None:
        """更新处理统计"""
        self._processing_stats['total_processed'] += 1
        total = self._processing_stats['total_processed']
        old_avg = self._processing_stats['avg_confidence']
        self._processing_stats['avg_confidence'] = (
            (old_avg * (total - 1) + confidence) / total
        )
        self._processing_stats['last_process_time'] = datetime.now()
    
    def get_recent_data(self, limit: int = 10) -> List[ConsciousnessData]:
        """获取最近处理的数据"""
        return self._buffer[-limit:]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取处理统计"""
        return self._processing_stats.copy()


class SensoryConsciousnessLayer(ConsciousnessLayer):
    """感官识层（前五识）"""
    
    def __init__(self, level: ConsciousnessLevel):
        if not level.is_sensory:
            raise ValueError(f"{level} is not a sensory consciousness level")
        super().__init__(level)
        self._feature_extractors = self._init_feature_extractors()
    
    def _init_feature_extractors(self) -> Dict[str, Any]:
        """初始化特征提取器"""
        extractors = {
            ConsciousnessLevel.EYE: self._extract_visual_features,
            ConsciousnessLevel.EAR: self._extract_auditory_features,
            ConsciousnessLevel.NOSE: self._extract_olfactory_features,
            ConsciousnessLevel.TONGUE: self._extract_gustatory_features,
            ConsciousnessLevel.BODY: self._extract_tactile_features,
        }
        return extractors
    
    def process(self, data: ConsciousnessData) -> ConsciousnessData:
        """处理感官数据"""
        extractor = self._feature_extractors.get(self.level)
        if extractor:
            features = extractor(data.raw_input)
        else:
            features = {'raw': data.raw_input}
        
        processed = ConsciousnessData(
            data_id=data.data_id,
            level=self.level,
            raw_input=data.raw_input,
            processed_content=features,
            confidence=self._calculate_confidence(features),
            clarity=self._calculate_clarity(features),
            source_level=data.source_level
        )
        
        self._store_to_buffer(processed)
        self._update_stats(processed.confidence)
        
        return processed
    
    def abstract(self, data: ConsciousnessData) -> AbstractionResult:
        """抽象感官数据为概念"""
        essence = self._extract_essence(data.processed_content)
        associations = self._generate_associations(data.processed_content)
        
        return AbstractionResult(
            source_level=self.level,
            target_level=ConsciousnessLevel.MIND,
            abstracted_content={
                'sensory_type': self.level.value,
                'key_features': self._get_key_features(data.processed_content),
                'intensity': data.processed_content.get('intensity', 0.5),
                'quality': data.processed_content.get('quality', 'neutral')
            },
            essence=essence,
            associations=associations,
            importance=data.confidence * data.clarity
        )
    
    def _extract_visual_features(self, raw_data: Any) -> Dict[str, Any]:
        """提取视觉特征"""
        features = {
            'objects': [],
            'colors': [],
            'shapes': [],
            'motion': False,
            'intensity': 0.5,
            'quality': 'normal'
        }
        
        if isinstance(raw_data, dict):
            features.update({
                'objects': raw_data.get('objects', []),
                'colors': raw_data.get('colors', []),
                'motion': raw_data.get('motion', False),
                'intensity': raw_data.get('intensity', 0.5)
            })
        elif isinstance(raw_data, str):
            features['text_detected'] = raw_data
        
        return features
    
    def _extract_auditory_features(self, raw_data: Any) -> Dict[str, Any]:
        """提取听觉特征"""
        features = {
            'sounds': [],
            'speech': '',
            'tone': 'neutral',
            'volume': 0.5,
            'intensity': 0.5,
            'quality': 'normal'
        }
        
        if isinstance(raw_data, dict):
            features.update({
                'sounds': raw_data.get('sounds', []),
                'speech': raw_data.get('speech', ''),
                'tone': raw_data.get('tone', 'neutral'),
                'volume': raw_data.get('volume', 0.5)
            })
        
        return features
    
    def _extract_olfactory_features(self, raw_data: Any) -> Dict[str, Any]:
        """提取嗅觉特征"""
        features = {
            'scents': [],
            'intensity': 0.5,
            'pleasantness': 0.5,
            'quality': 'neutral'
        }
        
        if isinstance(raw_data, dict):
            features.update({
                'scents': raw_data.get('scents', []),
                'intensity': raw_data.get('intensity', 0.5),
                'pleasantness': raw_data.get('pleasantness', 0.5)
            })
        
        return features
    
    def _extract_gustatory_features(self, raw_data: Any) -> Dict[str, Any]:
        """提取味觉特征"""
        features = {
            'tastes': [],
            'intensity': 0.5,
            'pleasantness': 0.5,
            'quality': 'neutral'
        }
        
        if isinstance(raw_data, dict):
            features.update({
                'tastes': raw_data.get('tastes', []),
                'intensity': raw_data.get('intensity', 0.5)
            })
        
        return features
    
    def _extract_tactile_features(self, raw_data: Any) -> Dict[str, Any]:
        """提取触觉特征"""
        features = {
            'sensations': [],
            'temperature': 0.5,
            'pressure': 0.5,
            'texture': 'neutral',
            'intensity': 0.5,
            'quality': 'normal'
        }
        
        if isinstance(raw_data, dict):
            features.update({
                'sensations': raw_data.get('sensations', []),
                'temperature': raw_data.get('temperature', 0.5),
                'pressure': raw_data.get('pressure', 0.5),
                'texture': raw_data.get('texture', 'neutral')
            })
        
        return features
    
    def _calculate_confidence(self, features: Dict[str, Any]) -> float:
        """计算置信度"""
        confidence = 0.3
        
        if features.get('objects') or features.get('sounds') or features.get('scents'):
            confidence += 0.3
        if features.get('intensity', 0) > 0.3:
            confidence += 0.2
        if features.get('quality') != 'neutral':
            confidence += 0.2
        
        return min(1.0, confidence)
    
    def _calculate_clarity(self, features: Dict[str, Any]) -> float:
        """计算清晰度"""
        clarity = 0.5
        
        if features.get('intensity', 0) > 0.5:
            clarity += 0.2
        if len(features.get('objects', features.get('sounds', []))) > 0:
            clarity += 0.3
        
        return min(1.0, clarity)
    
    def _extract_essence(self, features: Dict[str, Any]) -> str:
        """提取本质"""
        if self.level == ConsciousnessLevel.EYE:
            objects = features.get('objects', [])
            return f"视觉感知: {', '.join(map(str, objects[:3]))}" if objects else "视觉感知"
        elif self.level == ConsciousnessLevel.EAR:
            speech = features.get('speech', '')
            return f"听觉感知: {speech[:50]}" if speech else "听觉感知"
        elif self.level == ConsciousnessLevel.NOSE:
            scents = features.get('scents', [])
            return f"嗅觉感知: {', '.join(map(str, scents[:3]))}" if scents else "嗅觉感知"
        elif self.level == ConsciousnessLevel.TONGUE:
            tastes = features.get('tastes', [])
            return f"味觉感知: {', '.join(map(str, tastes[:3]))}" if tastes else "味觉感知"
        elif self.level == ConsciousnessLevel.BODY:
            sensations = features.get('sensations', [])
            return f"触觉感知: {', '.join(map(str, sensations[:3]))}" if sensations else "触觉感知"
        return "感官感知"
    
    def _generate_associations(self, features: Dict[str, Any]) -> List[str]:
        """生成关联"""
        associations = []
        
        for key in ['objects', 'sounds', 'scents', 'tastes', 'sensations']:
            items = features.get(key, [])
            associations.extend([str(item) for item in items[:5]])
        
        return associations
    
    def _get_key_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """获取关键特征"""
        key_features = {}
        
        for key in ['objects', 'sounds', 'speech', 'scents', 'tastes', 'sensations']:
            if key in features and features[key]:
                key_features[key] = features[key]
        
        key_features['intensity'] = features.get('intensity', 0.5)
        key_features['quality'] = features.get('quality', 'neutral')
        
        return key_features


class MindConsciousnessLayer(ConsciousnessLayer):
    """第六识 - 意识层"""
    
    def __init__(self):
        super().__init__(ConsciousnessLevel.MIND)
        self._integrated_thoughts: List[Dict[str, Any]] = []
        self._reasoning_depth = 0
    
    def process(self, data: ConsciousnessData) -> ConsciousnessData:
        """处理意识数据，综合前五识的信息"""
        if isinstance(data.raw_input, AbstractionResult):
            abstraction = data.raw_input
            processed_content = self._integrate_abstraction(abstraction)
        elif isinstance(data.raw_input, list):
            processed_content = self._integrate_multiple_abstractions(data.raw_input)
        else:
            processed_content = {
                'thought': str(data.raw_input),
                'abstraction_level': 0.5
            }
        
        processed = ConsciousnessData(
            data_id=data.data_id,
            level=self.level,
            raw_input=data.raw_input,
            processed_content=processed_content,
            confidence=self._calculate_confidence(processed_content),
            clarity=self._calculate_clarity(processed_content),
            source_level=data.source_level or ConsciousnessLevel.MIND
        )
        
        self._store_to_buffer(processed)
        self._update_stats(processed.confidence)
        
        return processed
    
    def abstract(self, data: ConsciousnessData) -> AbstractionResult:
        """抽象意识内容为自我认知素材"""
        essence = self._extract_thought_essence(data.processed_content)
        
        return AbstractionResult(
            source_level=self.level,
            target_level=ConsciousnessLevel.MANAS,
            abstracted_content={
                'thought_type': data.processed_content.get('thought_type', 'general'),
                'key_concepts': data.processed_content.get('key_concepts', []),
                'emotional_tone': data.processed_content.get('emotional_tone', 'neutral'),
                'reasoning_chain': data.processed_content.get('reasoning_chain', [])
            },
            essence=essence,
            associations=data.processed_content.get('associations', []),
            importance=data.confidence * data.clarity
        )
    
    def _integrate_abstraction(self, abstraction: AbstractionResult) -> Dict[str, Any]:
        """整合抽象结果"""
        return {
            'source_sense': abstraction.source_level.value,
            'sensory_essence': abstraction.essence,
            'integrated_meaning': self._derive_meaning(abstraction),
            'thought_type': self._classify_thought(abstraction),
            'key_concepts': abstraction.associations[:5],
            'emotional_tone': 'neutral',
            'reasoning_chain': [abstraction.essence],
            'abstraction_level': 0.6
        }
    
    def _integrate_multiple_abstractions(
        self, 
        abstractions: List[AbstractionResult]
    ) -> Dict[str, Any]:
        """整合多个抽象结果"""
        sources = [a.source_level.value for a in abstractions]
        essences = [a.essence for a in abstractions]
        all_associations = []
        for a in abstractions:
            all_associations.extend(a.associations)
        
        return {
            'source_senses': sources,
            'sensory_essences': essences,
            'integrated_meaning': self._synthesize_meaning(essences),
            'thought_type': 'integrated',
            'key_concepts': list(set(all_associations))[:10],
            'emotional_tone': self._detect_emotional_tone(abstractions),
            'reasoning_chain': essences,
            'abstraction_level': 0.7
        }
    
    def _derive_meaning(self, abstraction: AbstractionResult) -> str:
        """推导意义"""
        return f"理解: {abstraction.essence}"
    
    def _synthesize_meaning(self, essences: List[str]) -> str:
        """综合意义"""
        if not essences:
            return "综合理解"
        return " | ".join(essences[:3])
    
    def _classify_thought(self, abstraction: AbstractionResult) -> str:
        """分类思维类型"""
        source = abstraction.source_level
        
        if source == ConsciousnessLevel.EYE:
            return "visual_thought"
        elif source == ConsciousnessLevel.EAR:
            return "auditory_thought"
        elif source == ConsciousnessLevel.MIND:
            return "reflective_thought"
        else:
            return "sensory_thought"
    
    def _detect_emotional_tone(
        self, 
        abstractions: List[AbstractionResult]
    ) -> str:
        """检测情感基调"""
        return "neutral"
    
    def _calculate_confidence(self, content: Dict[str, Any]) -> float:
        """计算置信度"""
        confidence = 0.4
        
        if content.get('key_concepts'):
            confidence += 0.2
        if content.get('integrated_meaning'):
            confidence += 0.2
        if content.get('reasoning_chain'):
            confidence += 0.2
        
        return min(1.0, confidence)
    
    def _calculate_clarity(self, content: Dict[str, Any]) -> float:
        """计算清晰度"""
        clarity = 0.5
        
        if content.get('abstraction_level', 0) > 0.5:
            clarity += 0.3
        if len(content.get('key_concepts', [])) <= 5:
            clarity += 0.2
        
        return min(1.0, clarity)
    
    def _extract_thought_essence(self, content: Dict[str, Any]) -> str:
        """提取思维本质"""
        meaning = content.get('integrated_meaning', '')
        if meaning:
            return f"思维: {meaning[:100]}"
        return "思维活动"


class SixSensesPipeline:
    """六识递进处理流水线
    
    按眼识→耳识→鼻识→舌识→身识→意识顺序处理
    每层处理后传递抽象结果
    """
    
    SENSORY_ORDER = [
        ConsciousnessLevel.EYE,
        ConsciousnessLevel.EAR,
        ConsciousnessLevel.NOSE,
        ConsciousnessLevel.TONGUE,
        ConsciousnessLevel.BODY,
        ConsciousnessLevel.MIND,
    ]
    
    def __init__(self):
        self._layers: Dict[ConsciousnessLevel, ConsciousnessLayer] = {}
        self._init_layers()
        self._pipeline_stats = {
            'total_processed': 0,
            'successful_integrations': 0,
            'avg_processing_time': 0.0
        }
    
    def _init_layers(self) -> None:
        """初始化各识层"""
        for level in ConsciousnessLevel:
            if level.is_sensory:
                self._layers[level] = SensoryConsciousnessLayer(level)
            elif level.is_sixth:
                self._layers[level] = MindConsciousnessLayer()
    
    def process_sensory(
        self,
        level: ConsciousnessLevel,
        raw_data: Any
    ) -> Tuple[ConsciousnessData, AbstractionResult]:
        """
        处理单个感官数据
        
        Args:
            level: 感官识层级别
            raw_data: 原始数据
            
        Returns:
            (处理后的数据, 抽象结果)
        """
        if not level.is_sensory:
            raise ValueError(f"{level} is not a sensory consciousness level")
        
        layer = self._layers.get(level)
        if not layer:
            raise RuntimeError(f"Layer {level} not initialized")
        
        data = ConsciousnessData(
            level=level,
            raw_input=raw_data
        )
        
        processed = layer.process(data)
        abstraction = layer.abstract(processed)
        
        return processed, abstraction
    
    def process_pipeline(
        self,
        sensory_inputs: Dict[ConsciousnessLevel, Any]
    ) -> Tuple[ConsciousnessData, List[AbstractionResult]]:
        """
        执行完整的六识流水线处理
        
        Args:
            sensory_inputs: 各感官的输入数据字典
            
        Returns:
            (最终意识处理结果, 所有抽象结果列表)
        """
        abstractions: List[AbstractionResult] = []
        
        for level in self.SENSORY_ORDER[:-1]:
            if level in sensory_inputs and sensory_inputs[level] is not None:
                _, abstraction = self.process_sensory(level, sensory_inputs[level])
                abstractions.append(abstraction)
        
        mind_layer = self._layers.get(ConsciousnessLevel.MIND)
        if not mind_layer:
            raise RuntimeError("Mind consciousness layer not initialized")
        
        if abstractions:
            mind_data = ConsciousnessData(
                level=ConsciousnessLevel.MIND,
                raw_input=abstractions
            )
        else:
            mind_data = ConsciousnessData(
                level=ConsciousnessLevel.MIND,
                raw_input=None
            )
        
        mind_result = mind_layer.process(mind_data)
        mind_abstraction = mind_layer.abstract(mind_result)
        abstractions.append(mind_abstraction)
        
        self._pipeline_stats['total_processed'] += 1
        if mind_result.confidence > 0.5:
            self._pipeline_stats['successful_integrations'] += 1
        
        return mind_result, abstractions
    
    def process_single_stream(
        self,
        level: ConsciousnessLevel,
        raw_data: Any
    ) -> ConsciousnessData:
        """
        处理单一流水线（从指定感官到意识）
        
        Args:
            level: 起始感官识层
            raw_data: 原始数据
            
        Returns:
            意识层处理结果
        """
        _, abstraction = self.process_sensory(level, raw_data)
        
        mind_layer = self._layers.get(ConsciousnessLevel.MIND)
        if not mind_layer:
            raise RuntimeError("Mind consciousness layer not initialized")
        
        mind_data = ConsciousnessData(
            level=ConsciousnessLevel.MIND,
            raw_input=abstraction
        )
        
        return mind_layer.process(mind_data)
    
    def get_layer_stats(self, level: ConsciousnessLevel) -> Dict[str, Any]:
        """获取指定识层的统计信息"""
        layer = self._layers.get(level)
        if layer:
            return layer.get_stats()
        return {}
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """获取流水线统计信息"""
        return self._pipeline_stats.copy()
    
    def get_layer(self, level: ConsciousnessLevel) -> Optional[ConsciousnessLayer]:
        """获取指定识层"""
        return self._layers.get(level)


@dataclass
class SelfCognitionReport:
    """自我认知报告"""
    report_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: datetime = field(default_factory=datetime.now)
    self_involvement_score: float = 0.0
    attachment_level: float = 0.0
    ego_strength: float = 0.0
    self_awareness_depth: float = 0.0
    identified_self_patterns: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ManasConsciousness:
    """末那识 - 自我认知模块
    
    第七识，负责监控"自我"参与程度
    恒审思量，执著于"我"
    """
    
    def __init__(self):
        self._self_patterns: List[Dict[str, Any]] = []
        self._monitoring_history: List[SelfCognitionReport] = []
        self._ego_threshold = 0.7
        self._attachment_accumulator = 0.0
        self._self_references = [
            "我", "我的", "自己", "自我", "本人", "咱们",
            "I", "me", "my", "mine", "myself"
        ]
    
    def monitor_self(
        self,
        thought_data: ConsciousnessData,
        abstraction: Optional[AbstractionResult] = None
    ) -> SelfCognitionReport:
        """
        监控"自我"参与程度
        
        Args:
            thought_data: 意识层处理的数据
            abstraction: 意识层的抽象结果
            
        Returns:
            自我认知报告
        """
        self_involvement = self._calculate_self_involvement(thought_data)
        attachment_level = self._calculate_attachment(thought_data, abstraction)
        ego_strength = self._assess_ego_strength(thought_data)
        self_awareness_depth = self._calculate_awareness_depth(thought_data)
        
        patterns = self._identify_self_patterns(thought_data)
        recommendations = self._generate_recommendations(
            self_involvement,
            attachment_level,
            ego_strength
        )
        
        report = SelfCognitionReport(
            self_involvement_score=self_involvement,
            attachment_level=attachment_level,
            ego_strength=ego_strength,
            self_awareness_depth=self_awareness_depth,
            identified_self_patterns=patterns,
            recommendations=recommendations,
            metadata={
                'thought_confidence': thought_data.confidence,
                'thought_clarity': thought_data.clarity,
                'source_level': thought_data.source_level.value if thought_data.source_level else None
            }
        )
        
        self._monitoring_history.append(report)
        if len(self._monitoring_history) > 100:
            self._monitoring_history = self._monitoring_history[-100:]
        
        self._update_self_patterns(patterns, self_involvement)
        
        return report
    
    def generate_report(
        self,
        time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> Dict[str, Any]:
        """
        生成自我认知报告
        
        Args:
            time_range: 时间范围（可选）
            
        Returns:
            综合自我认知报告
        """
        reports = self._monitoring_history
        
        if time_range:
            start, end = time_range
            reports = [
                r for r in reports
                if start <= r.timestamp <= end
            ]
        
        if not reports:
            return {
                'status': 'no_data',
                'message': '没有足够的监控数据'
            }
        
        avg_self_involvement = sum(r.self_involvement_score for r in reports) / len(reports)
        avg_attachment = sum(r.attachment_level for r in reports) / len(reports)
        avg_ego_strength = sum(r.ego_strength for r in reports) / len(reports)
        avg_awareness = sum(r.self_awareness_depth for r in reports) / len(reports)
        
        all_patterns = []
        for r in reports:
            all_patterns.extend(r.identified_self_patterns)
        
        pattern_counts = {}
        for pattern in all_patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        dominant_patterns = sorted(
            pattern_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        trend = self._analyze_trend(reports)
        
        return {
            'report_type': 'self_cognition_summary',
            'period': {
                'start': reports[0].timestamp.isoformat() if reports else None,
                'end': reports[-1].timestamp.isoformat() if reports else None,
                'sample_count': len(reports)
            },
            'metrics': {
                'average_self_involvement': round(avg_self_involvement, 3),
                'average_attachment_level': round(avg_attachment, 3),
                'average_ego_strength': round(avg_ego_strength, 3),
                'average_self_awareness': round(avg_awareness, 3)
            },
            'dominant_patterns': [
                {'pattern': p, 'frequency': c}
                for p, c in dominant_patterns
            ],
            'trend_analysis': trend,
            'recommendations': self._generate_overall_recommendations(
                avg_self_involvement,
                avg_attachment,
                avg_ego_strength
            )
        }
    
    def _calculate_self_involvement(self, data: ConsciousnessData) -> float:
        """计算自我参与程度"""
        content = data.processed_content
        involvement = 0.0
        
        text_content = ""
        if isinstance(content, dict):
            text_content = str(content.get('integrated_meaning', ''))
            text_content += str(content.get('thought', ''))
            text_content += ' '.join(content.get('key_concepts', []))
        
        for ref in self._self_references:
            if ref in text_content:
                involvement += 0.15
        
        if '我执' in str(content):
            involvement += 0.3
        
        return min(1.0, involvement)
    
    def _calculate_attachment(
        self,
        data: ConsciousnessData,
        abstraction: Optional[AbstractionResult]
    ) -> float:
        """计算执著程度"""
        attachment = self._attachment_accumulator * 0.1
        
        if data.confidence > 0.9:
            attachment += 0.1
        
        if abstraction and abstraction.importance > 0.8:
            attachment += 0.15
        
        attachment_keywords = ['必须', '一定', '绝对', '应该', '非要']
        content_str = str(data.processed_content)
        for keyword in attachment_keywords:
            if keyword in content_str:
                attachment += 0.1
        
        return min(1.0, attachment)
    
    def _assess_ego_strength(self, data: ConsciousnessData) -> float:
        """评估我执强度"""
        ego_strength = 0.3
        
        content = data.processed_content
        
        if content.get('thought_type') == 'reflective_thought':
            ego_strength += 0.2
        
        if data.clarity > 0.7:
            ego_strength += 0.1
        
        self_involvement = self._calculate_self_involvement(data)
        ego_strength += self_involvement * 0.3
        
        return min(1.0, ego_strength)
    
    def _calculate_awareness_depth(self, data: ConsciousnessData) -> float:
        """计算自我觉察深度"""
        depth = 0.2
        
        if data.processed_content.get('reasoning_chain'):
            depth += 0.2
        
        if data.processed_content.get('abstraction_level', 0) > 0.6:
            depth += 0.2
        
        if len(data.processed_content.get('key_concepts', [])) > 3:
            depth += 0.2
        
        if data.confidence > 0.7:
            depth += 0.2
        
        return min(1.0, depth)
    
    def _identify_self_patterns(self, data: ConsciousnessData) -> List[str]:
        """识别自我模式"""
        patterns = []
        content = str(data.processed_content)
        
        if any(ref in content for ref in self._self_references):
            patterns.append("自我参照")
        
        if '应该' in content or '必须' in content:
            patterns.append("规范性执著")
        
        if '对' in content and '错' in content:
            patterns.append("二元判断")
        
        if '我的' in content:
            patterns.append("占有意识")
        
        if data.confidence > 0.9:
            patterns.append("高度确定")
        
        return patterns
    
    def _generate_recommendations(
        self,
        self_involvement: float,
        attachment: float,
        ego_strength: float
    ) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if self_involvement > 0.7:
            recommendations.append("觉察过强的自我参与，尝试以更客观的视角观察")
        
        if attachment > 0.6:
            recommendations.append("注意执著倾向，练习放下对结果的期待")
        
        if ego_strength > 0.7:
            recommendations.append('观察"我执"的生起，不随之反应')
        
        if self_involvement < 0.3 and attachment < 0.3:
            recommendations.append("保持当前的清明觉察状态")
        
        return recommendations
    
    def _update_self_patterns(
        self,
        patterns: List[str],
        involvement: float
    ) -> None:
        """更新自我模式记录"""
        for pattern in patterns:
            self._self_patterns.append({
                'pattern': pattern,
                'involvement': involvement,
                'timestamp': datetime.now()
            })
        
        if len(self._self_patterns) > 1000:
            self._self_patterns = self._self_patterns[-1000:]
    
    def _analyze_trend(self, reports: List[SelfCognitionReport]) -> Dict[str, Any]:
        """分析趋势"""
        if len(reports) < 2:
            return {'trend': 'insufficient_data'}
        
        recent = reports[-min(10, len(reports)):]
        earlier = reports[-min(20, len(reports)):-min(10, len(reports))]
        
        if not earlier:
            return {'trend': 'insufficient_data'}
        
        recent_avg = sum(r.self_involvement_score for r in recent) / len(recent)
        earlier_avg = sum(r.self_involvement_score for r in earlier) / len(earlier)
        
        diff = recent_avg - earlier_avg
        
        if diff > 0.1:
            trend = 'increasing'
        elif diff < -0.1:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'change': round(diff, 3),
            'recent_average': round(recent_avg, 3),
            'earlier_average': round(earlier_avg, 3)
        }
    
    def _generate_overall_recommendations(
        self,
        avg_involvement: float,
        avg_attachment: float,
        avg_ego: float
    ) -> List[str]:
        """生成总体建议"""
        recommendations = []
        
        if avg_involvement > 0.6:
            recommendations.append("建议增加正念练习，观察自我意识的生灭")
        
        if avg_attachment > 0.5:
            recommendations.append("建议练习无常观，减少对结果的执著")
        
        if avg_ego > 0.6:
            recommendations.append('建议修习无我观，观察"我"的虚幻性')
        
        if avg_involvement < 0.4 and avg_attachment < 0.4:
            recommendations.append("当前觉察状态良好，继续保持")
        
        return recommendations
    
    def get_recent_reports(self, limit: int = 10) -> List[SelfCognitionReport]:
        """获取最近的监控报告"""
        return self._monitoring_history[-limit:]


@dataclass
class AlayaSeed:
    """阿赖耶识种子"""
    seed_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    content: Any = None
    seed_type: str = "general"
    strength: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    last_activated: datetime = field(default_factory=datetime.now)
    activation_count: int = 0
    source_trace: List[str] = field(default_factory=list)
    karmic_weight: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def activate(self) -> None:
        """激活种子"""
        self.last_activated = datetime.now()
        self.activation_count += 1
    
    def strengthen(self, amount: float = 0.1) -> None:
        """增强种子"""
        self.strength = min(2.0, self.strength + amount)


class AlayaConsciousness:
    """阿赖耶识 - 根本存储层
    
    第八识，永久保存重要记忆
    不受普通衰减机制影响
    含藏一切种子
    """
    
    def __init__(self):
        self._seeds: Dict[str, AlayaSeed] = {}
        self._index_by_type: Dict[str, List[str]] = {}
        self._index_by_time: List[Tuple[datetime, str]] = []
        self._karmic_accumulator: float = 0.0
        self._importance_threshold = 0.7
    
    def store(
        self,
        content: Any,
        seed_type: str = "general",
        importance: float = 0.5,
        source_trace: Optional[List[str]] = None,
        karmic_weight: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AlayaSeed:
        """
        永久保存重要记忆
        
        Args:
            content: 存储内容
            seed_type: 种子类型
            importance: 重要程度
            source_trace: 来源追溯
            karmic_weight: 业力权重
            metadata: 元数据
            
        Returns:
            创建的种子
        """
        if importance < self._importance_threshold:
            existing_seed = self._find_similar_seed(content, seed_type)
            if existing_seed:
                existing_seed.strengthen(0.05)
                existing_seed.activate()
                return existing_seed
        
        seed = AlayaSeed(
            content=content,
            seed_type=seed_type,
            strength=1.0 + (importance - 0.5),
            source_trace=source_trace or [],
            karmic_weight=karmic_weight,
            metadata=metadata or {}
        )
        
        self._seeds[seed.seed_id] = seed
        
        if seed_type not in self._index_by_type:
            self._index_by_type[seed_type] = []
        self._index_by_type[seed_type].append(seed.seed_id)
        
        self._index_by_time.append((seed.created_at, seed.seed_id))
        self._index_by_time.sort(key=lambda x: x[0], reverse=True)
        
        self._karmic_accumulator += karmic_weight
        
        return seed
    
    def retrieve(
        self,
        query: Optional[str] = None,
        seed_type: Optional[str] = None,
        time_range: Optional[Tuple[datetime, datetime]] = None,
        min_strength: float = 0.0,
        limit: int = 10
    ) -> List[AlayaSeed]:
        """
        检索根本记忆
        
        Args:
            query: 查询关键词
            seed_type: 种子类型过滤
            time_range: 时间范围
            min_strength: 最小强度
            limit: 返回数量限制
            
        Returns:
            匹配的种子列表
        """
        candidates = list(self._seeds.values())
        
        if seed_type:
            candidates = [s for s in candidates if s.seed_type == seed_type]
        
        if time_range:
            start, end = time_range
            candidates = [
                s for s in candidates
                if start <= s.created_at <= end
            ]
        
        if min_strength > 0:
            candidates = [s for s in candidates if s.strength >= min_strength]
        
        if query:
            candidates = self._search_by_query(candidates, query)
        
        candidates.sort(key=lambda s: (
            -s.strength,
            -s.activation_count,
            -s.karmic_weight
        ))
        
        results = candidates[:limit]
        
        for seed in results:
            seed.activate()
        
        return results
    
    def retrieve_by_association(
        self,
        seed_id: str,
        depth: int = 1
    ) -> List[AlayaSeed]:
        """
        通过关联检索
        
        Args:
            seed_id: 起始种子ID
            depth: 关联深度
            
        Returns:
            关联的种子列表
        """
        if seed_id not in self._seeds:
            return []
        
        start_seed = self._seeds[seed_id]
        related = []
        
        for trace_id in start_seed.source_trace:
            if trace_id in self._seeds:
                related.append(self._seeds[trace_id])
        
        for other_seed in self._seeds.values():
            if seed_id in other_seed.source_trace:
                related.append(other_seed)
        
        return list(set(related))
    
    def get_seed(self, seed_id: str) -> Optional[AlayaSeed]:
        """获取指定种子"""
        seed = self._seeds.get(seed_id)
        if seed:
            seed.activate()
        return seed
    
    def plant_seed(
        self,
        abstraction: AbstractionResult,
        consciousness_report: Optional[SelfCognitionReport] = None
    ) -> AlayaSeed:
        """
        从抽象结果和自我认知报告种植种子
        
        Args:
            abstraction: 抽象结果
            consciousness_report: 自我认知报告
            
        Returns:
            创建的种子
        """
        karmic_weight = 0.0
        if consciousness_report:
            karmic_weight = consciousness_report.attachment_level * 0.5
        
        return self.store(
            content={
                'essence': abstraction.essence,
                'abstracted_content': abstraction.abstracted_content,
                'associations': abstraction.associations
            },
            seed_type=f"consciousness_{abstraction.source_level.value}",
            importance=abstraction.importance,
            source_trace=[abstraction.source_level.value],
            karmic_weight=karmic_weight,
            metadata={
                'source_level': abstraction.source_level.value,
                'target_level': abstraction.target_level.value
            }
        )
    
    def get_karmic_state(self) -> Dict[str, Any]:
        """获取业力状态"""
        total_seeds = len(self._seeds)
        total_karma = self._karmic_accumulator
        avg_strength = (
            sum(s.strength for s in self._seeds.values()) / total_seeds
            if total_seeds > 0 else 0
        )
        
        type_distribution = {
            seed_type: len(seeds)
            for seed_type, seeds in self._index_by_type.items()
        }
        
        return {
            'total_seeds': total_seeds,
            'total_karmic_weight': round(total_karma, 3),
            'average_seed_strength': round(avg_strength, 3),
            'type_distribution': type_distribution,
            'karmic_balance': 'positive' if total_karma > 0 else 'neutral'
        }
    
    def _find_similar_seed(
        self,
        content: Any,
        seed_type: str
    ) -> Optional[AlayaSeed]:
        """查找相似种子"""
        content_str = str(content)
        content_hash = self._hash_content(content)
        
        for seed in self._seeds.values():
            if seed.seed_type != seed_type:
                continue
            
            if self._hash_content(seed.content) == content_hash:
                return seed
            
            if content_str in str(seed.content) or str(seed.content) in content_str:
                return seed
        
        return None
    
    def _search_by_query(
        self,
        candidates: List[AlayaSeed],
        query: str
    ) -> List[AlayaSeed]:
        """通过查询搜索"""
        results = []
        query_lower = query.lower()
        
        for seed in candidates:
            content_str = str(seed.content).lower()
            metadata_str = str(seed.metadata).lower()
            
            if query_lower in content_str or query_lower in metadata_str:
                results.append(seed)
        
        return results
    
    def _hash_content(self, content: Any) -> str:
        """生成内容哈希"""
        try:
            content_str = json.dumps(content, sort_keys=True, default=str)
            return hashlib.md5(content_str.encode()).hexdigest()
        except:
            return hashlib.md5(str(content).encode()).hexdigest()
    
    def get_all_seeds(self) -> List[AlayaSeed]:
        """获取所有种子"""
        return list(self._seeds.values())
    
    def get_seeds_by_type(self, seed_type: str) -> List[AlayaSeed]:
        """按类型获取种子"""
        seed_ids = self._index_by_type.get(seed_type, [])
        return [self._seeds[sid] for sid in seed_ids if sid in self._seeds]


class EightConsciousnessSystem:
    """八识系统完整集成"""
    
    def __init__(self):
        self.pipeline = SixSensesPipeline()
        self.manas = ManasConsciousness()
        self.alaya = AlayaConsciousness()
        self._processing_history: List[Dict[str, Any]] = []
    
    def process(
        self,
        sensory_inputs: Dict[ConsciousnessLevel, Any],
        store_to_alaya: bool = True
    ) -> Dict[str, Any]:
        """
        完整的八识处理流程
        
        Args:
            sensory_inputs: 各感官输入
            store_to_alaya: 是否存储到阿赖耶识
            
        Returns:
            处理结果
        """
        mind_result, abstractions = self.pipeline.process_pipeline(sensory_inputs)
        
        mind_abstraction = abstractions[-1] if abstractions else None
        consciousness_report = self.manas.monitor_self(mind_result, mind_abstraction)
        
        alaya_seed = None
        if store_to_alaya and mind_abstraction:
            alaya_seed = self.alaya.plant_seed(mind_abstraction, consciousness_report)
        
        result = {
            'mind_result': {
                'data_id': mind_result.data_id,
                'processed_content': mind_result.processed_content,
                'confidence': mind_result.confidence,
                'clarity': mind_result.clarity
            },
            'consciousness_report': {
                'self_involvement': consciousness_report.self_involvement_score,
                'attachment_level': consciousness_report.attachment_level,
                'ego_strength': consciousness_report.ego_strength,
                'patterns': consciousness_report.identified_self_patterns,
                'recommendations': consciousness_report.recommendations
            },
            'abstractions': [
                {
                    'source': a.source_level.value,
                    'essence': a.essence,
                    'importance': a.importance
                }
                for a in abstractions
            ]
        }
        
        if alaya_seed:
            result['alaya_seed'] = {
                'seed_id': alaya_seed.seed_id,
                'seed_type': alaya_seed.seed_type,
                'strength': alaya_seed.strength
            }
        
        self._processing_history.append({
            'timestamp': datetime.now(),
            'result': result
        })
        
        if len(self._processing_history) > 100:
            self._processing_history = self._processing_history[-100:]
        
        return result
    
    def get_system_state(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            'pipeline_stats': self.pipeline.get_pipeline_stats(),
            'karmic_state': self.alaya.get_karmic_state(),
            'recent_processing_count': len(self._processing_history)
        }
    
    def generate_self_cognition_report(
        self,
        time_range: Optional[Tuple[datetime, datetime]] = None
    ) -> Dict[str, Any]:
        """生成自我认知报告"""
        return self.manas.generate_report(time_range)
