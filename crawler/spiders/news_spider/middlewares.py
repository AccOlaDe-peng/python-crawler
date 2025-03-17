"""
Scrapy爬虫的中间件
"""
import random
from scrapy import signals
from itemadapter import is_item, ItemAdapter

from crawler.utils.user_agents import get_random_user_agent, DEFAULT_USER_AGENTS

class RandomUserAgentMiddleware:
    """随机User-Agent中间件"""
    
    def __init__(self, user_agents=None):
        self.user_agents = user_agents or DEFAULT_USER_AGENTS
    
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware
    
    def process_request(self, request, spider):
        # 设置随机User-Agent
        request.headers['User-Agent'] = get_random_user_agent()
        return None
    
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class NewsSpiderMiddleware:
    """爬虫中间件"""
    
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
    
    def process_spider_input(self, response, spider):
        return None
    
    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i
    
    def process_spider_exception(self, response, exception, spider):
        pass
    
    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r
    
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class NewsDownloaderMiddleware:
    """下载器中间件"""
    
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
    
    def process_request(self, request, spider):
        return None
    
    def process_response(self, request, response, spider):
        return response
    
    def process_exception(self, request, exception, spider):
        pass
    
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name) 