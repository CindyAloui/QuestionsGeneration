import numpy
import os
import numpy as np
from sklearn.decomposition import TruncatedSVD

def compute_weight(corpus_dir):
    weight = {}
    nbwords = 0
    for dir in os.listdir(corpus_dir):
        dir = os.path.join(corpus_dir, dir)
        for file in os.listdir(dir):
            file = open(os.path.join(dir, file))
            for line in file:
                line = line.split()
                for word in line:
                    nbwords += 1
                    if word not in weight:
                        weight[word] = 1
                    else:
                        weight[word] += 1
    for word in weight:
        weight[word] = weight[word] / nbwords
    return weight

def compute_pc(X,npc=1):
    """
    Compute the principal components. DO NOT MAKE THE DATA ZERO MEAN!
    :param X: X[i,:] is a data point
    :param npc: number of principal components to remove
    :return: component_[i,:] is the i-th pc
    """
    svd = TruncatedSVD(n_components=npc, n_iter=7, random_state=0)
    svd.fit(X)
    return svd.components_

def remove_pc(X, npc=1):
    """
    Remove the projection on the principal components
    :param X: X[i,:] is a data point
    :param npc: number of principal components to remove
    :return: XX[i, :] is the data point after removing its projection
    """
    pc = compute_pc(X, npc)
    if npc==1:
        XX = X - X.dot(pc.transpose()) * pc
    else:
        XX = X - X.dot(pc.transpose()).dot(pc)
    return XX


weight = compute_weight("../Corpus/textCorpus/")

class Question:
    def get_vector_mean(self, model):
        embedding = None
        for word in self.question:
            if embedding is None:
                embedding = numpy.array(model[word])
            else:
                embedding += numpy.array(model[word])
        return embedding/len(self.question)

    def get_vector_ponderate_mean(self, model):
        embedding = None
        for word in self.question:
            if word not in weight:
                weight[word] = 0
            if embedding is None:
                embedding = (numpy.array(model[word])) * (0.001/(0.001 + weight[word]))
            else:
                embedding += (numpy.array(model[word])) * (0.001/(0.001 + weight[word]))
        embedding = embedding/len(self.question)
        #embedding = remove_pc(np.array(embedding))
        return embedding

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

    def __init__(self, question, answer, model=None):
        self.question = question
        self.answer = answer
        if model != None:
            self.vector = self.get_vector_mean(model)
        else:
            self.vector = None
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

