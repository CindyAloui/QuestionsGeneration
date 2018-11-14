import json
import os

if __name__ == "__main__":
    questions = []
    json_dir_name = "../Corpus/json_questions/"
    for dir in os.listdir(json_dir_name):
        for file in os.listdir(json_dir_name + '/' + dir):
            fileName = json_dir_name + dir + '/' + file
            data = json.load(open(fileName))
            for frame in data['annotations']:
                for frame_element in frame['frame_elements']:
                    questions = questions + frame_element["questions"]
    print(questions)
