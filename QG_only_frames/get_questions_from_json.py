import json
import os

if __name__ == "__main__":
    questions = []
    json_dir_name = "../Corpus/json_questions/"
    for dir in os.listdir(json_dir_name):
        for file in dir:
            fileName = json_dir_name + dir + '/' + file
            data = json.load(open(fileName))
            for _, frame in data['annotations'].items:
                for _, frame_element in frame['frame_element'].items:
                    questions = questions + frame_element["questions"]
    print(questions)