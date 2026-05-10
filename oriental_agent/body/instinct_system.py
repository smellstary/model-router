"""
Human Instinct Classification System - 人类本能分类体系

Integrates Maslow's hierarchy with Eastern wisdom (五行/阴阳) principles:
- 6-tier instinct hierarchy from survival to transcendence
- Maps instincts to Five Elements and Yin-Yang dynamics
- Provides instinct-driven behavior generation
"""

from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import math


class InstinctLevel(Enum):
    """本能层级枚举 - Instinct Level Enumeration"""
    LEVEL_1_SELF_PRESERVATION = 1
    LEVEL_2_BASIC_NEEDS = 2
    LEVEL_3_ATTACHMENT = 3
    LEVEL_4_COGNITION = 4
    LEVEL_5_REPRODUCTION = 5
    LEVEL_6_TRANSCENDENCE = 6


@dataclass
class InstinctCategory:
    """本能类别 - Instinct Category"""
    name: str
    instinct_type: str
    urgency: float
    threshold: float
    associated_wuxing: str
    yin_yang_nature: str


@dataclass
class DriveState:
    """驱力状态 - Drive State"""
    drive_name: str
    current_level: float
    threshold: float
    urgency: float
    last_activated: datetime
    activation_count: int = 0
    habituation_level: float = 0.0
    sensitization_level: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "drive_name": self.drive_name,
            "current_level": self.current_level,
            "threshold": self.threshold,
            "urgency": self.urgency,
            "last_activated": self.last_activated.isoformat(),
            "activation_count": self.activation_count,
            "habituation_level": self.habituation_level,
            "sensitization_level": self.sensitization_level
        }


@dataclass
class InstinctSignal:
    """本能信号 - Instinct Signal"""
    signal_id: str
    instinct_level: InstinctLevel
    signal_type: str
    intensity: float
    source: str
    timestamp: datetime
    associated_drives: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "signal_id": self.signal_id,
            "instinct_level": self.instinct_level.value,
            "signal_type": self.signal_type,
            "intensity": self.intensity,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "associated_drives": self.associated_drives,
            "metadata": self.metadata
        }


class InstinctTaxonomy:
    """本能分类体系 - Instinct Taxonomy"""
    
    INSTINCT_HIERARCHY = {
        InstinctLevel.LEVEL_1_SELF_PRESERVATION: {
            "name": "自我保存",
            "description": "内稳态维持、趋痛避害",
            "drives": ["self_preservation", "pain_avoidance", "homeostasis"],
            "wuxing": "水",
            "yin_yang": "阴"
        },
        InstinctLevel.LEVEL_2_BASIC_NEEDS: {
            "name": "基本需求",
            "description": "饥渴、栖身、睡眠",
            "drives": ["hunger", "thirst", "shelter", "sleep"],
            "wuxing": "土",
            "yin_yang": "阴"
        },
        InstinctLevel.LEVEL_3_ATTACHMENT: {
            "name": "依恋归属",
            "description": "依恋、归属、位阶、互惠",
            "drives": ["attachment", "belonging", "hierarchy", "reciprocity"],
            "wuxing": "木",
            "yin_yang": "阳"
        },
        InstinctLevel.LEVEL_4_COGNITION: {
            "name": "认知探索",
            "description": "好奇、模式识别、因果推理",
            "drives": ["curiosity", "pattern_recognition", "causal_reasoning"],
            "wuxing": "火",
            "yin_yang": "阳"
        },
        InstinctLevel.LEVEL_5_REPRODUCTION: {
            "name": "繁衍传承",
            "description": "求偶、亲代抚育、传承",
            "drives": ["mating", "parenting", "legacy"],
            "wuxing": "金",
            "yin_yang": "阳"
        },
        InstinctLevel.LEVEL_6_TRANSCENDENCE: {
            "name": "超越意义",
            "description": "审美、意义追寻、超越",
            "drives": ["aesthetics", "meaning_seeking", "transcendence"],
            "wuxing": "火",
            "yin_yang": "阳"
        }
    }
    
    WUXING_INSTINCT_MAP = {
        "水": [InstinctLevel.LEVEL_1_SELF_PRESERVATION],
        "土": [InstinctLevel.LEVEL_2_BASIC_NEEDS],
        "木": [InstinctLevel.LEVEL_3_ATTACHMENT],
        "火": [InstinctLevel.LEVEL_4_COGNITION, InstinctLevel.LEVEL_6_TRANSCENDENCE],
        "金": [InstinctLevel.LEVEL_5_REPRODUCTION]
    }
    
    def get_instinct_by_level(self, level: InstinctLevel) -> Dict:
        return self.INSTINCT_HIERARCHY.get(level, {})
    
    def get_instinct_drives(self, level: InstinctLevel) -> List[str]:
        return self.INSTINCT_HIERARCHY.get(level, {}).get("drives", [])
    
    def get_wuxing_instincts(self, wuxing: str) -> List[InstinctLevel]:
        return self.WUXING_INSTINCT_MAP.get(wuxing, [])
    
    def get_yin_yang_instincts(self, yin_yang: str) -> List[InstinctLevel]:
        return [
            level for level, info in self.INSTINCT_HIERARCHY.items()
            if info.get("yin_yang") == yin_yang
        ]


