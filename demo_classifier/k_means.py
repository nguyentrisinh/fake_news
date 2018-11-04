from test_stop_words import preprocessor
from db import Connection
from numpy import *
from sklearn.cluster import KMeans
import collections

n = 2
category = 'Chinh tri'


def createVocabList(dataSet):
    vocabSet = set([])  # create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document)  # union of the two sets
    return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary!" % word)
    return returnVec


def count_occurrences(word, sentence):
    return sentence.lower().split().count(word)


def createList3Times(list):
    counter = collections.Counter(list)
    words = []
    for key in counter:
        value = counter[key]
        if value >= 3:
            words.append(key)
    return words


connection = Connection()
connection.connect()
db_train_data_set = squeeze(asarray(connection.query(
    "SELECT details FROM public.crawler_engine_fakenewstrainingmodel where category='%s'" % category)))

id_train_data_set = squeeze(asarray(connection.query(
    "SELECT id FROM public.crawler_engine_fakenewstrainingmodel where category='%s'" % category)))

list_train_data_set = [preprocessor(x) for x in db_train_data_set]

list_3_times = []

for x in range(len(list_train_data_set)):
    counter = collections.Counter(list_train_data_set[x])
    words = []
    for key in counter:
        value = counter[key]
        if value >= 3:
            words.append(key)
    list_3_times.append(words)

# list_counter_words = [collections.Counter(x) for x in list_train_data_set]
#
# print(list_counter_words)

list_words = createVocabList(list_3_times)

train_mat = []
for x in list_3_times:
    train_mat.append(setOfWords2Vec(list_words, x))
train_mat = array(train_mat)

db = KMeans(n_clusters=n, random_state=0).fit(train_mat)
labels = db.labels_
print(len(labels), ' record')

for i in range(labels.size):
    query = """ UPDATE public.crawler_engine_fakenewstrainingmodel
                    SET type = %s
                    WHERE id = %s"""
    value = (int(labels[i]), int(id_train_data_set[i]))
    connection.update(query, value)

with open('result.txt', 'w') as f:
    for item in labels:
        f.write("%s\n" % item)

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
print(n_clusters_, 'number of cluster')
