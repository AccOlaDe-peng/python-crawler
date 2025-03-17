"""
Scrapy爬虫的Pipeline定义
"""
import os
import json
import csv
from datetime import datetime

from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

class DuplicatesPipeline:
    """去重Pipeline"""
    
    def __init__(self):
        self.urls_seen = set()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('url') in self.urls_seen:
            raise DropItem(f"重复的新闻: {item['url']}")
        else:
            self.urls_seen.add(adapter['url'])
            return item

class CleanDataPipeline:
    """数据清洗Pipeline"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # 清洗标题（去除首尾空格）
        if adapter.get('title'):
            adapter['title'] = adapter['title'].strip()
        
        # 清洗内容（去除首尾空格和多余换行）
        if adapter.get('content'):
            adapter['content'] = adapter['content'].strip().replace('\r\n', '\n').replace('\n\n', '\n')
        
        # 添加爬取时间
        if not adapter.get('crawl_time'):
            adapter['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return item

class JsonWriterPipeline:
    """JSON文件存储Pipeline"""
    
    def __init__(self, data_dir='crawler/data'):
        self.data_dir = data_dir
        self.file = None
        self.items = []
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            data_dir=crawler.settings.get('DATA_DIR', 'crawler/data')
        )
    
    def open_spider(self, spider):
        # 确保目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{spider.name}_{timestamp}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        # 打开文件
        self.file = open(filepath, 'w', encoding='utf-8')
        
        # 记录文件路径
        spider.logger.info(f"JSON文件路径: {filepath}")
        spider.json_file = filepath
    
    def close_spider(self, spider):
        # 写入数据
        json.dump(self.items, self.file, ensure_ascii=False, indent=2)
        self.file.close()
        
        spider.logger.info(f"已保存 {len(self.items)} 条数据到JSON文件")
    
    def process_item(self, item, spider):
        # 将Item转换为字典并添加到列表
        self.items.append(dict(item))
        return item

class CsvWriterPipeline:
    """CSV文件存储Pipeline"""
    
    def __init__(self, data_dir='crawler/data'):
        self.data_dir = data_dir
        self.file = None
        self.writer = None
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            data_dir=crawler.settings.get('DATA_DIR', 'crawler/data')
        )
    
    def open_spider(self, spider):
        # 确保目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{spider.name}_{timestamp}.csv"
        filepath = os.path.join(self.data_dir, filename)
        
        # 打开文件
        self.file = open(filepath, 'w', encoding='utf-8', newline='')
        
        # 记录文件路径
        spider.logger.info(f"CSV文件路径: {filepath}")
        spider.csv_file = filepath
    
    def close_spider(self, spider):
        self.file.close()
    
    def process_item(self, item, spider):
        # 如果writer还没有初始化
        if self.writer is None:
            # 获取所有字段名
            fieldnames = item.keys()
            self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
            self.writer.writeheader()
        
        # 将Item写入CSV
        self.writer.writerow(ItemAdapter(item).asdict())
        return item 