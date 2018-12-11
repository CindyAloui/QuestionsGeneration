import numpy


class Question:
    def get_vector(self, model):
        embedding = None
        for word in self.question:
            if embedding is None:
                embedding = numpy.array(model[word])
            else:
                embedding += numpy.array(model[word])
        return embedding/len(self.question)

    def get_wh_word(self):
        for word in self.question:
            if word.lower() == 'qui':
                return 'qui'
            if word.lower() == 'quand':
                return 'quand'
            if word.lower() == 'où':
                return 'où'
            if word.lower() == 'comment':
                return 'comment'
            if word.lower() == 'pourquoi':
                return 'pourquoi'
        return 'other'

    def __init__(self, question, answer, model):
        self.question = question
        self.answer = answer
        self.vector = self.get_vector(model)
        self.wh_word = self.get_wh_word()

    def get_distance_from(self, other_question):
        v1 = self.vector
        v2 = other_question.vector
        return numpy.linalg.norm(v2-v1)

    def __str__(self):
        s =''
        for word in self.question:
            s += word + ' '
        s += '\n'
        for word in self.answer:
            s += word + ' '
        return s


def get_questions_from_file(f, model):
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
        questions.append(Question(question, answer, model))
        i += 2
    return questions


def get_matching_questions(natural_question, generated_questions):
    result = []
    m = None
    for question in generated_questions:
        distance = natural_question.get_distance_from(question)
        if m is None or distance < m:
            result = [question]
            m = distance
        elif m == distance:
            result.append(question)
    return result
