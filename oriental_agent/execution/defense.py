"""
Self-Adaptive Defense System based on Taiji principles
基于太极原理的自适应防御系统
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class ThreatLevel(Enum):
    """威胁等级"""
    NORMAL = 0
    POTENTIAL = 1
    DEFINITE = 2
    CRITICAL = 3


class DefenseType(Enum):
    """防御类型"""
    TAIJI_REDIRECT = "太极引化"
    TAIJI_ABSORB = "太极吸收"
    YIJINJING_REINFORCE = "易筋经强化"
    WUQINXI_ADAPT = "五禽戏适应"
    WUGONGSHI_DEFEND = "无声防守"


@dataclass
class ThreatAssessment:
    """威胁评估"""
    threat_id: str
    threat_level: ThreatLevel
    threat_type: str
    source: str
    intensity: float
    direction: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DefenseAction:
    """防御动作"""
    action_id: str
    defense_type: DefenseType
    parameters: Dict[str, Any] = field(default_factory=dict)
    effectiveness: float = 0.0
    energy_cost: float = 0.0
    execution_time: float = 0.0


@dataclass
class DefenseState:
    """防御状态"""
    threat_level: ThreatLevel
    active_defenses: List[DefenseType] = field(default_factory=list)
    energy_allocated: float = 0.0
    stability_score: float = 1.0
    defense_effectiveness: float = 0.0


class TaijiDefenseSystem:
    """太极防御系统 - 以柔克刚、借力打力"""
    
    def __init__(self):
        self.threat_history: List[ThreatAssessment] = []
        self.defense_actions: List[DefenseAction] = []
        self.defense_effectiveness_history: List[float] = []
        
        self.yin_yang_balance = 0.0
        self.redirect_threshold = 0.5
        self.absorb_threshold = 0.3
        self.reinforce_threshold = 0.7
    
    def assess_threat(self, threat_data: Any) -> ThreatAssessment:
        """评估威胁"""
        threat_id = f"threat_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        threat_level = self._determine_threat_level(threat_data)
        threat_type = self._classify_threat_type(threat_data)
        
        assessment = ThreatAssessment(
            threat_id=threat_id,
            threat_level=threat_level,
            threat_type=threat_type,
            source=self._identify_source(threat_data),
            intensity=self._calculate_intensity(threat_data),
            direction=self._determine_direction(threat_data)
        )
        
        self.threat_history.append(assessment)
        return assessment
    
    def _determine_threat_level(self, threat_data: Any) -> ThreatLevel:
        """确定威胁等级"""
        if isinstance(threat_data, dict):
            intensity = threat_data.get('intensity', 0.5)
        else:
            intensity = 0.5
        
        if intensity < 0.3:
            return ThreatLevel.NORMAL
        elif intensity < 0.5:
            return ThreatLevel.POTENTIAL
        elif intensity < 0.7:
            return ThreatLevel.DEFINITE
        else:
            return ThreatLevel.CRITICAL
    
    def _classify_threat_type(self, threat_data: Any) -> str:
        """分类威胁类型"""
        if isinstance(threat_data, dict):
            threat_type = threat_data.get('type', 'unknown')
        else:
            threat_type = str(type(threat_data).__name__)
        
        type_mapping = {
            'malware': '恶意攻击',
            'intrusion': '入侵威胁',
            'dos': '拒绝服务',
            'data_breach': '数据泄露',
            'unknown': '未知威胁'
        }
        
        return type_mapping.get(threat_type, threat_type)
    
    def _identify_source(self, threat_data: Any) -> str:
        """识别威胁来源"""
        if isinstance(threat_data, dict):
            return threat_data.get('source', 'unknown')
        return 'internal'
    
    def _calculate_intensity(self, threat_data: Any) -> float:
        """计算威胁强度"""
        if isinstance(threat_data, dict):
            return threat_data.get('intensity', 0.5)
        return 0.5
    
    def _determine_direction(self, threat_data: Any) -> str:
        """确定威胁方向"""
        if isinstance(threat_data, dict):
            return threat_data.get('direction', 'unknown')
        return 'neutral'
    
    def select_defense_strategy(
        self,
        threat: ThreatAssessment
    ) -> List[DefenseAction]:
        """选择防御策略"""
        actions = []
        
        if threat.intensity < self.redirect_threshold:
            action = self._create_taiji_redirect(threat)
            actions.append(action)
        elif threat.intensity < self.absorb_threshold:
            action = self._create_taiji_absorb(threat)
            actions.append(action)
        elif threat.intensity < self.reinforce_threshold:
            actions.append(self._create_yijinjing_reinforce(threat))
            actions.append(self._create_taiji_redirect(threat))
        else:
            actions.append(self._create_yijinjing_reinforce(threat))
            actions.append(self._create_wuqinxi_adapt(threat))
        
        return actions
    
    def _create_taiji_redirect(self, threat: ThreatAssessment) -> DefenseAction:
        """创建太极引化动作"""
        return DefenseAction(
            action_id=f"defense_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            defense_type=DefenseType.TAIJI_REDIRECT,
            parameters={
                'redirect_direction': self._calculate_redirect_direction(threat),
                'energy_ratio': 0.3,
                'follow_through': True
            },
            effectiveness=0.8,
            energy_cost=0.2,
            execution_time=0.1
        )
    
    def _create_taiji_absorb(self, threat: ThreatAssessment) -> DefenseAction:
        """创建太极吸收动作"""
        return DefenseAction(
            action_id=f"defense_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            defense_type=DefenseType.TAIJI_ABSORB,
            parameters={
                'absorption_rate': 0.5,
                'transformation_ratio': 0.7,
                'grounding': True
            },
            effectiveness=0.6,
            energy_cost=0.4,
            execution_time=0.2
        )
    
    def _create_yijinjing_reinforce(self, threat: ThreatAssessment) -> DefenseAction:
        """创建易筋经强化动作"""
        return DefenseAction(
            action_id=f"defense_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            defense_type=DefenseType.YIJINJING_REINFORCE,
            parameters={
                'reinforcement_level': 'high',
                'energy_circulation': True,
                'core_protection': True
            },
            effectiveness=0.9,
            energy_cost=0.5,
            execution_time=0.15
        )
    
    def _create_wuqinxi_adapt(self, threat: ThreatAssessment) -> DefenseAction:
        """创建五禽戏适应动作"""
        return DefenseAction(
            action_id=f"defense_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            defense_type=DefenseType.WUQINXI_ADAPT,
            parameters={
                'adaptation_mode': 'flexible',
                'posture': self._select_posture(threat),
                'movement': 'fluid'
            },
            effectiveness=0.75,
            energy_cost=0.3,
            execution_time=0.1
        )
    
    def _calculate_redirect_direction(self, threat: ThreatAssessment) -> str:
        """计算引化方向"""
        if threat.direction == 'strong':
            return 'weak'
        elif threat.direction == 'up':
            return 'down'
        return 'neutral'
    
    def _select_posture(self, threat: ThreatAssessment) -> str:
        """选择姿态"""
        if threat.threat_type in ['入侵威胁', '恶意攻击']:
            return 'tiger'
        elif threat.threat_type in ['拒绝服务']:
            return 'bear'
        elif threat.threat_type in ['数据泄露']:
            return 'ape'
        return 'deer'
    
    def execute_defense(
        self,
        threat: ThreatAssessment
    ) -> DefenseState:
        """执行防御"""
        strategies = self.select_defense_strategy(threat)
        
        total_effectiveness = sum(s.effectiveness for s in strategies) / len(strategies)
        total_energy = sum(s.energy_cost for s in strategies)
        
        stability = 1.0 - (threat.intensity * 0.3)
        
        self.defense_actions.extend(strategies)
        self.defense_effectiveness_history.append(total_effectiveness)
        
        self._update_yin_yang_balance(threat, strategies)
        
        return DefenseState(
            threat_level=threat.threat_level,
            active_defenses=[s.defense_type for s in strategies],
            energy_allocated=total_energy,
            stability_score=stability,
            defense_effectiveness=total_effectiveness
        )
    
    def _update_yin_yang_balance(
        self,
        threat: ThreatAssessment,
        strategies: List[DefenseAction]
    ) -> None:
        """更新阴阳平衡"""
        if threat.intensity > 0.7:
            self.yin_yang_balance += 0.1
        else:
            self.yin_yang_balance -= 0.05
        
        self.yin_yang_balance = max(-1.0, min(1.0, self.yin_yang_balance))
    
    def evaluate_defense_effectiveness(self) -> float:
        """评估防御有效性"""
        if not self.defense_effectiveness_history:
            return 0.5
        
        recent = self.defense_effectiveness_history[-10:]
        return sum(recent) / len(recent)
    
    def predict_next_threat(self) -> Dict[str, Any]:
        """预测下一个威胁"""
        if len(self.threat_history) < 5:
            return {'prediction': 'insufficient_data'}
        
        recent_threats = self.threat_history[-5:]
        avg_intensity = sum(t.intensity for t in recent_threats) / len(recent_threats)
        trend = 'increasing' if recent_threats[-1].intensity > avg_intensity else 'decreasing'
        
        return {
            'predicted_intensity': avg_intensity,
            'trend': trend,
            'most_likely_type': self._predict_threat_type(),
            'recommended_readiness': 'high' if avg_intensity > 0.6 else 'normal'
        }
    
    def _predict_threat_type(self) -> str:
        """预测威胁类型"""
        if not self.threat_history:
            return 'unknown'
        
        recent_types = [t.threat_type for t in self.threat_history[-5:]]
        return max(set(recent_types), key=recent_types.count)
    
    def get_defense_state(self) -> Dict[str, Any]:
        """获取防御状态"""
        return {
            'yin_yang_balance': self.yin_yang_balance,
            'threat_history_length': len(self.threat_history),
            'defense_actions_count': len(self.defense_actions),
            'average_effectiveness': self.evaluate_defense_effectiveness(),
            'active_threat_level': self.threat_history[-1].threat_level if self.threat_history else ThreatLevel.NORMAL,
            'stability_score': self._calculate_stability()
        }
    
    def _calculate_stability(self) -> float:
        """计算稳定性"""
        if len(self.defense_effectiveness_history) < 3:
            return 1.0
        
        recent = self.defense_effectiveness_history[-5:]
        variance = sum((e - sum(recent)/len(recent))**2 for e in recent) / len(recent)
        return max(0.0, 1.0 - variance)
