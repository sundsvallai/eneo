import asyncio
import os
import shutil
import uuid
from pathlib import Path
from tempfile import SpooledTemporaryFile
from typing import IO

from fastapi import UploadFile

from instorage.info_blobs.file.text import TextMimeTypes
from instorage.main.exceptions import FileNotSupportedException, FileTooLargeException

TMP_DIR = "/tmp/"


class FileService:
    @staticmethod
    async def save_file_to_disk(file: SpooledTemporaryFile):
        destination = os.path.join(TMP_DIR, uuid.uuid4().hex)
        destination_path = Path(destination)

        try:
            with destination_path.open("wb") as buffer:
                await asyncio.to_thread(shutil.copyfileobj, file, buffer)
        finally:
            file.close()

        return destination

    @staticmethod
    def validate_file_types(files: list[UploadFile]):
        for file in files:
            if not TextMimeTypes.has_value(file.content_type):
                raise FileNotSupportedException(
                    f"{file.content_type} files is not supported"
                )

    @staticmethod
    def is_too_large(file: IO, max_size: int):
        real_file_size = 0
        for chunk in file:
            real_file_size += len(chunk)
            if real_file_size > max_size:
                return True

        # return the pointer back to the starting point so that
        # the next read starts from the starting point
        file.seek(0)

        return False

    @staticmethod
    def validate_file_sizes(files: list[UploadFile]):
        FILE_SIZE = 2097152  # 2MB

        real_file_size = 0
        for file in files:
            for chunk in file.file:
                real_file_size += len(chunk)
                if real_file_size > FILE_SIZE:
                    raise FileTooLargeException("File(s) too large")

            # return the pointer back to the starting point so that
            # the next read starts from the starting point
            file.file.seek(0)
