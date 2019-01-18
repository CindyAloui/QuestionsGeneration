from lxml import etree
import io

def is_unimportant_word(pos):
    return False


class Question:
    def __init__(self, words, pos, lemmas):
        self.words = words
        self.pos = pos
        self.lemmas = lemmas

    def contains(self, wh_words):
        for wh_word in wh_words:
            wh_word = wh_word.replace("_", " ")
            wh_word = wh_word.split()
            j = 0
            for i in range(len(self.words)):
                if self.words[i] == wh_word[j] or self.lemmas[i] == wh_word[j]:
                    j += 1
                else:
                    j = 0
                if j == len(wh_word):
                    return wh_word
        return None

    def get_pattern(self, wh_word):
        pattern = []
        for i in range(len(self.words)):
            if (self.words[i] in wh_word) or (self.lemmas[i] in wh_word):
                pattern.append(self.words[i])
            elif is_unimportant_word(self.pos[i]):
                pattern.append(self.words[i])
        return pattern


def get_questions(questions_filename):
    f = io.open(questions_filename, "r", encoding='utf8')
    words = None
    pos = None
    lemmas = None
    questions = []
    for row in f:
        tuple = row.split("\t")
        if len(tuple) < 2:
            continue
        if row[0] == "1":
            if words:
                questions.append(Question(words, pos, lemmas))
            words = []
            pos = []
            lemmas = []
        words.append(tuple[1])
        pos.append(tuple[4])
        lemmas.append(tuple[2])
    return questions


def get_wh_words(tree):
    wh_words = set()
    for fe in tree.xpath("/config/frameList/elem/feList/fe"):
        wh_word = fe.get("question")
        wh_words.add(wh_word)
    return wh_words


def get_questions_patterns(questions_filename, xml_filename):
    patterns = []
    tree = etree.parse(xml_filename)
    questions = get_questions(questions_filename)
    wh_words = get_wh_words(tree)
    for question in questions:
        wh_word = question.contains(wh_words)
        if wh_word:
            pattern = question.get_pattern(wh_word)
            patterns.append(pattern)
    return patterns


if __name__ == "__main__":
    question_patterns = get_questions_patterns("../data/FQBv1.0/FQB.v1.Deep.conll-like",
                                               "../../Corpus/frame_description.xml")
