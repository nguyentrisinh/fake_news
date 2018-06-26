from scrapy.spider import CrawlSpider, Rule, Spider
from scrapy.selector import Selector, HtmlXPathSelector
from unidecode import unidecode
from googletrans import Translator
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import datetime
from dateutil import parser
# from .items import NewsItem
import scrapy
from ..items import NewsDetailItem
from crawler_engine.models import NewsDetail
from .csv_helper import get_csv_file, get_specified_columns

MAX_PAGE = 10


class PolitifactSpider(Spider):
    name = 'politifact'
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
        # data = get_csv_file('spiders/politifact.csv')
        data = get_csv_file('spiders/politifact.csv')
        urls = get_specified_columns(data, [0, 4])

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
                i += 1
                print('step ', i)
                yield scrapy.Request(
                    url=url[0],
                    callback=self.parse, meta={'label': 1 if label == 'true'.upper() else 0, 'step': i}
                )

    def parse(self, response):
        if response.status != 200:
            print('response error')

        if not self.check_already_crawled_url(response):
            return None
        if response.url in self.crawledLinks:
            return None
        self.crawledLinks.append(response.url)

        hxs = Selector(response)

        item = NewsDetailItem()
        # base_url, url, title, top_image_url, details, authors, category,
        # keywords, published_date, status, crawled, created_at, updated_at
        item['base_url'] = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(response.url))

        item['url'] = response.url

        item['title'] = ''.join(hxs.select('//h1[@class="article__title"]/text()').extract()).strip()

        # print().extract()).strip())

        top_img_url = ''

        # if (hxs.select('//div[@class="pswp-content__image"]//img')):
        #     top_img_url = hxs.select('//div[@class="pswp-content__image"]//img/@src')[0].extract()
        item['top_image_url'] = top_img_url
        translator1 = Translator()
        translator2 = Translator()
        translator3 = Translator()
        details = ''.join(hxs.select('//div[@class="article__text"]//p/text()').extract()).strip() + '\n'
        details_list = details.split()
        range = int(len(details_list) / 3)

        firstpartlist, secondpartlist, thirdpartlist = details_list[:range], details_list[range:range*2], details_list[range*2: len(details_list)]

        translated_text1 = translator1.translate(' '.join(x for x in firstpartlist), dest='vi').text
        translated_text2 = translator2.translate(' '.join(x for x in firstpartlist), dest='vi').text
        translated_text3 = translator3.translate(' '.join(x for x in firstpartlist), dest='vi').text
        item['details'] = translated_text1 + ' ' + translated_text2+ ' '+translated_text3
        # item['details'] = ''.join(hxs.select('//div[@class="article__text"]//p/text()').extract()).strip() + '\n'

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
        print('received hihi',self.received)

        if not item['details'].strip():
            return None
        return item

