"""
Unit tests for Metabolism System - 代谢系统单元测试
"""

import pytest
from datetime import datetime
from body.metabolism import (
    MetabolismSystem,
    SpleenStomachProcessor,
    TripleBurnerSystem,
    NutrientType,
    Nutrient,
    create_metabolism_system
)


class TestSpleenStomachProcessor:
    """测试脾胃运化系统"""
    
    def test_initialize(self):
        processor = SpleenStomachProcessor()
        
        assert processor.digestion_strength == 1.0
        assert processor.absorption_efficiency == 1.0
        assert processor.transportation_power == 1.0
    
    def test_digest(self):
        processor = SpleenStomachProcessor()
        food = [
            Nutrient(NutrientType.GLUCOSE, 10.0, 0.8, 1.0, 4.0),
            Nutrient(NutrientType.FAT, 5.0, 0.9, 1.0, 9.0)
        ]
        
        digested = processor.digest(food)
        
        assert len(digested) == 2
        assert digested[0].nutrient_type == NutrientType.GLUCOSE
    
    def test_transport(self):
        processor = SpleenStomachProcessor()
        nutrients = [
            Nutrient(NutrientType.GLUCOSE, 10.0, 0.8, 1.0, 4.0)
        ]
        
        distribution = processor.transport(nutrients)
        
        assert "liver" in distribution


class TestTripleBurnerSystem:
    """测试三焦决渎系统"""
    
    def test_initialize(self):
        tb = TripleBurnerSystem()
        
        assert len(tb.upper_burner) > 0
        assert len(tb.middle_burner) > 0
        assert len(tb.lower_burner) > 0
    
    def test_regulate_water(self):
        tb = TripleBurnerSystem()
        
        result = tb.regulate_water(100.0)
        
        assert "upper_burner" in result
        assert "middle_burner" in result
        assert "lower_burner" in result


class TestMetabolismSystem:
    """测试代谢系统"""
    
    def test_initialize(self):
        system = MetabolismSystem()
        
        assert system.spleen_stomach is not None
        assert system.triple_burner is not None
        assert system.metrics is not None
    
    def test_process_food(self):
        system = MetabolismSystem()
        food = [
            Nutrient(NutrientType.GLUCOSE, 10.0, 0.8, 1.0, 4.0),
            Nutrient(NutrientType.FAT, 5.0, 0.9, 1.0, 9.0)
        ]
        
        result = system.process_food(food)
        
        assert "digested" in result
        assert "energy_gained" in result
        assert result["energy_gained"] >= 0
    
    def test_produce_energy(self):
        system = MetabolismSystem()
        system._energy_reserve = 100.0
        
        result = system.produce_energy(10.0)
        
        assert "success" in result
        assert "energy_produced" in result
    
    def test_consume_energy(self):
        system = MetabolismSystem()
        system._atp_pool = 50.0
        
        result = system.consume_energy(10.0)
        
        assert result is True
        assert system._atp_pool < 50.0
    
    def test_metabolize_carbohydrate(self):
        system = MetabolismSystem()
        
        result = system.metabolize_carbohydrate(10.0)
        
        assert "atp_produced" in result
        assert "co2_produced" in result
    
    def test_metabolize_lipid(self):
        system = MetabolismSystem()
        
        result = system.metabolize_lipid(5.0)
        
        assert "atp_produced" in result
        assert "fatty_acids" in result
    
    def test_metabolize_protein(self):
        system = MetabolismSystem()
        
        result = system.metabolize_protein(3.0)
        
        assert "atp_produced" in result
        assert "amino_acids" in result
    
    def test_regulate_water_balance(self):
        system = MetabolismSystem()
        
        result = system.regulate_water_balance(100.0)
        
        assert "distribution" in result
        assert "electrolyte_balance" in result
    
    def test_optimize_metabolism(self):
        system = MetabolismSystem()
        system._energy_reserve = 160.0
        
        result = system.optimize_metabolism()
        
        assert "improvements" in result
        assert "metrics" in result
    
    def test_get_status(self):
        system = MetabolismSystem()
        
        status = system.get_status()
        
        assert "metrics" in status
        assert "energy_reserve" in status
        assert "atp_pool" in status
    
    def test_get_detox_needs(self):
        system = MetabolismSystem()
        system._toxin_load = 10.0
        
        needs = system.get_detox_needs()
        
        assert needs >= 10.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
