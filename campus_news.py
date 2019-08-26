import requests
from bs4 import BeautifulSoup
url = 'http://news.gdut.edu.cn'
response = requests.get('http://news.gdut.edu.cn/ViewArticle.aspx?articleid=141318')

response_soup = BeautifulSoup(response.text, "lxml")
print(response_soup.prettify())
# hotNews = response_soup.find('div', id="hot_news")
# hotNewsTable = hotNews.ul.contents
#
# while '\n' in hotNewsTable:
#     hotNewsTable.remove('\n')
#
# for news_item in hotNewsTable:
#     print('title: ' + news_item.a['title'])
#     print('href: ' + news_item.a['href'])
#     print()
#
# print(hotNewsTable)





