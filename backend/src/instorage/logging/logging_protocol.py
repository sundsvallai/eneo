# Copyright (c) 2023 Sundsvalls Kommun
#
# Licensed under the MIT License.

from instorage.logging.logging import LoggingDetailsInDB, LoggingDetailsPublic


def from_domain(logging: LoggingDetailsInDB):
    return LoggingDetailsPublic(**logging.model_dump())
