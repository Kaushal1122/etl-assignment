from config import PROJECT_ROOT


def save_report(report, file_name, config, logger):
    """Save a report DataFrame as a CSV file."""

    output_directory = PROJECT_ROOT / config["output"]["directory"]

    output_directory.mkdir(parents=True, exist_ok=True)

    output_path = output_directory / file_name

    try:
        report.to_csv(output_path, index=False, encoding="utf-8")

    except OSError:
        logger.exception("Unable to save report: %s", output_path)
        raise

    logger.info("Report saved successfully: %s", output_path)

    return output_path
