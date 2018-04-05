from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from scrapy.http import Request
from datetime import datetime
# get all html tags out of text content
import lxml.html
import dateutil

from ..items import NewsDetailItem, StartupModelItem
from crawler_engine.models import NewsDetail


class VnExpressSpider(CrawlSpider):
    name = 'vn_express_spider'
    allowed_domains = ['vnexpress.net']

    allowed_categories = 'the-gioi|thoi-su'

    start_urls = [
        'https://vnexpress.net'
    ]

    rules = (
        # Rule(LinkExtractor(restrict_xpaths="//nav[@id='sub_menu']//a"), follow=True),
        # Follow ca main menu
        # Rule(LinkExtractor(restrict_xpaths='//nav[@id="sub_menu"]//a'), follow=True),
        # Follow luon sub menu
        # Rule(LinkExtractor(restrict_xpaths='//nav[@id="main_menu"]//a'), follow=True),
        Rule(LinkExtractor(allow='tin-tuc\/(%s)((\/([\w-])*)?)\/([\/\w-])*[0-9]*\.html$' % allowed_categories),
             callback="parse_item"),
        Rule(LinkExtractor(allow='tin-tuc\/(%s)((\/([\w-])*)?)((\/page\/[0-2].html$)|(/$)|$)' % allowed_categories),
             follow=True),
    )

    crawled_links = []

    def check_already_crawled_url(self, response):
        url = response.url
        url_crawled_list = NewsDetail.objects.all().values_list('url', flat=True)

        if url in url_crawled_list:
            return False

        return True

    # Function to check current url is main list page or not
    # Cause function parse_page will parse all the things including detail and sub main list page
    # Detail and sub main list page is including list_news list items
    # Not using it now
    def check_page_is_main_list_page(self, response):
        hxs = Selector(response)
        category = ''.join(hxs.xpath('//ul[@class="breadcrumb left"]/li[@class="start"]/h4/a/@href').extract()).strip()

        full_link = 'https://vnexpress.net' + category + '/page/'
        if response.url.find(full_link) != -1:
            return True

        return False

    def parse_item(self, response):
        # check trong db
        if not self.check_already_crawled_url(response):
            return None
        #check trong luc chay
        if response.url in self.crawled_links:
            return None
        self.crawled_links.append(response.url)
        hxs = Selector(response)
        # create news_item object
        news_item = NewsDetailItem()

        #comment here

        news_item['base_url'] = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(response.url))

        news_item['url'] = response.url

        # --------------------- Get News title ---------------------
        news_item['title'] = ''.join(hxs.xpath('//h1[@class="title_news_detail mb10"]/text()').extract()).strip()

        # --------------------- Get top News image ---------------------
        news_item['top_image_url'] = ''
        list_top_images = hxs.xpath('//table[@class="tplCaption"]/tbody/tr/td/img/@src').extract()

        if len(list_top_images) != 0:
            news_item['top_image_url'] = list_top_images[0]

        # --------------------- Get News' detail ---------------------
        # Note: [not(@style="text-align:right;")] exclude the author name which has style like note
        sub_title = ''.join(hxs.xpath('//h2[@class="description"]/text()').extract()).strip() + '\n'
        list_description = hxs.xpath('//article[@class="content_detail fck_detail width_common block_ads_connect"]'
                                     '/p[not(@style="text-align:right;")]').extract()

        # description = ''.join(list_description)
        description = ''.join(list_description).strip()
        description_without_html_tag = lxml.html.fromstring(description)  # load html format from string description
        description = sub_title + description_without_html_tag.text_content()  # get only text detail without html tags

        news_item['details'] = description

        # --------------------- Get News' Author ---------------------
        news_item['authors'] = ''
        authors = hxs.xpath('//article[@class="content_detail fck_detail width_common block_ads_connect"]'
                            '/p[@style="text-align:right;"]/strong/text()').extract()

        # if authors has item
        if authors:
            # make item.authors = authors[0]
            news_item['authors'] = ''.join(authors).strip()

        # --------------------- Get News' category ---------------------
        categories = hxs.xpath('//ul[@class="breadcrumb left"]/li[@class="start"]/h4/a/text()').extract()
        news_item['category'] = ''.join(categories).strip()

        # get News' keywords
        news_item['keywords'] = ''.join(hxs.xpath('//meta[@name="keywords"]/@content').extract()).strip()

        # --------------------- Get News' published date ---------------------
        published_date = hxs.xpath('//span[@class="time left"]/text()').extract()

        # Convert from string to date string with format DD/MM/YYYY
        date = published_date[0]
        date_start_index = date.index(',') + 2
        date = date[date_start_index:]

        # convert from string to time string with format %H:%M (HH:MM full 24h)
        time = published_date[1]
        time_end_index = time.index('GMT') - 1
        time = time[:time_end_index]

        # from date and time string merge into date time string (DD/MM/YYYY HH:MM)
        date_time = '{} {}'.format(date, time)
        # Parse from datetime string into DateTime object
        published_date = dateutil.parser.parse(date_time, dayfirst=True)

        news_item['published_date'] = published_date

        # --------------------- Make News' status default ---------------------
        news_item['status'] = 1

        # end comment here

        # print(news_ite)

        return news_item

    # def parse_page(self, response):
    #     # if self.check_page_is_main_list_page(response):
    #         links = response.xpath('//article[@class="list_news"]/h3/a/@href').extract()
    #         if links:
    #             # run all link in links
    #             for link in links:
    #                 # print(link)
    #                 if link not in self.crawled_links:
    #                     self.crawled_links.append(link)
    #                     yield Request(link, self.parse_item)
