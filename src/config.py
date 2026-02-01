"""
Configuration management for Resource Monitor
"""

import json
import os
from typing import Dict, Any


class Config:
    """Manage application configuration"""
    
    DEFAULT_CONFIG = {
        'update_interval': 2,
        'alert_enabled': True,
        'thresholds': {
            'cpu': 85.0,
            'memory': 90.0,
            'disk': 95.0,
            'battery': 15.0
        },
        'alert_cooldown': 300,
        'logging_enabled': False,
        'auto_export': False,
        'export_interval': 3600,  # 1 hour
        'theme': 'dark',
        'show_notifications': True,
        'history_size': 60
    }
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to config file, defaults to ~/.config/resource_monitor/config.json
        """
        if config_path is None:
            home = os.path.expanduser("~")
            config_dir = os.path.join(home, ".config", "resource_monitor")
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            config_path = os.path.join(config_dir, "config.json")
        
        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        """Load configuration from file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults (in case new keys were added)
                    self.config.update(loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}, using defaults")
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the final key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the final value
        config[keys[-1]] = value
        self.save()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()
