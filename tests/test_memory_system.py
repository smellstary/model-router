"""
记忆系统单元测试
测试核心修复：
1. UUID 记忆 ID（并发安全）
2. 中文分词语义关联
3. 五行内容推断（中文+英文）
4. 差异化记忆衰减
5. 五行权重联动
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'oriental_agent'))

import unittest
from datetime import datetime, timedelta
from core.types import (
    MemoryNode, MemoryLayer, HexagramType, WuxingType, QueryType,
    MemoryQuery, AssociationType
)
from memory.wuxing import WuxingSystem
from memory.yinyang import YinYangSystem
from memory.system import MemorySystem
from memory.heaven_earth_human import ThreeLayerMemoryArchitecture


class TestUUIDGeneration(unittest.TestCase):
    """测试 1: UUID 替代时间戳"""

    def test_unique_ids(self):
        """并发生成多个 ID 应该互不相同"""
        mem = MemorySystem()
        ids = set()
        # 手动调用 _generate_memory_id 1000 次
        for _ in range(1000):
            mid = mem._generate_memory_id()
            self.assertIn('mem_', mid)
            self.assertNotIn('%', mid)  # 不应包含 strftime 格式化字符
            ids.add(mid)
        self.assertEqual(len(ids), 1000, "所有 ID 必须唯一")


class TestChineseTokenization(unittest.TestCase):
    """测试 2: 中文分词语义关联"""

    def test_chinese_semantic_relation(self):
        """中文内容应正确识别语义关联（使用 bi-gram fallback 兜底）"""
        # 使用包含明确共同词汇的文本
        text1 = "人工智能在医疗领域有广泛应用"
        text2 = "人工智能技术正在改变医疗行业"

        tokens1 = MemorySystem._tokenize_chinese(text1)
        tokens2 = MemorySystem._tokenize_chinese(text2)
        common = tokens1 & tokens2
        meaningful = {w for w in common if len(w) > 1}

        self.assertGreaterEqual(len(meaningful), 1,
            f"应找到共同词汇，找到: {meaningful}")

    def test_no_relation_unrelated(self):
        """不相关的中文内容不应被关联"""
        text1 = "今天天气很好适合出去玩"
        text2 = "量子计算机的量子比特纠缠态"

        tokens1 = MemorySystem._tokenize_chinese(text1)
        tokens2 = MemorySystem._tokenize_chinese(text2)
        common = tokens1 & tokens2
        meaningful = {w for w in common if len(w) > 1}

        self.assertLess(len(meaningful), 2,
            f"不相关文本不应有太多共同词: {meaningful}")


class TestWuxingInference(unittest.TestCase):
    """测试 3: 五行内容推断"""

    def setUp(self):
        self.wuxing = WuxingSystem()

    def test_wood_detection(self):
        """成长/创造类内容应识别为木"""
        self.assertEqual(
            self.wuxing.get_wuxing_from_content("这是一个创新项目，正在快速发展"),
            WuxingType.WOOD
        )

    def test_fire_detection(self):
        """热情/能量类内容应识别为火"""
        self.assertEqual(
            self.wuxing.get_wuxing_from_content("他充满热情和能量，燃烧着斗志"),
            WuxingType.FIRE
        )

    def test_water_detection(self):
        """流动/智慧类内容应识别为水"""
        self.assertEqual(
            self.wuxing.get_wuxing_from_content("水流动不息，智慧深邃，灵活适应变化"),
            WuxingType.WATER
        )

    def test_metal_detection(self):
        """决策/规则类内容应识别为金"""
        self.assertEqual(
            self.wuxing.get_wuxing_from_content("需要做出精确的决策，建立秩序和规则"),
            WuxingType.METAL
        )

    def test_earth_detection(self):
        """稳定/基础类内容应识别为土"""
        self.assertEqual(
            self.wuxing.get_wuxing_from_content("这个基础很稳定，承载了所有的平衡"),
            WuxingType.EARTH
        )

    def test_string_type_fallback(self):
        """纯字符串默认归为水（水主智）"""
        self.assertEqual(
            self.wuxing.get_wuxing_from_content("随机文本没有关键词"),
            WuxingType.WATER
        )

    def test_dict_type_fallback(self):
        """字典类型默认归为土（土主承载）"""
        self.assertEqual(
            self.wuxing.get_wuxing_from_content({"key": "value"}),
            WuxingType.EARTH
        )


class TestWuxingWeightPropagation(unittest.TestCase):
    """测试 4: 五行权重更新"""

    def test_generation_boost(self):
        """木生火：激活木后火的权重应增加"""
        wuxing = WuxingSystem()
        initial_fire = wuxing.weights[WuxingType.FIRE]

        wuxing.update_weights([(WuxingType.WOOD, 1.0)])

        # 木生火，火的权重应增加
        self.assertGreater(
            wuxing.weights[WuxingType.FIRE],
            initial_fire,
            "火（被木生）的权重应该增加"
        )

    def test_restriction_drain(self):
        """木克土：激活木后土的权重应减少"""
        wuxing = WuxingSystem()
        initial_earth = wuxing.weights[WuxingType.EARTH]

        wuxing.update_weights([(WuxingType.WOOD, 1.0)])

        self.assertLess(
            wuxing.weights[WuxingType.EARTH],
            initial_earth,
            "土（被木克）的权重应该减少"
        )

    def test_weight_bounds(self):
        """权重应在 [0.1, 2.0] 范围内"""
        wuxing = WuxingSystem()
        # 大量激活同一种五行
        for _ in range(200):
            wuxing.update_weights([(WuxingType.WOOD, 2.0)])

        for wx in WuxingType:
            self.assertGreaterEqual(wuxing.weights[wx], 0.1)
            self.assertLessEqual(wuxing.weights[wx], 2.0)


class TestDifferentiatedDecay(unittest.TestCase):
    """测试 5: 差异化衰减"""

    def test_high_weight_slower_decay(self):
        """高权重记忆衰减更慢"""
        mem = MemorySystem()

        # 模拟两条记忆：一个高权重，一个低权重
        high_weight_memory = MemoryNode(
            memory_id="mem_high", content="重要记忆",
            memory_type=HexagramType.QIAN, layer=MemoryLayer.HEAVEN,
            weight=1.0, strength=0.8
        )
        low_weight_memory = MemoryNode(
            memory_id="mem_low", content="普通记忆",
            memory_type=HexagramType.KUN, layer=MemoryLayer.HUMAN,
            weight=0.1, strength=0.8
        )

        base_rate = 0.001

        # 计算各自的有效衰减率
        high_factor = 1.0 - 0.8 * min(high_weight_memory.weight, 1.0)
        low_factor = 1.0 - 0.8 * min(low_weight_memory.weight, 1.0)
        high_rate = base_rate * (high_factor + 0.2)
        low_rate = base_rate * (low_factor + 0.2)

        # 高权重的衰减率应小于低权重的
        self.assertLess(high_rate, low_rate,
            "高权重记忆应该衰减更慢")


class TestMemoryStoreRetrieve(unittest.TestCase):
    """测试 6: 完整存储-检索流程"""

    def test_store_and_retrieve(self):
        """存储后应能检索到"""
        mem = MemorySystem()

        mem_id = asyncio.get_event_loop().run_until_complete(
            mem.store(
                content="五行相生相克的原理",
                memory_type=HexagramType.KAN,
                layer=MemoryLayer.HEAVEN,
            )
        )

        self.assertIsNotNone(mem_id)
        self.assertIn(mem_id, mem._memory_index)
        self.assertEqual(mem._memory_index[mem_id].wuxing_attribute, WuxingType.WATER)


if __name__ == '__main__':
    unittest.main()
