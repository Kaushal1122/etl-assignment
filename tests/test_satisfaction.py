import logging

import pandas as pd

from report import (
    calculate_career_satisfaction_report,
    calculate_job_satisfaction_report,
)

logger = logging.getLogger("test")


def create_sample_dataframe():
    return pd.DataFrame(
        {
            "Continent": [
                "Asia",
                "Asia",
                "Asia",
                "Europe",
                "Europe",
                "Unknown",
            ],
            "GenderCategory": ["MAN", "WOMAN", "MAN", "OTHERS", "MAN", "MAN"],
            "JobSat": [
                "Very satisfied",
                "Slightly satisfied",
                "Very dissatisfied",
                "Neither satisfied nor dissatisfied",
                None,
                "Very satisfied",
            ],
            "CareerSat": [
                "Slightly satisfied",
                "Very satisfied",
                "Neither satisfied nor dissatisfied",
                "Very satisfied",
                "Slightly dissatisfied",
                "Very satisfied",
            ],
        }
    )


def test_calculate_job_satisfaction_report():
    dataframe = create_sample_dataframe()

    config = {"etl": {"job_satisfaction_column": "JobSat"}}

    result = calculate_job_satisfaction_report(dataframe, config, logger)

    asia_man = result[
        (result["Continent"] == "Asia") & (result["GenderCategory"] == "MAN")
    ].iloc[0]

    assert asia_man["Very satisfied"] == 1
    assert asia_man["Very dissatisfied"] == 1
    assert asia_man["TotalRespondents"] == 2

    assert "Unknown" not in result["Continent"].tolist()


def test_calculate_career_satisfaction_report():
    dataframe = create_sample_dataframe()

    config = {"etl": {"career_satisfaction_column": "CareerSat"}}

    result = calculate_career_satisfaction_report(dataframe, config, logger)

    asia_man = result[
        (result["Continent"] == "Asia") & (result["GenderCategory"] == "MAN")
    ].iloc[0]

    assert asia_man["Neither satisfied nor dissatisfied"] == 1
    assert asia_man["TotalRespondents"] == 2

    assert "Unknown" not in result["Continent"].tolist()
