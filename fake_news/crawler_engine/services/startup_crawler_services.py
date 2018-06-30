from ..constants import NEWS_STATUS


class StartupCrawlerServices:
    def __init__(self):
        pass

    def not_thread_safe(self):
        print('test')

    def simple_ping_from_different_app(self, data):
        data += 'test'
        return data

