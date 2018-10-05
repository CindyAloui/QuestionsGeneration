import sys
import os
import io
from corpus import Corpus
from generator import QuestionsGenerator

def printUsageAndExit() :
    print "Usage: " + sys.argv[0] + " <corpusDir> <patternsDir "
    sys.exit(0)
    
if __name__ == "__main__" :
    if len(sys.argv) != 3 : 
        printUsageAndExit()     
    
    dirName = sys.argv[1]
    questPatterns = sys.argv[2]
    
    questionsGenerator = QuestionsGenerator(questPatterns)

    for fname in os.listdir(dirName):
        corpus = Corpus(os.path.join(dirName, fname), fname)  

    questions, answers = questionsGenerator.generateFromCorpus(corpus, True)
    

