# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
import datetime


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
        sql = """INSERT INTO crawler_engine_newsdetail(base_url, url, title, top_image_url, details, authors, category, keywords, published_date, status, crawled, created_at, updated_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        self.cur.execute(sql, (item['base_url'], item['url'], item['title'], item['top_image_url'], item['details'], item['authors'], item['category'], item['keywords'], item['published_date'], item['status'], item['crawled'], item['created_at'], item['updated_at']))
        # sql = """INSERT INTO crawler_engine_newsdetail(base_url, url, status, crawled, created_at, updated_at) VALUES(%s,%s,%s,%s,%s,%s) """
        # self.cur.execute(sql, (item['base_url'], item['url'], 0, item['crawled'], item['created_at'], item['updated_at']))
        self.connection.commit()
        return item
        # def process_item(self, item, spider):
        #     return item
