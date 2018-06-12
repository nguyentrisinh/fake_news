from csv_helper import get_csv_file, get_specified_columns, write_csv_file, get_csv_headers
from googletrans import Translator
import numpy as np

dir = 'politifact'
filename = dir + '/politifact.csv'
part = 15
needed_columns = [1,4,9]
translated_file_name = '/t_p_%d.csv'
sort  = np.argsort([0,2,1])


header_array =get_specified_columns(get_csv_headers(filename), needed_columns)[:,sort]
data = get_csv_file(filename)
new_array = get_specified_columns(data, needed_columns)[:,sort]
length = len(new_array)
items_per_part = int(length / part)

for k in range(part):
    translator = Translator()
    translated_array = []
    for idx, i in enumerate(new_array[k * items_per_part:k * items_per_part + items_per_part if k != part-1 else length]):
        translated_row = []
        if (i[2].strip().upper() == 'true'.upper() or i[2].strip().upper() == 'false'.upper()):
            translated_row.append(translator.translate(i[0], dest='vi').text)
            translated_row.append(translator.translate(i[1], dest='vi').text)
            translated_row.append(1 if i[2].strip().upper() == 'true'.upper() else 0)
            translated_array.append(translated_row)
            print(idx, ' ', translated_row)

    write_csv_file(dir + translated_file_name % k,
                   np.concatenate((header_array, translated_array),
                                  axis=0))
