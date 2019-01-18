import sys
import os
import io
from lxml import etree
import json

if __name__ == "__main__":
    data_file = io.open("data/icsiboost/questions.data", 'w')
    name_file = io.open("data/icsiboost/questions.names", 'w')
    tree = etree.parse("../Corpus/frame_description.xml")
    question_type = {}
    qt = {"qui", "où", "quand", "quoi", "autre"}
    qui = ["qui", "contre_qui", "à_qui", "pour_qui", "à_la_place_de_qui", "qui_agent", "qui_agent_également", "avec_qui"]
    ou = ["où", "pour_quelle_destination", "vers_où", "d'où", "dans_quelle_direction", "pour_quelle_destination", "où_précisément"]
    quand = ["quand", "pour_combien_de_temps", "à_quel_moment", "de_quand", "combien_de_temps", "à_quelle_fréquence", "en_combien_de_temps"]
    quoi = ["quoi", "quoi_agent", "contre_quoi", "dans_quoi", "avec_quoi", "quoi_précisément", "de_quoi", "dans_quelle_entité"]
    autre = set()
    for fe in tree.xpath("/config/frameList/elem/feList/fe"):
        question = fe.get("question")
        if question in qui:
            question_type[fe.get("value")] = "qui"
        elif question in quoi:
            question_type[fe.get("value")] = "quoi"
        elif question in ou:
            question_type[fe.get("value")] = "où"
        elif question in quand:
            question_type[fe.get("value")] = "quand"
        else:
            question_type[fe.get("value")] = "autre"
            autre.add(question)
    for question in autre:
        print(question)
    for question in qt:
        name_file.write(question + ', ')
    name_file.write(('.\n'))
    dir_name = '../Corpus/questions_json/'
    questions = {}
    for dir in os.listdir(dir_name):
        dir = os.path.join(dir_name, dir)
        for fname in os.listdir(dir):
            file = open(os.path.join(dir, fname))
            data = json.load(file)
            frame = data["elem"]
            for fe in data["frame_elements"]:
                frame_element = fe["name"]
                for q in fe["questions"]:
                    q = q.replace(',', ' ')
                    data_file.write(q + ', ' + question_type[frame_element] + '.\n')
