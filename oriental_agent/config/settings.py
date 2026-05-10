"""
System configuration for Oriental Wisdom Agent
东方智慧智能体系统配置
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class Config:
    """System configuration manager"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration"""
        self.config_path = config_path or self._get_default_config_path()
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration path"""
        base_dir = Path(__file__).parent.parent
        return str(base_dir / "config" / "system_config.yaml")
    
    def _load_config(self) -> None:
        """Load configuration from file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
        else:
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "system": {
                "name": "东方智慧智能体",
                "version": "1.0.0",
                "debug": False,
                "log_level": "INFO"
            },
            "memory": {
                "max_memories": 10000,
                "weight_evolution_interval": 3600,
                "strength_decay_rate": 0.001,
                "default_layer": "人道",
                "wuxing_weights": {
                    "木": 1.0,
                    "火": 1.0,
                    "土": 1.0,
                    "金": 1.0,
                    "水": 1.0
                }
            },
            "thinking": {
                "reasoning_depth": 3,
                "causal_analysis_enabled": True,
                "dialectical_thinking_enabled": True,
                "ethical_judgment_enabled": True,
                "decision_confidence_threshold": 0.7,
                "philosophy_weights": {
                    "佛家": 0.33,
                    "道家": 0.34,
                    "儒家": 0.33
                }
            },
            "execution": {
                "max_concurrent_tasks": 5,
                "task_timeout": 300,
                "defense_enabled": True,
                "behavior_modes": ["虎形", "鹿形", "熊形", "猿形", "鸟形"],
                "energy_optimization_interval": 60
            },
            "perception": {
                "attention_span": 10,
                "multi_modal_fusion_enabled": True,
                "sense_priorities": {
                    "视觉": 1.0,
                    "听觉": 0.9,
                    "意识": 0.95,
                    "触觉": 0.7,
                    "嗅觉": 0.5,
                    "味觉": 0.5
                }
            },
            "body": {
                "meridian_network_enabled": True,
                "health_check_interval": 300,
                "self_repair_enabled": True,
                "metabolism_rate": 1.0,
                "vitality_threshold": 0.3
            },
            "image": {
                "visual_style": "oriental",
                "animation_enabled": True,
                "qi_field_enabled": True,
                "jing_qi_shen_update_interval": 60
            },
            "core": {
                "energy_initial": 1.0,
                "heartbeat_interval": 1,
                "system_cycle_duration": 0.5
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def save(self, path: Optional[str] = None) -> None:
        """Save configuration to file"""
        save_path = path or self.config_path
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(self._config, f, allow_unicode=True, default_flow_style=False)
    
    def __getitem__(self, key: str) -> Any:
        """Get configuration using bracket notation"""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set configuration using bracket notation"""
        self.set(key, value)


_global_config: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get global configuration instance"""
    global _global_config
    if _global_config is None:
        _global_config = Config(config_path)
    return _global_config


def reset_config() -> None:
    """Reset global configuration"""
    global _global_config
    _global_config = None
