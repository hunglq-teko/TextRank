import os
import spacy
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from spacy.lang.vi.stop_words import STOP_WORDS
nlp = spacy.load('vi_spacy_model')

def get_stop_words():
    return STOP_WORDS




def main():
    docs = list()
    root_dir = './Train_Full'

    for subdir, dir, files in os.walk(root_dir):
        for file in files:
            file_path = subdir + os.sep + file
            f = open(file_path, "r", encoding='utf16')
            content = f.read()
            doc = nlp(content)
            processed_content = str()
            for token in doc:
                processed_content = processed_content + token.text
            docs.append(processed_content)
    stopwords = get_stop_words()
    cv = CountVectorizer(max_df=0.85, stop_words=stopwords)
    word_count_vector = cv.fit_transform(docs)
    print(list(cv.vocabulary_.keys())[:10])

    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vector)


if __name__ == "__main__":
    main()