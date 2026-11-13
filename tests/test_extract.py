import logging

import pandas as pd
import pytest

from extract import extract_data

logger = logging.getLogger("test")


def create_config(file_path):
    return {
        "input": {"file_path": str(file_path), "country_column": "Country"},
        "etl": {"age_column": "Age1stCode", "gender_column": "Gender"},
    }


def test_extract_data_successfully(tmp_path):
    file_path = tmp_path / "survey.csv"

    dataframe = pd.DataFrame(
        {
            "Country": ["India", "Germany"],
            "Age1stCode": ["15", "18"],
            "Gender": ["Man", "Woman"],
        }
    )

    dataframe.to_csv(file_path, index=False)

    config = create_config(file_path)

    result = extract_data(config, logger)

    assert len(result) == 2
    assert list(result.columns) == ["Country", "Age1stCode", "Gender"]


def test_extract_data_file_not_found(tmp_path):
    file_path = tmp_path / "missing.csv"

    config = create_config(file_path)

    with pytest.raises(FileNotFoundError):
        extract_data(config, logger)


def test_extract_data_missing_columns(tmp_path):
    file_path = tmp_path / "survey.csv"

    dataframe = pd.DataFrame({"Country": ["India"], "Age1stCode": ["15"]})

    dataframe.to_csv(file_path, index=False)

    config = create_config(file_path)

    with pytest.raises(ValueError, match="Gender"):
        extract_data(config, logger)


def test_extract_data_empty_file(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8")

    config = create_config(file_path)

    with pytest.raises(ValueError, match="empty"):
        extract_data(config, logger)


def test_extract_data_invalid_csv(tmp_path, monkeypatch):
    file_path = tmp_path / "survey.csv"
    file_path.write_text("Country,Age\nIndia,15", encoding="utf-8")

    config = create_config(file_path)

    def mock_read_csv(*args, **kwargs):
        raise pd.errors.ParserError("Invalid CSV")

    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    with pytest.raises(ValueError, match="Invalid CSV"):
        extract_data(config, logger)


def test_extract_data_invalid_encoding(tmp_path, monkeypatch):
    file_path = tmp_path / "survey.csv"
    file_path.write_text("Country,Age\nIndia,15", encoding="utf-8")

    config = create_config(file_path)

    def mock_read_csv(*args, **kwargs):
        raise UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte")

    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    with pytest.raises(ValueError, match="encoding"):
        extract_data(config, logger)
