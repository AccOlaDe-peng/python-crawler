#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Selenium爬虫示例，用于爬取动态网页
"""
import os
import time
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from utils.logger import crawler_logger as logger
from utils.storage import DataStorage
from utils.user_agents import get_random_user_agent

class SeleniumCrawler:
    """Selenium爬虫类，用于爬取动态网页"""
    
    def __init__(self, headless=True, timeout=10, wait_time=2):
        """
        初始化Selenium爬虫
        
        Args:
            headless (bool, optional): 是否使用无头模式，默认为True
            timeout (int, optional): 页面加载超时时间（秒），默认为10秒
            wait_time (int, optional): 页面渲染等待时间（秒），默认为2秒
        """
        self.headless = headless
        self.timeout = timeout
        self.wait_time = wait_time
        self.driver = None
        self.storage = DataStorage()
    
    def _setup_driver(self):
        """
        设置WebDriver
        
        Returns:
            WebDriver: 配置好的WebDriver实例
        """
        # 设置Chrome选项
        chrome_options = Options()
        
        # 设置无头模式
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # 设置其他选项
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
        
        # 创建WebDriver
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(self.timeout)
            return driver
        except Exception as e:
            logger.error(f"设置WebDriver失败: {str(e)}")
            raise
    
    def start(self):
        """启动WebDriver"""
        if self.driver is None:
            self.driver = self._setup_driver()
            logger.info("WebDriver已启动")
    
    def stop(self):
        """停止WebDriver"""
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
            logger.info("WebDriver已停止")
    
    def get_page(self, url, wait_for_selector=None):
        """
        获取页面
        
        Args:
            url (str): 页面URL
            wait_for_selector (str, optional): 等待元素选择器，默认为None
            
        Returns:
            str: 页面HTML
        """
        try:
            logger.info(f"正在访问页面: {url}")
            self.driver.get(url)
            
            # 如果指定了等待选择器，等待元素出现
            if wait_for_selector:
                try:
                    WebDriverWait(self.driver, self.timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_selector))
                    )
                except TimeoutException:
                    logger.warning(f"等待元素超时: {wait_for_selector}")
            
            # 等待页面渲染
            time.sleep(self.wait_time)
            
            # 获取页面HTML
            return self.driver.page_source
        except Exception as e:
            logger.error(f"获取页面失败: {url}, 错误: {str(e)}")
            return None
    
    def parse_page(self, html, selector=None):
        """
        解析页面
        
        Args:
            html (str): 页面HTML
            selector (str, optional): 内容选择器，默认为None
            
        Returns:
            dict: 解析结果
        """
        if not html:
            return None
        
        try:
            # 解析HTML
            soup = BeautifulSoup(html, 'lxml')
            
            # 获取页面标题
            title = soup.title.text.strip() if soup.title else "无标题"
            
            # 获取页面内容
            if selector:
                content_elements = soup.select(selector)
                content = "\n".join([el.text.strip() for el in content_elements])
            else:
                # 默认获取所有段落文本
                content = "\n".join([p.text.strip() for p in soup.find_all('p')])
            
            # 获取当前URL
            current_url = self.driver.current_url
            
            return {
                "url": current_url,
                "title": title,
                "content": content,
                "crawl_time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            logger.error(f"解析页面失败: {str(e)}")
            return None
    
    def scroll_page(self, times=1, scroll_pause_time=1):
        """
        滚动页面
        
        Args:
            times (int, optional): 滚动次数，默认为1次
            scroll_pause_time (float, optional): 每次滚动后暂停时间（秒），默认为1秒
        """
        try:
            for i in range(times):
                # 执行JavaScript滚动到页面底部
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                logger.debug(f"页面滚动 ({i+1}/{times})")
                time.sleep(scroll_pause_time)
        except Exception as e:
            logger.error(f"滚动页面失败: {str(e)}")
    
    def take_screenshot(self, filename=None):
        """
        截取页面截图
        
        Args:
            filename (str, optional): 截图文件名，默认为None（自动生成）
            
        Returns:
            str: 截图文件路径
        """
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        filepath = os.path.join("crawler", "data", filename)
        
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # 截图
            self.driver.save_screenshot(filepath)
            logger.info(f"截图已保存: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"截图失败: {str(e)}")
            return None
    
    def crawl(self, url, content_selector=None, scroll_times=0, wait_for_selector=None):
        """
        爬取页面
        
        Args:
            url (str): 页面URL
            content_selector (str, optional): 内容选择器，默认为None
            scroll_times (int, optional): 滚动次数，默认为0（不滚动）
            wait_for_selector (str, optional): 等待元素选择器，默认为None
            
        Returns:
            dict: 爬取结果
        """
        try:
            # 启动WebDriver
            self.start()
            
            # 获取页面
            html = self.get_page(url, wait_for_selector=wait_for_selector)
            
            # 如果需要滚动页面
            if scroll_times > 0:
                self.scroll_page(times=scroll_times)
                # 重新获取页面HTML（因为滚动后页面内容可能更新）
                html = self.driver.page_source
            
            # 解析页面
            result = self.parse_page(html, selector=content_selector)
            
            # 截图
            screenshot = self.take_screenshot()
            if result and screenshot:
                result["screenshot"] = screenshot
            
            return result
        finally:
            # 停止WebDriver
            self.stop()
    
    def save_result(self, data, formats=None):
        """
        保存爬取结果
        
        Args:
            data (dict): 爬取的数据
            formats (list, optional): 保存格式列表，可选值为'json', 'csv', 'excel'，默认为['json']
            
        Returns:
            dict: 保存的文件路径字典
        """
        if not data:
            logger.warning("没有数据可保存")
            return {}
        
        if not formats:
            formats = ['json']
        
        result_files = {}
        
        if 'json' in formats:
            json_file = self.storage.save_json(data, name="selenium_result")
            result_files['json'] = json_file
        
        if 'csv' in formats:
            csv_file = self.storage.save_csv([data], name="selenium_result")
            result_files['csv'] = csv_file
        
        if 'excel' in formats:
            excel_file = self.storage.save_excel([data], name="selenium_result")
            result_files['excel'] = excel_file
        
        return result_files

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Selenium动态网页爬虫")
    parser.add_argument("url", help="要爬取的网页URL")
    parser.add_argument("-s", "--selector", help="内容选择器")
    parser.add_argument("-w", "--wait-for", help="等待元素选择器")
    parser.add_argument("-r", "--scroll", type=int, default=0, help="滚动次数，默认为0（不滚动）")
    parser.add_argument("--no-headless", action="store_true", help="不使用无头模式（显示浏览器窗口）")
    parser.add_argument("-t", "--timeout", type=int, default=10, help="页面加载超时时间（秒），默认为10秒")
    parser.add_argument("-f", "--formats", nargs="+", choices=["json", "csv", "excel"], default=["json"], 
                        help="保存格式，可选值为'json', 'csv', 'excel'，默认为'json'")
    args = parser.parse_args()
    
    # 创建爬虫实例
    crawler = SeleniumCrawler(headless=not args.no_headless, timeout=args.timeout)
    
    # 开始爬取
    data = crawler.crawl(
        args.url,
        content_selector=args.selector,
        scroll_times=args.scroll,
        wait_for_selector=args.wait_for
    )
    
    if data:
        # 保存结果
        result_files = crawler.save_result(data, formats=args.formats)
        
        # 打印结果
        print("\n爬取结果:")
        print(f"标题: {data['title']}")
        print(f"URL: {data['url']}")
        print(f"内容预览: {data['content'][:100]}..." if len(data['content']) > 100 else data['content'])
        print(f"截图: {data.get('screenshot', '无')}")
        
        print("\n保存的文件:")
        for fmt, filepath in result_files.items():
            print(f"- {fmt.upper()}: {filepath}")
    else:
        print("\n爬取失败，未获取到数据")

if __name__ == "__main__":
    main() 