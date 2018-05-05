from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django.conf.urls import url
from rest_framework.exceptions import APIException
from rest_framework import status
import datetime

from .api_base import ApiBase
from ..services import StartupServices
# from fake_news.fake_news_api.services import StartupServices


# Create your views here.
class StartupViewSet(ModelViewSet, ApiBase):
    permission_classes = (AllowAny,)

    startup_services = StartupServices()

    @classmethod
    def get_router(cls):
        urlpatterns = [
            url(r'ping/$', cls.as_view({'get': 'ping'})),
            url(r'ping_using_services/$', cls.as_view({'get': 'ping_using_services'})),
            url(r'ping_using_other_app_services/$', cls.as_view({'get': 'ping_using_other_app_services'})),
            url(r'ping_raise_error/$', cls.as_view({'get': 'ping_raise_error'})),
        ]

        return urlpatterns

    def ping(self, request, *args, **kwargs):
        now = datetime.datetime.utcnow()
        data = 'SERVER ON {0}'.format(now.strftime('%Y-%m-%d %H:%M'))

        return self.as_success(data)

    def ping_using_services(self, request, *args, **kwargs):
        now = datetime.datetime.utcnow()
        data = 'SERVER ON {0}'.format(now.strftime('%Y-%m-%d %H:%M'))

        response_text = self.startup_services.simple_ping(data)
        return self.as_success(response_text)

    def ping_using_other_app_services(self, request, *args, **kwargs):
        now = datetime.datetime.utcnow()
        data = 'SERVER ON {0}'.format(now.strftime('%Y-%m-%d %H:%M'))

        response_text = self.startup_services.simple_ping_from_other_app(data)
        return self.as_success(response_text)

    def ping_raise_error(self, request, *args, **kwargs):
        self.startup_services.ping_error_message()
        return self.as_success('test')
