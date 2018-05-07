from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django.conf.urls import url
from rest_framework.exceptions import APIException
from rest_framework import status
import datetime

from .api_base import ApiBase
from ..services import NaiveBayesServices

from crawler_engine.serializers import BaseNewsDetailSerializer, DescriptionSerializer


# Create your views here.
class NaiveBayesViewSet(ModelViewSet, ApiBase):
    permission_classes = (AllowAny,)

    naive_bayes_services = NaiveBayesServices()

    @classmethod
    def get_router(cls):
        urlpatterns = [
            url(r'stop_word_list/$', cls.as_view({'get': 'stop_word_list'})),
            url(r'preprocessor/$', cls.as_view({'post': 'preprocessor'})),
        ]

        return urlpatterns

    def get_serializer_class(self):
        if self.action == 'preprocessor':
            return DescriptionSerializer

        return BaseNewsDetailSerializer

    def stop_word_list(self, request, *args, **kwargs):
        stop_word_list, list_sign = self.naive_bayes_services.stop_word_list()
        return self.as_success(stop_word_list)

    def preprocessor(self, request, *args, **kwargs):
        news_detail = request.data['details']
        news_preprocess_string = self.naive_bayes_services.preprocessor(news_detail)
        return self.as_success(news_preprocess_string)
