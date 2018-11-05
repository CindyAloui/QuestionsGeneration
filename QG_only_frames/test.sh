#!/usr/bin/env bash

#python3 generateQuestions.py ../Corpus/corefsCorpus data/QuestionsPatterns_auto out/GeneratedQuestions_auto

python3 generateAnnotatedQuestions.py ../Corpus/corefsCorpus data/QuestionsPatterns_manual out/GeneratedQuestions_manual
