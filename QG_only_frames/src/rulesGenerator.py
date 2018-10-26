import io
import os
from lxml import etree


def get_question(answer, frame, tgv):
    answer_name = answer.get('value')
    question = answer.get('question')
    if question == "qui_agent":
        question = "qui"
    question += ' ' + tgv
    for fe_list in frame:
        for fe in fe_list:
            if fe.get('value') == answer_name:
                continue
            question += ' [ $' + fe.get('value') + " ]"
    question += ' ?\n$' + answer_name + ' .'
    return question


class RulesGenerator:
    def __init__(self, descriptor_file_name, dir_name):
        self.descriptor = etree.parse(descriptor_file_name)
        self.dir_name = dir_name

    def generate_and_write(self):
        for frame in self.descriptor.xpath("/config/frameList/frame"):
            frame_name = frame.get("name")
            file = io.open(self.dir_name + "/" + frame_name + ".rules", "w", encoding='utf8')
            frame_tgv = frame.get("tgv")
            frame_tgv = frame_tgv.split(',')
            for tgv in frame_tgv:
                for fe_list in frame:
                    for fe in fe_list:
                        question = get_question(fe, frame, tgv)
                        file.write(question + "\n\n")