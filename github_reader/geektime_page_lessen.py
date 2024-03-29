import re
from bs4 import BeautifulSoup
from geektime.get_website_data import GetWebsiteData
from github_reader.get_geektime_comments import GetComments


class GeektimePageLessen:

    def __init__(self, target_path, save_path, headers_file_path):
        self._target_file_path = target_path
        self._save_file_path = save_path
        self._html_soup = None
        self._headers_file_path = headers_file_path
        self.init()

    def init(self):
        with open(self._target_file_path, encoding="utf-8") as file:
            contents = file.read()
            self._html_soup = BeautifulSoup(contents, 'lxml')

    def complete_comment_zone(self, base_url=None):
        comment_zone_possible = self._html_soup.find_all('ul')
        page_url = None
        base = self._html_soup.find('base')
        save_page = self._html_soup.find_all('meta')
        if base is not None:
            page_url = base['href']
        if page_url is None and save_page is not None and not len(save_page) == 0:
            for meta in save_page:
                meta_content = meta.get('content')
                if meta_content is not None and re.match(r'http://', meta_content) is not None:
                    page_url = meta_content

        with open('files/comment_li.html', encoding='utf-8') as li_file:
            insert_li_content = li_file.read()

        if comment_zone_possible is not None and not len(comment_zone_possible) == 0:
            comment_zone = comment_zone_possible[-1]
            if page_url is not None:
                self.__insert_new_comment(page_url, comment_zone, insert_li_content)
            else:
                if base_url is not None:
                    self.__insert_new_comment(base_url, comment_zone, insert_li_content)
                else:
                    self.delete_collapse()
                    print(base_url)
                    print('本文件标题：' + self._html_soup.head.title.string)
                    print('目标文件url：' + str(base_url))
                    print('页面文件未找到url')
                    print('或未输入对应页面地址或输入地址对应的页面标题不一致')

    def __insert_new_comment(self, page_url, comment_zone, insert_li_content):
        comment_zone.clear()
        comment_url = 'https://time.geekbang.org/serv/v1/comments'
        header_append = {'Referer': page_url}
        geektime = GetWebsiteData(self._headers_file_path, comment_url, header_append)
        aid = page_url.split('/')[-1]
        prev = "0"
        print(aid)
        get_comment = GetComments(geektime, aid, prev)
        comments = get_comment.get_comments()
        print(comments)
        if comments is not None:
            for comment in comments:
                li_tag_soup = BeautifulSoup(insert_li_content, 'lxml')
                # 评论者名字
                user_name_tag = li_tag_soup.find('span', class_='username')
                user_name_tag_content = li_tag_soup.new_tag('strong')
                user_name_tag_content.string = comment.user_name
                user_name_tag.insert_after(user_name_tag_content)
                # 添加评论内容
                bd_tag = li_tag_soup.find('div', class_='bd')
                bd_tag_content = BeautifulSoup(comment.comment_content, 'lxml')
                bd_tag.insert_after(bd_tag_content)
                # 作者回复内容
                p_tag = li_tag_soup.find('p', class_="reply-content")
                replies = ''
                for reply in comment.replies:
                    replies += reply.content
                if not len(replies) == 0 and p_tag is not None:
                    p_tag.clear()
                    p_tag_content = BeautifulSoup(replies, 'lxml')
                    p_tag.insert_after(p_tag_content)
                comment_zone.append(li_tag_soup.li)
        else:
            self.delete_collapse()

    # 爬回来的数据异常，暂时抛弃验证功能
    def __verify_page(self, object_title, page_url):
        getter = GetWebsiteData(self._headers_file_path, page_url)
        response = getter.get()
        result = False
        if response is not None:
            print(response.text)
            soup = BeautifulSoup(response.content, 'lxml')
            print(soup.prettify())
            # page_title = soup.find_all('meta', id='metakeywords')[0]['content']
            # print('目标url title ' + page_title)
            # if page_title == object_title:
            #     result = True
        return result

    def delete_collapse(self):
        collapse_span_tags = self._html_soup.find_all('span')
        for collapse_span_tag in collapse_span_tags:
            if collapse_span_tag.string == u'展开':
                collapse_span_tag.decompose()

    def delete_all_style(self):
        paths = self._html_soup.find_all('path')
        for a_path in paths:
            a_path.decompose()

        svgs = self._html_soup.find_all('svg')
        for svg in svgs:
            svg.decompose()

        scrip_tags = self._html_soup.find_all('script')
        for scrip_tag in scrip_tags:
            scrip_tag.decompose()

        styles = self._html_soup.find_all('style')
        for style in styles:
            style.decompose()

        symbols = self._html_soup.find_all('symbol')
        for symbol in symbols:
            symbol.decompose()

    def delete_all_img_content(self):
        img_tags = self._html_soup.find_all('img')
        img_link = None
        for tag in img_tags:
            if tag.get('src') is not None:
                # 若src属性是一个链接的会将链接保存下来
                if re.match('http', tag['src']) is not None:
                    img_link = tag['src']
                # 不管是什么情况，src的内容都要改为picture, 不然页面会进行加载
                tag['src'] = 'picture'

            if img_link is None and tag.get('data-savepage-src') is not None:
                img_link = tag['data-savepage-src']

            if img_link is not None:
                center = self._html_soup.new_tag('center')
                a = self._html_soup.new_tag('a')
                a.attrs = {'href': img_link}
                a.string = u'图片链接'
                center.insert(0, a)
                tag.insert_after(center)

    def delete_meta_link(self):
        metas = self._html_soup.find_all('meta')
        for meta in metas:
            if meta.get("charset") is None:
                meta.decompose()
        links = self._html_soup.find_all('link')
        for link in links:
            link.decompose()

    def save(self):
        with open(self._save_file_path, "w", encoding="utf-8") as save_file:
            save_file.write(self._html_soup.prettify())

    def add_audio_download_url(self, audio_url, original_article_url=None):
        print(original_article_url)
        img_tag = self._html_soup.find('img')
        center_tag = self._html_soup.new_tag('center')
        audio_a_tag = self._html_soup.new_tag('a')
        audio_a_tag.attrs = {'href': audio_url}
        audio_a_tag.string = '音频链接'
        if original_article_url is not None:
            br_tag = self._html_soup.new_tag('br')
            article_a_tag = self._html_soup.new_tag('a')
            article_a_tag.attrs = {'href': original_article_url}
            article_a_tag.string = '原文档链接'
            center_tag.append(article_a_tag)
            center_tag.append(br_tag)
        # 将标签插入相应位置
        center_tag.append(audio_a_tag)
        img_tag.replace_with(center_tag)
