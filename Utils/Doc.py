import spacy

nlp = spacy.load('vi_spacy_model')

class Doc:

    def __init__(self, file_path):
        f = open(file_path, "r", encoding='utf8')
        if f.mode == "r":
            contents = f.read() 
        self.contents = contents 
        self.sents = nlp(self.contents).sents

def main():
    doc = Doc('E:\TextRank\input.txt')
    print(type(doc.sents))
    for sent in doc.sents:
        print(sent)
        print("")
        print("")
    


if __name__ == '__main__':
    main()