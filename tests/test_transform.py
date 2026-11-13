import logging

import pandas as pd

from transform import (
    add_continent_column,
    add_gender_category,
    add_python_knowledge_column,
    clean_age_first_code,
)


def test_add_gender_category():
    dataframe = pd.DataFrame(
        {"Gender": ["Man", "Woman", "Non-binary", "Man;Woman", None]}
    )

    config = {"etl": {"gender_column": "Gender"}}

    result = add_gender_category(dataframe, config, logging.getLogger("test"))

    expected = ["MAN", "WOMAN", "OTHERS", "OTHERS", "OTHERS"]

    assert result["GenderCategory"].tolist() == expected


def test_clean_age_first_code():
    dataframe = pd.DataFrame(
        {
            "Age1stCode": [
                "15",
                "18",
                "Younger than 5 years",
                "Older than 85",
                None,
            ]
        }
    )

    config = {"etl": {"age_column": "Age1stCode"}}

    result = clean_age_first_code(dataframe, config, logging.getLogger("test"))

    assert result["Age1stCode"].iloc[:2].tolist() == [15.0, 18.0]

    assert result["Age1stCode"].iloc[2:].isna().all()


def test_add_python_knowledge_column():
    dataframe = pd.DataFrame(
        {
            "LanguageWorkedWith": [
                "Python;Java",
                "Java;C++",
                "Python",
                "JavaScript;Python",
                None,
            ]
        }
    )

    config = {"etl": {"worked_languages_column": "LanguageWorkedWith"}}

    result = add_python_knowledge_column(
        dataframe, config, logging.getLogger("test")
    )

    assert result["KnowsPython"].tolist()[:4] == [True, False, True, True]

    assert pd.isna(result["KnowsPython"].iloc[4])


def test_add_continent_column():
    dataframe = pd.DataFrame({"Country": ["India", "Germany", "Brazil", None]})

    config = {"input": {"country_column": "Country"}}

    result = add_continent_column(dataframe, config, logging.getLogger("test"))

    expected = ["Asia", "Europe", "South America", "Unknown"]

    assert result["Continent"].tolist() == expected
