"""
Scrapy爬虫的设置
"""

# 爬虫名称
BOT_NAME = 'news_spider'

# 爬虫模块
SPIDER_MODULES = ['crawler.spiders.news_spider.spiders']
NEWSPIDER_MODULE = 'crawler.spiders.news_spider.spiders'

# 遵循robots.txt规则
ROBOTSTXT_OBEY = True

# 并发请求数
CONCURRENT_REQUESTS = 16

# 下载延迟
DOWNLOAD_DELAY = 1

# 随机下载延迟
RANDOMIZE_DOWNLOAD_DELAY = True

# 禁用Cookie
COOKIES_ENABLED = False

# 设置默认请求头
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

# 启用中间件
DOWNLOADER_MIDDLEWARES = {
    'crawler.spiders.news_spider.middlewares.RandomUserAgentMiddleware': 543,
}

# 启用Pipeline
ITEM_PIPELINES = {
    'crawler.spiders.news_spider.pipelines.DuplicatesPipeline': 300,
    'crawler.spiders.news_spider.pipelines.CleanDataPipeline': 400,
    'crawler.spiders.news_spider.pipelines.JsonWriterPipeline': 800,
    'crawler.spiders.news_spider.pipelines.CsvWriterPipeline': 900,
}

# 数据存储目录
DATA_DIR = 'crawler/data'

# 日志级别
LOG_LEVEL = 'INFO'

# 日志文件
LOG_FILE = 'crawler/logs/scrapy.log' 