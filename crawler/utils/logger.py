"""
日志工具模块，提供日志记录功能
"""
import os
import sys
from datetime import datetime
from loguru import logger

def setup_logger(log_file=None, level="INFO"):
    """
    设置日志记录器
    
    Args:
        log_file (str, optional): 日志文件路径，默认为None（不保存到文件）
        level (str, optional): 日志级别，默认为INFO
        
    Returns:
        logger: 配置好的日志记录器
    """
    # 移除默认的处理器
    logger.remove()
    
    # 添加控制台处理器
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True
    )
    
    # 如果指定了日志文件，添加文件处理器
    if log_file:
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=level,
            rotation="10 MB",  # 日志文件大小达到10MB时轮转
            compression="zip",  # 压缩旧的日志文件
            retention="30 days"  # 保留30天的日志
        )
    
    return logger

def get_default_logger():
    """
    获取默认配置的日志记录器
    
    Returns:
        logger: 配置好的日志记录器
    """
    # 生成默认日志文件名，包含日期
    today = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join("crawler", "logs", f"crawler_{today}.log")
    
    return setup_logger(log_file=log_file)

# 导出默认日志记录器
crawler_logger = get_default_logger()

if __name__ == "__main__":
    # 测试
    crawler_logger.debug("这是一条调试日志")
    crawler_logger.info("这是一条信息日志")
    crawler_logger.warning("这是一条警告日志")
    crawler_logger.error("这是一条错误日志")
    crawler_logger.critical("这是一条严重错误日志") 