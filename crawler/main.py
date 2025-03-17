#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
爬虫项目主程序入口
"""
import os
import sys
import argparse

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Python爬虫项目")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 基本爬虫命令
    basic_parser = subparsers.add_parser("basic", help="运行基本爬虫")
    basic_parser.add_argument("url", help="要爬取的网站URL")
    basic_parser.add_argument("-d", "--delay", type=float, default=1.0, help="请求间隔时间（秒），默认为1秒")
    basic_parser.add_argument("-m", "--max-pages", type=int, default=10, help="最大爬取页数，默认为10页")
    basic_parser.add_argument("-f", "--formats", nargs="+", choices=["json", "csv", "excel"], default=["json"], 
                            help="保存格式，可选值为'json', 'csv', 'excel'，默认为'json'")
    
    # Selenium爬虫命令
    selenium_parser = subparsers.add_parser("selenium", help="运行Selenium爬虫")
    selenium_parser.add_argument("url", help="要爬取的网页URL")
    selenium_parser.add_argument("-s", "--selector", help="内容选择器")
    selenium_parser.add_argument("-w", "--wait-for", help="等待元素选择器")
    selenium_parser.add_argument("-r", "--scroll", type=int, default=0, help="滚动次数，默认为0（不滚动）")
    selenium_parser.add_argument("--no-headless", action="store_true", help="不使用无头模式（显示浏览器窗口）")
    selenium_parser.add_argument("-t", "--timeout", type=int, default=10, help="页面加载超时时间（秒），默认为10秒")
    selenium_parser.add_argument("-f", "--formats", nargs="+", choices=["json", "csv", "excel"], default=["json"], 
                                help="保存格式，可选值为'json', 'csv', 'excel'，默认为'json'")
    
    # Scrapy爬虫命令
    scrapy_parser = subparsers.add_parser("scrapy", help="运行Scrapy爬虫")
    scrapy_parser.add_argument("spider", choices=["news", "sina_news"], help="爬虫名称")
    scrapy_parser.add_argument("-d", "--domain", help="域名")
    scrapy_parser.add_argument("-s", "--start-url", help="起始URL")
    
    args = parser.parse_args()
    
    # 根据命令执行相应的操作
    if args.command == "basic":
        # 导入基本爬虫模块
        from crawler.basic_crawler import main as basic_main
        
        # 设置命令行参数
        sys.argv = [sys.argv[0]]
        sys.argv.append(args.url)
        if args.delay != 1.0:
            sys.argv.extend(["-d", str(args.delay)])
        if args.max_pages != 10:
            sys.argv.extend(["-m", str(args.max_pages)])
        if args.formats != ["json"]:
            sys.argv.extend(["-f"] + args.formats)
        
        # 运行基本爬虫
        basic_main()
    
    elif args.command == "selenium":
        # 导入Selenium爬虫模块
        from crawler.selenium_crawler import main as selenium_main
        
        # 设置命令行参数
        sys.argv = [sys.argv[0]]
        sys.argv.append(args.url)
        if args.selector:
            sys.argv.extend(["-s", args.selector])
        if args.wait_for:
            sys.argv.extend(["-w", args.wait_for])
        if args.scroll != 0:
            sys.argv.extend(["-r", str(args.scroll)])
        if args.no_headless:
            sys.argv.append("--no-headless")
        if args.timeout != 10:
            sys.argv.extend(["-t", str(args.timeout)])
        if args.formats != ["json"]:
            sys.argv.extend(["-f"] + args.formats)
        
        # 运行Selenium爬虫
        selenium_main()
    
    elif args.command == "scrapy":
        # 导入Scrapy爬虫模块
        from crawler.run_scrapy import main as scrapy_main
        
        # 设置命令行参数
        sys.argv = [sys.argv[0]]
        sys.argv.append(args.spider)
        if args.domain:
            sys.argv.extend(["-d", args.domain])
        if args.start_url:
            sys.argv.extend(["-s", args.start_url])
        
        # 运行Scrapy爬虫
        scrapy_main()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 