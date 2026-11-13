
import logging

import pandas as pd

from report import (
    calculate_average_salary_by_continent,
    calculate_hobbyist_report,
    calculate_most_desired_language,
    calculate_python_percentage,
)

logger = logging.getLogger("test")


def test_calculate_python_percentage():
    dataframe = pd.DataFrame({
        "Country": (
            ["India"] * 10
            + ["Germany"] * 9
            + ["Brazil"] * 12
        ),
        "KnowsPython": (
            [True] * 7 + [False] * 3
            + [True] * 5 + [False] * 4
            + [True] * 6 + [False] * 6
        ),
    })

    config = {"input": {"country_column": "Country"}}

    result = calculate_python_percentage(dataframe, config, logger)

    assert "India" in result["Country"].values
    assert "Brazil" in result["Country"].values
    assert "Germany" not in result["Country"].values

    india = result[result["Country"] == "India"].iloc[0]
    brazil = result[result["Country"] == "Brazil"].iloc[0]

    assert india["TotalRespondents"] == 10
    assert india["PythonDevelopers"] == 7
    assert india["PythonPercentage"] == 70.0

    assert brazil["TotalRespondents"] == 12
    assert brazil["PythonDevelopers"] == 6
    assert brazil["PythonPercentage"] == 50.0



def test_calculate_average_salary_by_continent():
    dataframe = pd.DataFrame({
        "ConvertedComp": [100000, 120000, 80000, None],
        "Continent": ["Asia", "Asia", "Europe", "Unknown"],
    })

    config = {"etl": {"compensation_column": "ConvertedComp"}}

    result = calculate_average_salary_by_continent(
        dataframe, config, logger
    )

    asia = result[result["Continent"] == "Asia"].iloc[0]
    europe = result[result["Continent"] == "Europe"].iloc[0]

    assert asia["AverageSalaryUSD"] == 110000
    assert asia["MedianSalaryUSD"] == 110000
    assert asia["TotalRespondents"] == 2

    assert europe["AverageSalaryUSD"] == 80000
    assert europe["MedianSalaryUSD"] == 80000
    assert "Unknown" not in result["Continent"].values



def test_calculate_most_desired_language():
    dataframe = pd.DataFrame({
        "LanguageDesireNextYear": [
            "Python;JavaScript",
            "Python;Java",
            "JavaScript;Python",
            None,
        ]
    })

    config = {
        "etl": {
            "desired_languages_column": "LanguageDesireNextYear"
        }
    }

    result = calculate_most_desired_language(
        dataframe, config, logger
    )

    python_count = result[
        result["Language"] == "Python"
    ]["Respondents"].iloc[0]

    assert python_count == 3


def test_calculate_hobbyist_report():
    dataframe = pd.DataFrame({
        "Hobbyist": ["Yes", "Yes", "No", "Yes"],
        "GenderCategory": ["MAN", "WOMAN", "MAN", "OTHERS"],
        "Continent": ["Asia", "Asia", "Europe", "Europe"],
    })

    config = {"etl": {"hobbyist_column": "Hobbyist"}}

    result = calculate_hobbyist_report(dataframe, config, logger)

    assert len(result) == 3
    assert result["HobbyistCount"].sum() == 3
