"""
Unit tests for Yin-Yang Dual-State Storage System
阴阳双态存储系统单元测试
"""

import unittest
import sys
import os
import importlib.util
from datetime import datetime

_test_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.join(_test_dir, '..', '..')

_yinyang_storage_path = os.path.join(_project_root, "oriental_agent", "memory", "yinyang_storage.py")
_spec = importlib.util.spec_from_file_location("yinyang_storage", _yinyang_storage_path)
yinyang_storage_module = importlib.util.module_from_spec(_spec)
sys.modules["yinyang_storage"] = yinyang_storage_module
_spec.loader.exec_module(yinyang_storage_module)

MemoryState = yinyang_storage_module.MemoryState
YinYangMemory = yinyang_storage_module.YinYangMemory
YinYangStorage = yinyang_storage_module.YinYangStorage
YinYangBalancer = yinyang_storage_module.YinYangBalancer


class TestYinYangMemory(unittest.TestCase):
    """YinYangMemory 阴阳双态记忆数据结构测试"""
    
    def test_create_yin_memory(self):
        """测试创建阴态记忆"""
        memory = YinYangMemory(
            content="测试内容",
            state=MemoryState.YIN
        )
        
        self.assertEqual(memory.state, MemoryState.YIN)
        self.assertTrue(memory.is_yin())
        self.assertFalse(memory.is_yang())
        self.assertLessEqual(memory.visibility, 0.4)
        self.assertLessEqual(memory.activity, 0.4)
        self.assertLessEqual(memory.accessibility, 0.4)
        self.assertLessEqual(memory.weight, 0.4)
    
    def test_create_yang_memory(self):
        """测试创建阳态记忆"""
        memory = YinYangMemory(
            content="测试内容",
            state=MemoryState.YANG
        )
        
        self.assertEqual(memory.state, MemoryState.YANG)
        self.assertTrue(memory.is_yang())
        self.assertFalse(memory.is_yin())
        self.assertGreaterEqual(memory.visibility, 0.6)
        self.assertGreaterEqual(memory.activity, 0.6)
        self.assertGreaterEqual(memory.accessibility, 0.6)
        self.assertGreaterEqual(memory.weight, 0.6)
    
    def test_transform_yin_to_yang(self):
        """测试阴态转阳态（阳化）"""
        memory = YinYangMemory(
            content="测试内容",
            state=MemoryState.YIN
        )
        
        self.assertTrue(memory.is_yin())
        
        result = memory.transform_to_yang(intensity=0.8)
        
        self.assertTrue(result)
        self.assertTrue(memory.is_yang())
        self.assertGreater(memory.visibility, 0.5)
        self.assertGreater(memory.activity, 0.5)
        self.assertGreater(memory.accessibility, 0.5)
        self.assertGreater(memory.weight, 0.5)
        self.assertEqual(memory.transform_count, 1)
        self.assertIsNotNone(memory.last_transformed)
    
    def test_transform_yang_to_yin(self):
        """测试阳态转阴态（阴化）"""
        memory = YinYangMemory(
            content="测试内容",
            state=MemoryState.YANG
        )
        
        self.assertTrue(memory.is_yang())
        
        result = memory.transform_to_yin(intensity=0.8)
        
        self.assertTrue(result)
        self.assertTrue(memory.is_yin())
        self.assertLess(memory.visibility, 0.5)
        self.assertLess(memory.activity, 0.5)
        self.assertLess(memory.accessibility, 0.5)
        self.assertLess(memory.weight, 0.5)
        self.assertEqual(memory.transform_count, 1)
    
    def test_transform_same_state_returns_false(self):
        """测试对同状态转化返回False"""
        yin_memory = YinYangMemory(state=MemoryState.YIN)
        yang_memory = YinYangMemory(state=MemoryState.YANG)
        
        self.assertFalse(yin_memory.transform_to_yin())
        self.assertFalse(yang_memory.transform_to_yang())
    
    def test_transform_intensity_bounds(self):
        """测试转化强度边界值"""
        memory = YinYangMemory(state=MemoryState.YIN)
        
        memory.transform_to_yang(intensity=0.3)
        self.assertGreaterEqual(memory.visibility, 0.5)
        
        memory.transform_to_yin(intensity=1.5)
        self.assertGreaterEqual(memory.visibility, 0.1)
    
    def test_memory_has_unique_id(self):
        """测试每个记忆有唯一ID"""
        memory1 = YinYangMemory(content="内容1")
        memory2 = YinYangMemory(content="内容2")
        
        self.assertNotEqual(memory1.memory_id, memory2.memory_id)
    
    def test_to_dict(self):
        """测试转换为字典"""
        memory = YinYangMemory(
            content="测试内容",
            state=MemoryState.YIN,
            tags=["标签1", "标签2"]
        )
        
        result = memory.to_dict()
        
        self.assertEqual(result['state'], "阴态")
        self.assertEqual(result['content'], "测试内容")
        self.assertIn("标签1", result['tags'])
        self.assertIn("标签2", result['tags'])


