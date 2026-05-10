"""
Body Module - 人体系统模块

包含：
- JingQiShenModel: 精气神三宝模型
- MeridianNetwork: 经络能量网络
- InstinctSystem: 人类本能分类体系
"""

from body.jing_qi_shen import JingQiShenModel, JingQiShenLevel, TreasureType, RegulationMode
from body.meridian_network import MeridianNetwork, MeridianChannel, MeridianCategory, EnergyFlowResult, BlockageInfo
from body.instinct_system import (
    InstinctSystem,
    InstinctEngine,
    InstinctTaxonomy,
    InstinctLevel,
    InstinctSignal,
    DriveState,
    DriveIntegration,
    BehaviorMapper,
    BehaviorMode
)

__all__ = [
    'JingQiShenModel',
    'JingQiShenLevel',
    'TreasureType',
    'RegulationMode',
    'MeridianNetwork',
    'MeridianChannel',
    'MeridianCategory',
    'EnergyFlowResult',
    'BlockageInfo',
    'InstinctSystem',
    'InstinctEngine',
    'InstinctTaxonomy',
    'InstinctLevel',
    'InstinctSignal',
    'DriveState',
    'DriveIntegration',
    'BehaviorMapper',
    'BehaviorMode'
]
