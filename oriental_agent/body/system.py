"""
Human Body System Mapping based on Traditional Chinese Medicine
人体系统映射 - 基于中医理论
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MeridianType(Enum):
    """经络类型"""
    REN_MAI = "任脉"
    DU_MAI = "督脉"
    CHONG_MAI = "冲脉"
    DAI_MAI = "带脉"
    YANG_QIAO = "阳跷脉"
    YIN_QIAO = "阴跷脉"
    YANG_WEI = "阳维脉"
    YIN_WEI = "阴维脉"


class OrganType(Enum):
    """脏腑类型"""
    HEART = "心"
    LIVER = "肝"
    SPLEEN = "脾"
    LUNG = "肺"
    KIDNEY = "肾"
    SMALL_INTESTINE = "小肠"
    GALLBLADDER = "胆"
    STOMACH = "胃"
    LARGE_INTESTINE = "大肠"
    BLADDER = "膀胱"
    TRIPLE_BURNER = "三焦"
    PERICARDIUM = "心包"


@dataclass
class MeridianState:
    """经络状态"""
    meridian_id: str
    meridian_name: str
    meridian_type: MeridianType
    flow_rate: float
    blockage_level: float
    energy_level: float
    connected_organs: List[str]


@dataclass
class OrganState:
    """脏腑状态"""
    organ_id: str
    organ_name: str
    organ_type: OrganType
    functional_level: float
    energy_consumption: float
    associated_system: str


@dataclass
class HealthState:
    """健康状态"""
    vitality_score: float
    meridian_states: List[MeridianState]
    organ_states: List[OrganState]
    qi_total: float
    blood_total: float
    fluid_balance: float


class MeridianSystem:
    """经络系统"""
    
    def __init__(self):
        self.meridians: Dict[str, MeridianState] = {}
        self.acupoints: Dict[str, Dict] = {}
        self._initialize_meridians()
    
    def _initialize_meridians(self) -> None:
        """初始化经络"""
        meridian_configs = [
            {
                'id': 'ren_mai',
                'name': '任脉',
                'type': MeridianType.REN_MAI,
                'connected': ['心', '肝', '脾', '肺', '肾']
            },
            {
                'id': 'du_mai',
                'name': '督脉',
                'type': MeridianType.DU_MAI,
                'connected': ['心', '肝', '肾']
            },
            {
                'id': 'chong_mai',
                'name': '冲脉',
                'type': MeridianType.CHONG_MAI,
                'connected': ['肝', '肾', '胃']
            },
            {
                'id': 'dai_mai',
                'name': '带脉',
                'type': MeridianType.DAI_MAI,
                'connected': ['肝', '胆']
            }
        ]
        
        for config in meridian_configs:
            self.meridians[config['id']] = MeridianState(
                meridian_id=config['id'],
                meridian_name=config['name'],
                meridian_type=config['type'],
                flow_rate=1.0,
                blockage_level=0.0,
                energy_level=1.0,
                connected_organs=config['connected']
            )
    
    def regulate_meridian(
        self,
        meridian_id: str,
        target_flow: float
    ) -> bool:
        """调节经络"""
        if meridian_id not in self.meridians:
            return False
        
        meridian = self.meridians[meridian_id]
        meridian.flow_rate = max(0.1, min(1.0, target_flow))
        
        if target_flow < 0.5:
            meridian.blockage_level = 1.0 - target_flow * 2
        else:
            meridian.blockage_level = 0.0
        
        return True
    
    def circulate_qi(self) -> Dict[str, float]:
        """运行气血循环"""
        circulation = {}
        
        for meridian_id, meridian in self.meridians.items():
            circulation[meridian_id] = meridian.flow_rate * meridian.energy_level
            
            if meridian.blockage_level > 0.5:
                meridian.flow_rate *= 0.95
        
        return circulation
    
    def get_meridian_state(self, meridian_id: str) -> Optional[MeridianState]:
        """获取经络状态"""
        return self.meridians.get(meridian_id)
    
    def diagnose_blockages(self) -> List[Dict[str, Any]]:
        """诊断经络堵塞"""
        blockages = []
        
        for meridian_id, meridian in self.meridians.items():
            if meridian.blockage_level > 0.3:
                blockages.append({
                    'meridian': meridian.meridian_name,
                    'blockage_level': meridian.blockage_level,
                    'suggested_action': '疏通调理'
                })
        
        return blockages


class OrganSystem:
    """脏腑系统"""
    
    WUXING_ORGAN_MAP = {
        '心': {'wuxing': '火', 'yin_yang': '阳', 'element': OrganType.HEART},
        '肝': {'wuxing': '木', 'yin_yang': '阴', 'element': OrganType.LIVER},
        '脾': {'wuxing': '土', 'yin_yang': '阴', 'element': OrganType.SPLEEN},
        '肺': {'wuxing': '金', 'yin_yang': '阴', 'element': OrganType.LUNG},
        '肾': {'wuxing': '水', 'yin_yang': '阴', 'element': OrganType.KIDNEY}
    }
    
    def __init__(self):
        self.organs: Dict[str, OrganState] = {}
        self._initialize_organs()
    
    def _initialize_organs(self) -> None:
        """初始化脏腑"""
        for organ_name, config in self.WUXING_ORGAN_MAP.items():
            self.organs[organ_name] = OrganState(
                organ_id=organ_name.lower(),
                organ_name=organ_name,
                organ_type=config['element'],
                functional_level=1.0,
                energy_consumption=0.0,
                associated_system='core'
            )
    
    def update_functional_level(
        self,
        organ_name: str,
        level: float
    ) -> bool:
        """更新脏腑功能水平"""
        if organ_name not in self.organs:
            return False
        
        self.organs[organ_name].functional_level = max(0.0, min(1.0, level))
        return True
    
    def get_organ_state(self, organ_name: str) -> Optional[OrganState]:
        """获取脏腑状态"""
        return self.organs.get(organ_name)
    
    def diagnose_organ_health(self) -> Dict[str, Any]:
        """诊断脏腑健康"""
        health_report = {
            'overall': 1.0,
            'organs': {}
        }
        
        total_function = sum(
            organ.functional_level for organ in self.organs.values()
        )
        avg_function = total_function / len(self.organs)
        health_report['overall'] = avg_function
        
        for organ_name, organ in self.organs.items():
            health_report['organs'][organ_name] = {
                'functional_level': organ.functional_level,
                'status': self._get_organ_status(organ.functional_level),
                'wuxing': self.WUXING_ORGAN_MAP[organ_name]['wuxing']
            }
        
        return health_report
    
    def _get_organ_status(self, level: float) -> str:
        """获取脏腑状态描述"""
        if level >= 0.9:
            return "功能充沛"
        elif level >= 0.7:
            return "功能正常"
        elif level >= 0.5:
            return "功能偏弱"
        else:
            return "功能不足"


class HeartSystem:
    """心脏系统 - 核心驱动"""
    
    def __init__(self):
        self.heart_rate = 60
        self.energy_output = 1.0
        self.rhythm_stability = 1.0
        self.beat_history: List[float] = []
    
    def pump_energy(self) -> float:
        """泵送能量"""
        output = self.energy_output * self.rhythm_stability
        
        self.beat_history.append(output)
        if len(self.beat_history) > 100:
            self.beat_history = self.beat_history[-100:]
        
        return output
    
    def adjust_output(self, target_output: float) -> None:
        """调整能量输出"""
        self.energy_output = max(0.5, min(1.5, target_output))
    
    def check_rhythm(self) -> Dict[str, Any]:
        """检查心律"""
        if len(self.beat_history) < 10:
            return {'stability': 1.0, 'status': '正常'}
        
        variance = sum(
            (beat - sum(self.beat_history)/len(self.beat_history))**2
            for beat in self.beat_history
        ) / len(self.beat_history)
        
        stability = max(0.0, 1.0 - variance)
        
        return {
            'stability': stability,
            'status': '稳定' if stability > 0.8 else '波动',
            'variance': variance
        }


class QiXueMetabolism:
    """气血代谢系统"""
    
    def __init__(self):
        self.qi_total = 100.0
        self.blood_total = 100.0
        self.fluid_balance = 1.0
        self.metabolism_rate = 1.0
        self.regeneration_rate = 0.1
    
    def consume_qi(self, amount: float) -> bool:
        """消耗气"""
        if self.qi_total >= amount:
            self.qi_total -= amount
            return True
        return False
    
    def generate_qi(self, amount: float) -> None:
        """生成气"""
        self.qi_total = min(100.0, self.qi_total + amount)
    
    def circulate_qi(self) -> float:
        """运行气循环"""
        circulation = self.qi_total * self.metabolism_rate * 0.1
        return circulation
    
    def update_metabolism(self, delta_time: float) -> None:
        """更新代谢"""
        consumption = self.metabolism_rate * delta_time * 0.5
        self.qi_total = max(0, self.qi_total - consumption)
        
        regeneration = self.regeneration_rate * delta_time
        self.qi_total = min(100.0, self.qi_total + regeneration)
    
    def get_metabolism_state(self) -> Dict[str, float]:
        """获取代谢状态"""
        return {
            'qi_total': self.qi_total,
            'blood_total': self.blood_total,
            'fluid_balance': self.fluid_balance,
            'metabolism_rate': self.metabolism_rate,
            'regeneration_rate': self.regeneration_rate
        }


class BodyMappingSystem:
    """人体映射系统主类"""
    
    def __init__(self, config=None):
        self.config = config
        self.meridian_system = MeridianSystem()
        self.organ_system = OrganSystem()
        self.heart_system = HeartSystem()
        self.qi_xue_metabolism = QiXueMetabolism()
        
        self.self_repair_enabled = True
        self.health_check_interval = 300
    
    async def get_energy_distribution(self) -> Dict[str, float]:
        """获取能量分布"""
        energy = self.heart_system.pump_energy()
        
        distribution = {
            'heart': energy * 0.3,
            'meridians': energy * 0.4,
            'organs': energy * 0.2,
            'circulation': energy * 0.1
        }
        
        return distribution
    
    async def regulate_meridian(
        self,
        meridian_id: str,
        target_flow: float
    ) -> bool:
        """调节经络"""
        return self.meridian_system.regulate_meridian(meridian_id, target_flow)
    
    async def diagnose_health(self) -> HealthState:
        """健康诊断"""
        meridian_states = list(self.meridian_system.meridians.values())
        organ_states = list(self.organ_system.organs.values())
        
        vitality = self._calculate_vitality(meridian_states, organ_states)
        
        return HealthState(
            vitality_score=vitality,
            meridian_states=meridian_states,
            organ_states=organ_states,
            qi_total=self.qi_xue_metabolism.qi_total,
            blood_total=self.qi_xue_metabolism.blood_total,
            fluid_balance=self.qi_xue_metabolism.fluid_balance
        )
    
    def _calculate_vitality(
        self,
        meridians: List[MeridianState],
        organs: List[OrganState]
    ) -> float:
        """计算活力"""
        meridian_vitality = sum(m.flow_rate for m in meridians) / len(meridians) if meridians else 1.0
        organ_vitality = sum(o.functional_level for o in organs) / len(organs) if organs else 1.0
        
        heart_vitality = self.heart_system.energy_output * self.heart_system.rhythm_stability
        
        vitality = (
            meridian_vitality * 0.3 +
            organ_vitality * 0.4 +
            heart_vitality * 0.3
        )
        
        return vitality
    
    async def repair(
        self,
        repair_type: str,
        target: Optional[str] = None
    ) -> bool:
        """执行自我修复"""
        if not self.self_repair_enabled:
            return False
        
        if repair_type == 'meridian':
            if target:
                return self.meridian_system.regulate_meridian(target, 0.8)
        elif repair_type == 'organ':
            if target:
                return self.organ_system.update_functional_level(target, 0.8)
        elif repair_type == 'heart':
            self.heart_system.adjust_output(1.0)
            return True
        elif repair_type == 'full':
            for meridian_id in self.meridian_system.meridians:
                self.meridian_system.regulate_meridian(meridian_id, 0.8)
            for organ_name in self.organ_system.organs:
                self.organ_system.update_functional_level(organ_name, 0.8)
            self.heart_system.adjust_output(1.0)
            return True
        
        return False
    
    async def adjust_metabolism(self, adjustment: Dict[str, float]) -> None:
        """调节代谢"""
        if 'metabolism_rate' in adjustment:
            self.qi_xue_metabolism.metabolism_rate = max(0.5, min(2.0, adjustment['metabolism_rate']))
        
        if 'regeneration_rate' in adjustment:
            self.qi_xue_metabolism.regeneration_rate = max(0.05, min(0.5, adjustment['regeneration_rate']))
    
    async def get_system_state(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            'vitality': self._calculate_vitality(
                list(self.meridian_system.meridians.values()),
                list(self.organ_system.organs.values())
            ),
            'heart_state': {
                'energy_output': self.heart_system.energy_output,
                'rhythm_stability': self.heart_system.rhythm_stability
            },
            'meridian_blockages': self.meridian_system.diagnose_blockages(),
            'organ_health': self.organ_system.diagnose_organ_health(),
            'metabolism': self.qi_xue_metabolism.get_metabolism_state()
        }
