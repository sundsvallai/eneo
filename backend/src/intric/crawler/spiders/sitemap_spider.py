import scrapy
from scrapy.http import Response

from intric.crawler.parse_html import parse_response


class SitemapSpider(scrapy.spiders.SitemapSpider):
    name = "sitemapspider"

    def __init__(self, sitemap_url: str, *args, **kwargs):
        self.sitemap_urls = [sitemap_url]

        super().__init__(*args, **kwargs)

    def parse(self, response: Response):
        return parse_response(response)
