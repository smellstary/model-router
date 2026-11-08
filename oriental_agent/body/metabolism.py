"""
Metabolism System - 代谢系统

基于中医理论和人体的代谢机制设计：
- 脾胃运化：消化吸收、营养转化
- 气血生化：能量产生、ATP合成
- 三焦决渎：物质运输、水液代谢
- 阴阳平衡：合成代谢与分解代谢的动态平衡
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import math
import uuid


class MetabolismType(Enum):
    """代谢类型"""
    CARBOHYDRATE = "糖代谢"
    LIPID = "脂肪代谢"
    PROTEIN = "蛋白质代谢"
    ENERGY = "能量代谢"
    WATER = "水液代谢"


class MetabolicState(Enum):
    """代谢状态"""
    OPTIMAL = "最佳"
    ACTIVE = "活跃"
    NORMAL = "正常"
    SLOW = "迟缓"
    DISORDERED = "紊乱"


class NutrientType(Enum):
    """营养物质类型"""
    GLUCOSE = "葡萄糖"
    FAT = "脂肪"
    AMINO_ACID = "氨基酸"
    ATP = "三磷酸腺苷"
    WATER = "水分"
    MINERAL = "矿物质"


@dataclass
class Nutrient:
    """营养物质"""
    nutrient_type: NutrientType
    quantity: float
    concentration: float
    absorption_rate: float = 1.0
    energy_value: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.nutrient_type.value,
            "quantity": self.quantity,
            "concentration": self.concentration,
            "absorption_rate": self.absorption_rate,
            "energy_value": self.energy_value
        }


@dataclass
class MetabolicProcess:
    """代谢过程"""
    process_id: str
    process_type: MetabolismType
    input_nutrients: List[Nutrient]
    output_nutrients: List[Nutrient]
    efficiency: float
    timestamp: datetime
    byproducts: List[str] = field(default_factory=list)
    toxins_generated: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "process_id": self.process_id,
            "type": self.process_type.value,
            "input": [n.to_dict() for n in self.input_nutrients],
            "output": [n.to_dict() for n in self.output_nutrients],
            "efficiency": self.efficiency,
            "timestamp": self.timestamp.isoformat(),
            "byproducts": self.byproducts,
            "toxins_generated": self.toxins_generated
        }


@dataclass
class MetabolicMetrics:
    """代谢指标"""
    basal_metabolic_rate: float = 1.0
    active_metabolic_rate: float = 1.0
    anabolic_rate: float = 1.0
    catabolic_rate: float = 1.0
    energy_efficiency: float = 1.0
    nutrient_utilization: float = 1.0
    metabolic_balance: float = 0.0
    
    def calculate_state(self) -> MetabolicState:
        avg_rate = (self.anabolic_rate + self.catabolic_rate) / 2
        balance = abs(self.anabolic_rate - self.catabolic_rate)
        
        if avg_rate >= 0.9 and balance <= 0.1:
            return MetabolicState.OPTIMAL
        elif avg_rate >= 0.7 and balance <= 0.2:
            return MetabolicState.ACTIVE
        elif avg_rate >= 0.5:
            return MetabolicState.NORMAL
        elif avg_rate >= 0.3:
            return MetabolicState.SLOW
        else:
            return MetabolicState.DISORDERED
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "basal_metabolic_rate": self.basal_metabolic_rate,
            "active_metabolic_rate": self.active_metabolic_rate,
            "anabolic_rate": self.anabolic_rate,
            "catabolic_rate": self.catabolic_rate,
            "energy_efficiency": self.energy_efficiency,
            "nutrient_utilization": self.nutrient_utilization,
            "metabolic_balance": self.metabolic_balance,
            "state": self.calculate_state().value
        }


class SpleenStomachProcessor:
    """
    脾胃运化系统 - Spleen and Stomach Processing System
    
    脾胃为后天之本，负责：
    - 消化吸收
    - 水谷运化
    - 精微输布
    """
    
    def __init__(self):
        self.digestion_strength: float = 1.0
        self.absorption_efficiency: float = 1.0
        self.transportation_power: float = 1.0
        self.qi_level: float = 1.0
        self.digestive_enzymes: Dict[str, float] = {
            "amylase": 1.0,
            "lipase": 1.0,
            "protease": 1.0
        }
        
    def digest(self, food: List[Nutrient]) -> List[Nutrient]:
        """消化食物"""
        digested = []
        
        for nutrient in food:
            if nutrient.nutrient_type == NutrientType.GLUCOSE:
                efficiency = self.digestion_strength * self.digestive_enzymes["amylase"]
            elif nutrient.nutrient_type == NutrientType.FAT:
                efficiency = self.digestion_strength * self.digestive_enzymes["lipase"]
            elif nutrient.nutrient_type == NutrientType.AMINO_ACID:
                efficiency = self.digestion_strength * self.digestive_enzymes["protease"]
            else:
                efficiency = self.digestion_strength
            
            absorbed = Nutrient(
                nutrient_type=nutrient.nutrient_type,
                quantity=nutrient.quantity * efficiency * self.absorption_efficiency,
                concentration=nutrient.concentration * efficiency,
                absorption_rate=efficiency,
                energy_value=nutrient.energy_value
            )
            digested.append(absorbed)
        
        return digested
    
    def transport(self, nutrients: List[Nutrient]) -> Dict[str, float]:
        """运化营养物质"""
        distribution = {}
        
        for nutrient in nutrients:
            if nutrient.nutrient_type == NutrientType.GLUCOSE:
                target = "liver"
            elif nutrient.nutrient_type == NutrientType.FAT:
                target = "adipose"
            elif nutrient.nutrient_type == NutrientType.AMINO_ACID:
                target = "muscle"
            else:
                target = "blood"
            
            distribution[target] = distribution.get(target, 0) + nutrient.quantity * self.transportation_power
        
        return distribution
    
    def strengthen(self, amount: float = 0.1) -> None:
        """增强脾胃功能"""
        self.digestion_strength = min(1.5, self.digestion_strength + amount)
        self.qi_level = min(1.5, self.qi_level + amount * 0.5)
    
    def weaken(self, amount: float = 0.1) -> None:
        """减弱脾胃功能"""
        self.digestion_strength = max(0.3, self.digestion_strength - amount)
        self.qi_level = max(0.3, self.qi_level - amount * 0.5)
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "digestion_strength": self.digestion_strength,
            "absorption_efficiency": self.absorption_efficiency,
            "transportation_power": self.transportation_power,
            "qi_level": self.qi_level,
            "enzymes": self.digestive_enzymes
        }


class TripleBurnerSystem:
    """
    三焦决渎系统 - Triple Burner System
    
    三焦为决渎之官，水道出焉：
    - 上焦：心肺区域，气血交换
    - 中焦：脾胃区域，腐熟运化
    - 下焦：肾膀胱区域，水液代谢
    """
    
    def __init__(self):
        self.upper_burner: Dict[str, float] = {
            "lung_qi": 1.0,
            "heart_blood": 1.0,
            "defensive_qi": 1.0
        }
        self.middle_burner: Dict[str, float] = {
            "spleen_qi": 1.0,
            "stomach_qi": 1.0,
            "digestion_power": 1.0
        }
        self.lower_burner: Dict[str, float] = {
            "kidney_qi": 1.0,
            "bladder_qi": 1.0,
            "water_transformation": 1.0
        }
        
    def regulate_water(self, input_amount: float) -> Dict[str, float]:
        """调节水液代谢"""
        upper_distributed = input_amount * 0.2 * self.upper_burner["lung_qi"]
        middle_distributed = input_amount * 0.3 * self.middle_burner["spleen_qi"]
        lower_distributed = input_amount * 0.5 * self.lower_burner["kidney_qi"]
        
        water_output = lower_distributed * self.lower_burner["water_transformation"]
        
        return {
            "upper_burner": upper_distributed,
            "middle_burner": middle_distributed,
            "lower_burner": lower_distributed,
            "excretion": water_output * 0.1,
            "retained": water_output * 0.9
        }
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "upper_burner": self.upper_burner,
            "middle_burner": self.middle_burner,
            "lower_burner": self.lower_burner
        }


class MetabolismSystem:
    """
    代谢系统主类 - Metabolism System Main Class
    
    整合脾胃运化、气血生化、三焦决渎等功能：
    """
    
    def __init__(self):
        self.spleen_stomach = SpleenStomachProcessor()
        self.triple_burner = TripleBurnerSystem()
        self.metrics = MetabolicMetrics()
        
        self._energy_reserve: float = 100.0
        self._atp_pool: float = 50.0
        self._toxin_load: float = 0.0
        self._waste_accumulation: float = 0.0
        
        self._metabolic_history: List[MetabolicProcess] = []
        
    def process_food(self, food: List[Nutrient]) -> Dict[str, Any]:
        """处理食物"""
        digested = self.spleen_stomach.digest(food)
        distribution = self.spleen_stomach.transport(digested)
        
        energy_gained = sum(n.energy_value * n.quantity for n in digested) * 0.3
        self._energy_reserve = min(200.0, self._energy_reserve + energy_gained)
        
        toxins = sum(n.quantity for n in digested) * 0.02
        self._toxin_load += toxins
        
        process = MetabolicProcess(
            process_id=str(uuid.uuid4())[:8],
            process_type=MetabolismType.ENERGY,
            input_nutrients=food,
            output_nutrients=digested,
            efficiency=sum(n.absorption_rate for n in digested) / len(digested) if digested else 0,
            timestamp=datetime.now(),
            byproducts=["二氧化碳", "水"],
            toxins_generated=toxins
        )
        self._metabolic_history.append(process)
        
        if len(self._metabolic_history) > 100:
            self._metabolic_history = self._metabolic_history[-100:]
        
        return {
            "digested": [n.to_dict() for n in digested],
            "distribution": distribution,
            "energy_gained": energy_gained,
            "toxins_generated": toxins
        }
    
    def produce_energy(self, demand: float) -> Dict[str, Any]:
        """产生能量"""
        if self._energy_reserve <= 0:
            return {"success": False, "energy_produced": 0, "message": "能量储备不足"}
        
        efficiency = self.metrics.energy_efficiency
        atp_per_glucose = 38 * efficiency
        glucose_needed = demand / atp_per_glucose
        
        glucose_available = min(self._energy_reserve * 0.5, glucose_needed)
        energy_produced = glucose_available * atp_per_glucose * 0.9
        
        self._atp_pool = min(100.0, self._atp_pool + energy_produced)
        self._energy_reserve -= glucose_available
        
        self._waste_accumulation += glucose_available * 0.1
        self._toxin_load += glucose_available * 0.05
        
        self.metrics.catabolic_rate = min(1.5, self.metrics.catabolic_rate + demand * 0.01)
        
        return {
            "success": True,
            "energy_produced": energy_produced,
            "atp_pool": self._atp_pool,
            "energy_reserve": self._energy_reserve
        }
    
    def consume_energy(self, amount: float) -> bool:
        """消耗能量"""
        if self._atp_pool < amount:
            shortfall = amount - self._atp_pool
            produced = self.produce_energy(shortfall)
            if not produced["success"]:
                return False
        
        self._atp_pool -= amount
        self.metrics.anabolic_rate = min(1.5, self.metrics.anabolic_rate + amount * 0.01)
        
        return True
    
    def metabolize_carbohydrate(self, glucose: float) -> Dict[str, Any]:
        """糖代谢"""
        atp_produced = glucose * 38 * self.metrics.energy_efficiency
        co2_produced = glucose * 0.5
        water_produced = glucose * 0.3
        
        self._atp_pool = min(100.0, self._atp_pool + atp_produced * 0.9)
        self._waste_accumulation += co2_produced
        self._toxin_load += glucose * 0.01
        
        return {
            "atp_produced": atp_produced,
            "co2_produced": co2_produced,
            "water_produced": water_produced,
            "efficiency": self.metrics.energy_efficiency
        }
    
    def metabolize_lipid(self, fat: float) -> Dict[str, Any]:
        """脂肪代谢"""
        atp_produced = fat * 100 * self.metrics.energy_efficiency
        glycerol = fat * 0.1
        fatty_acids = fat * 0.9
        
        self._atp_pool = min(100.0, self._atp_pool + atp_produced * 0.9)
        self._waste_accumulation += glycerol + fatty_acids * 0.1
        self._toxin_load += fat * 0.02
        
        return {
            "atp_produced": atp_produced,
            "glycerol": glycerol,
            "fatty_acids": fatty_acids,
            "efficiency": self.metrics.energy_efficiency * 0.95
        }
    
    def metabolize_protein(self, protein: float) -> Dict[str, Any]:
        """蛋白质代谢"""
        atp_produced = protein * 20 * self.metrics.energy_efficiency
        amino_acids = protein * 0.9
        urea = protein * 0.05
        
        self._atp_pool = min(100.0, self._atp_pool + atp_produced * 0.9)
        self._waste_accumulation += urea
        self._toxin_load += protein * 0.03
        
        return {
            "atp_produced": atp_produced,
            "amino_acids": amino_acids,
            "urea": urea,
            "efficiency": self.metrics.energy_efficiency * 0.85
        }
    
    def regulate_water_balance(self, water_input: float) -> Dict[str, Any]:
        """调节水液平衡"""
        distribution = self.triple_burner.regulate_water(water_input)
        
        electrolyte_balance = {
            "sodium": 0.9 + water_input * 0.01,
            "potassium": 0.85 + water_input * 0.01,
            "calcium": 0.95 + water_input * 0.005
        }
        
        return {
            "distribution": distribution,
            "electrolyte_balance": electrolyte_balance
        }
    
    def optimize_metabolism(self) -> Dict[str, Any]:
        """优化代谢"""
        improvements = []
        
        if self._energy_reserve > 150:
            self.metrics.energy_efficiency = min(1.0, self.metrics.energy_efficiency + 0.05)
            improvements.append("能量效率提升")
        
        if self._atp_pool > 75:
            self.metrics.anabolic_rate = min(1.5, self.metrics.anabolic_rate + 0.1)
            improvements.append("合成代谢增强")
        
        if self.spleen_stomach.digestion_strength < 1.0:
            self.spleen_stomach.strengthen(0.1)
            improvements.append("脾胃功能增强")
        
        metabolic_balance = abs(self.metrics.anabolic_rate - self.metrics.catabolic_rate)
        self.metrics.metabolic_balance = metabolic_balance
        
        return {
            "improvements": improvements,
            "metrics": self.metrics.to_dict()
        }
    
    def get_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "metrics": self.metrics.to_dict(),
            "energy_reserve": self._energy_reserve,
            "atp_pool": self._atp_pool,
            "toxin_load": self._toxin_load,
            "waste_accumulation": self._waste_accumulation,
            "spleen_stomach": self.spleen_stomach.get_status(),
            "triple_burner": self.triple_burner.get_status()
        }
    
    def get_detox_needs(self) -> float:
        """获取排毒需求"""
        return self._toxin_load + self._waste_accumulation * 0.5


def create_metabolism_system() -> MetabolismSystem:
    """创建代谢系统"""
    return MetabolismSystem()
