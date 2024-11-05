# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

import os
from pathlib import Path

from fastapi import UploadFile

from instorage.files.file_models import FileBase, FileType
from instorage.files.file_size_service import FileSizeService
from instorage.files.image import ImageExtractor, ImageMimeTypes
from instorage.files.text import TextExtractor
from instorage.main.config import get_settings
from instorage.main.exceptions import FileTooLargeException


class FileProtocol:
    def __init__(
        self,
        file_size_service: FileSizeService,
        text_extractor: TextExtractor,
        image_extractor: ImageExtractor,
    ):
        self.file_size_service = file_size_service
        self.text_extractor = text_extractor
        self.image_extractor = image_extractor

    async def text_to_domain(self, upload_file: UploadFile):
        if self.file_size_service.is_too_large(
            upload_file.file,
            max_size=get_settings().upload_file_to_session_max_size,
        ):
            raise FileTooLargeException()

        filepath = await self.file_size_service.save_file_to_disk(upload_file.file)
        filepath = Path(filepath)
        try:
            content = self.text_extractor.extract(filepath, upload_file.content_type)
            checksum = self.file_size_service.get_file_checksum(filepath)
            size = len(content.encode("utf-8"))

            return FileBase(
                name=upload_file.filename,
                text=content,
                checksum=checksum,
                size=size,
                file_type=FileType.TEXT,
                mimetype=upload_file.content_type,
            )
        finally:
            os.remove(filepath)

    async def image_to_domain(self, upload_file: UploadFile):
        if self.file_size_service.is_too_large(
            upload_file.file,
            max_size=get_settings().upload_image_to_session_max_size,
        ):
            raise FileTooLargeException()

        filepath = await self.file_size_service.save_file_to_disk(upload_file.file)
        filepath = Path(filepath)
        try:
            content = self.image_extractor.extract(filepath, upload_file.content_type)
            checksum = self.file_size_service.get_file_checksum(filepath)
            size = len(content)

            return FileBase(
                name=upload_file.filename,
                image=content,
                checksum=checksum,
                size=size,
                file_type=FileType.IMAGE,
                mimetype=upload_file.content_type,
            )
        finally:
            os.remove(filepath)

    async def to_domain(self, upload_file: UploadFile):
        if ImageMimeTypes.has_value(upload_file.content_type):
            return await self.image_to_domain(upload_file)
        return await self.text_to_domain(upload_file)
