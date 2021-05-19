import requests
from datetime import datetime as d
from lxml import html
from pprint import pprint
from pymongo import MongoClient

# Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

# Функция для записи в бд
def new_item(arg, db):
    count = 0
    for i in arg:
        param = i['link_news']
        if db.count_documents({'link_news' : param}) == 0:
            count +=1
            db.insert_one(i)
    print(f"Вставлено {count} записей!")

def news_lenta():

    main_url = 'https://lenta.ru'
    response = requests.get(main_url, headers=header)

    # топ 10 новостей

    if response.ok:
        dom = html.fromstring(response.text)
        items = dom.xpath("//section[contains(@class,'js-top-seven')]/*/div[contains(@class,'item')]")
        news = []
        for item in items:
            news_item = {}
            name = item.xpath(".//a/text()")
            link_news = item.xpath(".//a/@href")
            datetime = item.xpath(".//a/time/@datetime")

            news_item['name'] = name[0].replace('\xa0', ' ')
            if link_news[0][0] == '/':
                news_item['link_news'] = main_url + link_news[0]
            else:
                news_item['link_news'] = link_news[0]
            news_item['datetime'] = datetime[0]
            news_item['link_source'] = main_url
            news_item['name_source'] = 'lenta.ru'

            news.append(news_item)
    return news

def news_yandex():

    main_url = 'https://yandex.ru/news'
    response = requests.get(main_url, headers=header)

    # топ 5 новостей

    if response.ok:
        dom = html.fromstring(response.text)
        items = dom.xpath("//div[contains(@class,'news-app__top')][1]/*")
        news = []
        for item in items:
            news_item = {}
            name = item.xpath(".//div[contains(@class,'mg-card__annotation')]/text()")
            link_news = item.xpath(".//a/@href")
            datetime = item.xpath(".//span[contains(@class,'mg-card-source__time')]/text()")
            name_source = item.xpath(".//a/text()")

            news_item['name'] = name[0].replace('\xa0', ' ')
            if link_news[0][0] == '/':
                news_item['link_news'] = main_url + link_news[0]
            else:
                news_item['link_news'] = link_news[0]
            news_item['datetime'] = datetime[0] + ', ' + d.date(d.now()).strftime('%d %B %Y')
            news_item['link_source'] = main_url
            news_item['name_source'] = name_source
            news.append(news_item)
    return news

def news_mail():

    main_url = 'https://news.mail.ru'
    response = requests.get(main_url, headers=header)

    # топ 5 новостей

    if response.ok:
        dom = html.fromstring(response.text)
        items = dom.xpath("//div[contains(@class,'daynews__item')]")
        news = []
        for item in items:
            news_item = {}
            name = item.xpath(".//span[contains(@class,'photo__title')]/text()")
            link_news = item.xpath(".//a/@href")

            response_mail = requests.get(link_news[0], headers=header)
            dom_mail = html.fromstring(response_mail.text)

            datetime = dom_mail.xpath("//span[contains(@class ,'breadcrumbs__text')]/@datetime")
            name_source = dom_mail.xpath("//span[contains(@class,'note')]//span[contains(@class,'link__text')]//text()")

            news_item['name'] = name[0].replace('\xa0', ' ')
            if link_news[0][0] == '/':
                news_item['link_news'] = main_url + link_news[0]
            else:
                news_item['link_news'] = link_news[0]
            news_item['datetime'] = datetime[0]
            news_item['link_source'] = main_url
            news_item['name_source'] = name_source
            news.append(news_item)
    return news

# pprint(news_lenta())
# pprint(news_yandex())
# pprint(news_mail())

client = MongoClient('127.0.0.1', 27017)
db = client['News']
db_news = db.news

new_item(news_lenta(),db_news)
new_item(news_yandex(),db_news)
new_item(news_mail(),db_news)

pprint(f'В бд {db_news.count_documents({})} записей!')

for db_news in db_news.find({}):
     pprint(db_news);




