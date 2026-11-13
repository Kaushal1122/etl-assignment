import logging

import pandas as pd

from config import load_config
from extract import extract_data
from load import save_report
from logger import setup_logger
from report import (
    calculate_average_salary_by_continent,
    calculate_career_satisfaction_report,
    calculate_hobbyist_report,
    calculate_job_satisfaction_report,
    calculate_most_desired_language,
    calculate_python_percentage,
)
from transform import (
    add_continent_column,
    add_gender_category,
    add_python_knowledge_column,
    clean_age_first_code,
)


def generate_reports(dataframe, config, logger):
    """Generate all reports from the transformed survey data."""

    age_column = config["etl"]["age_column"]

    average_age = dataframe[age_column].mean()

    age_report = pd.DataFrame(
        {"AverageAgeWhenStartedCoding": [round(average_age, 2)]}
    )

    reports = {
        "average_age_first_code.csv": age_report,
        "python_percentage_by_country.csv": calculate_python_percentage(
            dataframe, config, logger
        ),
       "average_salary_by_continent.csv":
            calculate_average_salary_by_continent(
                dataframe, config, logger
            ),
        "most_desired_language.csv": calculate_most_desired_language(
            dataframe, config, logger
        ),
        "hobbyist_by_gender_and_continent.csv": calculate_hobbyist_report(
            dataframe, config, logger
        ),
        "job_satisfaction.csv": calculate_job_satisfaction_report(
            dataframe, config, logger
        ),
        "career_satisfaction.csv": calculate_career_satisfaction_report(
            dataframe, config, logger
        ),
    }

    return reports


def run_pipeline(config, logger):
    """Execute the complete ETL pipeline."""

    logger.info("ETL pipeline started.")

    dataframe = extract_data(config, logger)

    dataframe = add_continent_column(dataframe, config, logger)

    dataframe = clean_age_first_code(dataframe, config, logger)

    dataframe = add_python_knowledge_column(dataframe, config, logger)

    dataframe = add_gender_category(dataframe, config, logger)

    logger.info("All transformations completed.")

    reports = generate_reports(dataframe, config, logger)

    for file_name, report in reports.items():
        save_report(report, file_name, config, logger)

    logger.info("ETL pipeline completed. Generated %d reports.", len(reports))


def main():
    """Load configuration and start the ETL pipeline."""

    try:
        config = load_config()
        logger = setup_logger(config)

        run_pipeline(config, logger)

    except Exception:
        logging.exception("ETL pipeline failed.")
        raise


if __name__ == "__main__":
    main()
