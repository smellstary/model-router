"""
Main Oriental Wisdom Agent - Core System Integration
东方智慧智能体主模块 - 核心系统集成
"""

import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field

from config.settings import get_config
from core.types import (
    MemoryLayer, HexagramType, WuxingType, SenseType,
    ExecutionTask, ThinkingContext, TimeHorizon
)

from memory.system import MemorySystem
from thinking.system import ThinkingSystem
from execution.system import ExecutionSystem
from perception.system import PerceptionSystem
from body.system import BodyMappingSystem
from image.system import ImageAndQiSystem

from commercial.agent import CommercialAgent, ShangDaoAdvisor


@dataclass
class AgentState:
    """智能体状态"""
    status: str
    uptime: float
    cycle_count: int
    energy_level: float
    vitality: float
    active_systems: List[str]


@dataclass
class AgentResponse:
    """智能体响应"""
    response_text: str
    actions_taken: List[Dict]
    memory_updates: List[str]
    state_changes: Dict[str, Any]


class OrientalWisdomAgent:
    """东方智慧智能体主类 - 集成商道智能系统"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = get_config(config_path)
        
        self.memory_system = MemorySystem(self.config)
        self.thinking_system = ThinkingSystem(self.config, self.memory_system)
        self.execution_system = ExecutionSystem(self.config)
        self.perception_system = PerceptionSystem(self.config)
        self.body_system = BodyMappingSystem(self.config)
        self.image_system = ImageAndQiSystem(self.config)
        
        # 商道智能系统集成
        self.commercial_agent = CommercialAgent()
        self.shangdao_advisor = ShangDaoAdvisor()
        
        self.status = "initialized"
        self.start_time: Optional[datetime] = None
        self.cycle_count = 0
        
        self._main_loop_task: Optional[asyncio.Task] = None
        self._is_running = False
    
    async def start(self) -> None:
        """启动智能体"""
        if self.status == "running":
            return
        
        self.start_time = datetime.now()
        self.status = "starting"
        
        await self.memory_system.start()
        await self.execution_system.start()
        
        self._is_running = True
        self._main_loop_task = asyncio.create_task(self._main_loop())
        
        self.status = "running"
    
    async def stop(self) -> None:
        """停止智能体"""
        self._is_running = False
        
        if self._main_loop_task:
            self._main_loop_task.cancel()
            try:
                await self._main_loop_task
            except asyncio.CancelledError:
                pass
        
        await self.memory_system.stop()
        await self.execution_system.stop()
        
        self.status = "stopped"
    
    async def process(self, input_data: Any) -> AgentResponse:
        """处理输入"""
        self.cycle_count += 1
        
        response_text = ""
        actions_taken = []
        memory_updates = []
        state_changes = {}
        
        if isinstance(input_data, str):
            perception = self.perception_system.perceive(
                SenseType.MENTAL,
                {'thought': input_data}
            )
            
            query = self._create_memory_query(input_data)
            relevant_memories = await self.memory_system.retrieve(query)
            
            thinking_context = ThinkingContext(
                question=input_data,
                situation={'input': input_data},
                available_options=self._generate_options(input_data),
                relevant_memories=relevant_memories
            )
            thinking_result = await self.thinking_system.analyze(thinking_context)
            
            memory_id = await self.memory_system.store(
                content=input_data,
                memory_type=HexagramType.LI,
                layer=MemoryLayer.HUMAN,
                context={'cycle': self.cycle_count}
            )
            memory_updates.append(memory_id)
            
            response_text = self._generate_response(thinking_result)
            
            body_health = await self.body_system.diagnose_health()
            image_state = await self.image_system.update_image_state({
                'vitality': body_health.vitality_score,
                'activity_level': 'focused'
            })
            
            state_changes = {
                'cycle': self.cycle_count,
                'vitality': body_health.vitality_score,
                'thinking_confidence': thinking_result.confidence,
                'philosophy_contributions': thinking_result.philosophy_contributions
            }
        
        return AgentResponse(
            response_text=response_text,
            actions_taken=actions_taken,
            memory_updates=memory_updates,
            state_changes=state_changes
        )
    
    def _create_memory_query(self, input_data: str):
        """创建记忆查询"""
        from core.types import MemoryQuery, QueryType
        return MemoryQuery(
            query_type=QueryType.KEYWORD,
            keywords=input_data.split()[:5]
        )
    
    def _generate_options(self, input_data: str) -> List[str]:
        """生成选项"""
        return [
            f"深入分析{input_data}",
            f"简单回应{input_data}",
            f"综合思考{input_data}"
        ]
    
    def _generate_response(self, thinking_result) -> str:
        """生成响应"""
        conclusion = thinking_result.conclusion
        
        if isinstance(conclusion, dict):
            dialectical_insight = conclusion.get('dialectical_insight', '分析完成')
            harmony = conclusion.get('harmony_with_tao', 0.5)
            
            return f"基于综合思考分析：{dialectical_insight}。整体和谐度：{harmony:.2f}"
        
        return f"已处理您的输入。置信度：{thinking_result.confidence:.2f}"
    
    async def _main_loop(self) -> None:
        """主循环"""
        cycle_duration = self.config.get('core.system_cycle_duration', 0.5)
        
        while self._is_running:
            try:
                await asyncio.sleep(cycle_duration)
                
                if self.execution_system:
                    await self.execution_system.optimize_energy()
                
                body_state = await self.body_system.get_system_state()
                if body_state.get('vitality', 1.0) < 0.3:
                    await self.body_system.repair('full')
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                pass
    
    async def get_state(self) -> AgentState:
        """获取状态"""
        uptime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        memory_state = await self.memory_system.get_system_state()
        body_state = await self.body_system.get_system_state()
        image_state = await self.image_system.get_system_state()
        
        energy_level = body_state.get('metabolism', {}).get('qi_total', 0) / 100.0
        vitality = body_state.get('vitality', 0.8)
        
        return AgentState(
            status=self.status,
            uptime=uptime,
            cycle_count=self.cycle_count,
            energy_level=energy_level,
            vitality=vitality,
            active_systems=['memory', 'thinking', 'execution', 'perception', 'body', 'image']
        )
    
    async def get_full_state(self) -> Dict[str, Any]:
        """获取完整状态"""
        return {
            'agent': {
                'status': self.status,
                'uptime': (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
                'cycle_count': self.cycle_count
            },
            'memory': await self.memory_system.get_system_state(),
            'thinking': await self.thinking_system.get_system_state(),
            'execution': await self.execution_system.get_system_state(),
            'perception': self.perception_system.get_system_state(),
            'body': await self.body_system.get_system_state(),
            'image': await self.image_system.get_system_state(),
            'commercial': self.commercial_agent.get_state()
        }

    # ==================== 商道智能系统接口 ====================

    def analyze_business_opportunity(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        商机洞察分析

        Args:
            market_data: 市场数据

        Returns:
            商机分析结果
        """
        return self.commercial_agent.analyze_opportunity(market_data)

    def analyze_business_model(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        商业模式分析

        Args:
            model_data: 商业模式数据

        Returns:
            模式分析结果
        """
        return self.commercial_agent.analyze_business_model(model_data)

    def analyze_competition(
        self,
        competitor_data: Dict[str, Any],
        market_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        竞争分析

        Args:
            competitor_data: 竞争对手数据
            market_data: 市场数据

        Returns:
            竞争分析结果
        """
        return self.commercial_agent.analyze_competition(competitor_data, market_data)

    def analyze_investment(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        投资分析

        Args:
            project_data: 项目数据

        Returns:
            投资分析结果
        """
        return self.commercial_agent.analyze_investment(project_data)

    def formulate_strategy(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        战略规划

        Args:
            business_data: 业务数据

        Returns:
            战略规划结果
        """
        return self.commercial_agent.formulate_strategy(business_data)

    def generate_commercial_report(self, context: Dict[str, Any]) -> Any:
        """
        生成综合商业报告

        Args:
            context: 分析上下文数据

        Returns:
            商业分析报告
        """
        return self.commercial_agent.generate_comprehensive_report(context)

    def get_shangdao_wisdom(self) -> List[Dict[str, Any]]:
        """获取东方智慧商业洞察"""
        return self.commercial_agent.get_wisdom_insights()

    def get_shangdao_advice(self, situation: str) -> Dict[str, str]:
        """
        获取商道建议

        Args:
            situation: 情境类型 (startup/growth/mature/turnaround/crisis)

        Returns:
            商道建议
        """
        return self.shangdao_advisor.get_advice(situation)

    def evaluate_business_decision(
        self,
        decision: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        评估商业决策

        Args:
            decision: 决策描述
            context: 决策上下文

        Returns:
            决策评估结果
        """
        return self.shangdao_advisor.evaluate_decision(decision, context)


async def create_agent(config_path: Optional[str] = None) -> OrientalWisdomAgent:
    """创建智能体实例"""
    agent = OrientalWisdomAgent(config_path)
    await agent.start()
    return agent


if __name__ == "__main__":
    async def main():
        agent = await create_agent()
        
        print("东方智慧智能体已启动")
        print("=" * 50)
        
        response = await agent.process("你好，请介绍一下你自己")
        print(f"响应: {response.response_text}")
        print(f"状态变化: {response.state_changes}")
        
        state = await agent.get_state()
        print(f"\n智能体状态:")
        print(f"  状态: {state.status}")
        print(f"  运行时间: {state.uptime:.2f}秒")
        print(f"  循环次数: {state.cycle_count}")
        print(f"  能量等级: {state.energy_level:.2f}")
        print(f"  活力值: {state.vitality:.2f}")
        
        await agent.stop()
        print("\n智能体已停止")
    
    asyncio.run(main())
