from lxml import etree
import io

#TODO
def get_wh_words(tree):
    wh_words = []
    for frame in tree.xpath("/config/frameList/frame"):
        for felist in frame:
            for fe in felist:
                wh_word = fe.get("question")
                print(wh_word)
    return wh_words


def get_questions_patterns(questions_filename, xml_filename):
    tree = etree.parse(xml_filename)
    questions = io.open(questions_filename, "r", encoding='utf8')
    wh_words = get_wh_words(tree)


if __name__ == "__main__":
    get_questions_patterns("../data/FQBv1.0/FQB.v1.Deep.conll-like", "../../Corpus/frame_description.xml")
