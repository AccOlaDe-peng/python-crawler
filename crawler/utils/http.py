"""
HTTP请求工具模块，封装常用的HTTP请求功能
"""
import time
import random
import requests
from requests.exceptions import RequestException

from .user_agents import get_random_user_agent
from .logger import crawler_logger as logger

class HttpClient:
    """HTTP客户端类，封装常用的HTTP请求方法"""
    
    def __init__(self, timeout=10, retry_times=3, retry_interval=(1, 3)):
        """
        初始化HTTP客户端
        
        Args:
            timeout (int, optional): 请求超时时间，默认为10秒
            retry_times (int, optional): 重试次数，默认为3次
            retry_interval (tuple, optional): 重试间隔时间范围（秒），默认为1-3秒
        """
        self.timeout = timeout
        self.retry_times = retry_times
        self.retry_interval = retry_interval
        self.session = requests.Session()
    
    def get(self, url, params=None, headers=None, cookies=None, proxies=None, **kwargs):
        """
        发送GET请求
        
        Args:
            url (str): 请求URL
            params (dict, optional): 查询参数
            headers (dict, optional): 请求头
            cookies (dict, optional): Cookie
            proxies (dict, optional): 代理设置
            **kwargs: 其他参数传递给requests.get()
            
        Returns:
            Response: 请求响应对象
            
        Raises:
            RequestException: 请求异常
        """
        return self._request('GET', url, params=params, headers=headers, 
                            cookies=cookies, proxies=proxies, **kwargs)
    
    def post(self, url, data=None, json=None, headers=None, cookies=None, proxies=None, **kwargs):
        """
        发送POST请求
        
        Args:
            url (str): 请求URL
            data (dict, optional): 表单数据
            json (dict, optional): JSON数据
            headers (dict, optional): 请求头
            cookies (dict, optional): Cookie
            proxies (dict, optional): 代理设置
            **kwargs: 其他参数传递给requests.post()
            
        Returns:
            Response: 请求响应对象
            
        Raises:
            RequestException: 请求异常
        """
        return self._request('POST', url, data=data, json=json, headers=headers, 
                            cookies=cookies, proxies=proxies, **kwargs)
    
    def _request(self, method, url, **kwargs):
        """
        发送HTTP请求的内部方法
        
        Args:
            method (str): 请求方法，如'GET'、'POST'
            url (str): 请求URL
            **kwargs: 其他参数传递给requests方法
            
        Returns:
            Response: 请求响应对象
            
        Raises:
            RequestException: 请求异常
        """
        # 设置默认超时
        kwargs.setdefault('timeout', self.timeout)
        
        # 设置默认请求头
        headers = kwargs.get('headers', {})
        if not headers.get('User-Agent'):
            headers['User-Agent'] = get_random_user_agent()
        kwargs['headers'] = headers
        
        # 重试机制
        for i in range(self.retry_times):
            try:
                logger.debug(f"发送 {method} 请求到 {url}")
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()  # 如果状态码不是200，抛出异常
                return response
            except RequestException as e:
                logger.warning(f"请求失败 ({i+1}/{self.retry_times}): {str(e)}")
                if i < self.retry_times - 1:  # 如果不是最后一次重试
                    # 随机等待一段时间再重试
                    sleep_time = random.uniform(self.retry_interval[0], self.retry_interval[1])
                    logger.info(f"等待 {sleep_time:.2f} 秒后重试...")
                    time.sleep(sleep_time)
                else:
                    logger.error(f"请求失败，已达到最大重试次数: {url}")
                    raise
    
    def close(self):
        """关闭会话"""
        self.session.close()
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()

# 创建默认HTTP客户端实例
http_client = HttpClient()

if __name__ == "__main__":
    # 测试
    try:
        with HttpClient() as client:
            response = client.get("https://httpbin.org/get")
            print(response.json())
            
            response = client.post("https://httpbin.org/post", json={"key": "value"})
            print(response.json())
    except Exception as e:
        print(f"测试失败: {str(e)}") 