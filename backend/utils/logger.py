"""
Simple logging configuration
"""
import logging
import sys
from config import settings


def setup_logger(name: str = __name__) -> logging.Logger:
    """Setup logger with consistent formatting"""
    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(settings.log_level)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# Default logger
logger = setup_logger("skyro")
