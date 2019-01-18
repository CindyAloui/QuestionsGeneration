import io
import os
import json
from src.questionsGenerator import QuestionsGenerator
from src.frame import Frame, FrameElement
from src.coref import Coref

if __name__ == "__main__":
    questionsGenerator_auto = QuestionsGenerator("data/QuestionsPatterns_auto")
    questionsGenerator_manual = QuestionsGenerator("data/QuestionsPatterns_manual")
    json_questions_dir = "../Corpus/questions_json/"
    json_dir = "../Corpus/json/"
    natural_questions = {}
    for dir in os.listdir(json_questions_dir):
        dir = os.path.join(json_questions_dir, dir)
        for f in os.listdir(dir):
            file_name = os.path.join(dir, f)
            data = json.load(io.open(file_name))
            id = data["id"]
            lu_index = data["lu_index"]
            natural_questions[(id, lu_index)] = data
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
                frame_name = elem["frame"]
                frame = Frame(id, frame_name)
                for fe in elem["frame_elements"]:
                    fe["generated_questions_from_manual_patterns"] = []
                    fe["generated_questions_from_auto_patterns"] = []
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
