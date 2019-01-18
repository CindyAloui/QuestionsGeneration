import io
import sys
import json
import os
from src.questions import get_questions_from_file, get_matching_questions, Question
from pyfasttext import FastText
from src.questionsGenerator import QuestionsGenerator
from src.corpus import Corpus
from lxml import etree


def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + " <naturalQuestionsFile> <GeneratedQuestionsFile>")
    sys.exit(0)


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print_usage_and_exit()

    question_type = {}
    qt = {"qui", "où", "quand", "quoi", "autre"}
    qui = ["qui", "contre_qui", "à_qui", "pour_qui", "à_la_place_de_qui", "qui_agent", "qui_agent_également",
           "avec_qui"]
    ou = ["où", "pour_quelle_destination", "vers_où", "d'où", "dans_quelle_direction", "pour_quelle_destination",
          "où_précisément"]
    quand = ["quand", "pour_combien_de_temps", "à_quel_moment", "de_quand", "combien_de_temps", "à_quelle_fréquence",
             "en_combien_de_temps"]
    quoi = ["quoi", "quoi_agent", "contre_quoi", "dans_quoi", "avec_quoi", "quoi_précisément", "de_quoi",
            "dans_quelle_entité"]
    tree = etree.parse("../Corpus/frame_description.xml")
    for fe in tree.xpath("/config/frameList/elem/feList/fe"):
        question = fe.get("question")
        if question in qui:
            question_type[fe.get("value")] = "qui"
        elif question in quoi:
            question_type[fe.get("value")] = "quoi"
        elif question in ou:
            question_type[fe.get("value")] = "où"
        elif question in quand:
            question_type[fe.get("value")] = "quand"
        else:
            question_type[fe.get("value")] = "autre"

    dirName = "../Corpus/corefsCorpus"
    questPatterns = "data/QuestionsPatterns_auto"
    model = FastText('../Corpus/WordEmbeddings/wiki.fr.bin', encoding='utf-8')
    questionsGenerator = QuestionsGenerator(questPatterns)

    type_prediction_file = io.open("data/icsiboost/predictions")
    test_file = io.open("data/icsiboost/questions.test")
    name_file = io.open("data/icsiboost/questions.names")
    lines = name_file.readlines()
    types = []
    line = lines[0].split(", ")
    for t in line:
        types.append(t.replace('\n', '').replace('.', ''))
    natural_questions_by_type = {}
    lines1 = type_prediction_file.readlines()
    lines2 = test_file.readlines()
    type = 'error'
    for i in range(len(lines1)):
        question = lines2[i].split(',')[0]
        line = lines1[i].split()
        for j in range(len(line)):
            if line[j] == '1':
                type = types[j]
                break
        natural_questions_by_type[question.lower()] = type

    questions_with_id = {}
    questions = []
    natural_questions = {}
    questions_by_type = {}
    for fname in os.listdir(dirName):
        print(fname)
        corpus = Corpus(os.path.join(dirName, fname), fname)
        for _, text in corpus.texts.items():
            questions_with_id[text.name] = []
            natural_questions[text.name] = []
            for _, frame in text.frames.items():
                new_questions, new_answers, frame_elements = questionsGenerator.generate(frame, False)
                for i in range(len(new_answers)):
                    q = Question(new_questions[i].lower().split(), new_answers[i][:-1].lower().split(), model)
                    t = question_type[frame_elements[i]]
                    questions_with_id[text.name].append(q)
                    questions.append(q)
                    if t not in questions_by_type:
                        questions_by_type[t] = []
                    questions_by_type[t].append(q)

    dir_name = '../Corpus/questions_json/'
    for dir in os.listdir(dir_name):
        print(dir)
        dir = os.path.join(dir_name, dir)
        for fname in os.listdir(dir):
            file = open(os.path.join(dir, fname))
            data = json.load(file)
            frame = data["elem"]
            id = data["id"]
            for fe in data["frame_elements"]:
                frame_element = fe["name"]
                if fe["coref"]["text"] != "":
                    answer = fe["coref"]["text"] + '.'
                else:
                    answer = fe["text"] + '.'
                for q in fe["questions"]:
                    question = Question(q.lower().replace('#', ' ').replace(',', ' ').split(),
                                        answer.lower().replace('#', ' ').split(), model)
                    natural_questions[id].append(question)

    accurate1 = 0.0
    accurate2 = 0.0
    accurate3 = 0.0
    nbMatchs = 0.0
    test = 0.0
    test3 = 0.0
    #print("Erreur sur les questions suivantes")
    for id in natural_questions:
        for question in natural_questions[id]:
            test += 1
            matchs = get_matching_questions(question, questions_with_id[id])
            flag = True
            for match in matchs:
                if question.answer == match.answer:
                    accurate1 += 1
                    flag = False
                    break

            # if flag:
            #     s = ''
            #     for word in question.question:
            #         s += word + ' '
            #     print("On a apparié :")
            #     print(s)
            #     print("Avec :")
            #     for match in matchs:
            #         s = ''
            #         for word in match.question:
            #             s += word + ' '
            #         print(s)
            #     print("\n")

            matchs = get_matching_questions(question, questions)
            nbMatchs += len(matchs)
            for match in matchs:
                if question.answer == match.answer:
                    accurate2 += 1
                    break
            s = ''
            for word in question.question:
                s += word + ' '
            s = s[0:-1]
            if s in natural_questions_by_type:
                print("ok")
                test3 += 1
                t = natural_questions_by_type[s]
                matchs = get_matching_questions(question, questions_by_type[t])
                for match in matchs:
                    if question.answer == match.answer:
                        accurate3 += 1
                        break
            else:
                print(s)

            # print("Pour l'instant le système1 a une précision de " + str((accurate1/test) * 100) + "%")
            # print("Pour l'instant le système2 a une précision de " + str((accurate2/test) * 100) + "%")
            # print("Le système3 (par type) a une précision de " + str((accurate3 / test3) * 100) + "%")
    print("\n\nLe système1 a une précision de " + str((accurate1 / test) * 100) + "%")
    print("Le système2 a une précision de " + str((accurate2 / test) * 100) + "%")
    print("Le système3 (par type) a une précision de " + str((accurate3 / test3) * 100) + "%")
    print("Match en moyenne : " + str(nbMatchs / test))



#################################################################################################################


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
#
# exit(1)

#################################################################################################################
