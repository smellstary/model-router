"""
Cache Manager - 缓存管理器
提供缓存管理、监控和优化功能
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

from skill.input_cache import (
    InputCacheSystem,
    CacheConfig,
    CacheStrategy,
    CacheStats
)


@dataclass
class OptimizationReport:
    """优化报告 - Optimization Report"""
    timestamp: datetime
    current_stats: CacheStats
    recommendations: List[str]
    performance_score: float


class CacheManager:
    """缓存管理器 - Cache Manager"""
    
    def __init__(self, cache_system: InputCacheSystem):
        self.cache_system = cache_system
        self._optimization_history: List[Dict] = []
    
    def analyze_performance(self) -> OptimizationReport:
        """分析性能 - Analyze performance"""
        stats = self.cache_system.get_stats()
        recommendations = []
        
        if stats.hit_rate < 0.3:
            recommendations.append("命中率过低，建议降低相似度阈值")
        
        if stats.cache_size < 50 and stats.total_queries > 100:
            recommendations.append("缓存利用率低，建议增加预热数据")
        
        if stats.evictions > stats.total_hits:
            recommendations.append("淘汰过于频繁，建议增加最大缓存条目")
        
        if stats.total_tokens_saved == 0 and stats.total_hits > 0:
            recommendations.append("建议在put操作时传入tokens_used参数")
        
        performance_score = self._calculate_performance_score(stats)
        
        return OptimizationReport(
            timestamp=datetime.now(),
            current_stats=stats,
            recommendations=recommendations,
            performance_score=performance_score
        )
    
    def _calculate_performance_score(self, stats: CacheStats) -> float:
        """计算性能分数 - Calculate performance score"""
        score = 0.0
        
        score += min(stats.hit_rate * 50, 50)
        score += min(stats.total_tokens_saved / 1000 * 30, 30)
        
        if stats.cache_size > 0:
            utilization = min(stats.cache_size / 500 * 20, 20)
            score += utilization
        
        return min(score, 100)
    
    def optimize_config(self) -> CacheConfig:
        """优化配置 - Optimize configuration"""
        stats = self.cache_system.get_stats()
        config = self.cache_system.config
        
        new_config = CacheConfig(
            max_entries=config.max_entries,
            ttl_seconds=config.ttl_seconds,
            similarity_threshold=config.similarity_threshold,
            min_query_length=config.min_query_length,
            strategy=config.strategy,
            enable_auto_eviction=config.enable_auto_eviction,
            enable_statistics=config.enable_statistics
        )
        
        if stats.hit_rate < 0.3:
            new_config.similarity_threshold = max(0.7, config.similarity_threshold - 0.1)
        
        if stats.hit_rate > 0.9:
            new_config.similarity_threshold = min(0.95, config.similarity_threshold + 0.05)
        
        if stats.evictions > stats.total_hits:
            new_config.max_entries = int(config.max_entries * 1.5)
        
        return new_config
    
    def get_top_queries(self, limit: int = 10) -> List[Dict]:
        """获取热门查询 - Get top queries"""
        entries = self.cache_system.get_recent_entries(limit * 2)
        sorted_entries = sorted(entries, key=lambda x: x.access_count, reverse=True)
        
        return [
            {
                'query': entry.input_text[:50] + '...' if len(entry.input_text) > 50 else entry.input_text,
                'access_count': entry.access_count,
                'tokens_saved': entry.tokens_saved,
                'last_accessed': entry.last_accessed
            }
            for entry in sorted_entries[:limit]
        ]
    
    def export_cache_data(self) -> List[Dict]:
        """导出缓存数据 - Export cache data"""
        entries = self.cache_system.get_recent_entries(1000)
        return [
            {
                'cache_id': entry.cache_id,
                'input_text': entry.input_text,
                'created_at': entry.created_at.isoformat(),
                'last_accessed': entry.last_accessed.isoformat(),
                'access_count': entry.access_count,
                'tokens_saved': entry.tokens_saved,
                'metadata': entry.metadata
            }
            for entry in entries
        ]
    
    async def apply_optimization(self) -> OptimizationReport:
        """应用优化 - Apply optimization"""
        new_config = self.optimize_config()
        self.cache_system.config = new_config
        
        report = self.analyze_performance()
        self._optimization_history.append({
            'timestamp': datetime.now().isoformat(),
            'old_config': {
                'max_entries': self.cache_system.config.max_entries,
                'similarity_threshold': self.cache_system.config.similarity_threshold
            },
            'new_config': {
                'max_entries': new_config.max_entries,
                'similarity_threshold': new_config.similarity_threshold
            },
            'report': {
                'hit_rate': report.current_stats.hit_rate,
                'performance_score': report.performance_score
            }
        })
        
        return report


def create_cache_manager(cache_system: InputCacheSystem) -> CacheManager:
    """创建缓存管理器 - Create cache manager"""
    return CacheManager(cache_system)
