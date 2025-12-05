"""
Configuration loading and validation.
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv


class ConfigError(Exception):
    """Configuration error."""
    pass


def load_config(config_path: str = 'config/config.yaml') -> dict:
    """
    Load configuration from YAML and .env files.

    Args:
        config_path: Path to config.yaml file

    Returns:
        Configuration dictionary

    Raises:
        ConfigError: If configuration is invalid
    """
    # Load .env file (look in config/ folder)
    env_path = Path('config/.env')
    if env_path.exists():
        load_dotenv(env_path)

    # Load YAML configuration
    config_file = Path(config_path)
    if not config_file.exists():
        raise ConfigError(f"Config file not found: {config_path}")

    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # Validate configuration
    validate_config(config)

    return config


def validate_config(config: dict):
    """
    Validate configuration has required sections.

    Args:
        config: Configuration dictionary

    Raises:
        ConfigError: If configuration is invalid
    """
    required_sections = ['folders', 'ai', 'processing', 'excel', 'logging']

    for section in required_sections:
        if section not in config:
            raise ConfigError(f"Missing config section: {section}")

    # Check API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ConfigError(
            "ANTHROPIC_API_KEY not set in environment.\n"
            "Please create config/.env file with: ANTHROPIC_API_KEY=sk-ant-your-key-here"
        )

    if not api_key.startswith('sk-ant-'):
        raise ConfigError(
            "Invalid ANTHROPIC_API_KEY format. "
            "Should start with 'sk-ant-'"
        )
