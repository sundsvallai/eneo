from urllib.parse import urlparse

import scrapy
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from intric.crawler.parse_html import parse_file, parse_response


class CrawlSpider(scrapy.spiders.CrawlSpider):
    name = "crawlspider"

    def __init__(
        self,
        url: str,
        *args,
        **kwargs,
    ):
        parsed_uri = urlparse(url)

        self.allowed_domains = [parsed_uri.netloc]
        self.start_urls = [url]

        self.rules = [
            Rule(
                LinkExtractor(allow=url),
                callback=parse_response,
                follow=True,
            ),
            Rule(LinkExtractor(deny_extensions=[]), callback=parse_file),
        ]

        super().__init__(*args, **kwargs)

    def parse_start_url(self, response: Response):
        return parse_response(response)
