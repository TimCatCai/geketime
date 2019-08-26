import json
import re
from pathlib import Path
from github_reader.get_website_data import GetWebsiteData


def get_audios():
    bian = GetWebsiteData(headers_path, url)
    # bian.post(payload)
    # print(bian.get_response_json())
    json_path = 'files/interpreter_json.txt'
    with open(json_path, encoding='utf-8') as json_file:
        json_content = json_file.read()
    json_back = json.loads(json_content)
    audio_list = json_back['data']['list']
    save_dir = Path('files/编译原理之美')

    if not save_dir.exists():
        save_dir.mkdir(parents=True)

    for audio_info in audio_list:
        title_replace_patten = r'[\/:*?"<>|]'
        article_title = re.sub(title_replace_patten, '', audio_info['article_title'])
        audio_download_url = audio_info['audio_download_url']
        save_path = Path(save_dir).joinpath(article_title+'.mp3')
        print(article_title)
        print(audio_download_url)
        bian.save_binary_file(save_path, audio_download_url)


headers_path = 'files/java_concurrent_json.txt'
url = "https://time.geekbang.org/serv/v1/column/articles"
payload = {
    'cid': '100023901',
    'order': "earliest",
    'prev': 0,
    'sample': False,
}
bian = GetWebsiteData(headers_path, url)
bian.post(payload)
print(bian.get_response_json())
