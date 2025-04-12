import requests
import json
from bs4 import BeautifulSoup

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
           "cookie": 'bid=vRfFyB2OjWw; _pk_id.100001.3ac3=51de9f11aaad80f5.1743595040.; _vwo_uuid_v2=D83B9703025A3456B16758489ABACFCFB|2403e3d14ab08ae34967cc2839b4df9d; __yadk_uid=rMAPAkA7ckqDERN9l9CeRHx48cOrrVrq; viewed="1007305"; dbcl2="288172148:KqMpJr1f2UY"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.28817; __utmz=30149280.1743863173.4.3.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=81379588.1743863173.4.3.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ck=knYI; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1744036637%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.3ac3=1; ap_v=0,6.0; __utma=30149280.2140059697.1743595040.1743863173.1744036638.5; __utmc=30149280; __utmt_douban=1; __utmb=30149280.1.10.1744036638; __utma=81379588.1744343069.1743595040.1743863173.1744036638.5; __utmc=81379588; __utmt=1; __utmb=81379588.1.10.1744036638'
}

pages = 6
result = []
for page in range(pages):
    start = page * 20
    base_url = f"https://book.douban.com/subject/1007305/comments/?percent_type=h&start={start}&limit=20&status=P&sort=score"
    url = base_url
    resp = requests.get(url, headers=headers)
    print(resp)

    bs = BeautifulSoup(resp.text, "html.parser")

    # comment_item = bs.find_all("li", {"class": "comment-item"})[0]
    # date_string = comment_item.find("a", {"class": "comment-time"}).get_text()

    from datetime import datetime
    date_format = "%Y-%m-%d %H:%M:%S"
    # timestamp = int(datetime.strptime(date_string, date_format).timestamp())

    # comment_info = comment_item.find('span', {"class": "comment-info"})
    # user_name = comment_info.find('a').get_text(strip=True)
    # comment_location = comment_item.find('span', {"class": "comment-location"}).get_text(strip=True)
    # comment_content = comment_item.find('p', {"class": "comment-content"}).get_text(strip=True)
    # isuseful = comment_item.find('span', {"class": "vote-count"}).get_text(strip=True)

    # star_class = comment_item.find('span', {'class': lambda x: x and x.startswith('allstar')})['class'][1]
    # rating = int(star_class[-2])

    
    for comment_item in bs.find_all("li", {"class": "comment-item"}):
        id = comment_item["data-cid"]
        date_string = comment_item.find("a",{"class": "comment-time"}).get_text()
        timestamp = int(datetime.strptime(date_string, date_format).timestamp())
        comment_info = comment_item.find('span', {"class": "comment-info"})
        user_name = comment_info.find('a').get_text(strip=True)
        location = comment_item.find('span', {"class": "comment-location"}).get_text(strip=True)
        content = comment_item.find('p', {"class": "comment-content"}).get_text(strip=True)
        isuseful = comment_item.find('span', {"class": "vote-count"}).get_text(strip=True)
        try:
            star_class = comment_item.find('span', {"class": lambda x: x and x.startswith('allstar')})['class'][1]
            rating = int(star_class[-2])
        except:
            rating = None
    
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


with open("html2.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False)

