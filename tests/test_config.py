import pytest
import yaml

from config import load_config


def test_load_config_successfully(tmp_path):
    config_path = tmp_path / "config.yaml"

    config_data = {
        "input": {"file_path": "data/survey.csv", "country_column": "Country"},
        "output": {"directory": "reports"},
        "logging": {"directory": "logs"},
        "etl": {"age_column": "Age1stCode"},
    }

    with config_path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(config_data, file)

    result = load_config(config_path)

    assert result == config_data


def test_load_config_file_not_found(tmp_path):
    config_path = tmp_path / "missing.yaml"

    with pytest.raises(FileNotFoundError):
        load_config(config_path)


def test_load_config_invalid_yaml(tmp_path):
    config_path = tmp_path / "invalid.yaml"
    config_path.write_text("input: [invalid", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid YAML"):
        load_config(config_path)


def test_load_config_missing_section(tmp_path):
    config_path = tmp_path / "config.yaml"

    config_data = {
        "input": {"file_path": "data/survey.csv", "country_column": "Country"}
    }

    with config_path.open("w", encoding="utf-8") as file:
        yaml.safe_dump(config_data, file)

    with pytest.raises(ValueError, match="output"):
        load_config(config_path)
