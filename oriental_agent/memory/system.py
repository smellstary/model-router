"""
Main Memory System - Integration of all memory components
记忆系统主模块 - 整合所有记忆组件
"""

import asyncio
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from core.types import (
    MemoryNode, MemoryAssociation, MemoryQuery, MemoryLayer,
    HexagramType, WuxingType, AssociationType, WuxingRelation,
    TianganType, DizhiType, QueryType
)
from memory.wuxing import WuxingSystem
from memory.yinyang import YinYangSystem
from memory.heaven_earth_human import ThreeLayerMemoryArchitecture
from memory.tiangan_dizhi import TianganDizhiSystem
from memory.hexagram_predictor import HexagramTransitionModel, TuibeituSequencePredictor
from config.settings import get_config


class MemorySystem:
    """融合易经理法的记忆系统主类"""
    
    def __init__(self, config=None):
        self.config = config or get_config()
        
        self.three_layer_architecture = ThreeLayerMemoryArchitecture()
        self.wuxing_system = WuxingSystem()
        self.yinyang_system = YinYangSystem()
        self.tiangan_dizhi_system = TianganDizhiSystem()
        self.hexagram_model = HexagramTransitionModel()
        self.predictor = TuibeituSequencePredictor()
        
        self._memory_index: Dict[str, MemoryNode] = {}
        self._association_index: List[MemoryAssociation] = []
        self._lock = asyncio.Lock()
        
        self._weight_evolution_task: Optional[asyncio.Task] = None
        self._decay_task: Optional[asyncio.Task] = None
    
    async def start(self) -> None:
        """启动记忆系统"""
        self._weight_evolution_task = asyncio.create_task(self._weight_evolution_loop())
        self._decay_task = asyncio.create_task(self._decay_loop())
    
    async def stop(self) -> None:
        """停止记忆系统"""
        if self._weight_evolution_task:
            self._weight_evolution_task.cancel()
        if self._decay_task:
            self._decay_task.cancel()
    
    async def store(
        self,
        content: Any,
        memory_type: HexagramType,
        layer: MemoryLayer,
        context: Optional[Dict[str, Any]] = None,
        tiangan_tag: Optional[TianganType] = None,
        dizhi_tag: Optional[DizhiType] = None
    ) -> str:
        """存储新记忆"""
        async with self._lock:
            memory_id = self._generate_memory_id()
            
            wuxing_attr = self.wuxing_system.get_wuxing_from_content(content)
            
            current_time = datetime.now()
            if tiangan_tag is None:
                tiangan_tag = self.tiangan_dizhi_system.get_tiangan(current_time)
            if dizhi_tag is None:
                dizhi_tag = self.tiangan_dizhi_system.get_dizhi(current_time)
            
            yin_yang_balance = self.yinyang_system.calculate_composite_yin_yang(
                memory_type, wuxing_attr.value
            )
            
            memory = MemoryNode(
                memory_id=memory_id,
                content=content,
                memory_type=memory_type,
                layer=layer,
                yin_yang_balance=yin_yang_balance,
                wuxing_attribute=wuxing_attr,
                tiangan_tag=tiangan_tag,
                dizhi_tag=dizhi_tag,
                weight=1.0,
                strength=1.0,
                created_at=current_time,
                last_accessed=current_time,
                associations=[],
                context=context or {}
            )
            
            self._memory_index[memory_id] = memory
            self.three_layer_architecture.store(memory)
            
            self.wuxing_system.update_weights([(wuxing_attr, 1.0)])
            self.yinyang_system.apply_yin_yang_adjustment(yin_yang_balance, 1.0)
            
            return memory_id
    
    async def retrieve(self, query: MemoryQuery) -> List[MemoryNode]:
        """查询记忆"""
        async with self._lock:
            results = []
            
            if query.query_type == QueryType.KEYWORD:
                results = self._search_by_keywords(query.keywords)
            elif query.query_type == QueryType.CONTEXT:
                results = self._search_by_context(query.keywords)
            elif query.query_type == QueryType.TIME_RANGE:
                results = self._search_by_time_range(query.time_range)
            elif query.query_type == QueryType.ASSOCIATION:
                results = self._search_by_association(query.keywords)
            elif query.query_type == QueryType.PREDICTION:
                results = await self._predict_related(query.keywords)
            
            if query.hexagram_filter:
                results = [m for m in results if m.memory_type in query.hexagram_filter]
            
            if query.layer_filter:
                results = [m for m in results if m.layer == query.layer_filter]
            
            if query.wuxing_filter:
                results = [m for m in results if m.wuxing_attribute == query.wuxing_filter]
            
            if query.limit > 0:
                results = results[:query.limit]
            
            return results
    
    async def associate(
        self,
        source_id: str,
        target_id: str,
        association_type: AssociationType
    ) -> bool:
        """建立记忆关联"""
        async with self._lock:
            source = self._memory_index.get(source_id)
            target = self._memory_index.get(target_id)
            
            if not source or not target:
                return False
            
            relation = self.wuxing_system.get_relation(
                source.wuxing_attribute,
                target.wuxing_attribute
            )
            
            association = MemoryAssociation(
                source_id=source_id,
                target_id=target_id,
                association_type=association_type,
                wuxing_relationship=relation,
                strength=1.0,
                bidirectional=True
            )
            
            self._association_index.append(association)
            
            source.associations.append(target_id)
            if association.bidirectional:
                target.associations.append(source_id)
            
            self.hexagram_model.update_transition(source.memory_type, target.memory_type)
            
            return True
    
    async def evolve_weights(self) -> None:
        """执行记忆权重演化"""
        async with self._lock:
            active_memories = self._get_active_memories()
            
            active_wuxing = [
                (m.wuxing_attribute, m.weight * m.strength)
                for m in active_memories
            ]
            
            self.wuxing_system.update_weights(active_wuxing)
            
            for memory in self._memory_index.values():
                if memory.memory_id in [m.memory_id for m in active_memories]:
                    continue
                
                yin_yang_change = self.yinyang_system.balance * 0.01
                memory.yin_yang_balance = max(-1.0, min(1.0, 
                    memory.yin_yang_balance + yin_yang_change))
    
    async def predict_association(self, memory_id: str) -> List[str]:
        """预测可能的记忆关联"""
        memory = self._memory_index.get(memory_id)
        if not memory:
            return []
        
        predictions = self.hexagram_model.predict_next(memory.memory_type)
        
        related_ids = []
        for predicted_hex, prob in predictions:
            for mid, mem in self._memory_index.items():
                if mem.memory_type == predicted_hex and mid != memory_id:
                    related_ids.append(mid)
        
        return related_ids[:5]
    
    async def get_temporal_context(self) -> Dict[str, Any]:
        """获取当前时空上下文"""
        return self.tiangan_dizhi_system.get_temporal_context(datetime.now())
    
    async def integrated_query(self, context: str) -> Dict[str, Any]:
        """整合查询，返回天地人三层记忆"""
        return self.three_layer_architecture.integrated_retrieval(context)
    
    def _generate_memory_id(self) -> str:
        """生成唯一记忆ID"""
        return f"mem_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    def _search_by_keywords(self, keywords: List[str]) -> List[MemoryNode]:
        """基于关键词搜索"""
        results = []
        for memory in self._memory_index.values():
            content_str = str(memory.content)
            if any(kw in content_str for kw in keywords):
                results.append(memory)
        return sorted(results, key=lambda m: m.weight * m.strength, reverse=True)
    
    def _search_by_context(self, keywords: List[str]) -> List[MemoryNode]:
        """基于上下文搜索"""
        results = []
        for memory in self._memory_index.values():
            context_str = str(memory.context)
            if any(kw in context_str for kw in keywords):
                results.append(memory)
        return sorted(results, key=lambda m: m.weight * m.strength, reverse=True)
    
    def _search_by_time_range(
        self,
        time_range: Optional[Tuple[datetime, datetime]]
    ) -> List[MemoryNode]:
        """基于时间范围搜索"""
        if not time_range:
            return list(self._memory_index.values())
        
        start, end = time_range
        results = []
        for memory in self._memory_index.values():
            if start <= memory.created_at <= end:
                results.append(memory)
        return results
    
    def _search_by_association(self, keywords: List[str]) -> List[MemoryNode]:
        """基于关联搜索"""
        seed_memories = self._search_by_keywords(keywords)
        related = []
        
        for memory in seed_memories:
            for assoc_id in memory.associations:
                if assoc_id in self._memory_index:
                    related.append(self._memory_index[assoc_id])
        
        return related
    
    async def _predict_related(self, keywords: List[str]) -> List[MemoryNode]:
        """预测相关记忆"""
        results = []
        for keyword in keywords:
            related_ids = []
            for memory in self._memory_index.values():
                if keyword in str(memory.content):
                    predicted = await self.predict_association(memory.memory_id)
                    related_ids.extend(predicted)
            
            for rid in related_ids:
                if rid in self._memory_index:
                    results.append(self._memory_index[rid])
        
        return list(set(results))[:10]
    
    def _get_active_memories(self) -> List[MemoryNode]:
        """获取活跃记忆"""
        now = datetime.now()
        active = []
        for memory in self._memory_index.values():
            time_diff = (now - memory.last_accessed).total_seconds()
            if time_diff < 3600:
                active.append(memory)
        return active
    
    async def _weight_evolution_loop(self) -> None:
        """权重演化循环"""
        interval = self.config.get('memory.weight_evolution_interval', 3600)
        while True:
            await asyncio.sleep(interval)
            await self.evolve_weights()
    
    async def _decay_loop(self) -> None:
        """记忆衰减循环"""
        decay_rate = self.config.get('memory.strength_decay_rate', 0.001)
        while True:
            await asyncio.sleep(60)
            async with self._lock:
                for memory in self._memory_index.values():
                    memory.strength = max(0.1, memory.strength - decay_rate)
    
    async def get_system_state(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            'total_memories': len(self._memory_index),
            'total_associations': len(self._association_index),
            'layer_counts': self.three_layer_architecture.get_layer_counts(),
            'wuxing_balance': self.wuxing_system.get_balance_score(),
            'yinyang_balance': self.yinyang_system.balance,
            'yinyang_polarity': self.yinyang_system.get_polarity()
        }
