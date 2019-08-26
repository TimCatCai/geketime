import json
from geektime.get_website_data import GetWebsiteData
from pathlib import Path, PurePath
import re
import time
from urllib.parse import quote


def go(keyword):
    headers_file_path = 'toutiao_headers_contents.txt'
    url = "https://www.toutiao.com/api/search/content/?aid=24&app_name=web_" \
          "search&offset={0}&format=json&keyword=" + quote(keyword) +\
          "&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis" \
          "&timestamp=1566625465021"
    print(url)
    go_on = True
    repeat_time = 10
    count = 0
    step = 0
    offset = 0
    pages = 20
    sleep_time = 3
    toutiao_page = GetWebsiteData(headers_file_path, url.format(offset))
    response = None
    while go_on:
        response = toutiao_page.get()
        print("offset: " + str(offset))
        if response is not None:
            new_file = 'toutiao_content.txt'
            beautify_result = toutiao_page.get_response_json_text()
            with open(new_file, 'w', encoding='utf-8') as file:
                file.write(beautify_result)
            response_list_data = toutiao_page.get_response_json()['data']
            print("count: " + str(toutiao_page.get_response_json()['count']))
            # print(response_list_data)
            image_dict = {}

            if response_list_data is not None:
                for item in response_list_data:
                    title = item.get('title')
                    page_image_list = item.get('image_list')

                    if page_image_list is not None and title is not None:
                        title_replace_patten = r'[\/:*?"<>|]'
                        title = re.sub(title_replace_patten, '', title)
                        image_dict[title] = page_image_list

                for image_title, image_list in image_dict.items():
                    # 为图片创建存储路径
                    images_dir = Path('pictures').joinpath('美图')
                    if not images_dir.exists():
                        Path.mkdir(images_dir, parents=True)
                    toutiao_page.get_all_image_in_list(image_title, image_list, images_dir)
                offset += pages
                step = 0
                count = 0
                toutiao_page.url = url.format(offset)
            else:
                step += 1
                count += step
                time.sleep(sleep_time)
        else:
            go_on = False

        # 当返回json的data字段为None的次数超过repeat_time 则退出循环
        print("offset repeat time: " + str(count))
        if count >= repeat_time:
            go_on = False

        # print(specify_page_urls[0])
        # specify_page = GetWebsiteData(headers_file_path, specify_page_urls[2])
        # specify_page_response = specify_page.get()
        # specify_page.get_all_img('div', class_string='bui-box container')


go(u'美女图片')

