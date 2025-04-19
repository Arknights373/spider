import json                  # 用于处理JSON数据
from urllib.parse import urlparse, parse_qs  # URL解析工具
import requests             # 发送HTTP请求
from bs4 import BeautifulSoup # HTML解析库

url = "https://news.uestc.edu.cn/?n=UestcNews.Front.CategoryV2.Page&CatId=42&page=1"

response = requests.get(url)
# 使用requests库获取网页内容，返回响应对象

bs = BeautifulSoup(response.text, "html.parser")
# 用BeautifulSoup将HTML文本解析为可操作的树形结构

items = bs.find_all("div", {"class": "news-item"})
# 查找所有class为"news-item"的div元素（每条新闻的容器）

news = []
for item in items:
    # 从每个新闻条目中提取信息
    
    # 提取新闻ID（从链接参数中获取）
    link = item.find("div",{"class": "title"}).a.get("href")
    news_id = parse_qs(urlparse(link).query)["Id"][0]
    
    # 提取其他信息
    news_date = item.find("div", {"class": "date"}).get_text().strip()
    news_title = item.find("div", {"class": "title"}).get_text().strip()
    news_content = item.find("div", {"class": "content"}).get_text().strip()
    
    # 存入字典
    news.append(
        {
            "news_id": news_id,
            "news_date": news_date,
            "news_title": news_title,
            "news_content": news_content
        }
    )

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(news, f, ensure_ascii=False)
# 将列表数据保存为UTF-8编码的JSON文件，ensure_ascii=False保证中文正常显示