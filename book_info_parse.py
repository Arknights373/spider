import json                  # 用于处理JSON数据
import re
import sys
from bs4 import BeautifulSoup # HTML解析库

html1 = sys.argv[1]

with open(html1, "r", encoding="utf-8") as f:
    html_doc = f.read()

bs = BeautifulSoup(html_doc, "html.parser")

book_info_json_str = bs.find("script", {"type": "application/ld+json"}).get_text()
book_info_json = json.loads(book_info_json_str)
book_url = book_info_json["url"]
book_id = book_url.split("/")[2]

book_info_str = bs.find("div", {"id": "info"}).get_text()
book_info_str2 = bs.find("span", {"property": "v:itemreviewed"}).get_text()

book_author = re.search(r"作者:\s*(.*?)\n", book_info_str, re.DOTALL).group(1).strip()

book_name = re.search(r"\s*(\S+)\s*", book_info_str2).group(1).strip()
book_isbn = re.search(r"ISBN:\s*(\S+)\n", book_info_str).group(1).strip()
book_publisher = re.search(r"定价:\s*(\S+)\n", book_info_str).group(1).strip()
book_price = re.search(r"出版社:\s*(\S+)\n", book_info_str).group(1).strip()
book_date = re.search(r"出版年:\s*(\S+)\n", book_info_str).group(1).strip()
book_rating = re.search(r"\s*(\S+)\s*", bs.strong.get_text()).group(1).strip()

book_info = {
    "book_id" : book_id,
    "book_name" : book_name,
    "book_author" : book_author,
    "book_isbn" : book_isbn,
    "book_publisher" : book_publisher,
    "book_price" : book_price,
    "book_date" : book_date,
    "book_rating" : book_rating,
}

with open("html1.json", "w", encoding="utf-8") as f:
    json.dump(book_info, f, ensure_ascii=False)