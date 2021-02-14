import spacy

class Parser():

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def noun_chunks(self, sentence):
        dict = {}
        sentence = self.nlp(sentence)
        for chunk in sentence.noun_chunks:
            dict[chunk.root.dep_] = chunk.text 
        return dict
        
    def entities(self, sentence):
        dict = {}
        sentence = self.nlp(sentence)
        for ent in sentence.ents:
            dict[ent.label_] = ent.text
        return dict
        
    def words(self, sentence):
        words = []
        sentence = self.nlp(sentence)
        for token in sentence:
            words.append(str(token))
        return words
        
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
    print(p.entities(sentence))
    
    