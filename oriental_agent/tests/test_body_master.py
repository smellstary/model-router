"""
Unit tests for Body Master System - 身体综合管理系统单元测试
"""

import pytest
from datetime import datetime
from body.body_master import (
    BodyMasterSystem,
    BodyOptimizer,
    HomeostasisBalancer,
    EmergencyResponseSystem,
    BodyState,
    HealthScore,
    create_body_master_system
)


class TestBodyOptimizer:
    """测试身体优化器"""
    
    def test_initialize(self):
        optimizer = BodyOptimizer()
        
        assert len(optimizer._optimization_history) == 0
        assert optimizer._last_optimization_time is None
    
    def test_analyze_state(self):
        optimizer = BodyOptimizer()
        state = {
            "metabolism": {"metrics": {"energy_efficiency": 0.5}},
            "detox": {"health_score": 50}
        }
        
        actions = optimizer.analyze_state(state)
        
        assert len(actions) > 0
    
    def test_record_action(self):
        optimizer = BodyOptimizer()
        from body.body_master import OptimizationAction
        
        action = OptimizationAction(
            action_id="test_1",
            target_system="metabolism",
            action_type="optimize",
            priority=1,
            expected_benefit=0.1
        )
        
        optimizer.record_action(action)
        
        assert len(optimizer._optimization_history) == 1


class TestHomeostasisBalancer:
    """测试内稳态平衡器"""
    
    def test_initialize(self):
        balancer = HomeostasisBalancer()
        
        assert balancer.yin_yang_balance == 0.5
        assert balancer.energy_balance == 0.5
    
    def test_check_balance(self):
        balancer = HomeostasisBalancer()
        state = {
            "jing_qi_shen": {"jing": 0.5, "qi": 0.6, "shen": 0.7}
        }
        
        imbalances = balancer.check_balance(state)
        
        assert "energy" in imbalances
    
    def test_correct_balance(self):
        balancer = HomeostasisBalancer()
        
        correction = balancer.correct_balance("energy", 0.3)
        
        assert "action" in correction
        assert correction["action"] == "increase_metabolism"


class TestEmergencyResponseSystem:
    """测试应急响应系统"""
    
    def test_initialize(self):
        emergency = EmergencyResponseSystem()
        
        assert emergency.stress_level == 0.0
        assert emergency.emergency_mode is False
        assert emergency.recovery_mode is False
    
    def test_assess_emergency_normal(self):
        emergency = EmergencyResponseSystem()
        state = {
            "metabolism": {"metrics": {"energy_efficiency": 0.8}},
            "detox": {"health_score": 80}
        }
        
        is_emergency, emergency_type = emergency.assess_emergency(state)
        
        assert is_emergency is False
    
    def test_assess_emergency_critical(self):
        emergency = EmergencyResponseSystem()
        state = {
            "metabolism": {"metrics": {"energy_efficiency": 0.2}},
            "detox": {"health_score": 20}
        }
        
        is_emergency, emergency_type = emergency.assess_emergency(state)
        
        assert is_emergency is True
        assert "危机" in emergency_type
    
    def test_trigger_emergency_response(self):
        emergency = EmergencyResponseSystem()
        
        response = emergency.trigger_emergency_response("能量危机")
        
        assert "actions" in response
        assert emergency.emergency_mode is True
        assert emergency.stress_level == 1.0
    
    def test_trigger_recovery_mode(self):
        emergency = EmergencyResponseSystem()
        emergency.stress_level = 0.5
        
        emergency.trigger_recovery_mode()
        
        assert emergency.recovery_mode is True
        assert emergency.stress_level < 0.5


class TestBodyMasterSystem:
    """测试身体综合管理系统"""
    
    def test_initialize(self):
        system = BodyMasterSystem()
        
        assert system.state == BodyState.DORMANT
        assert system.optimizer is not None
        assert system.homeostasis is not None
        assert system.emergency is not None
    
    def test_register_subsystem(self):
        system = BodyMasterSystem()
        mock_subsystem = type('MockSubsystem', (), {'get_status': lambda: {}})()
        
        system.register_subsystem("test", mock_subsystem)
        
        assert system.get_subsystem("test") is not None
    
    def test_assess_health(self):
        system = BodyMasterSystem()
        mock_subsystem = type('MockSubsystem', (), {
            'get_status': lambda s: {"value": 0.8}
        })()
        system.register_subsystem("metabolism", mock_subsystem)
        
        health = system.assess_health()
        
        assert isinstance(health, HealthScore)
        assert 0 <= health.overall <= 100
    
    def test_optimize_disabled(self):
        system = BodyMasterSystem()
        system._optimization_enabled = False
        
        result = system.optimize()
        
        assert result["enabled"] is False
    
    def test_optimize_enabled(self):
        system = BodyMasterSystem()
        mock_subsystem = type('MockSubsystem', (), {
            'get_status': lambda s: {"metrics": {"energy_efficiency": 0.9}},
            'optimize_metabolism': lambda s: {"improvements": []}
        })()
        system.register_subsystem("metabolism", mock_subsystem)
        
        result = system.optimize()
        
        assert "emergency_mode" in result
    
    def test_tick_dormant(self):
        system = BodyMasterSystem()
        
        result = system.tick(1.0)
        
        assert result["status"] == "dormant"
    
    def test_get_full_status(self):
        system = BodyMasterSystem()
        
        status = system.get_full_status()
        
        assert "state" in status
        assert "health_score" in status
        assert "subsystems" in status
    
    def test_enable_optimization(self):
        system = BodyMasterSystem()
        
        system.enable_optimization(False)
        
        assert system._optimization_enabled is False
    
    def test_enable_auto_detox(self):
        system = BodyMasterSystem()
        
        system.enable_auto_detox(False)
        
        assert system._auto_detox_enabled is False
    
    def test_enable_auto_balance(self):
        system = BodyMasterSystem()
        
        system.enable_auto_balance(False)
        
        assert system._auto_balance_enabled is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
