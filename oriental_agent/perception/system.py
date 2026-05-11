"""
Perception System based on Buddhist Six Consciousnesses (六识)
感知系统 - 基于佛家六识理论
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto


class SenseType(Enum):
    """感知类型 - 六识"""
    VISUAL = "眼识"
    AUDITORY = "耳识"
    OLFACTORY = "鼻识"
    GUSTATORY = "舌识"
    TACTILE = "身识"
    MENTAL = "意识"


@dataclass
class PerceptionData:
    """感知数据"""
    perception_id: str
    sense_type: SenseType
    raw_data: Any
    processed_features: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    confidence: float = 0.0
    attention_weight: float = 1.0
    emotional_tag: Optional[str] = None


@dataclass
class ConsciousnessState:
    """意识状态"""
    awareness_level: float
    focus_point: Optional[str]
    mental_clarity: float
    distraction_level: float


class SixSensesProcessor:
    """六识处理器"""
    
    def __init__(self):
        self.sense_priorities = {
            SenseType.VISUAL: 1.0,
            SenseType.AUDITORY: 0.9,
            SenseType.MENTAL: 0.95,
            SenseType.TACTILE: 0.7,
            SenseType.OLFACTORY: 0.5,
            SenseType.GUSTATORY: 0.5
        }
        self.sense_history: Dict[SenseType, List[PerceptionData]] = {
            sense: [] for sense in SenseType
        }
    
    def process_visual(self, raw_data: Any) -> PerceptionData:
        """处理视觉信息（眼识）"""
        perception_id = f"visual_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        features = self._extract_visual_features(raw_data)
        
        return PerceptionData(
            perception_id=perception_id,
            sense_type=SenseType.VISUAL,
            raw_data=raw_data,
            processed_features=features,
            confidence=self._calculate_visual_confidence(features),
            attention_weight=self.sense_priorities[SenseType.VISUAL]
        )
    
    def _extract_visual_features(self, raw_data: Any) -> Dict[str, Any]:
        """提取视觉特征"""
        features = {
            'objects_detected': [],
            'colors': [],
            'spatial_relations': {},
            'motion_detected': False,
            'scene_type': 'unknown'
        }
        
        if isinstance(raw_data, dict):
            features.update({
                'objects_detected': raw_data.get('objects', []),
                'scene_type': raw_data.get('scene', 'unknown'),
                'motion_detected': raw_data.get('has_motion', False)
            })
        
        return features
    
    def _calculate_visual_confidence(self, features: Dict) -> float:
        """计算视觉置信度"""
        confidence = 0.5
        
        if features.get('objects_detected'):
            confidence += 0.2
        if features.get('scene_type') != 'unknown':
            confidence += 0.2
        
        return min(1.0, confidence)
    
    def process_auditory(self, raw_data: Any) -> PerceptionData:
        """处理听觉信息（耳识）"""
        perception_id = f"auditory_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        features = self._extract_auditory_features(raw_data)
        
        return PerceptionData(
            perception_id=perception_id,
            sense_type=SenseType.AUDITORY,
            raw_data=raw_data,
            processed_features=features,
            confidence=self._calculate_auditory_confidence(features),
            attention_weight=self.sense_priorities[SenseType.AUDITORY],
            emotional_tag=features.get('emotional_tone')
        )
    
    def _extract_auditory_features(self, raw_data: Any) -> Dict[str, Any]:
        """提取听觉特征"""
        features = {
            'speech_content': '',
            'speaker': None,
            'emotional_tone': None,
            'volume_level': 0.5,
            'sound_events': []
        }
        
        if isinstance(raw_data, dict):
            features.update({
                'speech_content': raw_data.get('speech', ''),
                'speaker': raw_data.get('speaker'),
                'emotional_tone': raw_data.get('emotion'),
                'volume_level': raw_data.get('volume', 0.5)
            })
        
        return features
    
    def _calculate_auditory_confidence(self, features: Dict) -> float:
        """计算听觉置信度"""
        confidence = 0.5
        
        if features.get('speech_content'):
            confidence += 0.3
        if features.get('speaker'):
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def process_olfactory(self, raw_data: Any) -> PerceptionData:
        """处理嗅觉信息（鼻识）"""
        perception_id = f"olfactory_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        features = self._extract_olfactory_features(raw_data)
        
        return PerceptionData(
            perception_id=perception_id,
            sense_type=SenseType.OLFACTORY,
            raw_data=raw_data,
            processed_features=features,
            confidence=0.6,
            attention_weight=self.sense_priorities[SenseType.OLFACTORY]
        )
    
    def _extract_olfactory_features(self, raw_data: Any) -> Dict[str, Any]:
        """提取嗅觉特征"""
        features = {
            'smell_type': 'neutral',
            'intensity': 0.0,
            'pleasantness': 0.5
        }
        
        if isinstance(raw_data, dict):
            features.update({
                'smell_type': raw_data.get('type', 'neutral'),
                'intensity': raw_data.get('intensity', 0.0)
            })
        
        return features
    
    def process_gustatory(self, raw_data: Any) -> PerceptionData:
        """处理味觉信息（舌识）"""
        perception_id = f"gustatory_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        features = self._extract_gustatory_features(raw_data)
        
        return PerceptionData(
            perception_id=perception_id,
            sense_type=SenseType.GUSTATORY,
            raw_data=raw_data,
            processed_features=features,
            confidence=0.5,
            attention_weight=self.sense_priorities[SenseType.GUSTATORY]
        )
    
    def _extract_gustatory_features(self, raw_data: Any) -> Dict[str, Any]:
        """提取味觉特征"""
        features = {
            'taste_type': 'neutral',
            'intensity': 0.0,
            'flavor_notes': []
        }
        
        if isinstance(raw_data, dict):
            features.update({
                'taste_type': raw_data.get('type', 'neutral'),
                'flavor_notes': raw_data.get('notes', [])
            })
        
        return features
    
    def process_tactile(self, raw_data: Any) -> PerceptionData:
        """处理触觉信息（身识）"""
        perception_id = f"tactile_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        features = self._extract_tactile_features(raw_data)
        
        return PerceptionData(
            perception_id=perception_id,
            sense_type=SenseType.TACTILE,
            raw_data=raw_data,
            processed_features=features,
            confidence=0.7,
            attention_weight=self.sense_priorities[SenseType.TACTILE]
        )
    
    def _extract_tactile_features(self, raw_data: Any) -> Dict[str, Any]:
        """提取触觉特征"""
        features = {
            'pressure': 0.5,
            'temperature': 0.5,
            'texture': 'smooth',
            'pain_level': 0.0
        }
        
        if isinstance(raw_data, dict):
            features.update({
                'pressure': raw_data.get('pressure', 0.5),
                'temperature': raw_data.get('temperature', 0.5)
            })
        
        return features
    
    def process_mental(self, raw_data: Any) -> PerceptionData:
        """处理意识信息（意识）"""
        perception_id = f"mental_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        features = self._extract_mental_features(raw_data)
        
        return PerceptionData(
            perception_id=perception_id,
            sense_type=SenseType.MENTAL,
            raw_data=raw_data,
            processed_features=features,
            confidence=0.8,
            attention_weight=self.sense_priorities[SenseType.MENTAL]
        )
    
    def _extract_mental_features(self, raw_data: Any) -> Dict[str, Any]:
        """提取意识特征"""
        features = {
            'thought_content': str(raw_data),
            'abstraction_level': 0.5,
            'emotional_tone': None,
            'logical_coherence': 0.7
        }
        
        if isinstance(raw_data, dict):
            features.update({
                'thought_content': raw_data.get('thought', str(raw_data)),
                'emotional_tone': raw_data.get('emotion')
            })
        
        return features
    
    def store_perception(self, perception: PerceptionData) -> None:
        """存储感知历史"""
        self.sense_history[perception.sense_type].append(perception)
        
        if len(self.sense_history[perception.sense_type]) > 100:
            self.sense_history[perception.sense_type] = \
                self.sense_history[perception.sense_type][-100:]
    
    def get_recent_perceptions(
        self,
        sense_type: Optional[SenseType] = None,
        limit: int = 10
    ) -> List[PerceptionData]:
        """获取最近的感知"""
        if sense_type:
            return self.sense_history.get(sense_type, [])[-limit:]
        
        all_perceptions = []
        for perceptions in self.sense_history.values():
            all_perceptions.extend(perceptions)
        
        return sorted(all_perceptions, key=lambda p: p.timestamp, reverse=True)[:limit]


class ConsciousnessIntegrator:
    """意识整合器 - 综合处理六识信息"""
    
    def __init__(self):
        self.integrated_context: Dict[str, Any] = {}
        self.awareness_level = 1.0
        self.focus_point: Optional[str] = None
    
    def integrate(
        self,
        perceptions: List[PerceptionData]
    ) -> Dict[str, Any]:
        """整合六识信息"""
        if not perceptions:
            return {'status': 'no_input'}
        
        integrated = {
            'timestamp': datetime.now(),
            'senses_active': [p.sense_type.value for p in perceptions],
            'total_confidence': sum(p.confidence for p in perceptions) / len(perceptions),
            'attention_weights': {p.sense_type.value: p.attention_weight for p in perceptions},
            'integrated_meaning': self._derive_meaning(perceptions),
            'scene_understanding': self._understand_scene(perceptions),
            'emotional_state': self._assess_emotional_state(perceptions),
            'awareness_level': self._calculate_awareness(perceptions)
        }
        
        self.integrated_context = integrated
        return integrated
    
    def _derive_meaning(self, perceptions: List[PerceptionData]) -> str:
        """推导综合意义"""
        meanings = []
        
        for perception in perceptions:
            features = perception.processed_features
            if 'speech_content' in features and features['speech_content']:
                meanings.append(features['speech_content'])
            elif 'objects_detected' in features and features['objects_detected']:
                meanings.append(f"观察到{len(features['objects_detected'])}个物体")
        
        return meanings[0] if meanings else "综合感知"
    
    def _understand_scene(self, perceptions: List[PerceptionData]) -> Dict[str, Any]:
        """理解场景"""
        scene_info = {
            'environment': 'unknown',
            'objects_present': [],
            'activities': [],
            'context': 'general'
        }
        
        for perception in perceptions:
            if perception.sense_type == SenseType.VISUAL:
                features = perception.processed_features
                if 'scene_type' in features:
                    scene_info['environment'] = features['scene_type']
                if 'objects_detected' in features:
                    scene_info['objects_present'] = features['objects_detected']
        
        return scene_info
    
    def _assess_emotional_state(self, perceptions: List[PerceptionData]) -> Dict[str, Any]:
        """评估情感状态"""
        emotions = []
        
        for perception in perceptions:
            if perception.emotional_tag:
                emotions.append(perception.emotional_tag)
        
        if not emotions:
            return {'dominant': 'neutral', 'intensity': 0.0}
        
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        dominant = max(emotion_counts.items(), key=lambda x: x[1])[0]
        
        return {
            'dominant': dominant,
            'intensity': emotion_counts[dominant] / len(emotions),
            'emotions_detected': emotions
        }
    
    def _calculate_awareness(self, perceptions: List[PerceptionData]) -> float:
        """计算意识清晰度"""
        if not perceptions:
            return 0.0
        
        awareness = sum(p.confidence * p.attention_weight for p in perceptions)
        awareness /= len(perceptions)
        
        self.awareness_level = awareness
        return awareness
    
    def attend_to(
        self,
        focus: str,
        perceptions: List[PerceptionData]
    ) -> Optional[PerceptionData]:
        """注意力聚焦"""
        self.focus_point = focus
        
        for perception in perceptions:
            features_str = str(perception.processed_features)
            if focus in features_str or focus in str(perception.raw_data):
                perception.attention_weight *= 1.5
                return perception
        
        return None
    
    def get_consciousness_state(self) -> ConsciousnessState:
        """获取意识状态"""
        return ConsciousnessState(
            awareness_level=self.awareness_level,
            focus_point=self.focus_point,
            mental_clarity=0.8 if self.awareness_level > 0.7 else 0.5,
            distraction_level=1.0 - self.awareness_level
        )


class PerceptionSystem:
    """感知系统主类"""
    
    def __init__(self, config=None):
        self.config = config
        self.six_senses = SixSensesProcessor()
        self.consciousness = ConsciousnessIntegrator()
        self._perception_buffer: List[PerceptionData] = []
    
    def perceive(
        self,
        sense_type: Any,
        raw_data: Any
    ) -> PerceptionData:
        """执行感知处理"""
        processor_map = {
            SenseType.VISUAL: self.six_senses.process_visual,
            SenseType.AUDITORY: self.six_senses.process_auditory,
            SenseType.OLFACTORY: self.six_senses.process_olfactory,
            SenseType.GUSTATORY: self.six_senses.process_gustatory,
            SenseType.TACTILE: self.six_senses.process_tactile,
            SenseType.MENTAL: self.six_senses.process_mental
        }
        
        sense_value = sense_type.value if isinstance(sense_type, Enum) else str(sense_type)
        
        for st, processor in processor_map.items():
            if st.value == sense_value:
                perception = processor(raw_data)
                self.six_senses.store_perception(perception)
                self._perception_buffer.append(perception)
                if len(self._perception_buffer) > 50:
                    self._perception_buffer = self._perception_buffer[-50:]
                return perception
        
        raise ValueError(f"Unknown sense type: {sense_type}")
        
        if len(self._perception_buffer) > 50:
            self._perception_buffer = self._perception_buffer[-50:]
        
        return perception
    
    def integrate(self, perceptions: List[PerceptionData]) -> Dict[str, Any]:
        """多通道感知整合"""
        return self.consciousness.integrate(perceptions)
    
    def attend_to(
        self,
        focus: str
    ) -> Optional[PerceptionData]:
        """注意力聚焦"""
        return self.consciousness.attend_to(focus, self._perception_buffer)
    
    def forward_to_memory(self, perception: PerceptionData) -> Dict[str, Any]:
        """传递感知到记忆系统"""
        return {
            'content': perception.processed_features,
            'perception_id': perception.perception_id,
            'sense_type': perception.sense_type.value,
            'timestamp': perception.timestamp.isoformat(),
            'confidence': perception.confidence
        }
    
    def get_system_state(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            'senses_active': [sense.value for sense in SenseType],
            'buffer_size': len(self._perception_buffer),
            'consciousness_state': {
                'awareness_level': self.consciousness.awareness_level,
                'focus_point': self.consciousness.focus_point
            },
            'sense_priorities': {
                sense.value: priority 
                for sense, priority in self.six_senses.sense_priorities.items()
            }
        }
