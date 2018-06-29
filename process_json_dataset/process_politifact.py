import json
import os
from googletrans import Translator
from dateutil import parser
from helper.db import Connection
from helper.divide_helper import divide_trans

dataset_dir = 'Data'
subdataset_dir = 'Politifact'
real_dir = 'RealNewsContent'
fake_dir = 'FakeNewsContent'
label = 2


def process_json():
    #Cho nay truyen fake_dir thi label chinh lai =0, neu truyen real dir thi label =1
    file_dir = 'dataset/%s/%s/%s' % (dataset_dir, subdataset_dir, real_dir)
    directory = os.fsencode(file_dir)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        f = open(file_dir + '/' + filename, 'rt')
        data = json.load(f)
        item= {}

        try:
            item['base_url'] = data['source']
        except:
            item['base_url'] = ''

        try:
            item['url'] = data['url']
        except:
            item['url'] = ''

        try:
            item['title'] = data['title']
        except:
            item['title'] = ''

        # try:
        #     item['top_image_url'] = data['top_img']
        # except:
        #     item['top_image_url'] = ''
            # print(filename)

        item['details'] = divide_trans(data['text'],10)

        item['authors'] = ''

        # try:
        #     item['authors'] = ' '.join(x for x in data['authors'])
        # except:
        # item['authors'] = ''
        #
        # item['category'] = ''
        # try:
        #     item['keywords'] = ' '.join(x for x in data['keywords'])
        # except:
        #     item['keywords'] = ''

        item['published_date'] = parser.parse('2018-06-24T06:00:00T+07:00')

        item['status'] = label
        # item['crawled'] = item['published_date']
        # item['created_at'] = item['published_date']
        # item['updated_at'] = item['published_date']
        print(item['details'])

        con = Connection()
        con.connect()
        # insert_query = 'insert into crawler_engine_newsdetail(base_url,url,title,top_image_url,details,authors,category,keywords,published_date,status,crawled,created_at,updated_at) ' \
        #                'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%d,\'%s\',\'%s\',\'%s\')' % \
        #                (item['base_url'].replace('\'','\'\''),item['url'].replace('\'','\'\''),
        #                 item['title'].replace('\'','\'\''),item['top_image_url'].replace('\'','\'\''),
        #                 item['details'].replace('\'','\'\''),item['authors'].replace('\'','\'\''),
        #                 item['category'].replace('\'','\'\''),item['keywords'].replace('\'','\'\''),
        #                 item['published_date'],item['status'],
        #                 item['published_date'],item['published_date'],item['published_date']
        #                 )

        insert_query = 'insert into crawler_engine_fakenewstrainingmodel(base_url,url,title,details,published_date,status,crawled,created_at,updated_at) ' \
                       'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%d,\'%s\',\'%s\',\'%s\')' % \
                       (item['base_url'].replace('\'', '\'\''),
                        item['url'].replace('\'', '\'\''),
                        item['title'].replace('\'', '\'\''),
                        item['details'].replace('\'', '\'\''),
                        item['published_date'],
                        item['status'],
                        item['published_date'],
                        item['published_date'],
                        item['published_date']
                        )
        try:
            con.insert(insert_query)
        except:
            print(filename)
        con.close()


if __name__ == '__main__':
    process_json()
