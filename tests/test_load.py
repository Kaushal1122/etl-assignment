import logging

import pandas as pd
import pytest

from load import save_report

logger = logging.getLogger("test")


def test_save_report_successfully(tmp_path):
    dataframe = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [25, 30]})

    config = {"output": {"directory": str(tmp_path)}}

    output_path = save_report(dataframe, "test_report.csv", config, logger)

    assert output_path.is_file()

    saved_dataframe = pd.read_csv(output_path)

    pd.testing.assert_frame_equal(saved_dataframe, dataframe)


def test_save_report_creates_output_directory(tmp_path):
    output_directory = tmp_path / "reports"

    dataframe = pd.DataFrame({"Name": ["Alice"]})

    config = {"output": {"directory": str(output_directory)}}

    output_path = save_report(dataframe, "test_report.csv", config, logger)

    assert output_directory.is_dir()
    assert output_path.is_file()


def test_save_report_handles_os_error(tmp_path, monkeypatch):
    dataframe = pd.DataFrame({"Name": ["Alice"]})

    config = {"output": {"directory": str(tmp_path)}}

    def mock_to_csv(*args, **kwargs):
        raise OSError("Unable to write file")

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    with pytest.raises(OSError, match="Unable to write file"):
        save_report(dataframe, "test_report.csv", config, logger)
