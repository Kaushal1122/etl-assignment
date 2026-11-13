import logging

import pandas as pd
import pytest

import main

logger = logging.getLogger("test")


def create_sample_dataframe():
    return pd.DataFrame(
        {
            "Country": ["India", "Germany"],
            "Age1stCode": [15.0, 18.0],
            "LanguageWorkedWith": ["Python;Java", "Java;C++"],
            "LanguageDesireNextYear": ["Python;JavaScript", "Python;C++"],
            "ConvertedComp": [50000, 60000],
            "Hobbyist": ["Yes", "No"],
            "Gender": ["Man", "Woman"],
            "JobSat": ["Very satisfied", "Slightly satisfied"],
            "CareerSat": ["Very satisfied", "Slightly satisfied"],
            "Continent": ["Asia", "Europe"],
            "KnowsPython": [True, False],
            "GenderCategory": ["MAN", "WOMAN"],
        }
    )


def create_config():
    return {
        "input": {"country_column": "Country"},
        "etl": {
            "age_column": "Age1stCode",
            "compensation_column": "ConvertedComp",
            "worked_languages_column": "LanguageWorkedWith",
            "desired_languages_column": "LanguageDesireNextYear",
            "hobbyist_column": "Hobbyist",
            "gender_column": "Gender",
            "job_satisfaction_column": "JobSat",
            "career_satisfaction_column": "CareerSat",
        },
        "output": {"directory": "reports"},
    }


def test_generate_reports():
    dataframe = create_sample_dataframe()
    config = create_config()

    reports = main.generate_reports(dataframe, config, logger)

    assert len(reports) == 7

    expected_files = {
        "average_age_first_code.csv",
        "python_percentage_by_country.csv",
        "average_salary_by_continent.csv",
        "most_desired_language.csv",
        "hobbyist_by_gender_and_continent.csv",
        "job_satisfaction.csv",
        "career_satisfaction.csv",
    }

    assert set(reports.keys()) == expected_files

    age_report = reports["average_age_first_code.csv"]

    assert age_report["AverageAgeWhenStartedCoding"].iloc[0] == 16.5


def test_run_pipeline(monkeypatch):
    config = create_config()
    dataframe = create_sample_dataframe()

    saved_reports = []

    monkeypatch.setattr(main, "extract_data", lambda config, logger: dataframe)

    monkeypatch.setattr(
        main,
        "add_continent_column",
        lambda dataframe, config, logger: dataframe,
    )

    monkeypatch.setattr(
        main,
        "clean_age_first_code",
        lambda dataframe, config, logger: dataframe,
    )

    monkeypatch.setattr(
        main,
        "add_python_knowledge_column",
        lambda dataframe, config, logger: dataframe,
    )

    monkeypatch.setattr(
        main,
        "add_gender_category",
        lambda dataframe, config, logger: dataframe,
    )

    def mock_save_report(report, file_name, config, logger):
        saved_reports.append(file_name)

    monkeypatch.setattr(main, "save_report", mock_save_report)

    main.run_pipeline(config, logger)

    assert len(saved_reports) == 7


def test_main_successfully(monkeypatch):
    config = create_config()

    monkeypatch.setattr(main, "load_config", lambda: config)

    monkeypatch.setattr(main, "setup_logger", lambda config: logger)

    pipeline_called = []

    def mock_run_pipeline(config, logger):
        pipeline_called.append(True)

    monkeypatch.setattr(main, "run_pipeline", mock_run_pipeline)

    main.main()

    assert pipeline_called == [True]


def test_main_handles_pipeline_error(monkeypatch):
    monkeypatch.setattr(main, "load_config", lambda: create_config())

    monkeypatch.setattr(main, "setup_logger", lambda config: logger)

    def mock_run_pipeline(config, logger):
        raise RuntimeError("Pipeline failed")

    monkeypatch.setattr(main, "run_pipeline", mock_run_pipeline)

    with pytest.raises(RuntimeError, match="Pipeline failed"):
        main.main()
