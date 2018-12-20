#!/usr/bin/env bash

python3 generateRules.py
echo "Rules ok!"
python3 generateQuestions.py ../Corpus/corefsCorpus data/QuestionsPatterns_manual out/GeneratedQuestions_manual
echo "Manual ok"
python3 generateQuestions.py ../Corpus/corefsCorpus data/QuestionsPatterns_auto out/GeneratedQuestions_auto
echo "Auto ok"
#python3 generateAnnotatedQuestions.py ../Corpus/corefsCorpus data/QuestionsPatterns_manual out/GeneratedQuestions_manual

#python3 eval.py ../Corpus/exemplesQuestions/exemplesQuestions.txt out/GeneratedQuestions_auto/question_lemmas.txt