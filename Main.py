import KeyWordExtract

import spacy


def main():
    f = open('input.txt', 'r', encoding='utf8')
    text = f.read()
    
    tr4w = KeyWordExtract.TextRankForKeyWord()
    tr4w.analyze(text, candidate_tag=['N', 'Np'], window_size=4, lower=False, stopwords=['con_gái', 'con_trai'])
    tr4w.get_keywords(30)


if __name__ == "__main__":
    main()
