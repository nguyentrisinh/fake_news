from django.apps import AppConfig


class CrawlerEngineConfig(AppConfig):
    name = 'fake_news.crawler_engine'

    def ready(self):
        pass
