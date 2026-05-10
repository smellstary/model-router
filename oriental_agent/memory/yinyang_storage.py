"""
Yin-Yang Dual-State Storage System
阴阳双态存储系统

Implements the Oriental wisdom concept of Yin-Yang duality for memory management.
Each memory can exist in either Yin state (latent/hidden) or Yang state (manifest/active).
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import uuid


class MemoryState(Enum):
    """阴阳态枚举 - Yin-Yang Memory States"""
    YIN = "阴态"
    YANG = "阳态"


@dataclass
class YinYangMemory:
    """
    阴阳双态记忆数据结构 - Yin-Yang Dual-State Memory Data Structure
    
    阴态 (Yin State): 潜隐、内敛、低可访问性、低权重
    阳态 (Yang State): 显明、活跃、高可访问性、高权重
    """
    
    memory_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: Any = None
    state: MemoryState = MemoryState.YIN
    
    visibility: float = 0.3
    activity: float = 0.2
    accessibility: float = 0.3
    weight: float = 0.3
    
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    last_transformed: Optional[datetime] = None
    transform_count: int = 0
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self._sync_state_attributes()
    
    def _sync_state_attributes(self) -> None:
        """根据当前状态同步属性值"""
        if self.state == MemoryState.YIN:
            self._apply_yin_attributes()
        else:
            self._apply_yang_attributes()
    
    def _apply_yin_attributes(self) -> None:
        """应用阴态属性：潜隐、内敛、低可访问性、低权重"""
        self.visibility = min(self.visibility, 0.4)
        self.activity = min(self.activity, 0.4)
        self.accessibility = min(self.accessibility, 0.4)
        self.weight = min(self.weight, 0.4)
    
    def _apply_yang_attributes(self) -> None:
        """应用阳态属性：显明、活跃、高可访问性、高权重"""
        self.visibility = max(self.visibility, 0.6)
        self.activity = max(self.activity, 0.6)
        self.accessibility = max(self.accessibility, 0.6)
        self.weight = max(self.weight, 0.6)
    
    def transform_to_yang(self, intensity: float = 0.7) -> bool:
        """
        阳化：将记忆从阴态转化为阳态
        
        Args:
            intensity: 阳化强度，范围 [0.5, 1.0]
        
        Returns:
            是否成功转化
        """
        if self.state == MemoryState.YANG:
            return False
        
        intensity = max(0.5, min(1.0, intensity))
        
        self.state = MemoryState.YANG
        self.visibility = 0.5 + intensity * 0.5
        self.activity = 0.5 + intensity * 0.5
        self.accessibility = 0.5 + intensity * 0.5
        self.weight = 0.5 + intensity * 0.5
        
        self.last_transformed = datetime.now()
        self.transform_count += 1
        self.last_accessed = datetime.now()
        
        return True
    
    def transform_to_yin(self, intensity: float = 0.7) -> bool:
        """
        阴化：将记忆从阳态转化为阴态
        
        Args:
            intensity: 阴化强度，范围 [0.5, 1.0]
        
        Returns:
            是否成功转化
        """
        if self.state == MemoryState.YIN:
            return False
        
        intensity = max(0.5, min(1.0, intensity))
        
        self.state = MemoryState.YIN
        self.visibility = 0.5 - intensity * 0.4
        self.activity = 0.5 - intensity * 0.4
        self.accessibility = 0.5 - intensity * 0.4
        self.weight = 0.5 - intensity * 0.4
        
        self.visibility = max(0.1, self.visibility)
        self.activity = max(0.1, self.activity)
        self.accessibility = max(0.1, self.accessibility)
        self.weight = max(0.1, self.weight)
        
        self.last_transformed = datetime.now()
        self.transform_count += 1
        
        return True
    
    def is_yin(self) -> bool:
        """检查是否为阴态"""
        return self.state == MemoryState.YIN
    
    def is_yang(self) -> bool:
        """检查是否为阳态"""
        return self.state == MemoryState.YANG
    
    def get_state_name(self) -> str:
        """获取状态名称"""
        return self.state.value
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典表示"""
        return {
            'memory_id': self.memory_id,
            'content': str(self.content),
            'state': self.state.value,
            'visibility': self.visibility,
            'activity': self.activity,
            'accessibility': self.accessibility,
            'weight': self.weight,
            'created_at': self.created_at.isoformat(),
            'last_accessed': self.last_accessed.isoformat(),
            'last_transformed': self.last_transformed.isoformat() if self.last_transformed else None,
            'transform_count': self.transform_count,
            'metadata': self.metadata,
            'tags': self.tags
        }


