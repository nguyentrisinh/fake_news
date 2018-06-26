from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django.conf.urls import url
from rest_framework.exceptions import APIException
from rest_framework import status
import datetime
import time

from .api_base import ApiBase
from ..services import SVMServices
from crawler_engine.serializers import BaseNewsDetailSerializer, DescriptionSerializer, ListNewsDetailSerializer, \
    PredictedResultSerializer

# Create your views here.
class SVMViewSet(ModelViewSet, ApiBase):
    permission_classes = (AllowAny,)

    svm_services = SVMServices()

    @classmethod
    def get_router(cls):
        urlpatterns = [
            url(r'test_simple_svm/$', cls.as_view({'get': 'test_simple_svm'})),
            url(r'test_preprocessor/$', cls.as_view({'get': 'test_preprocessor'})),
            url(r'test_pipeline/$', cls.as_view({'get': 'test_pipeline'})),
            url(r'test_pipeline_real_classify/$', cls.as_view({'get': 'test_pipeline_real_classify'})),
            url(r'svm_classify/$', cls.as_view({'post': 'svm_classify'})),
        ]

        return urlpatterns

    def get_serializer_class(self):
        if self.action == 'svm_classify':
            return ListNewsDetailSerializer

        return BaseNewsDetailSerializer

    def test_simple_svm(self, request, *args, **kwargs):
        data = self.svm_services.test_simple_svm()
        return self.as_success(data)

    def test_preprocessor(self, request, *args, **kwargs):
        data = self.svm_services.test_preprocessor()

        return self.as_success(data)

    def test_pipeline(self, request, *args, **kwargs):
        data = self.svm_services.test_pipeline()

        return self.as_success(data)

    def test_pipeline_real_classify(self, request, *args, **kwargs):
        data = self.svm_services.test_pipeline_real_classify()

        return self.as_success(data)

    def svm_classify(self, request, *args, **kwargs):
        details = request.data['details']
        data = request.data

        # Process classify
        start_time = time.time()
        predicted_result = self.svm_services.pipeline_svm_classify(details)
        elapsed_time = time.time() - start_time

        # return data
        return_data = {
            'predicted_result': predicted_result,
            'elapsed_time': 'The process take {} seconds'.format(str(elapsed_time))
        }

        # return_data['predicted_result'] = self.naive_bayes_services.naive_bayes_classify_api(details)
        serializer = PredictedResultSerializer(return_data)

        # serializer = ListNewsDetailSerializer(request.data)
        return self.as_success(serializer.data)