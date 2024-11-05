# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

from pathlib import Path

from instorage.files.text import MimeTypesBase
from instorage.main.exceptions import FileNotSupportedException


class ImageMimeTypes(MimeTypesBase):
    PNG = "image/png"
    JPEG = "image/jpeg"


class ImageExtractor:
    @staticmethod
    def extract_from_image(filepath: Path) -> str:
        with open(filepath, "rb") as image_file:
            return image_file.read()

    def extract(self, filepath: Path, mimetype: str) -> bytearray:
        if ImageMimeTypes.has_value(mimetype):
            return self.extract_from_image(filepath)
        raise FileNotSupportedException(f"{mimetype} files is not supported")
