import json
import os
from src.questions import Question
import io

if __name__ == "__main__":
    dir_name = '../Corpus/questions_json/'
    questions = {}
    for dir in os.listdir(dir_name):
        dir = os.path.join(dir_name, dir)
        for fname in os.listdir(dir):
            file = open(os.path.join(dir, fname))
            data = json.load(file)
            frame = data["frame"]
            for fe in data["frame_elements"]:
                frame_element = fe["name"]
                if fe["coref"]["text"] != "":
                    answer = fe["coref"]["text"] + '.'
                else:
                    answer = fe["text"] + '.'
                for q in fe["questions_with_id"]:
                    question = Question(q, answer)
                    if frame not in questions:
                        questions[frame] = [question]
                    else:
                        questions[frame].append(question)
    result_file1 = io.open("data/natural_questions/questions_with_id.txt", "w")
    for type in questions:
        result_file2 = io.open("data/natural_questions/" + type, "w")
        for question in questions[type]:
            result_file2.write(question.question + '\n' + question.answer + '\n\n')
            result_file1.write(question.question + '\n' + question.answer + '\n\n')
