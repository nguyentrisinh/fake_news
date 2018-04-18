from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from pyvi import ViTokenizer, ViPosTagger
nltk.download('punkt')
file_stop_words = open('vietnamese-stopwords.txt',encoding="utf8");
file_sign = open('sign.txt',encoding="utf8") ;
# Doc file

list_stop_words = file_stop_words.read()
list_sign = file_sign.read()

# Chuyen file sang dinh dung dinh dang
# {'a_b','b','c_d'}
stop_words = set(['_'.join(w.split(' ')) for w in list_stop_words.split('\n') ]+list_sign.split('\n'))

file_sign.close()
file_stop_words.close()

def preprocessor(text):
    preprecessor_words = ViTokenizer.tokenize(text)
    word_tokens = word_tokenize(preprecessor_words)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return filtered_sentence
# example_sent = u"Theo yêu cầu của Bộ trưởng Bộ GD-ĐT, ngày 31.3, Thanh tra Bộ phải hoàn thiện báo cáo về kết quả kiểm tra, rà soát gửi Bộ trưởng Bộ GD-ĐT. Đến thời điểm này, Thanh tra Bộ cũng chưa nhận được đơn xin rút của ứng viên Nguyễn Thị Kim Tiến."
# Xu ly word segment truoc khi loai bo stop word
# preprecessor_words = ViTokenizer.tokenize(example_sent)

# Xu ly tach tu
# word_tokens = word_tokenize(preprecessor_words)

# Loai bo stop word
# filtered_sentence = [w for w in word_tokens if not w in stop_words]
# Continue, xu ly nhung dau cau thua nhu dau phay, dau cham ....

# print(filtered_sentence)

