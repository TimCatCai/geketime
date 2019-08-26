import json

from github_reader.article import Article
from github_reader.geektime_page_lessen import GeektimePageLessen


def go(num, original_article_url=None, audio_download_url=None):
    # 1. 原始文档  添加评论
    target_file_path = "files/course{0}.html".format(num)
    # 2. 删除图片数据，添加评论
    file_without_img_src = 'files/course{0}_beatify_without_img_src.html'.format(num)
    headers_content_file_path = 'files/geektime_java_concurrent_headers_contents.txt'
    geektime = GeektimePageLessen(target_file_path, file_without_img_src, headers_content_file_path)
    geektime.complete_comment_zone(original_article_url)
    geektime.delete_all_img_content()
    if audio_download_url is not None and original_article_url is not None:
        geektime.add_audio_download_url(audio_download_url, original_article_url)
    geektime.save()

    # 3. 删除所有样式 添加评论（为方便客户端读取）
    file_without_style = 'files/course{0}_beatify_without_style.html'.format(num)
    geektime = GeektimePageLessen(file_without_img_src, file_without_style, headers_content_file_path)
    geektime.delete_all_style()
    geektime.delete_meta_link()
    geektime.save()


def get_column_articles(json_file_path):
    with open(json_file_path, encoding='utf-8') as json_file:
        json_content = json.loads(json_file.read())
        print(json_content)
    articles = []
    if json_content is not None:
        if json_content.get('data') is not None:
            data = json_content['data']
            data_list = data['list']
            for article in data_list:
                id = article['id']
                audio_down_url = article.get('audio_download_url', '')
                articles.append(Article(id, audio_down_url))

    return articles


java_concurrent_content_json_path = 'files/java_concurrent_json.txt'
articles_for_java_concurrent = get_column_articles(java_concurrent_content_json_path)
base_search_url = 'https://time.geekbang.org/column/article/{0}'
count = 0
for an_article in articles_for_java_concurrent:
    print(str(count) + ': ' + str(an_article.id))
    print(str(count) + ': ' + base_search_url.format(an_article.id))
    print(str(count) + ': ' + str(an_article.audio_download_url))
    count += 1

for count in range(2, 7):
    if len(articles_for_java_concurrent) >= count + 1:
        original_article_url = base_search_url.format(articles_for_java_concurrent[count].id)
        audio_download_url = articles_for_java_concurrent[count].audio_download_url

        go(count - 1, original_article_url, audio_download_url)
# go(5)
