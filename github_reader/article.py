class Article:
    def __init__(self, id, audio_download_url):
        self._id = id
        self._audio_download_url = audio_download_url
        self._original_article_url = 'https://time.geekbang.org/column/article/{0}'

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def audio_download_url(self):
        return self._audio_download_url

    @audio_download_url.setter
    def audio_download_url(self, url):
        self._audio_download_url = url

    @property
    def original_article_url(self):
        return self._original_article_url.format(self.id)
