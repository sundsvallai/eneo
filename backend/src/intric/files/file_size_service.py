import asyncio
import hashlib
import os
import shutil
import uuid
from pathlib import Path
from tempfile import SpooledTemporaryFile
from typing import IO

TMP_DIR = "/tmp/"


class FileSizeService:
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
    def get_file_checksum(filepath: Path):
        """Taken from https://stackoverflow.com/a/44873382"""
        h = hashlib.sha256()
        b = bytearray(128 * 1024)
        mv = memoryview(b)

        with open(filepath, "rb", buffering=0) as f:
            while n := f.readinto(mv):
                h.update(mv[:n])

        return h.hexdigest()
