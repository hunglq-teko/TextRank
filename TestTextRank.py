import numpy as np
import spacy

def main():
    # g = [[0, 0, 0, 0], [0, 0, 0, 0], [1, 0.5, 0, 0], [0, 0.5, 0, 0]]
    #
    # g = np.array(g)
    # pr = np.array([1, 1, 1, 1])
    # d = 0.85
    #
    # for _ in range(10):
    #     pr = 0.15 + 0.85 * np.dot(g, pr)
    #     print(iter)
    #     print(pr)



    nlp = spacy.load('en_core_web_sm')

    content = '''The Wandering Earth, described as China’s first big-budget science fiction thriller, quietly made it onto screens at AMC theaters in North America this weekend, and it shows a new side of Chinese filmmaking — one focused toward futuristic spectacles rather than China’s traditionally grand, massive historical epics. At the same time, The Wandering Earth feels like a throwback to a few familiar eras of American filmmaking. While the film’s cast, setting, and tone are all Chinese, longtime science fiction fans are going to see a lot on the screen that reminds them of other movies, for better or worse.'''

    doc = nlp(content)

    candidate_pos = ['NOUN', 'PROPN', 'VERB']
    sentences = list()

    for sent in doc.sents:
        selected_words = list()
        for token in sent:
            if token.pos_ in candidate_pos and token.is_stop is False:
                selected_words.append(token)
        sentences.append(selected_words)

    for sent in sentences:
        print(sent)


if __name__ == "__main__":
    main()
