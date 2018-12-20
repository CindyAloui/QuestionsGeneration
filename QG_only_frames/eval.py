import io
import sys
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

    questionsGenerator = QuestionsGenerator(questPatterns)

    questions = {}

    for fname in os.listdir(dirName):
        corpus = Corpus(os.path.join(dirName, fname), fname)
        for _, text in corpus.texts.items():
            questions[text.id] = []


    model = FastText('../Corpus/WordEmbeddings/wiki.fr.bin', encoding='utf-8')

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
