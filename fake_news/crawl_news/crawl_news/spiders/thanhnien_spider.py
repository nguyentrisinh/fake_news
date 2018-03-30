from scrapy.spider import CrawlSpider, Rule, BaseSpider
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
# from .items import NewsItem
import scrapy

MAX_PAGE = 10


class DmozSpider(CrawlSpider):
    name = "thanhnien"
    allowed_domains = ["thanhnien.vn"]
    allowed_categories_re = 'thoi-su|the-gioi|chinh-tri|kinh-doanh|doi-song|van-hoa|gioi-tre|giao-duc|suc-khoe|cong-nghe'

    start_urls = [
        "https://thanhnien.vn"
    ]
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//nav[@class='site-header__nav']//a"), follow=True),

        Rule(LinkExtractor(allow='(%s)\/((trang-[0-5].html$)|(^$))' % allowed_categories_re),callback="parse_page",follow=True),
    )
    def parse_item(self, response):
        hxs = Selector(response)
        item = {}
        item['title'] = ''.join(hxs.select('//h1[@class="details__headline"]/text()').extract()).strip() + '\n'
        item['link'] = response.url
        item['description'] = ''.join(hxs.select('//div[@class="sapo"]/text()').extract()).strip() + '\n'
        yield item

    def parse_page(self, response):
        links = response.xpath('//article[@class="story"]/a/@href').extract()

        crawledLinks = []
        for link in links:
            if link not in crawledLinks:
                link = 'https://thanhnien.vn%s' % link
                crawledLinks.append(link)
                yield Request(link, self.parse_item)