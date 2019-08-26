import requests
from bs4 import BeautifulSoup
import json
from geektime.get_website_data import GetWebsiteData

headers_file_path = 'toutiao_headers_contents.txt'
url = "https://www.toutiao.com/api/search/content/?aid=24" \
      "&app_name=web_search&offset={0}&format=json" \
      "&keyword=%E7%BE%8E%E5%A5%B3%E5%9B%BE%E7%89%87&autoload=true" \
      "&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis" \
      "&timestamp=1566625465021"
go_on = True
while go_on:
    toutiao_page = GetWebsiteData(headers_file_path, url)
    response = toutiao_page.get()
    new_file = 'toutiao_content.txt'
    response_json = toutiao_page.get_response_json()
    for item in response_json['data']:
        print(item['article_url'])
    with open(new_file, 'w', encoding='utf-8') as file:
        beautify_result = toutiao_page.get_response_json_text()
        file.write(beautify_result)

