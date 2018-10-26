import json
import os
from src.corpus import Corpus
import io


def add_annotations_from_frame(annot, f, txt_index):
    if len(f.frame_elements) < 3:
        return annot
    new_annot = {'id': txt_index, 'lu_index': f.index, 'frame': f.semantic_frame,
                 'lu': None, 'frame_elements': []}
    for _, frame_element in f.frame_elements.items():
        if frame_element.mention:
            new_annot['lu'] = frame_element.name
            continue
        fe_data = {'name': frame_element.name, 'start_index': frame_element.index,
                   'text': frame_element.get_string_of_superficial_form(),
                   'coref': {"start_index": frame_element.get_start_index_of_coref(),
                    "text": frame_element.get_string_of_coref()},
                   "questions": []}
        new_annot['frame_elements'].append(fe_data)
    annot.append(new_annot)
    return annot


if __name__ == "__main__":

    corpus_dir_name = "../Corpus/corefsCorpus"
    json_dir_name = "../Corpus/json"
    for fname in os.listdir(corpus_dir_name):
        corpus = Corpus(os.path.join(corpus_dir_name, fname), fname)
        json_file_name = os.path.join(json_dir_name, fname) + '/' + corpus.name + ".json"
        outfile = io.open(json_file_name, "w", encoding='utf8')
        annotations = []
        for _, t in corpus.texts.items():
            for _, frame in t.frames.items():
                annotations = add_annotations_from_frame(annotations, frame, t.name)
        data = {'annotations': annotations}
        json_data = json.dump(data, outfile, indent=4, ensure_ascii=False)
