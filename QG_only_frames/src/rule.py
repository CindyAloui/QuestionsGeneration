# encoding=utf8

from itertools import chain, combinations
from src.lemmatizer import get_lemma_of

def powerset(iterable):
    """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def get_frame_element(frame_element):
    if frame_element.coref and frame_element.coref.mention == frame_element.words and \
            frame_element.get_string_of_coref() != '':
        return frame_element.get_string_of_coref()
    fe = frame_element.get_string_of_superficial_form()
    if fe == 'on ' or fe == 'il ' or fe == 'elle ':
        return ''
    return frame_element.get_string_of_superficial_form()


def get_frame_element_with_annot(frame_element):
    if frame_element.coref and frame_element.coref.mention == frame_element.words and \
            frame_element.get_string_of_coref() != '':
        s = frame_element.get_string_of_coref()
    else:
        s = frame_element.get_string_of_superficial_form()
    result = ''
    s = s.split()
    result += s[0] + '\t' + 'B:' + frame_element.frame + ':FE:' + frame_element.name + '\n'
    for i in range(1, len(s)):
        result += s[i] + '\t' + 'I:' + frame_element.frame + ':FE:' + frame_element.name + '\n'
    return result


class Rule:
    def __init__(self, frame_name, question, answer):
        self.question = question
        self.answer = answer
        self.frame_name = frame_name
        self.options = []
        self.mandatory = []
        self.answer_fe = None
        optional = False
        for word in question:
            if word == '[':
                optional = True
            elif word == ']':
                optional = False
            elif word[0] == '$':
                if optional:
                    self.options.append(word[1:])
                else:
                    self.mandatory.append(word[1:])
                self.answer_fe = word[1:]
        for word in answer:
            if word == '[':
                optional = True
            elif word == ']':
                optional = False
            elif word[0] == '$':
                if optional:
                    self.options.append(word[1:])
                else:
                    self.mandatory.append(word[1:])

    def is_applicable(self, frame, mandatory):
        if self.frame_name != frame.semantic_frame:
            return False
        for m in mandatory:
            if m not in frame.frame_elements:
                return False
            if get_frame_element(frame.frame_elements[m]) == '':
                return False
        return True

    def get_question(self, frame, options, annotation):
        question = ''
        optional = False
        flag = False
        to_annot = False
        start = False
        tmp = ''
        for word in self.question:
            if word == '[':
                flag = False
                optional = True
                tmp = ''
            elif word == '{':
                to_annot = True
                start = True
            elif word == '}':
                to_annot = False
            elif word == ']':
                optional = False
                if flag:
                    question += tmp
            elif word[0] == '<':
                if optional:
                    tmp += word[1:-1]
                    if annotation:
                        tmp += '\tB:' + frame.name + ':TARGET:' + word[1:-1] + '\n'
                    else:
                        tmp += ' '
                else:
                    question += word[1:-1]
                    if annotation:
                        question += '\tB:' + frame.semantic_frame + ':TARGET:' + get_lemma_of(word[1:-1]) + '\n'
                    else:
                        question += ' '
            elif word[0] != '$':
                if optional:
                    tmp += word
                    if annotation:
                        tmp += '\t_\n'
                    else:
                        tmp += ' '
                else:
                    question += word
                    if annotation:
                        if to_annot:
                            if start:
                                question += '\tB:' + frame.semantic_frame + ':FE:' + self.answer_fe + '\n'
                                start = False
                            else:
                                question += '\tI:' + frame.semantic_frame + ':FE:' + self.answer_fe + '\n'
                        else:
                            question += '\t_\n'
                    else:
                        question += ' '
            else:
                frame_element = word[1:]
                if optional:
                    if frame_element in options:
                        flag = True
                        if annotation:
                            tmp += get_frame_element_with_annot(frame.frame_elements[frame_element])
                        else:
                            tmp += get_frame_element(frame.frame_elements[frame_element])

                else:
                    if annotation :
                        question += get_frame_element_with_annot(frame.frame_elements[frame_element])
                    else:
                        question += get_frame_element(frame.frame_elements[frame_element])
        return question

    def get_answer(self, frame, options, annotation):
        answer = ''
        optional = False
        flag = False
        tmp = ''
        for word in self.answer:
            if word == '[':
                flag = False
                optional = True
                tmp = ''
            elif word == ']':
                optional = False
                if flag:
                    answer += tmp
            elif word[0] != '$':
                if optional:
                    tmp += word + ' '
                else:
                    answer += word + ' '
            else:
                frame_element = word[1:]
                if optional:
                    if frame_element in options:
                        flag = True
                        tmp += get_frame_element(frame.frame_elements[frame_element])
                else:
                    answer += get_frame_element(frame.frame_elements[frame_element])
        return answer

    def apply(self, frame, annotation):
        questions = []
        answers = []
        if not self.is_applicable(frame, self.mandatory):
            return questions, answers
        for options in powerset(self.options):
            if not self.is_applicable(frame, options):
                continue
            new_question = self.get_question(frame, options, annotation)
            new_answer = self.get_answer(frame, options, annotation)
            if len(new_question.split()) <= 25:
                questions.append(new_question)
                answers.append(new_answer)
        return questions, answers

    def __str__(self):
        s = "Question applicable à la frame : " + self.frame_name + '\nQuestion : '
        for word in self.question:
            s += word + ' '
        s += '\nRéponse : '
        for word in self.answer:
            s += word + ' '
        return s
