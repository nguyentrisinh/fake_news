# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider

from ..items import StartupModelItem


class ExampleSpider(BaseSpider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = ['http://www.example.com/']

    def parse(self, response):
        # do stuff
        return StartupModelItem(name='rolando')
