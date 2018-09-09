from scrapy.spider import CrawlSpider, Rule, BaseSpider
from scrapy.selector import Selector, HtmlXPathSelector
from unidecode import unidecode
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import datetime
from dateutil import parser
# from .items import NewsItem
import scrapy
from ..items import NewsDetailItem, FakeNewsTrainingModelItem
from crawler_engine.models import NewsDetail, FakeNewsTrainingModel

MAX_PAGE = 10


class ThanhNienSpider(CrawlSpider):
    name = "thanhnien"
    allowed_domains = ["thanhnien.vn"]
    allowed_categories_re = 'thoi-su|the-gioi|chinh-tri|kinh-doanh|doi-song|van-hoa|gioi-tre|giao-duc|suc-khoe|cong-nghe'
    # allowed_categories_re = 'thoi-su|the-gioi|chinh-tri'

    start_urls = [
        "https://thanhnien.vn"
    ]
    crawledLinks = []
    rules = (
        Rule(LinkExtractor(allow='(%s)\/[\/\w(0-9)-]*[0-9]*\.html$' % allowed_categories_re), callback="parse_item",
             follow=False),
        Rule(LinkExtractor(restrict_xpaths="//nav[@class='site-header__nav']//a"), follow=True),
        Rule(LinkExtractor(allow='(%s)((\/trang-(\d{1,2}).html$))' % allowed_categories_re), follow=True,
             callback=None),
    )

    count_number = 0

    def check_already_crawled_url(self, response):
        url = response.url

        # Category classify system
        # url_crawled_list = NewsDetail.objects.all().values_list('url', flat=True)

        # Fake news classify system
        url_crawled_list = FakeNewsTrainingModel.objects.all().values_list('url', flat=True)

        if url in url_crawled_list:
            return False

        if self.count_number >= 100:
            return False

        return True

    def parse_item(self, response):
        if not self.check_already_crawled_url(response):
            return None
        if response.url in self.crawledLinks:
            return None

        self.crawledLinks.append(response.url)
        hxs = Selector(response)

        # Category classify system
        # item = NewsDetailItem()

        # Fake news calssify system
        item = FakeNewsTrainingModelItem()

        # base_url, url, title, top_image_url, details, authors, category, keywords, published_date,
        # status, crawled, created_at, updated_at
        item['base_url'] = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(response.url))

        item['url'] = response.url

        item['title'] = ''.join(hxs.select('//h1[@class="details__headline"]/text()').extract()).strip()

        # top_img_url = ''
        #
        # if (hxs.select('//div[@class="pswp-content__image"]//img')):
        #     top_img_url = hxs.select('//div[@class="pswp-content__image"]//img/@src')[0].extract()
        # item['top_image_url'] = top_img_url

        item['details'] = ''.join(hxs.select('//div[@id="main_detail"]//div/text()').extract()).strip() + '\n'

        # item['authors'] = ''.join(
        #     hxs.select('//div[@class="details__author__meta" and position()=1]//text()').extract()).strip() +'\n'
        #
        # item['category'] = unidecode(''.join(hxs.select('//meta[@property="article:section"]/@content').extract()).strip())
        #
        # item['keywords'] = ''.join(hxs.select('//meta[@name="keywords"]/@content').extract()).strip()

        item['published_date'] = parser.parse(
            ''.join(hxs.select('//meta[@itemprop="datePublished"]/@content').extract()).strip())

        item['status'] = 1

        if not item['details'].strip():
            return None

        self.count_number += 1
        return item

