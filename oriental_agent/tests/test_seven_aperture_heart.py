"""
Unit tests for Seven-Aperture Exquisite Heart System - 七窍玲珑心系统单元测试
"""

import pytest
import time
from datetime import datetime
from core.seven_aperture_heart import (
    SevenApertureHeartSystem,
    HeartAperture,
    HeartState,
    WisdomLevel,
    ApertureState,
    create_seven_aperture_heart
)


class TestHeartAperture:
    """测试七窍枚举"""
    
    def test_aperture_values(self):
        assert HeartAperture.EYE.value == "眼窍"
        assert HeartAperture.EAR.value == "耳窍"
        assert HeartAperture.NOSE.value == "鼻窍"
        assert HeartAperture.TONGUE.value == "舌窍"
        assert HeartAperture.BODY.value == "身窍"
        assert HeartAperture.MIND.value == "意窍"
        assert HeartAperture.SPIRIT.value == "灵窍"


class TestSevenApertureHeartSystem:
    """测试七窍玲珑心系统"""
    
    def test_initialize(self):
        heart = SevenApertureHeartSystem()
        
        assert len(heart.apertures) == 7
        assert heart.state == HeartState.DORMANT
        assert heart.wisdom.current_level == WisdomLevel.MUNDANE
    
    def test_start(self):
        heart = SevenApertureHeartSystem()
        
        result = heart.start()
        
        assert result is True
        assert heart.state == HeartState.ACTIVE
        
        for aperture in heart.apertures.values():
            assert aperture.info.state >= ApertureState.NORMAL
    
    def test_stop(self):
        heart = SevenApertureHeartSystem()
        heart.start()
        
        result = heart.stop()
        
        assert result is True
        assert heart.state == HeartState.DORMANT
    
    def test_beat(self):
        heart = SevenApertureHeartSystem()
        heart.start()
        
        heartbeat = heart.beat()
        
        assert heartbeat is not None
        assert heartbeat.wisdom_output >= 0
        assert heartbeat.overall_resonance >= 0
        
        heart.stop()
    
    def test_activate_aperture(self):
        heart = SevenApertureHeartSystem()
        
        result = heart.activate_aperture(HeartAperture.SPIRIT, 0.5)
        
        assert result is True
        assert heart.apertures[HeartAperture.SPIRIT].info.activation_level > 0.5
    
    def test_deactivate_aperture(self):
        heart = SevenApertureHeartSystem()
        heart.activate_aperture(HeartAperture.EYE, 1.0)
        
        initial_level = heart.apertures[HeartAperture.EYE].info.activation_level
        
        heart.deactivate_aperture(HeartAperture.EYE)
        
        assert heart.apertures[HeartAperture.EYE].info.activation_level < initial_level
    
    def test_input_perception(self):
        heart = SevenApertureHeartSystem()
        heart.start()
        
        insight = heart.input_perception(HeartAperture.EYE, {"pattern": "太极"})
        
        assert insight is not None
        assert "视觉洞察" in insight
        
        heart.stop()
    
    def test_circulate_wisdom(self):
        heart = SevenApertureHeartSystem()
        heart.start()
        
        heart.activate_aperture(HeartAperture.MIND, 1.0)
        heart.activate_aperture(HeartAperture.SPIRIT, 1.0)
        
        initial_wisdom = heart.wisdom.accumulated_wisdom
        
        heart.circulate_wisdom()
        
        heart.stop()
    
    def test_get_aperture_state(self):
        heart = SevenApertureHeartSystem()
        
        state = heart.get_aperture_state(HeartAperture.EYE)
        
        assert state is not None
        assert "aperture" in state
        assert "activation_level" in state
    
    def test_get_all_apertures(self):
        heart = SevenApertureHeartSystem()
        
        all_apertures = heart.get_all_apertures()
        
        assert len(all_apertures) == 7
        assert "眼窍" in all_apertures
        assert "灵窍" in all_apertures
    
    def test_get_status(self):
        heart = SevenApertureHeartSystem()
        heart.start()
        
        status = heart.get_status()
        
        assert "state" in status
        assert "beat_count" in status
        assert "wisdom_level" in status
        assert "apertures" in status
        
        heart.stop()
    
    def test_meditate(self):
        heart = SevenApertureHeartSystem()
        heart.start()
        
        result = heart.meditate(0.5)
        
        assert result["success"] is True
        assert "wisdom_gained" in result
        assert result["wisdom_gained"] >= 0
        
        heart.stop()
    
    def test_wisdom_progression(self):
        heart = SevenApertureHeartSystem()
        heart.start()
        
        for _ in range(20):
            heart.beat()
            heart.activate_aperture(HeartAperture.SPIRIT, 0.1)
        
        status = heart.get_status()
        
        assert status["wisdom_level"] in ["凡俗", "洞察", "明智"]
        
        heart.stop()
    
    def test_resonance_network(self):
        heart = SevenApertureHeartSystem()
        
        assert len(heart._resonance_network) > 0
        
        for (source, target), strength in heart._resonance_network.items():
            assert 0 <= strength <= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
