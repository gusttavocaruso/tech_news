from datetime import datetime
from tech_news.database import search_news
import re


# Requisito 6
def search_by_title(title):
    news_in_db = search_news({"title": re.compile(title, re.IGNORECASE)})
    # https://localcoder.org/querying-mongodb-via-pymongo-in-case-insensitive-efficiently
    # print(news_in_db)

    news_tuple = [(news['title'], news['url']) for news in news_in_db]
    return news_tuple


# Requisito 7
def search_by_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        # https://www.programiz.com/python-programming/datetime/strptime
        news_in_db = search_news({"timestamp": {"$regex": date}})

        news_tuple = [(news['title'], news['url']) for news in news_in_db]
        return news_tuple
    except(ValueError):
        raise ValueError('Data inválida')


# Requisito 8
def search_by_source(source):
    news_in_db = search_news({"sources": re.compile(source, re.IGNORECASE)})
    # usando mesma lógica do requisito 6

    news_tuple = [(news['title'], news['url']) for news in news_in_db]
    return news_tuple


# Requisito 9
def search_by_category(category):
    news_in_db = search_news(
        {"categories": re.compile(category, re.IGNORECASE)})
    # usando mesma lógica do requisito 6

    news_tuple = [(news['title'], news['url']) for news in news_in_db]
    return news_tuple
