"""Skill module for Oriental Wisdom Agent - Input Cache Optimization
东方智慧智能体技能模块 - 输入缓存优化"""

from skill.input_cache import (
    InputCacheSystem,
    CacheEntry,
    CacheConfig,
    CacheStrategy,
    CacheStats,
    create_cache_system,
    get_cache_stats
)
from skill.manager import (
    CacheManager,
    OptimizationReport,
    create_cache_manager
)

__all__ = [
    'InputCacheSystem',
    'CacheEntry',
    'CacheConfig',
    'CacheStrategy',
    'CacheStats',
    'create_cache_system',
    'get_cache_stats',
    'CacheManager',
    'OptimizationReport',
    'create_cache_manager'
]
