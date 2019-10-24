import spacy
from spacy.lang.vi.stop_words import STOP_WORDS

nlp = spacy.load('vi_spacy_model')


def main():
    doc = nlp('Hôm nay tôi đi học ở Hà Nội và tôi rất vui vì điều đó. Trời cũng rất đẹp nữa')
    for token in doc:
        if "_" in token.text:
            print(token)


if __name__ == "__main__":
    main()
