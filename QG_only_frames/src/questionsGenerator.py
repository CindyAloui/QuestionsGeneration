# encoding=utf8
import io
import os
from src.rule import Rule


class QuestionsGenerator:
    def __init__(self, dir_name):
        self.rules = []
        for fname in os.listdir(dir_name):
            frame_name = fname[:-6]
            f = io.open(os.path.join(dir_name, fname), encoding='utf8')
            lines = f.readlines()
            i = 0
            rule_name = None
            while i < len(lines):
                line = lines[i]
                if not line.strip():
                    i += 1
                    continue
                if '#Pattern' in line:
                    rule_name = line[1:-1]
                    i += 1
                    continue
                question = line.split()
                if question[0] != '{' and '{' in question[0]:
                    print(line)
                answer = lines[i + 1].split()
                self.rules.append(Rule(frame_name, question, answer, rule_name))
                rule_name = None
                i += 2

    def generate(self, frame, annotation, patterns_id=False):
        questions = []
        answers = []
        frame_elements = []
        for rule in self.rules:
            new_questions, new_answers, new_frame_elements = rule.apply(frame, annotation, patterns_id=patterns_id)
            questions = questions + new_questions
            answers = answers + new_answers
            frame_elements = frame_elements + new_frame_elements
        return questions, answers, frame_elements


    def __str__(self):
        s = 'Questions Generator with rules :\n'
        for rule in self.rules:
            s += str(rule) + ' ; '
        s += '\n'
        return s

    def generate_from_corpus(self, corpus, display):
        questions = []
        answers = []
        if display:
            print("Corpus : " + corpus.name)
        for _, text in corpus.texts.items():
            for _, frame in text.frames.items():
                new_questions, new_answers = self.generate(frame, False)
                if new_questions and display:
                    print(
                        'Pour la Frame : \n' + str(frame) + 'Nous avons généré les questions_with_id/réponses suivantes :')
                    for i in range(len(new_questions)):
                        print(new_questions[i] + " " + new_answers[i])
                    print("\n")
                questions = questions + new_questions
                answers = answers + new_answers
        return questions, answers

    def generate_annotated_from_corpus(self, corpus, display):
        questions = []
        if display:
            print("Corpus : " + corpus.name)
        for _, text in corpus.texts.items():
            for _, frame in text.frames.items():
                new_questions, _, _ = self.generate(frame, True)
                if new_questions and display:
                    print(
                        'Pour la Frame : \n' + str(frame) + 'Nous avons généré les questions_with_id suivantes :')
                    for i in range(len(new_questions)):
                        print(new_questions[i] + "\n")
                    print("\n")
                questions = questions + new_questions
        return questions
