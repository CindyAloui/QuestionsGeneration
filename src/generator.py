from rule import Rule
from corpus import Corpus

class QuestionsGenerator :
    def __init__(self) : 
        self.rules = Rule.setOfRules()
        
    def generate(self, frame, corefs) : 
        questions = []
        for rule in self.rules:
            if rule.isApplicable(frame):
                questions = questions + rule.applicate(frame, corefs)
        return questions 

    def __str__(self):
        s = 'Questions Generator with rules :\n'
        for rule in self.rules :
            s += str(rule) + ' ; '
        s += '\n'
        return s
           
#TODO (generateFromCorpus)        
    
if __name__ == "__main__" :                
    g = QuestionsGenerator()
    print g.generate(1,1)
    print g
