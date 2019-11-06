# import os
# import spacy
# import re
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from spacy.lang.vi.stop_words import STOP_WORDS
# nlp = spacy.load('vi_spacy_model')
#
#
# def get_stop_words():
#     return STOP_WORDS
#
#
# def sort_coo(coo_matrix):
#     tuples = zip(coo_matrix.col, coo_matrix.data)
#     return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
#
#
# def extract_topn_from_vector(feature_names, sorted_items, topn=10):
#     """get the feature names and tf-idf score of top n items"""
#
#     # use only topn items from vector
#     sorted_items = sorted_items[:topn]
#
#     score_vals = []
#     feature_vals = []
#
#     # word index and corresponding tf-idf score
#     for idx, score in sorted_items:
#         # keep track of feature name and its corresponding score
#         score_vals.append(round(score, 3))
#         feature_vals.append(feature_names[idx])
#
#     # create a tuples of feature,score
#     # results = zip(feature_vals,score_vals)
#     results = {}
#     for idx in range(len(feature_vals)):
#         results[feature_vals[idx]] = score_vals[idx]
#
#     return results
#
#
# def main():
#     docs = list()
#     root_dir = './Train_Full'
#
#     for subdir, dir, files in os.walk(root_dir):
#         for file in files:
#             file_path = subdir + os.sep + file
#             f = open(file_path, "r", encoding='utf16')
#             content = f.read()
#             doc = nlp(content)
#             processed_content = str()
#             for token in doc:
#                 processed_content = processed_content + token.text
#             docs.append(processed_content)
#     stopwords = get_stop_words()
#     cv = CountVectorizer(max_df=0.85, stop_words=stopwords)
#     word_count_vector = cv.fit_transform(docs)
#     print(list(cv.vocabulary_.keys())[:10])
#
#     tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
#     tfidf_transformer.fit(word_count_vector)
#
#     f = open("input.txt", "r", encoding='utf8')
#     test_content = f.read()
#     test_docs = list()
#     test_docs.append(test_content)
#     feature_names = cv.get_feature_names()
#     test_doc = test_docs[0]
#     tf_idf_vector = tfidf_transformer.transform(cv.transform([test_doc]))
#     sorted_items = sort_coo(tf_idf_vector.tocoo())
#     keywords = extract_topn_from_vector(feature_names, sorted_items, 20)
#     for k in keywords:
#         print(k)
#
#
# if __name__ == "__main__":
#     main()

import os
import random
import numpy as np
from spacy.lang.vi.stop_words import STOP_WORDS
import spacy
import heapq

nlp = spacy.load('vi_spacy_model')

SPECIAL_CHARACTER = '0123456789%@$.,=+-!;/()*"&^:#|\n\t\''


class FileReader:
    def __init__(self, file_path, encoder=None):
        self.file_path = file_path
        self.encoder = encoder if encoder is not None else 'utf16'

    def read(self):
        with open(self.file_path, encoding=self.encoder) as f:
            s = f.read()
        return s

    def content(self):
        s = self.read()
        return s


class DataLoader:
    def __init__(self, data_path):
        self.data_path = data_path

    def __get_files(self):
        folders = [self.data_path + folder + '/' for folder in os.listdir(self.data_path)]
        class_titles = os.listdir(self.data_path)
        files = dict()
        for folder, title in zip(folders, class_titles):
            files[title] = [folder + f for f in os.listdir(folder)]
        self.files = files

    def get_json(self):
        self.__get_files()
        data = list()
        for topic in self.files:
            # rand = random.randint(200, 400)
            rand = 3
            index = 0
            for file in self.files[topic]:
                content = FileReader(file_path=file).content()
                data.append({
                    'category': topic,
                    'content': content
                })
                if index == rand:
                    break
                else:
                    index += 1
        return data


class NLP:
    def __init__(self, text=None):
        self.text = text
        self.__set_stopwords()
        self.word_frequency = dict()

    def segmentation(self):
        return nlp(self.text)

    def __set_stopwords(self):
        self.stopwords = list(STOP_WORDS)

    def split_words(self):
        text = self.segmentation()
        string_text = str()
        for word in text:
            if len(word.text) > 1:
                string_text += word.text + ' '
        try:
            return [x.strip(SPECIAL_CHARACTER) for x in string_text.split()]
        except TypeError:
            return list()

    def get_words_feature(self):
        split_words = self.split_words()
        return [word for word in split_words if word not in self.stopwords]

    def get_word_frequency(self):
        tokens = self.get_words_feature()
        for token in tokens:
            if token not in self.word_frequency:
                self.word_frequency[token] = 1
            else:
                self.word_frequency[token] += 1
        return self.word_frequency


if __name__ == "__main__":
    json_train = DataLoader(data_path='./Train_Full/').get_json()
    word_idf_values = dict()
    test_file = open("input.txt", "r", encoding='utf8')
    test_content = test_file.read()
    test_words = NLP(test_content)
    test_words_frequency = test_words.get_word_frequency()
    # print(len(test_words_frequency.keys()))
    for keywords, value in test_words_frequency.items():
        doc_containing_word = 0
        for train in json_train:
            content = train['content']
            n = NLP(content)
            list_word = n.get_words_feature()
            if keywords in list_word:
                doc_containing_word += 1
        word_idf_values[keywords] = np.log(len(json_train)/(1 + doc_containing_word))
    result = list()
    # print(word_idf_values)
    for key in test_words_frequency.keys():
        result.append((key, test_words_frequency[key]/len(test_words_frequency.keys()) * word_idf_values[key]))
    result = sorted(result, key=lambda tup: tup[1])
    for r in result:
        print(r)



    # for train in json_train:
    #     content = train['content']
    #     n = NLP(content)
    #     word_frequency = n.get_word_frequency()
    #     most_freq = heapq.nlargest(20, word_frequency, key=word_frequency.get)
    #     print(most_freq)
    #     word_tf_values = dict()
    #     for token in most_freq:
    #         doc_containing_word = dict()

