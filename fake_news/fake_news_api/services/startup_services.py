# from ...crawler_engine.services import StartupCrawlerServices
from crawler_engine.services import StartupCrawlerServices


class StartupServices:
    def __init__(self):
        self.startup_crawler_services = StartupCrawlerServices()

    def simple_ping(self, data):
        return data

    def simple_ping_from_other_app(self, data):
        ping = self.startup_crawler_services.simple_ping_from_different_app(data)
        return ping