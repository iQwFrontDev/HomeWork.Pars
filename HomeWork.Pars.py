import re

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import lxml
def getPost(query,pages):
    habr_blog = pd.DataFrame()
    arr = []

    for s in query:
        for p in range(1,pages+1):
            URL = f'https://habr.com/ru/search/page2'
            params = {
                'q': s,
                'page': p
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
            }
            req = requests.get(URL, params=params,headers=headers)
            time.sleep(0.1)
            soup = BeautifulSoup(req.text, features='lxml')
            news = soup.find_all('article', class_ = 'tm-articles-list__item')
            for article in news:
                date = article.find('time').get('title')
                # print(date)
                title = article.find('h2', class_ = 'tm-title_h2')
                title_text = title.text if title else "Мегапост"
                try:
                    link = article.find('h2', class_ = 'tm-title_h2').find('a').get('href')
                except:
                    link = article.find('a', class_ = 'tm-megapost-snippet__link').get('href')
                response = requests.get('https://habr.com'+link)
                soup = BeautifulSoup(response.text, features='lxml')
                search_text = soup.find('div',class_ = 'article-formatted-body')
                if search_text == None:
                    text = "Страница удалена"


                elif title_text == "Мегапост":
                    text = search_text.text if search_text else "Мегапост"

                else:
                    text= search_text.text

                like = article.find('span', class_ = 'tm-votes-meter__value_rating').get('title')[0:16]
                # print(like)
                arr.append({'Data':date, 'title':title_text, 'link':link, 'text': text, 'likes': like })
            time.sleep(0.1)
            habr_blog = pd.concat([habr_blog, pd.DataFrame(arr)], ignore_index=True)

    return print(len(habr_blog))

getPost(['анализ данных','python'],1)

# def record(x):
#     x.to_csv('habr.csv', encoding='utf-8')
# record (getPost(['анализ данных','python']))