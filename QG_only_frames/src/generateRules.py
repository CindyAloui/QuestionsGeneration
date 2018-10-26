import sys
import os
from rulesGenerator import RulesGenerator


if __name__ == "__main__":
    rulesGenerator = RulesGenerator("../data/frame_description.xml", "../data/QuestionsPatterns")
    rulesGenerator.generate_and_write()
