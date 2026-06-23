import logging
import sys

from src.core.infrastructure.config.settings import settings


def setup_logging() -> None:
    """
    Configures the standard logging for the application.
    """

    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance with the given name.
    """

    return logging.getLogger(name)
