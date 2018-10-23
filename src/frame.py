class FrameElement:
    def __init__(self, name, mention, index):
        self.name = name
        self.index = index
        self.words = []
        self.lemmas = []
        self.coref = None
        if mention == "TARGET":
            self.mention = True
        else:
            self.mention = False

    def is_a_mention(self):
        return self.mention

    def add_word(self, word, lemma):
        self.words.append(word)
        self.lemmas.append(lemma)

    def get_string_of_superficial_form(self):
        s = ""
        for word in self.words:
            s += word + ' '
        return s

    def get_string_of_lemmas(self):
        s = ""
        for word in self.lemmas:
            s += word + ' '
        return s

    def get_string_of_coref(self):
        if not self.coref:
            return ''
        mention = ''
        coref = ''
        frame_element = ''
        for word in self.words:
            frame_element += word + ' '
        for word in self.coref.mention:
            mention += word + ' '
        for word in self.coref.coref:
            coref += word + ' '
        return frame_element.replace(mention, coref)

    def resolve_corefs(self, corefs):
        if self.index in corefs:
            self.coref = corefs[self.index]

    def __str__(self):
        s = self.name + ' : ' + self.get_string_of_superficial_form() + '\n'
        return s


######################################################################################################################


class Frame:
    def __init__(self, index, semantic_frame):
        self.semantic_frame = semantic_frame
        self.index = index
        self.frame_elements = {}

    def add_word(self, row, annot):
        if annot[0] == "B":
            self.frame_elements[annot[3]] = FrameElement(annot[3], annot[2], row[1])
        self.frame_elements[annot[3]].add_word(row[3], row[4])

    def __str__(self):
        s = self.semantic_frame + ', ' + self.index + ' : \n'
        for key in self.frame_elements:
            s += str(self.frame_elements[key])
        s += '\n'
        return s

    def resolve_corefs(self, corefs):
        for _, frame_element in self.frame_elements.items():
            frame_element.resolve_corefs(corefs)
