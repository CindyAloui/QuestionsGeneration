import sys
import os
import io
from corpus import Corpus
from questionsGenerator import QuestionsGenerator


def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + " <corpusDir> <patternsDir> ")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage_and_exit()

    dirName = sys.argv[1]
    questPatterns = sys.argv[2]

    questionsGenerator = QuestionsGenerator(questPatterns)

    questions_answers_file = io.open('../data/Corpus/GeneratedQuestions/questions_superficial_form.txt', 'w')
    for fname in os.listdir(dirName):
        corpus = Corpus(os.path.join(dirName, fname), fname)
        questions, answers = questionsGenerator.generate_from_corpus(corpus, True)
        for i in range(len(questions)):
            questions_answers_file.write(questions[i] + "\n" + answers[i] + "\n\n")