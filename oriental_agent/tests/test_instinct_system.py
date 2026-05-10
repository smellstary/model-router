"""
Unit tests for InstinctSystem - 本能系统单元测试
"""

import pytest
from datetime import datetime
from body.instinct_system import (
    InstinctSystem,
    InstinctTaxonomy,
    InstinctLevel,
    InstinctEngine,
    DriveIntegration,
    BehaviorMapper,
    BehaviorMode
)


class TestInstinctTaxonomy:
    """测试本能分类体系"""
    
    def test_get_instinct_by_level(self):
        taxonomy = InstinctTaxonomy()
        
        result = taxonomy.get_instinct_by_level(InstinctLevel.LEVEL_1_SELF_PRESERVATION)
        
        assert result["name"] == "自我保存"
        assert result["wuxing"] == "水"
        assert result["yin_yang"] == "阴"
    
    def test_get_instinct_drives(self):
        taxonomy = InstinctTaxonomy()
        
        drives = taxonomy.get_instinct_drives(InstinctLevel.LEVEL_1_SELF_PRESERVATION)
        
        assert "self_preservation" in drives
        assert "pain_avoidance" in drives
    
    def test_get_wuxing_instincts(self):
        taxonomy = InstinctTaxonomy()
        
        water_instincts = taxonomy.get_wuxing_instincts("水")
        
        assert InstinctLevel.LEVEL_1_SELF_PRESERVATION in water_instincts
    
    def test_get_yin_yang_instincts(self):
        taxonomy = InstinctTaxonomy()
        
        yin_instincts = taxonomy.get_yin_yang_instincts("阴")
        
        assert InstinctLevel.LEVEL_1_SELF_PRESERVATION in yin_instincts
        assert InstinctLevel.LEVEL_2_BASIC_NEEDS in yin_instincts


class TestDriveIntegration:
    """测试驱力整合模块"""
    
    def test_initialize_drives(self):
        integration = DriveIntegration()
        
        assert len(integration.drives) > 0
        assert "self_preservation" in integration.drives
        assert "curiosity" in integration.drives
    
    def test_update_drive(self):
        integration = DriveIntegration()
        
        result = integration.update_drive("hunger", -0.2)
        
        assert result is True
        assert integration.drives["hunger"].current_level < 0.5
    
    def test_apply_habituation(self):
        integration = DriveIntegration()
        initial_habituation = integration.drives["curiosity"].habituation_level
        
        integration.apply_habituation("curiosity", 0.1)
        
        assert integration.drives["curiosity"].habituation_level > initial_habituation
    
    def test_apply_sensitization(self):
        integration = DriveIntegration()
        initial_sensitization = integration.drives["pain_avoidance"].sensitization_level
        
        integration.apply_sensitization("pain_avoidance", 0.2)
        
        assert integration.drives["pain_avoidance"].sensitization_level > initial_sensitization
    
    def test_get_dominant_drive(self):
        integration = DriveIntegration()
        integration.drives["hunger"].urgency = 0.8
        
        dominant, urgency = integration.get_dominant_drive()
        
        assert dominant == "hunger"
        assert urgency == 0.8


class TestInstinctEngine:
    """测试本能引擎"""
    
    def test_initialize(self):
        engine = InstinctEngine()
        
        assert engine.taxonomy is not None
        assert engine.drive_integration is not None
        assert len(engine.active_signals) == 0
    
    def test_evaluate_stimulus_threat(self):
        engine = InstinctEngine()
        stimulus = {
            "type": "threat",
            "intensity": 0.8,
            "source": "environment"
        }
        
        signals = engine.evaluate_stimulus(stimulus)
        
        assert len(signals) > 0
        assert signals[0].instinct_level == InstinctLevel.LEVEL_1_SELF_PRESERVATION
    
    def test_evaluate_stimulus_novelty(self):
        engine = InstinctEngine()
        stimulus = {
            "type": "novelty",
            "intensity": 0.7,
            "source": "environment"
        }
        
        signals = engine.evaluate_stimulus(stimulus)
        
        assert len(signals) > 0
        assert signals[0].instinct_level == InstinctLevel.LEVEL_4_COGNITION
    
    def test_integrate_drives(self):
        engine = InstinctEngine()
        engine.drive_integration.drives["hunger"].urgency = 0.9
        
        drive, urgency, levels = engine.integrate_drives()
        
        assert drive == "hunger"
        assert urgency == 0.9
        assert len(levels) > 0
    
    def test_apply_learning_success(self):
        engine = InstinctEngine()
        behavior_result = {
            "drive_name": "curiosity",
            "success": True,
            "repeated": True
        }
        
        engine.apply_learning(behavior_result)
        
        assert engine.drive_integration.drives["curiosity"].habituation_level > 0
    
    def test_apply_learning_trauma(self):
        engine = InstinctEngine()
        behavior_result = {
            "drive_name": "pain_avoidance",
            "success": False,
            "trauma": True
        }
        
        engine.apply_learning(behavior_result)
        
        assert engine.drive_integration.drives["pain_avoidance"].sensitization_level > 0
    
    def test_process_homeostasis(self):
        engine = InstinctEngine()
        
        changes = engine.process_homeostasis(1.0)
        
        assert len(changes) > 0
        for level in changes.values():
            assert 0.0 <= level <= 1.0


