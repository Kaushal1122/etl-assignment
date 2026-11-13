


MIN_RESPONDENTS_PER_COUNTRY = 10


def calculate_python_percentage(dataframe, config, logger):
    """Calculate Python knowledge percentage by country."""

    country_column = config["input"]["country_column"]

    if country_column not in dataframe.columns:
        raise ValueError(f"Country column not found: {country_column}")

    if "KnowsPython" not in dataframe.columns:
        raise ValueError(
            "KnowsPython column not found. "
            "Run the Python knowledge transformation first."
        )

    logger.info("Calculating Python knowledge percentage by country.")

    valid_data = dataframe.dropna(subset=[country_column, "KnowsPython"])

    report = (
        valid_data.groupby(country_column)
        .agg(
            TotalRespondents=("KnowsPython", "count"),
            PythonDevelopers=("KnowsPython", "sum"),
            PythonPercentage=("KnowsPython", "mean"),
        )
        .reset_index()
    )

    excluded_countries = (
        report["TotalRespondents"] < MIN_RESPONDENTS_PER_COUNTRY
    ).sum()

    report = report[
        report["TotalRespondents"] >= MIN_RESPONDENTS_PER_COUNTRY
    ].copy()

    report["PythonPercentage"] = (report["PythonPercentage"] * 100).round(2)

    report = report.sort_values(
        by="PythonPercentage", ascending=False
    ).reset_index(drop=True)

    logger.info(
        "Excluded %d countries with fewer than %d valid respondents.",
        excluded_countries,
        MIN_RESPONDENTS_PER_COUNTRY,
    )

    logger.info(
        "Python percentage report calculated for %d countries.",
        len(report),
    )

    return report


def calculate_average_salary_by_continent(dataframe, config, logger):
    """Calculate average and median developer salary by continent."""

    salary_column = config["etl"]["compensation_column"]

    if salary_column not in dataframe.columns:
        raise ValueError(f"Salary column not found: {salary_column}")

    if "Continent" not in dataframe.columns:
        raise ValueError(
            "Continent column not found. "
            "Run the continent transformation first."
        )

    logger.info("Calculating average and median salary by continent.")

    valid_data = dataframe.dropna(subset=[salary_column])

    valid_data = valid_data[valid_data["Continent"] != "Unknown"]

    report = (
        valid_data.groupby("Continent")
        .agg(
            TotalRespondents=(salary_column, "count"),
            AverageSalaryUSD=(salary_column, "mean"),
            MedianSalaryUSD=(salary_column, "median"),
        )
        .reset_index()
    )

    report["AverageSalaryUSD"] = report["AverageSalaryUSD"].round(2)
    report["MedianSalaryUSD"] = report["MedianSalaryUSD"].round(2)

    report = report.sort_values(
        by="AverageSalaryUSD", ascending=False
    ).reset_index(drop=True)

    logger.info(
        "Average and median salary report calculated for %d continents.",
        len(report),
    )

    return report


def calculate_most_desired_language(dataframe, config, logger):
    """Calculate the number of respondents desiring each language."""

    language_column = config["etl"]["desired_languages_column"]

    if language_column not in dataframe.columns:
        raise ValueError(
            f"Desired language column not found: {language_column}"
        )

    logger.info("Calculating the most desired programming languages.")

    languages = (
        dataframe[language_column]
        .dropna()
        .str.split(";")
        .explode()
        .str.strip()
    )

    report = (
        languages.value_counts()
        .rename_axis("Language")
        .reset_index(name="Respondents")
    )

    logger.info(
        "Desired language report calculated for %d languages.", len(report)
    )

    return report


def calculate_hobbyist_report(dataframe, config, logger):
    """Count hobby coders by gender and continent."""

    hobbyist_column = config["etl"]["hobbyist_column"]

    required_columns = [hobbyist_column, "GenderCategory", "Continent"]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns missing from dataset: {missing_columns}"
        )

    logger.info("Calculating hobbyist report by gender and continent.")

    valid_data = dataframe[
        (dataframe[hobbyist_column] == "Yes")
        & (dataframe["Continent"] != "Unknown")
    ]

    report = (
        valid_data.groupby(["Continent", "GenderCategory"])
        .size()
        .reset_index(name="HobbyistCount")
    )

    report = report.sort_values(
        by=["Continent", "GenderCategory"]
    ).reset_index(drop=True)

    logger.info("Hobbyist report calculated for %d groups.", len(report))

    return report


def _calculate_satisfaction_report(dataframe, satisfaction_column, logger):
    """Calculate satisfaction counts by gender and continent."""

    required_columns = [satisfaction_column, "GenderCategory", "Continent"]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns missing from dataset: {missing_columns}"
        )

    logger.info("Calculating %s by gender and continent.", satisfaction_column)

    satisfaction_levels = [
        "Very dissatisfied",
        "Slightly dissatisfied",
        "Neither satisfied nor dissatisfied",
        "Slightly satisfied",
        "Very satisfied",
    ]

    valid_data = dataframe[
        dataframe[satisfaction_column].notna()
        & (dataframe["Continent"] != "Unknown")
    ]

    report = (
        valid_data.groupby(
            ["Continent", "GenderCategory", satisfaction_column]
        )
        .size()
        .unstack(fill_value=0)
        .reindex(columns=satisfaction_levels, fill_value=0)
        .reset_index()
    )

    report["TotalRespondents"] = report[satisfaction_levels].sum(axis=1)

    report = report.sort_values(
        by=["Continent", "GenderCategory"]
    ).reset_index(drop=True)

    logger.info(
        "%s report calculated for %d groups.", satisfaction_column, len(report)
    )

    return report


def calculate_job_satisfaction_report(dataframe, config, logger):
    """Calculate job satisfaction by gender and continent."""

    satisfaction_column = config["etl"]["job_satisfaction_column"]

    return _calculate_satisfaction_report(
        dataframe, satisfaction_column, logger
    )


def calculate_career_satisfaction_report(dataframe, config, logger):
    """Calculate career satisfaction by gender and continent."""

    satisfaction_column = config["etl"]["career_satisfaction_column"]

    return _calculate_satisfaction_report(
        dataframe, satisfaction_column, logger
    )
