import io
import sys
from src.questions import get_questions_from_file, get_matching_questions, Question
from pyfasttext import FastText


def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + " <naturalQuestionsFile> <GeneratedQuestionsFile>")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage_and_exit()

    model = FastText('../Corpus/WordEmbeddings/wiki.fr.bin', encoding='utf-8')

    natural_questions_file = io.open(sys.argv[1], 'r', encoding='utf-8')
    natural_questions = get_questions_from_file(natural_questions_file, model)
    generated_questions_file = io.open(sys.argv[2], 'r', encoding='utf-8')

    #######################
    questions = set()
    lines = generated_questions_file.readlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line[0] == '#' or not line.strip():
            i += 1
            continue
        questions.add(line)
        i += 2
    print(len(questions))
    #############
    generated_questions_file = io.open(sys.argv[2], 'r', encoding='utf-8')
    generated_questions = get_questions_from_file(generated_questions_file, model)
    print(len(generated_questions))
    print(len(natural_questions))
    exit(0)
    generated_questions_by_type = {}
    for question in generated_questions:
        if question.wh_word not in generated_questions_by_type:
            generated_questions_by_type[question.wh_word] = [question]
        else:
            generated_questions_by_type[question.wh_word].append(question)
    accurate = 0.0
    test = 0.0
    for question in natural_questions:
        test += 1
        type = question.wh_word
        matchs = get_matching_questions(question, generated_questions)
        for match in matchs:
            if question.answer == match.answer:
                accurate += 1
                break
        print("Pour l'instant le système a une précision de " + str((accurate/test) * 100) + "%")
    print("Le système a une précision de " + str((accurate/len(natural_questions)) * 100) + "%")
