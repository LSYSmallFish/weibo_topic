# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import random
from weibotest.settings import IPPOOL


class WeibotestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddlware(object):
    # 随机更换user-agent
    # 我们先定义好代理池
    http = ['http://121.8.98.196:8540', 'http://120.194.18.90:8130']
    https = ['https://39.137.107.98:8659', 'https://182.92.105.136:8434']

    # http://www.goubanjia.com 提供很好的代理ip

    def process_request(self, request, spider):
        """
        这是下载中间件中 拦截请求 的方法
        :param request: 拦截到的请求
       """
        # print(request)  # <GET https://www.baidu.com/s?wd=ip>

        # ua = UserAgent(use_cache_server=False).random  # 生成随机UA
        # request.headers['User-Agent'] = ua  # 将生成的UA写入请求头中

        # # 判断请求是超文本传输协议，还是安全套接字超文本传输协议，并对其使用对应的代理池
        # request.meta['proxy'] = random.choice(getattr(self, request.url.split(':')[0]))

        # thisip = random.choice(IPPOOL)
        # # print("this is ip:" + thisip["ipaddr"])
        # request.meta["proxy"] = "http://" + thisip["ipaddr"]
        return None

    def process_response(self, request, response, spider):
        """这是下载中间件中 拦截响应 的方法"""
        # print(response)  # <200 https://www.baidu.com/s?wd=ip>
        return response
