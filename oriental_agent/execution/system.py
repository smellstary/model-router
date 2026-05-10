"""
Main Execution System - Integration of defense, energy, and behavior systems
执行系统主模块 - 整合防御、能量和行为系统
"""

import asyncio
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from core.types import ExecutionTask, DefenseState, BehaviorMode
from execution.defense import TaijiDefenseSystem, ThreatAssessment, ThreatLevel
from execution.energy_management import EnergyManagementSystem
from execution.behavior_modes import WuQinXiBehaviorSystem, BehaviorContext
from config.settings import get_config


@dataclass
class ExecutionResult:
    """执行结果"""
    task_id: str
    status: str
    outcome: Any
    execution_time: float
    energy_consumed: float
    defense_actions: List[Dict] = field(default_factory=list)
    behavior_mode: str = ""
    deviations: List[str] = field(default_factory=list)


class ExecutionSystem:
    """执行系统主类"""
    
    def __init__(self, config=None):
        self.config = config or get_config()
        
        self.defense_system = TaijiDefenseSystem()
        self.energy_system = EnergyManagementSystem()
        self.behavior_system = WuQinXiBehaviorSystem()
        
        self.active_tasks: Dict[str, ExecutionTask] = {}
        self.execution_history: List[ExecutionResult] = []
        self._lock = asyncio.Lock()
        
        self._monitoring_task: Optional[asyncio.Task] = None
        self._optimization_task: Optional[asyncio.Task] = None
    
    async def start(self) -> None:
        """启动执行系统"""
        self._monitoring_task = asyncio.create_task(self._monitoring_loop())
        self._optimization_task = asyncio.create_task(self._optimization_loop())
    
    async def stop(self) -> None:
        """停止执行系统"""
        if self._monitoring_task:
            self._monitoring_task.cancel()
        if self._optimization_task:
            self._optimization_task.cancel()
    
    async def execute(self, task: ExecutionTask) -> ExecutionResult:
        """执行任务"""
        start_time = datetime.now()
        
        async with self._lock:
            self.active_tasks[task.task_id] = task
        
        behavior_context = self._create_behavior_context(task)
        selected_mode = self.behavior_system.select_mode(behavior_context)
        
        threat_assessment = self.defense_system.assess_threat({
            'intensity': 0.3,
            'type': 'execution_risk',
            'source': 'task_execution'
        })
        defense_state = self.defense_system.execute_defense(threat_assessment)
        
        required_energy = self._estimate_energy_requirement(task, selected_mode)
        if not self.energy_system.allocate_energy('execution', required_energy):
            return ExecutionResult(
                task_id=task.task_id,
                status='failed',
                outcome='insufficient_energy',
                execution_time=0.0,
                energy_consumed=0.0,
                defense_actions=[],
                behavior_mode=selected_mode.value,
                deviations=['能量不足']
            )
        
        outcome = await self._perform_task(task, selected_mode)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        energy_consumed = required_energy * 0.8
        
        result = ExecutionResult(
            task_id=task.task_id,
            status='completed',
            outcome=outcome,
            execution_time=execution_time,
            energy_consumed=energy_consumed,
            defense_actions=[
                {'type': da.defense_type.value, 'effectiveness': da.effectiveness}
                for da in defense_state.active_defenses
            ],
            behavior_mode=selected_mode.value,
            deviations=[]
        )
        
        async with self._lock:
            self.active_tasks.pop(task.task_id, None)
            self.execution_history.append(result)
        
        return result
    
    async def _perform_task(
        self,
        task: ExecutionTask,
        mode: BehaviorMode
    ) -> Any:
        """执行具体任务"""
        execution_result = {
            'task_type': task.task_type,
            'actions_taken': len(task.action_sequence),
            'mode_used': mode.value,
            'completion': 'success'
        }
        
        return execution_result
    
    def _estimate_energy_requirement(
        self,
        task: ExecutionTask,
        mode: BehaviorMode
    ) -> float:
        """估算能量需求"""
        base_energy = task.priority * 5.0
        
        mode_costs = {
            BehaviorMode.TIGER: 1.5,
            BehaviorMode.DEER: 0.7,
            BehaviorMode.BEAR: 1.0,
            BehaviorMode.APE: 1.2,
            BehaviorMode.BIRD: 0.8
        }
        
        energy_mult = mode_costs.get(mode, 1.0)
        
        return base_energy * energy_mult
    
    def _create_behavior_context(self, task: ExecutionTask) -> BehaviorContext:
        """创建行为上下文"""
        return BehaviorContext(
            environment_type=self._infer_environment(task),
            threat_level=0.3,
            resource_availability=self.energy_system.get_total_available_energy() / 
                                  self.energy_system.get_total_capacity(),
            time_constraint=task.priority / 10.0 if task.priority else None,
            precision_requirement=0.6
        )
    
    def _infer_environment(self, task: ExecutionTask) -> str:
        """推断环境类型"""
        task_type = task.task_type.lower()
        
        if 'attack' in task_type or 'offensive' in task_type:
            return 'hostile'
        elif 'stealth' in task_type or 'hidden' in task_type:
            return 'stealth'
        elif 'stable' in task_type or 'maintain' in task_type:
            return 'stable'
        elif 'complex' in task_type or 'detail' in task_type:
            return 'complex'
        elif 'plan' in task_type or 'strategic' in task_type:
            return 'strategic'
        
        return 'stable'
    
    async def assess_threat(self) -> ThreatAssessment:
        """评估威胁"""
        threat_data = {
            'intensity': 0.3,
            'type': 'general',
            'source': 'system'
        }
        return self.defense_system.assess_threat(threat_data)
    
    async def activate_defense(
        self,
        defense_type: str,
        intensity: float = 0.5
    ) -> DefenseState:
        """激活防御"""
        threat = ThreatAssessment(
            threat_id=f"manual_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            threat_level=ThreatLevel.DEFINITE,
            threat_type=defense_type,
            source='manual',
            intensity=intensity
        )
        return self.defense_system.execute_defense(threat)
    
    async def select_behavior_mode(
        self,
        context: Optional[Dict[str, Any]] = None
    ) -> BehaviorMode:
        """选择行为模式"""
        behavior_context = BehaviorContext(
            environment_type=context.get('environment', 'stable') if context else 'stable',
            threat_level=context.get('threat_level', 0.3) if context else 0.3,
            resource_availability=context.get('resource_availability', 0.7) if context else 0.7
        )
        return self.behavior_system.select_mode(behavior_context)
    
    async def optimize_energy(self) -> Dict[str, float]:
        """优化能量分配"""
        task_demands = {}
        for task in self.active_tasks.values():
            mode = self.behavior_system.current_mode
            task_demands['execution'] = task_demands.get('execution', 0) + \
                                        self._estimate_energy_requirement(task, mode)
        
        allocation = self.energy_system.optimize_allocation(task_demands)
        return allocation
    
    async def get_system_state(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            'active_tasks': len(self.active_tasks),
            'execution_history_length': len(self.execution_history),
            'defense_state': self.defense_system.get_defense_state(),
            'energy_state': self.energy_system.get_system_state(),
            'behavior_state': self.behavior_system.get_system_state()
        }
    
    async def _monitoring_loop(self) -> None:
        """监控循环"""
        while True:
            await asyncio.sleep(5)
            
            threat_pred = self.defense_system.predict_next_threat()
            if threat_pred.get('recommended_readiness') == 'high':
                await self.activate_defense('preemptive', 0.4)
    
    async def _optimization_loop(self) -> None:
        """优化循环"""
        interval = self.config.get('execution.energy_optimization_interval', 60)
        while True:
            await asyncio.sleep(interval)
            await self.optimize_energy()
            self.energy_system.update_metabolism(interval / 60.0)
