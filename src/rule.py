from abc import ABCMeta, abstractmethod

class Rule:
    __metaclass__ = ABCMeta
    
    name = 'Unnamed rule'
    
    @abstractmethod
    def isApplicable(self, frame):
        pass

    @abstractmethod
    def applicate(self, frame, corefs):
        pass
    
    @staticmethod    
    def setOfRules() :
        rules = []
        rules.append(TestRule())
        return rules
    
    def __str__(self) :
        return self.name
        
class TestRule(Rule) :

    name = 'Test rule'
   
    def isApplicable(self, frame) :
        return True
    
    def applicate(self, frame, corefs) :
        return ["Question?"]
        

