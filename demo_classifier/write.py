from db import Connection
from numpy import *
import os

connection = Connection()
connection.connect()

n = 50

for i in range(n):
    query = """ SELECT title, details from public.crawler_engine_fakenewstrainingmodel
                    WHERE type = %s AND category = 'The gioi'""" % (i)
    list_data = connection.query(query)
    print(len(list_data))
    for x in range(len(list_data)):
        filename = 'cluster/type-%s/%s.txt' % (i, x)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w+", encoding='utf8', ) as f:
            # print('%s\n%s' % ((list_data[x])[0], (list_data[x])[1]))
            f.write('%s\n%s' % ((list_data[x])[0], (list_data[x])[1]))
