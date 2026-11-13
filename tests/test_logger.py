import logging

from logger import setup_logger


def test_setup_logger_successfully(tmp_path):
    config = {
        "logging": {
            "directory": str(tmp_path),
            "file_name": "test.log",
            "level": "INFO",
            "format": "%(levelname)s - %(message)s",
        }
    }

    logger = setup_logger(config)

    assert logger.name == "etl_assignment"
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 2

    logger.info("Test log message")

    log_file = tmp_path / "test.log"

    assert log_file.is_file()

    log_content = log_file.read_text(encoding="utf-8")

    assert "Test log message" in log_content

    for handler in logger.handlers:
        handler.close()

    logger.handlers.clear()
