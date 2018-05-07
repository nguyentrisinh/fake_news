import nltk
import os
from nltk.tokenize import word_tokenize
from pyvi import ViTokenizer
from django.conf import settings


class NaiveBayesServices:
    # get base_dir
    base_dir = settings.BASE_DIR
    file_root = os.path.join(base_dir, 'fake_news_api/assets')

    # initialize empty objects
    stop_words = []
    list_sign = ''

    def __init__(self):
        # Download model for tokenize
        # nltk.download('punkt') # Don't need

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
        return self.stop_words, self.list_sign


