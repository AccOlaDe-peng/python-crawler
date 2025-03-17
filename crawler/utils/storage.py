"""
数据存储工具模块，用于保存爬取的数据
"""
import os
import json
import csv
import pandas as pd
from datetime import datetime

from .logger import crawler_logger as logger

class DataStorage:
    """数据存储类，提供多种数据存储方法"""
    
    def __init__(self, data_dir="crawler/data"):
        """
        初始化数据存储类
        
        Args:
            data_dir (str, optional): 数据存储目录，默认为'crawler/data'
        """
        self.data_dir = data_dir
        self._ensure_dir_exists(data_dir)
    
    def _ensure_dir_exists(self, directory):
        """
        确保目录存在，如果不存在则创建
        
        Args:
            directory (str): 目录路径
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"创建目录: {directory}")
    
    def _get_filename(self, name, ext, timestamp=True):
        """
        生成文件名
        
        Args:
            name (str): 文件名前缀
            ext (str): 文件扩展名
            timestamp (bool, optional): 是否添加时间戳，默认为True
            
        Returns:
            str: 完整的文件路径
        """
        if timestamp:
            # 添加时间戳，格式为：name_YYYYMMDD_HHMMSS.ext
            time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{time_str}.{ext}"
        else:
            filename = f"{name}.{ext}"
        
        return os.path.join(self.data_dir, filename)
    
    def save_json(self, data, name="data", timestamp=True, ensure_ascii=False, indent=2):
        """
        保存数据为JSON文件
        
        Args:
            data (dict/list): 要保存的数据
            name (str, optional): 文件名前缀，默认为'data'
            timestamp (bool, optional): 是否添加时间戳，默认为True
            ensure_ascii (bool, optional): 是否确保ASCII编码，默认为False
            indent (int, optional): 缩进空格数，默认为2
            
        Returns:
            str: 保存的文件路径
        """
        filepath = self._get_filename(name, "json", timestamp)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)
            
            logger.info(f"数据已保存为JSON: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"保存JSON失败: {str(e)}")
            raise
    
    def save_csv(self, data, name="data", timestamp=True, encoding='utf-8'):
        """
        保存数据为CSV文件
        
        Args:
            data (list): 要保存的数据列表，每个元素为一个字典
            name (str, optional): 文件名前缀，默认为'data'
            timestamp (bool, optional): 是否添加时间戳，默认为True
            encoding (str, optional): 文件编码，默认为'utf-8'
            
        Returns:
            str: 保存的文件路径
        """
        filepath = self._get_filename(name, "csv", timestamp)
        
        try:
            # 如果数据为空，返回
            if not data:
                logger.warning("没有数据可保存")
                return None
            
            # 获取所有字段名
            fieldnames = set()
            for item in data:
                fieldnames.update(item.keys())
            fieldnames = list(fieldnames)
            
            with open(filepath, 'w', encoding=encoding, newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            logger.info(f"数据已保存为CSV: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"保存CSV失败: {str(e)}")
            raise
    
    def save_excel(self, data, name="data", timestamp=True, sheet_name="Sheet1"):
        """
        保存数据为Excel文件
        
        Args:
            data (list/DataFrame): 要保存的数据，可以是字典列表或DataFrame
            name (str, optional): 文件名前缀，默认为'data'
            timestamp (bool, optional): 是否添加时间戳，默认为True
            sheet_name (str, optional): 工作表名称，默认为'Sheet1'
            
        Returns:
            str: 保存的文件路径
        """
        filepath = self._get_filename(name, "xlsx", timestamp)
        
        try:
            # 如果数据不是DataFrame，转换为DataFrame
            if not isinstance(data, pd.DataFrame):
                df = pd.DataFrame(data)
            else:
                df = data
            
            # 保存为Excel
            df.to_excel(filepath, sheet_name=sheet_name, index=False)
            
            logger.info(f"数据已保存为Excel: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"保存Excel失败: {str(e)}")
            raise
    
    def load_json(self, filepath):
        """
        加载JSON文件
        
        Args:
            filepath (str): 文件路径
            
        Returns:
            dict/list: 加载的数据
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"已加载JSON数据: {filepath}")
            return data
        except Exception as e:
            logger.error(f"加载JSON失败: {str(e)}")
            raise
    
    def load_csv(self, filepath, encoding='utf-8'):
        """
        加载CSV文件
        
        Args:
            filepath (str): 文件路径
            encoding (str, optional): 文件编码，默认为'utf-8'
            
        Returns:
            list: 加载的数据列表，每个元素为一个字典
        """
        try:
            with open(filepath, 'r', encoding=encoding, newline='') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            logger.info(f"已加载CSV数据: {filepath}")
            return data
        except Exception as e:
            logger.error(f"加载CSV失败: {str(e)}")
            raise

# 创建默认数据存储实例
data_storage = DataStorage()

if __name__ == "__main__":
    # 测试
    test_data = [
        {"id": 1, "name": "测试1", "url": "https://example.com/1"},
        {"id": 2, "name": "测试2", "url": "https://example.com/2"},
        {"id": 3, "name": "测试3", "url": "https://example.com/3"}
    ]
    
    storage = DataStorage()
    
    # 测试保存JSON
    json_file = storage.save_json(test_data, name="test_data")
    
    # 测试保存CSV
    csv_file = storage.save_csv(test_data, name="test_data")
    
    # 测试保存Excel
    excel_file = storage.save_excel(test_data, name="test_data")
    
    # 测试加载JSON
    loaded_json = storage.load_json(json_file)
    print("加载的JSON数据:", loaded_json)
    
    # 测试加载CSV
    loaded_csv = storage.load_csv(csv_file)
    print("加载的CSV数据:", loaded_csv) 