class TestYinYangStorage(unittest.TestCase):
    """YinYangStorage 阴阳双态存储系统测试"""
    
    def test_store_default_yin_state(self):
        """测试存储默认为阴态"""
        storage = YinYangStorage()
        
        memory = storage.store(content="测试内容")
        
        self.assertTrue(memory.is_yin())
        self.assertEqual(len(storage.get_all_memories()), 1)
    
    def test_store_with_yang_state(self):
        """测试存储指定阳态"""
        storage = YinYangStorage()
        
        memory = storage.store(
            content="测试内容",
            initial_state=MemoryState.YANG
        )
        
        self.assertTrue(memory.is_yang())
    
    def test_activate_memory(self):
        """测试激活（阳化）记忆"""
        storage = YinYangStorage()
        memory = storage.store(content="测试内容")
        
        self.assertTrue(memory.is_yin())
        
        activated = storage.activate(memory.memory_id)
        
        self.assertIsNotNone(activated)
        self.assertTrue(activated.is_yang())
    
    def test_recess_memory(self):
        """测试潜隐（阴化）记忆"""
        storage = YinYangStorage()
        memory = storage.store(
            content="测试内容",
            initial_state=MemoryState.YANG
        )
        
        self.assertTrue(memory.is_yang())
        
        recessed = storage.recess(memory.memory_id)
        
        self.assertIsNotNone(recessed)
        self.assertTrue(recessed.is_yin())
    
    def test_activate_nonexistent_memory(self):
        """测试激活不存在的记忆"""
        storage = YinYangStorage()
        
        result = storage.activate("nonexistent-id")
        
        self.assertIsNone(result)
    
    def test_get_memory(self):
        """测试获取记忆"""
        storage = YinYangStorage()
        memory = storage.store(content="测试内容")
        
        retrieved = storage.get(memory.memory_id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.memory_id, memory.memory_id)
    
    def test_delete_memory(self):
        """测试删除记忆"""
        storage = YinYangStorage()
        memory = storage.store(content="测试内容")
        
        self.assertTrue(storage.delete(memory.memory_id))
        self.assertIsNone(storage.get(memory.memory_id))
        self.assertFalse(storage.delete("nonexistent-id"))
    
    def test_get_yang_memories(self):
        """测试获取所有阳态记忆"""
        storage = YinYangStorage()
        
        storage.store(content="阴态1", initial_state=MemoryState.YIN)
        storage.store(content="阳态1", initial_state=MemoryState.YANG)
        storage.store(content="阳态2", initial_state=MemoryState.YANG)
        
        yang_memories = storage.get_yang_memories()
        
        self.assertEqual(len(yang_memories), 2)
    
    def test_get_yin_memories(self):
        """测试获取所有阴态记忆"""
        storage = YinYangStorage()
        
        storage.store(content="阴态1", initial_state=MemoryState.YIN)
        storage.store(content="阴态2", initial_state=MemoryState.YIN)
        storage.store(content="阳态1", initial_state=MemoryState.YANG)
        
        yin_memories = storage.get_yin_memories()
        
        self.assertEqual(len(yin_memories), 2)
    
    def test_search_by_state(self):
        """测试按状态搜索"""
        storage = YinYangStorage()
        
        storage.store(content="阴态1", initial_state=MemoryState.YIN)
        storage.store(content="阳态1", initial_state=MemoryState.YANG)
        
        results = storage.search(state=MemoryState.YANG)
        
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].is_yang())
    
    def test_search_by_tags(self):
        """测试按标签搜索"""
        storage = YinYangStorage()
        
        storage.store(content="内容1", tags=["重要", "工作"])
        storage.store(content="内容2", tags=["个人"])
        storage.store(content="内容3", tags=["工作"])
        
        results = storage.search(tags=["工作"])
        
        self.assertEqual(len(results), 2)
    
    def test_search_by_min_weight(self):
        """测试按最小权重搜索"""
        storage = YinYangStorage()
        
        storage.store(content="低权重", initial_state=MemoryState.YIN)
        storage.store(content="高权重", initial_state=MemoryState.YANG)
        
        results = storage.search(min_weight=0.5)
        
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].is_yang())
    
    def test_get_statistics(self):
        """测试获取统计信息"""
        storage = YinYangStorage()
        
        storage.store(content="阴态1", initial_state=MemoryState.YIN)
        storage.store(content="阴态2", initial_state=MemoryState.YIN)
        storage.store(content="阳态1", initial_state=MemoryState.YANG)
        
        stats = storage.get_statistics()
        
        self.assertEqual(stats['total_memories'], 3)
        self.assertEqual(stats['yin_memories'], 2)
        self.assertEqual(stats['yang_memories'], 1)
        self.assertAlmostEqual(stats['yin_ratio'], 2/3, places=2)
        self.assertAlmostEqual(stats['yang_ratio'], 1/3, places=2)
    
    def test_clear(self):
        """测试清空存储"""
        storage = YinYangStorage()
        
        storage.store(content="内容1")
        storage.store(content="内容2")
        
        count = storage.clear()
        
        self.assertEqual(count, 2)
        self.assertEqual(len(storage.get_all_memories()), 0)


