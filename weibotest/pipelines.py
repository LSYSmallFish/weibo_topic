# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import json
from weibotest.items import *
from weibotest.utils import *


class WeibosPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            print(item['text'])
            print('\n')
            item['text'] = ReSymbol(item['text'])
            print(item['text'])
            print('\n')
            print(splittest1(item['text']))
            # print(splittest())
            item['hot'] = Calc_HD(item['followers_count'], item['reposts_count'], item['comments_count'])
            # print(type(item['hot']),item['hot'])

            if item.get('created_at'):
                item['created_at'] = item['created_at'].strip()
                item['created_at'] = parse_Date(item['created_at'])

        return item

class WeibotestPipeline(object):
    def __init__(self, host, database, user, password, port):
        # self.f=open("itcast_pipline.json","wb")
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )
        pass

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()
        # pass

    def process_item(self, item, spider):
        if isinstance(item, WeiboUserItem):
            sql = "INSERT INTO blogger(id,screen_name, verified,follow_count,followers_count) VALUES ('%s', '%s', '%s','%s','%s')" % \
                  (item['id'], item['screen_name'], item['verified'], item['follow_count'], item['followers_count'])
            # print(sql)
            # self.cursor.execute(sql)
        if isinstance(item, WeiboItem):
            if (calc_Days(item['created_at']) <= 3 and item['text'] != ' ' and len(item['text']) >4):
                sql = "INSERT INTO blog(id,attitudes_count, reposts_count,comments_count,text,user_name,created_at,hot) VALUES ('%s', '%s', '%s','%s','%s', '%s', '%s','%s')" % \
                      (item['id'], item['attitudes_count'], item['reposts_count'], item['comments_count'], item['text'],
                       item['user_name'], item['created_at'], item['hot'])
                # print(sql)
                # self.cursor.execute(sql)
        self.db.commit()
        return item

    def close_spider(self, spider):
        # f.close()
        self.db.close()
        pass
