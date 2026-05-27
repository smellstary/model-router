# 输入缓存优化 Skill

## 概述

这个 skill 为东方智慧智能体提供输入缓存优化功能，显著提升 OpenClaw 和 Hermes 等模型的缓存命中率，降低 token 消耗，提高工作效率。

## 核心功能

### 1. 多种缓存策略

- **精确匹配 (EXACT_MATCH)**: 完全相同的查询才命中
- **模糊匹配 (FUZZY_MATCH)**: 使用 Jaccard 相似度匹配
- **语义相似 (SEMANTIC_SIMILARITY)**: 结合 Jaccard 和余弦相似度（推荐）
- **模式匹配 (PATTERN_MATCH)**: 基于规则的模式匹配

### 2. 智能缓存管理

- 自动过期淘汰 (TTL)
- LRU 缓存策略
- 最大条目限制
- 异步安全设计

### 3. 统计与监控

- 实时命中率统计
- Token 节省统计
- 热门查询追踪
- 性能评分与优化建议

## 快速开始

### 基本使用

```python
from skill.input_cache import (
    InputCacheSystem,
    CacheConfig,
    CacheStrategy,
    create_cache_system
)

# 创建缓存系统
cache = create_cache_system()

# 存入缓存
await cache.put("你的查询", "查询回答", tokens_used=150)

# 获取缓存
response, similarity = await cache.get("你的查询")

# 获取统计信息
stats = cache.get_stats()
```

### 配置自定义

```python
config = CacheConfig(
    max_entries=2000,           # 最大缓存条目
    ttl_seconds=7200,           # 2小时过期
    similarity_threshold=0.75,  # 相似度阈值
    strategy=CacheStrategy.SEMANTIC_SIMILARITY
)

cache = create_cache_system(config)
```

### 集成到智能体

智能体已默认集成缓存系统：

```python
from core.agent import OrientalWisdomAgent, create_agent

# 创建带缓存的智能体（默认启用）
agent = await create_agent()

# 禁用缓存
agent_without_cache = OrientalWisdomAgent(enable_cache=False)

# 获取缓存统计
cache_stats = agent.get_cache_stats()
```

### 使用缓存管理器

```python
from skill.manager import create_cache_manager

manager = create_cache_manager(cache)

# 分析性能
report = manager.analyze_performance()
print(f"性能分数: {report.performance_score}")
print(f"优化建议: {report.recommendations}")

# 获取热门查询
top_queries = manager.get_top_queries(10)
```

## 测试

运行完整测试套件：

```bash
cd /workspace
python test_cache_standalone.py
```

## 文件结构

```
oriental_agent/skill/
├── __init__.py          # 模块导出
├── input_cache.py       # 核心缓存系统
├── manager.py           # 缓存管理器
├── test_cache.py        # 测试脚本
└── README.md            # 使用说明
```

## 性能指标

- 命中延迟: < 1ms
- 支持并发访问
- 内存高效（使用 OrderedDict）
- 自动 GC 和淘汰机制

## 最佳实践

1. **相似度阈值调整**: 0.7-0.85 通常是良好的平衡点
2. **预热缓存**: 系统启动时提前加载常用查询
3. **监控统计**: 定期检查命中率和优化建议
4. **合理设置 TTL**: 根据查询时效性调整

## 更新日志

### v1.0.0 (2026-05-27)
- 初始版本发布
- 支持多种缓存策略
- 集成到主智能体系统
- 完整的测试覆盖
