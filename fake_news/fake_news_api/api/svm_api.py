from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django.conf.urls import url
from rest_framework.exceptions import APIException
from rest_framework import status
import datetime
import time

from .api_base import ApiBase
from ..services import SVMServices
from ..serializers import AccuracySerializer
from crawler_engine.serializers import BaseNewsDetailSerializer, DescriptionSerializer, ListNewsDetailSerializer, \
    PredictedResultSerializer, FakeNewsPredictedResultSerializer

# Create your views here.
class SVMViewSet(ModelViewSet, ApiBase):
    permission_classes = (AllowAny,)

    svm_services = SVMServices()

    @classmethod
    def get_router(cls):
        urlpatterns = [
            url(r'test_simple_svm/$', cls.as_view({'get': 'test_simple_svm'})),
            url(r'test_preprocessor/$', cls.as_view({'get': 'test_preprocessor'})),
            url(r'test_pipeline_real_classify/$', cls.as_view({'get': 'test_pipeline_real_classify'})),
            url(r'accuracy_validate/$', cls.as_view({'get': 'accuracy_validate'})),
            url(r'svm_classify/$', cls.as_view({'post': 'svm_classify'})),
            url(r'fake_news_classify/$', cls.as_view({'post': 'fake_news_classify'})),
            # Preprocessor and save csv file of fake news training data
            url(r'save_preprocessor_to_csv/$', cls.as_view({'get': 'save_preprocessor_to_csv'})),
        ]

        return urlpatterns

    def get_serializer_class(self):
        if self.action == 'svm_classify':
            return ListNewsDetailSerializer

        if self.action == 'fake_news_classify':
            return ListNewsDetailSerializer

        return BaseNewsDetailSerializer

    def test_simple_svm(self, request, *args, **kwargs):
        data = self.svm_services.test_simple_svm()
        return self.as_success(data)

    def test_preprocessor(self, request, *args, **kwargs):
        data = self.svm_services.test_preprocessor()

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

    def fake_news_classify(self, request, *args, **kwargs):
        details = request.data['details']

        # Process classify
        start_time = time.time()
        predicted_result = self.svm_services.fake_news_pipeline_svm_classify(details)
        elapsed_time = time.time() - start_time

        # return data
        return_data = {
            'predicted_result': predicted_result,
            'elapsed_time': 'The process take {} seconds'.format(str(elapsed_time))
        }

        # return_data['predicted_result'] = self.naive_bayes_services.naive_bayes_classify_api(details)
        serializer = FakeNewsPredictedResultSerializer(return_data)

        # serializer = ListNewsDetailSerializer(request.data)
        return self.as_success(serializer.data)

    def save_preprocessor_to_csv(self, request, *args, **kwargs):
        status = self.svm_services.write_preprocessor_to_csv()

        return self.as_success(status)

    def accuracy_validate(self, request, *args, **kwargs):
        # Process classify
        start_time = time.time()
        accuracy_result = self.svm_services.fake_news_validate_accuracy()
        elapsed_time = time.time() - start_time

        # return data
        # return data
        return_data = {
            'result': 'The accuracy is {}%'.format(accuracy_result),
            'elapsed_time': 'The process take {} seconds'.format(str(elapsed_time))
        }

        serializer = AccuracySerializer(return_data)

        return self.as_success(serializer.data)
