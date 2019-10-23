import KeyWordExtract

def main():
    text = '''Of the original nine subspecies of tigers, three have become extinct in the last 80 years; an average of one every 20 years. It has been predicted all tigers may become extinct in the wild within the next decade. Poaching, habitat loss and fragmentation have reduced the global population of tigers from over 100,000 in the 1900′s, to less than 4,000 in the 1970′s.

Today, four of the remaining subspecies of tigers are considered endangered by the IUCN, while two of the subspecies are considered “critically” endangered. The total number of all the wild populations of the six remaining subspecies of tigers (Bengal, Indochinese, Malayan, Siberian, South China, and Sumatran) is estimated to be between 3,000 – 3,600 tigers.'''
    tr4w = KeyWordExtract.TextRankForKeyWord()
    tr4w.analyze(text, candidate_pos=['NOUN', 'PROPN'], window_size=4, lower=False)
    tr4w.get_keywords(10)


if __name__ == "__main__":
    main()
