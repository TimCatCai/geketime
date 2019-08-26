import requests
from bs4 import BeautifulSoup

# 01
# url = 'http://httpbin.org/get'
# data = {"key": "value", "abc": "xyz"}
# response = requests.get(url, data)
# print(response.json())

# 02

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "close",
    "Cookie": "_gauges_unique_hour=1;_gauges_unique_day=1;_gauges_unique_month=1;_gauges_unique_year=1;_gauges_unique=1",
    "Referer": "http://www.infoq.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
                  "(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
}


def craw(url):
    with open("infoq_news.html", encoding='utf-8') as fl:
        text = fl.read()

    response = requests.get(url, headers=headers)
    content = BeautifulSoup(response.text.replace('\n', ''), 'lxml')

    for card_items__content in content.find_all("div", class_="items__content"):
        card_items = card_items__content.div.ul.contents
        while ' ' in card_items:
            card_items.remove(' ')
        # all <li> tag
        for card_item in card_items:
            card__data = card_item.div.div
            card__data_contents = card_item.div.div.contents
            while ' ' in card__data_contents:
                card__data_contents.remove(' ')

            card__topics_a_tag = card__data_contents[0].span.a
            card__topics = card__topics_a_tag.string.strip()
            card__topics_href = card__topics_a_tag['href']

            card__title_a_tag = card__data.h3.a
            card__title = card__title_a_tag.string.strip()
            card__title_href = card__title_a_tag['href']

            card__excerpt = card__data.p.string.strip()
            print("topic: " + card__topics + " href: " + card__topics_href)
            print("title: " + card__title + " href: " + card__title_href)
            print("excerpt: " + card__excerpt)
            print()


url = 'http://www.infoq.com/news'
for i in range(10):
    craw(url + str(i * 15) + '/')
