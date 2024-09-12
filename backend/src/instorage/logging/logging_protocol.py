# MIT License

from instorage.logging.logging import LoggingDetailsInDB, LoggingDetailsPublic


def from_domain(logging: LoggingDetailsInDB):
    return LoggingDetailsPublic(**logging.model_dump())
