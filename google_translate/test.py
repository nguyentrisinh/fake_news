from googletrans import Translator
from csv_helper import get_csv_file, write_csv

raw_data = get_csv_file('politifact.csv')
translator = Translator()
translator.translate().text