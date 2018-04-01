from scrapy.spider import CrawlSpider, Rule, BaseSpider
from scrapy.selector import Selector, HtmlXPathSelector
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import datetime
from dateutil   import parser
# from .items import NewsItem
import scrapy

MAX_PAGE = 10


class ThanhNienSpider(CrawlSpider):
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
        # base_url, url, title, top_image_url, details, authors, category, keywords, published_date, status, crawled, created_at, updated_at
        item['base_url'] = domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(response.url))

        item['url'] = response.url

        item['title'] = ''.join(hxs.select('//h1[@class="details__headline"]/text()').extract()).strip() + '\n'

        top_img_url = ''
        # if (hxs.select('//img[@class="storyavatar"]/@src')):
        #     top_img_url = hxs.select('//img[@class="storyavatar"]/@src').extract()
        # else:
        if (hxs.select('//div[@class="pswp-content__image"]//img')):
            top_img_url =  hxs.select('//div[@class="pswp-content__image"]//img/@src')[0].extract()
        item['top_image_url'] = top_img_url

        item['details'] = ''.join(hxs.select('//div[@id="main_detail"]//div/text()').extract()).strip()+'\n'

        item['authors'] = ''.join(hxs.select('//div[@class="details__author__meta" and position()=1]//text()').extract()).strip()+'\n'

        item['category']= ''.join(hxs.select('//meta[@property="article:section"]/@content').extract()).strip()+'\n'

        item['keywords'] = ''.join(hxs.select('//meta[@name="keywords"]/@content').extract()).strip() + '\n'

        item['published_date'] = parser.parse(''.join(hxs.select('//meta[@itemprop="datePublished"]/@content').extract()).strip() + '\n')

        item['status'] = 0

        item['crawled']= datetime.date.today()

        item['created_at'] = datetime.date.today()

        item['updated_at'] = datetime.date.today()

        yield item

    def parse_page(self, response):
        links = response.xpath('//article[@class="story"]/a/@href').extract()

        crawledLinks = []
        for link in links:
            if link not in crawledLinks:
                link = 'https://thanhnien.vn%s' % link
                crawledLinks.append(link)
                yield Request(link, self.parse_item)