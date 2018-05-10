
from test_stop_words import preprocessor
from db import Connection
from numpy import *
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score


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
db_train_data_set = squeeze(asarray(connection.query("SELECT details FROM public.crawler_engine_newsdetail where category='Chinh tri' or category='Suc khoe' offset 10")))

#preprocessor du lieu train
list_train_data_set = [preprocessor(x) for x in db_train_data_set]

#lay du lieu labels
db_train_labels = squeeze(asarray(connection.query("SELECT category FROM public.crawler_engine_newsdetail where category='Chinh tri' or category='Suc khoe' offset 10")))

#Lay du lieu test
db_test_data_set = squeeze(asarray(connection.query("SELECT details FROM public.crawler_engine_newsdetail where category='Chinh tri' or category='Suc khoe' limit 10")))

#preprocessor du lieu test
list_test_data_set = [preprocessor(x) for x in db_test_data_set]

#lay du lieu labels
db_test_labels = squeeze(asarray(connection.query("SELECT category FROM public.crawler_engine_newsdetail where category='Chinh tri' or category='Suc khoe' limit 10")))

# print(type(connection.query("SELECT details FROM public.crawler_engine_newsdetail where category='Chinh tri' or category='Suc khoe' offset 10")))
# print(connection.query("SELECT title FROM public.crawler_engine_newsdetail where category='Chinh tri' or category='Suc khoe' offset 10"))
# print(asarray(connection.query("SELECT title FROM public.crawler_engine_newsdetail where category='Chinh tri' or category='Suc khoe' offset 10")))
# print(squeeze(asarray(connection.query("SELECT title FROM public.crawler_engine_newsdetail where category='Chinh tri' or category='Suc khoe' offset 10"))))

connection.close()

# lay set cua tat ca cac tu
list_words = createVocabList(list_train_data_set)

# chuyen du lieu train sang so

file = open('training.txt', 'w')
train_mat=[]
for x in list_train_data_set:
    file.write(' '.join(str(x) for x in setOfWords2Vec(list_words, x)))
    file.write('\n')
    train_mat.append(setOfWords2Vec(list_words, x))
train_mat = array(train_mat)
file.close()

# chuyen du lieu test sang so
test_mat =[]
for x in list_test_data_set:
    test_mat.append(setOfWords2Vec(list_words,x))

# thuc hien thuat
clf = BernoulliNB()
clf.fit(train_mat, db_train_labels)
y_pred = clf.predict(test_mat)
print(y_pred)
print(db_test_labels)
print(test_mat)
print('Training size = %d,accuracy = %.2f%%' % \
      (train_mat.shape[0],accuracy_score(db_test_labels, y_pred)*100))




