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


def ngrams(s, n):
    output = []
    for i in range(len(s)-n+1):
        output.append(s[i:i+n])
    return output


def is_acceptable_questions(question, corpus_ngrams):
    question_ngrams = ngrams(question, 3)
    for ngram in question_ngrams:
        if ngram not in corpus_ngrams:
            return False
    return True


def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + " <dirName>")
    sys.exit(0)


if __name__ == "__main__":
    #if len(sys.argv) != 2:
    #    print_usage_and_exit()

    corpus = io.open('../Corpus/questions_with_id/pos.txt').read()
    corpus_ngrams = ngrams(corpus.split(), 3)
    nb_tests = 0.0
    nb_errors = 0.0
    good_question = io.open('eval/filter/good.txt')
    question = []
    for line in good_question:
        row = line.split('\t')
        question.append(row[1])
        if row[6] == '1\n':
            nb_tests += 1
            if not is_acceptable_questions(question, corpus_ngrams):
                nb_errors += 1
            question = []
    print('Precision : ' + str(1 - nb_errors/nb_tests))
    bad_question = io.open('eval/filter/bad.txt')
    question = []
    for line in bad_question:
        row = line.split('\t')
        question.append(row[1])
        if row[6] == '1\n':
            nb_tests += 1
            if is_acceptable_questions(question, corpus_ngrams):
                nb_errors += 1
            question = []
    print('Precision : ' + str(1 - nb_errors/nb_tests))