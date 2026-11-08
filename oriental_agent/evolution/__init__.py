"""
Evolution Module - 进化模块

修炼自提升机制，实现系统自我进化能力
"""

from .cultivation import (
    CultivationLevel,
    CultivationMethod,
    CultivationProgress,
    ExperienceAccumulator,
    BreakthroughMechanism,
    SelfEvolutionEngine,
    TaskResult,
    BreakthroughResult,
    EvolutionPlan,
    create_cultivation_engine,
)

__all__ = [
    "CultivationLevel",
    "CultivationMethod",
    "CultivationProgress",
    "ExperienceAccumulator",
    "BreakthroughMechanism",
    "SelfEvolutionEngine",
    "TaskResult",
    "BreakthroughResult",
    "EvolutionPlan",
    "create_cultivation_engine",
]
