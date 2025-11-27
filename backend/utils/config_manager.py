"""
Configuration management for the application.
"""
import json
import os
from typing import Dict, Any


class ConfigManager:
    """Manages application configuration with defaults and validation."""

    DEFAULT_CONFIG = {
        "device": "cpu",  # Default to CPU for safety
        "model_dirs": {
            "summarizer": "backend/models/summ_model",
            "translator": "backend/models/trans_model"
        },
        "qa_model": "deepset/roberta-base-squad2",
        "max_text_length": 512,
        "max_summary_length": 512
    }

    def __init__(self, config_path: str = "backend/app_config.json"):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file with fallback to defaults."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Merge with defaults for missing keys
                merged_config = self.DEFAULT_CONFIG.copy()
                self._deep_update(merged_config, config)
                return merged_config
            else:
                print(f"Warning: Config file {self.config_path} not found, using defaults")
                return self.DEFAULT_CONFIG.copy()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Error loading config: {e}, using defaults")
            return self.DEFAULT_CONFIG.copy()

    def _deep_update(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """Deep update a dictionary."""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value

    @property
    def device(self) -> str:
        return self._config.get("device", "cpu")

    @property
    def model_dirs(self) -> Dict[str, str]:
        return self._config.get("model_dirs", {})

    @property
    def qa_model(self) -> str:
        return self._config.get("qa_model", self.DEFAULT_CONFIG["qa_model"])

    @property
    def max_text_length(self) -> int:
        return self._config.get("max_text_length", 512)

    @property
    def max_summary_length(self) -> int:
        return self._config.get("max_summary_length", 512)

    def get_model_dir(self, model_type: str) -> str:
        """Get model directory for a specific type."""
        return self.model_dirs.get(model_type, "")


# Global config instance
config_manager = ConfigManager()
