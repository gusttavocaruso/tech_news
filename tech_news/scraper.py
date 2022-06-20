import requests
import parsel
import time
from tech_news.database import create_news


# Requisito 1:
def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        time.sleep(1)
    except (requests.HTTPError, requests.ReadTimeout):
        return None

    return response.text


# Requisito 2
def scrape_novidades(html_content):

    selector = parsel.Selector(text=html_content)
    url_list = selector.css(
        "div.tec--list a.tec--card__title__link::attr(href)").getall()

    return url_list


# Requisito 3
def scrape_next_page_link(html_content):

    selector = parsel.Selector(text=html_content)
    url_next_page = selector.css(
        "div.tec--list a.tec--btn--lg::attr(href)").get()

    return url_next_page


# Requisito 4
def scrape_noticia(html_content):
    selector = parsel.Selector(text=html_content)

    url = selector.css("link[rel=canonical]::attr(href)").get()
    title = selector.css(".tec--article__header__title::text").get()
    timestp = selector.css(".tec--timestamp__item time::attr(datetime)").get()
    sources = selector.css('div.z--mb-16 a.tec--badge::text').getall()
    categories = selector.css('div#js-categories a.tec--badge::text').getall()
    share = selector.css("div.tec--toolbar__item::text").get()
    writer = selector.css(
            "div.tec--author__info *::text").get() or selector.css(
            "div.tec--timestamp__item:last-child *::text").get()
    comments = selector.css(
        "div.tec--toolbar__item button::attr(data-count)").get()
    summary = selector.css(
        'div.tec--article__body > p:first-child *::text').getall()

    news_info = {
        "url": url,
        "title": title,
        "timestamp": timestp,
        "writer": str(writer).strip(),
        "shares_count": int(share.split(" ")[1]) if share else 0,
        "comments_count": int(comments) if type(comments) == str else 0,
        "summary": str().join(summary),
        "sources": [src.strip() for src in sources],
        "categories": [category.strip() for category in categories],
    }

    return news_info


# Requisito 5
def get_tech_news(amount):
    news = []
    url = 'https://www.tecmundo.com.br/novidades'

    while len(news) < amount:
        html = fetch(url)
        news_links = scrape_novidades(html)

        for link in news_links:
            noticia_html = fetch(link)
            news.append(scrape_noticia(noticia_html))
            if len(news) == amount:
                break

        url = scrape_next_page_link(html)

    create_news(news)
    return news


# if __name__ == "__main__":
#     print(get_tech_news(20))
