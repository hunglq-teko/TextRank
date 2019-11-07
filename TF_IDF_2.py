import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import random
import numpy as np
from spacy.lang.vi.stop_words import STOP_WORDS
from scipy.sparse import coo_matrix
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
            rand = 50
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
        return [word for word in split_words if word not in self.stopwords and "_" in word]

    def get_word_frequency(self):
        tokens = self.get_words_feature()
        for token in tokens:
            if token not in self.word_frequency:
                self.word_frequency[token] = 1
            else:
                self.word_frequency[token] += 1
        return self.word_frequency


def get_top_n3_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(3,3), max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in
                  vec1.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 5))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


if __name__ == "__main__":
    json_train = DataLoader(data_path='./Train_Full/').get_json()
    corpus = list()
    for train in json_train:
        processed_train = nlp(train['content'])
        tokens = [token for token in processed_train if "_" in token.text]
        temp = [token.text for token in tokens]
        processes_text = ' '.join(temp)
        corpus.append(processes_text)
    cv = CountVectorizer(stop_words=list(STOP_WORDS), max_features=10000, ngram_range=(1, 3),
                         lowercase=False, strip_accents=False)
    X = cv.fit_transform(corpus)
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(X)
    feature_names = cv.get_feature_names()
    test_file = open("input.txt", "r", encoding='utf8')
    test_content = test_file.read()
    test_features = NLP(test_content).get_words_feature()
    doc = ' '.join(test_features)
    # k = cv.transform([doc])
    k = cv.transform([doc])
    print(type(k))
    tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    print(sorted_items)
    keywords = extract_topn_from_vector(feature_names, sorted_items, 50)
    for k in keywords:
        print(k, keywords[k])


    # test_words = ' '.join(NLP(test_content).get_words_feature())
    # word_idf_values = dict()
    # test_file = open("input.txt", "r", encoding='utf8')
    # test_content = test_file.read()
    # test_words = NLP(test_content)
    # test_words_frequency = test_words.get_word_frequency()
    # # print(len(test_words_frequency.keys()))
    # for keywords, value in test_words_frequency.items():
    #     doc_containing_word = 0
    #     for train in json_train:
    #         content = train['content']
    #         n = NLP(content)
    #         list_word = n.get_words_feature()
    #         if keywords in list_word:
    #             doc_containing_word += 1
    #     word_idf_values[keywords] = np.log(len(json_train)/(1 + doc_containing_word))
    # result = list()
    # # print(word_idf_values)
    # for key in test_words_frequency.keys():
    #     result.append((key, test_words_frequency[key]/len(test_words_frequency.keys()) * word_idf_values[key]))
    # result = sorted(result, key=lambda tup: tup[1])
    # for r in result:
    #     print(r)