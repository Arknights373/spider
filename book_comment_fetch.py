import requests
headers = {"user-agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64; rv:109.0)Gecko/20100101 Firefox/109.0"}
url = "http://book.douban.com/subject/1007305/comments"
resp = requests.get(url, headers=headers)

from bs4 import BeautifulSoup
bs = BeautifulSoup(resp.text, "html.parser")

comment_item = bs.find_all("li", {"class": "comment-item"})[0]
date_string = comment_item.find("a", {"class": "comment-time"}).get_text()

from datetime import datetime
date_format = "%Y-%m-%d %H:%M:%S"
timestamp = int(datetime.strptime(date_string, date_format).timestamp())

# comment_info = comment_item.find('span', {"class": "comment-info"})
# user_name = comment_info.find('a').get_text(strip=True)
# comment_location = comment_item.find('span', {"class": "comment-location"}).get_text(strip=True)
# comment_content = comment_item.find('p', {"class": "comment-content"}).get_text(strip=True)
# isuseful = comment_item.find('span', {"class": "vote-count"}).get_text(strip=True)

# star_class = comment_item.find('span', {'class': lambda x: x and x.startswith('allstar')})['class'][1]
# rating = int(star_class[-2])

result = []
for comment_item in bs.find_all("li", {"class": "comment-item"}):
    id = comment_item["data-cid"]
    date_string = comment_item.find("a",{"class": "comment-time"}).get_text()
    timestamp = int(datetime.strptime(date_string, date_format).timestamp())
    comment_info = comment_item.find('span', {"class": "comment-info"})
    user_name = comment_info.find('a').get_text(strip=True)
    location = comment_item.find('span', {"class": "comment-location"}).get_text(strip=True)
    content = comment_item.find('p', {"class": "comment-content"}).get_text(strip=True)
    isuseful = comment_item.find('span', {"class": "vote-count"}).get_text(strip=True)
    star_class = comment_item.find('span', {"class": lambda x: x and x.startswith('allstar')})['class'][1]
    rating = int(star_class[-2])
    commit = {
        "comment_id": id,
        "comment_timestamp": timestamp,
        "comment_username": user_name,
        "comment_location": location,
        "comment_rating": rating,
        "comment_content": content,
        "comment_isuseful": isuseful,
    }
    result.append(commit)
print(result)

