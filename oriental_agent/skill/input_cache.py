"""
Input Cache Optimization Skill - 输入缓存优化技能
提升OpenClaw和Hermes输入缓存命中率，降低token消耗
"""

import hashlib
import json
import re
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import OrderedDict
import asyncio


class CacheStrategy(Enum):
    """缓存策略 - Cache Strategy"""
    EXACT_MATCH = "exact_match"        # 精确匹配
    SEMANTIC_SIMILARITY = "semantic"   # 语义相似
    FUZZY_MATCH = "fuzzy"              # 模糊匹配
    PATTERN_MATCH = "pattern"          # 模式匹配


@dataclass
class CacheConfig:
    """缓存配置 - Cache Configuration"""
    max_entries: int = 1000
    ttl_seconds: int = 3600  # 1小时
    similarity_threshold: float = 0.85
    min_query_length: int = 3
    strategy: CacheStrategy = CacheStrategy.SEMANTIC_SIMILARITY
    enable_auto_eviction: bool = True
    enable_statistics: bool = True


@dataclass
class CacheEntry:
    """缓存条目 - Cache Entry"""
    cache_id: str
    input_text: str
    input_hash: str
    response_data: Any
    created_at: datetime
    last_accessed: datetime
    access_count: int = 0
    tokens_saved: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CacheStats:
    """缓存统计 - Cache Statistics"""
    total_hits: int = 0
    total_misses: int = 0
    total_queries: int = 0
    hit_rate: float = 0.0
    total_tokens_saved: int = 0
    cache_size: int = 0
    evictions: int = 0
    strategy_used: str = ""


