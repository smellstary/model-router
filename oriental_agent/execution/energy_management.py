"""
Energy Management System based on Yi Jin Jing principles
基于易筋经原理的能量管理系统
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class EnergyState(Enum):
    """能量状态"""
    ABUNDANT = "充沛"
    NORMAL = "正常"
    LOW = "偏低"
    DEPLETED = "耗尽"


@dataclass
class EnergyPool:
    """能量池"""
    pool_id: str
    pool_type: str
    capacity: float
    current_level: float
    regeneration_rate: float
    consumption_rate: float


@dataclass
class MeridianChannel:
    """经络通道"""
    channel_id: str
    channel_name: str
    flow_rate: float
    capacity: float
    connected_pools: List[str]


class EnergyManagementSystem:
    """能量管理系统 - 易筋经导引原理"""
    
    def __init__(self):
        self.energy_pools: Dict[str, EnergyPool] = {}
        self.meridian_channels: Dict[str, MeridianChannel] = {}
        self.energy_flow_history: List[Dict] = []
        
        self._initialize_default_pools()
        self._initialize_default_channels()
        
        self.metabolism_rate = 1.0
        self.restoration_rate = 0.1
    
    def _initialize_default_pools(self) -> None:
        """初始化默认能量池"""
        self.energy_pools = {
            'core': EnergyPool(
                pool_id='core',
                pool_type='核心',
                capacity=100.0,
                current_level=100.0,
                regeneration_rate=0.5,
                consumption_rate=0.0
            ),
            'memory': EnergyPool(
                pool_id='memory',
                pool_type='记忆',
                capacity=80.0,
                current_level=80.0,
                regeneration_rate=0.3,
                consumption_rate=0.0
            ),
            'thinking': EnergyPool(
                pool_id='thinking',
                pool_type='思考',
                capacity=60.0,
                current_level=60.0,
                regeneration_rate=0.4,
                consumption_rate=0.0
            ),
            'execution': EnergyPool(
                pool_id='execution',
                pool_type='执行',
                capacity=70.0,
                current_level=70.0,
                regeneration_rate=0.4,
                consumption_rate=0.0
            ),
            'perception': EnergyPool(
                pool_id='perception',
                pool_type='感知',
                capacity=50.0,
                current_level=50.0,
                regeneration_rate=0.3,
                consumption_rate=0.0
            )
        }
    
    def _initialize_default_channels(self) -> None:
        """初始化默认经络通道"""
        self.meridian_channels = {
            'ren_mai': MeridianChannel(
                channel_id='ren_mai',
                channel_name='任脉',
                flow_rate=1.0,
                capacity=100.0,
                connected_pools=['core', 'thinking']
            ),
            'du_mai': MeridianChannel(
                channel_id='du_mai',
                channel_name='督脉',
                flow_rate=1.0,
                capacity=100.0,
                connected_pools=['core', 'execution']
            ),
            'chong_mai': MeridianChannel(
                channel_id='chong_mai',
                channel_name='冲脉',
                flow_rate=0.8,
                capacity=80.0,
                connected_pools=['core', 'memory']
            )
        }
    
    def allocate_energy(
        self,
        pool_id: str,
        amount: float,
        priority: str = 'normal'
    ) -> bool:
        """分配能量"""
        if pool_id not in self.energy_pools:
            return False
        
        pool = self.energy_pools[pool_id]
        
        if pool.current_level >= amount:
            pool.current_level -= amount
            pool.consumption_rate += amount * 0.1
            return True
        
        return False
    
    def release_energy(
        self,
        pool_id: str,
        amount: float
    ) -> bool:
        """释放能量"""
        if pool_id not in self.energy_pools:
            return False
        
        pool = self.energy_pools[pool_id]
        
        if pool.current_level + amount <= pool.capacity:
            pool.current_level += amount
            return True
        
        return False
    
    def transfer_energy(
        self,
        from_pool: str,
        to_pool: str,
        amount: float
    ) -> bool:
        """经络传输能量"""
        if from_pool not in self.energy_pools or to_pool not in self.energy_pools:
            return False
        
        if self.allocate_energy(from_pool, amount):
            transfer_efficiency = self._calculate_transfer_efficiency(from_pool, to_pool)
            actual_amount = amount * transfer_efficiency
            self.release_energy(to_pool, actual_amount)
            return True
        
        return False
    
    def _calculate_transfer_efficiency(self, from_pool: str, to_pool: str) -> float:
        """计算传输效率"""
        channel_efficiency = 0.9
        
        for channel in self.meridian_channels.values():
            if from_pool in channel.connected_pools and to_pool in channel.connected_pools:
                channel_efficiency = channel.flow_rate * 0.95
        
        return channel_efficiency
    
    def regulate_flow(
        self,
        channel_id: str,
        target_flow: float
    ) -> bool:
        """调节经络流量"""
        if channel_id not in self.meridian_channels:
            return False
        
        channel = self.meridian_channels[channel_id]
        channel.flow_rate = max(0.1, min(1.0, target_flow))
        return True
    
    def circulate_energy(self) -> Dict[str, float]:
        """运行能量循环"""
        circulation_amounts = {}
        
        for channel_id, channel in self.meridian_channels.items():
            if channel.flow_rate > 0:
                pools = channel.connected_pools
                if len(pools) >= 2:
                    amount = channel.flow_rate * 10.0
                    self.transfer_energy(pools[0], pools[1], amount)
                    circulation_amounts[channel_id] = amount
        
        return circulation_amounts
    
    def optimize_allocation(
        self,
        task_demands: Dict[str, float]
    ) -> Dict[str, float]:
        """优化能量分配"""
        total_demand = sum(task_demands.values())
        total_available = self.get_total_available_energy()
        
        if total_available < total_demand:
            allocation = self._emergency_allocation(task_demands)
        else:
            allocation = self._normal_allocation(task_demands)
        
        return allocation
    
    def _normal_allocation(
        self,
        task_demands: Dict[str, float]
    ) -> Dict[str, float]:
        """正常分配策略"""
        allocation = {}
        total_demand = sum(task_demands.values())
        
        for pool_id, demand in task_demands.items():
            proportion = demand / total_demand if total_demand > 0 else 0
            pool = self.energy_pools.get(pool_id)
            if pool:
                target_level = pool.capacity * proportion
                if pool.current_level < target_level:
                    needed = target_level - pool.current_level
                    self.release_energy(pool_id, needed)
                allocation[pool_id] = target_level
        
        return allocation
    
    def _emergency_allocation(
        self,
        task_demands: Dict[str, float]
    ) -> Dict[str, float]:
        """紧急分配策略 - 优先核心功能"""
        allocation = {}
        priorities = {
            'core': 1.0,
            'execution': 0.7,
            'thinking': 0.6,
            'memory': 0.4,
            'perception': 0.3
        }
        
        sorted_tasks = sorted(
            task_demands.items(),
            key=lambda x: priorities.get(x[0], 0.5),
            reverse=True
        )
        
        remaining = self.get_total_available_energy()
        
        for pool_id, demand in sorted_tasks:
            allocated = min(demand, remaining)
            allocation[pool_id] = allocated
            remaining -= allocated
        
        return allocation
    
    def get_total_available_energy(self) -> float:
        """获取总可用能量"""
        return sum(pool.current_level for pool in self.energy_pools.values())
    
    def get_total_capacity(self) -> float:
        """获取总容量"""
        return sum(pool.capacity for pool in self.energy_pools.values())
    
    def get_energy_state(self, pool_id: str) -> EnergyState:
        """获取能量池状态"""
        if pool_id not in self.energy_pools:
            return EnergyState.NORMAL
        
        pool = self.energy_pools[pool_id]
        ratio = pool.current_level / pool.capacity
        
        if ratio >= 0.8:
            return EnergyState.ABUNDANT
        elif ratio >= 0.5:
            return EnergyState.NORMAL
        elif ratio >= 0.2:
            return EnergyState.LOW
        else:
            return EnergyState.DEPLETED
    
    def update_metabolism(self, delta_time: float) -> None:
        """更新代谢"""
        self.metabolism_rate = max(0.5, min(2.0, self.metabolism_rate))
        
        for pool in self.energy_pools.values():
            consumption = pool.consumption_rate * delta_time
            pool.consumption_rate = max(0, pool.consumption_rate - 0.01)
            
            regeneration = pool.regeneration_rate * self.metabolism_rate * delta_time
            pool.current_level = min(
                pool.capacity,
                max(0, pool.current_level + regeneration - consumption)
            )
        
        self.circulate_energy()
    
    def suggest_energy_recovery(self) -> Dict[str, Any]:
        """建议能量恢复"""
        suggestions = []
        
        for pool_id, pool in self.energy_pools.items():
            if pool.current_level < pool.capacity * 0.5:
                suggestions.append({
                    'pool_id': pool_id,
                    'current': pool.current_level,
                    'target': pool.capacity * 0.8,
                    'method': self._suggest_recovery_method(pool_id)
                })
        
        return {
            'suggestions': suggestions,
            'overall_status': self.get_overall_energy_status()
        }
    
    def _suggest_recovery_method(self, pool_id: str) -> str:
        """建议恢复方法"""
        methods = {
            'core': '静心调息，汇聚元气',
            'memory': '整理归纳，消化吸收',
            'thinking': '放松冥想，梳理思路',
            'execution': '休养生息，蓄势待发',
            'perception': '收敛感官，减少输入'
        }
        return methods.get(pool_id, '适当休息')
    
    def get_overall_energy_status(self) -> str:
        """获取整体能量状态"""
        available = self.get_total_available_energy()
        capacity = self.get_total_capacity()
        ratio = available / capacity if capacity > 0 else 0
        
        if ratio >= 0.8:
            return "能量充沛，气血充盈"
        elif ratio >= 0.6:
            return "能量充足，运行平稳"
        elif ratio >= 0.4:
            return "能量偏弱，需要休整"
        elif ratio >= 0.2:
            return "能量不足，急需恢复"
        else:
            return "能量枯竭，紧急救援"
    
    def trigger_recovery_mode(self) -> None:
        """触发恢复模式"""
        for pool in self.energy_pools.values():
            pool.regeneration_rate *= 1.5
        
        for channel in self.meridian_channels.values():
            channel.flow_rate = 1.0
        
        self.metabolism_rate = 0.5
    
    def exit_recovery_mode(self) -> None:
        """退出恢复模式"""
        self._initialize_default_pools()
        self._initialize_default_channels()
        self.metabolism_rate = 1.0
    
    def get_system_state(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            'total_available': self.get_total_available_energy(),
            'total_capacity': self.get_total_capacity(),
            'utilization_ratio': self.get_total_available_energy() / self.get_total_capacity() if self.get_total_capacity() > 0 else 0,
            'metabolism_rate': self.metabolism_rate,
            'pool_states': {
                pool_id: {
                    'level': pool.current_level,
                    'capacity': pool.capacity,
                    'state': self.get_energy_state(pool_id).value
                }
                for pool_id, pool in self.energy_pools.items()
            },
            'channel_flows': {
                channel_id: channel.flow_rate
                for channel_id, channel in self.meridian_channels.items()
            },
            'overall_status': self.get_overall_energy_status()
        }
