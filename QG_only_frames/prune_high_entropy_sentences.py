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
    # if len(sys.argv) != 2:
    #    print_usage_and_exit()

    good_entropies_file = io.open('eval/filter/good_entropies')
    bad_entropies_file = io.open('eval/filter/bad_entropies')

    good_entropies = get_entropies(good_entropies_file)
    bad_entropies = get_entropies(bad_entropies_file)
    threshold = -10
    good_mean = 0.0
    nb_errors = 0
    nb_tests = 0
    for entropie in good_entropies:
        nb_tests += 1
        if float(entropie) > threshold:
            nb_errors += 1
    print('Precision : ' + str(1 - nb_errors / nb_tests))

    for entropie in bad_entropies:
        nb_tests += 1
        if float(entropie) < threshold:
            nb_errors += 1
    print('Precision : ' + str(1 - nb_errors / nb_tests))
