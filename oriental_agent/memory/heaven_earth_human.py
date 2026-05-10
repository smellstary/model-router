"""
Heaven-Earth-Human Three-layer Memory Architecture
天地人三层记忆架构
"""

from typing import Dict, List, Optional, Set
from datetime import datetime
from core.types import MemoryLayer, MemoryNode, HexagramType, WuxingType


class HeavenLayer:
    """天道层 - 存储宏观规律与普遍法则记忆"""
    
    def __init__(self):
        self.macro_memories: Dict[str, MemoryNode] = {}
        self.principles: Dict[str, str] = {}
        self.causal_models: Dict[str, any] = {}
        self.universal_laws: List[str] = []
    
    def store_principle(self, principle_id: str, content: any, model: str = None) -> None:
        """存储宏观原理"""
        self.principles[principle_id] = content
        if model:
            self.causal_models[principle_id] = model
    
    def store_universal_law(self, law: str) -> None:
        """存储普遍法则"""
        if law not in self.universal_laws:
            self.universal_laws.append(law)
    
    def get_principles(self, domain: Optional[str] = None) -> List[str]:
        """获取相关原理"""
        if domain:
            return [p for p in self.principles.values() if domain in str(p)]
        return list(self.principles.values())
    
    def find_applicable_laws(self, context: str) -> List[str]:
        """查找适用的普遍法则"""
        applicable = []
        for law in self.universal_laws:
            if any(keyword in law for keyword in context.split()):
                applicable.append(law)
        return applicable
    
    def get_memory_count(self) -> int:
        """获取记忆数量"""
        return len(self.macro_memories)
    
    def get_all_memories(self) -> List[MemoryNode]:
        """获取所有记忆"""
        return list(self.macro_memories.values())


class EarthLayer:
    """地道层 - 存储环境交互与外部刺激记忆"""
    
    def __init__(self):
        self.environmental_memories: Dict[str, MemoryNode] = {}
        self.stimulus_patterns: Dict[str, int] = {}
        self.interaction_history: List[Dict] = []
        self.adaptation_models: Dict[str, float] = {}
    
    def store_interaction(
        self,
        interaction_id: str,
        content: any,
        stimulus_type: str,
        response: any
    ) -> None:
        """存储环境交互记忆"""
        self.interaction_history.append({
            'id': interaction_id,
            'stimulus': stimulus_type,
            'response': response,
            'timestamp': datetime.now()
        })
        
        if stimulus_type not in self.stimulus_patterns:
            self.stimulus_patterns[stimulus_type] = 0
        self.stimulus_patterns[stimulus_type] += 1
    
    def get_adapted_response(self, stimulus: str) -> Optional[any]:
        """获取适应性的响应"""
        for interaction in reversed(self.interaction_history):
            if interaction.get('stimulus') == stimulus:
                return interaction.get('response')
        return None
    
    def get_stimulus_frequency(self, stimulus_type: str) -> int:
        """获取刺激类型频率"""
        return self.stimulus_patterns.get(stimulus_type, 0)
    
    def update_adaptation_model(self, context: str, adaptation_level: float) -> None:
        """更新适应模型"""
        self.adaptation_models[context] = adaptation_level
    
    def get_memory_count(self) -> int:
        """获取记忆数量"""
        return len(self.environmental_memories)
    
    def get_all_memories(self) -> List[MemoryNode]:
        """获取所有记忆"""
        return list(self.environmental_memories.values())


