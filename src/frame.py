class FrameElement :
    def __init__(self, name, mention) :
        self.name = name
        self.words = []
        self.lemmas = []
        if mention == "TARGET" :
            self.mention = True
        else : 
            self.mention = False
            
    def isAMention(self) :
        return self.mention

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
        
    def __str__(self) :
        s = self.name + ' : ' + self.getStringOfSuperficialForm() + '\n'     
        return s

######################################################################################################################

             
class Frame :
    def __init__(self, index, semanticFrame) :
        self.semanticFrame = semanticFrame
        self.index = index
        self.frameElements = {}
        
    def addWord(self, row, annot) :
        if annot[0] == "B" :
            self.frameElements[annot[3]] = FrameElement(annot[3], annot[2])
        self.frameElements[annot[3]].addWord(row[3], row[4])
        
    def __str__(self):
        s = self.semanticFrame + ', ' + self.index + ' : \n'
        for key in self.frameElements :
            s += str(self.frameElements[key])
        s += '\n'
        return s


######################################################################################################################
