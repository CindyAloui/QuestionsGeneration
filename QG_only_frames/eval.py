import io
import sys
from src.questions import get_questions_from_file, get_matching_question


def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + " <naturalQuestionsFile> <GeneratedQuestionsFile>")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage_and_exit()

    natural_questions_file = io.open(sys.argv[1], 'r')
    generated_questions_file = io.open(sys.argv[1], 'r')
    natural_questions = get_questions_from_file(natural_questions_file)
    generated_questions = get_questions_from_file(generated_questions_file)
    accurate = 0.0
    for question in natural_questions:
        match = get_matching_question(question, generated_questions)
        print("Nous avons rattaché la question naturelle : ")
        print(question)
        print("A la question générée :")
        print(match)
        if question.answer == match.answer:
            accurate += 1
    print("Le système a une précision de " + (accurate/len(natural_questions)) * 100 + "%")