from email.message import Message
from pathlib import PurePosixPath
from urllib.parse import urlparse

import scrapy
import scrapy.http
from scrapy.pipelines.files import FilesPipeline


class FileNamePipeline(FilesPipeline):
    def file_path(
        self,
        request: scrapy.Request,
        response: scrapy.http.Response = None,
        info=None,
        *,
        item=None
    ):
        if response is not None:
            content_disposition_header = response.headers.get(b'Content-Disposition')
            if content_disposition_header is not None:
                msg = Message()
                msg['content-disposition'] = content_disposition_header
                return msg.get_filename()

        return PurePosixPath(urlparse(request.url).path).name
