import io

if __name__ == "__main__":
    questions_file = io.open('300_questions.txt', encoding='utf-8')
    total = 0
    good_file = io.open('good_questions.txt', 'w', encoding='utf-8')
    good = 0
    bad_file = io.open('bad_questions.txt', 'w', encoding='utf-8')
    bad = 0
    undefined_file = io.open('undefined.txt', 'w', encoding='utf-8')
    undefined = 0
    for question in questions_file:
        if question[0] == 'T':
            good += 1
            good_file.write(question[1:])
            total += 1
        elif question[0] == '?':
            undefined += 1
            undefined_file.write(question[1:])
            total += 1
        elif question[0] == 'F':
            bad += 1
            bad_file.write(question[1:])
            total += 1
    print("Good = " + str(good) + "\nBad = " + str(bad) + "\nUndefined = " + str(undefined) + "\nTotal = " + str(total))
