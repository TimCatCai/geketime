class Reply:
    def __init__(self, ctime, user_name_real, content, user_name):
        self.ctime = ctime
        self.user_name_real = user_name_real
        self.content = content
        self.user_name = user_name

    def __str__(self) -> str:
        return 'ctime = {0}' \
               'user_name_real = {1}' \
               'content = {2}' \
               'user_name = {3}' \
                .format(self.ctime, self.user_name_real, self.content, self.user_name)
