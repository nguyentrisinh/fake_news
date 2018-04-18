
from test_stop_words import preprocessor
from db import Connection
from numpy import *
from sklearn.naive_bayes import BernoulliNB


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


connection = Connection()
connection.connect()
#lay du lieu train
db_train_data_set = squeeze(asarray(connection.query("SELECT details FROM public.crawler_engine_newsdetail")))
#preprocessor du lieu train
list_train_data_set = [preprocessor(x) for x in db_train_data_set]

#Lay du lieu test
db_test_data_set = squeeze(asarray(connection.query("SELECT details FROM public.crawler_engine_newsdetail limit 4 offset 434")))
#preprocessor du lieu test
list_test_data_set = [preprocessor(x) for x in db_test_data_set]

#lay du lieu labels
db_train_labels = squeeze(asarray(connection.query("SELECT category FROM public.crawler_engine_newsdetail")))
connection.close()

# lay set cua tat ca cac tu
list_words = createVocabList(list_train_data_set)

# chuyen du lieu train sang so
train_mat=[]
for x in list_train_data_set:
    train_mat.append(setOfWords2Vec(list_words,x))

# chuyen du lieu test sang so
test_mat =[]
for x in list_test_data_set:
    test_mat.append(setOfWords2Vec(list_words,x))

# thuc hien thuat
clf  = BernoulliNB()
clf.fit(train_mat,db_train_labels)
print(test_mat)
print(clf.predict(test_mat))




