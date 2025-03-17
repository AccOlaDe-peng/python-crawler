#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行Scrapy爬虫的脚本
"""
import os
import sys
import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_spider(spider_name, domain=None, start_url=None):
    """
    运行爬虫
    
    Args:
        spider_name (str): 爬虫名称
        domain (str, optional): 域名，默认为None
        start_url (str, optional): 起始URL，默认为None
    """
    # 获取项目设置
    settings = get_project_settings()
    
    # 设置项目设置模块
    settings.setmodule('crawler.spiders.news_spider.settings')
    
    # 创建爬虫进程
    process = CrawlerProcess(settings)
    
    # 设置爬虫参数
    kwargs = {}
    if domain:
        kwargs['domain'] = domain
    if start_url:
        kwargs['start_url'] = start_url
    
    # 启动爬虫
    process.crawl(spider_name, **kwargs)
    
    # 启动爬虫进程
    process.start()

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="运行Scrapy爬虫")
    parser.add_argument("spider", choices=["news", "sina_news"], help="爬虫名称")
    parser.add_argument("-d", "--domain", help="域名")
    parser.add_argument("-s", "--start-url", help="起始URL")
    args = parser.parse_args()
    
    # 运行爬虫
    run_spider(args.spider, domain=args.domain, start_url=args.start_url)

if __name__ == "__main__":
    main() 