"""
Scrapy爬虫的Item定义
"""
import scrapy

class NewsItem(scrapy.Item):
    """新闻Item定义"""
    
    # 新闻标题
    title = scrapy.Field()
    
    # 新闻URL
    url = scrapy.Field()
    
    # 新闻内容
    content = scrapy.Field()
    
    # 发布时间
    publish_time = scrapy.Field()
    
    # 作者
    author = scrapy.Field()
    
    # 分类
    category = scrapy.Field()
    
    # 标签
    tags = scrapy.Field()
    
    # 爬取时间
    crawl_time = scrapy.Field() 