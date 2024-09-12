import logging
from logging import Logger

from instorage.main.config import get_loglevel


def _set_log_level(logger: Logger, log_level: int):
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)


def get_logger(module_name: str):
    # If we don't add a handler manually one will be created for us
    logger = logging.getLogger(module_name)
    _set_log_level(logger, get_loglevel())

    return logger


def set_log_level(logger_name: str, log_level: int):
    logger = logging.getLogger(logger_name)
    logger.propagate = False
    _set_log_level(logger=logger, log_level=log_level)
