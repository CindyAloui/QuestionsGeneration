# encoding=utf8
import io
import os

from rule import Rule


class QuestionsGenerator:
    def __init__(self, dir_name):
        self.rules = []
        for fname in os.listdir(dir_name):
            frame_name = fname[:-6]
            f = io.open(os.path.join(dir_name, fname), encoding='utf8')
            lines = f.readlines()
            i = 0
            while i < len(lines):
                line = lines[i]
                if line[0] == '#':
                    i += 1
                    continue
                question = line.split()
                answer = lines[i + 1].split()
                self.rules.append(Rule(frame_name, question, answer))
                i += 2

    def generate(self, frame, corefs):
        questions = []
        answers = []
        for rule in self.rules:
            new_questions, new_answers = rule.apply(frame)
            questions = questions + new_questions
            answers = answers + new_answers
        return questions, answers

    def __str__(self):
        s = 'Questions Generator with rules :\n'
        for rule in self.rules:
            s += str(rule) + ' ; '
        s += '\n'
        return s

    def generateFromCorpus(self, corpus, display):
        questions = []
        answers = []
        if display:
            print("Corpus : " + corpus.name)
        for _, text in corpus.texts.items():
            for _, frame in text.frames.items():
                new_questions, new_answers = self.generate(frame, text.corefs)
                if new_questions:
                    if display:
                        print(
                            "Pour la Frame : \n" + str(frame) + "Nous avons généré les questions/réponses suivantes :")
                        for i in range(len(new_questions)):
                            print(new_questions[i] + " " + new_answers[i])
                        print("\n")
                questions = questions + new_questions
                answers = answers + new_answers
        return questions, answers