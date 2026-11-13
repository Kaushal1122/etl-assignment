import pandas as pd

from config import PROJECT_ROOT


def extract_data(config, logger):
    """Extract survey data from the configured CSV file."""

    file_path = PROJECT_ROOT / config["input"]["file_path"]

    logger.info("Starting data extraction.")

    if not file_path.is_file():
        raise FileNotFoundError(f"Survey dataset not found: {file_path}")

    try:
        dataframe = pd.read_csv(file_path, low_memory=False, encoding="utf-8")

    except pd.errors.EmptyDataError as error:
        logger.exception("The input CSV file is empty.")
        raise ValueError("Input CSV file is empty.") from error

    except pd.errors.ParserError as error:
        logger.exception("Unable to parse the input CSV file.")
        raise ValueError("Invalid CSV file format.") from error

    except UnicodeDecodeError as error:
        logger.exception("Unable to decode the input CSV file.")
        raise ValueError("Unsupported CSV file encoding.") from error

    required_columns = list(config["etl"].values())
    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns missing from dataset: {missing_columns}"
        )

    logger.info(
        "Data extraction completed. Rows: %d, Columns: %d",
        dataframe.shape[0],
        dataframe.shape[1],
    )

    return dataframe
