
class Coref:
    def __init__(self, index, word, lemma):
        self.index = index
        self.words = [word]
        self.lemmas = [lemma]
        
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

    def __str__(self):
        s = self.index + ' : ' + self.get_string_of_superficial_form() + '\n'
        return s
