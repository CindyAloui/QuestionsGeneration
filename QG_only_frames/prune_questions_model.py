import io
import kenlm
import matplotlib.pyplot as plt
from scipy.interpolate import spline
import numpy as np

if __name__ == "__main__":
    pos_model = kenlm.LanguageModel('../Corpus/questions/pos_trigram.bin')
    morpho_model = kenlm.LanguageModel('../Corpus/questions/morpho_trigram.bin')
    langage_model = kenlm.LanguageModel('../Corpus/langage_model/trigram_model.bin')

    good_questions = io.open('eval/filter/good.txt')
    pos = ''
    sentence = ''
    morpho = ''
    array = []
    nb_good = 0
    for line in good_questions:
        row = line.split('\t')
        sentence += row[0] + ' '
        pos += row[1] + ' '
        morpho += row[2] + ' '
        if row[6] == '1\n':
            nb_good += 1
            array.append(("good", sentence, langage_model.score(sentence), pos_model.score(pos),
                          morpho_model.score(morpho)))
            pos = ''
            sentence = ''
            morpho = ''

    bad_questions = io.open('eval/filter/bad.txt')
    pos = ''
    sentence = ''
    morpho = ''
    nb_bad = 0
    for line in bad_questions:
        row = line.split('\t')
        sentence += row[0] + ' '
        pos += row[1] + ' '
        morpho += row[2] + ' '
        if row[6] == '1\n':
            nb_bad += 1
            array.append(("bad", sentence, langage_model.score(sentence), pos_model.score(pos),
                          morpho_model.score(morpho)))
            pos = ''
            sentence = ''
            morpho = ''

    questions_to_delete = set()
    for i in range(2, len(array[0])):
        array.sort(key=lambda array: array[i])
        threshold = int((len(array) / 100) * 40)
        for j in range(threshold):
            questions_to_delete.add(array[j])

    remnant_bad = []
    for question in array:
        if question not in questions_to_delete and question[0] == 'bad':
            remnant_bad.append(question[1])

    print("On a enlevé " + str(len(questions_to_delete)) + " questions, dont " + str(
        nb_bad - len(remnant_bad)) + " questions fausses")
    print("Il reste " + str(len(remnant_bad)) + " questions fausses sur les " + str(nb_bad))
    print("Dans les questions restantes " + str(
        int(len(remnant_bad) / (len(array) - len(questions_to_delete)) * 100)) + "% sont fausses")
    print("Il reste en tout " + str(len(array) - len(questions_to_delete)) + ' questions.')

    #    for question in remnant_bad:
    #        print(question)

    # plt.plot([1, 2, 2.5, 4])
    # plt.ylabel('some numbers')
    # plt.show()

    step = 0.1
    i = 2
    plt.subplot(2, 2, 1)
    array.sort(key=lambda array: array[i])
    min = array[0][i]
    max = array[len(array) - 1][i]
    thresholds = []
    precisions = []
    recalls = []
    threshold = min
    while threshold < max:
        true_positive = 0.0
        false_positive = 0.0
        true_negative = 0.0
        false_negative = 0.0
        thresholds.append(threshold)
        for question in array:
            if question[i] < threshold and question[0] == 'bad':
                true_negative += 1
            if question[i] < threshold and question[0] == 'good':
                false_negative += 1
            if question[i] > threshold and question[0] == 'bad':
                false_positive += 1
            if question[i] > threshold and question[0] == 'good':
                true_positive += 1
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        precisions.append(precision)
        recalls.append(recall)
        threshold += step

    list_x_new = np.linspace(min, max, 1000)
    list_y_smooth = spline(thresholds, precisions, list_x_new)
    list_z_smooth = spline(thresholds, recalls, list_x_new)
    plt.plot(list_x_new, list_y_smooth, '-', label='Precision')
    plt.plot(list_x_new, list_z_smooth, '--', label='Recall')
    plt.axis([min, max, 0, 1])
    plt.legend()
    plt.xlabel('Threshold')
    plt.title('Langage Model (3-gram)')

    i = 3
    plt.subplot(2, 2, 2)
    array.sort(key=lambda array: array[i])
    min = array[0][i]
    max = array[len(array) - 1][i]
    thresholds = []
    precisions = []
    recalls = []
    threshold = min
    while threshold < max:
        true_positive = 0.0
        false_positive = 0.0
        true_negative = 0.0
        false_negative = 0.0
        thresholds.append(threshold)
        for question in array:
            if question[i] < threshold and question[0] == 'bad':
                true_negative += 1
            if question[i] < threshold and question[0] == 'good':
                false_negative += 1
            if question[i] > threshold and question[0] == 'bad':
                false_positive += 1
            if question[i] > threshold and question[0] == 'good':
                true_positive += 1
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        precisions.append(precision)
        recalls.append(recall)
        threshold += step

    list_x_new = np.linspace(min, max, 1000)
    list_y_smooth = spline(thresholds, precisions, list_x_new)
    list_z_smooth = spline(thresholds, recalls, list_x_new)
    plt.plot(list_x_new, list_y_smooth, '-', label='Precision')
    plt.plot(list_x_new, list_z_smooth, '--', label='Recall')
    plt.axis([min, max, 0, 1])
    plt.legend()
    plt.xlabel('Threshold')
    plt.title('POS Model (trigram)')

    i = 4
    plt.subplot(2, 2, 3)
    array.sort(key=lambda array: array[i])
    min = array[0][i]
    max = array[len(array) - 1][i]
    thresholds = []
    precisions = []
    recalls = []
    threshold = min
    while threshold < max:
        true_positive = 0.0
        false_positive = 0.0
        true_negative = 0.0
        false_negative = 0.0
        thresholds.append(threshold)
        for question in array:
            if question[i] < threshold and question[0] == 'bad':
                true_negative += 1
            if question[i] < threshold and question[0] == 'good':
                false_negative += 1
            if question[i] > threshold and question[0] == 'bad':
                false_positive += 1
            if question[i] > threshold and question[0] == 'good':
                true_positive += 1
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        precisions.append(precision)
        recalls.append(recall)
        threshold += step

    list_x_new = np.linspace(min, max, 1000)
    list_y_smooth = spline(thresholds, precisions, list_x_new)
    list_z_smooth = spline(thresholds, recalls, list_x_new)
    plt.plot(list_x_new, list_y_smooth, '-', label='Precision')
    plt.plot(list_x_new, list_z_smooth, '--', label='Recall')
    plt.axis([min, max, 0, 1])
    plt.legend()
    plt.xlabel('Threshold')
    plt.title('Morpho Model (trigram)')
    plt.show()
