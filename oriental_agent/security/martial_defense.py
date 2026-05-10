"""
Martial Arts Defense System Module
武学防御体系模块

基于中国传统武学思想，设计三种防御策略：
- 太极（以柔克刚）
- 易筋经（强筋健骨）
- 五禽戏（模仿自然）
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime
import math
import random


class ThreatType(Enum):
    """威胁类型"""
    BRUTE_FORCE = "暴力攻击"
    STEALTH = "隐蔽渗透"
    PERSISTENT = "持续威胁"
    ADAPTIVE = "自适应攻击"
    COMPLEX = "复合威胁"
    UNKNOWN = "未知威胁"


class AttackIntensity(Enum):
    """攻击强度"""
    WEAK = 0.2
    MODERATE = 0.5
    STRONG = 0.75
    OVERWHELMING = 0.95


class AnimalForm(Enum):
    """五禽戏动物形态"""
    TIGER = "虎"
    DEER = "鹿"
    BEAR = "熊"
    MONKEY = "猿"
    BIRD = "鸟"


@dataclass
class Attack:
    """攻击数据结构"""
    attack_id: str
    attack_type: ThreatType
    intensity: float
    direction: str
    source: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThreatAnalysis:
    """威胁分析结果"""
    threat_type: ThreatType
    intensity_level: str
    vulnerability_points: List[str]
    recommended_strategy: str
    confidence: float
    analysis_timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DefenseResult:
    """防御结果"""
    success: bool
    damage_mitigated: float
    energy_consumed: float
    counter_attack_potential: float
    strategy_used: str
    details: Dict[str, Any] = field(default_factory=dict)


class DefenseStrategy(ABC):
    """防御策略基类"""
    
    def __init__(
        self,
        name: str,
        philosophy: str,
        defense_power: float,
        adaptability: float
    ):
        self.name = name
        self.philosophy = philosophy
        self.defense_power = max(0.0, min(1.0, defense_power))
        self.adaptability = max(0.0, min(1.0, adaptability))
        self._effectiveness_history: List[float] = []
    
    @abstractmethod
    def execute(self, attack: Attack) -> DefenseResult:
        """执行防御"""
        pass
    
    @abstractmethod
    def get_characteristics(self) -> Dict[str, Any]:
        """获取策略特征"""
        pass
    
    def record_effectiveness(self, effectiveness: float) -> None:
        """记录防御效果"""
        self._effectiveness_history.append(
            max(0.0, min(1.0, effectiveness))
        )
    
    def get_average_effectiveness(self) -> float:
        """获取平均防御效果"""
        if not self._effectiveness_history:
            return 0.5
        return sum(self._effectiveness_history) / len(self._effectiveness_history)
    
    def calculate_overall_score(self) -> float:
        """计算综合评分"""
        return (self.defense_power * 0.6 + self.adaptability * 0.4)


class TaijiDefense(DefenseStrategy):
    """太极防御 - 以柔克刚"""
    
    def __init__(self):
        super().__init__(
            name="太极防御",
            philosophy="以柔克刚，借力打力，四两拨千斤",
            defense_power=0.6,
            adaptability=0.95
        )
        self.circular_defense_radius: float = 1.0
        self.yield_threshold: float = 0.3
        self._redirect_angle: float = 45.0
        self._qi_flow_state: float = 0.5
    
    def yield_and_redirect(self, attack: Attack) -> Tuple[float, str]:
        """借力打力 - 将攻击能量化解、转移"""
        if attack.intensity < self.yield_threshold:
            redirect_ratio = 0.9
            message = "顺势化解，完全引导"
        elif attack.intensity < 0.6:
            redirect_ratio = 0.7
            message = "部分引导，化整为零"
        else:
            redirect_ratio = 0.4
            message = "强力化解，消耗较大"
        
        self._qi_flow_state = max(0.1, self._qi_flow_state - attack.intensity * 0.1)
        
        return redirect_ratio, message
    
    def _circular_defense(self, attack: Attack) -> Dict[str, Any]:
        """圆形防御圈"""
        angle = self._calculate_deflection_angle(attack)
        radius = self.circular_defense_radius * (1.0 + attack.intensity * 0.5)
        
        return {
            "defense_type": "圆形防御",
            "deflection_angle": angle,
            "defense_radius": radius,
            "energy_dissipation": self._calculate_energy_dissipation(attack)
        }
    
    def _calculate_deflection_angle(self, attack: Attack) -> float:
        """计算偏转角度"""
        base_angle = self._redirect_angle
        intensity_factor = 1.0 + attack.intensity
        return base_angle * intensity_factor
    
    def _calculate_energy_dissipation(self, attack: Attack) -> float:
        """计算能量耗散"""
        return attack.intensity * self.adaptability * 0.8
    
    def execute(self, attack: Attack) -> DefenseResult:
        """执行太极防御"""
        redirect_ratio, message = self.yield_and_redirect(attack)
        circular_info = self._circular_defense(attack)
        
        damage_mitigated = attack.intensity * redirect_ratio * self.adaptability
        energy_consumed = attack.intensity * (1 - redirect_ratio) * 0.5
        
        counter_potential = redirect_ratio * self._qi_flow_state
        
        effectiveness = damage_mitigated / max(attack.intensity, 0.01)
        self.record_effectiveness(effectiveness)
        
        return DefenseResult(
            success=redirect_ratio > 0.3,
            damage_mitigated=damage_mitigated,
            energy_consumed=energy_consumed,
            counter_attack_potential=counter_potential,
            strategy_used=self.name,
            details={
                "redirect_ratio": redirect_ratio,
                "message": message,
                "circular_defense": circular_info,
                "qi_flow_state": self._qi_flow_state
            }
        )
    
    def get_characteristics(self) -> Dict[str, Any]:
        """获取太极防御特征"""
        return {
            "name": self.name,
            "philosophy": self.philosophy,
            "defense_power": self.defense_power,
            "adaptability": self.adaptability,
            "circular_defense_radius": self.circular_defense_radius,
            "yield_threshold": self.yield_threshold,
            "qi_flow_state": self._qi_flow_state,
            "average_effectiveness": self.get_average_effectiveness()
        }
    
    def restore_qi(self, amount: float = 0.1) -> None:
        """恢复气机"""
        self._qi_flow_state = min(1.0, self._qi_flow_state + amount)


class YijinjingDefense(DefenseStrategy):
    """易筋经防御 - 强筋健骨"""
    
    def __init__(self):
        super().__init__(
            name="易筋经防御",
            philosophy="强筋健骨，易筋洗髓，固本培元",
            defense_power=0.95,
            adaptability=0.5
        )
        self._core_strength: float = 0.5
        self._bone_density: float = 0.5
        self._muscle_tension: float = 0.3
        self._transformation_efficiency: float = 0.6
    
    def strengthen_core(self, intensity: float = 0.1) -> Dict[str, float]:
        """强化核心"""
        self._core_strength = min(1.0, self._core_strength + intensity * 0.5)
        self._bone_density = min(1.0, self._bone_density + intensity * 0.3)
        self._muscle_tension = min(1.0, self._muscle_tension + intensity * 0.2)
        
        return {
            "core_strength": self._core_strength,
            "bone_density": self._bone_density,
            "muscle_tension": self._muscle_tension
        }
    
    def absorb_and_transform(self, attack: Attack) -> Tuple[float, float]:
        """吸收转化攻击"""
        absorption_rate = self._core_strength * self.defense_power
        
        absorbed_energy = attack.intensity * absorption_rate
        transformed_energy = absorbed_energy * self._transformation_efficiency
        
        self._core_strength = max(0.3, self._core_strength - attack.intensity * 0.05)
        
        return absorbed_energy, transformed_energy
    
    def _calculate_resistance(self, attack: Attack) -> float:
        """计算抵抗力"""
        base_resistance = self.defense_power * self._core_strength
        bone_factor = self._bone_density * 0.3
        muscle_factor = self._muscle_tension * 0.2
        
        return base_resistance + bone_factor + muscle_factor
    
    def execute(self, attack: Attack) -> DefenseResult:
        """执行易筋经防御"""
        resistance = self._calculate_resistance(attack)
        absorbed, transformed = self.absorb_and_transform(attack)
        
        damage_mitigated = attack.intensity * resistance
        energy_consumed = attack.intensity * (1 - resistance) * 0.3
        
        counter_potential = transformed * 0.5
        
        effectiveness = damage_mitigated / max(attack.intensity, 0.01)
        self.record_effectiveness(effectiveness)
        
        self.strengthen_core(transformed * 0.1)
        
        return DefenseResult(
            success=resistance > 0.5,
            damage_mitigated=damage_mitigated,
            energy_consumed=energy_consumed,
            counter_attack_potential=counter_potential,
            strategy_used=self.name,
            details={
                "resistance": resistance,
                "absorbed_energy": absorbed,
                "transformed_energy": transformed,
                "core_strength": self._core_strength,
                "bone_density": self._bone_density,
                "muscle_tension": self._muscle_tension
            }
        )
    
    def get_characteristics(self) -> Dict[str, Any]:
        """获取易筋经防御特征"""
        return {
            "name": self.name,
            "philosophy": self.philosophy,
            "defense_power": self.defense_power,
            "adaptability": self.adaptability,
            "core_strength": self._core_strength,
            "bone_density": self._bone_density,
            "muscle_tension": self._muscle_tension,
            "transformation_efficiency": self._transformation_efficiency,
            "average_effectiveness": self.get_average_effectiveness()
        }
    
    def meditate(self, duration: float = 1.0) -> None:
        """冥想恢复"""
        recovery = duration * 0.1
        self._core_strength = min(1.0, self._core_strength + recovery)
        self._bone_density = min(1.0, self._bone_density + recovery * 0.5)
        self._muscle_tension = max(0.1, self._muscle_tension - recovery * 0.3)


class WuqinxiDefense(DefenseStrategy):
    """五禽戏防御 - 模仿自然"""
    
    FORM_CHARACTERISTICS = {
        AnimalForm.TIGER: {
            "power": 0.9,
            "agility": 0.5,
            "stealth": 0.3,
            "description": "虎形 - 威猛刚强，气势磅礴"
        },
        AnimalForm.DEER: {
            "power": 0.4,
            "agility": 0.9,
            "stealth": 0.6,
            "description": "鹿形 - 轻盈灵动，优雅从容"
        },
        AnimalForm.BEAR: {
            "power": 0.8,
            "agility": 0.3,
            "stealth": 0.2,
            "description": "熊形 - 沉稳厚重，力拔山兮"
        },
        AnimalForm.MONKEY: {
            "power": 0.5,
            "agility": 0.95,
            "stealth": 0.7,
            "description": "猿形 - 灵巧多变，机敏过人"
        },
        AnimalForm.BIRD: {
            "power": 0.3,
            "agility": 0.85,
            "stealth": 0.8,
            "description": "鸟形 - 轻盈飘逸，高瞻远瞩"
        }
    }
    
    def __init__(self):
        super().__init__(
            name="五禽戏防御",
            philosophy="模仿自然，五形合一，变化无穷",
            defense_power=0.75,
            adaptability=0.85
        )
        self._current_form: Optional[AnimalForm] = None
        self._form_history: List[AnimalForm] = []
        self._form_mastery: Dict[AnimalForm, float] = {
            form: 0.5 for form in AnimalForm
        }
    
    def tiger_form(self) -> Dict[str, Any]:
        """虎形 - 威猛"""
        self._current_form = AnimalForm.TIGER
        self._form_history.append(AnimalForm.TIGER)
        
        char = self.FORM_CHARACTERISTICS[AnimalForm.TIGER]
        mastery = self._form_mastery[AnimalForm.TIGER]
        
        return {
            "form": "虎形",
            "action": "猛虎下山",
            "power_multiplier": char["power"] * (1 + mastery * 0.5),
            "agility_multiplier": char["agility"],
            "special_ability": "虎啸震慑",
            "intimidation_factor": 0.8 * mastery
        }
    
    def deer_form(self) -> Dict[str, Any]:
        """鹿形 - 灵动"""
        self._current_form = AnimalForm.DEER
        self._form_history.append(AnimalForm.DEER)
        
        char = self.FORM_CHARACTERISTICS[AnimalForm.DEER]
        mastery = self._form_mastery[AnimalForm.DEER]
        
        return {
            "form": "鹿形",
            "action": "灵鹿跃涧",
            "power_multiplier": char["power"],
            "agility_multiplier": char["agility"] * (1 + mastery * 0.5),
            "special_ability": "鹿角格挡",
            "evasion_factor": 0.85 * mastery
        }
    
    def bear_form(self) -> Dict[str, Any]:
        """熊形 - 厚重"""
        self._current_form = AnimalForm.BEAR
        self._form_history.append(AnimalForm.BEAR)
        
        char = self.FORM_CHARACTERISTICS[AnimalForm.BEAR]
        mastery = self._form_mastery[AnimalForm.BEAR]
        
        return {
            "form": "熊形",
            "action": "黑熊蹭背",
            "power_multiplier": char["power"] * (1 + mastery * 0.5),
            "agility_multiplier": char["agility"],
            "special_ability": "熊抱固守",
            "endurance_factor": 0.9 * mastery
        }
    
    def monkey_form(self) -> Dict[str, Any]:
        """猿形 - 敏捷"""
        self._current_form = AnimalForm.MONKEY
        self._form_history.append(AnimalForm.MONKEY)
        
        char = self.FORM_CHARACTERISTICS[AnimalForm.MONKEY]
        mastery = self._form_mastery[AnimalForm.MONKEY]
        
        return {
            "form": "猿形",
            "action": "灵猿献果",
            "power_multiplier": char["power"],
            "agility_multiplier": char["agility"] * (1 + mastery * 0.5),
            "special_ability": "猿臂舒展",
            "trickery_factor": 0.75 * mastery
        }
    
    def bird_form(self) -> Dict[str, Any]:
        """鸟形 - 轻盈"""
        self._current_form = AnimalForm.BIRD
        self._form_history.append(AnimalForm.BIRD)
        
        char = self.FORM_CHARACTERISTICS[AnimalForm.BIRD]
        mastery = self._form_mastery[AnimalForm.BIRD]
        
        return {
            "form": "鸟形",
            "action": "鹤翔九天",
            "power_multiplier": char["power"],
            "agility_multiplier": char["agility"] * (1 + mastery * 0.5),
            "special_ability": "羽翼护身",
            "flight_factor": 0.8 * mastery
        }
    
    def _select_optimal_form(self, attack: Attack) -> AnimalForm:
        """选择最优形态"""
        if attack.intensity > 0.7:
            return AnimalForm.BEAR
        elif attack.intensity < 0.3:
            return AnimalForm.TIGER
        elif attack.attack_type == ThreatType.STEALTH:
            return AnimalForm.MONKEY
        elif attack.attack_type == ThreatType.ADAPTIVE:
            return AnimalForm.DEER
        elif attack.attack_type == ThreatType.COMPLEX:
            return AnimalForm.BIRD
        else:
            return random.choice(list(AnimalForm))
    
    def _transform_to_form(self, form: AnimalForm) -> Dict[str, Any]:
        """转换到指定形态"""
        form_methods = {
            AnimalForm.TIGER: self.tiger_form,
            AnimalForm.DEER: self.deer_form,
            AnimalForm.BEAR: self.bear_form,
            AnimalForm.MONKEY: self.monkey_form,
            AnimalForm.BIRD: self.bird_form
        }
        return form_methods[form]()
    
    def _calculate_form_effectiveness(
        self,
        form_info: Dict[str, Any],
        attack: Attack
    ) -> float:
        """计算形态效果"""
        power = form_info["power_multiplier"]
        agility = form_info["agility_multiplier"]
        
        if attack.intensity > 0.6:
            return power * 0.7 + agility * 0.3
        else:
            return power * 0.3 + agility * 0.7
    
    def execute(self, attack: Attack) -> DefenseResult:
        """执行五禽戏防御"""
        optimal_form = self._select_optimal_form(attack)
        form_info = self._transform_to_form(optimal_form)
        
        effectiveness = self._calculate_form_effectiveness(form_info, attack)
        
        damage_mitigated = attack.intensity * effectiveness * self.defense_power
        energy_consumed = attack.intensity * (1 - effectiveness) * 0.4
        
        counter_potential = form_info.get("power_multiplier", 0.5) * 0.3
        
        self._form_mastery[optimal_form] = min(
            1.0,
            self._form_mastery[optimal_form] + 0.01
        )
        
        self.record_effectiveness(effectiveness)
        
        return DefenseResult(
            success=effectiveness > 0.4,
            damage_mitigated=damage_mitigated,
            energy_consumed=energy_consumed,
            counter_attack_potential=counter_potential,
            strategy_used=f"{self.name} - {form_info['form']}",
            details={
                "current_form": form_info["form"],
                "form_action": form_info["action"],
                "special_ability": form_info["special_ability"],
                "effectiveness": effectiveness,
                "form_mastery": self._form_mastery[optimal_form]
            }
        )
    
    def get_characteristics(self) -> Dict[str, Any]:
        """获取五禽戏防御特征"""
        return {
            "name": self.name,
            "philosophy": self.philosophy,
            "defense_power": self.defense_power,
            "adaptability": self.adaptability,
            "current_form": self._current_form.value if self._current_form else None,
            "form_mastery": {k.value: v for k, v in self._form_mastery.items()},
            "form_history_count": len(self._form_history),
            "average_effectiveness": self.get_average_effectiveness()
        }
    
    def get_form_description(self, form: AnimalForm) -> str:
        """获取形态描述"""
        return self.FORM_CHARACTERISTICS[form]["description"]


class AdaptiveDefenseSelector:
    """自适应防御选择器"""
    
    STRATEGY_SCORES = {
        ThreatType.BRUTE_FORCE: {
            "taiji": 0.9,
            "yijinjing": 0.7,
            "wuqinxi": 0.5
        },
        ThreatType.STEALTH: {
            "taiji": 0.6,
            "yijinjing": 0.4,
            "wuqinxi": 0.85
        },
        ThreatType.PERSISTENT: {
            "taiji": 0.5,
            "yijinjing": 0.95,
            "wuqinxi": 0.6
        },
        ThreatType.ADAPTIVE: {
            "taiji": 0.7,
            "yijinjing": 0.5,
            "wuqinxi": 0.9
        },
        ThreatType.COMPLEX: {
            "taiji": 0.6,
            "yijinjing": 0.6,
            "wuqinxi": 0.85
        },
        ThreatType.UNKNOWN: {
            "taiji": 0.7,
            "yijinjing": 0.7,
            "wuqinxi": 0.7
        }
    }
    
    def __init__(self):
        self.taiji = TaijiDefense()
        self.yijinjing = YijinjingDefense()
        self.wuqinxi = WuqinxiDefense()
        
        self._current_strategy: Optional[DefenseStrategy] = None
        self._strategy_history: List[Dict[str, Any]] = []
        self._threat_history: List[ThreatAnalysis] = []
    
    def analyze_threat(self, threat: Attack) -> ThreatAnalysis:
        """分析威胁类型"""
        intensity_level = self._classify_intensity(threat.intensity)
        vulnerability_points = self._identify_vulnerabilities(threat)
        recommended = self._get_initial_recommendation(threat.attack_type)
        confidence = self._calculate_confidence(threat)
        
        analysis = ThreatAnalysis(
            threat_type=threat.attack_type,
            intensity_level=intensity_level,
            vulnerability_points=vulnerability_points,
            recommended_strategy=recommended,
            confidence=confidence
        )
        
        self._threat_history.append(analysis)
        return analysis
    
    def _classify_intensity(self, intensity: float) -> str:
        """分类强度等级"""
        if intensity < 0.25:
            return "微弱"
        elif intensity < 0.5:
            return "中等"
        elif intensity < 0.75:
            return "强烈"
        else:
            return "毁灭性"
    
    def _identify_vulnerabilities(self, threat: Attack) -> List[str]:
        """识别薄弱点"""
        vulnerabilities = []
        
        if threat.intensity > 0.7:
            vulnerabilities.append("高强度冲击点")
        if threat.attack_type == ThreatType.STEALTH:
            vulnerabilities.append("隐蔽渗透点")
        if threat.attack_type == ThreatType.ADAPTIVE:
            vulnerabilities.append("动态变化点")
        if threat.attack_type == ThreatType.COMPLEX:
            vulnerabilities.append("多重威胁点")
        
        return vulnerabilities if vulnerabilities else ["无明显薄弱点"]
    
    def _get_initial_recommendation(self, threat_type: ThreatType) -> str:
        """获取初始推荐"""
        scores = self.STRATEGY_SCORES.get(threat_type, self.STRATEGY_SCORES[ThreatType.UNKNOWN])
        best = max(scores, key=scores.get)
        
        strategy_names = {
            "taiji": "太极防御",
            "yijinjing": "易筋经防御",
            "wuqinxi": "五禽戏防御"
        }
        return strategy_names[best]
    
    def _calculate_confidence(self, threat: Attack) -> float:
        """计算分析置信度"""
        base_confidence = 0.7
        
        if len(self._threat_history) > 5:
            base_confidence += 0.1
        if threat.attack_type != ThreatType.UNKNOWN:
            base_confidence += 0.1
        if threat.metadata:
            base_confidence += 0.05
        
        return min(1.0, base_confidence)
    
    def select_strategy(
        self,
        threat_analysis: ThreatAnalysis
    ) -> DefenseStrategy:
        """选择最佳策略"""
        scores = self.STRATEGY_SCORES.get(
            threat_analysis.threat_type,
            self.STRATEGY_SCORES[ThreatType.UNKNOWN]
        )
        
        taiji_score = scores["taiji"] * self.taiji.get_average_effectiveness()
        yijinjing_score = scores["yijinjing"] * self.yijinjing.get_average_effectiveness()
        wuqinxi_score = scores["wuqinxi"] * self.wuqinxi.get_average_effectiveness()
        
        if taiji_score == yijinjing_score == wuqinxi_score == 0:
            taiji_score = scores["taiji"]
            yijinjing_score = scores["yijinjing"]
            wuqinxi_score = scores["wuqinxi"]
        
        max_score = max(taiji_score, yijinjing_score, wuqinxi_score)
        
        if max_score == taiji_score:
            selected = self.taiji
        elif max_score == yijinjing_score:
            selected = self.yijinjing
        else:
            selected = self.wuqinxi
        
        self._current_strategy = selected
        
        self._strategy_history.append({
            "threat_type": threat_analysis.threat_type.value,
            "selected_strategy": selected.name,
            "timestamp": datetime.now()
        })
        
        return selected
    
    def switch_strategy(
        self,
        reason: str = "performance_optimization"
    ) -> DefenseStrategy:
        """动态切换策略"""
        strategies = [self.taiji, self.yijinjing, self.wuqinxi]
        
        if self._current_strategy:
            strategies.remove(self._current_strategy)
        
        best = max(strategies, key=lambda s: s.get_average_effectiveness())
        
        if best.get_average_effectiveness() == 0:
            best = max(strategies, key=lambda s: s.calculate_overall_score())
        
        self._current_strategy = best
        
        self._strategy_history.append({
            "threat_type": "dynamic_switch",
            "selected_strategy": best.name,
            "reason": reason,
            "timestamp": datetime.now()
        })
        
        return best
    
    def execute_defense(self, attack: Attack) -> DefenseResult:
        """执行完整防御流程"""
        analysis = self.analyze_threat(attack)
        
        if not self._current_strategy:
            self.select_strategy(analysis)
        
        result = self._current_strategy.execute(attack)
        
        if not result.success and self._should_switch(result):
            self.switch_strategy("defense_failure")
            result = self._current_strategy.execute(attack)
        
        return result
    
    def _should_switch(self, result: DefenseResult) -> bool:
        """判断是否需要切换策略"""
        return result.damage_mitigated < 0.3
    
    def get_status(self) -> Dict[str, Any]:
        """获取当前状态"""
        return {
            "current_strategy": self._current_strategy.name if self._current_strategy else None,
            "strategy_history_count": len(self._strategy_history),
            "threat_history_count": len(self._threat_history),
            "taiji_effectiveness": self.taiji.get_average_effectiveness(),
            "yijinjing_effectiveness": self.yijinjing.get_average_effectiveness(),
            "wuqinxi_effectiveness": self.wuqinxi.get_average_effectiveness()
        }
    
    def get_all_characteristics(self) -> Dict[str, Dict[str, Any]]:
        """获取所有策略特征"""
        return {
            "taiji": self.taiji.get_characteristics(),
            "yijinjing": self.yijinjing.get_characteristics(),
            "wuqinxi": self.wuqinxi.get_characteristics()
        }
    
    def reset(self) -> None:
        """重置所有状态"""
        self._current_strategy = None
        self._strategy_history.clear()
        self._threat_history.clear()
        
        self.taiji = TaijiDefense()
        self.yijinjing = YijinjingDefense()
        self.wuqinxi = WuqinxiDefense()


def create_martial_defense_system() -> AdaptiveDefenseSelector:
    """创建武学防御系统"""
    return AdaptiveDefenseSelector()
