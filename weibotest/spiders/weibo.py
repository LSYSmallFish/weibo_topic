# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
from weibotest.items import WeiboUserItem, WeiboItem

global sum
sum = 0


class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["m.weibo.cn"]
    # start_urls = ['https://m.weibo.cn/']
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'
    follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&page={page}'
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=107603{uid}'
    # weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=107603{uid}'
    start_users = ['5044281310', '1618051664', '1192329374', '5878659096', '2656274875', '3937348351', '2803301701']

    # start_users = ['1776845763']

    # 如果没有start_urls必须要有start_requests，它会循环生成要访问的网址
    def start_requests(self):
        for uid in self.start_users:
            # 使用yield可把这个函数当成一个生成器，不断进行操作
            # callback可以指定函数执行的回调函数
            yield Request(self.user_url.format(uid=uid), callback=self.parse)

    def parse(self, response):
        # 将取到的json对象转换为python对象方便对数据进行处理,类型为dict
        res = json.loads(response.body)
        # print(res)
        global sum
        if res['ok']:
            user_item = WeiboUserItem()
            # user_info = res.get('data').get('userInfo')

            user_info = res['data']['userInfo']
            if int(user_info.get('followers_count')) != 0:
                # 获取此博主的id
                user_item['id'] = user_info.get('id')
                # 获取此博主的名字
                user_item['screen_name'] = user_info.get('screen_name')
                # 获取此博主是否是认证用户
                user_item['verified'] = user_info.get('verified')
                # 获取此博主的关注人数
                user_item['follow_count'] = user_info.get('follow_count')
                # 获取此博主的粉丝人数
                user_item['followers_count'] = user_info.get('followers_count')

                # 使用yield返回生成器，将user_item数据提交给管道进行处理并返回来进行执行
                yield user_item

            # 使用yield发送请求，爬取关注列表中关注人的信息，Request函数会发送一个请求，根据里面的参数调用回调函数
            yield Request(self.follow_url.format(uid=user_info.get('id'), page=1), callback=self.follow_parse,
                          meta={'uid': user_info.get('id'), 'page': 1})
            # 使用yield发送请求，爬取关注列表中关注人的信息，Request函数会发送一个请求，根据里面的参数调用回调函数
            yield Request(self.fan_url.format(uid=user_info.get('id'), page=1), callback=self.fan_parse,
                          meta={'uid': user_info.get('id'), 'page': 1})
            # 同关注列表，此请求获取的是微博博文
            yield Request(self.weibo_url.format(uid=user_info.get('id'), page=1), callback=self.parse_Blog,
                          meta={'uid': user_info.get('id'), 'page': 1})

    def follow_parse(self, response):
        res = json.loads(response.body)
        # print(res)
        if res['ok']:
            # data为网页信息。cards为关注信息有几个 前几个是他关注的某种类型的博主，
            # 最后一个是全部关注所以取[-1]
            card_group = res['data']['cards'][-1]['card_group']
            sum = 0
            for i in card_group:
                # 获取关注的用户的信息集
                follow_info = i['user']

                # 获取用户id
                follow_id = follow_info.get('id')
                # 将获取的id用前面处理用户信息的parse函数进行处理
                yield Request(self.user_url.format(uid=follow_id), callback=self.parse)
            # 请求下一页关注列表
            page = response.meta.get('page') + 1
            uid = response.meta.get('uid')
            # print(uid)
            yield Request(self.follow_url.format(uid=uid, page=page), callback=self.follow_parse,
                          meta={"page": page, "uid": uid})

    def fan_parse(self, response):
        res = json.loads(response.body)
        # print(res)
        if res['ok']:
            # data为网页信息。cards为关注信息有几个 前几个是他关注的某种类型的博主，
            # 最后一个是全部关注所以取[-1]
            card_group = res.get('data').get('cards')[-1]['card_group']
            # print(card_group)
            for i in card_group:
                # print(i)
                if 'user' in i:
                    # 获取关注的用户的信息集
                    fan_info = i['user']
                    # 获取用户id
                    fan_id = fan_info.get('id')
                    # 将获取的id用前面处理用户信息的parse函数进行处理
                    yield Request(self.user_url.format(uid=fan_id), callback=self.parse)
            # 请求下一页关注列表
            page = response.meta.get('page') + 1
            uid = response.meta.get('uid')
            yield Request(self.fan_url.format(uid=uid, page=page), callback=self.fan_parse,
                          meta={"page": page, "uid": uid})

    def parse_Blog(self, response):
        res = json.loads(response.body)
        if res['ok']:
            blogs = res['data']['cards']

            for i in blogs:
                blog = i.get('mblog')
                if blog:
                    if int(blog.get('attitudes_count')) != 0:
                        weibo_item = WeiboItem()
                        weibo_item['id'] = blog.get('id')
                        weibo_item['attitudes_count'] = blog.get('attitudes_count')
                        weibo_item['reposts_count'] = blog.get('reposts_count')
                        weibo_item['comments_count'] = blog.get('comments_count')
                        weibo_item['text'] = blog.get('text')
                        weibo_item['user_name'] = blog.get('user').get('screen_name')
                        weibo_item['created_at'] = blog.get('created_at')
                        weibo_item['followers_count'] = blog.get('user').get('followers_count')
                        # print(blog.get('user').get('followers_count'))
                        yield weibo_item

        pass
