
import logging

import pandas as pd

from transform import (
    add_continent_column,
    add_gender_category,
    add_python_knowledge_column,
    clean_age_first_code,
)


def test_add_gender_category():
    dataframe = pd.DataFrame({
        "Gender": [
            "Man",
            "Woman",
            "Non-binary",
            "Man;Woman",
            None,
            "",
            "   "
        ]
    })

    config = {"etl": {"gender_column": "Gender"}}

    result = add_gender_category(
        dataframe,
        config,
        logging.getLogger("test")
    )

    expected = [
        "MAN",
        "WOMAN",
        "OTHERS",
        "OTHERS",
        pd.NA,
        pd.NA,
        pd.NA
    ]

    pd.testing.assert_series_equal(
        result["GenderCategory"],
        pd.Series(
            expected,
            name="GenderCategory",
            dtype="string"
        )
    )


def test_clean_age_first_code():
    dataframe = pd.DataFrame({
        "Age1stCode": ["15", "18", "Younger than 5", None]
    })

    config = {"etl": {"age_column": "Age1stCode"}}

    result = clean_age_first_code(
        dataframe,
        config,
        logging.getLogger("test")
    )

    assert result["Age1stCode"].iloc[0] == 15.0
    assert result["Age1stCode"].iloc[1] == 18.0
    assert pd.isna(result["Age1stCode"].iloc[2])
    assert pd.isna(result["Age1stCode"].iloc[3])


def test_add_python_knowledge_column():
    dataframe = pd.DataFrame({
        "LanguageWorkedWith": [
            "Python;JavaScript",
            "Java",
            "Python;C++",
            "Python",
            None
        ]
    })

    config = {
        "etl": {
            "worked_languages_column": "LanguageWorkedWith"
        }
    }

    result = add_python_knowledge_column(
        dataframe,
        config,
        logging.getLogger("test")
    )

    assert bool(result["KnowsPython"].iloc[0]) is True
    assert bool(result["KnowsPython"].iloc[1]) is False
    assert bool(result["KnowsPython"].iloc[2]) is True
    assert bool(result["KnowsPython"].iloc[3]) is True
    assert pd.isna(result["KnowsPython"].iloc[4])


def test_add_continent_column():
    dataframe = pd.DataFrame({
        "Country": ["India", "Germany", "Brazil", None]
    })

    config = {"input": {"country_column": "Country"}}

    result = add_continent_column(
        dataframe,
        config,
        logging.getLogger("test")
    )

    assert result["Continent"].iloc[0] == "Asia"
    assert result["Continent"].iloc[1] == "Europe"
    assert result["Continent"].iloc[2] == "South America"
    assert result["Continent"].iloc[3] == "Unknown"
