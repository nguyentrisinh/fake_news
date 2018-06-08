import nltk
import os
from nltk.tokenize import word_tokenize
from pyvi import ViTokenizer
from django.conf import settings
from numpy import *
from django.db.models import Q
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score
# import array

from crawler_engine.models import NewsDetail


class NaiveBayesServices:
    # get base_dir
    base_dir = settings.BASE_DIR
    file_root = os.path.join(base_dir, 'fake_news_api/assets')

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

    # ---------------------- Function for Naive Bayes Api -------------------------
    def get_training_data(self):
        # ----------------- Training models -----------------------------
        # Get all News exclude 10 first news
        # training_news_query_set = NewsDetail.objects.filter(Q(category='Chinh tri') | Q(category='Suc khoe'))[10:]
        training_news_query_set = NewsDetail.objects.filter(Q(category='Chinh tri') | Q(category='Suc khoe'))

        # List details to train
        db_train_data_set = asarray(list(training_news_query_set.values_list('details', flat=True)))

        # preprocessor training data
        list_train_data_set = [self.preprocessor(detail) for detail in db_train_data_set]

        # List training label
        db_train_labels = asarray(list(training_news_query_set.values_list('category', flat=True)))

        # ---------------------------------------------------------------

        return list_train_data_set, db_train_labels

    def get_list_words(self, list_train_data_set):
        # get set of all words
        list_words = self.create_vocabulary_list(list_train_data_set)

        return list_words

    def get_training_matrix(self, list_words, list_train_data_set ):
        # Get training input for naive bayes algorithm

        # change training data into array number
        file = open(os.path.join(self.file_root, 'training_test.txt'), 'w')
        train_matrix = []
        for train_data_set in list_train_data_set:
            file.write(' '.join(str(x) for x in self.set_of_words_to_vector(list_words, train_data_set)))
            file.write('\n')
            train_matrix.append(self.set_of_words_to_vector(list_words, train_data_set))

        # create array of train_matrix
        train_matrix = array(train_matrix)

        # close file
        file.close()
        # End get training input for naive bayes algorithm

        return train_matrix

    def get_predict_processed_matrix(self, list_words, news_details):
        # preprocessor test data
        list_predict_detail_set = [self.preprocessor(detail) for detail in news_details]

        # change test data into array number
        predict_matrix = []
        for predict_data_set in list_predict_detail_set:
            predict_matrix.append(self.set_of_words_to_vector(list_words, predict_data_set))

        return predict_matrix

    def naive_bayes_classify_api(self, details):
        # Get training data
        list_train_data_set, db_train_labels = self.get_training_data()

        # Get list words
        list_words = self.get_list_words(list_train_data_set)

        # Get training matrix
        train_matrix = self.get_training_matrix(list_words, list_train_data_set)

        # Get matrix of news details that need to predicted classify
        predict_matrix = self.get_predict_processed_matrix(list_words, details)

        # Process Naive Bayes algorithm
        clf = BernoulliNB()
        clf.fit(train_matrix, db_train_labels)
        y_predict = clf.predict(predict_matrix)
        print(y_predict)

        return y_predict
    # ---------------------- End function for Naive Bayes Api -------------------------

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
        filtered_sentence = [word_token for word_token in word_tokens if word_token not in stop_words]

        # Return filtered_sentence
        return filtered_sentence

    def stop_word_list(self):
        # list_details = list(NewsDetail.objects.filter(Q(category='Thời sự') | Q(category='Giáo dục'))
        #                     .values_list('category', flat=True))
        # print(asarray(list_details))
        # print(type(list_details))
        return self.stop_words, self.list_sign

    # This test is base on Liem db to test it structures
    def naive_bayes_classify_test(self):
        # ----------------- Training models -----------------------------
        # Get all News exclude 10 first news
        training_news_query_set = NewsDetail.objects.filter(Q(category='Chinh tri') | Q(category='Suc khoe'))[10:]

        # List details to train
        db_train_data_set = asarray(list(training_news_query_set.values_list('details', flat=True)))

        # preprocessor training data
        list_train_data_set = [self.preprocessor(detail) for detail in db_train_data_set]

        # List training label
        db_train_labels = asarray(list(training_news_query_set.values_list('category', flat=True)))

        # ---------------------------------------------------------------

        # ----------------- Test models ---------------------------------
        # get 10 first news to test naive bayes algorithm
        test_news_query_set = NewsDetail.objects.filter(Q(category='Chinh tri') | Q(category='Suc khoe'))[:10]

        # List details to test
        db_test_data_set = asarray(list(test_news_query_set.values_list('details', flat=True)))

        # preprocessor test data
        list_test_data_set = [self.preprocessor(detail) for detail in db_test_data_set]

        # List test label
        db_test_labels = asarray(list(test_news_query_set.values_list('category', flat=True)))
        # ---------------------------------------------------------------

        # ---------------- Naive Bayes algorithm test -------------------
        # get set of all words
        list_words = self.create_vocabulary_list(list_train_data_set)

        # Get training input for naive bayes algorithm

        # change training data into array number
        file = open(os.path.join(self.file_root, 'training.txt'), 'w')
        train_matrix = []
        for train_data_set in list_train_data_set:
            file.write(' '.join(str(x) for x in self.set_of_words_to_vector(list_words, train_data_set)))
            file.write('\n')
            train_matrix.append(self.set_of_words_to_vector(list_words, train_data_set))

        # create array of train_matrix
        train_matrix = array(train_matrix)

        # close file
        file.close()
        # End get training input for naive bayes algorithm

        # Get test input for naive bayes algorithm

        # change test data into array number
        test_matrix = []
        for test_data_set in list_test_data_set:
            test_matrix.append(self.set_of_words_to_vector(list_words, test_data_set))

        # End get test input for naive bayes algorithm

        # Process Naive Bayes algorithm
        clf = BernoulliNB()
        clf.fit(train_matrix, db_train_labels)
        y_predict = clf.predict(test_matrix)
        print(y_predict)
        # print(db_test_labels)
        # print(test_matrix)
        print('Training size = %d,accuracy = %.2f%%' %
              (train_matrix.shape[0], accuracy_score(db_test_labels, y_predict) * 100))
        # End process Naive Bayes algorithm

        # ---------------------------------------------------------------
        return list_train_data_set, db_train_labels, list_test_data_set, db_test_labels, train_matrix, test_matrix

    # Support function
    @staticmethod
    def create_vocabulary_list(data_set):
        # create empty set
        vocabulary_set = set([])

        for document in data_set:
            # union of the two sets
            vocabulary_set = vocabulary_set | set(document)

        return list(vocabulary_set)

    @staticmethod
    def set_of_words_to_vector(vocabulary_list, input_set):
        return_vector = [0] * len(vocabulary_list)

        for word in input_set:
            if word in vocabulary_list:
                return_vector[vocabulary_list.index(word)] = 1
            else:
                print("the word: %s is not in my Vocabulary!" % word)

        return return_vector



