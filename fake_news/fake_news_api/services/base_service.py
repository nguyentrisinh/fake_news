import os
import numpy as np
import pandas as pd
from django.conf import settings
from numpy import asarray

from crawler_engine.models import NewsDetail, FakeNewsTrainingModel
from crawler_engine.constants import NEWS_STATUS


class BaseService:

    # get base_dir
    base_dir = settings.BASE_DIR
    file_root = os.path.join(base_dir, 'fake_news_api/assets')

    # validate resources path
    validate_resources_path = os.path.join(file_root, 'validate_resources')

    # Fake news validate model
    fake_translated_part_one_name = 't_p_0.csv'

    # fake translated full path
    fake_translated_part_one_path = os.path.join(validate_resources_path, fake_translated_part_one_name)

    def __init__(self):
        pass

    def load_validate_data(self):
        pandas_dataframe = pd.read_csv(self.fake_translated_part_one_path, header=None, encoding='utf-8')

        fake_news_validate_model = pandas_dataframe[5].astype(str).tolist()

        del fake_news_validate_model[0]

        fake_news_validate_labels = [2] * len(fake_news_validate_model)

        # get the first 100 news with status is real news and details is not null
        validate_news_query_set = NewsDetail.objects.filter(status=1).exclude(details='', details__isnull=True)[0:100]

        # List real news details to validate
        db_train_data_set = asarray(list(validate_news_query_set.values_list('details', flat=True)))

        db_validate_label = asarray(list(validate_news_query_set.values_list('status', flat=True)))

        # merge real and fake news
        # details
        # fake_news_validate_model.append(db_train_data_set)
        fake_news_validate_model = np.append(fake_news_validate_model, db_train_data_set)

        # label
        # fake_news_validate_labels.append(db_validate_label)
        fake_news_validate_labels = np.append(fake_news_validate_labels, db_validate_label)

        return fake_news_validate_model, fake_news_validate_labels

    @staticmethod
    def return_result(predicted_result, label_list, training_set=None):
        accuracy = np.round(np.mean(predicted_result == label_list) * 100, decimals=4)

        print(predicted_result)
        if training_set is not None:
            print('Training site = {training_site}'.format(training_site=len(training_set)))

        print('The accuracy is {algorithm_accuracy}%'.format(algorithm_accuracy=accuracy))

        return accuracy


