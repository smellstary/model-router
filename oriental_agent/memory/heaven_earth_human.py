"""
天地人三层记忆架构
Heaven, Earth, Human Three-Layer Memory Architecture

- 天层（HeavenLayer）：高层次的哲学、原则、价值观。存储长期不变的核心信念。
- 地层（EarthLayer）：中层次的经验、技能、方法论。存储可复用的工作模式。
- 人层（HumanLayer）：低层次的上下文、当前对话、即时信息。存储短期工作记忆。

记忆流向：
  感知 → 人层 → 地层（提炼） → 天层（升华）
  天层 ← 地层 ← 人层（检索时自底向上）
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import re
import hashlib
import logging

try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False

logger = logging.getLogger(__name__)


class MemoryLayer(Enum):
    """记忆层级"""
    HEAVEN = "天"
    EARTH = "地"
    HUMAN = "人"


@dataclass
class MemoryNode:
    """记忆节点"""
    id: str
    content: str
    layer: MemoryLayer
    timestamp: datetime
    importance: float
    associations: Set[str] = field(default_factory=set)
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_keywords(self) -> List[str]:
        if JIEBA_AVAILABLE:
            words = jieba.cut(self.content)
            return [w for w in words if len(w) >= 2]
        else:
            text = re.sub(r'[^\w\s]', '', self.content.lower())
            return text.split()[:20]

    def get_semantic_hash(self) -> str:
        keywords = self.get_keywords()
        keyword_str = ','.join(sorted(keywords))
        return hashlib.md5(keyword_str.encode()).hexdigest()[:12]


class HeavenLayer:
    """天层 - 高层次哲学、原则、价值观"""

    def __init__(self):
        self.principles: Dict[str, MemoryNode] = {}
        self.values: Dict[str, MemoryNode] = {}
        self.beliefs: Dict[str, MemoryNode] = {}
        self.wisdom: Dict[str, MemoryNode] = {}

    def store(self, node: MemoryNode) -> bool:
        if node.layer != MemoryLayer.HEAVEN:
            return False

        if "principle" in node.metadata.get("type", "").lower():
            self.principles[node.id] = node
        elif "value" in node.metadata.get("type", "").lower():
            self.values[node.id] = node
        elif "belief" in node.metadata.get("type", "").lower():
            self.beliefs[node.id] = node
        elif "wisdom" in node.metadata.get("type", "").lower():
            self.wisdom[node.id] = node
        else:
            self.principles[node.id] = node

        return True

    def retrieve_by_theme(self, theme: str) -> List[MemoryNode]:
        results = []
        theme_lower = theme.lower()

        for collection in [self.principles, self.values, self.beliefs, self.wisdom]:
            for node in collection.values():
                keywords = node.get_keywords()
                if any(theme_lower in kw.lower() for kw in keywords):
                    results.append(node)

        return results

    def get_all(self) -> List[MemoryNode]:
        all_nodes = []
        for collection in [self.principles, self.values, self.beliefs, self.wisdom]:
            all_nodes.extend(collection.values())
        return sorted(all_nodes, key=lambda n: n.importance, reverse=True)


class EarthLayer:
    """地层 - 中层次的经验、技能、方法论"""

    def __init__(self):
        self.skills: Dict[str, MemoryNode] = {}
        self.experiences: Dict[str, MemoryNode] = {}
        self.patterns: Dict[str, MemoryNode] = {}
        self.methodologies: Dict[str, MemoryNode] = {}

    def store(self, node: MemoryNode) -> bool:
        if node.layer != MemoryLayer.EARTH:
            return False

        node_type = node.metadata.get("type", "experience").lower()

        if "skill" in node_type:
            self.skills[node.id] = node
        elif "experience" in node_type:
            self.experiences[node.id] = node
        elif "pattern" in node_type:
            self.patterns[node.id] = node
        elif "methodology" in node_type or "method" in node_type:
            self.methodologies[node.id] = node
        else:
            self.experiences[node.id] = node

        return True

    def retrieve_by_context(self, context: str) -> List[MemoryNode]:
        results = []
        context_lower = context.lower()

        for collection in [self.skills, self.experiences, self.patterns, self.methodologies]:
            for node in collection.values():
                keywords = node.get_keywords()
                if any(context_lower in kw.lower() for kw in keywords):
                    results.append(node)

        return results

    def get_all(self) -> List[MemoryNode]:
        all_nodes = []
        for collection in [self.skills, self.experiences, self.patterns, self.methodologies]:
            all_nodes.extend(collection.values())
        return sorted(all_nodes, key=lambda n: n.importance, reverse=True)


class HumanLayer:
    """人层 - 低层次的上下文、当前对话、即时信息"""

    def __init__(self, max_size: int = 100):
        self.context_stack: List[MemoryNode] = []
        self.current_conversation: List[MemoryNode] = []
        self.working_memory: Dict[str, Any] = {}
        self.max_size = max_size

    def store(self, node: MemoryNode) -> bool:
        if node.layer != MemoryLayer.HUMAN:
            return False

        self.context_stack.append(node)

        if len(self.context_stack) > self.max_size:
            self.context_stack.pop(0)

        return True

    def store_conversation(self, node: MemoryNode) -> bool:
        self.current_conversation.append(node)

        if len(self.current_conversation) > 50:
            self.current_conversation.pop(0)

        return True

    def get_recent(self, n: int = 10) -> List[MemoryNode]:
        return self.context_stack[-n:]

    def get_conversation(self) -> List[MemoryNode]:
        return self.current_conversation.copy()

    def clear_conversation(self) -> None:
        self.current_conversation.clear()

    def get_working_memory(self, key: str) -> Any:
        return self.working_memory.get(key)

    def set_working_memory(self, key: str, value: Any) -> None:
        self.working_memory[key] = value

    def clear_working_memory(self) -> None:
        self.working_memory.clear()


class HeavenEarthHumanMemory:
    """天地人三层记忆主系统"""

    def __init__(self):
        self.heaven_layer = HeavenLayer()
        self.earth_layer = EarthLayer()
        self.human_layer = HumanLayer()
        self._interaction_log: List[Dict] = []

    def store(self, content: str, layer: MemoryLayer, importance: float = 0.5,
              metadata: Optional[Dict[str, Any]] = None) -> str:
        node_id = self._generate_node_id(content)
        node = MemoryNode(
            id=node_id,
            content=content,
            layer=layer,
            timestamp=datetime.now(),
            importance=importance,
            metadata=metadata or {}
        )

        if layer == MemoryLayer.HEAVEN:
            self.heaven_layer.store(node)
        elif layer == MemoryLayer.EARTH:
            self.earth_layer.store(node)
        elif layer == MemoryLayer.HUMAN:
            self.human_layer.store(node)

        self._log_interaction("store", layer, node_id)
        return node_id

    def retrieve(self, query: str, layer: Optional[MemoryLayer] = None,
                 top_k: int = 5) -> List[MemoryNode]:
        results = []

        if layer is None or layer == MemoryLayer.HEAVEN:
            heaven_results = self.heaven_layer.retrieve_by_theme(query)
            results.extend(heaven_results)

        if layer is None or layer == MemoryLayer.EARTH:
            earth_results = self.earth_layer.retrieve_by_context(query)
            results.extend(earth_results)

        if layer is None or layer == MemoryLayer.HUMAN:
            human_results = self._retrieve_human_layer(query)
            results.extend(human_results)

        results = sorted(results, key=lambda n: n.importance, reverse=True)
        return results[:top_k]

    def _retrieve_human_layer(self, query: str) -> List[MemoryNode]:
        results = []
        query_lower = query.lower()
        keywords = self._extract_keywords(query_lower)

        for node in self.human_layer.get_recent(50):
            node_keywords = node.get_keywords()
            if self._has_semantic_relation(query_lower, keywords, node.content, node_keywords):
                results.append(node)

        return results

    def _has_semantic_relation(self, query: str, query_keywords: List[str],
                               content: str, content_keywords: List[str]) -> bool:
        if not query_keywords or not content_keywords:
            return query in content.lower()

        if JIEBA_AVAILABLE:
            content_jieba = set(jieba.cut(content.lower()))
            query_set = set(query_keywords)
            common = content_jieba & query_set
            return len(common) >= 1
        else:
            query_set = set(query_keywords)
            content_set = set(content_keywords)
            common = query_set & content_set
            return len(common) >= 1

    def _extract_keywords(self, text: str) -> List[str]:
        if JIEBA_AVAILABLE:
            words = jieba.cut(text)
            return [w for w in words if len(w) >= 2]
        else:
            text_clean = re.sub(r'[^\w\s]', '', text)
            words = text_clean.split()
            return [w for w in words if len(w) >= 2]

    def distill(self, human_node_id: str) -> Optional[str]:
        human_nodes = self.human_layer.get_recent(100)
        node_map = {n.id: n for n in human_nodes}

        if human_node_id not in node_map:
            return None

        node = node_map[human_node_id]

        if node.importance >= 0.8 and len(node.content) > 50:
            earth_node_id = self.store(
                content=node.content,
                layer=MemoryLayer.EARTH,
                importance=node.importance * 0.9,
                metadata={**node.metadata, "distilled_from": human_node_id}
            )
            return earth_node_id

        return None

    def ascend(self, earth_node_id: str) -> Optional[str]:
        earth_nodes = self.earth_layer.get_all()
        node_map = {n.id: n for n in earth_nodes}

        if earth_node_id not in node_map:
            return None

        node = node_map[earth_node_id]

        if node.importance >= 0.95 and len(node.content) > 30:
            heaven_node_id = self.store(
                content=node.content,
                layer=MemoryLayer.HEAVEN,
                importance=1.0,
                metadata={**node.metadata, "ascended_from": earth_node_id}
            )
            return heaven_node_id

        return None

    def get_layer_summary(self, layer: MemoryLayer) -> Dict[str, Any]:
        if layer == MemoryLayer.HEAVEN:
            nodes = self.heaven_layer.get_all()
        elif layer == MemoryLayer.EARTH:
            nodes = self.earth_layer.get_all()
        elif layer == MemoryLayer.HUMAN:
            nodes = self.human_layer.get_recent(50)
        else:
            nodes = []

        return {
            "layer": layer.value,
            "count": len(nodes),
            "total_importance": sum(n.importance for n in nodes),
            "avg_importance": sum(n.importance for n in nodes) / len(nodes) if nodes else 0,
            "recent_nodes": [n.id for n in nodes[-5:]] if nodes else [],
        }

    def get_full_summary(self) -> Dict[str, Any]:
        return {
            "heaven": self.get_layer_summary(MemoryLayer.HEAVEN),
            "earth": self.get_layer_summary(MemoryLayer.EARTH),
            "human": self.get_layer_summary(MemoryLayer.HUMAN),
            "interaction_log_size": len(self._interaction_log),
        }

    def _generate_node_id(self, content: str) -> str:
        timestamp = datetime.now().isoformat()
        raw = f"{content[:50]}_{timestamp}"
        return hashlib.md5(raw.encode()).hexdigest()[:16]

    def _log_interaction(self, action: str, layer: MemoryLayer, node_id: str) -> None:
        self._interaction_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "layer": layer.value,
            "node_id": node_id,
        })

        if len(self._interaction_log) > 1000:
            self._interaction_log = self._interaction_log[-500:]


from enum import Enum