class DriveIntegration:
    """驱力整合模块 - Drive Integration Module"""
    
    def __init__(self):
        self.drives: Dict[str, DriveState] = {}
        self._initialize_drives()
    
    def _initialize_drives(self) -> None:
        drive_configs = [
            ("self_preservation", 0.8, 0.3),
            ("pain_avoidance", 0.7, 0.4),
            ("homeostasis", 0.9, 0.2),
            ("hunger", 0.5, 0.5),
            ("thirst", 0.5, 0.5),
            ("shelter", 0.6, 0.4),
            ("sleep", 0.4, 0.5),
            ("attachment", 0.6, 0.4),
            ("belonging", 0.5, 0.5),
            ("hierarchy", 0.4, 0.6),
            ("reciprocity", 0.5, 0.5),
            ("curiosity", 0.6, 0.4),
            ("pattern_recognition", 0.7, 0.3),
            ("causal_reasoning", 0.6, 0.4),
            ("mating", 0.3, 0.6),
            ("parenting", 0.4, 0.5),
            ("legacy", 0.5, 0.4),
            ("aesthetics", 0.4, 0.5),
            ("meaning_seeking", 0.5, 0.4),
            ("transcendence", 0.3, 0.6)
        ]
        
        for name, level, threshold in drive_configs:
            self.drives[name] = DriveState(
                drive_name=name,
                current_level=level,
                threshold=threshold,
                urgency=0.0,
                last_activated=datetime.now()
            )
    
    def update_drive(self, drive_name: str, delta: float) -> bool:
        if drive_name not in self.drives:
            return False
        
        drive = self.drives[drive_name]
        drive.current_level = max(0.0, min(1.0, drive.current_level + delta))
        drive.urgency = self._calculate_urgency(drive)
        return True
    
    def _calculate_urgency(self, drive: DriveState) -> float:
        deficit = max(0.0, drive.threshold - drive.current_level)
        return min(1.0, deficit * (1.0 - drive.habituation_level))
    
    def apply_habituation(self, drive_name: str, amount: float = 0.1) -> None:
        if drive_name in self.drives:
            self.drives[drive_name].habituation_level = min(
                1.0, self.drives[drive_name].habituation_level + amount
            )
    
    def apply_sensitization(self, drive_name: str, amount: float = 0.2) -> None:
        if drive_name in self.drives:
            self.drives[drive_name].sensitization_level = min(
                1.0, self.drives[drive_name].sensitization_level + amount
            )
    
    def trigger_drive(self, drive_name: str) -> bool:
        if drive_name not in self.drives:
            return False
        
        drive = self.drives[drive_name]
        drive.activation_count += 1
        drive.last_activated = datetime.now()
        drive.urgency = self._calculate_urgency(drive)
        return True
    
    def get_dominant_drive(self) -> Tuple[Optional[str], float]:
        if not self.drives:
            return None, 0.0
        
        dominant = max(self.drives.items(), key=lambda x: x[1].urgency)
        return dominant[0], dominant[1].urgency
    
    def get_all_drives(self) -> Dict[str, DriveState]:
        return self.drives.copy()


