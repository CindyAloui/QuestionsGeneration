# encoding=utf8
import os
import io
import csv
import sys
from frame import Frame
from coref import Coref
reload(sys)
sys.setdefaultencoding('utf8')


######################################################################################################################

class Text :
    def __init__(self, name) :
        self.name = name
        self.frames = {}
        self.corefs = {}
        
    def __str__(self):
        s = 'Text : ' + self.name +  '\nFrames : \n\n'
        for frame in self.frames :
            s += self.frames[frame].__str__()
            s += '\n'
        s += 'Corefs :\n'
        for coref in self.corefs :
            s += str(self.corefs[coref])
        return s
        
    def processRow(self, row):
        for s in row :
            if s.startswith("B:") or  s.startswith("I:") :
                annot = s.split(":")
                index = annot[len(annot) - 1]
                if annot[1] == "COREF-TARGET-INDIRECT" or annot[1] == "COREF-TARGET-DIRECT" :
                    if annot[0] == 'B' :
                        self.corefs[index] = Coref(index, row[3], row[4])
                    if annot[0] == 'I' :
                        self.corefs[index].addWord(row[3], row[4])                    
                if annot[2] == "FE" or annot[2] == "TARGET" :
                    semanticFrame = annot[1]
                    if (index, semanticFrame) not in self.frames :
                        self.frames[index, semanticFrame] = Frame(index, semanticFrame)
                    self.frames[index, semanticFrame].addWord(row, annot)


######################################################################################################################

        
class Corpus:
    def __init__(self, dirName, corpusName) :
        self.name = corpusName
        self.texts = {}
        for fname in os.listdir(dirName):
            f = io.open(os.path.join(dirName, fname), encoding='utf8')
            self.addTexts(f)
          

    def addTexts(self, f) :
        reader = csv.reader(f, delimiter='\t')
        frames = {}
        corefs = {}
        sentence = []
        textName = None
        for row in reader:
            if (len(row) > 2) :
                if row[0] != textName:
                    textName = row[0]
                    self.texts[textName] = Text(textName)
                self.texts[textName].processRow(row)

    
    def __str__(self) :
        s = 'Corpus : ' + self.name + '\n\n'
        for text in self.texts :
            s += str(self.texts[text])
        return s


######################################################################################################################


        
if __name__ == "__main__" :        
    for fname in os.listdir("../../Corpus/corefCorpus"):
        c = Corpus(os.path.join("../../Corpus/corefCorpus", fname), fname)  
        print c
