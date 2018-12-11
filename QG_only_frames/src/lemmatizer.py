import io

lemmas_file = io.open("../Corpus/lexical_units_lemmas.txt")
lemmas = {}
for line in lemmas_file:
    line = line.split()
    lemmas[line[0]] = line[1]


def get_lemma_of(word):
    if word in lemmas:
        return lemmas[word]
    return ''