class InstinctEngine:
    """本能引擎 - Instinct Engine
    
    Core processing unit that handles:
    - Fast path: stimulus evaluation and signal generation
    - Drive integration: homeostasis and threshold triggering
    - Learning: habituation and sensitization
    """
    
    def __init__(self):
        self.taxonomy = InstinctTaxonomy()
        self.drive_integration = DriveIntegration()
        self.active_signals: List[InstinctSignal] = []
        self.signal_history: List[InstinctSignal] = []
        self.processing_mode = "parallel"
    
    def evaluate_stimulus(
        self,
        stimulus: Dict[str, Any]
    ) -> List[InstinctSignal]:
        signals = []
        
        stimulus_type = stimulus.get("type", "unknown")
        intensity = stimulus.get("intensity", 0.5)
        source = stimulus.get("source", "unknown")
        
        mapped_drives = self._map_stimulus_to_drives(stimulus_type)
        
        for drive_name in mapped_drives:
            for level in InstinctLevel:
                if drive_name in self.taxonomy.get_instinct_drives(level):
                    signal = InstinctSignal(
                        signal_id=f"sig_{len(self.active_signals)}",
                        instinct_level=level,
                        signal_type=stimulus_type,
                        intensity=intensity,
                        source=source,
                        timestamp=datetime.now(),
                        associated_drives=[drive_name]
                    )
                    signals.append(signal)
                    self.active_signals.append(signal)
                    break
        
        return signals
    
    def _map_stimulus_to_drives(self, stimulus_type: str) -> List[str]:
        mapping = {
            "threat": ["self_preservation", "pain_avoidance"],
            "hunger_signal": ["hunger"],
            "thirst_signal": ["thirst"],
            "cold": ["shelter"],
            "fatigue": ["sleep"],
            "social_isolation": ["attachment", "belonging"],
            "status_threat": ["hierarchy"],
            "novelty": ["curiosity", "pattern_recognition"],
            "unknown": ["curiosity", "causal_reasoning"],
            "potential_mate": ["mating"],
            "offspring": ["parenting"],
            "beauty": ["aesthetics"],
            "existential": ["meaning_seeking", "transcendence"]
        }
        return mapping.get(stimulus_type, ["curiosity"])
    
    def integrate_drives(self) -> Tuple[str, float, List[str]]:
        dominant_drive, urgency = self.drive_integration.get_dominant_drive()
        
        if dominant_drive is None:
            return "none", 0.0, []
        
        triggered_levels = []
        for level in InstinctLevel:
            if dominant_drive in self.taxonomy.get_instinct_drives(level):
                triggered_levels.append(level)
                break
        
        return dominant_drive, urgency, [lv.name for lv in triggered_levels]
    
    def apply_learning(
        self,
        behavior_result: Dict[str, Any]
    ) -> None:
        drive_name = behavior_result.get("drive_name")
        success = behavior_result.get("success", False)
        trauma = behavior_result.get("trauma", False)
        
        if drive_name:
            if success and behavior_result.get("repeated", False):
                self.drive_integration.apply_habituation(drive_name)
            elif trauma:
                self.drive_integration.apply_sensitization(drive_name)
    
    def process_homeostasis(self, delta_time: float) -> Dict[str, float]:
        changes = {}
        
        for drive_name, drive in self.drive_integration.drives.items():
            decay = 0.01 * delta_time
            drive.current_level = max(0.0, drive.current_level - decay)
            drive.urgency = self.drive_integration._calculate_urgency(drive)
            changes[drive_name] = drive.current_level
        
        return changes
    
    def get_system_state(self) -> Dict[str, Any]:
        return {
            "active_signals": len(self.active_signals),
            "dominant_drive": self.drive_integration.get_dominant_drive()[0],
            "drive_states": {
                name: state.to_dict() 
                for name, state in self.drive_integration.drives.items()
            }
        }


class BehaviorMode(Enum):
    """行为模式枚举"""
    FIGHT = "战"
    FLEE = "逃"
    FREEZE = "僵"
    HIDE = "藏"
    EAT = "食"
    DRINK = "水"
    SHELTER = "巢"
    SLEEP = "眠"
    APPROACH = "近"
    RETREAT = "退"
    SUBMIT = "服"
    DOMINATE = "主"
    GROOM = "理"
    ENJOY = "享"
    COOPERATE = "合"
    EXPLORE = "探"
    INVESTIGATE = "查"
    OBSERVE = "观"
    PLAY = "玩"
    COURT = "偶"
    NURTURE = "育"
    TEACH = "教"
    CREATE = "创"
    MEDITATE = "思"
    INTEGRATE = "融"


