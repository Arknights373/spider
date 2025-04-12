import requests
import json
from bs4 import BeautifulSoup

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
           "cookie": 'bid=vRfFyB2OjWw; _vwo_uuid_v2=D83B9703025A3456B16758489ABACFCFB|2403e3d14ab08ae34967cc2839b4df9d; viewed="1007305"; dbcl2="288172148:KqMpJr1f2UY"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.28817; ck=knYI; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1744187274%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_id.100001.4cf6=5b0a1ba68d6f0d29.1744187274.; _pk_ses.100001.4cf6=1; ap_v=0,6.0; __utma=30149280.2140059697.1743595040.1744036638.1744187274.6; __utmb=30149280.0.10.1744187274; __utmc=30149280; __utmz=30149280.1744187274.6.4.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.844491994.1744187274.1744187274.1744187274.1; __utmb=223695111.0.10.1744187274; __utmc=223695111; __utmz=223695111.1744187274.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __yadk_uid=DbQbfS1Gourpsve3tWDOhIP4GylYujUo; ll="118318"; frodotk_db="871751c943025cba9545f55bc907162e"'
}

movie_page = 1
final_result = []
for page in range(movie_page):
    movie_num = page * 25
    url_1 = f"https://movie.douban.com/top250?start={movie_num}&filter="
    resp = requests.get(url_1, headers=headers)

    bs1= BeautifulSoup(resp.text, "html.parser")


    for movie_item in bs1.find_all("div", {"class": "info"}):

        http = movie_item.find("a")["href"]
        list = http.split('/')
        id = list[-2]

        title = movie_item.find("span", {"class": "title"}).get_text()

        rating = movie_item.find("span", {"class": "rating_num"}).get_text()

        comment_list = []
        comment_page = 1
        comment_num = comment_page * 20
        url_2 = f"{http}/comments?start={comment_num}&limit=20&status=P&sort=new_score"
        resp2 = requests.get(url_2, headers=headers)
        bs2= BeautifulSoup(resp2.text, "html.parser")


        for comment_item in bs2.find_all("div", {"class": "comment"}):

            cid = comment_item.find("input")["value"]
            
            from datetime import datetime
            date_format = "%Y-%m-%d %H:%M:%S"
            date_string = comment_item.find("span",{"class": "comment-time"}).get_text(strip=True)
            timestamp = int(datetime.strptime(date_string, date_format).timestamp()) 
             
            try:
                star_class = comment_item.find('span', {"class": lambda x: x and x.startswith('allstar')})['class'][0]
                rating2 = int(star_class[-2])
            except:
                rating2 = None

            content = comment_item.find("span", {"class": "short"}).get_text()

            commit2 = {
                "comment_cid": cid,
                "comment_timestamp": timestamp,
                "comment_rating": rating2,
                "comment_content": content
            }
            comment_list.append(commit2)


        commit = {
            "movie_id": id,
            "movie_title": title,
            "movie_rating": rating,
            "comment_list": comment_list
        }
        final_result.append(commit)


with open("html3.json", "w", encoding="utf-8") as f:
    json.dump(final_result, f, ensure_ascii=False)






















