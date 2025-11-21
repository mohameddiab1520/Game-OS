"""
GameOS AI - Configuration Management
"""

import os
import json
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class GameOSConfig(BaseSettings):
    """Main configuration for GameOS AI"""

    # Server Settings
    server_host: str = Field(default="localhost", description="Server host")
    server_port: int = Field(default=8765, description="Server port")
    log_level: str = Field(default="INFO", description="Logging level")

    # Unity Connection
    unity_host: str = Field(default="localhost", description="Unity connection host")
    unity_port_range: tuple[int, int] = Field(
        default=(5555, 5565), description="Unity port range"
    )
    unity_connection_timeout: int = Field(default=30, description="Connection timeout in seconds")

    # AI Model API Keys
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    google_api_key: Optional[str] = Field(default=None, description="Google AI API key")
    groq_api_key: Optional[str] = Field(default=None, description="Groq API key")

    # Asset Generation API Keys
    meshy_api_key: Optional[str] = Field(default=None, description="Meshy API key")
    leonardo_api_key: Optional[str] = Field(default=None, description="Leonardo.ai API key")
    replicate_api_key: Optional[str] = Field(default=None, description="Replicate API key")

    # Default AI Model
    default_model: str = Field(
        default="claude-sonnet-4.5", description="Default AI model"
    )

    # Orchestrator Settings
    orchestrator_enabled: bool = Field(default=True, description="Enable orchestrator mode")
    orchestrator_plan_file: str = Field(
        default="Assets/GamePlan.md", description="Default plan file path"
    )
    orchestrator_auto_retry: bool = Field(
        default=True, description="Auto retry failed tasks"
    )
    orchestrator_max_retries: int = Field(default=3, description="Max retry attempts")

    # Asset Generation Settings
    asset_generation_enabled: bool = Field(default=True, description="Enable asset generation")
    asset_cache_dir: str = Field(
        default="~/.gameos/cache/assets", description="Asset cache directory"
    )
    asset_import_timeout: int = Field(default=300, description="Asset import timeout (seconds)")

    # Pipeline Recording
    pipeline_recording_enabled: bool = Field(
        default=True, description="Enable pipeline recording"
    )
    pipeline_storage_dir: str = Field(
        default="~/.gameos/pipelines", description="Pipeline storage directory"
    )

    # Todo System
    todo_enabled: bool = Field(default=True, description="Enable todo system")
    todo_auto_create: bool = Field(
        default=True, description="Auto-create todos from plan"
    )

    # Telemetry
    telemetry_enabled: bool = Field(default=True, description="Enable anonymous telemetry")
    telemetry_timeout: float = Field(default=5.0, description="Telemetry timeout (seconds)")

    # Development
    debug_mode: bool = Field(default=False, description="Debug mode")

    class Config:
        env_prefix = "GAMEOS_"
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_config_dir() -> Path:
    """Get configuration directory"""
    config_dir = Path.home() / ".gameos"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def load_config() -> GameOSConfig:
    """Load configuration from file or environment"""
    config_file = get_config_dir() / "config.json"

    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            return GameOSConfig(**config_data)
        except Exception as e:
            print(f"Error loading config file: {e}")

    # Load from environment variables
    return GameOSConfig()


def save_config(config: GameOSConfig) -> None:
    """Save configuration to file"""
    config_file = get_config_dir() / "config.json"

    try:
        with open(config_file, 'w') as f:
            json.dump(config.model_dump(), f, indent=2)
    except Exception as e:
        print(f"Error saving config file: {e}")


# Global configuration instance
config = load_config()
