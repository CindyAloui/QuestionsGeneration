import io
import os
import json
from src.questionsGenerator import QuestionsGenerator
from src.frame import Frame, FrameElement
from src.coref import Coref
from random import shuffle


if __name__ == "__main__":
    tmp = ["ok", "non", "truc"]
    sets = powerset(tmp)
    questionsGenerator_auto = QuestionsGenerator("data/QuestionsPatterns_auto")
    questionsGenerator_manual = QuestionsGenerator("data/QuestionsPatterns_manual")
    json_questions_dir = "../Corpus/questions_json/"
    json_dir = "../Corpus/json/"
    natural_questions = {}
    questions = []
    for dir in os.listdir(json_questions_dir):
        dir = os.path.join(json_questions_dir, dir)
        for f in os.listdir(dir):
            file_name = os.path.join(dir, f)
            data = json.load(io.open(file_name))
            id = data["id"]
            lu_index = data["lu_index"]
            if (id, lu_index) not in natural_questions:
                natural_questions[(id, lu_index)] = data
            else:
                for fe in natural_questions[(id, lu_index)]["frame_elements"]:
                    for fe2 in data["frame_elements"]:
                        if fe["name"] == fe2["name"]:
                            fe["questions"] = fe["questions"] + fe2["questions"]
            for fe in data["frame_elements"]:
                for q in fe["questions"]:
                    questions.append(q)
    questions = []
    for key in natural_questions:
        for fe in natural_questions[key]["frame_elements"]:
            for q in fe["questions"]:
                questions.append(q)

    question_index = 0
    for dir in os.listdir(json_dir):
        dir1 = os.path.join(json_dir, dir)
        for f in os.listdir(dir1):
            file_name = os.path.join(dir1, f)
            data = json.load(io.open(file_name))
            for elem in data["annotations"]:
                result_file_name = "out/corpus/" + dir + '/question.' + str(question_index) + '.json'
                question_index += 1
                id = elem["id"]
                lu_index = elem["lu_index"]
                if (id, lu_index) in natural_questions:
                    elem = natural_questions[(id, lu_index)]
                    del natural_questions[(id, lu_index)]
                frame_name = elem["frame"]
                frame = Frame(id, frame_name)
                for fe in elem["frame_elements"]:
                    fe["generated_questions_from_auto_patterns"] = []
                    fe["generated_questions_from_manual_patterns"] = []
                    fe_name = fe["name"]
                    frame.frame_elements[fe_name] = FrameElement(fe_name, None, None, frame.semantic_frame)
                    frame.frame_elements[fe_name].words = fe["text"].split()
                    coref = fe["coref"]["text"]
                    if coref != "":
                        new_coref = Coref(None, None)
                        new_coref.coref = coref.split()
                        frame.frame_elements[fe_name].coref = new_coref
                questions, answers, _ = questionsGenerator_manual.generate(frame, False, patterns_id=True)
                for i in range(len(questions)):
                    answer = answers[i][:-2]
                    for fe in elem["frame_elements"]:
                        fe_text = fe["text"]
                        if fe_text == answer:
                            fe["generated_questions_from_manual_patterns"].append(questions[i])

                questions, answers, _ = questionsGenerator_auto.generate(frame, False, patterns_id=True)
                for i in range(len(questions)):
                    answer = answers[i][:-2]
                    for fe in elem["frame_elements"]:

                        fe_text = fe["text"]
                        if fe_text == answer:
                            fe["generated_questions_from_auto_patterns"].append(questions[i])
                json.dump(elem, io.open(result_file_name, 'w'), indent=4, ensure_ascii=False)

    list_80_file = io.open("out/lists/list_80.txt", "w")
    list_20_file = io.open("out/lists/list_20.txt", "w")
    list_no_natural_questions_file = io.open("out/lists/list_no_natural_questions.txt", "w")
    file_by_text = {}
    text_by_file = {}
    texts = []
    file_dict = {}
    for dir in os.listdir("out/corpus"):
        dir = os.path.join("out/corpus/", dir)
        for file_name in os.listdir(dir):
            data = json.load(io.open(os.path.join(dir, file_name)))
            has_natural_questions = False
            for fe in data["frame_elements"]:
                if fe["questions"]:
                    has_natural_questions = True
            if not has_natural_questions:
                list_no_natural_questions_file.write(file_name + "\n")
            else:
                text = data["id"]
                if text not in file_by_text:
                    file_by_text[text] = []
                file_by_text[text].append(file_name)
                text_by_file[file_name] = text
                file_dict[file_name] = data
                if text not in texts:
                    texts.append(text)

    flag = True
    list_text_in_80 = []
    border = 0
    for _, files in file_by_text.items():
        for file in files:
            data = file_dict[file]
            for fe in data["frame_elements"]:
                border += len(fe["questions"])

    print(border)
    border = int(border * 80 / 100)
    print(border)
    shuffle(texts)
    tmp = 0
    sum = 0
    for text in texts:
        tmp += 1
        for file in file_by_text[text]:
            data = file_dict[file]
            for fe in data["frame_elements"]:
                sum += len(fe["questions"])
        if sum > border:
            print("ok")
            break
        list_text_in_80.append(text)

    nb_questions_80 = 0
    nb_questions_20 = 0

    for text in list_text_in_80:
        for file_name in file_by_text[text]:
            list_80_file.write(file_name + '\n')
            data = file_dict[file_name]
            for fe in data["frame_elements"]:
                nb_questions_80 += len(fe["questions"])
    for text in file_by_text:
        if text not in list_text_in_80:
            for file_name in file_by_text[text]:
                list_20_file.write(file_name + '\n')
                data = file_dict[file_name]
                for fe in data["frame_elements"]:
                    nb_questions_20 += len(fe["questions"])
    print(nb_questions_80)
    print(nb_questions_20)

    # nb_questions_80 = 0
    # nb_questions_20 = 0
    # for i in range(border):
    #     key = list_keys[i]
    #     data = file_by_text[key]
    #     for fe in data["frame_elements"]:
    #         nb_questions_80 += len(fe["questions"])
    # for i in range(border, len(list_keys)):
    #     key = list_keys[i]
    #     data = file_by_text[key]
    #     for fe in data["frame_elements"]:
    #         nb_questions_20 += len(fe["questions"])
