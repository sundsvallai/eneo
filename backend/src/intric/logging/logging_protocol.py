# MIT License

from intric.logging.logging import LoggingDetailsInDB, LoggingDetailsPublic


def from_domain(logging: LoggingDetailsInDB):
    return LoggingDetailsPublic(**logging.model_dump())
