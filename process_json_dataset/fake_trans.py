from helper.csv_helper import get_csv_file, get_specified_columns, write_csv_file, get_csv_headers
from googletrans import Translator
import numpy as np
from helper.divide_helper import divide_trans


dir = 'dataset/fake'
filename = dir + '/fake.csv'
part = 100
needed_columns = None
translated_file_name = '/t_p_%d.csv'
sort  = np.argsort([0,2,1])


header_array =get_specified_columns(get_csv_headers(filename), needed_columns)
# [:,sort]
data = get_csv_file(filename)
new_array = data
    # get_specified_columns(data, needed_columns)[:]
length = len(new_array)
items_per_part = int(length / part)

# print(new_array)

for k in range(part):
    translator = Translator()
    translated_array = []
    for idx, i in enumerate(new_array[k * items_per_part:k * items_per_part + items_per_part if k != part-1 else length]):

        translated_row = i.copy()
        # print(i)
        # if (i[2].strip().upper() == 'true'.upper() or i[2].strip().upper() == 'false'.upper()):
        # translated_row.append(translator.translate(i[0], dest='vi').text)
        # translated_row.append(translator.translate(i[1], dest='vi').text)
        # translated_row.append(1 if i[2].strip().upper() == 'true'.upper() else 0)
        translated_row[5] = divide_trans(translated_row[5],10)
        translated_array.append(translated_row)
        print(idx, ' ', translated_row)

    write_csv_file(dir + translated_file_name % k,
                   np.concatenate((header_array, translated_array),
                                  axis=0))
