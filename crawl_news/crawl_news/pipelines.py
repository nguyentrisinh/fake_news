# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2

class CrawlNewsPipeline(object):
    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres'
        password = '123456'  # your password
        database = 'fake_news_db'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("insert into crawler_engine_newsitem(link,description,title) values(%s,%s,%s)", (item['link'], item['description'],item['title']))
        self.connection.commit()
        return item
    # def process_item(self, item, spider):
    #     return item
