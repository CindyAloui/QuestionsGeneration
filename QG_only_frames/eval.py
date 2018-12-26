import io
import sys
import json
import os
from src.questions import get_questions_from_file, get_matching_questions, Question
from pyfasttext import FastText
from src.questionsGenerator import QuestionsGenerator
from src.corpus import Corpus


def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + " <naturalQuestionsFile> <GeneratedQuestionsFile>")
    sys.exit(0)


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print_usage_and_exit()

    dirName = "../Corpus/corefsCorpus"
    questPatterns = "data/QuestionsPatterns_auto"
    model = FastText('../Corpus/WordEmbeddings/wiki.fr.bin', encoding='utf-8')
    questionsGenerator = QuestionsGenerator(questPatterns)

    questions = {}
    natural_questions = {}
    for fname in os.listdir(dirName):
        print(fname)
        corpus = Corpus(os.path.join(dirName, fname), fname)
        for _, text in corpus.texts.items():
            questions[text.name] = []
            natural_questions[text.name] = []
            for _, frame in text.frames.items():
                new_questions, new_answers = questionsGenerator.generate(frame, False)
                for i in range(len(new_answers)):
                    questions[text.name].append(Question(new_questions[i].lower(), new_answers[i][:-1].lower(), model))

    dir_name = '../Corpus/questions_json/'
    for dir in os.listdir(dir_name):
        print(dir)
        dir = os.path.join(dir_name, dir)
        for fname in os.listdir(dir):
            file = open(os.path.join(dir, fname))
            data = json.load(file)
            frame = data["frame"]
            id = data["id"]
            for fe in data["frame_elements"]:
                frame_element = fe["name"]
                if fe["coref"]["text"] != "":
                    answer = fe["coref"]["text"] + '.'
                else:
                    answer = fe["text"] + '.'
                for q in fe["questions"]:
                    question = Question(q.lower().replace('#', ' '), answer.lower().replace('#', ' '), model)
                    natural_questions[id].append(question)

    accurate = 0.0
    test = 0.0
    for id in natural_questions:
        for question in natural_questions[id]:
            test += 1
            matchs = get_matching_questions(question, questions[id])
            for match in matchs:
                if question.answer == match.answer:
                    accurate += 1
                    break
            flag = True
            for q in questions[id]:
                if question.answer == q.answer:
                    flag = False
            if flag:
                print("\nPROBLEME")
                print(question.answer)
                for q in questions[id]:
                    print(q.answer)
            #print("Pour l'instant le système a une précision de " + str((accurate/test) * 100) + "%")
    print("Le système a une précision de " + str((accurate/test) * 100) + "%")



    # natural_questions_file = io.open(sys.argv[1], 'r', encoding='utf-8')
    # natural_questions = get_questions_from_file(natural_questions_file, model)
    # generated_questions_file = io.open(sys.argv[2], 'r', encoding='utf-8')
    #
    # generated_questions_file = io.open(sys.argv[2], 'r', encoding='utf-8')
    # generated_questions = get_questions_from_file(generated_questions_file, model)
    # generated_questions_by_type = {}
    # for question in generated_questions:
    #     if question.wh_word not in generated_questions_by_type:
    #         generated_questions_by_type[question.wh_word] = [question]
    #     else:
    #         generated_questions_by_type[question.wh_word].append(question)
    # accurate = 0.0
    # test = 0.0
    # for question in natural_questions:
    #     test += 1
    #     type = question.wh_word
    #     matchs = get_matching_questions(question, generated_questions)
    #     for match in matchs:
    #         if question.answer == match.answer:
    #             accurate += 1
    #             break
    #     print("Pour l'instant le système a une précision de " + str((accurate/test) * 100) + "%")
    # print("Le système a une précision de " + str((accurate/len(natural_questions)) * 100) + "%")
