from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

from ..items import NewsDetailItem, StartupModelItem


class DanTriSpider(CrawlSpider):
    name = 'dan_tri_spider'
    allowed_domains = ['dantri.com.vn']

    allowed_categories = 'the-gioi|the-thao|giao-duc-khuyen-hoc'

    # full category from dantri.com.vn
    # allowed_categories = 'su-kien|xa-hoi|the-gioi|the-thao|giao-duc-khuyen-hoc|tam-long-nhan-ai|kinh-doanh|van-hoa|' \
    #                      'giai-tri|phap-luat|nhip-song-tre|suc-khoe|suc-manh-so|o-to-xe-may|tinh-yeu-gioi-tinh|' \
    #                      'chuyen-la'

    start_urls = [
        'http://dantri.com.vn/'
    ]

    rules = (
        # Rule(LinkExtractor(allow='{}\/'.format(allowed_categories), follow=True)),

        # Rule for page
        Rule(LinkExtractor(allow='{}\/((trang-[0-2].htm$)|(^$))'.format(allowed_categories)), callback="parse_page",
             follow=True),

    )

    def parse_item(self, response):
        hxs = Selector(response)

        return StartupModelItem(name='rolando')

    def parse_page(self, response):
        links = response.xpath("//div[@class='mt3 clearfix eplcheck']/a/@href").extract()
        # links = response.xpath('//div[@class="mt3"]').extract()
        # print(links, response)

        crawled_links = []

        for link in links:
            full_link = 'http://dantri.com.vn{}'.format(link)
            if full_link not in crawled_links:
                print(full_link, '---------------------------------------------')
                crawled_links.append(full_link)
                yield Request(full_link, self.parse_item)

