import numpy
import fasttext


class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def get_vector(self):
        model = fasttext.load_model('../../Corpus/WordEmbeddings/wiki.fr.bin')
        question = self.question.split()
        embedding = None
        for word in question:
            if not embedding:
                embedding = numpy.array(model[word])
            else:
                embedding += numpy.array(model[word])
        return embedding/len(question)

    def get_distance_from(self, other_question):
        self_vector = self.get_vector()
        other_vector = other_question.get_vector()
        dist = numpy.linalg.norm(self_vector-other_vector)
        return dist


def get_questions_from_file(f):
    lines = f.readlines()
    i = 0
    questions = []
    while i < len(lines):
        line = lines[i]
        if line[0] == '#' or not line.strip():
            i += 1
            continue
        question = line.split()
        answer = lines[i + 1].split()
        questions.append(Question(question, answer))
    return questions


def get_matching_question(natural_question, generated_questions):
    result = None
    m = None
    for question in generated_questions:
        distance = natural_question.get_distance_from(question)
        if not m or distance < m:
            result = question
    return result
