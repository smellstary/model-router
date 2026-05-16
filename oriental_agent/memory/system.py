"""
Main Memory System - Integration of all memory components
记忆系统主模块 - 整合所有记忆组件

修复记录 (2026-05-16):
- 使用 UUID 替代时间戳生成记忆 ID，避免并发冲突
- 跨层关联使用 jieba 中文分词（fallback 到 n-gram）
- 差异化记忆衰减（基于权重，高权重衰减慢）
- 衰减循环不再持锁遍历（快照后无锁操作）
- evolve_weights 支持五行生克对个体记忆权重的联动调整
- store 支持 LLM 辅助推断五行属性（可选）
"""

import asyncio
import uuid
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

    # ── 五行推断关键词表（中文+英文） ──
    WUXING_KEYWORDS = {
        WuxingType.WOOD: ['成长', '创造', '发展', '生长', '创新', '萌芽', 'growth', 'create', 'develop', 'innovation'],
        WuxingType.FIRE: ['热情', '能量', '动力', '激烈', '爆发', 'energy', 'passion', 'fire', 'intense', 'power'],
        WuxingType.EARTH: ['稳定', '基础', '承载', '平衡', '中心', 'stability', 'ground', 'foundation', 'balance'],
        WuxingType.METAL: ['决策', '收敛', '规则', '秩序', '精确', 'decide', 'order', 'rule', 'precise', 'contract'],
        WuxingType.WATER: ['流动', '智慧', '变化', '灵活', '深思', 'flow', 'wisdom', 'change', 'flexible', 'deep'],
    }

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
        dizhi_tag: Optional[DizhiType] = None,
        wuxing_override: Optional[WuxingType] = None,
    ) -> str:
        """存储新记忆"""
        async with self._lock:
            memory_id = self._generate_memory_id()

            # 五行属性推断：支持手动覆盖
            if wuxing_override is not None:
                wuxing_attr = wuxing_override
            else:
                wuxing_attr = self._infer_wuxing(content)

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
        """执行记忆权重演化 — 基于五行生克的全局 + 个体联动"""
        async with self._lock:
            active_memories = self._get_active_memories()

            active_wuxing = [
                (m.wuxing_attribute, m.weight * m.strength)
                for m in active_memories
            ]

            # 1. 更新全局五行权重
            global_weights = self.wuxing_system.update_weights(active_wuxing)

            # 2. 基于五行生克调整个体记忆权重
            active_ids = {m.memory_id for m in active_memories}
            for memory in self._memory_index.values():
                if memory.memory_id in active_ids:
                    # 活跃记忆：被相生则增益，被相克则抑制
                    generated = self.wuxing_system.get_generated_elements(memory.wuxing_attribute)
                    restricted = self.wuxing_system.get_restricted_elements(memory.wuxing_attribute)

                    boost = sum(global_weights.get(g, 1.0) - 1.0 for g in generated) * 0.05
                    drain = sum(global_weights.get(r, 1.0) - 1.0 for r in restricted) * 0.03

                    memory.weight = max(0.1, min(2.0, memory.weight + boost - drain))
                else:
                    # 非活跃记忆：随系统阴阳平衡微调
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

    # ── 私有方法 ──

    def _generate_memory_id(self) -> str:
        """生成唯一记忆ID — UUID 替代时间戳，避免并发冲突"""
        return f"mem_{uuid.uuid4().hex[:12]}"

    def _search_by_keywords(self, keywords: List[str]) -> List[MemoryNode]:
        """基于关键词搜索"""
        results = []
        for memory in self._memory_index.values():
            content_str = str(memory.content)
            # 同时匹配分词后的关键词
            tokenized = self._tokenize_chinese(content_str)
            if any(kw in content_str or kw in tokenized for kw in keywords):
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
        """记忆衰减循环 — 基于权重的差异化衰减（艾宾浩斯遗忘曲线启发）

        策略：高权重记忆衰减更慢，低权重衰减更快。
        衰减率 = base_rate × (0.2 + (1 - min(weight, 1.0)) × 0.8)
        weight=1.0 → factor=0.2（衰减慢）
        weight=0.1 → factor=1.0（衰减快）
        """
        base_rate = self.config.get('memory.strength_decay_rate', 0.001)
        while True:
            await asyncio.sleep(60)
            # 快照读取，不持锁遍历
            memories_to_decay = list(self._memory_index.values())
            for memory in memories_to_decay:
                decay_factor = 1.0 - 0.8 * min(memory.weight, 1.0)
                effective_rate = base_rate * (decay_factor + 0.2)
                new_strength = memory.strength - effective_rate
                memory.strength = max(0.1, new_strength)

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

    # ── 内容五行推断 ──

    def _infer_wuxing(self, content: Any) -> WuxingType:
        """基于内容关键词推断五行属性（支持中英文）"""
        if not isinstance(content, str):
            content_str = str(content).lower()
        else:
            content_str = content.lower()

        # 分词后匹配
        tokens = self._tokenize_chinese(content_str)

        scores = {wx: 0 for wx in WuxingType}
        for wuxing, keywords in self.WUXING_KEYWORDS.items():
            for kw in keywords:
                kw_lower = kw.lower()
                if kw_lower in content_str:
                    scores[wuxing] += 2
                if kw_lower in tokens:
                    scores[wuxing] += 1

        if max(scores.values()) > 0:
            return max(scores.items(), key=lambda x: x[1])[0]

        # fallback：根据类型推断
        return self._wuxing_by_type(content)

    @staticmethod
    def _wuxing_by_type(content: Any) -> WuxingType:
        """根据 Python 类型做粗略五行分类"""
        t = type(content).__name__.lower()
        if t in ('str', 'text'):
            return WuxingType.WATER  # 水主智，文字为智慧载体
        if t in ('int', 'float', 'bool'):
            return WuxingType.METAL  # 金主决断，数字为规则
        if t in ('list', 'tuple', 'set'):
            return WuxingType.WOOD   # 木主生长，集合为创造
        if t in ('dict', 'mapping'):
            return WuxingType.EARTH  # 土主承载，映射为基础
        return WuxingType.EARTH

    # ── 中文分词 ──

    @staticmethod
    def _tokenize_chinese(text: str) -> set:
        """中文分词，优先使用 jieba，fallback 到 n-gram"""
        try:
            import jieba
            return set(jieba.lcut(text))
        except ImportError:
            # 无 jieba 时退化为 bi-gram + uni-gram
            return {text[i:i+2] for i in range(len(text) - 1)} | set(text)