class HumanLayer:
    """人道层 - 存储主体经验与决策历史记忆"""
    
    def __init__(self):
        self.experience_memories: Dict[str, MemoryNode] = {}
        self.decision_history: List[Dict] = {}
        self.execution_traces: List[Dict] = {}
        self.self_models: Dict[str, any] = {}
        self.capability_bounds: Dict[str, tuple] = {}
    
    def store_experience(
        self,
        experience_id: str,
        content: any,
        decision: any,
        outcome: any
    ) -> None:
        """存储经验记忆"""
        self.experience_memories[experience_id] = {
            'content': content,
            'decision': decision,
            'outcome': outcome,
            'timestamp': datetime.now()
        }
        
        if experience_id not in self.decision_history:
            self.decision_history[experience_id] = []
        self.decision_history[experience_id].append({
            'decision': decision,
            'outcome': outcome,
            'time': datetime.now()
        })
    
    def record_execution_trace(self, trace_id: str, trace_data: Dict) -> None:
        """记录执行轨迹"""
        self.execution_traces[trace_id] = trace_data
    
    def update_self_model(self, model_type: str, model_data: any) -> None:
        """更新自我模型"""
        self.self_models[model_type] = model_data
    
    def update_capability_bounds(
        self,
        capability: str,
        lower: float,
        upper: float
    ) -> None:
        """更新能力边界"""
        self.capability_bounds[capability] = (lower, upper)
    
    def get_recent_experiences(self, limit: int = 10) -> List[Dict]:
        """获取最近的经验"""
        experiences = list(self.experience_memories.values())
        experiences.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
        return experiences[:limit]
    
    def evaluate_decision_quality(
        self,
        decision: any,
        expected_outcome: any
    ) -> float:
        """评估决策质量"""
        quality_score = 0.5
        
        for exp in self.experience_memories.values():
            if exp.get('decision') == decision:
                if exp.get('outcome') == expected_outcome:
                    quality_score += 0.1
                else:
                    quality_score -= 0.1
        
        return max(0.0, min(1.0, quality_score))
    
    def get_memory_count(self) -> int:
        """获取记忆数量"""
        return len(self.experience_memories)
    
    def get_all_memories(self) -> List[MemoryNode]:
        """获取所有记忆"""
        return list(self.experience_memories.values())


