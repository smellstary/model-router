"""
Unit tests for Liver Detoxification System - 肝胆排毒系统单元测试
"""

import pytest
from datetime import datetime
from body.liver_detox import (
    LiverGallbladderDetoxSystem,
    LiverSystem,
    GallbladderSystem,
    DetoxCycleManager,
    Toxin,
    ToxinType,
    DetoxPhase,
    create_liver_gallbladder_system
)


class TestLiverSystem:
    """测试肝脏系统"""
    
    def test_initialize(self):
        liver = LiverSystem()
        
        assert liver.metrics is not None
        assert liver._qi_level == 1.0
        assert liver._blood_volume == 100.0
    
    def test_filter_blood(self):
        liver = LiverSystem()
        
        result = liver.filter_blood(0.7)
        
        assert "toxins_removed" in result
        assert "blood_quality" in result
        assert result["blood_quality"] > 0.7
    
    def test_store_blood(self):
        liver = LiverSystem()
        
        stored = liver.store_blood(20.0)
        
        assert stored > 0
        assert liver._blood_volume > 100.0
    
    def test_release_blood(self):
        liver = LiverSystem()
        liver._blood_volume = 110.0
        
        released = liver.release_blood(10.0)
        
        assert released > 0
        assert liver._blood_volume < 110.0
    
    def test_detoxify(self):
        liver = LiverSystem()
        toxin = Toxin(
            toxin_id="test_toxin",
            toxin_type=ToxinType.METABOLIC,
            quantity=10.0,
            toxicity_level=0.5,
            source="test",
            timestamp=datetime.now()
        )
        
        result = liver.detoxify(toxin)
        
        assert "processed" in result
        assert "remaining" in result
        assert 0 <= result["processed"] <= 1.0
    
    def test_regenerate(self):
        liver = LiverSystem()
        liver.metrics.toxin_processing_speed = 0.5
        
        liver.regenerate()
        
        assert liver.metrics.toxin_processing_speed >= 0.5


class TestGallbladderSystem:
    """测试胆囊系统"""
    
    def test_initialize(self):
        gb = GallbladderSystem()
        
        assert gb.state.value == "最佳"
        assert gb._bile_reserve == 100.0
        assert gb._bile_quality == 1.0
    
    def test_produce_bile(self):
        gb = GallbladderSystem()
        
        bile = gb.produce_bile(10.0)
        
        assert bile.amount == 10.0
        assert bile.bile_acids > 0
    
    def test_secrete_bile(self):
        gb = GallbladderSystem()
        gb._bile_reserve = 50.0
        
        bile = gb.secrete_bile(20.0)
        
        assert bile.amount == 20.0
        assert gb._bile_reserve == 30.0
    
    def test_make_decision(self):
        gb = GallbladderSystem()
        options = ["option_a", "option_b", "option_c"]
        criteria = {"safety": 0.8, "efficiency": 0.7}
        
        decision, confidence = gb.make_decision(options, criteria)
        
        assert decision in options
        assert 0 <= confidence <= 1.0


class TestDetoxCycleManager:
    """测试排毒周期管理器"""
    
    def test_initialize(self):
        manager = DetoxCycleManager()
        
        assert len(manager._cycles) == 0
        assert manager._current_cycle is None
    
    def test_start_cycle(self):
        manager = DetoxCycleManager()
        
        cycle = manager.start_cycle()
        
        assert cycle is not None
        assert cycle.phase == DetoxPhase.MOBILIZATION
        assert len(manager._cycles) == 1
    
    def test_progress_cycle(self):
        manager = DetoxCycleManager()
        manager.start_cycle()
        
        phase = manager.progress_cycle(1.0)
        
        assert phase in DetoxPhase


class TestLiverGallbladderDetoxSystem:
    """测试肝胆排毒系统"""
    
    def test_initialize(self):
        system = LiverGallbladderDetoxSystem()
        
        assert system.liver is not None
        assert system.gallbladder is not None
        assert system.detox_manager is not None
        assert system._health_score == 100.0
    
    def test_receive_toxins(self):
        system = LiverGallbladderDetoxSystem()
        toxins = [
            Toxin(
                toxin_id="toxin_1",
                toxin_type=ToxinType.METABOLIC,
                quantity=10.0,
                toxicity_level=0.5,
                source="test",
                timestamp=datetime.now()
            )
        ]
        
        result = system.receive_toxins(toxins)
        
        assert result["toxins_received"] == 1
        assert "processing_results" in result
    
    def test_start_detox_cycle(self):
        system = LiverGallbladderDetoxSystem()
        
        result = system.start_detox_cycle()
        
        assert result["cycle_started"] is True
        assert "cycle" in result
    
    def test_perform_detox(self):
        system = LiverGallbladderDetoxSystem()
        system.start_detox_cycle()
        
        result = system.perform_detox(1.0)
        
        assert "phase" in result
        assert "liver" in result
        assert "health_score" in result
    
    def test_provide_bile(self):
        system = LiverGallbladderDetoxSystem()
        
        result = system.provide_bile("intestine", 10.0)
        
        assert "bile" in result
        assert result["target"] == "intestine"
    
    def test_make_major_decision(self):
        system = LiverGallbladderDetoxSystem()
        options = ["defend", "adapt", "withdraw"]
        
        result = system.make_major_decision("threat", options)
        
        assert "decision" in result
        assert "confidence" in result
    
    def test_get_full_status(self):
        system = LiverGallbladderDetoxSystem()
        
        status = system.get_full_status()
        
        assert "health_score" in status
        assert "liver" in status
        assert "gallbladder" in status
    
    def test_get_detox_needs(self):
        system = LiverGallbladderDetoxSystem()
        system.liver._stored_toxins.append(Toxin(
            toxin_id="test",
            toxin_type=ToxinType.METABOLIC,
            quantity=10.0,
            toxicity_level=0.5,
            source="test",
            timestamp=datetime.now()
        ))
        
        needs = system.get_detox_needs()
        
        assert "stored_toxins" in needs
        assert needs["stored_toxins"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
