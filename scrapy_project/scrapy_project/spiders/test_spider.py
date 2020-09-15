# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TestSpider(scrapy.Spider):
    name = 'test_spider'

    def __init__(self, *args, **kwargs):
        super(TestSpider, self).__init__(*args, **kwargs)
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            }

        next_page_url = response.xpath(
            '//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))


# To test spider from CLI
# class TestSpider(scrapy.Spider):
#     name = 'test_spider'
#     start_urls = [
#         'http://quotes.toscrape.com/',
#     ]

#     def parse(self, response):
#         for quote in response.xpath('//div[@class="quote"]'):
#             yield {
#                 'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
#                 'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
#                 'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
#             }

#         next_page_url = response.xpath(
#             '//li[@class="next"]/a/@href').extract_first()
#         if next_page_url is not None:
#             yield scrapy.Request(response.urljoin(next_page_url))
