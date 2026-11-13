import country_converter as coco
import pandas as pd


def add_continent_column(dataframe, config, logger):
    """Add a continent column using country names."""

    country_column = config["input"]["country_column"]

    if country_column not in dataframe.columns:
        raise ValueError(f"Country column not found: {country_column}")

    logger.info("Starting country-to-continent mapping.")

    transformed_data = dataframe.copy()

    countries = (
        transformed_data[country_column].dropna().astype(str).unique().tolist()
    )

    converter = coco.CountryConverter()

    continents = converter.convert(
        names=countries, to="continent_7", not_found="Unknown"
    )

    country_mapping = dict(zip(countries, continents, strict=True))

    transformed_data["Continent"] = (
        transformed_data[country_column]
        .astype("string")
        .map(country_mapping)
        .fillna("Unknown")
    )

    unknown_count = (transformed_data["Continent"] == "Unknown").sum()

    logger.info("Country-to-continent mapping completed.")
    logger.info("Unknown or missing countries: %d", unknown_count)

    return transformed_data


def clean_age_first_code(dataframe, config, logger):
    """Convert first-code age responses into numeric values."""

    age_column = config["etl"]["age_column"]

    if age_column not in dataframe.columns:
        raise ValueError(f"Age column not found: {age_column}")

    logger.info("Starting age column cleaning.")

    transformed_data = dataframe.copy()

    numeric_ages = pd.to_numeric(transformed_data[age_column], errors="coerce")

    non_numeric_count = (
        transformed_data[age_column].notna() & numeric_ages.isna()
    ).sum()

    transformed_data[age_column] = numeric_ages

    logger.info("Age column cleaning completed.")
    logger.info(
        "Non-numeric age responses converted to missing: %d", non_numeric_count
    )

    return transformed_data


def add_python_knowledge_column(dataframe, config, logger):
    """Identify respondents who reported working with Python."""

    language_column = config["etl"]["worked_languages_column"]

    if language_column not in dataframe.columns:
        raise ValueError(f"Language column not found: {language_column}")

    logger.info("Starting Python knowledge identification.")

    transformed_data = dataframe.copy()

    def knows_python(languages):
        if pd.isna(languages):
            return pd.NA

        return "Python" in languages.split(";")

    transformed_data["KnowsPython"] = (
        transformed_data[language_column].apply(knows_python).astype("boolean")
    )

    logger.info("Python knowledge identification completed.")

    return transformed_data


def add_gender_category(dataframe, config, logger):
    """Classify gender responses into three categories."""

    gender_column = config["etl"]["gender_column"]

    if gender_column not in dataframe.columns:
        raise ValueError(f"Gender column not found: {gender_column}")

    logger.info("Starting gender classification.")

    transformed_data = dataframe.copy()

    gender_mapping = {"Man": "MAN", "Woman": "WOMAN"}

    transformed_data["GenderCategory"] = (
        transformed_data[gender_column].map(gender_mapping).fillna("OTHERS")
    )

    logger.info("Gender classification completed.")

    logger.info(
        "Gender category counts: %s",
        transformed_data["GenderCategory"].value_counts().to_dict(),
    )

    return transformed_data
