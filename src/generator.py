# encoding=utf8
import os
import io
from rule import Rule
from corpus import Corpus

class QuestionsGenerator :
    def __init__(self, dirName) : 
        self.rules = []
        for fname in os.listdir(dirName):        
            frameName = fname[:-6]
            f = io.open(os.path.join(dirName, fname), encoding='utf8')
            lines = f.readlines()
            i = 0
            while i < len(lines) :
                line = lines[i]
                if line[0] == '#' :
                    i += 1
                    continue
                question = line.split()
                answer = lines[i+1].split()
                self.rules.append(Rule(frameName, question, answer))
                i += 2


        
        
    def generate(self, frame, corefs) : 
        questions = []
        answers = []
        for rule in self.rules:
            newQuestions, newAnswers = rule.apply(frame, corefs)
            questions = questions + newQuestions
            answers = answers + newAnswers                
        return questions, answers


    def __str__(self):
        s = 'Questions Generator with rules :\n'
        for rule in self.rules :
            s += str(rule) + ' ; '
        s += '\n'
        return s
           
           
    def generateFromCorpus(self, corpus, display) :
        questions = []
        answers = []
        if display :
            print "Corpus :" + corpus.name
        for _, text in corpus.texts.iteritems():
            for _, frame in text.frames.iteritems():
                newQuestions, newAnswers = self.generate(frame, text.corefs)
                if newQuestions :
                    if display :
                        print "Pour la Frame : \n" + str(frame) + "Nous avons généré les questions/réponses suivantes :"
                        for i in range(len(newQuestions)) :
                            print newQuestions[i] + " " + newAnswers[i] + "\n"
                        print "\n"
                questions = questions + newQuestions
                answers = answers + newAnswers
        return questions, answers
        
    
if __name__ == "__main__" :                
    g = QuestionsGenerator()
    print g.generate(1,1)
    print g
