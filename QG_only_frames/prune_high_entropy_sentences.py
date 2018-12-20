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
    array = []
    nb_bad = len(bad_entropies)
    for entropie in good_entropies:
        array.append(("good", entropie))

    for entropie in bad_entropies:
        array.append(("bad", entropie))

    threshold = int((len(array) / 100) * 60)

    array.sort(key=lambda array: array[1])



    questions_to_delete = set()
    for j in range(threshold):
        questions_to_delete.add(array[j])

    remnant_bad = []
    for question in array:
        if question not in questions_to_delete and question[0] == 'bad':
            remnant_bad.append(question[1])
    print("On a retire" + str(len(questions_to_delete)) + " questions, dont " + str(nb_bad - len(remnant_bad)) +
          " questions fausses")
    print("Il reste " + str(len(remnant_bad)) + " questions fausses sur les " + str(nb_bad))
    print("Dans les questions restantes " + str(int(len(remnant_bad) / (len(array) - len(questions_to_delete)) * 100)) + "% sont fausses")
    print("Il reste en tout " + str(len(array) - len(questions_to_delete)) + ' questions.')
