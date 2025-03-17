# Python 爬虫项目

这是一个功能齐全的 Python 爬虫项目，提供了多种爬虫示例和工具。

## 项目结构

```
crawler/
├── spiders/         # 爬虫脚本目录
├── utils/           # 工具函数目录
├── data/            # 数据存储目录
└── logs/            # 日志文件目录
```

## 功能特点

- 基本网页爬取（使用 requests 和 BeautifulSoup）
- Scrapy 爬虫框架示例
- Selenium 动态网页爬取
- 数据存储（CSV、JSON）
- 用户代理随机化
- 日志记录
- 异常处理

## 安装

1. 克隆此仓库
2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用示例

### 基本爬虫

```bash
python crawler/basic_crawler.py
```

### Scrapy 爬虫

```bash
cd crawler
scrapy crawl news_spider
```

### Selenium 爬虫

```bash
python crawler/selenium_crawler.py
```

## 注意事项

- 请遵守网站的 robots.txt 规则
- 控制爬取频率，避免对目标网站造成压力
- 仅用于学习和研究目的，请勿用于非法用途

## 许可证

MIT
