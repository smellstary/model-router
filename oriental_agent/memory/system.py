"""
记忆系统 - 基于五行生克的管理与检索
Memory System with Wu Xing Dynamics

功能：
- 五行记忆分类与权重管理
- 生克关系驱动的记忆检索
- 记忆强度动态调整
- 基于相生相克的联想扩展
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import uuid
import logging

logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """记忆类型"""
    EPISODIC = "情景记忆"
    SEMANTIC = "语义记忆"
    PROCEDURAL = "程序记忆"
    WORKING = "工作记忆"


class WuxingType(Enum):
    """五行类型"""
    WOOD = "木"
    FIRE = "火"
    EARTH = "土"
    METAL = "金"
    WATER = "水"


class WuxingRelation(Enum):
    """五行关系"""
    GENERATE = "相生"
    RESTRICT = "相克"
    SAME_NATURE = "同性"


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    content: str
    memory_type: MemoryType
    wuxing: WuxingType
    importance: float
    activation: float
    timestamp: datetime
    last_accessed: datetime
    associations: Set[str] = field(default_factory=set)
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def update_access(self) -> None:
        self.last_accessed = datetime.now()
        self.activation = min(1.0, self.activation + 0.1)

    def decay(self, factor: float = 0.95) -> None:
        self.activation *= factor
        if self.activation < 0.01:
            self.activation = 0.01


@dataclass
class Association:
    """关联记录"""
    source_id: str
    target_id: str
    relation_type: WuxingRelation
    strength: float


class WuxingMemorySystem:
    """五行记忆系统主类"""

    GENERATION_CYCLE = {
        WuxingType.WOOD: WuxingType.FIRE,
        WuxingType.FIRE: WuxingType.EARTH,
        WuxingType.EARTH: WuxingType.METAL,
        WuxingType.METAL: WuxingType.WATER,
        WuxingType.WATER: WuxingType.WOOD,
    }

    RESTRICTION_CYCLE = {
        WuxingType.WOOD: WuxingType.EARTH,
        WuxingType.EARTH: WuxingType.WATER,
        WuxingType.WATER: WuxingType.FIRE,
        WuxingType.FIRE: WuxingType.METAL,
        WuxingType.METAL: WuxingType.WOOD,
    }

    WUXING_KEYWORDS = {
        WuxingType.WOOD: ["成长", "创造", "发展", "建设", "创业", "萌芽"],
        WuxingType.FIRE: ["热情", "能量", "动力", "爆发", "爱情", "激情"],
        WuxingType.EARTH: ["稳定", "安全", "信任", "根基", "积累", "诚信"],
        WuxingType.METAL: ["决断", "价值", "严格", "效率", "法律", "秩序"],
        WuxingType.WATER: ["智慧", "流动", "变通", "财富", "流动性", "深邃"],
    }

    def __init__(self):
        self.memories: Dict[str, MemoryEntry] = {}
        self.associations: List[Association] = []
        self.wuxing_weights: Dict[WuxingType, float] = {
            wuxing: 1.0 for wuxing in WuxingType
        }
        self.access_history: List[str] = []

    def store(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.EPISODIC,
        wuxing: Optional[WuxingType] = None,
        importance: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        memory_id = f"mem_{uuid.uuid4().hex[:12]}"

        if wuxing is None:
            wuxing = self.infer_wuxing(content)

        entry = MemoryEntry(
            id=memory_id,
            content=content,
            memory_type=memory_type,
            wuxing=wuxing,
            importance=importance,
            activation=importance,
            timestamp=datetime.now(),
            last_accessed=datetime.now(),
            metadata=metadata or {}
        )

        self.memories[memory_id] = entry
        self._update_wuxing_weight(wuxing, importance)

        logger.info(f"Stored memory {memory_id} with wuxing {wuxing.value}")

        return memory_id

    def infer_wuxing(self, content: str) -> WuxingType:
        """基于内容关键词推断五行属性"""
        content_lower = content.lower()

        scores = {wx: 0 for wx in WuxingType}

        for wuxing, keywords in self.WUXING_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    scores[wuxing] += 1

        if max(scores.values()) > 0:
            return max(scores.items(), key=lambda x: x[1])[0]

        return WuxingType.EARTH

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        use_association: bool = True
    ) -> List[MemoryEntry]:
        """检索记忆"""
        query_wuxing = self.infer_wuxing(query)

        candidates = []

        for memory_id, entry in self.memories.items():
            relevance = self._calculate_relevance(entry, query, query_wuxing)
            candidates.append((entry, relevance))

        if use_association:
            candidates = self._expand_by_association(candidates, query_wuxing)

        candidates.sort(key=lambda x: x[1], reverse=True)

        self.access_history.extend([entry.id for entry, _ in candidates[:top_k]])

        return [entry for entry, _ in candidates[:top_k]]

    def _calculate_relevance(
        self,
        entry: MemoryEntry,
        query: str,
        query_wuxing: WuxingType
    ) -> float:
        content_score = 0.0
        if query.lower() in entry.content.lower():
            content_score = 0.5

        wuxing_relation = self.get_relation(query_wuxing, entry.wuxing)
        if wuxing_relation == WuxingRelation.SAME_NATURE:
            wuxing_score = 0.3
        elif wuxing_relation == WuxingRelation.GENERATE:
            wuxing_score = 0.2
        elif wuxing_relation == WuxingRelation.RESTRICT:
            wuxing_score = 0.1
        else:
            wuxing_score = 0.0

        activation_score = entry.activation * 0.2

        total_score = content_score + wuxing_score + activation_score + entry.importance * 0.2

        return min(1.0, total_score)

    def _expand_by_association(
        self,
        candidates: List[Tuple[MemoryEntry, float]],
        query_wuxing: WuxingType
    ) -> List[Tuple[MemoryEntry, float]]:
        expanded = candidates.copy()

        generated = self.get_generated_elements(query_wuxing)
        restricted = self.get_restricted_elements(query_wuxing)

        for memory_id, entry in self.memories.items():
            if any(entry.id == c[0].id for c in candidates):
                continue

            boost = 0.0
            if entry.wuxing in generated:
                boost = 0.1
            elif entry.wuxing in restricted:
                boost = 0.05

            if boost > 0:
                expanded.append((entry, boost))

        return expanded

    def get_relation(self, source: WuxingType, target: WuxingType) -> WuxingRelation:
        """判断五行关系"""
        if self.GENERATION_CYCLE.get(source) == target:
            return WuxingRelation.GENERATE
        if self.RESTRICTION_CYCLE.get(source) == target:
            return WuxingRelation.RESTRICT
        return WuxingRelation.SAME_NATURE

    def get_generated_elements(self, element: WuxingType) -> List[WuxingType]:
        """获取被相生的元素"""
        return [k for k, v in self.GENERATION_CYCLE.items() if v == element]

    def get_restricted_elements(self, element: WuxingType) -> List[WuxingType]:
        """获取被相克的元素"""
        return [k for k, v in self.RESTRICTION_CYCLE.items() if v == element]

    def create_association(
        self,
        source_id: str,
        target_id: str,
        relation_type: WuxingRelation,
        strength: float = 0.5
    ) -> bool:
        """创建记忆关联"""
        if source_id not in self.memories or target_id not in self.memories:
            return False

        source = self.memories[source_id]
        target = self.memories[target_id]

        relation = self.get_relation(source.wuxing, target.wuxing)

        association = Association(
            source_id=source_id,
            target_id=target_id,
            relation_type=relation,
            strength=strength
        )

        self.associations.append(association)

        source.associations.add(target_id)
        target.associations.add(source_id)

        return True

    def get_associations(self, memory_id: str) -> List[MemoryEntry]:
        """获取关联记忆"""
        if memory_id not in self.memories:
            return []

        memory = self.memories[memory_id]
        associated = []

        for assoc in self.associations:
            if assoc.source_id == memory_id:
                target = self.memories.get(assoc.target_id)
                if target:
                    associated.append(target)
            elif assoc.target_id == memory_id:
                source = self.memories.get(assoc.source_id)
                if source:
                    associated.append(source)

        return associated

    def _update_wuxing_weight(self, wuxing: WuxingType, importance: float) -> None:
        """更新五行权重"""
        current = self.wuxing_weights[wuxing]
        adjustment = importance * 0.1
        self.wuxing_weights[wuxing] = max(0.5, min(2.0, current + adjustment))

    def decay_all(self) -> None:
        """衰减所有记忆"""
        for entry in self.memories.values():
            entry.decay()

    def get_system_state(self) -> Dict[str, Any]:
        """获取系统状态"""
        total_memories = len(self.memories)
        avg_activation = (
            sum(e.activation for e in self.memories.values()) / total_memories
            if total_memories > 0 else 0
        )

        wuxing_distribution = {
            wx.value: sum(1 for e in self.memories.values() if e.wuxing == wx)
            for wx in WuxingType
        }

        return {
            "total_memories": total_memories,
            "total_associations": len(self.associations),
            "average_activation": avg_activation,
            "wuxing_distribution": wuxing_distribution,
            "wuxing_weights": {wx.value: w for wx, w in self.wuxing_weights.items()},
            "recent_access_count": len(self.access_history[-20:]),
        }

    def export_memories(self) -> str:
        """导出记忆数据"""
        data = []
        for entry in self.memories.values():
            data.append({
                "id": entry.id,
                "content": entry.content,
                "memory_type": entry.memory_type.value,
                "wuxing": entry.wuxing.value,
                "importance": entry.importance,
                "activation": entry.activation,
                "timestamp": entry.timestamp.isoformat(),
                "metadata": entry.metadata,
            })
        return json.dumps(data, ensure_ascii=False, indent=2)

    def import_memories(self, json_data: str) -> int:
        """导入记忆数据"""
        try:
            data = json.loads(json_data)
            count = 0
            for item in data:
                memory_type = MemoryType(item.get("memory_type", "EPISODIC"))
                wuxing = WuxingType(item.get("wuxing", "EARTH"))

                self.store(
                    content=item["content"],
                    memory_type=memory_type,
                    wuxing=wuxing,
                    importance=item.get("importance", 0.5),
                    metadata=item.get("metadata", {})
                )
                count += 1

            return count
        except Exception as e:
            logger.error(f"Import failed: {e}")
            return 0
