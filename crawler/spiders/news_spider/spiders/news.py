"""
新闻爬虫示例
"""
import re
import time
from urllib.parse import urljoin

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from crawler.spiders.news_spider.items import NewsItem

class NewsSpider(CrawlSpider):
    """新闻爬虫"""
    
    name = 'news'
    allowed_domains = ['example.com']  # 替换为实际的域名
    start_urls = ['https://example.com/news/']  # 替换为实际的起始URL
    
    # 定义爬取规则
    rules = (
        # 提取新闻列表页中的新闻链接，并使用parse_news方法解析
        Rule(LinkExtractor(restrict_css='.news-list .news-item a'), callback='parse_news'),
        
        # 提取分页链接，并跟随
        Rule(LinkExtractor(restrict_css='.pagination a')),
    )
    
    def __init__(self, *args, **kwargs):
        """初始化爬虫"""
        super(NewsSpider, self).__init__(*args, **kwargs)
        
        # 如果命令行参数中指定了domain和start_url，则使用指定的值
        domain = kwargs.get('domain')
        if domain:
            self.allowed_domains = [domain]
        
        start_url = kwargs.get('start_url')
        if start_url:
            self.start_urls = [start_url]
    
    def parse_news(self, response):
        """
        解析新闻页面
        
        Args:
            response: 响应对象
            
        Returns:
            NewsItem: 新闻Item
        """
        self.logger.info(f'正在解析新闻: {response.url}')
        
        # 创建NewsItem
        item = NewsItem()
        
        # 设置URL
        item['url'] = response.url
        
        # 提取标题
        item['title'] = response.css('h1.title::text').get() or response.css('title::text').get()
        
        # 提取内容
        content_parts = response.css('.article-content p::text').getall()
        item['content'] = '\n'.join([part.strip() for part in content_parts if part.strip()])
        
        # 提取发布时间
        publish_time = response.css('.publish-time::text').get()
        if publish_time:
            # 清理时间字符串
            publish_time = re.sub(r'[\s发布时间：]+', '', publish_time)
            item['publish_time'] = publish_time
        
        # 提取作者
        author = response.css('.author::text').get()
        if author:
            item['author'] = author.strip()
        
        # 提取分类
        category = response.css('.category::text').get()
        if category:
            item['category'] = category.strip()
        
        # 提取标签
        tags = response.css('.tags a::text').getall()
        if tags:
            item['tags'] = [tag.strip() for tag in tags if tag.strip()]
        
        # 设置爬取时间
        item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        return item

class SinaNewsSpider(CrawlSpider):
    """新浪新闻爬虫示例"""
    
    name = 'sina_news'
    allowed_domains = ['sina.com.cn']
    start_urls = ['https://news.sina.com.cn/']
    
    # 定义爬取规则
    rules = (
        # 提取新闻链接，并使用parse_sina_news方法解析
        Rule(LinkExtractor(allow=r'/\d{4}-\d{2}-\d{2}/doc-[a-zA-Z0-9]+\.shtml'), callback='parse_sina_news'),
        
        # 提取导航链接，并跟随
        Rule(LinkExtractor(restrict_css='#blk_nav_1, .nav')),
    )
    
    def parse_sina_news(self, response):
        """
        解析新浪新闻页面
        
        Args:
            response: 响应对象
            
        Returns:
            NewsItem: 新闻Item
        """
        self.logger.info(f'正在解析新浪新闻: {response.url}')
        
        # 创建NewsItem
        item = NewsItem()
        
        # 设置URL
        item['url'] = response.url
        
        # 提取标题
        item['title'] = response.css('#artibodyTitle::text').get() or response.css('title::text').get()
        
        # 提取内容
        content_parts = response.css('#artibody p::text').getall()
        item['content'] = '\n'.join([part.strip() for part in content_parts if part.strip()])
        
        # 提取发布时间
        publish_time = response.css('.time-source::text').get()
        if publish_time:
            # 清理时间字符串
            publish_time = publish_time.strip()
            item['publish_time'] = publish_time
        
        # 提取作者
        author = response.css('.show_author::text').get()
        if author:
            item['author'] = author.strip().replace('责任编辑：', '')
        
        # 提取分类
        breadcrumb = response.css('.breadcrumb a::text').getall()
        if breadcrumb and len(breadcrumb) > 1:
            item['category'] = breadcrumb[1].strip()
        
        # 提取标签
        keywords = response.css('meta[name="keywords"]::attr(content)').get()
        if keywords:
            item['tags'] = [tag.strip() for tag in keywords.split(',') if tag.strip()]
        
        # 设置爬取时间
        item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        return item