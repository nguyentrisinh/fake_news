from pandas import read_csv
from googletrans import Translator

import time

import numpy as np
import csv
def get_csv_headers(filename):
    df_header = np.array([read_csv(filename, nrows=1).columns])
    return df_header
def get_csv_file(filename):
    df_content = read_csv(filename).values
    # return df_content
    return df_content
def get_specified_columns(data,array):
    new_array = data[:, [x for x in range(data.shape[1]) if (x in array)]]
    return new_array

def translate(data):
    return translator.translate(data,dest='vi').text

def write_csv_file(filename,array):
    with open(filename, "wt",encoding='utf8',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(array)




data = get_csv_file('politifact.csv')
new_array = get_specified_columns(data,[1,9,11])

part = 15
length = len(new_array)
items_per_part = int(length / 15)


for k in range(part):
    translator = Translator()
    translated_array = []
    for idx, i in enumerate(new_array[k * items_per_part:k * items_per_part + items_per_part if k!=14 else length]):
        translated_row = []
        # if (idx == 0):
        #     translated_row = i
        # else:
        translated_row.append(translator.translate(i[0], dest='vi').text)
        translated_row.append(translator.translate(i[1], dest='vi').text)
        translated_row.append(1 if i[2] == True else 0)
        translated_array.append(translated_row)
        print(idx, ' ', translated_row)
    write_csv_file('t_p_%d.csv' % k, np.concatenate((get_specified_columns(get_csv_headers('politifact.csv'),[1,9,11]),translated_array), axis=0))