class YinYangBalancer:
    """
    阴阳平衡调节器 - Yin-Yang Balance Regulator
    
    监控并调节系统整体阴阳比例，确保系统处于动态平衡状态。
    
    平衡规则：
    - 阳态超过70%触发阴化
    - 阴态超过70%触发阳化
    """
    
    YANG_THRESHOLD = 0.70
    YIN_THRESHOLD = 0.70
    TARGET_BALANCE = 0.50
    
    def __init__(self, storage: 'YinYangStorage' = None):
        self.storage = storage
        self.balance_history: List[Dict[str, Any]] = []
        self.adjustment_log: List[Dict[str, Any]] = []
    
    def calculate_ratio(self) -> Dict[str, float]:
        """
        计算当前阴阳比例
        
        Returns:
            包含阳态比例、阴态比例和总数的字典
        """
        if self.storage is None:
            return {'yang_ratio': 0.5, 'yin_ratio': 0.5, 'total': 0}
        
        memories = self.storage.get_all_memories()
        total = len(memories)
        
        if total == 0:
            return {'yang_ratio': 0.5, 'yin_ratio': 0.5, 'total': 0}
        
        yang_count = sum(1 for m in memories if m.is_yang())
        yin_count = total - yang_count
        
        yang_ratio = yang_count / total
        yin_ratio = yin_count / total
        
        return {
            'yang_ratio': yang_ratio,
            'yin_ratio': yin_ratio,
            'total': total,
            'yang_count': yang_count,
            'yin_count': yin_count
        }
    
    def check_balance(self) -> Tuple[bool, str]:
        """
        检查阴阳平衡状态
        
        Returns:
            (是否失衡, 状态描述)
        """
        ratio = self.calculate_ratio()
        yang_ratio = ratio['yang_ratio']
        yin_ratio = ratio['yin_ratio']
        
        if yang_ratio > self.YANG_THRESHOLD:
            return True, "阳盛阴衰"
        elif yin_ratio > self.YIN_THRESHOLD:
            return True, "阴盛阳衰"
        else:
            return False, "阴阳平衡"
    
    def balance(self, auto_adjust: bool = True) -> Dict[str, Any]:
        """
        执行阴阳平衡调节
        
        Args:
            auto_adjust: 是否自动执行调节
        
        Returns:
            调节结果报告
        """
        ratio = self.calculate_ratio()
        is_imbalanced, status = self.check_balance()
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'before': ratio,
            'status': status,
            'is_imbalanced': is_imbalanced,
            'adjustments': [],
            'after': None
        }
        
        if not is_imbalanced or not auto_adjust:
            result['after'] = self.calculate_ratio()
            self.balance_history.append(result)
            return result
        
        adjustments = []
        
        if ratio['yang_ratio'] > self.YANG_THRESHOLD:
            adjustments = self._perform_yinization(ratio)
        elif ratio['yin_ratio'] > self.YIN_THRESHOLD:
            adjustments = self._perform_yangization(ratio)
        
        result['adjustments'] = adjustments
        result['after'] = self.calculate_ratio()
        
        self.balance_history.append(result)
        self.adjustment_log.extend(adjustments)
        
        return result
    
    def _perform_yinization(self, ratio: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        执行阴化操作：将部分阳态记忆转化为阴态
        
        Args:
            ratio: 当前比例信息
        
        Returns:
            调整记录列表
        """
        adjustments = []
        yang_memories = [m for m in self.storage.get_all_memories() if m.is_yang()]
        
        excess_ratio = ratio['yang_ratio'] - self.TARGET_BALANCE
        target_count = int(excess_ratio * ratio['total'])
        
        yang_memories.sort(key=lambda m: m.weight)
        
        for memory in yang_memories[:target_count]:
            success = memory.transform_to_yin()
            if success:
                adjustments.append({
                    'memory_id': memory.memory_id,
                    'action': 'yinize',
                    'from_state': '阳态',
                    'to_state': '阴态',
                    'timestamp': datetime.now().isoformat()
                })
        
        return adjustments
    
    def _perform_yangization(self, ratio: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        执行阳化操作：将部分阴态记忆转化为阳态
        
        Args:
            ratio: 当前比例信息
        
        Returns:
            调整记录列表
        """
        adjustments = []
        yin_memories = [m for m in self.storage.get_all_memories() if m.is_yin()]
        
        excess_ratio = ratio['yin_ratio'] - self.TARGET_BALANCE
        target_count = int(excess_ratio * ratio['total'])
        
        yin_memories.sort(key=lambda m: m.weight, reverse=True)
        
        for memory in yin_memories[:target_count]:
            success = memory.transform_to_yang()
            if success:
                adjustments.append({
                    'memory_id': memory.memory_id,
                    'action': 'yangize',
                    'from_state': '阴态',
                    'to_state': '阳态',
                    'timestamp': datetime.now().isoformat()
                })
        
        return adjustments
    
    def get_balance_report(self) -> Dict[str, Any]:
        """
        获取阴阳平衡报告
        
        Returns:
            详细的平衡状态报告
        """
        ratio = self.calculate_ratio()
        is_imbalanced, status = self.check_balance()
        
        return {
            'current_state': {
                'yang_ratio': f"{ratio['yang_ratio']*100:.1f}%",
                'yin_ratio': f"{ratio['yin_ratio']*100:.1f}%",
                'total_memories': ratio['total'],
                'yang_count': ratio.get('yang_count', 0),
                'yin_count': ratio.get('yin_count', 0)
            },
            'balance_status': status,
            'is_imbalanced': is_imbalanced,
            'thresholds': {
                'yang_threshold': f"{self.YANG_THRESHOLD*100:.0f}%",
                'yin_threshold': f"{self.YIN_THRESHOLD*100:.0f}%",
                'target_balance': f"{self.TARGET_BALANCE*100:.0f}%"
            },
            'adjustment_history_count': len(self.adjustment_log),
            'balance_check_history_count': len(self.balance_history)
        }


class YinYangStorage:
    """
    阴阳双态存储系统 - Yin-Yang Dual-State Storage System
    
    核心功能：
    - store(): 存储记忆（默认阴态）
    - activate(): 阳化（激活）记忆
    - recess(): 阴化（潜隐）记忆
    - balance(): 平衡调节
    """
    
    def __init__(self):
        self._memories: Dict[str, YinYangMemory] = {}
        self._balancer: YinYangBalancer = YinYangBalancer(self)
        self._operation_log: List[Dict[str, Any]] = []
    
    def store(
        self,
        content: Any,
        initial_state: MemoryState = MemoryState.YIN,
        metadata: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> YinYangMemory:
        """
        存储记忆（默认阴态）
        
        Args:
            content: 记忆内容
            initial_state: 初始状态，默认为阴态
            metadata: 元数据
            tags: 标签列表
        
        Returns:
            创建的记忆对象
        """
        memory = YinYangMemory(
            content=content,
            state=initial_state,
            metadata=metadata or {},
            tags=tags or []
        )
        
        memory._sync_state_attributes()
        
        self._memories[memory.memory_id] = memory
        
        self._log_operation('store', memory)
        
        return memory
    
    def activate(
        self,
        memory_id: str,
        intensity: float = 0.7
    ) -> Optional[YinYangMemory]:
        """
        阳化（激活）记忆：将记忆从阴态转化为阳态
        
        Args:
            memory_id: 记忆ID
            intensity: 阳化强度
        
        Returns:
            激活后的记忆对象，如果不存在则返回None
        """
        memory = self._memories.get(memory_id)
        if memory is None:
            return None
        
        success = memory.transform_to_yang(intensity)
        if success:
            self._log_operation('activate', memory, {'intensity': intensity})
        
        return memory
    
    def recess(
        self,
        memory_id: str,
        intensity: float = 0.7
    ) -> Optional[YinYangMemory]:
        """
        阴化（潜隐）记忆：将记忆从阳态转化为阴态
        
        Args:
            memory_id: 记忆ID
            intensity: 阴化强度
        
        Returns:
            潜隐后的记忆对象，如果不存在则返回None
        """
        memory = self._memories.get(memory_id)
        if memory is None:
            return None
        
        success = memory.transform_to_yin(intensity)
        if success:
            self._log_operation('recess', memory, {'intensity': intensity})
        
        return memory
    
    def balance(self, auto_adjust: bool = True) -> Dict[str, Any]:
        """
        平衡调节：自动调节系统阴阳比例
        
        Args:
            auto_adjust: 是否自动执行调节
        
        Returns:
            调节结果报告
        """
        result = self._balancer.balance(auto_adjust)
        self._log_operation('balance', None, result)
        return result
    
    def get(self, memory_id: str) -> Optional[YinYangMemory]:
        """
        获取指定记忆
        
        Args:
            memory_id: 记忆ID
        
        Returns:
            记忆对象，如果不存在则返回None
        """
        memory = self._memories.get(memory_id)
        if memory:
            memory.last_accessed = datetime.now()
        return memory
    
    def get_all_memories(self) -> List[YinYangMemory]:
        """获取所有记忆"""
        return list(self._memories.values())
    
    def get_yang_memories(self) -> List[YinYangMemory]:
        """获取所有阳态记忆"""
        return [m for m in self._memories.values() if m.is_yang()]
    
    def get_yin_memories(self) -> List[YinYangMemory]:
        """获取所有阴态记忆"""
        return [m for m in self._memories.values() if m.is_yin()]
    
    def delete(self, memory_id: str) -> bool:
        """
        删除指定记忆
        
        Args:
            memory_id: 记忆ID
        
        Returns:
            是否成功删除
        """
        if memory_id in self._memories:
            memory = self._memories[memory_id]
            self._log_operation('delete', memory)
            del self._memories[memory_id]
            return True
        return False
    
    def search(
        self,
        state: Optional[MemoryState] = None,
        min_weight: Optional[float] = None,
        tags: Optional[List[str]] = None
    ) -> List[YinYangMemory]:
        """
        搜索记忆
        
        Args:
            state: 状态过滤
            min_weight: 最小权重过滤
            tags: 标签过滤
        
        Returns:
            符合条件的记忆列表
        """
        results = list(self._memories.values())
        
        if state is not None:
            results = [m for m in results if m.state == state]
        
        if min_weight is not None:
            results = [m for m in results if m.weight >= min_weight]
        
        if tags:
            results = [m for m in results if any(tag in m.tags for tag in tags)]
        
        return results
    
    def get_balancer(self) -> YinYangBalancer:
        """获取平衡调节器"""
        return self._balancer
    
    def get_balance_report(self) -> Dict[str, Any]:
        """获取阴阳平衡报告"""
        return self._balancer.get_balance_report()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取存储统计信息
        
        Returns:
            统计信息字典
        """
        total = len(self._memories)
        yang_count = sum(1 for m in self._memories.values() if m.is_yang())
        yin_count = total - yang_count
        
        avg_weight = (
            sum(m.weight for m in self._memories.values()) / total
            if total > 0 else 0
        )
        
        avg_accessibility = (
            sum(m.accessibility for m in self._memories.values()) / total
            if total > 0 else 0
        )
        
        return {
            'total_memories': total,
            'yang_memories': yang_count,
            'yin_memories': yin_count,
            'yang_ratio': yang_count / total if total > 0 else 0,
            'yin_ratio': yin_count / total if total > 0 else 0,
            'average_weight': avg_weight,
            'average_accessibility': avg_accessibility,
            'operation_count': len(self._operation_log)
        }
    
    def _log_operation(
        self,
        operation: str,
        memory: Optional[YinYangMemory],
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """记录操作日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'memory_id': memory.memory_id if memory else None,
            'details': details or {}
        }
        self._operation_log.append(log_entry)
    
    def clear(self) -> int:
        """
        清空所有记忆
        
        Returns:
            清除的记忆数量
        """
        count = len(self._memories)
        self._memories.clear()
        self._log_operation('clear', None, {'cleared_count': count})
        return count
