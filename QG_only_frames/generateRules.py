import sys
import os
from src.rulesGenerator import RulesGenerator


if __name__ == "__main__":
    rulesGenerator = RulesGenerator("../Corpus/frame_description.xml", "data/QuestionsPatterns")
    rulesGenerator.generate_and_write()
