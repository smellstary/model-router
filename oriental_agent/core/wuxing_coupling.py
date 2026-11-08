"""
Wu Xing (Five Elements) Non-linear Coupling System
五行生克非线性耦合系统

Implements the generation (相生) and restriction (相克) cycles of the Five Elements,
creating a dynamic balance network where elements influence each other through
non-linear coupling relationships.

相生链条: 木→火→土→金→水→木
相克链条: 木→土→水→火→金→木
"""

from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
import math


class WuxingElement(Enum):
    """五行元素枚举 - Five Elements Enumeration"""
    WOOD = "木"
    FIRE = "火"
    EARTH = "土"
    METAL = "金"
    WATER = "水"


@dataclass
class WuxingModule:
    """五行模块数据结构 - Five Elements Module Data Structure"""
    element: WuxingElement
    activation_level: float = 0.5
    connected_modules: Dict[WuxingElement, float] = field(default_factory=dict)
    energy_reserve: float = 1.0
    stability: float = 1.0
    last_updated: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not 0.0 <= self.activation_level <= 1.0:
            raise ValueError(f"activation_level must be between 0 and 1, got {self.activation_level}")
    
    def update_activation(self, delta: float) -> float:
        new_level = max(0.0, min(1.0, self.activation_level + delta))
        self.activation_level = new_level
        self.last_updated = datetime.now()
        return new_level
    
    def add_connection(self, element: WuxingElement, weight: float = 1.0):
        self.connected_modules[element] = weight
        self.last_updated = datetime.now()
    
    def remove_connection(self, element: WuxingElement) -> bool:
        if element in self.connected_modules:
            del self.connected_modules[element]
            self.last_updated = datetime.now()
            return True
        return False
    
    def get_connection_weight(self, element: WuxingElement) -> float:
        return self.connected_modules.get(element, 0.0)
    
    def to_dict(self) -> Dict:
        return {
            "element": self.element.value,
            "activation_level": self.activation_level,
            "connected_modules": {e.value: w for e, w in self.connected_modules.items()},
            "energy_reserve": self.energy_reserve,
            "stability": self.stability,
            "last_updated": self.last_updated.isoformat()
        }


