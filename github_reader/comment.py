class Comment:
    def __init__(self, comment_ctime, user_name, replies, comment_content, score):
        self.comment_ctime = comment_ctime
        self.user_name = user_name
        self.replies = replies
        self.comment_content = comment_content
        self.score = score

    def __str__(self) -> str:
        return 'comment_ctime = {0}\n' \
               'user_name = {1}\n' \
               'replies = {2}\n' \
               'comment_content ={3}\n' \
               'score ={4}\n' \
               .format(self.comment_ctime,
                       self.user_name,
                       self.replies,
                       self.comment_content,
                       self.score)