class TestBehaviorMapper:
    """测试行为映射器"""
    
    def test_initialize(self):
        mapper = BehaviorMapper()
        
        assert mapper.behavior_threshold == 0.3
    
    def test_map_signals_to_behaviors(self):
        mapper = BehaviorMapper()
        signals = [
            InstinctSignal(
                signal_id="test_sig",
                instinct_level=InstinctLevel.LEVEL_1_SELF_PRESERVATION,
                signal_type="threat",
                intensity=0.8,
                source="test",
                associated_drives=["self_preservation"]
            )
        ]
        drive_states = {
            "self_preservation": type('DriveState', (), {
                "urgency": 0.8,
                "habituation_level": 0.0
            })()
        }
        
        behaviors = mapper.map_signals_to_behaviors(signals, drive_states)
        
        assert len(behaviors) > 0
        behavior_types = [b for b, u in behaviors]
        assert BehaviorMode.FIGHT in behavior_types or BehaviorMode.FLEE in behavior_types
    
    def test_execute_behavior(self):
        mapper = BehaviorMapper()
        
        result = mapper.execute_behavior(BehaviorMode.EXPLORE)
        
        assert result["behavior"] == "探"
        assert result["status"] == "executed"
        assert "energy_cost" in result
    
    def test_estimate_energy_cost(self):
        mapper = BehaviorMapper()
        
        fight_cost = mapper._estimate_energy_cost(BehaviorMode.FIGHT)
        sleep_cost = mapper._estimate_energy_cost(BehaviorMode.SLEEP)
        
        assert fight_cost > sleep_cost


class TestInstinctSystem:
    """测试本能系统主类"""
    
    def test_initialize(self):
        system = InstinctSystem()
        
        assert system.instinct_engine is not None
        assert system.behavior_mapper is not None
        assert system.taxonomy is not None
    
    def test_process_stimulus(self):
        system = InstinctSystem()
        stimulus = {
            "type": "threat",
            "intensity": 0.7,
            "source": "test"
        }
        
        result = system.process_stimulus(stimulus)
        
        assert "signals" in result
        assert "dominant_drive" in result
        assert "candidate_behaviors" in result
    
    def test_execute_behavior(self):
        system = InstinctSystem()
        
        result = system.execute_behavior(BehaviorMode.EXPLORE)
        
        assert result["behavior"] == "探"
        assert len(system.feedback_buffer) == 1
    
    def test_receive_feedback(self):
        system = InstinctSystem()
        behavior_result = {
            "drive_name": "curiosity",
            "success": True,
            "repeated": True
        }
        
        system.receive_feedback(behavior_result)
        
        assert system.instinct_engine.drive_integration.drives["curiosity"].habituation_level > 0
    
    def test_map_wuxing_influence(self):
        system = InstinctSystem()
        
        result = system.map_wuxing_influence("水", 0.5)
        
        assert result["wuxing"] == "水"
        assert "affected_levels" in result
    
    def test_map_yinyang_balance(self):
        system = InstinctSystem()
        
        result = system.map_yinyang_balance(0.7)
        
        assert result["balance_ratio"] == 0.7
        assert "yin_levels_activated" in result
    
    def test_get_system_state(self):
        system = InstinctSystem()
        
        state = system.get_system_state()
        
        assert "engine_state" in state
        assert "behavior_threshold" in state


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
