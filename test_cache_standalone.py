#!/usr/bin/env python3
"""
Standalone Test Script for Input Cache System
独立测试脚本 - 输入缓存系统
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'oriental_agent'))

import asyncio
from skill.input_cache import (
    InputCacheSystem,
    CacheConfig,
    CacheStrategy,
    create_cache_system
)
from skill.manager import create_cache_manager


async def test_basic_functionality():
    """测试基本功能 - Test basic functionality"""
    print("=" * 60)
    print("测试1: 基本缓存功能")
    print("=" * 60)
    
    cache = create_cache_system()
    
    test_queries = [
        ("如何学习Python编程？", "Python编程学习指南...", 150),
        ("解释什么是机器学习", "机器学习是人工智能的一个分支...", 200),
        ("帮我写一个排序算法", "这里是一个快速排序的实现...", 180),
    ]
    
    for query, response, tokens in test_queries:
        await cache.put(query, response, tokens_used=tokens)
        print(f"已缓存: {query[:30]}...")
    
    print("\n--- 查询测试 ---")
    
    response, score = await cache.get("如何学习Python编程？")
    print(f"精确查询: 命中={'是' if response else '否'}, 相似度={score:.2f}")
    
    response, score = await cache.get("学习Python编程的方法")
    print(f"相似查询: 命中={'是' if response else '否'}, 相似度={score:.2f}")
    
    response, score = await cache.get("今天天气怎么样？")
    print(f"新查询: 命中={'是' if response else '否'}, 相似度={score:.2f}")
    
    stats = cache.get_stats()
    print(f"\n统计信息:")
    print(f"  总查询: {stats.total_queries}")
    print(f"  命中数: {stats.total_hits}")
    print(f"  未命中: {stats.total_misses}")
    print(f"  命中率: {stats.hit_rate:.2%}")
    print(f"  节省Token: {stats.total_tokens_saved}")
    
    print()


async def test_different_strategies():
    """测试不同策略 - Test different strategies"""
    print("=" * 60)
    print("测试2: 不同缓存策略对比")
    print("=" * 60)
    
    strategies = [
        (CacheStrategy.EXACT_MATCH, "精确匹配"),
        (CacheStrategy.FUZZY_MATCH, "模糊匹配"),
        (CacheStrategy.SEMANTIC_SIMILARITY, "语义相似"),
    ]
    
    base_query = "如何编写Python代码"
    test_variations = [
        "如何编写Python代码",
        "编写Python代码的方法",
        "Python代码如何写",
        "如何学习Java编程",
    ]
    
    for strategy, name in strategies:
        print(f"\n--- {name} 策略 ---")
        
        config = CacheConfig(strategy=strategy, similarity_threshold=0.6)
        cache = create_cache_system(config)
        
        await cache.put(base_query, "这是基础回答", tokens_used=100)
        
        for variation in test_variations:
            response, score = await cache.get(variation)
            status = "✓ 命中" if response else "✗ 未命中"
            print(f"  '{variation}' -> {status} (相似度: {score:.2f})")


async def test_cache_manager():
    """测试缓存管理器 - Test cache manager"""
    print("\n" + "=" * 60)
    print("测试3: 缓存管理与优化")
    print("=" * 60)
    
    cache = create_cache_system(CacheConfig(similarity_threshold=0.7))
    manager = create_cache_manager(cache)
    
    print("\n填充测试数据...")
    for i in range(20):
        query = f"这是第{i}个测试问题"
        response = f"这是第{i}个测试回答"
        await cache.put(query, response, tokens_used=50 + i * 10)
    
    for i in range(5):
        await cache.get("这是第0个测试问题")
    
    print("\n获取统计信息:")
    report = manager.analyze_performance()
    print(f"  性能分数: {report.performance_score:.1f}/100")
    print(f"  命中率: {report.current_stats.hit_rate:.2%}")
    
    if report.recommendations:
        print(f"  优化建议:")
        for rec in report.recommendations:
            print(f"    - {rec}")
    
    print("\n热门查询:")
    top_queries = manager.get_top_queries(5)
    for q in top_queries:
        print(f"  {q['query']} (访问: {q['access_count']}次)")


async def main():
    """主测试函数 - Main test function"""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "输入缓存优化技能 - 测试套件" + " " * 20 + "║")
    print("║" + " " * 10 + "Input Cache Optimization Skill - Test Suite" + " " * 8 + "║")
    print("╚" + "═" * 58 + "╝\n")
    
    try:
        await test_basic_functionality()
        await test_different_strategies()
        await test_cache_manager()
        
        print("\n" + "=" * 60)
        print("✓ 所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 测试出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
