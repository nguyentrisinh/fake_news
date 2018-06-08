import os
import nltk
import numpy
from django.conf import settings
from sklearn import svm
from nltk.tokenize import word_tokenize
from pyvi import ViTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.datasets import fetch_20newsgroups
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from django.db.models import Q
from numpy import *

from crawler_engine.models import NewsDetail


class SVMServices:
    # Test training data

    # get base_dir
    base_dir = settings.BASE_DIR
    file_root = os.path.join(base_dir, 'fake_news_api/assets')

    # Example for dataset
    twenty_train = fetch_20newsgroups(subset='train', shuffle=True)
    twenty_test = fetch_20newsgroups(subset='test', shuffle=True)

    # initialize empty objects
    stop_words = []
    list_sign = ''

    def __init__(self):
        # Download model for tokenize
        # nltk.download('punkt')  # Don't need

        # Open sign and vietnamese stop words
        file_stop_words = open(os.path.join(self.file_root, 'vietnamese-stopwords.txt'), encoding="utf8")
        file_sign = open(os.path.join(self.file_root, 'sign.txt'), encoding="utf8")

        # Read sign and vietnamese stop words file
        list_stop_words = file_stop_words.read()
        self.list_sign = file_sign.read()

        # Change into right format for preprocessor
        self.stop_words = set(['_'.join(w.split(' ')) for w in list_stop_words.split('\n')] + self.list_sign.split('\n'))

        file_sign.close()
        file_stop_words.close()

    def get_training_data(self):
        # ----------------- Training models -----------------------------
        # Get all News exclude 10 first news
        # training_news_query_set = NewsDetail.objects.filter(Q(category='Chinh tri') | Q(category='Suc khoe'))[10:]
        # training_news_query_set = NewsDetail.objects.filter(Q(category='Chinh tri') | Q(category='Suc khoe'))[20:]
        # training_news_query_set = NewsDetail.objects.filter()[50:]
        training_news_query_set = NewsDetail.objects.filter()

        # List details to train
        db_train_data_set = asarray(list(training_news_query_set.values_list('details', flat=True)))

        # preprocessor training data
        list_train_data_set = [self.preprocessor(detail) for detail in db_train_data_set]

        # List training label
        db_train_labels = asarray(list(training_news_query_set.values_list('category', flat=True)))

        # ---------------------------------------------------------------

        return list_train_data_set, db_train_labels

    def get_test_data(self):
        # test_news_query_set = NewsDetail.objects.filter(Q(category='Chinh tri') | Q(category='Suc khoe'))
        test_news_query_set = NewsDetail.objects.filter()[:50]

        # List details to train
        db_test_data_set = asarray(list(test_news_query_set.values_list('details', flat=True)))

        # preprocessor training data
        list_test_data_set = [self.preprocessor(detail) for detail in db_test_data_set]

        # List training label
        db_test_labels = asarray(list(test_news_query_set.values_list('category', flat=True)))

        # ---------------------------------------------------------------

        return list_test_data_set, db_test_labels

    def stop_word_list(self):
        # list_details = list(NewsDetail.objects.filter(Q(category='Thời sự') | Q(category='Giáo dục'))
        #                     .values_list('category', flat=True))
        # print(asarray(list_details))
        # print(type(list_details))
        return self.stop_words, self.list_sign

    def preprocessor(self, description):
        stop_words, list_sign = self.stop_word_list()

        # Get news description
        news_description = description

        # Replace sign in news_description
        for sign in list_sign:
            news_description = news_description.replace(sign, ' ')

        # Tokenize vietnamese  news_description
        preprocessor_words = ViTokenizer.tokenize(news_description.lower())

        # tokenize nltk preprocessor_words
        word_tokens = word_tokenize(preprocessor_words)

        # filter sentences into words array that not in stop_words
        # filtered_sentence = [word_token for word_token in word_tokens if word_token not in stop_words]
        filtered_sentence = [word_token for word_token in word_tokens if word_token not in stop_words]

        # Return filtered_sentence
        return ' '.join(filtered_sentence)

    def test_simple_svm(self):
        X = [[0, 0], [1, 1], [4, 6], [8, 12], [12, 18]]
        y = [1, 1, 2, 2, 2]

        clf = svm.SVC()
        clf.fit(X, y)

        print(clf.predict([[16, 24], [2, 3], [5, 5]]))
        return 'Test something'

    def test_preprocessor(self):
        test_set = ("The sky is blue.", "The sun is bright.")
        train_set = ('Đây là một đoạn text mẫu', 'bầu trời thì màu xanh', 'mặt trời thì sáng, bầu trời trong xanh. '
                                                                          'bầu trời', 'trường mẫu giáo rất vui')
        train_label = (1, 2, 2, 2,)

        train_preprocessor_array = list()

        for text in train_set:
            text = self.preprocessor(text)
            train_preprocessor_array.append(text)

        train_preprocessor_tuple = tuple(train_preprocessor_array)
        # print(train_preprocessor_tuple)

        count_vectorizer = CountVectorizer(stop_words='english')
        X_train_counts = count_vectorizer.fit_transform(train_preprocessor_tuple)
        print("Vocabulary:", count_vectorizer.vocabulary_)
        # print(X_train_counts)

        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        # print(X_train_tfidf)

        # Preprocessor data test
        test_preprocessor_array = list()

        for text in test_set:
            text = self.preprocessor(text)
            test_preprocessor_array.append(text)

        test_preprocessor_tuple = tuple(test_preprocessor_array)
        # print(test_preprocessor_tuple, 'test_preprocessor_tuple')

        test_count_vectorizer = CountVectorizer(stop_words='english')
        X_test_counts = test_count_vectorizer.fit_transform(test_preprocessor_tuple)
        # print("Vocabulary:", test_count_vectorizer.vocabulary_)
        # print(X_train_counts)

        tfidf_transformer_test = TfidfTransformer()
        X_test_tfidf = tfidf_transformer.fit_transform(X_test_counts)
        # print(X_test_tfidf, 'X_test_tfidf')

        # Test classify
        print(type(X_train_tfidf), X_train_tfidf)
        print(type(X_train_counts), X_train_counts)
        clf = svm.SVC()
        clf.fit(X_train_tfidf, train_label)

        # SVC Predict
        test = clf.predict(X_train_tfidf)
        print(test)

        return 'test'

    def test_pipeline(self):
        train_set = ('Đây là một đoạn text mẫu', 'bầu trời thì màu xanh', 'mặt trời thì sáng, bầu trời trong xanh. '
                                                                          'bầu trời', 'trường mẫu giáo rất vui')

        train_preprocessor_array = list()

        for text in train_set:
            text = self.preprocessor(text)
            train_preprocessor_array.append(text)

        # train_preprocessor_tuple = tuple(train_preprocessor_array)

        text_clf_svm = Pipeline([('vect', CountVectorizer()),
                                 ('tfidf', TfidfTransformer()),
                                 ('clf-svm', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5,
                                                           random_state=42))
                                 ])

        _ = text_clf_svm.fit(self.twenty_train.data, self.twenty_train.target)
        predicted_svm = text_clf_svm.predict(train_preprocessor_array)
        # predicted_svm = text_clf_svm.predict(self.twenty_test.data)
        print(type(self.twenty_train.data))
        print(predicted_svm)

        # print(numpy.mean(predicted_svm == self.twenty_test.target))

        return 'test'

    def test_pipeline_real_classify(self):
        list_train_data_set, db_train_labels = self.get_training_data()

        list_test_data_set, db_test_labels = self.get_test_data()

        # train_preprocessor_tuple = tuple(train_preprocessor_array)

        text_clf_svm = Pipeline([('vect', CountVectorizer()),
                                 ('tfidf', TfidfTransformer()),
                                 ('clf-svm', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5,
                                                           random_state=42))
                                 ])

        _ = text_clf_svm.fit(list_train_data_set, db_train_labels)
        predicted_svm = text_clf_svm.predict(list_test_data_set)
        # predicted_svm = text_clf_svm.predict(self.twenty_test.data)

        print(numpy.mean(predicted_svm == db_test_labels))

        print(predicted_svm)

        return 'test'

    def pipeline_svm_classify(self, news_details):
        list_train_data_set, db_train_labels = self.get_training_data()

        predict_dataset = [self.preprocessor(detail) for detail in news_details]

        text_clf_svm = Pipeline([('vect', CountVectorizer()),
                                 ('tfidf', TfidfTransformer()),
                                 ('clf-svm', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5,
                                                           random_state=42))
                                 ])

        _ = text_clf_svm.fit(list_train_data_set, db_train_labels)

        predicted_svm = text_clf_svm.predict(predict_dataset)
        print(predicted_svm)

        return predicted_svm
