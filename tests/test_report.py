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
    dataframe = pd.DataFrame(
        {
            "Country": ["India", "India", "India", "Germany", "Germany"],
            "KnowsPython": [True, False, True, True, False],
        }
    )

    config = {"input": {"country_column": "Country"}}

    result = calculate_python_percentage(dataframe, config, logger)

    india = result[result["Country"] == "India"].iloc[0]
    germany = result[result["Country"] == "Germany"].iloc[0]

    assert india["TotalRespondents"] == 3
    assert india["PythonDevelopers"] == 2
    assert india["PythonPercentage"] == 66.67

    assert germany["TotalRespondents"] == 2
    assert germany["PythonDevelopers"] == 1
    assert germany["PythonPercentage"] == 50.0


def test_calculate_average_salary_by_continent():
    dataframe = pd.DataFrame(
        {
            "ConvertedComp": [50000, 70000, 40000, None],
            "Continent": ["Asia", "Asia", "Europe", "Unknown"],
        }
    )

    config = {"etl": {"compensation_column": "ConvertedComp"}}

    result = calculate_average_salary_by_continent(dataframe, config, logger)

    asia = result[result["Continent"] == "Asia"].iloc[0]
    europe = result[result["Continent"] == "Europe"].iloc[0]

    assert asia["TotalRespondents"] == 2
    assert asia["AverageSalaryUSD"] == 60000.0

    assert europe["TotalRespondents"] == 1
    assert europe["AverageSalaryUSD"] == 40000.0

    assert "Unknown" not in result["Continent"].tolist()


def test_calculate_most_desired_language():
    dataframe = pd.DataFrame(
        {
            "LanguageDesireNextYear": [
                "Python;Java",
                "Python;C++",
                "Java;C++",
                None,
            ]
        }
    )

    config = {"etl": {"desired_languages_column": "LanguageDesireNextYear"}}

    result = calculate_most_desired_language(dataframe, config, logger)

    language_counts = dict(
        zip(result["Language"], result["Respondents"], strict=True)
    )

    assert language_counts["Python"] == 2
    assert language_counts["Java"] == 2
    assert language_counts["C++"] == 2
    assert len(result) == 3


def test_calculate_hobbyist_report():
    dataframe = pd.DataFrame(
        {
            "Hobbyist": ["Yes", "Yes", "No", "Yes", "Yes"],
            "GenderCategory": ["MAN", "WOMAN", "MAN", "OTHERS", "MAN"],
            "Continent": ["Asia", "Asia", "Asia", "Europe", "Unknown"],
        }
    )

    config = {"etl": {"hobbyist_column": "Hobbyist"}}

    result = calculate_hobbyist_report(dataframe, config, logger)

    asia_man = result[
        (result["Continent"] == "Asia") & (result["GenderCategory"] == "MAN")
    ].iloc[0]

    asia_woman = result[
        (result["Continent"] == "Asia") & (result["GenderCategory"] == "WOMAN")
    ].iloc[0]

    europe_others = result[
        (result["Continent"] == "Europe")
        & (result["GenderCategory"] == "OTHERS")
    ].iloc[0]

    assert asia_man["HobbyistCount"] == 1
    assert asia_woman["HobbyistCount"] == 1
    assert europe_others["HobbyistCount"] == 1

    assert "Unknown" not in result["Continent"].tolist()
