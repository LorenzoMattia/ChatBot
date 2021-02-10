import json 
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from Bea import Bea
import random
import pickle
import speech_recognition as sr

def chat():
    # load trained model
    model = keras.models.load_model('chat_model')

    # load tokenizer object
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
    max_len = 20
    
    while True:
        understood = True
        print("User: ")

        guess = assistent.hear()
        inp = guess["transcription"]
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])

        method = None 
        try:
            method = getattr(assistent, tag[0])
            print(method)
        except AttributeError:
            understood = False
            assistent.notunderstood()
        if understood:
            method(inp)    

print("Start messaging with the bot (type quit to stop)!")

if __name__ == '__main__':
    with open("intents.json") as file:
        data = json.load(file)
    PROMPT_LIMIT = 5
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    assistent = Bea(recognizer, microphone, PROMPT_LIMIT)
    chat()
    
    
    
    
    
    
    
    
    
    
    
    