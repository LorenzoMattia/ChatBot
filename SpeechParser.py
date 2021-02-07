import spacy

class Parser():
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def parse(self, sentence):
        dict = {}
        sentence = self.nlp(sentence)
        for token in sentence:
            print(token.text, token.dep_, token.head.text, token.head.pos_,
                    [child for child in token.children])
            print('\n')
            dict[token.dep_] = token.text
        return dict