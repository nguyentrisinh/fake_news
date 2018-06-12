from csv_helper import get_csv_file, get_specified_columns, write_csv_file, get_csv_headers
from googletrans import Translator
import numpy as np

# Config
dir = 'snopes'
filename = dir + '/snopes.csv'
part = 85
needed_columns = [2,3]
translated_file_name = '/translated_snopes_%d.csv'
# End Config


data = get_csv_file(filename)
new_array = get_specified_columns(data, needed_columns)
length = len(new_array)
items_per_part = int(length / part)

for k in range(part):
    translator = Translator()
    translated_array = []
    for idx, i in enumerate(new_array[k * items_per_part:k * items_per_part + items_per_part if k != part-1 else length]):
        translated_row = []
        # if (idx == 0):
        #     translated_row = i
        # else:
        translated_row.append(translator.translate(i[0], dest='vi').text)
        translated_row.append(i[1])
        translated_array.append(translated_row)
        print(idx, ' ', translated_row)
    write_csv_file(dir + translated_file_name % k,
                   np.concatenate((get_specified_columns(get_csv_headers(filename), needed_columns), translated_array),
                                  axis=0))