class WuxingCouplingNetwork:
    """五行耦合网络 - Five Elements Coupling Network"""
    
    GENERATION_CYCLE: Dict[WuxingElement, WuxingElement] = {
        WuxingElement.WOOD: WuxingElement.FIRE,
        WuxingElement.FIRE: WuxingElement.EARTH,
        WuxingElement.EARTH: WuxingElement.METAL,
        WuxingElement.METAL: WuxingElement.WATER,
        WuxingElement.WATER: WuxingElement.WOOD
    }
    
    RESTRICTION_CYCLE: Dict[WuxingElement, WuxingElement] = {
        WuxingElement.WOOD: WuxingElement.EARTH,
        WuxingElement.EARTH: WuxingElement.WATER,
        WuxingElement.WATER: WuxingElement.FIRE,
        WuxingElement.FIRE: WuxingElement.METAL,
        WuxingElement.METAL: WuxingElement.WOOD
    }
    
    GENERATION_GAIN_FACTOR = 0.25
    RESTRICTION_SUPPRESS_FACTOR = 0.20
    DECAY_FACTOR = 0.05
    BALANCE_THRESHOLD_HIGH = 0.75
    BALANCE_THRESHOLD_LOW = 0.35
    
    def __init__(self, nonlinearity_factor: float = 1.5):
        self.modules: Dict[WuxingElement, WuxingModule] = {}
        self.nonlinearity_factor = nonlinearity_factor
        self.propagation_history: List[Dict] = []
        self._initialize_network()
    
    def _initialize_network(self):
        for element in WuxingElement:
            self.modules[element] = WuxingModule(element=element)
        
        for element in WuxingElement:
            generated = self.GENERATION_CYCLE[element]
            restricted = self.RESTRICTION_CYCLE[element]
            
            self.modules[element].add_connection(generated, 1.0)
            self.modules[element].add_connection(restricted, -1.0)
    
    def add_module(self, module: WuxingModule) -> bool:
        if module.element in self.modules:
            return False
        self.modules[module.element] = module
        return True
    
    def get_module(self, element: WuxingElement) -> Optional[WuxingModule]:
        return self.modules.get(element)
    
    def activate(self, element: WuxingElement, intensity: float = 0.3) -> Dict[str, float]:
        if element not in self.modules:
            return {"error": f"Element {element.value} not found"}
        
        module = self.modules[element]
        module.update_activation(intensity)
        
        results = {
            "activated_element": element.value,
            "new_level": module.activation_level,
            "propagated": {}
        }
        
        generation_results = self.propagate_generation(element, intensity)
        restriction_results = self.propagate_restriction(element, intensity)
        
        results["propagated"]["generation"] = generation_results
        results["propagated"]["restriction"] = restriction_results
        
        self._record_propagation("activate", element, intensity, results)
        
        return results
    
    def propagate_generation(self, source: WuxingElement, intensity: float) -> Dict[str, float]:
        results = {}
        current_element = source
        current_intensity = intensity
        
        for step in range(5):
            target_element = self.GENERATION_CYCLE[current_element]
            
            if target_element not in self.modules:
                break
            
            target_module = self.modules[target_element]
            
            nonlinearity = self._compute_nonlinearity(current_intensity)
            gain = self.GENERATION_GAIN_FACTOR * current_intensity * nonlinearity
            
            old_level = target_module.activation_level
            new_level = target_module.update_activation(gain)
            
            results[f"{current_element.value}→{target_element.value}"] = {
                "gain": gain,
                "old_level": old_level,
                "new_level": new_level
            }
            
            current_element = target_element
            current_intensity = gain
        
        return results
    
    def propagate_restriction(self, source: WuxingElement, intensity: float) -> Dict[str, float]:
        results = {}
        current_element = source
        current_intensity = intensity
        
        for step in range(5):
            target_element = self.RESTRICTION_CYCLE[current_element]
            
            if target_element not in self.modules:
                break
            
            target_module = self.modules[target_element]
            
            nonlinearity = self._compute_nonlinearity(current_intensity)
            suppression = self.RESTRICTION_SUPPRESS_FACTOR * current_intensity * nonlinearity
            
            old_level = target_module.activation_level
            new_level = target_module.update_activation(-suppression)
            
            results[f"{current_element.value}⊃{target_element.value}"] = {
                "suppression": suppression,
                "old_level": old_level,
                "new_level": new_level
            }
            
            current_element = target_element
            current_intensity = abs(new_level - old_level)
        
        return results
    
    def _compute_nonlinearity(self, intensity: float) -> float:
        return 1.0 + (intensity ** self.nonlinearity_factor) * 0.5
    
    def balance(self) -> Dict:
        balancer = WuxingBalancer(self)
        return balancer.balance()
    
    def get_network_state(self) -> Dict[str, float]:
        return {
            element.value: module.activation_level
            for element, module in self.modules.items()
        }
    
    def get_balance_score(self) -> float:
        levels = [m.activation_level for m in self.modules.values()]
        if not levels:
            return 0.0
        
        avg = sum(levels) / len(levels)
        variance = sum((l - avg) ** 2 for l in levels) / len(levels)
        max_variance = 0.25
        
        return 1.0 - min(1.0, variance / max_variance)
    
    def reset(self):
        for module in self.modules.values():
            module.activation_level = 0.5
            module.energy_reserve = 1.0
            module.stability = 1.0
        self.propagation_history.clear()
    
    def _record_propagation(self, action: str, element: WuxingElement, 
                           intensity: float, results: Dict):
        record = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "element": element.value,
            "intensity": intensity,
            "results": results
        }
        self.propagation_history.append(record)
        
        if len(self.propagation_history) > 100:
            self.propagation_history = self.propagation_history[-100:]
    
    def get_generation_chain(self, element: WuxingElement) -> List[WuxingElement]:
        chain = [element]
        current = element
        for _ in range(4):
            current = self.GENERATION_CYCLE[current]
            chain.append(current)
        return chain
    
    def get_restriction_chain(self, element: WuxingElement) -> List[WuxingElement]:
        chain = [element]
        current = element
        for _ in range(4):
            current = self.RESTRICTION_CYCLE[current]
            chain.append(current)
        return chain


