from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django.conf.urls import url
from rest_framework.exceptions import APIException
from rest_framework import status
import datetime
import time

from .api_base import ApiBase
from ..services import DecisionTreeServices
from ..serializers import AccuracySerializer
from crawler_engine.serializers import BaseNewsDetailSerializer, DescriptionSerializer, ListNewsDetailSerializer, \
    PredictedResultSerializer, FakeNewsPredictedResultSerializer


# Create your views here.
class DecisionTreeViewSet(ModelViewSet, ApiBase):
    permission_classes = (AllowAny,)

    decision_tree_services = DecisionTreeServices()

    @classmethod
    def get_router(cls):
        urlpatterns = [
            url(r'stop_word_list/$', cls.as_view({'get': 'stop_word_list'})),
            url(r'preprocessor/$', cls.as_view({'post': 'preprocessor'})),
            url(r'decision_tree_classify_test/$', cls.as_view({'get': 'decision_tree_classify_test'})),
            url(r'accuracy_validate/$', cls.as_view({'get': 'accuracy_validate'})),
            url(r'decision_tree_classify/$', cls.as_view({'post': 'decision_tree_classify'})),
            url(r'fake_news_classify/$', cls.as_view({'post': 'fake_news_classify'})),
            # Save preprocessor to file
            url(r'save_preprocessor_to_file/$', cls.as_view({'get': 'save_preprocessor_to_file'})),
        ]

        return urlpatterns

    def get_serializer_class(self):
        if self.action == 'preprocessor':
            return DescriptionSerializer

        if self.action == 'decision_tree_classify':
            return ListNewsDetailSerializer

        if self.action == 'fake_news_classify':
            return ListNewsDetailSerializer

        return BaseNewsDetailSerializer

    def stop_word_list(self, request, *args, **kwargs):
        stop_word_list, list_sign = self.decision_tree_services.stop_word_list()
        return self.as_success(stop_word_list)

    def preprocessor(self, request, *args, **kwargs):
        news_detail = request.data['details']
        news_preprocess_string = self.decision_tree_services.preprocessor(news_detail)
        return self.as_success(news_preprocess_string)

    def decision_tree_classify_test(self, request, *args, **kwargs):
        start_time = time.time()

        list_train_data_set, db_train_labels, list_test_data_set, db_test_labels, train_matrix, test_matrix \
            = self.decision_tree_services.decision_tree_classify_test()

        elapsed_time = time.time() - start_time

        print('The process take {} seconds'.format(str(elapsed_time)))

        return self.as_success(test_matrix)

    def decision_tree_classify(self, request, *args, **kwargs):
        details = request.data['details']
        data = request.data

        # Process classify
        start_time = time.time()
        predicted_result = self.decision_tree_services.decision_tree_classify_api(details)
        elapsed_time = time.time() - start_time

        # return data
        return_data = {
            'predicted_result': predicted_result,
            'elapsed_time': 'The process take {} seconds'.format(str(elapsed_time))
        }

        # return_data['predicted_result'] = self.decision_tree_services.decision_tree_classify_api(details)
        serializer = PredictedResultSerializer(return_data)

        # serializer = ListNewsDetailSerializer(request.data)
        return self.as_success(serializer.data)

    def fake_news_classify(self, request, *args, **kwargs):
        details = request.data['details']

        # Process classify
        start_time = time.time()
        predicted_result = self.decision_tree_services.fake_news_classify(details)
        elapsed_time = time.time() - start_time

        # return data
        return_data = {
            'predicted_result': predicted_result,
            'elapsed_time': 'The process take {} seconds'.format(str(elapsed_time))
        }

        serializer = FakeNewsPredictedResultSerializer(return_data)

        return self.as_success(serializer.data)

    def save_preprocessor_to_file(self, request, *args, **kwargs):
        self.decision_tree_services.save_preprocessor_to_file()

        return self.as_success('success')

    def accuracy_validate(self, request, *args, **kwargs):
        # Process classify
        start_time = time.time()
        accuracy_result = self.decision_tree_services.fake_news_validate_accuracy()
        elapsed_time = time.time() - start_time

        # return data
        return_data = {
            'result': 'The accuracy is {}%'.format(accuracy_result),
            'elapsed_time': 'The process take {} seconds'.format(str(elapsed_time))
        }

        serializer = AccuracySerializer(return_data)

        return self.as_success(serializer.data)
