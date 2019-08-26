import time

from github_reader.comment import Comment
from github_reader.reply import Reply
from geektime.get_website_data import GetWebsiteData


class GetComments:
    def __init__(self, getter, aid, prev):
        self._getter = getter
        self._aid = aid
        self._prev = prev

    def get_comment(self, payload):
        repeat_time = 5
        wait_time = 3
        json_back = None
        go_on = True
        for i in range(0, repeat_time):
            self._getter.post(payload=payload)
            json_back = self._getter.get_response_json()
            if json_back is not None \
                    and json_back.get('data') is not None \
                    and not len(json_back['data']) == 0:
                break
            else:
                # 循环结束时还没有得到合适的json数据，不继续进行，即不进行获取评论操作
                if repeat_time == repeat_time - 1:
                    go_on = False
                # 否则等待wait_time后再次发起请求
                else:
                    time.sleep(wait_time)

        comments = None
        if go_on:
            comments = []
            data = json_back['data']
            data_list = data['list']
            for a_comment_json in data_list:
                if a_comment_json is not None:
                    # 获取评论的回复内容
                    replys = []
                    if a_comment_json.get('replies') is not None:
                        for reply in a_comment_json['replies']:
                            replys.append(Reply(reply['ctime'], reply['user_name_real'], reply['content'], reply['user_name']))

                    # 获取评论
                    comment = Comment(
                        a_comment_json['comment_ctime'],
                        a_comment_json['user_name'],
                        replys,
                        a_comment_json['comment_content'],
                        a_comment_json['score']
                    )
                    comments.append(comment)
        return comments

    def get_comments(self):
        payload = {'aid': self._aid, 'prev': self._prev}
        comments_list = self.get_comment(payload)
        if comments_list is None:
            return None
        for comment in comments_list:
            print(comment)
            print('-------------------------------')
        prev = comments_list[-1].comment_ctime
        payload['prev'] = prev
        new_comments_list = self.get_comment(payload)
        if new_comments_list is None:
            return None
        for comment in new_comments_list:
            print(comment)
            print('-------------------------------')

        while not comments_list[0].comment_ctime == new_comments_list[0].comment_ctime:
            comments_list += new_comments_list
            prev = new_comments_list[-1].comment_ctime
            payload['prev'] = prev
            new_comments_list = self.get_comment(payload)
            if new_comments_list is None:
                break
            for comment in new_comments_list:
                print(comment)
                print('-------------------------------')

        return comments_list


# headers_file_path = 'files/geektime_java_concurrent_headers_contents.txt'
# url = 'https://time.geekbang.org/serv/v1/comments'
# geektime = GetWebsiteData(headers_file_path, url)
# aid = "83267"
# pre = "0"
# comments = get_comments(geektime, aid, pre)
# for comment in comments:
#     print(comment)
#     print()
