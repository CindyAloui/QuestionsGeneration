# encoding=utf8
import os
import io
import csv
import sys
from frame import addFrames

reload(sys)
sys.setdefaultencoding('utf8')

def getFramesAndCorefsFromFile(f) : 
    reader = csv.reader(f, delimiter='\t')
    frames = {}
    corefs = {}
    sentence = []
    for row in reader:
        if (len(row) > 2) :
            if row[2] == '1' :
                frames = addFrames(frames, sentence)
                sentence = [row]
            else :
                sentence.append(row)
        for s in row :
            if s.startswith("B:") or  s.startswith("I:") :
                annot = s.split(":")
                index = annot[len(annot) - 1]
                if annot[2] == "COREF-TARGET-INDIRECT" or annot[2] == "COREF-TARGET-DIRECT" :
                    if annot[0] == 'B' :
                        correfs[index] = [elem[3]]
                    if annot[0] == 'I' :
                        correfs[index].append(elem[3])                    
    return frames, corefs

class Text :
    def __init__(self, f, name) :
        self.name = name
        self.frames, self.corefs = getFramesAndCorefsFromFile(f)
        
class Corpus:
    def __init__(self, dirName, corpusName) :
        self.name = corpusName
        self.texts = []
        for fname in os.listdir(dirName):
            f = io.open(os.path.join(dirName, fname), encoding='utf8') 
            self.texts.append(Text(f, fname))
            
c = Corpus('../../Corpus/corefCorpus/histwiki/', 'corpus')  
