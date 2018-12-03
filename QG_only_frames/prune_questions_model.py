import io
import kenlm

if __name__ == "__main__":
    model = kenlm.LanguageModel('../Corpus/langage_model/model.bin')
    nb_tests = 0.0
    nb_errors = 0.0
    good_question = io.open('eval/filter/good.txt')
    question = ''
    good_mean = 0.0
    for line in good_question:
        row = line.split('\t')
        question += row[1] + ' '
        if row[6] == '1\n':
            nb_tests += 1
            good_mean += model.score(question)
            if model.score(question) < -75:
                nb_errors += 1
            question = ''
    print('Precision : ' + str(1 - nb_errors/nb_tests))
    print('Good mean =' + str(good_mean/nb_tests))
    bad_question = io.open('eval/filter/bad.txt')
    question = ''
    bad_mean = 0.0
    nb_bad = 0
    for line in bad_question:
        row = line.split('\t')
        question += row[1] + ' '
        if row[6] == '1\n':
            nb_tests += 1
            nb_bad += 1
            bad_mean += model.score(question)
            if model.score(question) > -75:
                nb_errors += 1
            question = ''
    print('Precision : ' + str(1 - nb_errors/nb_tests))
    print('Bad mean =' + str(bad_mean/nb_bad))
