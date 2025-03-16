import logging
import sys
from typing import Optional


class Logger:
    _instance: Optional["Logger"] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._setup_logger()
        return cls._instance

    @classmethod
    def _setup_logger(cls):
        # Create logger
        cls._logger = logging.getLogger("app_logger")
        cls._logger.setLevel(logging.DEBUG)

        # Create console handler and set level
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        # Create file handler and set level
        file_handler = logging.FileHandler("app.log")
        file_handler.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Add formatter to handlers
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to logger
        cls._logger.addHandler(console_handler)
        cls._logger.addHandler(file_handler)

    @classmethod
    def info(cls, message: str):
        if cls._logger is None:
            cls._setup_logger()
        cls._logger.info(message)

    @classmethod
    def error(cls, message: str):
        if cls._logger is None:
            cls._setup_logger()
        cls._logger.error(message)

    @classmethod
    def debug(cls, message: str):
        if cls._logger is None:
            cls._setup_logger()
        cls._logger.debug(message)


# Create singleton instance
logger = Logger()
