
class Coref :
    def __init__(self, index, word, lemma) :
        self.index = index
        self.words = [word]
        self.lemmas = [lemma]
        
    def addWord(self, word, lemma) :
        self.words.append(word)
        self.lemmas.append(lemma)

    def getStringOfSuperficialForm(self) :
        s = ""
        for word in self.words :
            s += word + ' '
        return s    

    def getStringOfLemmas(self) :
        s = ""
        for word in self.lemmas :
            s += word + ' '
        return s  

    def __str__ (self) :
        s = self.index + ' : ' + self.getStringOfSuperficialForm() + '\n'
        return s