class BehaviorMapper:
    """行为映射器 - Behavior Mapper
    
    Maps instinct signals to concrete behaviors:
    Signal matching → Candidate behaviors → Conflict resolution → Threshold filtering → Execution
    """
    
    BEHAVIOR_INSTINCT_MAP = {
        BehaviorMode.FIGHT: ["self_preservation", "hierarchy"],
        BehaviorMode.FLEE: ["self_preservation", "pain_avoidance"],
        BehaviorMode.FREEZE: ["self_preservation"],
        BehaviorMode.HIDE: ["self_preservation", "pain_avoidance"],
        BehaviorMode.EAT: ["hunger"],
        BehaviorMode.DRINK: ["thirst"],
        BehaviorMode.SHELTER: ["shelter"],
        BehaviorMode.SLEEP: ["sleep"],
        BehaviorMode.APPROACH: ["attachment", "belonging"],
        BehaviorMode.RETREAT: ["attachment"],
        BehaviorMode.SUBMIT: ["hierarchy"],
        BehaviorMode.DOMINATE: ["hierarchy"],
        BehaviorMode.GROOM: ["attachment", "reciprocity"],
        BehaviorMode.ENJOY: ["aesthetics"],
        BehaviorMode.COOPERATE: ["reciprocity", "belonging"],
        BehaviorMode.EXPLORE: ["curiosity"],
        BehaviorMode.INVESTIGATE: ["curiosity", "pattern_recognition"],
        BehaviorMode.OBSERVE: ["pattern_recognition"],
        BehaviorMode.PLAY: ["curiosity", "attachment"],
        BehaviorMode.COURT: ["mating"],
        BehaviorMode.NURTURE: ["parenting"],
        BehaviorMode.TEACH: ["legacy", "parenting"],
        BehaviorMode.CREATE: ["transcendence", "meaning_seeking"],
        BehaviorMode.MEDITATE: ["meaning_seeking", "transcendence"],
        BehaviorMode.INTEGRATE: ["transcendence", "causal_reasoning"]
    }
    
    def __init__(self):
        self.behavior_threshold = 0.3
        self.conflict_strategy = "priority"
    
    def map_signals_to_behaviors(
        self,
        signals: List[InstinctSignal],
        drive_states: Dict[str, DriveState],
        context: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[BehaviorMode, float]]:
        candidates = []
        
        for signal in signals:
            for drive in signal.associated_drives:
                if drive in drive_states:
                    for behavior, required_drives in self.BEHAVIOR_INSTINCT_MAP.items():
                        if drive in required_drives:
                            urgency = drive_states[drive].urgency * signal.intensity
                            candidates.append((behavior, urgency))
        
        if context:
            candidates = self._apply_context_filter(candidates, context)
        
        candidates = self._resolve_conflicts(candidates)
        candidates = self._apply_threshold_filter(candidates)
        
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:5]
    
    def _apply_context_filter(
        self,
        candidates: List[Tuple[BehaviorMode, float]],
        context: Dict[str, Any]
    ) -> List[Tuple[BehaviorMode, float]]:
        available = context.get("available_behaviors", list(BehaviorMode))
        energy = context.get("available_energy", 1.0)
        
        filtered = [
            (b, u) for b, u in candidates 
            if b in available and u <= energy
        ]
        
        return filtered if filtered else candidates
    
    def _resolve_conflicts(
        self,
        candidates: List[Tuple[BehaviorMode, float]]
    ) -> List[Tuple[BehaviorMode, float]]:
        behavior_scores: Dict[BehaviorMode, float] = {}
        
        for behavior, urgency in candidates:
            if behavior not in behavior_scores:
                behavior_scores[behavior] = 0.0
            behavior_scores[behavior] += urgency
        
        return list(behavior_scores.items())
    
    def _apply_threshold_filter(
        self,
        candidates: List[Tuple[BehaviorMode, float]]
    ) -> List[Tuple[BehaviorMode, float]]:
        return [
            (b, u) for b, u in candidates 
            if u >= self.behavior_threshold
        ]
    
    def execute_behavior(
        self,
        behavior: BehaviorMode
    ) -> Dict[str, Any]:
        return {
            "behavior": behavior.value,
            "timestamp": datetime.now().isoformat(),
            "status": "executed",
            "energy_cost": self._estimate_energy_cost(behavior),
            "duration": self._estimate_duration(behavior)
        }
    
    def _estimate_energy_cost(self, behavior: BehaviorMode) -> float:
        high_cost = {BehaviorMode.FIGHT, BehaviorMode.FLEE, BehaviorMode.CREATE}
        medium_cost = {BehaviorMode.EXPLORE, BehaviorMode.INVESTIGATE, BehaviorMode.HUNT} if hasattr(BehaviorMode, 'HUNT') else {BehaviorMode.EXPLORE, BehaviorMode.INVESTIGATE}
        
        if behavior in high_cost:
            return 0.3
        elif behavior in medium_cost:
            return 0.2
        else:
            return 0.1
    
    def _estimate_duration(self, behavior: BehaviorMode) -> float:
        sustained = {BehaviorMode.SLEEP, BehaviorMode.MEDITATE, BehaviorMode.CREATE}
        
        if behavior in sustained:
            return 60.0
        else:
            return 5.0


