# encoding=utf8

from itertools import chain, combinations

# def powerset(seq):
#     if len(seq) <= 1:
#         yield seq
#         yield []
#     else:
#         for item in powerset(seq[1:]):
#             yield [seq[0]] + item
#             yield item

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


class Rule:
    def __init__(self, frame_name, question, answer):
        self.question = question
        self.answer = answer
        self.frame_name = frame_name
        self.options = []
        self.mandatory = []
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
        return True

    def get_frame_element(self, frame_element):
        if frame_element.coref and frame_element.coref.mention == frame_element.words:
            return frame_element.get_string_of_coref()
        return frame_element.get_string_of_superficial_form()

    def get_question(self, frame, options):
        question = ''
        optional = False
        flag = False
        tmp = ''
        for word in self.question:
            if word == '[':
                flag = False
                optional = True
                tmp = ''
            elif word == ']':
                optional = False
                if flag:
                    question += tmp
            elif word[0] != '$':
                if optional:
                    tmp += word + ' '
                else:
                    question += word + ' '
            else:
                frame_element = word[1:]
                if optional:
                    if frame_element in options:
                        flag = True
                        tmp += self.get_frame_element(frame.frame_elements[frame_element])
                else:
                    question += self.get_frame_element(frame.frame_elements[frame_element])
        return question

    def get_answer(self, frame, options):
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
                        tmp += self.get_frame_element(frame.frame_elements[frame_element])
                else:
                    answer += self.get_frame_element(frame.frame_elements[frame_element])
        return answer

    def apply(self, frame):
        questions = []
        answers = []
        if not self.is_applicable(frame, self.mandatory):
            return questions, answers
        for options in powerset(self.options):
            if not self.is_applicable(frame, options):
                continue
            new_question = self.get_question(frame, options)
            new_answer = self.get_answer(frame, options)
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
