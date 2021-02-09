import spacy

class Parser():
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    def parse(self, sentence):
        dict = {}
        parents2children = {}
        labels = {}
        sentence = self.nlp(sentence)
        for token in sentence:
            print(token.text, token.dep_, token.head.text, token.head.pos_,
                    [child for child in token.children])
            print('\n')
            parents2children[str(token)] = [child for child in token.children]
            dict[token.dep_] = token.text
            
        return dict, parents2children
        
    
if __name__ == '__main__':
    sentence = input()
    p = Parser()
    p.parse(sentence)
    