class InputCacheSystem:
    """输入缓存系统 - Input Cache System"""
    
    def __init__(self, config: Optional[CacheConfig] = None):
        self.config = config or CacheConfig()
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._stats = CacheStats(strategy_used=self.config.strategy.value)
        self._lock = asyncio.Lock()
        self._stopwords = self._load_stopwords()
        
    def _load_stopwords(self) -> set:
        """加载停用词 - Load stopwords"""
        return {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
            '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
            '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '有',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would'
        }
    
    def _compute_hash(self, text: str) -> str:
        """计算文本哈希值 - Compute text hash"""
        normalized_text = self._normalize_text(text)
        return hashlib.sha256(normalized_text.encode('utf-8')).hexdigest()
    
    def _normalize_text(self, text: str) -> str:
        """文本归一化 - Normalize text"""
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def _tokenize(self, text: str) -> List[str]:
        """简单分词 - Simple tokenization (支持中英文)"""
        normalized = self._normalize_text(text)
        
        # 对于中文文本，进行简单的n-gram处理
        if any('\u4e00' <= char <= '\u9fff' for char in normalized):
            tokens = []
            # 2-gram分词
            for i in range(len(normalized) - 1):
                token = normalized[i:i+2]
                if token not in self._stopwords:
                    tokens.append(token)
            # 同时保留完整的词（按空格分割）
            words = normalized.split()
            for word in words:
                if word not in self._stopwords and len(word) > 1:
                    tokens.append(word)
            return tokens
        else:
            words = normalized.split()
            return [word for word in words if word not in self._stopwords]
    
    def _compute_jaccard_similarity(self, text1: str, text2: str) -> float:
        """计算Jaccard相似度 - Compute Jaccard similarity"""
        set1 = set(self._tokenize(text1))
        set2 = set(self._tokenize(text2))
        
        if not set1 or not set2:
            return 0.0
            
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def _compute_cosine_similarity(self, text1: str, text2: str) -> float:
        """计算余弦相似度（基于词频）- Compute cosine similarity"""
        tokens1 = self._tokenize(text1)
        tokens2 = self._tokenize(text2)
        
        if not tokens1 or not tokens2:
            return 0.0
            
        all_tokens = set(tokens1 + tokens2)
        
        vec1 = [tokens1.count(token) for token in all_tokens]
        vec2 = [tokens2.count(token) for token in all_tokens]
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
    
    def _find_best_match(self, input_text: str) -> Tuple[Optional[CacheEntry], float]:
        """查找最佳匹配 - Find best match"""
        if len(input_text) < self.config.min_query_length:
            return None, 0.0
            
        best_entry = None
        best_score = 0.0
        
        for entry in self._cache.values():
            if self.config.strategy == CacheStrategy.EXACT_MATCH:
                if entry.input_text == input_text:
                    return entry, 1.0
                    
            elif self.config.strategy == CacheStrategy.SEMANTIC_SIMILARITY:
                jaccard = self._compute_jaccard_similarity(input_text, entry.input_text)
                cosine = self._compute_cosine_similarity(input_text, entry.input_text)
                score = (jaccard + cosine) / 2
                
                if score > best_score:
                    best_score = score
                    best_entry = entry
                    
            elif self.config.strategy == CacheStrategy.FUZZY_MATCH:
                jaccard = self._compute_jaccard_similarity(input_text, entry.input_text)
                if jaccard > best_score:
                    best_score = jaccard
                    best_entry = entry
        
        if best_score >= self.config.similarity_threshold:
            return best_entry, best_score
            
        return None, 0.0
    
    async def get(self, input_text: str) -> Tuple[Optional[Any], float]:
        """获取缓存 - Get from cache"""
        async with self._lock:
            self._stats.total_queries += 1
            
            entry, score = self._find_best_match(input_text)
            
            if entry:
                self._stats.total_hits += 1
                self._stats.hit_rate = self._stats.total_hits / self._stats.total_queries
                
                entry.access_count += 1
                entry.last_accessed = datetime.now()
                self._cache.move_to_end(entry.cache_id)
                
                return entry.response_data, score
                
            self._stats.total_misses += 1
            self._stats.hit_rate = self._stats.total_hits / self._stats.total_queries if self._stats.total_queries > 0 else 0
            
            return None, 0.0
    
    async def put(self, input_text: str, response_data: Any, tokens_used: int = 0, metadata: Optional[Dict] = None) -> str:
        """存入缓存 - Put to cache"""
        async with self._lock:
            cache_id = self._compute_hash(input_text)
            
            if cache_id in self._cache:
                entry = self._cache[cache_id]
                entry.response_data = response_data
                entry.last_accessed = datetime.now()
                entry.access_count += 1
                if metadata:
                    entry.metadata.update(metadata)
                self._cache.move_to_end(cache_id)
            else:
                entry = CacheEntry(
                    cache_id=cache_id,
                    input_text=input_text,
                    input_hash=cache_id,
                    response_data=response_data,
                    created_at=datetime.now(),
                    last_accessed=datetime.now(),
                    access_count=1,
                    tokens_saved=tokens_used,
                    metadata=metadata or {}
                )
                self._cache[cache_id] = entry
                
            self._stats.cache_size = len(self._cache)
            
            if self.config.enable_auto_eviction:
                await self._evict_if_needed()
                
            return cache_id
    
    async def _evict_if_needed(self) -> None:
        """按需淘汰缓存 - Evict if needed"""
        now = datetime.now()
        to_evict = []
        
        for cache_id, entry in list(self._cache.items()):
            age = (now - entry.created_at).total_seconds()
            if age > self.config.ttl_seconds:
                to_evict.append(cache_id)
        
        while len(self._cache) > self.config.max_entries:
            oldest_id = next(iter(self._cache))
            to_evict.append(oldest_id)
            self._cache.popitem(last=False)
        
        for cache_id in to_evict:
            if cache_id in self._cache:
                self._cache.pop(cache_id)
                self._stats.evictions += 1
        
        self._stats.cache_size = len(self._cache)
    
    def get_stats(self) -> CacheStats:
        """获取统计信息 - Get statistics"""
        return CacheStats(
            total_hits=self._stats.total_hits,
            total_misses=self._stats.total_misses,
            total_queries=self._stats.total_queries,
            hit_rate=self._stats.hit_rate,
            total_tokens_saved=sum(e.tokens_saved for e in self._cache.values()),
            cache_size=self._stats.cache_size,
            evictions=self._stats.evictions,
            strategy_used=self._stats.strategy_used
        )
    
    async def clear(self) -> None:
        """清空缓存 - Clear cache"""
        async with self._lock:
            self._cache.clear()
            self._stats = CacheStats(strategy_used=self.config.strategy.value)
    
    async def warmup(self, sample_data: List[Tuple[str, Any]]) -> None:
        """预热缓存 - Warm up cache"""
        for input_text, response in sample_data:
            await self.put(input_text, response)
    
    def get_recent_entries(self, limit: int = 10) -> List[CacheEntry]:
        """获取最近使用的条目 - Get recent entries"""
        entries = list(self._cache.values())
        return sorted(entries, key=lambda x: x.last_accessed, reverse=True)[:limit]


def create_cache_system(config: Optional[CacheConfig] = None) -> InputCacheSystem:
    """创建缓存系统 - Create cache system"""
    return InputCacheSystem(config)


def get_cache_stats(cache_system: InputCacheSystem) -> CacheStats:
    """获取缓存统计 - Get cache statistics"""
    return cache_system.get_stats()
