# encoding=utf8
import csv
import os

from coref import Coref
from frame import Frame


######################################################################################################################


class Text:
    def __init__(self, name):
        self.name = name
        self.frames = {}
        self.corefs = {}
        
    @property
    def __str__(self):
        s = 'Text : ' + self.name + '\nFrames : \n\n'
        for frame in self.frames:
            s += self.frames[frame].__str__
            s += '\n'
        s += 'Corefs :\n'
        for coref in self.corefs:
            s += str(self.corefs[coref])
        return s

    def process_row(self, row):
        for s in row:
            if s.startswith("B:") or s.startswith("I:"):
                annot = s.split(":")
                index = annot[len(annot) - 1]
                if annot[1] == "COREF-TARGET-INDIRECT" or annot[1] == "COREF-TARGET-DIRECT" or annot[1] == "MENTION":
                    if index not in self.corefs:
                        self.corefs[index] = Coref(index)
                    if annot[1] == "COREF-TARGET-INDIRECT" or annot[1] == "COREF-TARGET-DIRECT":
                        self.corefs[index].add_coref(row[3], row[4])
                    else:
                        self.corefs[index].add_mention(row[3])
                if annot[2] == "FE" or annot[2] == "TARGET":
                    semantic_frame = annot[1]
                    if (index, semantic_frame) not in self.frames:
                        self.frames[index, semantic_frame] = Frame(index, semantic_frame)
                    self.frames[index, semantic_frame].add_word(row, annot)

    def resolve_corefs(self):
        for _, frame in self.frames.items():
            frame.resolve_corefs(self.corefs)

######################################################################################################################

        
class Corpus:
    def __init__(self, dir_name, corpus_name):
        self.name = corpus_name
        self.texts = {}
        for f in os.listdir(dir_name):
            f = open(os.path.join(dir_name, f), encoding='utf8')
            self.add_texts(f)

    def add_texts(self, f):
        reader = csv.reader(f, delimiter='\t')
        text_name = None
        for row in reader:
            if len(row) > 2:
                if row[0] != text_name:
                    if text_name:
                        self.texts[text_name].resolve_corefs()
                    text_name = row[0]
                    self.texts[text_name] = Text(text_name)
                self.texts[text_name].process_row(row)

    def __str__(self):
        s = 'Corpus : ' + self.name + '\n\n'
        for text in self.texts:
            s += str(self.texts[text])
        return s


######################################################################################################################
        
if __name__ == "__main__":
    for f in os.listdir("../../Corpus/corefsCorpus"):
        c = Corpus(os.path.join("../../Corpus/corefsCorpus", f), f)
        print(c)
