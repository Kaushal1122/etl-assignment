import logging
from pathlib import Path


def setup_logger(config):
    """Configure and return the application logger."""

    logging_config = config["logging"]

    log_directory = Path(logging_config["directory"])
    log_directory.mkdir(parents=True, exist_ok=True)

    log_file = log_directory / logging_config["file_name"]

    logger = logging.getLogger("etl_assignment")
    logger.setLevel(getattr(logging, logging_config["level"].upper()))

    logger.handlers.clear()

    formatter = logging.Formatter(logging_config["format"])

    file_handler = logging.FileHandler(log_file, encoding="utf-8")

    console_handler = logging.StreamHandler()

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
