from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from scrapy.http import Request
from dateutil import parser
# get all html tags out of text content
import lxml.html


from ..items import NewsDetailItem, StartupModelItem


class VnExpressSpider(CrawlSpider):
    name = 'vn_express_spider'
    allowed_domains = ['vnexpress.net']

    allowed_categories = 'the-gioi|thoi-su'

    start_urls = [
        'https://vnexpress.net/'
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//nav[@id='sub_menu']//a"), follow=True),

        Rule(LinkExtractor(allow='tin-tuc\/%s\/((page\/[0-2].html$)|(^$))' % allowed_categories),
             callback="parse_page", follow=True),

        # Rule(LinkExtractor(allow='tin-tuc\/%s\/((page\/[0-2]\.html$))' % allowed_categories),
        #      callback="parse_page", follow=True),
    )

    def parse_item(self, response):
        hxs = Selector(response)
        # create news_item object
        news_item = NewsDetailItem()

        news_item['base_url'] = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(response.url))

        news_item['url'] = response.url

        # get News title
        news_item['title'] = ''.join(hxs.xpath('//h1[@class="title_news_detail mb10"]/text()').extract()).strip()

        # get top News image
        news_item['top_image_url'] = ''
        list_top_images = hxs.xpath('//table[@class="tplCaption"]/tbody/tr/td/img/@src').extract()

        if len(list_top_images) != 0:
            news_item['top_image_url'] = list_top_images[0]

        # get News' detail
        # Note: [not(@style="text-align:right;")] exclude the author name which has style like note
        sub_title = ''.join(hxs.xpath('//h2[@class="description"]/text()').extract()).strip() + '\n'
        list_description = hxs.xpath('//article[@class="content_detail fck_detail width_common block_ads_connect"]'
                                     '/p[not(@style="text-align:right;")]').extract()

        # description = ''.join(list_description)
        description = ''.join(list_description).strip()
        description_without_html_tag = lxml.html.fromstring(description)  # load html format from string description
        description = sub_title + description_without_html_tag.text_content()  # get only text detail without html tags

        news_item['details'] = description

        # Get News' Author
        news_item['authors'] = ''
        authors = hxs.xpath('//article[@class="content_detail fck_detail width_common block_ads_connect"]'
                            '/p[@style="text-align:right;"]/strong/text()').extract()

        # if authors has item
        if authors:
            # make item.authors = authors[0]
            news_item['authors'] = ''.join(authors).strip()

        # get News' category
        categories = hxs.xpath('//ul[@class="breadcrumb left"]/li[@class="start"]/h4/a/text()').extract()
        news_item['category'] = ''.join(categories).strip()

        # get News' keywords
        news_item['keywords'] = ''.join(hxs.xpath('//meta[@name="keywords"]/@content').extract()).strip()

        # get News' published date
        published_date = hxs.xpath('//span[@class="time left"]/text()').extract()
        print(published_date)
        date = published_date[0]
        date_start_index = date.index(',')
        date = date[date_start_index:]
        print(date, '------------------------------')
        time = published_date[1]
        # published_date = ''.join(published_date)
        #
        # news_item['published_date'] = published_date

        return news_item

    def parse_page(self, response):
        # links = response.xpath("//div[@class='mt3']/a/@href").extract()
        links = response.xpath('//article[@class="list_news"]/h3/a/@href').extract()
        # links_test = response.xpath('//nav[@id="sub_menu"]//a').extract()
        # print(links, response)

        crawled_links = []

        for link in links:
            # print(link)
            if link not in crawled_links:
                # print(link, '---------------------------------------------')
                crawled_links.append(link)
                # print('test')
                # self.parse_item('test')
                yield Request(link, self.parse_item)