class ThreeLayerMemoryArchitecture:
    """天地人三层记忆架构整合"""
    
    def __init__(self):
        self.heaven_layer = HeavenLayer()
        self.earth_layer = EarthLayer()
        self.human_layer = HumanLayer()
        self.cross_layer_associations: Dict[str, List[str]] = {}
    
    def store(self, memory: MemoryNode) -> None:
        """存储记忆到对应层次"""
        layer = memory.layer
        
        if layer == MemoryLayer.HEAVEN:
            self.heaven_layer.macro_memories[memory.memory_id] = memory
        elif layer == MemoryLayer.EARTH:
            self.earth_layer.environmental_memories[memory.memory_id] = memory
        elif layer == MemoryLayer.HUMAN:
            self.human_layer.experience_memories[memory.memory_id] = memory
        
        self._establish_cross_layer_associations(memory)
    
    def retrieve(
        self,
        layer: Optional[MemoryLayer] = None,
        memory_id: Optional[str] = None
    ) -> List[MemoryNode]:
        """从指定层次检索记忆"""
        if memory_id:
            if layer == MemoryLayer.HEAVEN:
                memory = self.heaven_layer.macro_memories.get(memory_id)
            elif layer == MemoryLayer.EARTH:
                memory = self.earth_layer.environmental_memories.get(memory_id)
            elif layer == MemoryLayer.HUMAN:
                memory = self.human_layer.experience_memories.get(memory_id)
            else:
                memory = self._find_memory_across_layers(memory_id)
            return [memory] if memory else []
        
        if layer == MemoryLayer.HEAVEN:
            return self.heaven_layer.get_all_memories()
        elif layer == MemoryLayer.EARTH:
            return self.earth_layer.get_all_memories()
        elif layer == MemoryLayer.HUMAN:
            return self.human_layer.get_all_memories()
        else:
            return self._get_all_memories()
    
    def _find_memory_across_layers(self, memory_id: str) -> Optional[MemoryNode]:
        """跨层次查找记忆"""
        for layer_memories in [
            self.heaven_layer.macro_memories,
            self.earth_layer.environmental_memories,
            self.human_layer.experience_memories
        ]:
            if memory_id in layer_memories:
                return layer_memories[memory_id]
        return None
    
    def _establish_cross_layer_associations(self, memory: MemoryNode) -> None:
        """建立跨层次关联"""
        associations = []
        
        if memory.layer == MemoryLayer.HEAVEN:
            for earth_mem in self.earth_layer.environmental_memories.values():
                if self._has_semantic_relation(memory.content, earth_mem.content):
                    associations.append(earth_mem.memory_id)
        elif memory.layer == MemoryLayer.EARTH:
            for heaven_mem in self.heaven_layer.macro_memories.values():
                if self._has_semantic_relation(memory.content, heaven_mem.content):
                    associations.append(heaven_mem.memory_id)
            for human_mem in self.human_layer.experience_memories.values():
                if self._has_semantic_relation(memory.content, human_mem.content):
                    associations.append(human_mem.memory_id)
        elif memory.layer == MemoryLayer.HUMAN:
            for earth_mem in self.earth_layer.environmental_memories.values():
                if self._has_semantic_relation(memory.content, earth_mem.content):
                    associations.append(earth_mem.memory_id)
        
        if associations:
            self.cross_layer_associations[memory.memory_id] = associations
    
    def _has_semantic_relation(self, content1: any, content2: any) -> bool:
        """判断语义关联性"""
        if isinstance(content1, str) and isinstance(content2, str):
            common_words = set(content1.split()) & set(content2.split())
            return len(common_words) > 2
        return content1 == content2
    
    def get_heaven_insights(self, context: str) -> List[str]:
        """从天道层获取洞见"""
        insights = []
        
        for principle in self.heaven_layer.principles.values():
            if isinstance(principle, str) and context in principle:
                insights.append(principle)
        
        for law in self.heaven_layer.universal_laws:
            if any(keyword in law for keyword in context.split()):
                insights.append(law)
        
        return insights
    
    def get_earth_adaptations(self, context: str) -> List[Dict]:
        """从地道层获取适应经验"""
        adaptations = []
        
        for interaction in self.earth_layer.interaction_history[-20:]:
            if context in str(interaction):
                adaptations.append(interaction)
        
        return adaptations
    
    def get_human_experiences(self, context: str) -> List[Dict]:
        """从人道层获取相关经验"""
        experiences = []
        
        for exp in self.human_layer.experience_memories.values():
            if context in str(exp.get('content', '')):
                experiences.append(exp)
        
        return experiences
    
    def integrated_retrieval(self, context: str) -> Dict[str, List]:
        """整合检索，返回天地人三层的综合结果"""
        return {
            'heaven_insights': self.get_heaven_insights(context),
            'earth_adaptations': self.get_earth_adaptations(context),
            'human_experiences': self.get_human_experiences(context)
        }
    
    def _get_all_memories(self) -> List[MemoryNode]:
        """获取所有层次的所有记忆"""
        all_memories = []
        all_memories.extend(self.heaven_layer.get_all_memories())
        all_memories.extend(self.earth_layer.get_all_memories())
        all_memories.extend(self.human_layer.get_all_memories())
        return all_memories
    
    def get_layer_counts(self) -> Dict[MemoryLayer, int]:
        """获取各层记忆数量"""
        return {
            MemoryLayer.HEAVEN: self.heaven_layer.get_memory_count(),
            MemoryLayer.EARTH: self.earth_layer.get_memory_count(),
            MemoryLayer.HUMAN: self.human_layer.get_memory_count()
        }
    
    def promote_memory(self, memory_id: str) -> bool:
        """提升记忆层次（从地道到人道，从人道到天道）"""
        memory = self._find_memory_across_layers(memory_id)
        if not memory:
            return False
        
        if memory.layer == MemoryLayer.EARTH:
            memory.layer = MemoryLayer.HUMAN
            self.earth_layer.environmental_memories.pop(memory_id, None)
            self.human_layer.experience_memories[memory_id] = memory
            return True
        elif memory.layer == MemoryLayer.HUMAN:
            memory.layer = MemoryLayer.HEAVEN
            self.human_layer.experience_memories.pop(memory_id, None)
            self.heaven_layer.macro_memories[memory_id] = memory
            return True
        
        return False
    
    def descend_memory(self, memory_id: str) -> bool:
        """降级记忆层次（从天道到人道，从人道到地道）"""
        memory = self._find_memory_across_layers(memory_id)
        if not memory:
            return False
        
        if memory.layer == MemoryLayer.HEAVEN:
            memory.layer = MemoryLayer.HUMAN
            self.heaven_layer.macro_memories.pop(memory_id, None)
            self.human_layer.experience_memories[memory_id] = memory
            return True
        elif memory.layer == MemoryLayer.HUMAN:
            memory.layer = MemoryLayer.EARTH
            self.human_layer.experience_memories.pop(memory_id, None)
            self.earth_layer.environmental_memories[memory_id] = memory
            return True
        
        return False
