from pathlib import Path
import requests
import shutil
from bs4 import BeautifulSoup
import bs4
import time
import socket
import urllib3
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "close",
    "Cookie": "_gauges_unique_hour=1;_gauges_unique_day=1;_gauges_unique_month=1;_gauges_unique_year=1;_gauges_unique=1",
    "Referer": "http://www.cnu.cc",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
                  "(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
}


def down_picture(url, picture_store_dir=Path.cwd()):
    # 判断传入路径是否存在，存在则使用该路径否则新建该路径
    if not Path.exists(picture_store_dir) or not Path.is_dir(picture_store_dir):
        Path.mkdir(picture_store_dir, parents=True)
    downloaded = False
    try:
        pic_content = requests.get(url, headers=headers, stream=True, timeout=1)
        if pic_content.status_code == 200:
            pic_name = Path(url).name.split(u'?')[0]
            pic_store_path = Path.joinpath(picture_store_dir, pic_name)
            with pic_store_path.open("wb") as pic:
                pic_content.raw.deconde_content = True
                shutil.copyfileobj(pic_content.raw, pic)
            print('已下载图片：' + pic_name)
            downloaded = True
    except (requests.exceptions.RequestException, socket.timeout,urllib3.exceptions.ReadTimeoutError):
        print("下载超时，跳过下载")
    return downloaded


def parse_desire_content(content, property_string=''):
    if isinstance(content, bs4.element.Tag):
        if property_string in content.attrs:
            result = content[property_string]
        else:
            result = "unknown"
    elif isinstance(content, bs4.element.ResultSet):
        if len(content) != 0:
            result = content[0].string.strip()
            if len(result) == 0:
                result = 'unknown'
        else:
            result = 'unknown'
    else:
        result = 'known'

    return result


def download_one_category(url, pictures_store_dir=Path.cwd()):
    # 爬取网站的html源码
    html_content = None
    try:
        html_content = requests.get(url, headers=headers)
    except (requests.exceptions.RequestException, socket.timeout, urllib3.exceptions.ReadTimeoutError):
        print("html源码爬取超时")

    pic_downloaded_num = 0
    if not (html_content is None):

        # 获取所有< div class ="grid-item work-thumbnail" >标签，其包含了图片的地址
        pic_content_tags = BeautifulSoup(html_content.text.replace('\n', ''), 'lxml')
        works_list = []
        for pic_content_tag in pic_content_tags.find_all('div', class_="grid-item work-thumbnail"):
            # <a href = "http://www.cnu.cc/works/364609" class ="thumbnail" target="_blank" >
            #     <div class ="title" >
            #         IMPETUOUS.
            #     </ div >
            #      <div class ="author" >
            # 快门怪咖
            #      < / div >
            #     < img src = "http://img.cnu.cc/uploads/images/flow/1907/23/64603963141735a08d0624d34
            #     e303c08.jpg?width=2832&amp;height=4240" alt = "IMPETUOUS." >
            # < / a >
            # a标签的引用
            pic_content_tag_a = pic_content_tag.a

            # 在a标签的属性中获取作者的url
            author_website_url = parse_desire_content(pic_content_tag_a, 'href')

            # 在a标签中获取类型为"author"的div标签，再解析得到的标签，得到标签的内容
            author_content = pic_content_tag_a.find_all('div', class_="author")
            author = parse_desire_content(author_content)

            # 在a标签中获取类型为"title"的div标签，再解析得到的标签，得到标签的内容
            title_content = pic_content_tag_a.find_all('div', class_="title")
            title = parse_desire_content(title_content)
            # 在a标签中获取img标签，并得到图片所对应的链接
            img_link = parse_desire_content(pic_content_tag.a.img, 'src')
            works_list.append(Work(author, author_website_url, title, img_link))
            print('--------------------------')
            print("作者：" + author)
            print("作者url：" + author_website_url)
            print("内容标题：" + title)
            print("图片链接：" + img_link)
            print('--------------------------')
        for work in works_list:
            if down_picture(work.img_link, pictures_store_dir):
                pic_downloaded_num += 1
    return pic_downloaded_num


class Work:
    def __init__(self, author, author_website_url, title, img_link):
        self.author = author
        self.author_url = author_website_url
        self.title = title
        self.img_link = img_link


currentPath = Path.cwd()
pic_dir = Path.joinpath(currentPath, 'cnu')
url = "http://www.cnu.cc/discoveryPage/hot-%E4%BA%BA%E5%83%8F?page="
pic_downloaded_total = 0
for page in range(5):
    pic_downloaded_total += download_one_category(url + str(page + 1), pic_dir)
    print("已下载图片数量：" + str(pic_downloaded_total))
    time.sleep(3)
