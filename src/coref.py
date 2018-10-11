
class Coref:
    def __init__(self, index):
        self.index = index
        self.mention = []
        self.coref = []
        self.coref_lemmas = []
        
    def add_coref(self, word, lemma):
        self.coref.append(word)
        self.coref_lemmas.append(lemma)

    def add_mention(self, mention):
        self.mention.append(mention)

    def get_string_of_superficial_form(self):
        s = ""
        for word in self.mention:
            s += word + ' '
        s += ' : '
        for word in self.coref:
            s += word + ' '
        return s

    def get_string_of_lemmas(self):
        s = ""
        for word in self.coref_lemmas:
            s += word + ' '
        return s  

    def __str__(self):
        s = self.index + ' : ' + self.get_string_of_superficial_form() + '\n'
        return s
