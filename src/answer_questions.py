import json
import os
import io


def get_questions_and_answers_from_json(dir_name):
    questions = []
    answers = []
    for dir in os.listdir(dir_name):
        for file in os.listdir(dir_name + "/" + dir):
            json_file_name = dir_name + '/' + dir + '/' + file
            f = io.open(json_file_name, "r", encoding='utf8')
            data = json.load(f)
            data = data["annotations"]
            for annot in data:
                for fe in annot['frame_elements']:
                    new_questions = fe["questions"]
                    new_answers = []
                    for i in range(len(new_questions)):
                        new_answers.append(fe["text"])
                    questions = questions + new_questions
                    answers = answers + new_answers
    return questions, answers


if __name__ == "__main__":
    json_dir_name = "../data/Corpus/json_questions"
    questions, answers = get_questions_and_answers_from_json(json_dir_name)

    print(questions)
    print(answers)