class WuxingBalancer:
    """五行动态平衡调节器 - Five Elements Dynamic Balance Regulator"""
    
    OVERSTRONG_THRESHOLD = 0.75
    OVERWEAK_THRESHOLD = 0.35
    BALANCE_TARGET = 0.5
    ADJUSTMENT_STRENGTH = 0.15
    
    def __init__(self, network: WuxingCouplingNetwork):
        self.network = network
        self.balance_history: List[Dict] = []
        self.adjustment_log: List[Dict] = []
    
    def monitor(self) -> Dict[WuxingElement, str]:
        status: Dict[WuxingElement, str] = {}
        
        for element, module in self.network.modules.items():
            level = module.activation_level
            
            if level > self.OVERSTRONG_THRESHOLD:
                status[element] = "overstrong"
            elif level < self.OVERWEAK_THRESHOLD:
                status[element] = "overweak"
            else:
                status[element] = "balanced"
        
        return status
    
    def trigger_restriction(self, element: WuxingElement) -> Dict:
        results = {
            "action": "trigger_restriction",
            "element": element.value,
            "reason": "overstrong",
            "effects": {}
        }
        
        restrictor = self._find_restrictor(element)
        if restrictor:
            restrictor_module = self.network.modules[restrictor]
            target_module = self.network.modules[element]
            
            intensity = self.ADJUSTMENT_STRENGTH * restrictor_module.activation_level
            
            propagation = self.network.propagate_restriction(restrictor, intensity)
            results["effects"] = propagation
            results["restrictor"] = restrictor.value
        
        self._log_adjustment(results)
        return results
    
    def trigger_generation(self, element: WuxingElement) -> Dict:
        results = {
            "action": "trigger_generation",
            "element": element.value,
            "reason": "overweak",
            "effects": {}
        }
        
        generator = self._find_generator(element)
        if generator:
            generator_module = self.network.modules[generator]
            
            intensity = self.ADJUSTMENT_STRENGTH * (1.0 + generator_module.activation_level)
            
            propagation = self.network.propagate_generation(generator, intensity)
            results["effects"] = propagation
            results["generator"] = generator.value
        
        self._log_adjustment(results)
        return results
    
    def balance(self) -> Dict:
        status = self.monitor()
        results = {
            "initial_state": self.network.get_network_state(),
            "initial_status": {e.value: s for e, s in status.items()},
            "adjustments": [],
            "final_state": {},
            "balance_score": 0.0
        }
        
        overstrong_elements = [
            e for e, s in status.items() if s == "overstrong"
        ]
        overweak_elements = [
            e for e, s in status.items() if s == "overweak"
        ]
        
        for element in overstrong_elements:
            adjustment = self.trigger_restriction(element)
            results["adjustments"].append(adjustment)
        
        for element in overweak_elements:
            adjustment = self.trigger_generation(element)
            results["adjustments"].append(adjustment)
        
        self._apply_decay()
        
        results["final_state"] = self.network.get_network_state()
        results["balance_score"] = self.network.get_balance_score()
        
        self._record_balance(results)
        
        return results
    
    def _find_restrictor(self, element: WuxingElement) -> Optional[WuxingElement]:
        for src, tgt in self.network.RESTRICTION_CYCLE.items():
            if tgt == element:
                return src
        return None
    
    def _find_generator(self, element: WuxingElement) -> Optional[WuxingElement]:
        for src, tgt in self.network.GENERATION_CYCLE.items():
            if tgt == element:
                return src
        return None
    
    def _apply_decay(self):
        for module in self.network.modules.values():
            decay = WuxingCouplingNetwork.DECAY_FACTOR * (module.activation_level - self.BALANCE_TARGET)
            module.update_activation(-decay * 0.5)
    
    def _log_adjustment(self, adjustment: Dict):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            **adjustment
        }
        self.adjustment_log.append(log_entry)
        
        if len(self.adjustment_log) > 100:
            self.adjustment_log = self.adjustment_log[-100:]
    
    def _record_balance(self, results: Dict):
        self.balance_history.append({
            "timestamp": datetime.now().isoformat(),
            "balance_score": results["balance_score"],
            "adjustments_count": len(results["adjustments"])
        })
        
        if len(self.balance_history) > 50:
            self.balance_history = self.balance_history[-50:]
    
    def get_balance_trend(self) -> List[float]:
        return [record["balance_score"] for record in self.balance_history]
    
    def suggest_adjustments(self) -> List[Dict]:
        suggestions = []
        status = self.monitor()
        
        for element, state in status.items():
            if state == "overstrong":
                restrictor = self._find_restrictor(element)
                if restrictor:
                    suggestions.append({
                        "element": element.value,
                        "action": "enhance_restriction",
                        "source": restrictor.value,
                        "reason": f"{element.value}过强，需增强{restrictor.value}的克制"
                    })
            elif state == "overweak":
                generator = self._find_generator(element)
                if generator:
                    suggestions.append({
                        "element": element.value,
                        "action": "enhance_generation",
                        "source": generator.value,
                        "reason": f"{element.value}过弱，需增强{generator.value}的生助"
                    })
        
        return suggestions


def create_wuxing_network(nonlinearity_factor: float = 1.5) -> WuxingCouplingNetwork:
    """工厂函数：创建五行耦合网络"""
    return WuxingCouplingNetwork(nonlinearity_factor=nonlinearity_factor)


def create_wuxing_balancer(network: WuxingCouplingNetwork) -> WuxingBalancer:
    """工厂函数：创建五行平衡调节器"""
    return WuxingBalancer(network)
