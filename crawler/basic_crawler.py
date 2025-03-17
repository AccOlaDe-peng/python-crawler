#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基本爬虫示例，使用requests和BeautifulSoup爬取网页
"""
import os
import time
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

from utils.logger import crawler_logger as logger
from utils.http import HttpClient
from utils.storage import DataStorage

class BasicCrawler:
    """基本爬虫类，使用requests和BeautifulSoup爬取网页"""
    
    def __init__(self, base_url, delay=1, max_pages=10):
        """
        初始化爬虫
        
        Args:
            base_url (str): 基础URL
            delay (float, optional): 请求间隔时间（秒），默认为1秒
            max_pages (int, optional): 最大爬取页数，默认为10页
        """
        self.base_url = base_url
        self.delay = delay
        self.max_pages = max_pages
        self.http_client = HttpClient(timeout=10, retry_times=3)
        self.storage = DataStorage()
        self.visited_urls = set()
    
    def parse_page(self, url):
        """
        解析页面
        
        Args:
            url (str): 页面URL
            
        Returns:
            tuple: (页面标题, 页面内容, 页面链接列表)
        """
        try:
            # 发送请求
            try:
                response = self.http_client.get(url)
            except Exception as e:
                logger.error(f"HTTP请求失败，尝试使用requests库: {str(e)}")
                response = requests.get(url, timeout=10)
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 获取页面标题
            title = soup.title.text.strip() if soup.title else "无标题"
            
            # 获取页面内容（这里简单获取所有段落文本）
            content = "\n".join([p.text.strip() for p in soup.find_all('p')])
            
            # 获取页面链接
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                # 将相对URL转换为绝对URL
                abs_url = urljoin(url, href)
                # 只保留同域名的链接
                if abs_url.startswith(self.base_url):
                    links.append(abs_url)
            
            return title, content, links
        except Exception as e:
            logger.error(f"解析页面失败: {url}, 错误: {str(e)}")
            return None, None, []
    
    def crawl(self):
        """
        开始爬取
        
        Returns:
            list: 爬取的数据列表
        """
        logger.info(f"开始爬取: {self.base_url}")
        
        # 初始化数据列表和待爬取队列
        data = []
        queue = [self.base_url]
        
        # 开始爬取
        page_count = 0
        while queue and page_count < self.max_pages:
            # 获取下一个URL
            url = queue.pop(0)
            
            # 如果已经访问过，跳过
            if url in self.visited_urls:
                continue
            
            logger.info(f"爬取页面 ({page_count+1}/{self.max_pages}): {url}")
            
            # 解析页面
            title, content, links = self.parse_page(url)
            
            # 如果解析成功，保存数据
            if title is not None:
                data.append({
                    "url": url,
                    "title": title,
                    "content_preview": content[:200] + "..." if len(content) > 200 else content,
                    "crawl_time": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                
                # 将新链接添加到队列
                for link in links:
                    if link not in self.visited_urls and link not in queue:
                        queue.append(link)
            
            # 标记为已访问
            self.visited_urls.add(url)
            page_count += 1
            
            # 延迟一段时间
            if queue and page_count < self.max_pages:
                logger.debug(f"等待 {self.delay} 秒...")
                time.sleep(self.delay)
        
        logger.info(f"爬取完成，共爬取 {len(data)} 个页面")
        return data
    
    def save_results(self, data, formats=None):
        """
        保存爬取结果
        
        Args:
            data (list): 爬取的数据列表
            formats (list, optional): 保存格式列表，可选值为'json', 'csv', 'excel'，默认为['json']
            
        Returns:
            dict: 保存的文件路径字典
        """
        if not formats:
            formats = ['json']
        
        result_files = {}
        
        if 'json' in formats:
            json_file = self.storage.save_json(data, name="crawl_results")
            result_files['json'] = json_file
        
        if 'csv' in formats:
            csv_file = self.storage.save_csv(data, name="crawl_results")
            result_files['csv'] = csv_file
        
        if 'excel' in formats:
            excel_file = self.storage.save_excel(data, name="crawl_results")
            result_files['excel'] = excel_file
        
        return result_files

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="基本网页爬虫")
    parser.add_argument("url", help="要爬取的网站URL")
    parser.add_argument("-d", "--delay", type=float, default=1.0, help="请求间隔时间（秒），默认为1秒")
    parser.add_argument("-m", "--max-pages", type=int, default=10, help="最大爬取页数，默认为10页")
    parser.add_argument("-f", "--formats", nargs="+", choices=["json", "csv", "excel"], default=["json"], 
                        help="保存格式，可选值为'json', 'csv', 'excel'，默认为'json'")
    args = parser.parse_args()
    
    # 创建爬虫实例
    crawler = BasicCrawler(args.url, delay=args.delay, max_pages=args.max_pages)
    
    # 开始爬取
    data = crawler.crawl()
    
    # 保存结果
    result_files = crawler.save_results(data, formats=args.formats)
    
    # 打印结果
    print("\n爬取结果:")
    print(f"共爬取 {len(data)} 个页面")
    print("\n保存的文件:")
    for fmt, filepath in result_files.items():
        print(f"- {fmt.upper()}: {filepath}")

if __name__ == "__main__":
    main() 