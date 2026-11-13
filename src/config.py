from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config.yaml"


def load_config(config_path=DEFAULT_CONFIG_PATH):
    """Load and validate the application configuration."""

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with config_path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

    except yaml.YAMLError as error:
        raise ValueError(f"Invalid YAML configuration: {error}") from error

    if not isinstance(config, dict):
        raise ValueError("Configuration must contain a YAML mapping.")

    required_sections = ["input", "output", "logging", "etl"]

    for section in required_sections:
        if section not in config or not isinstance(config[section], dict):
            raise ValueError(
                f"Missing or invalid configuration section: {section}"
            )

    required_input_keys = ["file_path", "country_column"]

    for key in required_input_keys:
        if key not in config["input"]:
            raise ValueError(f"Missing input configuration: {key}")

    return config
