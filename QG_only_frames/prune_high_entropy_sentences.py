import sys
import io


def get_questions(f):
    questions = []
    new_question = ''
    for line in f:
        new_question += line
        if line[0] == '?':
            questions.append(new_question)
            new_question = ''
    return questions


def get_entropies(f):
    entropies = []
    for line in f:
        line = line.split()
        if len(line) == 3:
            entropies.append(line[2])
    return entropies


def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + " <dirName>")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_usage_and_exit()

    entropies_file = io.open(sys.argv[1] + 'entropies')
    questions_file = io.open(sys.argv[1] + 'annotated_questions.txt')

    questions = get_questions(questions_file)
    entropies = get_entropies(entropies_file)

    result_file = io.open(sys.argv[1] + 'filtered_annotated_questions.txt', 'w')

    n = 0
    for i in range(len(entropies)):
        if float(entropies[i]) < 2:
            n += 1
            result_file.write(questions[i])
    print(n)