class TestYinYangBalancer(unittest.TestCase):
    """YinYangBalancer 阴阳平衡调节器测试"""
    
    def test_calculate_ratio_empty_storage(self):
        """测试空存储的比例计算"""
        storage = YinYangStorage()
        balancer = storage.get_balancer()
        
        ratio = balancer.calculate_ratio()
        
        self.assertEqual(ratio['total'], 0)
        self.assertEqual(ratio['yang_ratio'], 0.5)
        self.assertEqual(ratio['yin_ratio'], 0.5)
    
    def test_calculate_ratio_balanced(self):
        """测试平衡状态的比例计算"""
        storage = YinYangStorage()
        
        for i in range(5):
            storage.store(content=f"阴态{i}", initial_state=MemoryState.YIN)
        for i in range(5):
            storage.store(content=f"阳态{i}", initial_state=MemoryState.YANG)
        
        balancer = storage.get_balancer()
        ratio = balancer.calculate_ratio()
        
        self.assertEqual(ratio['total'], 10)
        self.assertEqual(ratio['yang_ratio'], 0.5)
        self.assertEqual(ratio['yin_ratio'], 0.5)
    
    def test_check_balance_yang_excess(self):
        """测试阳盛阴衰检测"""
        storage = YinYangStorage()
        
        for i in range(8):
            storage.store(content=f"阳态{i}", initial_state=MemoryState.YANG)
        for i in range(2):
            storage.store(content=f"阴态{i}", initial_state=MemoryState.YIN)
        
        balancer = storage.get_balancer()
        is_imbalanced, status = balancer.check_balance()
        
        self.assertTrue(is_imbalanced)
        self.assertEqual(status, "阳盛阴衰")
    
    def test_check_balance_yin_excess(self):
        """测试阴盛阳衰检测"""
        storage = YinYangStorage()
        
        for i in range(8):
            storage.store(content=f"阴态{i}", initial_state=MemoryState.YIN)
        for i in range(2):
            storage.store(content=f"阳态{i}", initial_state=MemoryState.YANG)
        
        balancer = storage.get_balancer()
        is_imbalanced, status = balancer.check_balance()
        
        self.assertTrue(is_imbalanced)
        self.assertEqual(status, "阴盛阳衰")
    
    def test_check_balance_healthy(self):
        """测试健康平衡状态"""
        storage = YinYangStorage()
        
        for i in range(6):
            storage.store(content=f"阴态{i}", initial_state=MemoryState.YIN)
        for i in range(4):
            storage.store(content=f"阳态{i}", initial_state=MemoryState.YANG)
        
        balancer = storage.get_balancer()
        is_imbalanced, status = balancer.check_balance()
        
        self.assertFalse(is_imbalanced)
        self.assertEqual(status, "阴阳平衡")
    
    def test_balance_yang_excess_triggers_yinization(self):
        """测试阳态过多触发阴化"""
        storage = YinYangStorage()
        
        for i in range(8):
            storage.store(content=f"阳态{i}", initial_state=MemoryState.YANG)
        for i in range(2):
            storage.store(content=f"阴态{i}", initial_state=MemoryState.YIN)
        
        result = storage.balance()
        
        self.assertTrue(result['is_imbalanced'])
        self.assertGreater(len(result['adjustments']), 0)
        
        for adj in result['adjustments']:
            self.assertEqual(adj['action'], 'yinize')
            self.assertEqual(adj['from_state'], '阳态')
            self.assertEqual(adj['to_state'], '阴态')
    
    def test_balance_yin_excess_triggers_yangization(self):
        """测试阴态过多触发阳化"""
        storage = YinYangStorage()
        
        for i in range(8):
            storage.store(content=f"阴态{i}", initial_state=MemoryState.YIN)
        for i in range(2):
            storage.store(content=f"阳态{i}", initial_state=MemoryState.YANG)
        
        result = storage.balance()
        
        self.assertTrue(result['is_imbalanced'])
        self.assertGreater(len(result['adjustments']), 0)
        
        for adj in result['adjustments']:
            self.assertEqual(adj['action'], 'yangize')
            self.assertEqual(adj['from_state'], '阴态')
            self.assertEqual(adj['to_state'], '阳态')
    
    def test_balance_no_auto_adjust(self):
        """测试不自动调节"""
        storage = YinYangStorage()
        
        for i in range(8):
            storage.store(content=f"阳态{i}", initial_state=MemoryState.YANG)
        for i in range(2):
            storage.store(content=f"阴态{i}", initial_state=MemoryState.YIN)
        
        result = storage.balance(auto_adjust=False)
        
        self.assertTrue(result['is_imbalanced'])
        self.assertEqual(len(result['adjustments']), 0)
    
    def test_get_balance_report(self):
        """测试获取平衡报告"""
        storage = YinYangStorage()
        
        for i in range(7):
            storage.store(content=f"阳态{i}", initial_state=MemoryState.YANG)
        for i in range(3):
            storage.store(content=f"阴态{i}", initial_state=MemoryState.YIN)
        
        report = storage.get_balance_report()
        
        self.assertIn('current_state', report)
        self.assertIn('balance_status', report)
        self.assertIn('thresholds', report)
        self.assertEqual(report['current_state']['total_memories'], 10)
    
    def test_balance_after_adjustment(self):
        """测试调节后达到平衡"""
        storage = YinYangStorage()
        
        for i in range(8):
            storage.store(content=f"阳态{i}", initial_state=MemoryState.YANG)
        for i in range(2):
            storage.store(content=f"阴态{i}", initial_state=MemoryState.YIN)
        
        storage.balance()
        
        is_imbalanced, _ = storage.get_balancer().check_balance()
        self.assertFalse(is_imbalanced)
    
    def test_multiple_balance_operations(self):
        """测试多次平衡操作"""
        storage = YinYangStorage()
        
        for i in range(8):
            storage.store(content=f"阳态{i}", initial_state=MemoryState.YANG)
        
        storage.balance()
        
        for i in range(8):
            storage.store(content=f"阴态{i}", initial_state=MemoryState.YIN)
        
        storage.balance()
        
        balancer = storage.get_balancer()
        self.assertEqual(len(balancer.balance_history), 2)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流"""
        storage = YinYangStorage()
        
        m1 = storage.store(content="记忆1", tags=["工作"])
        m2 = storage.store(content="记忆2", tags=["工作"])
        m3 = storage.store(content="记忆3", tags=["个人"])
        
        self.assertTrue(all(m.is_yin() for m in [m1, m2, m3]))
        
        storage.activate(m1.memory_id)
        storage.activate(m2.memory_id)
        
        self.assertTrue(m1.is_yang())
        self.assertTrue(m2.is_yang())
        self.assertTrue(m3.is_yin())
        
        stats = storage.get_statistics()
        self.assertEqual(stats['yang_memories'], 2)
        self.assertEqual(stats['yin_memories'], 1)
        
        report = storage.get_balance_report()
        self.assertEqual(report['balance_status'], "阴阳平衡")
    
    def test_memory_transformation_cycle(self):
        """测试记忆转化循环"""
        memory = YinYangMemory(
            content="循环测试",
            state=MemoryState.YIN
        )
        
        self.assertTrue(memory.is_yin())
        self.assertEqual(memory.transform_count, 0)
        
        memory.transform_to_yang()
        self.assertTrue(memory.is_yang())
        self.assertEqual(memory.transform_count, 1)
        
        memory.transform_to_yin()
        self.assertTrue(memory.is_yin())
        self.assertEqual(memory.transform_count, 2)
        
        memory.transform_to_yang()
        self.assertTrue(memory.is_yang())
        self.assertEqual(memory.transform_count, 3)
    
    def test_storage_with_metadata(self):
        """测试带元数据的存储"""
        storage = YinYangStorage()
        
        memory = storage.store(
            content="重要记忆",
            initial_state=MemoryState.YANG,
            metadata={"priority": "high", "source": "user"},
            tags=["重要", "用户输入"]
        )
        
        self.assertEqual(memory.metadata["priority"], "high")
        self.assertIn("重要", memory.tags)
        self.assertTrue(memory.is_yang())
    
    def test_threshold_boundary(self):
        """测试阈值边界条件"""
        storage = YinYangStorage()
        
        for i in range(7):
            storage.store(content=f"阳态{i}", initial_state=MemoryState.YANG)
        for i in range(3):
            storage.store(content=f"阴态{i}", initial_state=MemoryState.YIN)
        
        balancer = storage.get_balancer()
        is_imbalanced, _ = balancer.check_balance()
        
        self.assertFalse(is_imbalanced)


if __name__ == '__main__':
    unittest.main(verbosity=2)
