"""
用户代理工具模块，提供随机用户代理功能
"""
import random
from fake_useragent import UserAgent

# 预定义的一些常用User-Agent
DEFAULT_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux i686; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
]

def get_random_user_agent():
    """
    获取随机用户代理
    
    Returns:
        str: 随机用户代理字符串
    """
    try:
        ua = UserAgent()
        return ua.random
    except Exception:
        # 如果fake-useragent库出现问题，使用预定义的用户代理
        return random.choice(DEFAULT_USER_AGENTS)

def get_specific_user_agent(browser_type):
    """
    获取特定类型的用户代理
    
    Args:
        browser_type (str): 浏览器类型，如'chrome', 'firefox', 'safari', 'edge'
        
    Returns:
        str: 特定类型的用户代理字符串
    """
    try:
        ua = UserAgent()
        if browser_type.lower() == 'chrome':
            return ua.chrome
        elif browser_type.lower() == 'firefox':
            return ua.firefox
        elif browser_type.lower() == 'safari':
            return ua.safari
        elif browser_type.lower() == 'edge':
            return ua.edge
        else:
            return ua.random
    except Exception:
        # 如果出现问题，返回预定义的用户代理
        return random.choice(DEFAULT_USER_AGENTS)

if __name__ == "__main__":
    # 测试
    print("随机用户代理:", get_random_user_agent())
    print("Chrome用户代理:", get_specific_user_agent("chrome"))
    print("Firefox用户代理:", get_specific_user_agent("firefox")) 