"""
兼容垫片，不是安全边界。

武学攻防是叙事状态机，实现已迁到 narrative.martial_state_machine。
本文件只把旧导入路径转到那里，避免已有脚本立刻断开。

真实认证、限流和安全响应头只在 integration/：
- integration/config_secure.py
- integration/api_server_secure.py

不要把本模块写进安全说明，也不要在这里加鉴权逻辑。
"""

from narrative.martial_state_machine import (  # noqa: F401
    AdaptiveDefenseSelector,
    AnimalForm,
    Attack,
    AttackIntensity,
    DefenseResult,
    TaijiDefense,
    ThreatAnalysis,
    ThreatType,
    WuqinxiDefense,
    YijinjingDefense,
    create_martial_defense_system,
)

__all__ = [
    "AdaptiveDefenseSelector",
    "AnimalForm",
    "Attack",
    "AttackIntensity",
    "DefenseResult",
    "TaijiDefense",
    "ThreatAnalysis",
    "ThreatType",
    "WuqinxiDefense",
    "YijinjingDefense",
    "create_martial_defense_system",
]
