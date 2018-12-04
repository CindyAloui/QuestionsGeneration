import io
import kenlm

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
            array.append(("good", sentence,  langage_model.score(sentence), pos_model.score(pos), morpho_model.score(morpho)))
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
            array.append(("bad", sentence, langage_model.score(sentence), pos_model.score(pos), morpho_model.score(morpho)))
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

    print("On a enlevé " + str(len(questions_to_delete)) + " questions, dont " + str(nb_bad - len(remnant_bad)) + " questions fausses")
    print("Il reste " + str(len(remnant_bad)) + " questions fausses sur les " + str(nb_bad))
    print("Dans les questions restantes " + str(int(len(remnant_bad) / len(array) * 100)) + "% sont fausses")
    print("Il reste en tout " + str(len(array) - len(questions_to_delete)) + ' questions.')
    #for question in remnant_bad:
    #    print(question)
