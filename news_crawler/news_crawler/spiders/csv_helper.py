import time
import csv
import numpy as np
from pandas import read_csv


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


def write_csv_file(filename,array):
    with open(filename, "wt", encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(array)