class InstinctSystem:
    """本能系统主类 - Instinct System Main Class
    
    Integrates InstinctEngine and BehaviorMapper with the Eastern wisdom framework.
    """
    
    def __init__(self):
        self.instinct_engine = InstinctEngine()
        self.behavior_mapper = BehaviorMapper()
        self.taxonomy = InstinctTaxonomy()
        self.feedback_buffer: List[Dict] = []
        self.learning_enabled = True
    
    def process_stimulus(
        self,
        stimulus: Dict[str, Any],
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        signals = self.instinct_engine.evaluate_stimulus(stimulus)
        
        dominant_drive, urgency, levels = self.instinct_engine.integrate_drives()
        
        behaviors = self.behavior_mapper.map_signals_to_behaviors(
            signals,
            self.instinct_engine.drive_integration.drives,
            context
        )
        
        return {
            "signals": [s.to_dict() for s in signals],
            "dominant_drive": dominant_drive,
            "urgency": urgency,
            "instinct_levels": levels,
            "candidate_behaviors": [(b.value, u) for b, u in behaviors]
        }
    
    def execute_behavior(
        self,
        behavior: BehaviorMode
    ) -> Dict[str, Any]:
        result = self.behavior_mapper.execute_behavior(behavior)
        
        self.feedback_buffer.append({
            "behavior": behavior.value,
            "result": result,
            "timestamp": datetime.now()
        })
        
        if len(self.feedback_buffer) > 100:
            self.feedback_buffer = self.feedback_buffer[-100:]
        
        return result
    
    def receive_feedback(
        self,
        behavior_result: Dict[str, Any]
    ) -> None:
        if self.learning_enabled:
            self.instinct_engine.apply_learning(behavior_result)
    
    def update_homeostasis(self, delta_time: float) -> Dict[str, float]:
        return self.instinct_engine.process_homeostasis(delta_time)
    
    def get_system_state(self) -> Dict[str, Any]:
        return {
            "engine_state": self.instinct_engine.get_system_state(),
            "behavior_threshold": self.behavior_mapper.behavior_threshold,
            "feedback_buffer_size": len(self.feedback_buffer),
            "learning_enabled": self.learning_enabled
        }
    
    def map_wuxing_influence(
        self,
        wuxing: str,
        influence_strength: float
    ) -> Dict[str, Any]:
        affected_levels = self.taxonomy.get_wuxing_instincts(wuxing)
        
        effects = []
        for level in affected_levels:
            drives = self.taxonomy.get_instinct_drives(level)
            for drive in drives:
                self.instinct_engine.drive_integration.update_drive(
                    drive, influence_strength * 0.1
                )
            effects.append(level.name)
        
        return {
            "wuxing": wuxing,
            "affected_levels": effects,
            "influence_applied": influence_strength
        }
    
    def map_yinyang_balance(
        self,
        balance_ratio: float
    ) -> Dict[str, Any]:
        yin_levels = self.taxonomy.get_yin_yang_instincts("阴")
        yang_levels = self.taxonomy.get_yin_yang_instincts("阳")
        
        for level in yin_levels:
            drives = self.taxonomy.get_instinct_drives(level)
            for drive in drives:
                self.instinct_engine.drive_integration.update_drive(
                    drive, balance_ratio * 0.05
                )
        
        for level in yang_levels:
            drives = self.taxonomy.get_instinct_drives(level)
            for drive in drives:
                self.instinct_engine.drive_integration.update_drive(
                    drive, (1 - balance_ratio) * 0.05
                )
        
        return {
            "balance_ratio": balance_ratio,
            "yin_levels_activated": [l.name for l in yin_levels],
            "yang_levels_activated": [l.name for l in yang_levels]
        }
