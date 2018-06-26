from scrapy.spider import CrawlSpider, Rule, Spider
from scrapy.selector import Selector, HtmlXPathSelector
from googletrans import Translator
from unidecode import unidecode
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import datetime
from dateutil import parser
# from .items import NewsItem
import scrapy
import os

from ..items import NewsDetailItem
from crawler_engine.models import NewsDetail
from .csv_helper import get_csv_file,get_specified_columns
MAX_PAGE = 10


class SnopesSpider(Spider):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    name = 'snopes'
    crawledLinks = []
    received = []

    def check_already_crawled_url(self, response):
        url = response.url
        url_crawled_list = NewsDetail.objects.all().values_list('url', flat=True)
        # if ()
        if url in url_crawled_list:
            return False

        return True

    def start_requests(self):
        data = get_csv_file(self.BASE_DIR + '/snopes.csv')
        urls = get_specified_columns(data,[0,3])

        # with get_csv_file('spiders/politifact.csv', 'rt') as f:
        #     list = []
        #     for line in f.readlines():
        #         array = line.split(',')
        #         url = array[0]
        #         list.append(url)
        #     list.pop(0)
        i=0
        for url in urls:
            label = url[1].strip().upper()
            if label == 'true'.upper() or label == 'false'.upper():
                i+=1
                print('step ',i)
                yield scrapy.Request(url=url[0], callback=self.parse, meta={'label':1 if label == 'true'.upper() else 0,'step':i})


    def parse(self, response):
        translator = Translator()
        if response.status !=200:
            print('response error');
        if not self.check_already_crawled_url(response):
            return None
        if response.url in self.crawledLinks:
            return None
        self.crawledLinks.append(response.url)

        hxs = Selector(response)

        item = NewsDetailItem()
        # base_url, url, title, top_image_url, details, authors, category, keywords, published_date, status, crawled, created_at, updated_at
        item['base_url'] = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(response.url))

        item['url'] = response.url

        item['title'] = ''.join(hxs.select('//h1[@class="article-title"]/text()').extract()).strip()

        # print().extract()).strip())

        top_img_url = ''

        # if (hxs.select('//div[@class="pswp-content__image"]//img')):
        #     top_img_url = hxs.select('//div[@class="pswp-content__image"]//img/@src')[0].extract()
        item['top_image_url'] = top_img_url

        item['details'] = ''.join(hxs.select('//div[@class="article__text"]//p/text()').extract()).strip() + '\n'

        item['authors'] = ''
            # ''.join(
            # hxs.select('//div[@class="details__author__meta" and position()=1]//text()').extract()).strip() + '\n'

        item['category'] = ''
            # unidecode(
            # ''.join(hxs.select('//meta[@property="article:section"]/@content').extract()).strip())

        item['keywords'] =''
            # ''.join(hxs.select('//meta[@name="keywords"]/@content').extract()).strip()

        item['published_date'] = parser.parse('2018-06-24T06:00:00T+07:00')
            # parser.parse(
            # ''.join(hxs.select('//meta[@itemprop="datePublished"]/@content').extract()).strip())

        item['status'] = 1

        self.received.append(response.meta["step"])
        print('received hihi', self.received)

        # if not item['details'].strip():
        #     return None
        # return item

