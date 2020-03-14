# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboUserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 博主id
    id = scrapy.Field()
    # 博主用户名
    screen_name = scrapy.Field()
    # 博主微博是否验证
    verified = scrapy.Field()
    # 博主微博关注数
    follow_count = scrapy.Field()
    # 博主微博粉丝数
    followers_count = scrapy.Field()

    pass
class WeiboItem(scrapy.Item):
    # collection = 'weibos'
    id = scrapy.Field()
    attitudes_count = scrapy.Field()
    comments_count =scrapy. Field()
    reposts_count = scrapy.Field()
    followers_count = scrapy.Field()
    text =scrapy. Field()

    user_name = scrapy.Field()
    created_at =scrapy. Field()
    topic=scrapy.Field()
    hot=scrapy.Field()