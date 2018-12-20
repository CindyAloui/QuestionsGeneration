import io
import os
import json
from src.questionsGenerator import QuestionsGenerator
from src.frame import Frame, FrameElement
from src.coref import Coref

if __name__ == "__main__":
    questionsGenerator_auto = QuestionsGenerator("data/QuestionsPatterns_auto")
    questionsGenerator_manual = QuestionsGenerator("data/QuestionsPatterns_manual")
    json_dir = "../Corpus/questions_json/"
    result_dir = "out/questions_json"
    for dir in os.listdir(json_dir):
        dir1 = os.path.join(json_dir, dir)
        dir2 = os.path.join(result_dir, dir)
        for f in os.listdir(dir1):
            input_file_name = os.path.join(dir1, f)
            result_file_name = os.path.join(dir2, f)
            data = json.load(io.open(input_file_name))
            id = data["id"]
            frame_name = data["frame"]
            frame = Frame(id, frame_name)
            for fe in data["frame_elements"]:
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

            questions, answers = questionsGenerator_manual.generate(frame, False)
            for i in range(len(questions)):
                answer = answers[i][:-2]
                for fe in data["frame_elements"]:
                    fe_text = fe["text"]
                    if fe_text == answer:
                        fe["generated_questions_from_manual_patterns"].append(questions[i])

            questions, answers = questionsGenerator_auto.generate(frame, False)
            for i in range(len(questions)):
                answer = answers[i][:-2]
                for fe in data["frame_elements"]:
                    fe_text = fe["text"]
                    if fe_text == answer:
                        fe["generated_questions_from_auto_patterns"].append(questions[i])
            json.dump(data, io.open(result_file_name, 'w'), indent=4, ensure_ascii=False)