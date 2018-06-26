# from ...crawler_engine.services import StartupCrawlerServices
# import crawler_engine.services
from ..constants import ErrorDefine
from ..infrastructures import ApiCustomException

from crawler_engine.services import StartupCrawlerServices


class StartupServices:
    def __init__(self):
        self.startup_crawler_services = StartupCrawlerServices()
        # self.startup_crawler_services = crawler_engine.services.StartupCrawlerServices()

    def simple_ping(self, data):
        return data

    def simple_ping_from_other_app(self, data):
        ping = self.startup_crawler_services.simple_ping_from_different_app(data)
        return ping

    def ping_error_message(self):
        raise ApiCustomException(ErrorDefine.LOGIN_FAIL)

