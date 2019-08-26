import requests
from requests import exceptions
import json
from bs4 import BeautifulSoup
import re
from pathlib import Path, PurePath
import threading


class GetWebsiteData:
    def __init__(self, header_file_path, url, header_append=None):
        self._headers = format_headers(header_file_path)
        if header_append is not None:
            for key, value in header_append.items():
                self._headers[key] = value

        self._url = url
        self._response = None
        self._timeout = 1
        self._html = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def response(self):
        return self._response

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        self._timeout = timeout

    def get(self):
        self._response = self._request_get(self._url)
        return self._response

    def post(self, url='', payload={}):
        response = None
        try:
            response = requests.post(self._url, headers=self._headers, timeout=self._timeout, json=payload)
        except requests.exceptions.Timeout as e:
            print("请求超时：%s" % {str(e)})
        except requests.exceptions.RequestException as e:
            print("网络异常: " + str(e))
        except Exception as e:
            print("不可知错误: %s" % {e})
        self._response = response
        return response

    def _request_get(self, url):
        response = None
        try:
            response = requests.get(url, headers=self._headers, timeout=self._timeout)
        except requests.exceptions.Timeout as e:
            print("请求超时：%s" % {str(e)})
        except requests.exceptions.RequestException as e:
            print("网络异常: " + str(e))
        except Exception as e:
            print("不可知错误: %s" % {e})

        return response

    def get_response_json(self):
        if self._response is not None:
            return self._response.json()
        else:
            return None

    def get_response_json_text(self):
        if self._response is not None:
            return json.dumps(json.loads(self._response.text),
                              sort_keys=True, indent=4, separators=(',', ':'))
        else:
            return None

    # 头条的机制是，在搜索列表中预加载对应新闻的所有图片链接，链接保存在返回json数据的image_list字段中
    # http://p3-tt.byteimg.com/list/pgc-image/1522829520265c754030f23 为小图链接，即image_list数据
    # http://p3-tt.byteimg.com/large/pgc-image/1522829520265c754030f23 为大图链接，
    # 保存在large_image_url字段中，作为读取模板
    def get_all_img(self, container_tag_string, path='.', class_string=''):
        if self._html is None and self._response is not None:
            self._html = BeautifulSoup(self._response.text, 'lxml')
            # print(self._html.prettify())
            with open('specify.html', 'w') as page_file:
                page_file.write(self._html.prettify())

        container_tags = self._html.find_all(container_tag_string, class_=class_string)
        # print(container_tags)
        for container_tag in container_tags:
            print(type(container_tag))
            imgs = container_tag.find_all('img')
            print(imgs)
            for img in imgs:
                print(img['src'])

    def get_all_image_in_list(self, title, image_list, images_dir):
        thread = threading.Thread(target=self.down_img_run, args=(title, image_list, images_dir))
        thread.start()

    def down_img_run(self, title, image_list, images_dir):
        print(title)
        # 每张图片以新闻标题为加计数为文件名
        count = 1
        image_name = '{0}{1}.png'
        for small_image_url in image_list:
            pattern = r'list(/\d*x\d*)?'
            large_image_url = re.sub(pattern, 'large', small_image_url['url'])
            # print(large_image_url)
            image_path = Path(images_dir).joinpath(image_name.format(title, count))
            self.save_img(image_path, large_image_url)
            count += 1

    def save_img(self, path, url):
        response = self._request_get(url)
        if response is not None:
            with open(path, 'wb') as image:
                image.write(response.content)


def format_headers(file_path):
    with open(file_path, encoding='utf-8') as headers_file:
        header_text = headers_file.read()
    result = {}
    header_items = header_text.split('\n')
    for item in header_items:
        item_content = item.split(': ')
        item_name = item_content[0]
        item_set = item_content[1]
        result[item_name] = item_set
    return result

