import io
import kenlm


if __name__ == "__main__":
    threshold = 80
    pos_model = kenlm.LanguageModel('../Corpus/questions_with_id/pos_trigram.bin')
    morpho_model = kenlm.LanguageModel('../Corpus/questions_with_id/morpho_trigram.bin')
    langage_model = kenlm.LanguageModel('../Corpus/langage_model/trigram_model.bin')

    questions_file = io.open('out/GeneratedQuestions_manual/questions_to_filter.txt', 'r', encoding='utf8')
    result_file = io.open('out/GeneratedQuestions_manual/questions_superficial_form_filtered.txt', 'w', encoding='utf8')

    pos = ''
    sentence = ''
    morpho = ''
    array = []
    for line in questions_file:
        row = line.split('\t')
        sentence += row[0] + ' '
        pos += row[1] + ' '
        morpho += row[2] + ' '
        if row[6] == '1\n':
            array.append([sentence, langage_model.score(sentence), pos_model.score(pos), morpho_model.score(morpho)])

    print('ok')
    pos_model = ''
    morpho_model = ''
    langage_model = ''

    array.sort(key=lambda array: array[1])
    mini = array[0][1]
    maxi = array[len(array) - 1][1]
    array.sort(key=lambda array: array[2])
    minj = array[0][2]
    maxj = array[len(array) - 1][2]
    array.sort(key=lambda array: array[3])
    minz = array[0][3]
    maxz = array[len(array) - 1][3]
    threshold_i = mini + (maxi - mini) * (threshold / 100)
    threshold_j = minj + (maxj - minj) * (threshold / 100)
    threshold_z = minz + (maxz - minz) * (threshold / 100)
    for question in array:
        if question[1] > threshold_i and question[2] > threshold_j and question[3] > threshold_z :
            result_file.write(question[0] + '\n')

